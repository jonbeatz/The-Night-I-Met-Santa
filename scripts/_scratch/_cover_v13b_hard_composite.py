#!/usr/bin/env python3
"""Cover v13b — HARD composite only (no AI unify). Original boy+Santa head onto v06; Pillow deepen.
Soft-blend was creating the double-head; Banana unify was rewriting poses.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/Cover"
COVER = DEV / "art.png"
V06 = DEV / "v06-peek-poster-santa-right" / "art.png"
OUT = DEV / "v13b-hard-composite"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-29"
GEN = 2048
PRINT = 2625


def soft_mask(size, box, feather: int) -> Image.Image:
    w, h = size
    l, t, r, b = box
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rectangle([l, t, r, b], fill=255)
    if feather:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    return m


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INDEX.mkdir(parents=True, exist_ok=True)

    base = Image.open(V06).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)
    orig = Image.open(COVER).convert("RGB").resize((GEN, GEN), Image.Resampling.LANCZOS)

    # Harder boy replace — tight box, light feather only on outer edge
    # Cover doorframe + boy; exclude most of living room
    boy_box = (0, 420, 520, 1850)
    boy_mask = soft_mask((GEN, GEN), boy_box, feather=14)
    out = Image.composite(orig, base, boy_mask)

    # Santa head from original (face more hidden like KEEP cover)
    santa_box = (1180, 760, 1580, 1260)
    santa_mask = soft_mask((GEN, GEN), santa_box, feather=20)
    out = Image.composite(orig, out, santa_mask)

    # Scrub hallway poster (original left wall)
    poster_box = (40, 360, 230, 740)
    wall = out.crop((70, 880, 190, 1080)).resize(
        (poster_box[2] - poster_box[0], poster_box[3] - poster_box[1]),
        Image.Resampling.LANCZOS,
    )
    # darken toward burgundy hallway
    wall = ImageEnhance.Color(wall).enhance(1.15)
    wall = ImageEnhance.Brightness(wall).enhance(0.55)
    pm = soft_mask(wall.size, (0, 0, wall.size[0], wall.size[1]), feather=12)
    region = out.crop(poster_box)
    out.paste(Image.composite(wall, region, pm), poster_box[:2])

    # Kill any leftover title gold at top of boy strip using v06 sky/ceiling
    top_box = (0, 0, 700, 260)
    top_mask = soft_mask((GEN, GEN), top_box, feather=18)
    out = Image.composite(base, out, top_mask)

    # Deepen overall toward v06 richness (color + contrast only — no pose AI)
    out = ImageEnhance.Color(out).enhance(1.12)
    out = ImageEnhance.Contrast(out).enhance(1.06)

    out.save(OUT / "art.png", optimize=True)
    out.resize((PRINT, PRINT), Image.Resampling.LANCZOS).save(
        OUT / "art-2625.png", optimize=True, dpi=(300, 300)
    )

    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — Cover / v13b-hard-composite

| Field | Value |
|-------|--------|
| **version** | v13b-hard-composite |
| **date** | {DAY} |
| **method** | HARD Pillow composite — no generative unify |
| **print** | **{PRINT}×{PRINT}** @ 300 DPI |
| **status** | dial |

## Layers

1. Base = v06 deep paint room
2. Replace boy/door strip from original (single lean, one head)
3. Replace Santa head from original (face more hidden)
4. Scrub hallway poster + top title bleed
5. Pillow saturate/contrast only
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v13b-hard-composite",
                "date": DAY,
                "method": "pillow_hard_composite_no_ai",
                "status": "dial",
            },
            indent=2,
        ),
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
    draw.text(
        (pad, 12),
        "Cover — beige-v2 KEEP  vs  v13b HARD composite (no AI pose rewrite)",
        fill=(40, 40, 40),
        font=font,
    )
    board.paste(keep, (pad, label_h))
    board.paste(out, (pad * 2 + GEN, label_h))
    board.save(INDEX / "Cover-beige-v2-vs-v13b-board.png", optimize=True)
    out.crop((0, 400, 700, 1600)).resize((350, 600)).save(INDEX / "cover-v13b-boy-crop.png")
    out.crop((1100, 750, 1650, 1350)).resize((400, 400)).save(INDEX / "cover-v13b-santa-head.png")
    # also vs v06
    v06 = base.copy()
    board2 = Image.new("RGB", (GEN * 2 + pad * 3, GEN + pad * 2 + label_h), (250, 248, 244))
    d2 = ImageDraw.Draw(board2)
    d2.text((pad, 12), "v06  vs  v13b hard composite", fill=(40, 40, 40), font=font)
    board2.paste(v06, (pad, label_h))
    board2.paste(out, (pad * 2 + GEN, label_h))
    board2.save(INDEX / "Cover-v06-vs-v13b-board.png", optimize=True)
    print("DONE", OUT / "art-2625.png")


if __name__ == "__main__":
    main()
