"""Cover title logo: Gemini recreate on green → rembg → clean RGBA. ONE file."""
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
TMP_GREEN = ROOT / "Media" / "approved" / "covers" / "_tmp_title-green.png"

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
    print("crop", crop.size)

    crop_url = upload(TMP_CROP)
    prompt = (
        "Recreate ONLY the exact cover TITLE LOGO treatment from this reference: "
        "ornate golden glowing serif title reading exactly \"The Night I Met Santa\", "
        "with the delicate golden flourish/star line above, and below it the credit line "
        "exactly \"Written By Jack Farrell\" in smaller lighter serif. "
        "Match the metallic gold glow, flourishes, and letterforms as closely as possible. "
        "Place the FULL logo centered on a flat solid pure chroma-key GREEN background "
        "RGB(0,255,0) — no room, no boy, no tree, no scene, no texture, no vignette. "
        "Wide landscape title-card composition. No extra words."
    )
    print("Gemini recreate on green…")
    result = fal_run(
        GEMINI,
        {
            "prompt": prompt,
            "image_urls": [crop_url],
            "num_images": 1,
            "output_format": "png",
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "limit_generations": True,
            "safety_tolerance": "4",
            "seed": 880011,
        },
    )
    imgs = result.get("images") or []
    if not imgs:
        raise SystemExit(result)
    gurl = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
    download(gurl, TMP_GREEN)
    print("green plate", TMP_GREEN.stat().st_size)

    print("rembg…")
    rembg = fal_run(REMBG, {"image_url": upload(TMP_GREEN)})
    out_url = None
    if isinstance(rembg.get("image"), dict):
        out_url = rembg["image"].get("url")
    elif isinstance(rembg.get("image"), str):
        out_url = rembg["image"]
    if not out_url:
        raise SystemExit(rembg)
    download(out_url, OUT)

    TMP_CROP.unlink(missing_ok=True)
    TMP_GREEN.unlink(missing_ok=True)

    check = Image.open(OUT)
    a = check.split()[-1] if check.mode == "RGBA" else None
    zeros = a.histogram()[0] if a else 0
    (OUT.parent / "cover-title-logo.recipe.md").write_text(
        f"""# cover-title-logo.recipe.md

| Field | Value |
|-------|--------|
| **file** | `Media/approved/covers/cover-title-logo.png` |
| **source lock** | `cover-front.png` (beige-v2) title treatment |
| **process** | Title crop → fal `{GEMINI}` recreate on chroma green → `{REMBG}` |
| **contents** | *The Night I Met Santa* + flourish + *Written By Jack Farrell* |
| **format** | RGBA transparent PNG |
| **size** | {check.size[0]}×{check.size[1]} · mode {check.mode} |
| **note** | Separate asset for comps/overlays. Interior P01 still uses live Cinzel in InDesign when preferred. |
""",
        encoding="utf-8",
    )
    print(json.dumps({
        "success": True,
        "file": str(OUT),
        "bytes": OUT.stat().st_size,
        "size": list(check.size),
        "mode": check.mode,
        "fully_transparent_px": zeros,
    }, indent=2))


if __name__ == "__main__":
    main()
