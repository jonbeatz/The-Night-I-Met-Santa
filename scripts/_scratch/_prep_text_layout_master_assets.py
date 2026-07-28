#!/usr/bin/env python3
"""Prep assets for text-layout-master PSD build (cloud placeholder + DESIGN-TOKENS strip)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Xtraz" / "Adobe-Photoshop" / "text-layout-master"
OUT.mkdir(parents=True, exist_ok=True)

# DESIGN-TOKENS key colors
SWATCHES = [
    ("wall-burgundy", "#4A0E17"),
    ("santa-coat", "#CC2936"),
    ("boy-pjs", "#D4C5A9"),
    ("sky-night", "#1A2744"),
    ("page-cream", "#FDFBF7"),
    ("text-primary", "#1A1A1A"),
    ("firelight", "#F4A236"),
    ("gold-light", "#FFD700"),
    ("tree-green", "#2E5E2E"),
    ("vignette", "#FDFBF7"),
]


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def make_cloud() -> Path:
    """Soft translucent cream cloud placeholder (spread-wide, for type underlay)."""
    w, h = 5250, 2625
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Soft oval in lower-center-left and center-right zones (typical poem pockets)
    cream = (253, 251, 247, 140)
    for box in [
        (280, 900, 2200, 2300),
        (2800, 700, 4900, 2100),
    ]:
        draw.ellipse(box, fill=cream)
    # feather by downscale trick
    small = img.resize((w // 8, h // 8), Image.Resampling.LANCZOS)
    img = small.resize((w, h), Image.Resampling.LANCZOS)
    path = OUT / "_cloud-placeholder.png"
    img.save(path)
    return path


def make_tokens_strip() -> Path:
    """Reference strip: color chips + font specs (place at top of layers)."""
    w, h = 5250, 420
    img = Image.new("RGB", (w, h), (253, 251, 247))
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 36)
        font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 22)
        font_sm = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
    except OSError:
        font_title = font = font_sm = ImageFont.load_default()

    draw.text((40, 20), "DESIGN-TOKENS — reference (not print)", fill=(26, 26, 26), font=font_title)
    draw.text(
        (40, 70),
        "Poem: Cormorant Garamond Medium 20/26 tracking +5 centered #1A1A1A · "
        "Title: Cinzel Decorative · God bless.: Cormorant Bold · Live type in InDesign",
        fill=(26, 26, 26),
        font=font_sm,
    )
    draw.text(
        (40, 100),
        "Canvas 5250x2625 @300dpi · Bleed 0.125in · Safety 0.5in from trim (=0.625in from art edge) · "
        "Cyan=TRIM Magenta=SAFETY Orange=FOLD",
        fill=(74, 14, 23),
        font=font_sm,
    )

    x = 40
    y = 160
    chip = 90
    for name, hx in SWATCHES:
        rgb = hex_rgb(hx)
        draw.rectangle([x, y, x + chip, y + chip], fill=rgb, outline=(26, 26, 26))
        draw.text((x, y + chip + 6), f"{name}", fill=(26, 26, 26), font=font_sm)
        draw.text((x, y + chip + 28), hx, fill=(90, 90, 90), font=font_sm)
        x += chip + 40

    path = OUT / "_tokens-swatch-strip.png"
    img.save(path)
    return path


def main() -> None:
    cloud = make_cloud()
    tokens = make_tokens_strip()
    print("wrote", cloud)
    print("wrote", tokens)


if __name__ == "__main__":
    main()
