"""Extract cover title logo to transparent PNG (crop + fal rembg). ONE file."""
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
OUT_DIR = ROOT / "Media" / "approved" / "covers"
CROP = OUT_DIR / "_tmp_cover-title-crop.png"
OUT = OUT_DIR / "cover-title-logo.png"  # single canonical asset
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


def main() -> None:
    img = Image.open(COVER).convert("RGBA")
    w, h = img.size
    # Top title block on locked beige-v2 cover (title + credit line + flourish)
    top = int(h * 0.02)
    bottom = int(h * 0.28)
    left = int(w * 0.05)
    right = int(w * 0.95)
    crop = img.crop((left, top, right, bottom))
    crop.save(CROP)
    print(f"crop {crop.size} -> {CROP}")

    url = upload(CROP)
    print("uploaded crop")
    body = {"image_url": url}
    req = urllib.request.Request(
        f"https://fal.run/{REMBG}",
        data=json.dumps(body).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        result = json.loads(r.read().decode())

    # rembg returns image url in various shapes
    out_url = None
    if isinstance(result.get("image"), dict):
        out_url = result["image"].get("url")
    elif isinstance(result.get("image"), str):
        out_url = result["image"]
    elif result.get("images"):
        im0 = result["images"][0]
        out_url = im0.get("url") if isinstance(im0, dict) else im0
    if not out_url:
        raise SystemExit(json.dumps(result)[:2000])

    with urllib.request.urlopen(out_url) as r:
        OUT.write_bytes(r.read())
    CROP.unlink(missing_ok=True)

    # Verify alpha
    check = Image.open(OUT)
    has_alpha = check.mode == "RGBA" and any(px[3] < 255 for px in check.getdata())
    recipe = OUT_DIR / "cover-title-logo.recipe.md"
    recipe.write_text(
        f"""# cover-title-logo.recipe.md

| Field | Value |
|-------|--------|
| **file** | `Media/approved/covers/cover-title-logo.png` |
| **source** | Locked `cover-front.png` (beige-v2) title block crop |
| **process** | Crop top title region → fal `{REMBG}` → RGBA PNG |
| **contents** | Full cover title treatment: *The Night I Met Santa* + flourish + *Written By Jack Farrell* |
| **use** | Overlay on covers / comps — transparent background |
| **note** | Exact baked lettering from locked cover (not a re-type). Live type in InDesign still preferred for P01 interior. |
""",
        encoding="utf-8",
    )
    print(json.dumps({
        "success": True,
        "file": str(OUT),
        "bytes": OUT.stat().st_size,
        "size": list(check.size),
        "mode": check.mode,
        "has_transparency": has_alpha,
    }, indent=2))


if __name__ == "__main__":
    main()
