#!/usr/bin/env python3
"""Assemble an 8.5×8.5\" sRGB flipbook PDF + verdict card.

Primary input (LOCKED): Media/generated/mocks/_FLOW-CURRENT.json
  — single source of truth for current plates. No path guessing.

Legacy: --manifest still accepted for one-off exports.

Output: Output/flipbook-{date}.pdf + Output/flipbook-{date}-verdicts.json
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from io import BytesIO
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


PAGE = 8.5 * inch
DEFAULT_FLOW = Path("Media/generated/mocks/_FLOW-CURRENT.json")


def _register_fonts() -> tuple[str, str]:
    regular = "Helvetica"
    bold = "Helvetica-Bold"
    candidates = [
        (r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\arialbd.ttf"),
        (r"C:\Windows\Fonts\calibri.ttf", r"C:\Windows\Fonts\calibrib.ttf"),
    ]
    for reg, bld in candidates:
        if Path(reg).is_file() and Path(bld).is_file():
            pdfmetrics.registerFont(TTFont("FlipBook", reg))
            pdfmetrics.registerFont(TTFont("FlipBook-Bold", bld))
            return "FlipBook", "FlipBook-Bold"
    return regular, bold


def _to_srgb_jpeg(path: Path, max_side: int = 2550) -> bytes:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    scale = max_side / max(w, h)
    if scale < 1:
        im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
    side = max(im.size)
    canvas_im = Image.new("RGB", (side, side), (250, 246, 238))
    canvas_im.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    if side != max_side:
        canvas_im = canvas_im.resize((max_side, max_side), Image.Resampling.LANCZOS)
    buf = BytesIO()
    canvas_im.save(buf, format="JPEG", quality=92, optimize=True)
    return buf.getvalue()


def _split_wide(path: Path, side: str, max_side: int = 2550) -> bytes:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w >= int(h * 1.6):
        mid = w // 2
        crop = im.crop((0, 0, mid, h) if side == "L" else (mid, 0, w, h))
    else:
        crop = im
    buf0 = BytesIO()
    crop.save(buf0, format="PNG")
    buf0.seek(0)
    crop_im = Image.open(buf0).convert("RGB")
    side_px = max(crop_im.size)
    sq = Image.new("RGB", (side_px, side_px), (250, 246, 238))
    sq.paste(crop_im, ((side_px - crop_im.width) // 2, (side_px - crop_im.height) // 2))
    if side_px != max_side:
        sq = sq.resize((max_side, max_side), Image.Resampling.LANCZOS)
    out = BytesIO()
    sq.save(out, format="JPEG", quality=92, optimize=True)
    return out.getvalue()


def flow_current_to_manifest(flow: dict, root: Path) -> dict:
    """Build flipbook manifest strictly from _FLOW-CURRENT.json plates."""
    plates = flow.get("plates")
    if not isinstance(plates, list) or not plates:
        raise SystemExit("_FLOW-CURRENT.json missing non-empty 'plates' array — refuse to guess.")
    pages = []
    for p in plates:
        pages.append(
            {
                "caption": p.get("caption") or f"{p.get('page','')} · {p.get('beat','')}",
                "path": p.get("path"),
                "beat": p.get("beat"),
                "split": p.get("split"),
                "status": p.get("status"),
                "decided_by": p.get("decided_by"),
                "date": p.get("date"),
            }
        )
    verdicts = flow.get("verdicts") or []
    for v in verdicts:
        if "decided_by" not in v or "date" not in v:
            raise SystemExit(
                f"Verdict missing decided_by/date: {v.get('beat')} — required for reopen in August."
            )
    models = sorted({(p.get("model") or "") for p in plates if p.get("model")})
    return {
        "title": flow.get("title") or "Book Flipbook (from _FLOW-CURRENT)",
        "date": flow.get("updated") or date.today().isoformat(),
        "flow_doc": flow.get("flow_doc", ""),
        "models": " · ".join(m for m in models if m),
        "root": str(root),
        "pages": pages,
        "verdicts": verdicts,
        "source": "_FLOW-CURRENT.json",
    }


def _draw_cover(c: canvas.Canvas, meta: dict, font: str, bold: str) -> None:
    c.setFillColor(HexColor("#F7F1E6"))
    c.rect(0, 0, PAGE, PAGE, fill=1, stroke=0)
    c.setFillColor(HexColor("#2C2C2C"))
    c.setFont(bold, 22)
    c.drawCentredString(PAGE / 2, PAGE - 1.4 * inch, meta.get("title", "Flipbook"))
    c.setFont(font, 12)
    lines = [
        f"Date: {meta.get('date', '')}",
        f"Source: {meta.get('source', 'manifest')}",
        f"Flow doc: {meta.get('flow_doc', '')}",
        f"Models: {meta.get('models', '')}",
        f"Image plates: {meta.get('image_count', 0)}",
        f"PDF pages (excl. cover+verdict): {meta.get('content_pages', 0)}",
        "",
        "Review only — not Lulu print finals.",
        "sRGB · 8.5×8.5 · full bleed · no crop marks",
    ]
    y = PAGE - 2.2 * inch
    for line in lines:
        c.drawCentredString(PAGE / 2, y, line)
        y -= 20
    c.showPage()


def _draw_image_page(c: canvas.Canvas, jpeg: bytes, caption: str, font: str) -> None:
    c.setFillColor(white)
    c.rect(0, 0, PAGE, PAGE, fill=1, stroke=0)
    c.drawImage(ImageReader(BytesIO(jpeg)), 0, 0, width=PAGE, height=PAGE, preserveAspectRatio=True, anchor="c")
    c.setFillColor(HexColor("#2C2C2C"))
    c.rect(0, 0, PAGE, 0.38 * inch, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(font, 9)
    c.drawString(0.2 * inch, 0.14 * inch, caption[:110])
    c.showPage()


def _draw_placeholder(c: canvas.Canvas, caption: str, font: str, bold: str) -> None:
    c.setFillColor(HexColor("#F0EAE0"))
    c.rect(0, 0, PAGE, PAGE, fill=1, stroke=0)
    c.setFillColor(HexColor("#6A5F55"))
    c.setFont(bold, 16)
    c.drawCentredString(PAGE / 2, PAGE / 2 + 20, "PENDING — no plate yet")
    c.setFont(font, 11)
    c.drawCentredString(PAGE / 2, PAGE / 2 - 10, caption[:100])
    c.showPage()


def _draw_verdict(c: canvas.Canvas, rows: list[dict], font: str, bold: str) -> None:
    c.setFillColor(HexColor("#F7F1E6"))
    c.rect(0, 0, PAGE, PAGE, fill=1, stroke=0)
    c.setFillColor(HexColor("#2C2C2C"))
    c.setFont(bold, 16)
    c.drawCentredString(PAGE / 2, PAGE - 0.5 * inch, "Verdict Card")
    c.setFont(font, 7.5)
    c.drawCentredString(
        PAGE / 2,
        PAGE - 0.72 * inch,
        "Statuses: keep · keep-leaning · reject · locked  ·  decided_by + date required",
    )

    headers = ["Page", "Beat", "Ver", "Model", "Status", "By", "Date", "Notes"]
    col_w = [0.55, 1.15, 0.55, 1.0, 0.75, 0.45, 0.7, 2.15]
    x0 = 0.28 * inch
    y = PAGE - 1.0 * inch
    c.setFont(bold, 7)
    x = x0
    for h, w in zip(headers, col_w):
        c.drawString(x, y, h)
        x += w * inch
    y -= 12
    c.setStrokeColor(HexColor("#C8BDB0"))
    c.line(x0, y + 6, PAGE - 0.28 * inch, y + 6)
    c.setFont(font, 6.5)
    for row in rows:
        if y < 0.45 * inch:
            c.showPage()
            c.setFillColor(HexColor("#F7F1E6"))
            c.rect(0, 0, PAGE, PAGE, fill=1, stroke=0)
            c.setFillColor(HexColor("#2C2C2C"))
            y = PAGE - 0.55 * inch
            c.setFont(bold, 11)
            c.drawString(x0, y, "Verdict Card (cont.)")
            y -= 16
            c.setFont(font, 6.5)
        vals = [
            str(row.get("page", "")),
            str(row.get("beat", "")),
            str(row.get("version", "")),
            str(row.get("model", "")),
            str(row.get("status", "")),
            str(row.get("decided_by", "")),
            str(row.get("date", "")),
            str(row.get("notes", "")),
        ]
        x = x0
        for v, w in zip(vals, col_w):
            c.drawString(x, y, v[: max(4, int(w * 11))])
            x += w * inch
        y -= 11
    c.showPage()


def assemble(manifest: dict, out_pdf: Path, out_json: Path) -> None:
    font, bold = _register_fonts()
    pages = manifest.get("pages", [])
    verdicts = manifest.get("verdicts", [])
    meta = {
        "title": manifest.get("title", "Book Flipbook"),
        "date": manifest.get("date", date.today().isoformat()),
        "flow_doc": manifest.get("flow_doc", ""),
        "models": manifest.get("models", ""),
        "source": manifest.get("source", "manifest"),
        "image_count": sum(1 for p in pages if p.get("path")),
        "content_pages": len(pages),
    }
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_pdf), pagesize=(PAGE, PAGE))
    c.setTitle(meta["title"])
    c.setAuthor("Hermes Book Pipeline")
    _draw_cover(c, meta, font, bold)

    root = Path(manifest.get("root", "."))
    for p in pages:
        caption = p.get("caption", p.get("beat", ""))
        path = p.get("path")
        split = p.get("split")
        if not path:
            _draw_placeholder(c, caption, font, bold)
            continue
        full = root / path if not Path(path).is_absolute() else Path(path)
        if not full.is_file():
            _draw_placeholder(c, f"{caption} · missing {path}", font, bold)
            continue
        try:
            jpeg = _split_wide(full, split, 2550) if split else _to_srgb_jpeg(full, 2550)
            _draw_image_page(c, jpeg, caption, font)
        except Exception as exc:  # noqa: BLE001
            _draw_placeholder(c, f"{caption} · error: {exc}", font, bold)

    _draw_verdict(c, verdicts, font, bold)
    c.save()
    out_json.write_text(
        json.dumps({"meta": meta, "verdicts": verdicts, "pages": pages}, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {out_pdf}")
    print(f"Wrote {out_json}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble picture-book flipbook PDF")
    ap.add_argument(
        "--flow-current",
        type=Path,
        default=None,
        help="Path to _FLOW-CURRENT.json (default: Media/generated/mocks/_FLOW-CURRENT.json)",
    )
    ap.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Legacy manifest (discouraged). Prefer --flow-current.",
    )
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--root", type=Path, default=Path("."))
    args = ap.parse_args()

    root = args.root.resolve()
    if args.manifest and not args.flow_current:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if "root" not in manifest:
            manifest["root"] = str(root)
        manifest.setdefault("source", "legacy-manifest")
    else:
        flow_path = args.flow_current or (root / DEFAULT_FLOW)
        if not flow_path.is_file():
            raise SystemExit(f"Missing {flow_path} — create _FLOW-CURRENT.json; flipbook will not guess.")
        flow = json.loads(flow_path.read_text(encoding="utf-8"))
        manifest = flow_current_to_manifest(flow, root)

    day = manifest.get("date", date.today().isoformat())
    out = args.out or (root / "Output" / f"flipbook-{day}.pdf")
    out_json = out.with_name(out.stem + "-verdicts.json")
    assemble(manifest, out, out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
