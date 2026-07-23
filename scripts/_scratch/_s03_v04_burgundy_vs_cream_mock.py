#!/usr/bin/env python3
"""S3 v04 wall-color A/B: burgundy vs cream/beige walls + same text clouds."""
from __future__ import annotations

import colorsys
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
ART = ROOT / "Media/development/S03-eyes-met/v04/art.png"
REF = ROOT / "Images/styles3/spread-01-eyes-met-WIDE.png"
BURGUNDY_MOCK = (
    ROOT
    / "Media/generated/mocks/S03-eyes-met/_INDEX/S03-eyes-met-v04-text-cloud-mock-2026-07-22.png"
)
OUT_DIR = ROOT / "Media/generated/mocks/S03-eyes-met/_INDEX"
CREAM_ART = OUT_DIR / "S03-eyes-met-v04-walls-cream-test.png"
CREAM_MOCK = OUT_DIR / "S03-eyes-met-v04-text-cloud-mock-CREAM-walls-2026-07-22.png"
COMPARE = OUT_DIR / "S03-eyes-met-v04-burgundy-vs-cream-text-mock-2026-07-22.png"
FONT = (
    ROOT
    / "Xtraz/Fonts/Allura,Cabin,Cinzel_Decorative,Cormorant_Garamond,Dancing_Script,etc"
    / "Cormorant_Garamond/static/CormorantGaramond-Medium.ttf"
)

INK = (44, 44, 44)
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


def sample_wall_cream(ref: Image.Image) -> tuple[float, float, float]:
    """Sample warm cream/beige from upper wall band of the WIDE ref (avoid fireplace/tree)."""
    r = ref.convert("RGB").resize((1024, 512), Image.Resampling.LANCZOS)
    arr = np.asarray(r, dtype=np.float32)
    # Upper center band — open cream wall in the reference
    band = arr[40:160, 280:720]
    # Prefer light warm pixels (beige walls)
    lum = band.mean(axis=2)
    warm = band[:, :, 0] > band[:, :, 2]  # R > B slightly
    light = lum > 140
    mask = warm & light
    if mask.sum() < 50:
        mask = lum > 160
    pix = band[mask]
    mean = pix.mean(axis=0)
    return float(mean[0]), float(mean[1]), float(mean[2])


def burgundy_wall_mask(rgb: Image.Image) -> Image.Image:
    """
    Soft mask of burgundy/wine WALL paint (vectorized).
    Avoid bright Santa-coat reds, fire orange, tree greens, skin, floor.
    """
    arr = np.asarray(rgb.convert("RGB"), dtype=np.float32) / 255.0
    h, w, _ = arr.shape
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    dif = np.maximum(mx - mn, 1e-6)
    sat = np.where(mx < 1e-6, 0.0, (mx - mn) / np.maximum(mx, 1e-6))
    val = mx

    hue = np.zeros_like(mx)
    mask_r = (mx == r) & (mx != mn)
    mask_g = (mx == g) & (mx != mn) & ~mask_r
    mask_b = (mx == b) & (mx != mn) & ~mask_r & ~mask_g
    hue[mask_r] = (60 * ((g[mask_r] - b[mask_r]) / dif[mask_r]) + 360) % 360
    hue[mask_g] = 60 * ((b[mask_g] - r[mask_g]) / dif[mask_g]) + 120
    hue[mask_b] = 60 * ((r[mask_b] - g[mask_b]) / dif[mask_b]) + 240

    is_wine_hue = (hue <= 25) | (hue >= 330) | ((hue >= 300) & (hue <= 345))
    is_darkish = (val >= 0.12) & (val <= 0.55)
    is_sat = (sat >= 0.18) & (sat <= 0.75)
    not_bright_coat = ~((val > 0.42) & (sat > 0.45) & (hue < 20))
    not_fire = ~((hue > 15) & (hue < 50) & (val > 0.45))
    keep = is_wine_hue & is_darkish & is_sat & not_bright_coat & not_fire

    strength = np.zeros((h, w), dtype=np.float32)
    strength[keep] = 1.0
    strength[(keep) & (val > 0.40)] *= 0.55
    strength[(keep) & (sat < 0.25)] *= 0.6

    # Vertical fade: walls upper, spare floor/gifts
    yy = np.linspace(0, 1, h, dtype=np.float32)
    vfade = np.ones(h, dtype=np.float32)
    mid = (yy > 0.55) & (yy <= 0.72)
    vfade[mid] = np.clip(1.0 - (yy[mid] - 0.55) / 0.17, 0, 1)
    vfade[yy > 0.72] = 0.0
    strength *= vfade[:, None]

    m = Image.fromarray((np.clip(strength, 0, 1) * 255).astype(np.uint8), mode="L")
    m = m.filter(ImageFilter.GaussianBlur(radius=6))
    m = m.filter(ImageFilter.GaussianBlur(radius=4))
    return m


def recolor_walls_to_cream(art: Image.Image, cream_rgb: tuple[float, float, float]) -> Image.Image:
    rgb = art.convert("RGB")
    mask = burgundy_wall_mask(rgb)
    arr = np.asarray(rgb, dtype=np.float32)
    m = np.asarray(mask, dtype=np.float32) / 255.0
    m = m[..., None]

    # Target cream with slight luminance variation from original wall (keep paint texture)
    lum = arr.mean(axis=2, keepdims=True)
    # Normalize local luminance into cream shading
    lum_n = (lum - lum.min()) / max(1.0, float(lum.max() - lum.min()))
    cream = np.array(cream_rgb, dtype=np.float32).reshape(1, 1, 3)
    # Slightly darker in corners (preserve depth feel)
    shaded = cream * (0.82 + 0.28 * lum_n)
    # Soft paper grain from original chroma noise
    out = arr * (1.0 - m) + shaded * m
    out = np.clip(out, 0, 255).astype(np.uint8)
    result = Image.fromarray(out, mode="RGB")
    # One more gentle blur on the seam
    soft = result.filter(ImageFilter.GaussianBlur(radius=0.8))
    # Only blend seam: where mask mid-strength
    mimg = mask.point(lambda p: 255 if 20 < p < 200 else 0).filter(ImageFilter.GaussianBlur(8))
    return Image.composite(soft, result, mimg)


def watercolor_cloud(w: int, h: int, seed_offset: int = 0) -> Image.Image:
    import random

    rng = random.Random(42 + seed_offset)
    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = w // 2, h // 2
    for _ in range(18):
        rw = int(w * rng.uniform(0.28, 0.55))
        rh = int(h * rng.uniform(0.32, 0.58))
        ox = int(rng.uniform(-w * 0.28, w * 0.28))
        oy = int(rng.uniform(-h * 0.28, h * 0.28))
        x0, y0 = cx + ox - rw // 2, cy + oy - rh // 2
        a = rng.randint(170, 230)
        color = (*CREAM, a) if rng.random() > 0.35 else (*CREAM_MID, a)
        d.ellipse([x0, y0, x0 + rw, y0 + rh], fill=color)
    core = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(core).ellipse(
        [int(w * 0.12), int(h * 0.15), int(w * 0.88), int(h * 0.85)],
        fill=(*CREAM, 235),
    )
    base = Image.alpha_composite(base, layer)
    base = Image.alpha_composite(base, core)
    base = base.filter(ImageFilter.GaussianBlur(radius=18))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([8, 8, w - 9, h - 9], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=28))
    r, g, b, a = base.split()
    a = Image.composite(a, Image.new("L", (w, h), 0), mask)
    return Image.merge("RGBA", (r, g, b, a))


def draw_centered_lines(canvas, lines, box, font, fill, line_gap):
    draw = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = box
    heights, widths = [], []
    for line in lines:
        bbox = font.getbbox(line)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    y = y0 + max(0, (y1 - y0 - total_h) // 2)
    for i, line in enumerate(lines):
        tw, th = widths[i], heights[i]
        x = x0 + (x1 - x0 - tw) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += th + line_gap


def apply_text_clouds(art_rgb: Image.Image) -> Image.Image:
    art = art_rgb.convert("RGBA")
    w, h = art.size
    mid = w // 2
    cw, ch = int(mid * 0.72), int(h * 0.38)
    left_cloud = watercolor_cloud(cw, ch, 0)
    right_cloud = watercolor_cloud(cw, ch, 7)
    lx, ly = int(mid * 0.08), int(h * 0.06)
    rx, ry = mid + int(mid * 0.20), int(h * 0.05)
    art.alpha_composite(left_cloud, (lx, ly))
    art.alpha_composite(right_cloud, (rx, ry))
    font = ImageFont.truetype(str(FONT), 26)
    pad = 28
    draw_centered_lines(art, LEFT_LINES, (lx + pad, ly + pad, lx + cw - pad, ly + ch - pad), font, INK, 10)
    draw_centered_lines(art, RIGHT_LINES, (rx + pad, ry + pad, rx + cw - pad, ry + ch - pad), font, INK, 10)
    tiny = ImageFont.truetype(str(FONT), 16)
    ImageDraw.Draw(art).text(
        (24, h - 36),
        "MOCK · cream/beige walls test · same clouds · not final",
        font=tiny,
        fill=(120, 110, 100),
    )
    return art.convert("RGB")


def build_compare(burgundy: Image.Image, cream: Image.Image, out: Path) -> None:
    panel_h = 460
    sc = panel_h / burgundy.height
    pw = int(burgundy.width * sc)
    a = burgundy.resize((pw, panel_h), Image.Resampling.LANCZOS)
    b = cream.resize((pw, panel_h), Image.Resampling.LANCZOS)
    margin, gap, header, label = 28, 18, 70, 40
    sheet_w = margin * 2 + pw
    sheet_h = margin * 2 + header + panel_h + label + gap + panel_h + label
    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    try:
        title_f = ImageFont.truetype(str(FONT), 28)
        sub_f = ImageFont.truetype(str(FONT), 16)
        lab_f = ImageFont.truetype(str(FONT), 18)
    except OSError:
        title_f = sub_f = lab_f = ImageFont.load_default()
    d.text((margin, 12), "S3 Eyes Met v04 — wall color A/B (text cloud mock)", fill=(28, 24, 20), font=title_f)
    d.text(
        (margin, 44),
        "Same art + clouds + type · only wall color changes (burgundy vs WIDE-ref cream/beige)",
        fill=(110, 100, 90),
        font=sub_f,
    )
    y = margin + header
    sheet.paste(a, (margin, y))
    d.text((margin, y + panel_h + 8), "A — BURGUNDY walls (current book lock)", fill=(32, 28, 24), font=lab_f)
    y2 = y + panel_h + label + gap
    sheet.paste(b, (margin, y2))
    d.text((margin, y2 + panel_h + 8), "B — CREAM / warm beige walls (from WIDE ref)", fill=(32, 28, 24), font=lab_f)
    sheet.save(out, "PNG", optimize=True)
    print("compare", out)


def main() -> None:
    art = Image.open(ART).convert("RGB")
    ref = Image.open(REF).convert("RGB")
    cream_rgb = sample_wall_cream(ref)
    print("sampled cream RGB", tuple(round(c) for c in cream_rgb))

    cream_art = recolor_walls_to_cream(art, cream_rgb)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cream_art.save(CREAM_ART, "PNG", optimize=True)

    cream_mock = apply_text_clouds(cream_art)
    cream_mock.save(CREAM_MOCK, "PNG", optimize=True)

    if BURGUNDY_MOCK.is_file():
        burgundy_mock = Image.open(BURGUNDY_MOCK).convert("RGB")
    else:
        burgundy_mock = apply_text_clouds(art)

    # Match sizes
    if burgundy_mock.size != cream_mock.size:
        burgundy_mock = burgundy_mock.resize(cream_mock.size, Image.Resampling.LANCZOS)

    build_compare(burgundy_mock, cream_mock, COMPARE)
    subprocess.run(["cmd", "/c", "start", "", str(COMPARE)], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(CREAM_MOCK)], check=False)
    print("DONE")


if __name__ == "__main__":
    main()
