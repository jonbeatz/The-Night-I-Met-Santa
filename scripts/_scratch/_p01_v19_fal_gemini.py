"""P01 v19: fal Gemini 3 Pro edit — v18 look + fireplace & stockings. ONE output file only."""
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
OUT_DIR = ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v19"
# Single canonical file — do NOT also write art.png or art-P01-title-dial.png
OUT_FILE = OUT_DIR / "art-P01-title-gemini-fal.png"

REFS = [
    ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v18" / "art-P01-title-gemini.png",
    ROOT / "Images" / "styles1" / "p21-beat12-13-note-LEFT.png",
    ROOT / "Media" / "approved" / "covers" / "cover-front.png",
]

PROMPT = """Edit/create an alternate children's Christmas TITLE PAGE illustration.

KEEP the soft heirloom watercolor/gouache LOOK of the first reference (v18 Gemini tree spot):
gentle brush, warm cream/ivory open space, print-ready Santore-inspired storybook paint.

CHANGE the composition: add a cozy stone fireplace with Christmas stockings on the mantel
AND keep a decorated Christmas tree with a few presents under it. Fireplace on the LEFT,
tree on the RIGHT (or balanced), still relatively CLEAN — not overcrowded. Leave calm open
cream wall / sky area for later title typography.

Match fireplace/stocking paint mood from the p21 reference. Match overall paint quality of
the locked cover. Soft watercolor washes, blended edges, warm hearth glow + soft tree lights.

No people, no faces, no text, no letters, no glyphs, no watermark, no logos. Square 1:1.
Traditional children's Christmas picture-book illustration, heavily painted gouache and soft
watercolor, NOT colored pencil, NOT crayon, NOT flat cartoon.
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
    print(f"endpoint={ENDPOINT}")
    urls = []
    for p in REFS:
        if not p.is_file():
            raise SystemExit(f"missing {p}")
        u = upload(p)
        print(f"uploaded {p.name} -> {u}")
        urls.append(u)

    body = {
        "prompt": PROMPT,
        "image_urls": urls,
        "num_images": 1,
        "output_format": "png",
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "limit_generations": True,
        "safety_tolerance": "4",
        "seed": 719201,
    }
    print("calling fal Gemini 3 Pro edit @ 2K…")
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
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(img_url) as r:
        OUT_FILE.write_bytes(r.read())

    # Ensure no accidental twins in this folder
    for twin in ("art.png", "art-P01-title-dial.png", "art-P01-title-gemini.png"):
        t = OUT_DIR / twin
        if t.exists() and t.resolve() != OUT_FILE.resolve():
            t.unlink()

    recipe = f"""# RECIPE — P01-title / v19

| Field | Value |
|-------|--------|
| **unit** | P01-title |
| **version** | v19 |
| **date** | 2026-07-20 |
| **lane** | B finals (fal Gemini) |
| **service** | fal.ai |
| **model** | `{ENDPOINT}` |
| **resolution** | 2K · 1:1 |
| **base look** | v18 Gemini spot tree |
| **change** | + fireplace + stockings |
| **refs** | v18 · p21 · cover-front |
| **output** | **one file only:** `{OUT_FILE.name}` |
| **seed** | 719201 |
| **verdict** | pending Jon review |

## Prompt

{PROMPT}
"""
    (OUT_DIR / "RECIPE.md").write_text(recipe, encoding="utf-8")
    print(json.dumps({
        "success": True,
        "endpoint": ENDPOINT,
        "file": str(OUT_FILE),
        "bytes": OUT_FILE.stat().st_size,
        "description": result.get("description", "")[:200],
    }, indent=2))


if __name__ == "__main__":
    main()
