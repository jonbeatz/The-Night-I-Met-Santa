#!/usr/bin/env python3
"""God Bless logo from styles3/logo2.png — gold foil, readable, transparent PNG."""
from __future__ import annotations

import io
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
SRC = ROOT / "Images/styles3/logo2.png"
OUT = ROOT / "Images/styles3/logo-god-bless.png"
OUT_BLACK = ROOT / "Images/styles3/logo-god-bless-on-black.png"
# Keep prior squashed pass for comparison
OUT_PREV = ROOT / "Images/styles3/logo-god-bless-v1-squashed.png"


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


def black_to_alpha(im: Image.Image, threshold: int = 30) -> Image.Image:
    """Solid black (or near-black) -> transparent; keep gold foil."""
    rgba = im.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r <= threshold and g <= threshold and b <= threshold:
                px[x, y] = (0, 0, 0, 0)
            else:
                px[x, y] = (r, g, b, 255)
    return rgba


def crop_to_content(im: Image.Image, pad: int = 24) -> Image.Image:
    """Tight crop to non-transparent / non-black content with padding."""
    rgba = im.convert("RGBA")
    alpha = rgba.split()[-1]
    bbox = alpha.getbbox()
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
    if OUT.exists() and not OUT_PREV.exists():
        OUT.replace(OUT_PREV)
        print("archived prior ->", OUT_PREV)

    url = fal_client.upload_file(str(SRC))
    prompt = """\
Edit IMAGE 1 into a matching Christmas storybook TITLE LOGO badge.

KEEP from IMAGE 1 (style only):
- Distressed warm gold-leaf / hammered metal texture (multi-tonal shimmering gold)
- Same classic high-contrast serif letterforms with elegant calligraphic swashes
- Small four-pointed sparkle/glints near flourish tips
- Top decorative border: centered 8-point star/snowflake with symmetrical scrollwork
- Bottom decorative border: thinner horizontal rule with small centered diamond ornament
- SOLID PURE BLACK background only
- Premium fairytale Christmas logo look

CRITICAL PROPORTIONS (fix the squashed look):
- Text is ONLY two words: **God Bless** — much shorter than the source title
- Letterforms must be TALLER and more OPEN — natural serif proportions, NOT horizontally stretched
- Generous letter spacing / kerning so every letter is clearly readable (G-o-d  B-l-e-s-s)
- Capitals G and B may have elegant swashes, but do not crush or overlap neighboring letters
- Composition ~2.4:1 or 16:9 wide — NOT ultra-wide 4:1. Logo should feel balanced, not flattened
- Comfortable breathing room around the type; ornaments scale to the shorter phrase

CHANGE:
- Replace ALL title text with exactly: God Bless
- No other words. No "The Night I Met Santa".
- Do NOT bake a white matte.
"""
    print("=== Banana Pro edit -> God Bless logo (readable) ===")
    result = fal_client.subscribe(
        "fal-ai/nano-banana-pro/edit",
        arguments={
            "prompt": prompt,
            "image_urls": [url],
            "num_images": 1,
            # 16:9 keeps native height healthier than 21:9; shorter phrase fits well
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "output_format": "png",
            "limit_generations": True,
            "safety_tolerance": "4",
            "seed": 26080102,
        },
        with_logs=True,
    )
    out_url = result["images"][0]["url"]
    raw = download(out_url)
    print("native", raw.size, "aspect", round(raw.size[0] / raw.size[1], 2))

    # Do NOT force-stretch to the long title's 3909x959 — that caused the squash.
    clear = black_to_alpha(raw, threshold=30)
    clear = crop_to_content(clear, pad=32)
    # Optional mild upscale if under ~2K wide (print-friendly)
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
