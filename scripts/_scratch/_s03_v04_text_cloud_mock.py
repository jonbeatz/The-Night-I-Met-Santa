#!/usr/bin/env python3
"""S3 Eyes Met v04 — text-cloud placement mock (art unchanged)."""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
ART = ROOT / "Media/development/S03-eyes-met/v04/art.png"
OUT_DIR = ROOT / "Media/generated/mocks/S03-eyes-met/_INDEX"
OUT = OUT_DIR / "S03-eyes-met-v04-text-cloud-mock-2026-07-22.png"
FONT = (
    ROOT
    / "Xtraz/Fonts/Allura,Cabin,Cinzel_Decorative,Cormorant_Garamond,Dancing_Script,etc"
    / "Cormorant_Garamond/static/CormorantGaramond-Medium.ttf"
)
INK = (44, 44, 44)  # #2C2C2C
CREAM = (250, 244, 232)
CREAM_MID = (245, 238, 222)

LEFT_LINES = [
    "My jaw dropped when our eyes finally met.",
    "I knew right then, it was a moment",
    "I would never forget.",
]
RIGHT_LINES = [
    "For there he was in all his splendor,",
    "brilliant white hair, red coat",
    "with suspenders.",
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT), size)


def watercolor_cloud(w: int, h: int, seed_offset: int = 0) -> Image.Image:
    """Soft irregular cream cloud with feathered edges (RGBA)."""
    import random

    rng = random.Random(42 + seed_offset)
    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = w // 2, h // 2
    # Overlapping soft blobs → organic watercolor paper wash
    for _ in range(18):
        rw = int(w * rng.uniform(0.28, 0.55))
        rh = int(h * rng.uniform(0.32, 0.58))
        ox = int(rng.uniform(-w * 0.28, w * 0.28))
        oy = int(rng.uniform(-h * 0.28, h * 0.28))
        x0, y0 = cx + ox - rw // 2, cy + oy - rh // 2
        x1, y1 = x0 + rw, y0 + rh
        a = rng.randint(170, 230)
        color = (*CREAM, a) if rng.random() > 0.35 else (*CREAM_MID, a)
        d.ellipse([x0, y0, x1, y1], fill=color)
    # Core denser ivory
    core = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)
    cd.ellipse(
        [int(w * 0.12), int(h * 0.15), int(w * 0.88), int(h * 0.85)],
        fill=(*CREAM, 235),
    )
    base = Image.alpha_composite(base, layer)
    base = Image.alpha_composite(base, core)
    base = base.filter(ImageFilter.GaussianBlur(radius=18))
    # Soft outer vignette so edges dissolve into burgundy
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([8, 8, w - 9, h - 9], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=28))
    r, g, b, a = base.split()
    a = Image.composite(a, Image.new("L", (w, h), 0), mask)
    return Image.merge("RGBA", (r, g, b, a))


def draw_centered_lines(
    canvas: Image.Image,
    lines: list[str],
    box: tuple[int, int, int, int],
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    line_gap: int,
) -> None:
    draw = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = box
    # Measure block height
    heights = []
    widths = []
    for line in lines:
        bbox = font.getbbox(line)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    y = y0 + max(0, (y1 - y0 - total_h) // 2)
    for i, line in enumerate(lines):
        tw = widths[i]
        th = heights[i]
        x = x0 + (x1 - x0 - tw) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += th + line_gap


def main() -> None:
    if not ART.is_file():
        raise SystemExit(f"missing {ART}")
    if not FONT.is_file():
        raise SystemExit(f"missing {FONT}")

    art = Image.open(ART).convert("RGBA")
    w, h = art.size  # 2048×1024
    mid = w // 2

    # Cloud sizes relative to half-page
    cw, ch = int(mid * 0.72), int(h * 0.38)
    left_cloud = watercolor_cloud(cw, ch, seed_offset=0)
    right_cloud = watercolor_cloud(cw, ch, seed_offset=7)

    # Placement: upper-left wall (L page), upper-right wall (R page)
    # Keep clear of faces — sit on burgundy above figures
    lx = int(mid * 0.08)
    ly = int(h * 0.06)
    rx = mid + int(mid * 0.20)
    ry = int(h * 0.05)

    comp = art.copy()
    comp.alpha_composite(left_cloud, (lx, ly))
    comp.alpha_composite(right_cloud, (rx, ry))

    # Cormorant Medium — scaled for 2048 mock readability (~print 20pt feel on half-page)
    font = load_font(26)
    pad = 28
    draw_centered_lines(
        comp,
        LEFT_LINES,
        (lx + pad, ly + pad, lx + cw - pad, ly + ch - pad),
        font,
        INK,
        line_gap=10,
    )
    draw_centered_lines(
        comp,
        RIGHT_LINES,
        (rx + pad, ry + pad, rx + cw - pad, ry + ch - pad),
        font,
        INK,
        line_gap=10,
    )

    # Tiny mock label
    tiny = load_font(16)
    note = "MOCK · S3 Eyes Met v04 · cream text clouds · Cormorant Medium · not final"
    nd = ImageDraw.Draw(comp)
    bbox = tiny.getbbox(note)
    nd.text(
        (24, h - 36),
        note,
        font=tiny,
        fill=(230, 220, 210),
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rgb = comp.convert("RGB")
    rgb.save(OUT, "PNG", optimize=True)
    # Also stash next to v04 for easy find
    side = ROOT / "Media/development/S03-eyes-met/v04/text-cloud-mock.png"
    rgb.save(side, "PNG", optimize=True)
    print("saved", OUT)
    print("saved", side)
    subprocess.run(["cmd", "/c", "start", "", str(OUT)], check=False)


if __name__ == "__main__":
    main()
