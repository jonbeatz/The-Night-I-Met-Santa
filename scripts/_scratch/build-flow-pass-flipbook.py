"""Assemble flow-pass flipbook PDF — page order, sRGB, full bleed, no crop marks.

Splits spreads L/R; fits singles to square; cream placeholders for type-only pages.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = ROOT / "Output"
FLIP_PAGES = ROOT / "Media" / "generated" / "mocks" / "_INDEX" / "flow-pass-2026-07-21-pages"
PDF_OUT = OUT_DIR / "flow-pass-2026-07-21-flipbook.pdf"
PAGE_PX = 2048  # square review pages
CREAM = (245, 238, 224)


def fit_cover(im: Image.Image, size: int = PAGE_PX) -> Image.Image:
    """Cover-fit into square (full bleed, may crop edges)."""
    im = im.convert("RGB")
    w, h = im.size
    scale = max(size / w, size / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - size) // 2
    top = (nh - size) // 2
    return im.crop((left, top, left + size, top + size))


def fit_contain_cream(im: Image.Image, size: int = PAGE_PX) -> Image.Image:
    """Contain-fit on cream (for framed vignettes that need paper margin)."""
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
    # Soft vignette ring suggestion — no crop marks
    margin = size // 12
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        outline=(220, 210, 190),
        width=2,
    )
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except OSError:
        font = ImageFont.load_default()
    # Tiny corner cue only (not poem text baked into art)
    draw.text((margin + 24, size - margin - 48), label, fill=(180, 168, 150), font=font)
    return canvas


def save_page(im: Image.Image, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # JPEG keeps PDF lean; sRGB assumed for RGB PIL images
    im.save(dest, "JPEG", quality=92, optimize=True, subsampling=1)
    return dest


def build(include_cover: bool = False) -> Path:
    try:
        import img2pdf
    except ImportError:
        print("img2pdf required: python -m pip install img2pdf", file=sys.stderr)
        raise SystemExit(1)

    M = ROOT / "Media"
    mocks = M / "generated" / "mocks"
    approved = M / "approved"

    pages: list[tuple[str, Image.Image]] = []

    if include_cover:
        pages.append(("00-cover", fit_cover(Image.open(approved / "covers" / "cover-front.png"))))

    # 1 Title
    pages.append(("01-p01-title", fit_contain_cream(Image.open(approved / "pages" / "p01-title.png"))))
    # 2 Copyright
    pages.append(("02-p02-copyright", fit_contain_cream(Image.open(mocks / "P02-copyright" / "v01" / "art.png"))))
    # 3 Dedication
    pages.append(("03-p03-dedication", fit_contain_cream(Image.open(mocks / "P03-dedication" / "v01" / "art.png"))))
    # 4|5 About
    pages.append(("04-p04-about-type", cream_placeholder("p4 · About (type)")))
    pages.append(("05-p05-about-vignette", fit_contain_cream(Image.open(mocks / "P05-about-vignette" / "v01" / "art.png"))))

    spreads = [
        ("06-07", "S01-approach", mocks / "S01-approach" / "v01" / "art.png"),
        ("08-09", "S02-threshold", mocks / "S02-threshold" / "v02" / "art.png"),
        ("10-11", "S03-eyes-met", approved / "spreads" / "spread-eyes-met.png"),
        ("12-13", "S04-sit-here", mocks / "S04-sit-here" / "v01" / "art.png"),
        ("14-15", "S05-chat", mocks / "S05-chat" / "v02" / "art.png"),
        ("16-17", "S06-cocoa", mocks / "S06-cocoa" / "v01" / "art.png"),
        ("18-19", "S07-proof", mocks / "S07-proof" / "v01" / "art.png"),
        ("20-21", "S08-gone", mocks / "S08-gone" / "v01" / "art.png"),
        ("22-23", "S09-search", mocks / "S09-search" / "v01" / "art.png"),
        ("24-25", "S10-note", mocks / "S10-note" / "v01" / "art.png"),
        ("26-27", "S11-wish", mocks / "S11-wish" / "v02" / "art.png"),
        ("28-29", "S12-blessing", mocks / "S12-blessing" / "v01" / "art.png"),
    ]

    for pages_label, slug, path in spreads:
        if not path.is_file():
            raise FileNotFoundError(path)
        left, right = split_spread(path)
        lo, hi = pages_label.split("-")
        pages.append((f"{lo}-{slug}-L", left))
        pages.append((f"{hi}-{slug}-R", right))

    # 30|31 Thanks + Jack
    pages.append(("30-p30-thanks", cream_placeholder("p30 · Thank You (type)")))
    pages.append(("31-p31-jack", fit_cover(Image.open(approved / "characters" / "jack-farrell-portrait.png"))))
    # 32|33 Quiet close
    pages.append(("32-p32-quiet-close", fit_contain_cream(Image.open(mocks / "P32-quiet-close" / "v01" / "art.png"))))
    pages.append(("33-p33-merry", fit_contain_cream(Image.open(mocks / "P33-merry-christmas" / "v01" / "art.png"))))

    FLIP_PAGES.mkdir(parents=True, exist_ok=True)
    # clear old
    for old in FLIP_PAGES.glob("*.jpg"):
        old.unlink()

    ordered: list[Path] = []
    for i, (name, im) in enumerate(pages, start=1):
        dest = FLIP_PAGES / f"page-{i:02d}-{name}.jpg"
        save_page(im, dest)
        ordered.append(dest)
        print(f"  [{i:02d}] {dest.name}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # 8.5" square review — no bleed marks
    side = img2pdf.in_to_pt(8.5)
    layout = img2pdf.get_layout_fun(pagesize=(side, side))
    with open(PDF_OUT, "wb") as fh:
        fh.write(img2pdf.convert([str(p) for p in ordered], layout_fun=layout))

    print(f"Wrote {PDF_OUT} ({len(ordered)} pages @ 8.5\" square, sRGB JPEG to PDF)")
    return PDF_OUT


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-cover", action="store_true")
    args = ap.parse_args()
    build(include_cover=args.include_cover)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


