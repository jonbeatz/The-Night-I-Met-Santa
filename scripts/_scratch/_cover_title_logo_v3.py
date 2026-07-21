"""Cover title logo v3: recreate on white → rembg. Prefer exact cover lettering."""
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

COVER = ROOT / "Media" / "approved" / "covers" / "cover-front.png"
OUT = ROOT / "Media" / "approved" / "covers" / "cover-title-logo.png"
TMP_CROP = ROOT / "Media" / "approved" / "covers" / "_tmp_title-crop.png"
TMP_WHITE = ROOT / "Media" / "approved" / "covers" / "_tmp_title-white.png"
GEMINI = "fal-ai/gemini-3-pro-image-preview/edit"
REMBG = "fal-ai/imageutils/rembg"


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
    img = Image.open(COVER).convert("RGBA")
    w, h = img.size
    crop = img.crop((int(w * 0.04), int(h * 0.01), int(w * 0.96), int(h * 0.30)))
    crop.save(TMP_CROP)

    prompt = (
        "Recreate ONLY the cover TITLE LOGO from this reference as a clean standalone graphic: "
        "ornate metallic GOLD glowing serif title exactly \"The Night I Met Santa\", "
        "with the delicate GOLD flourish and star line ABOVE the title, "
        "and below in smaller gold/cream serif exactly \"Written By Jack Farrell\". "
        "Keep flourishes gold (NOT green). Match the locked cover lettering style closely. "
        "Place centered on a flat solid pure WHITE background RGB(255,255,255). "
        "No room, no boy, no tree, no scene, no vignette. Landscape title card. No extra words."
    )
    print("Gemini on white…")
    result = fal_run(
        GEMINI,
        {
            "prompt": prompt,
            "image_urls": [upload(TMP_CROP)],
            "num_images": 1,
            "output_format": "png",
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "limit_generations": True,
            "safety_tolerance": "4",
            "seed": 880022,
        },
    )
    imgs = result.get("images") or []
    gurl = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
    download(gurl, TMP_WHITE)

    rembg = fal_run(REMBG, {"image_url": upload(TMP_WHITE)})
    out_url = rembg["image"]["url"] if isinstance(rembg.get("image"), dict) else rembg.get("image")
    download(out_url, OUT)
    TMP_CROP.unlink(missing_ok=True)
    TMP_WHITE.unlink(missing_ok=True)

    check = Image.open(OUT)
    # Soft-kill near-white leftover fringe
    px = check.load()
    for y in range(check.height):
        for x in range(check.width):
            r, g, b, a = px[x, y]
            if a and r > 245 and g > 245 and b > 245:
                px[x, y] = (0, 0, 0, 0)
    check.save(OUT)

    (OUT.parent / "cover-title-logo.recipe.md").write_text(
        f"""# cover-title-logo.recipe.md

| Field | Value |
|-------|--------|
| **file** | `Media/approved/covers/cover-title-logo.png` |
| **source lock** | `cover-front.png` / beige-v2 title treatment |
| **process** | Title crop → fal `{GEMINI}` on white → `{REMBG}` → RGBA |
| **contents** | *The Night I Met Santa* + gold flourish + *Written By Jack Farrell* |
| **size** | {check.size[0]}×{check.size[1]} |
| **note** | Overlay asset. P01 interior type can still be live Cinzel in InDesign. |
""",
        encoding="utf-8",
    )
    print(json.dumps({"success": True, "file": str(OUT), "bytes": OUT.stat().st_size, "size": list(check.size)}, indent=2))


if __name__ == "__main__":
    main()
