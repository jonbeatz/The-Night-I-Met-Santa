#!/usr/bin/env python3
"""Merry Christmas logo from styles3/logo2.png — gold foil, transparent PNG."""
from __future__ import annotations

import io
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
SRC = ROOT / "Images/styles3/logo2.png"
OUT = ROOT / "Images/styles3/logo-merry-christmas.png"
OUT_BLACK = ROOT / "Images/styles3/logo-merry-christmas-on-black.png"


def load_env() -> None:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def download(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGBA")


def bg_to_alpha(im: Image.Image, dark: int = 30, light: int = 225) -> Image.Image:
    """Near-black OR near-white -> transparent; keep gold foil."""
    rgba = im.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if (r <= dark and g <= dark and b <= dark) or (
                r >= light and g >= light and b >= light
            ):
                px[x, y] = (0, 0, 0, 0)
            else:
                px[x, y] = (r, g, b, 255)
    return rgba


def crop_to_content(im: Image.Image, pad: int = 32) -> Image.Image:
    rgba = im.convert("RGBA")
    bbox = rgba.split()[-1].getbbox()
    if not bbox:
        return rgba
    l, t, r, b = bbox
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(rgba.width, r + pad)
    b = min(rgba.height, b + pad)
    return rgba.crop((l, t, r, b))


def main() -> None:
    load_env()
    url = fal_client.upload_file(str(SRC))
    prompt = """\
Edit IMAGE 1 into a matching Christmas storybook TITLE LOGO badge.

KEEP from IMAGE 1 (style only):
- Distressed warm gold-leaf / hammered metal texture (multi-tonal shimmering gold)
- Same classic high-contrast serif letterforms with elegant calligraphic swashes
- Small four-pointed sparkle/glints near flourish tips
- Top decorative border: centered 8-point star/snowflake with symmetrical scrollwork
- Bottom decorative border: thinner horizontal rule with small centered diamond/star ornament
- SOLID PURE BLACK background only
- Premium fairytale Christmas logo look

PROPORTIONS (readable — do NOT squash):
- Text is ONLY two words: **Merry Christmas**
- Letterforms TALLER and OPEN — natural serif proportions, NOT horizontally stretched or flattened
- Generous letter spacing so every letter is clearly readable
- Capitals M and C may have elegant swashes; do not crush or overlap neighboring letters
- Composition ~2:1 to 16:9 wide — balanced, not ultra-wide 4:1
- Comfortable breathing room; ornaments scale to the phrase length

CHANGE:
- Replace ALL title text with exactly: Merry Christmas
- No other words. No "The Night I Met Santa". No "Jack Farrell". No "God Bless".
- Do NOT bake a white matte.
"""
    print("=== Banana Pro edit -> Merry Christmas logo ===")
    result = fal_client.subscribe(
        "fal-ai/nano-banana-pro/edit",
        arguments={
            "prompt": prompt,
            "image_urls": [url],
            "num_images": 1,
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "output_format": "png",
            "limit_generations": True,
            "safety_tolerance": "4",
            "seed": 26080104,
        },
        with_logs=True,
    )
    out_url = result["images"][0]["url"]
    raw = download(out_url)
    print("native", raw.size, "aspect", round(raw.size[0] / raw.size[1], 2))
    print("corner", raw.getpixel((0, 0)))

    clear = bg_to_alpha(raw)
    clear = crop_to_content(clear, pad=32)
    if clear.width < 2400:
        scale = 2400 / clear.width
        clear = clear.resize(
            (int(clear.width * scale), int(clear.height * scale)),
            Image.Resampling.LANCZOS,
        )

    on_black = Image.new("RGBA", clear.size, (0, 0, 0, 255))
    on_black.paste(clear, (0, 0), clear)
    on_black.convert("RGB").save(OUT_BLACK, "PNG")
    clear.save(OUT, "PNG")
    print("saved", OUT, clear.size)
    print("saved", OUT_BLACK)
    print("fal_url", out_url)


if __name__ == "__main__":
    main()
