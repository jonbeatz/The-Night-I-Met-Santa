"""P01 v23: alt of v22 — scenery TOP, empty text space BOTTOM. FRAME ON."""
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
OUT_DIR = ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v23"
OUT_FILE = OUT_DIR / "art-P01-title-gemini-fal.png"

REFS = [
    ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v22" / "art-P01-title-gemini-fal.png",
    ROOT / "Images" / "styles2" / "spread-Frame-Style1.png",
    ROOT / "Images" / "styles2" / "p21-beat12-13-note-LEFT.png",
]

PROMPT = """Edit this title-page illustration carefully — keep the SAME paint style, watercolor frame,
fireplace+stockings LEFT, Christmas tree RIGHT, simplified decor, soft heirloom look.

CRITICAL COMPOSITION FLIP:
- Move the WHOLE scenic vignette to the UPPER portion of the frame.
- Put the generous empty cream/soft watercolor wash space for typography at the BOTTOM
  (soft feathered painted edge into open paper below the scene — like a matter-about text band).
- Do NOT leave the big empty zone at the top anymore.

KEEP:
- WATERCOLOR FRAME ON: soft irregular white/cream vignette, feathered edges (styles2 look)
- No hard ceiling lines / no crown molding
- Simple decor (not busy)
- No people, no faces, no text, no letters, no watermark

Square 1:1, print-ready gouache/watercolor storybook quality.
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
    urls = []
    for p in REFS:
        if not p.is_file():
            raise SystemExit(f"missing {p}")
        print("upload", p.name)
        urls.append(upload(p))
    body = {
        "prompt": PROMPT,
        "image_urls": urls,
        "num_images": 1,
        "output_format": "png",
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "limit_generations": True,
        "safety_tolerance": "4",
        "seed": 723101,
    }
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
        raise SystemExit(result)
    url = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as r:
        OUT_FILE.write_bytes(r.read())
    (OUT_DIR / "RECIPE.md").write_text(
        f"""# RECIPE — P01-title / v23

| Field | Value |
|-------|--------|
| **base** | v22 (Jon loved) |
| **model** | `{ENDPOINT}` |
| **FRAME** | **ON** |
| **layout** | scenery **TOP** · empty text wash **BOTTOM** |
| **output** | **one file:** `{OUT_FILE.name}` |
| **seed** | 723101 |
""",
        encoding="utf-8",
    )
    print(json.dumps({"success": True, "file": str(OUT_FILE), "bytes": OUT_FILE.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
