#!/usr/bin/env python3
"""Build a labeled three-panel comparison board for picture-book style decisions.

Locked rule: Left = Klein 9B control · Center = new model · Right = current favorite.
Poem rule (Jon 2026-07-22): pass --unit so Flow v2 script text appears under the board.

Usage:
  python book-comparison-board.py \\
    --unit S04-sit-here \\
    --out Media/generated/mocks/S04-sit-here/_INDEX/S04-sit-here-comparison-plain-2026-07-22.png \\
    --left path.png --left-label "Klein 9B|v01|~$0.01|1536²|baseline control" \\
    --center path.png --center-label "Krea 2 Med|v02|~$0.03|1536²|painterly candidate" \\
    --right path.png --right-label "Qwen 2 Pro|v03|~$0.08|1536²|alt / detail"
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _font(size: int) -> ImageFont.ImageFont:
    for name in (
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
    ):
        p = Path(name)
        if p.is_file():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def _fit(im: Image.Image, box: int) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    scale = box / max(w, h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    return im.resize((nw, nh), Image.Resampling.LANCZOS)


def _panel(im: Image.Image, label: str, box: int, label_h: int) -> Image.Image:
    """label = 'Model|version|cost|resolution|strengths' (pipe-separated)."""
    parts = [p.strip() for p in label.split("|")]
    while len(parts) < 5:
        parts.append("—")
    model, ver, cost, res, strengths = parts[:5]
    canvas = Image.new("RGB", (box, box + label_h), (245, 240, 232))
    fitted = _fit(im, box - 16)
    ox = (box - fitted.width) // 2
    oy = 8 + (box - 16 - fitted.height) // 2
    canvas.paste(fitted, (ox, oy))
    draw = ImageDraw.Draw(canvas)
    title_f = _font(22)
    body_f = _font(16)
    y = box + 10
    draw.text((12, y), f"{model}  ·  {ver}", fill=(40, 36, 32), font=title_f)
    y += 28
    draw.text((12, y), f"{cost}  ·  {res}", fill=(70, 64, 58), font=body_f)
    y += 22
    draw.text((12, y), strengths, fill=(90, 82, 74), font=body_f)
    return canvas


def build(
    left: Path,
    center: Path,
    right: Path,
    left_label: str,
    center_label: str,
    right_label: str,
    out: Path,
    title: str,
    panel: int = 900,
    unit: str | None = None,
) -> Path:
    label_h = 100
    gap = 24
    margin = 36
    header = 72
    poem_extra = 64 if unit else 0
    panels = [
        _panel(Image.open(left), left_label, panel, label_h),
        _panel(Image.open(center), center_label, panel, label_h),
        _panel(Image.open(right), right_label, panel, label_h),
    ]
    w = margin * 2 + panel * 3 + gap * 2
    h = margin * 2 + header + panel + label_h + poem_extra
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 22), title, fill=(32, 28, 24), font=_font(28))
    roles = ("LEFT · Klein control", "CENTER · new model", "RIGHT · favorite / prior")
    x = margin
    for i, p in enumerate(panels):
        sheet.paste(p, (x, margin + header))
        draw.text((x, margin + header - 28), roles[i], fill=(110, 100, 90), font=_font(14))
        x += panel + gap
    if unit:
        try:
            from book_poem_map import footer_lines

            py = margin + header + panel + label_h + 10
            for line in footer_lines(unit):
                shown = line if len(line) <= 160 else line[:157] + "..."
                draw.text((margin, py), shown, fill=(70, 64, 58), font=_font(13))
                py += 18
        except Exception as exc:  # noqa: BLE001
            print("poem caption skipped:", exc)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Three-panel picture-book comparison board")
    ap.add_argument("--left", type=Path, required=True)
    ap.add_argument("--center", type=Path, required=True)
    ap.add_argument("--right", type=Path, required=True)
    ap.add_argument("--left-label", required=True)
    ap.add_argument("--center-label", required=True)
    ap.add_argument("--right-label", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--title", default="Style comparison")
    ap.add_argument("--panel", type=int, default=900)
    ap.add_argument("--unit", default=None, help="Flow beat id e.g. S05-chat — adds poem captions")
    args = ap.parse_args()
    path = build(
        args.left,
        args.center,
        args.right,
        args.left_label,
        args.center_label,
        args.right_label,
        args.out,
        args.title,
        args.panel,
        args.unit,
    )
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
