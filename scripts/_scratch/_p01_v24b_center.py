"""P01 v24b: stronger center band — equal top+bottom text wash."""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
load_dotenv(ROOT / ".env.local")
KEY = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
ENDPOINT = "fal-ai/gemini-3-pro-image-preview/edit"
OUT_DIR = ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v24"
OUT_FILE = OUT_DIR / "art-P01-title-gemini-fal.png"

REFS = [
    ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v22" / "art-P01-title-gemini-fal.png",
    ROOT / "Images" / "styles2" / "spread-Frame-Style1.png",
]

PROMPT = """Recompose this title-page art for a VERTICALLY CENTERED scenic band.

Layout (strict):
- Imagine the square divided into three bands.
- TOP ~25–30%: empty soft cream watercolor wash ONLY (for title text later).
- MIDDLE ~40–50%: the fireplace + Christmas tree scene (scaled smaller so it fits comfortably).
- BOTTOM ~25–30%: empty soft cream watercolor wash ONLY (for author/credit text later).
- TOP and BOTTOM empty bands should feel roughly EQUAL — do NOT pin the scenery to the bottom.

Keep paint style, soft watercolor frame vignette, simplified fireplace LEFT + tree RIGHT,
no hard ceiling lines, no people, no text, no letters. Square 1:1.
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


def main() -> None:
    urls = [upload(p) for p in REFS]
    body = {
        "prompt": PROMPT,
        "image_urls": urls,
        "num_images": 1,
        "output_format": "png",
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "limit_generations": True,
        "safety_tolerance": "4",
        "seed": 724202,
    }
    req = urllib.request.Request(
        f"https://fal.run/{ENDPOINT}",
        data=json.dumps(body).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        result = json.loads(r.read().decode())
    url = result["images"][0]["url"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as r:
        OUT_FILE.write_bytes(r.read())
    (OUT_DIR / "RECIPE.md").write_text(
        f"""# RECIPE — P01-title / v24

| Field | Value |
|-------|--------|
| **layout** | scenery **CENTER band** · open wash **TOP + BOTTOM** (roughly equal) |
| **model** | `{ENDPOINT}` |
| **FRAME** | **ON** |
| **seed** | 724202 (re-roll for stronger centering) |
| **output** | `{OUT_FILE.name}` |
""",
        encoding="utf-8",
    )
    print(json.dumps({"success": True, "file": str(OUT_FILE), "bytes": OUT_FILE.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
