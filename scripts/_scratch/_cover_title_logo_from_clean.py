"""Clean hi-res logo from cleanLogo.png: clarity upscale → navy→alpha. NO rembg / NO re-AI text."""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
load_dotenv(ROOT / ".env.local")
KEY = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")

REF = ROOT / "Images" / "styles1" / "cleanLogo.png"
OUT = ROOT / "Media" / "approved" / "covers" / "cover-title-logo.png"
UPSCALE = "fal-ai/clarity-upscaler"


def fal_headers(json_body: bool = False) -> dict:
    h = {"Authorization": f"Key {KEY}"}
    if json_body:
        h["Content-Type"] = "application/json"
    return h


def upload(path: Path) -> str:
    req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps({"file_name": path.name, "content_type": "image/png"}).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        meta = json.loads(r.read().decode())
    put = urllib.request.Request(
        meta["upload_url"], data=path.read_bytes(), method="PUT",
        headers={"Content-Type": "image/png"},
    )
    with urllib.request.urlopen(put) as r:
        if r.status not in (200, 201):
            raise RuntimeError(f"PUT {r.status}")
    return meta["file_url"]


def fal_run(endpoint: str, body: dict) -> dict:
    req = urllib.request.Request(
        f"https://fal.run/{endpoint}",
        data=json.dumps(body).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode())


def is_navy_bg(r: int, g: int, b: int) -> bool:
    """True for dark night-sky navy (not gold, not white credit)."""
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # white / light credit
    if lum > 170 and min(r, g, b) > 140:
        return False
    # gold / warm metal
    if r > 90 and r >= g and r > b + 15:
        return False
    if r > 70 and r > b and (r - b) > 20 and lum > 55:
        return False
    # navy / dark blue sky
    if b >= g and b >= r and lum < 130:
        return True
    if lum < 45 and b >= r:
        return True
    return False


def navy_to_alpha(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if is_navy_bg(r, g, b):
                px[x, y] = (0, 0, 0, 0)
            else:
                # soft edge: dark navy-ish fringe → partial alpha
                lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
                if lum < 70 and b > r and b > g and not (r > b):
                    alpha = max(0, min(255, int(lum * 3)))
                    px[x, y] = (r, g, b, alpha)
    return im


def crop_content(im: Image.Image, pad: int = 16) -> Image.Image:
    # Drop bottom moon/roof band (~bottom 18%) before bbox if mostly scenery
    h = im.height
    top_band = im.crop((0, 0, im.width, int(h * 0.82)))
    bbox = top_band.getbbox()
    if not bbox:
        bbox = im.getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(im.width, r + pad)
    b = min(im.height, b + pad)
    return im.crop((l, t, r, b))


def main() -> None:
    print("Upscaling cleanLogo (clarity 2x, high resemblance)…")
    result = fal_run(
        UPSCALE,
        {
            "image_url": upload(REF),
            "upscale_factor": 2,
            "resemblance": 0.85,
            "creativity": 0.15,
            "guidance_scale": 3.5,
            "num_inference_steps": 18,
            "prompt": (
                "clean sharp ornate gold book title logo typography, smooth letter edges, "
                "high detail metallic gold text, crisp serif, no blur, no artifacts"
            ),
            "negative_prompt": (
                "blurry, jagged edges, white blotches, muddy texture, noise, compression artifacts, "
                "low quality, pixelated"
            ),
            "seed": 42,
            "enable_safety_checker": True,
        },
    )
    img_info = result.get("image")
    url = img_info["url"] if isinstance(img_info, dict) else img_info
    tmp = ROOT / "Media" / "approved" / "covers" / "_tmp_logo_up.png"
    with urllib.request.urlopen(url) as r:
        tmp.write_bytes(r.read())
    up = Image.open(tmp)
    print("upscaled", up.size)

    out = crop_content(navy_to_alpha(up))
    out.save(OUT)
    tmp.unlink(missing_ok=True)

    (OUT.parent / "cover-title-logo.recipe.md").write_text(
        f"""# cover-title-logo.recipe.md

| Field | Value |
|-------|--------|
| **file** | `Media/approved/covers/cover-title-logo.png` |
| **main ref** | `Images/styles1/cleanLogo.png` (exact logo — not re-drawn) |
| **process** | fal `{UPSCALE}` 2× (high resemblance) → Pillow navy-sky→transparent → crop |
| **why** | Avoid AI re-type jaggedness + rembg white blotch halos |
| **size** | {out.size[0]}×{out.size[1]} RGBA |
""",
        encoding="utf-8",
    )
    print(json.dumps({"success": True, "file": str(OUT), "bytes": OUT.stat().st_size, "size": list(out.size)}, indent=2))


if __name__ == "__main__":
    main()
