"""Clean logo from cleanLogo.png — Gemini on white, Pillow alpha (NO rembg)."""
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
GEMINI = "fal-ai/gemini-3-pro-image-preview/edit"

PROMPT = """Recreate this EXACT book title logo as a CLEAN, SHARP, HIGH-RESOLUTION print graphic.

KEEP exactly:
- \"The Night I Met Santa\" ornate metallic GOLD decorative serif with elegant swashes
- Gold star ornament line above the title
- Gold underline flourish below the title  
- \"Written By Jack Farrell\" in clean smaller LIGHT GOLD / champagne serif under the title
  (NOT pure white — must stay visible when white background is keyed out)
- Small gold sparkle stars in the lettering like the cleanLogo reference

QUALITY (critical):
- Perfectly smooth sharp letter edges — NO jagged pixels, NO aliasing
- Smooth even gold metal fill — NO white blotches inside letters
- Crisp vector-like clarity

BACKGROUND: flat solid pure WHITE (#FFFFFF) only — no night sky, moon, buildings, glow mist, or vignette.
Landscape 16:9 title card. No extra words.
"""


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


def white_to_alpha(im: Image.Image, threshold: int = 245) -> Image.Image:
    """Turn near-white background transparent; keep gold + white credit text."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            # Pure / near-white paper → transparent
            if r >= threshold and g >= threshold and b >= threshold:
                px[x, y] = (0, 0, 0, 0)
                continue
            # Soft anti-alias fringe: mostly white → partial alpha
            mn = min(r, g, b)
            if mn > 220 and abs(r - g) < 12 and abs(g - b) < 12:
                # Keep slight warmth only if clearly gold-tinted
                if r > g + 15 or r > b + 15:
                    continue
                alpha = max(0, 255 - int((mn - 200) * 4))
                px[x, y] = (r, g, b, alpha)
    return im


def crop_content(im: Image.Image, pad: int = 24) -> Image.Image:
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
    print("Gemini clean logo @ 2K from cleanLogo…")
    result = fal_run(
        GEMINI,
        {
            "prompt": PROMPT,
            "image_urls": [upload(REF)],
            "num_images": 1,
            "output_format": "png",
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "limit_generations": True,
            "safety_tolerance": "4",
            "seed": 991202,
        },
    )
    imgs = result.get("images") or []
    url = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
    raw = Path(os.environ.get("TEMP", ".")) / "logo-white-plate.png"
    with urllib.request.urlopen(url) as r:
        raw.write_bytes(r.read())
    plate = Image.open(raw).convert("RGBA")
    print("plate", plate.size)

    out = crop_content(white_to_alpha(plate, threshold=242))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT)
    raw.unlink(missing_ok=True)

    (OUT.parent / "cover-title-logo.recipe.md").write_text(
        f"""# cover-title-logo.recipe.md

| Field | Value |
|-------|--------|
| **file** | `Media/approved/covers/cover-title-logo.png` |
| **main ref** | `Images/styles1/cleanLogo.png` |
| **model** | `{GEMINI}` @ 2K |
| **alpha** | Pillow white→transparent (**no rembg** — avoids blotchy halos) |
| **size** | {out.size[0]}×{out.size[1]} |
| **seed** | 991202 |
""",
        encoding="utf-8",
    )
    print(json.dumps({"success": True, "file": str(OUT), "bytes": OUT.stat().st_size, "size": list(out.size)}, indent=2))


if __name__ == "__main__":
    main()
