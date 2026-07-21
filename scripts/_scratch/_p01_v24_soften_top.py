"""P01 v24 pass3: regenerate centered vignette with soft TOP frame like bottom."""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
load_dotenv(ROOT / ".env.local")
KEY = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
if not KEY:
    raise SystemExit("FAL_API_KEY missing")

ENDPOINT = "fal-ai/gemini-3-pro-image-preview/edit"
OUT_DIR = ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v24"
OUT_FILE = OUT_DIR / "art-P01-title-gemini-fal.png"

REFS = [
    ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v22" / "art-P01-title-gemini-fal.png",
    ROOT / "Images" / "styles2" / "spread-Frame-Style1.png",
]

PROMPT = """Create a NEW square children's Christmas TITLE PAGE plate from these references.

FROM Image 1 (keep the same scene and paint):
- Cozy stone fireplace LEFT with fire, garland + lights, three stockings
- Decorated Christmas tree RIGHT with ornaments, lights, three gift boxes, rug
- Soft heirloom watercolor/gouache look, warm cream paper

NEW LAYOUT (important):
- Place the painted vignette in the VERTICAL MIDDLE of the square
- Leave generous OPEN CREAM paper ABOVE the art (for book title)
- Leave generous OPEN CREAM paper BELOW the art (for author credit)
- Scenery about half the page tall — not full-bleed, not stuck to the bottom

WATERCOLOR FRAME — all four sides must match:
- Soft irregular wet watercolor bleed / feathered vignette on TOP, BOTTOM, LEFT, and RIGHT
- Match Image 2's soft frame edge language
- TOP edge must NOT be a straight cropped line — it must dissolve into cream with uneven translucent brush fades like the bottom edge
- Chimney and warm wall wash gently feather upward into cream

STRICT:
- No people, no text, no letters, no logos, no watermark
- Do not duplicate or ghost the scene
- Do not pin the scenery to the bottom of the page
"""


def fal_headers(json_body: bool = False) -> dict:
    h = {"Authorization": f"Key {KEY}"}
    if json_body:
        h["Content-Type"] = "application/json"
    return h


def upload(path: Path) -> str:
    ctype = "image/png"
    req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps({"file_name": path.name, "content_type": ctype}).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        meta = json.loads(r.read().decode())
    put = urllib.request.Request(
        meta["upload_url"],
        data=path.read_bytes(),
        method="PUT",
        headers={"Content-Type": ctype},
    )
    with urllib.request.urlopen(put) as r:
        if r.status not in (200, 201):
            raise RuntimeError(f"upload PUT {r.status}")
    return meta["file_url"]


def main() -> None:
    urls = []
    for p in REFS:
        if not p.is_file():
            raise SystemExit(f"missing {p}")
        urls.append(upload(p))
        print(f"uploaded {p.name}")

    body = {
        "prompt": PROMPT,
        "image_urls": urls,
        "num_images": 1,
        "output_format": "png",
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "limit_generations": True,
        "safety_tolerance": "4",
        "seed": 724301,
    }
    print("fal Gemini — centered soft-frame v24…")
    req = urllib.request.Request(
        f"https://fal.run/{ENDPOINT}",
        data=json.dumps(body).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        result = json.loads(r.read().decode())

    imgs = result.get("images") or []
    if not imgs:
        raise SystemExit(f"no images: {json.dumps(result)[:1500]}")
    img_url = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
    with urllib.request.urlopen(img_url) as r:
        OUT_FILE.write_bytes(r.read())
    print(f"wrote {OUT_FILE}")


if __name__ == "__main__":
    main()
