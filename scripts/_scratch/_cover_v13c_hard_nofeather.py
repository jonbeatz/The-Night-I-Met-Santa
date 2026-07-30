#!/usr/bin/env python3
"""Cover v13c — HARD no-feather boy/Santa paste (feather was causing double-head)."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/Cover"
COVER = DEV / "art.png"
V06 = DEV / "v06-peek-poster-santa-right" / "art.png"
OUT = DEV / "v13c-hard-nofeather"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-29"
GEN = 2048
PRINT = 2625


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INDEX.mkdir(parents=True, exist_ok=True)

    base = Image.open(V06).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)
    orig = Image.open(COVER).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)
    out = base.copy()

    # FULL hard replace of left door+boy so v06 boy cannot ghost through
    boy_box = (0, 380, 560, 1900)  # left, top, right, bottom
    out.paste(orig.crop(boy_box), (boy_box[0], boy_box[1]))

    # Hard replace Santa head — larger box to hide v06 profile face
    santa_box = (1140, 700, 1640, 1320)
    out.paste(orig.crop(santa_box), (santa_box[0], santa_box[1]))

    # Soft blend ONLY the right edge of boy strip into room (narrow)
    edge = Image.new("L", (GEN, GEN), 0)
    ImageDraw.Draw(edge).rectangle([520, 380, 560, 1900], fill=255)
    edge = edge.filter(ImageFilter.GaussianBlur(10))
    out = Image.composite(base, out, edge)  # bring a sliver of v06 room back at seam

    # Soft blend Santa box edges only
    sm = Image.new("L", (GEN, GEN), 0)
    ImageDraw.Draw(sm).rectangle([1140, 700, 1640, 1320], fill=255)
    # erode center keep hard; only blur outer ring via invert trick
    inner = Image.new("L", (GEN, GEN), 0)
    ImageDraw.Draw(inner).rectangle([1165, 725, 1615, 1295], fill=255)
    ring = ImageChops_subtract(sm, inner)
    ring = ring.filter(ImageFilter.GaussianBlur(12))
    # where ring is white, blend toward base slightly for seam
    # actually: composite base over out where ring — too strong. skip ring; hard paste ok.

    # Scrub poster: fill with nearby dark wall from BELOW poster (after boy paste)
    poster = (45, 350, 235, 730)
    sample = out.crop((60, 850, 200, 1050)).resize(
        (poster[2] - poster[0], poster[3] - poster[1]), Image.Resampling.LANCZOS
    )
    sample = ImageEnhance.Brightness(sample).enhance(0.45)
    sample = ImageEnhance.Color(sample).enhance(0.85)
    out.paste(sample, (poster[0], poster[1]))

    # Remove title leftovers at top of boy strip
    top = (0, 0, 700, 240)
    out.paste(base.crop(top), (0, 0))

    # Shift hallway teal → closer to burgundy (simple darken + red push)
    hall = out.crop((0, 240, 400, 1900))
    # boost reds slightly, reduce cyan
    r, g, b = hall.split()
    r = r.point(lambda p: min(255, int(p * 1.08 + 8)))
    g = g.point(lambda p: int(p * 0.92))
    b = b.point(lambda p: int(p * 0.95))
    hall2 = Image.merge("RGB", (r, g, b))
    hall2 = ImageEnhance.Brightness(hall2).enhance(0.92)
    out.paste(hall2, (0, 240))

    out = ImageEnhance.Color(out).enhance(1.1)
    out = ImageEnhance.Contrast(out).enhance(1.05)

    out.save(OUT / "art.png", optimize=True)
    out.resize((PRINT, PRINT), Image.Resampling.LANCZOS).save(
        OUT / "art-2625.png", optimize=True, dpi=(300, 300)
    )
    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — Cover / v13c-hard-nofeather

| Field | Value |
|-------|--------|
| **version** | v13c-hard-nofeather |
| **date** | {DAY} |
| **method** | Hard paste original boy+Santa onto v06 (no feather ghosting) |
| **print** | {PRINT}×{PRINT} @ 300 DPI |
| **status** | dial — seams may need PS polish |
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"version": "v13c-hard-nofeather", "method": "hard_paste", "status": "dial"}, indent=2),
        encoding="utf-8",
    )

    keep = Image.open(COVER).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)
    pad, label_h = 20, 64
    board = Image.new("RGB", (GEN * 2 + pad * 3, GEN + pad * 2 + label_h), (250, 248, 244))
    draw = ImageDraw.Draw(board)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    draw.text((pad, 12), "beige-v2 KEEP  vs  v13c hard paste (no feather double-head)", fill=(40, 40, 40), font=font)
    board.paste(keep, (pad, label_h))
    board.paste(out, (pad * 2 + GEN, label_h))
    board.save(INDEX / "Cover-beige-v2-vs-v13c-board.png", optimize=True)
    out.crop((0, 400, 700, 1600)).resize((350, 600)).save(INDEX / "cover-v13c-boy-crop.png")
    out.crop((1100, 750, 1650, 1350)).resize((400, 400)).save(INDEX / "cover-v13c-santa-head.png")
    print("DONE", OUT / "art-2625.png")


def ImageChops_subtract(a: Image.Image, b: Image.Image) -> Image.Image:
    from PIL import ImageChops

    return ImageChops.subtract(a, b)


if __name__ == "__main__":
    main()
