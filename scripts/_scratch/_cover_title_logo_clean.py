"""Clean hi-res cover title logo from styles1/cleanLogo.png → transparent RGBA. ONE file."""
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
TMP = ROOT / "Media" / "approved" / "covers" / "_tmp_logo-white.png"

GEMINI = "fal-ai/gemini-3-pro-image-preview/edit"
REMBG = "fal-ai/imageutils/rembg"

PROMPT = """Recreate this EXACT book title logo as a CLEAN, SHARP, HIGH-RESOLUTION graphic for print.

KEEP layout and wording exactly:
- Main title: \"The Night I Met Santa\" in ornate metallic GOLD decorative serif with elegant swashes/flourishes
- Gold star/snowflake ornament line ABOVE the title
- Gold underline flourish BELOW the title
- Credit line: \"Written By Jack Farrell\" in clean smaller WHITE (or cream-white) serif under the title
- Small gold sparkle stars integrated in the lettering like the reference

QUALITY (critical):
- Razor-sharp smooth letter edges — NO jagged pixels, NO aliasing, NO fringing
- Smooth consistent gold metal texture — NO white blotches, NO muddy speckles inside letters
- Crisp, polished, vector-like clarity at high resolution
- Match the cleanLogo reference style closely

BACKGROUND: flat solid pure WHITE (#FFFFFF) only. No night sky, no moon, no rooftops, no vignette, no texture.
Landscape title-card composition. No extra words, no watermark.
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


def download(url: str, dest: Path) -> None:
    with urllib.request.urlopen(url) as r:
        dest.write_bytes(r.read())


def main() -> None:
    if not REF.is_file():
        raise SystemExit(f"missing {REF}")
    print("ref", REF, REF.stat().st_size)
    print("Gemini clean logo @ 2K (white plate)…")
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
            "seed": 991101,
        },
    )
    imgs = result.get("images") or []
    if not imgs:
        raise SystemExit(result)
    url = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
    download(url, TMP)
    print("white plate", TMP.stat().st_size, Image.open(TMP).size)

    print("rembg…")
    rembg = fal_run(REMBG, {"image_url": upload(TMP), "crop_to_bbox": True})
    out_url = rembg["image"]["url"] if isinstance(rembg.get("image"), dict) else rembg.get("image")
    download(out_url, OUT)

    # Clean near-white fringe only
    im = Image.open(OUT).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and r > 248 and g > 248 and b > 248:
                px[x, y] = (0, 0, 0, 0)
    im.save(OUT)
    TMP.unlink(missing_ok=True)

    (OUT.parent / "cover-title-logo.recipe.md").write_text(
        f"""# cover-title-logo.recipe.md

| Field | Value |
|-------|--------|
| **file** | `Media/approved/covers/cover-title-logo.png` |
| **main ref** | `Images/styles1/cleanLogo.png` |
| **model** | `{GEMINI}` @ 2K → `{REMBG}` |
| **goal** | Clean sharp gold title + white credit · transparent RGBA |
| **size** | {im.size[0]}×{im.size[1]} |
| **seed** | 991101 |
""",
        encoding="utf-8",
    )
    print(json.dumps({"success": True, "file": str(OUT), "bytes": OUT.stat().st_size, "size": list(im.size)}, indent=2))


if __name__ == "__main__":
    main()
