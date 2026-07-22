"""Best-of mockup book PDF — cover to cover from current keepers.

Front cover → P01…P33 (spreads split L/R) → soft back placeholder.
sRGB · 8.5\" square · full bleed · no crop marks.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = ROOT / "Output"
PAGES_DIR = ROOT / "Media" / "generated" / "mocks" / "_INDEX" / "best-of-mockup-2026-07-21-pages"
PDF_OUT = OUT_DIR / "The-Night-I-Met-Santa-BEST-OF-MOCKUP-2026-07-21.pdf"
MANIFEST = ROOT / "Media" / "generated" / "mocks" / "_INDEX" / "best-of-mockup-2026-07-21.md"
PAGE_PX = 2048
CREAM = (245, 238, 224)


def fit_cover(im: Image.Image, size: int = PAGE_PX) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    scale = max(size / w, size / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - size) // 2
    top = (nh - size) // 2
    return im.crop((left, top, left + size, top + size))


def fit_contain_cream(im: Image.Image, size: int = PAGE_PX) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    scale = min(size / w, size / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), CREAM)
    canvas.paste(im, ((size - nw) // 2, (size - nh) // 2))
    return canvas


def split_spread(path: Path, size: int = PAGE_PX) -> tuple[Image.Image, Image.Image]:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    mid = w // 2
    left = im.crop((0, 0, mid, h))
    right = im.crop((mid, 0, w, h))
    return fit_cover(left, size), fit_cover(right, size)


def cream_placeholder(label: str, size: int = PAGE_PX) -> Image.Image:
    canvas = Image.new("RGB", (size, size), CREAM)
    draw = ImageDraw.Draw(canvas)
    margin = size // 12
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        outline=(220, 210, 190),
        width=2,
    )
    try:
        font = ImageFont.truetype("arial.ttf", 36)
        font_sm = ImageFont.truetype("arial.ttf", 28)
    except OSError:
        font = font_sm = ImageFont.load_default()
    draw.text((margin + 24, size - margin - 56), label, fill=(180, 168, 150), font=font)
    return canvas


def save_page(im: Image.Image, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=92, optimize=True, subsampling=1)
    return dest


def main() -> int:
    try:
        import img2pdf
    except ImportError:
        print("img2pdf required", file=sys.stderr)
        return 1

    M = ROOT / "Media"
    mocks = M / "generated" / "mocks"
    approved = M / "approved"

    # Best-of map (Jon keeps / locks as of 2026-07-21 night)
    spreads = [
        ("06-07", "S01-approach", mocks / "S01-approach" / "v01" / "art.png"),
        ("08-09", "S02-threshold", mocks / "S02-threshold" / "v02" / "art.png"),
        ("10-11", "S03-eyes-met", approved / "spreads" / "spread-eyes-met.png"),
        ("12-13", "S04-sit-here", mocks / "S04-sit-here" / "v01" / "art.png"),
        ("14-15", "S05-chat", mocks / "S05-chat" / "v02" / "art.png"),
        ("16-17", "S06-cocoa", mocks / "S06-cocoa" / "v01" / "art.png"),
        ("18-19", "S07-proof", mocks / "S07-proof" / "v05" / "art.png"),  # Gemini keep
        ("20-21", "S08-gone", mocks / "S08-gone" / "v02" / "art.png"),
        ("22-23", "S09-search", mocks / "S09-search" / "v01" / "art.png"),
        ("24-25", "S10-note", mocks / "S10-note" / "v01" / "art.png"),
        ("26-27", "S11-wish", mocks / "S11-wish" / "v02" / "art.png"),
        ("28-29", "S12-blessing", mocks / "S12-blessing" / "v01" / "art.png"),
    ]

    pages: list[tuple[str, Image.Image, str]] = []

    # 00 Front cover
    pages.append(
        (
            "00-cover-front",
            fit_cover(Image.open(approved / "covers" / "cover-front.png")),
            "Cover front · locked beige-v2 · Media/approved/covers/cover-front.png",
        )
    )
    # Interior
    pages.append(
        (
            "01-p01-title",
            fit_contain_cream(Image.open(approved / "pages" / "p01-title.png")),
            "P01 Title · locked v22 · Media/approved/pages/p01-title.png",
        )
    )
    pages.append(
        (
            "02-p02-copyright",
            fit_contain_cream(Image.open(mocks / "P02-copyright" / "v01" / "art.png")),
            "P02 Copyright · keep v01",
        )
    )
    pages.append(
        (
            "03-p03-dedication",
            fit_contain_cream(Image.open(mocks / "P03-dedication" / "v01" / "art.png")),
            "P03 Dedication · keep v01",
        )
    )
    pages.append(
        (
            "04-p04-about-type",
            cream_placeholder("p4 · About (type zone)"),
            "P04 About L · type only (placeholder)",
        )
    )
    pages.append(
        (
            "05-p05-about-vignette",
            fit_contain_cream(Image.open(mocks / "P05-about-vignette" / "v01" / "art.png")),
            "P05 About R · keep v01",
        )
    )

    for pages_label, slug, path in spreads:
        if not path.is_file():
            raise FileNotFoundError(path)
        left, right = split_spread(path)
        lo, hi = pages_label.split("-")
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        pages.append((f"{lo}-{slug}-L", left, f"{slug} LEFT · {rel}"))
        pages.append((f"{hi}-{slug}-R", right, f"{slug} RIGHT · {rel}"))

    pages.append(
        (
            "30-p30-thanks",
            cream_placeholder("p30 · Thank You (type zone)"),
            "P30 Thanks · type only (placeholder)",
        )
    )
    pages.append(
        (
            "31-p31-jack",
            fit_cover(Image.open(approved / "characters" / "jack-farrell-portrait.png")),
            "P31 Jack Farrell · locked portrait",
        )
    )
    pages.append(
        (
            "32-p32-quiet-close",
            fit_contain_cream(Image.open(mocks / "P32-quiet-close" / "v01" / "art.png")),
            "P32 Quiet close · keep v01",
        )
    )
    pages.append(
        (
            "33-p33-merry",
            fit_contain_cream(Image.open(mocks / "P33-merry-christmas" / "v01" / "art.png")),
            "P33 Merry Christmas · keep v01",
        )
    )
    # Back cover TBD
    pages.append(
        (
            "99-cover-back-tbd",
            cream_placeholder("Back cover · TBD (not locked)"),
            "Back cover · pending (style-refs/back candidates exist)",
        )
    )

    # Clear + write pages
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    for old in PAGES_DIR.glob("*.jpg"):
        old.unlink()

    ordered: list[Path] = []
    manifest_rows: list[str] = []
    for i, (name, im, note) in enumerate(pages, start=1):
        dest = PAGES_DIR / f"page-{i:02d}-{name}.jpg"
        save_page(im, dest)
        ordered.append(dest)
        manifest_rows.append(f"| {i} | {name} | {note} |")
        print(f"  [{i:02d}] {dest.name}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    side = img2pdf.in_to_pt(8.5)
    layout = img2pdf.get_layout_fun(pagesize=(side, side))
    with open(PDF_OUT, "wb") as fh:
        fh.write(img2pdf.convert([str(p) for p in ordered], layout_fun=layout))

    MANIFEST.write_text(
        f"""# Best-of mockup book — 2026-07-21

**PDF:** `Output/The-Night-I-Met-Santa-BEST-OF-MOCKUP-2026-07-21.pdf`  
**Pages:** {len(ordered)} · 8.5″ square · sRGB · full bleed · no crop marks  
**JPGs:** `Media/generated/mocks/_INDEX/best-of-mockup-2026-07-21-pages/`

Cover → interior keeps → soft back placeholder. Spreads split L/R for page-turn review.

| # | Sheet | Source |
|---|-------|--------|
{chr(10).join(manifest_rows)}

## Notes

- S7 = **v05** (Gemini keep; v04 Klein alt not used in this PDF)
- S8 = **v02** · S2/S5/S11 = **v02** · S3/P01/cover/Jack = locked
- P04 / P30 / back cover = cream placeholders (type or TBD)
- Art only — no live poem type / clouds yet (InDesign phase)
""",
        encoding="utf-8",
    )

    print(f"Wrote {PDF_OUT} ({len(ordered)} pages)")
    print(f"Manifest {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
