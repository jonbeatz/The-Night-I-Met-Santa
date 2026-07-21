"""P01 v22: reimagine styles2/p01-title — FRAME ON, simpler, open top, no hard ceiling."""
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
OUT_DIR = ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v22"
OUT_FILE = OUT_DIR / "art-P01-title-gemini-fal.png"

REFS = [
    ROOT / "Images" / "styles2" / "p01-title.png",
    ROOT / "Images" / "styles2" / "spread-Frame-Style1.png",
    ROOT / "Images" / "styles2" / "p21-beat12-13-note-LEFT.png",
    ROOT / "Media" / "approved" / "covers" / "cover-front.png",
]

PROMPT = """Reimagine this Christmas TITLE PAGE illustration.

KEEP the cozy mood: stone fireplace LEFT with stockings, decorated Christmas tree RIGHT,
warm heirloom gouache/watercolor storybook paint (match locked cover paint quality).

SIMPLIFY: fewer ornaments, fewer gifts (2–4 packages), less clutter on the mantel,
calmer room — still festive, not busy.

COMPOSITION:
- Move the WHOLE scene slightly DOWNWARD so the TOP has generous empty cream/soft wash
  space for later title typography.
- NO hard ceiling lines, NO crown molding, NO sharp architectural ceiling edge —
  soft blended watercolor wash into open paper at the top (no ruled room box).
- Soft night window / moon OK but keep it quiet.

WATERCOLOR FRAME ON: soft irregular white/cream watercolor paper vignette around the scene —
feathered painted edges bleeding into open paper, hand-painted storybook plate (not a hard
rectangle crop, not full-bleed edge-to-edge). Match styles2 frame refs (spread-Frame-Style1 / p21).

Traditional children's Christmas picture-book illustration, rich gouache and soft watercolor,
NOT colored pencil, Charles Santore–inspired, no people, no faces, no text, no letters,
no watermark. Square 1:1.
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
    print(f"endpoint={ENDPOINT}")
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
        "seed": 722101,
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
        f"""# RECIPE — P01-title / v22

| Field | Value |
|-------|--------|
| **lane** | B finals |
| **model** | `{ENDPOINT}` |
| **FRAME** | **ON** |
| **base** | `Images/styles2/p01-title.png` |
| **frame refs** | spread-Frame-Style1 · p21 |
| **changes** | simpler · open top for text · no hard ceiling lines · watercolor frame |
| **output** | **one file:** `{OUT_FILE.name}` |
| **seed** | 722101 |
""",
        encoding="utf-8",
    )
    print(json.dumps({"success": True, "file": str(OUT_FILE), "bytes": OUT_FILE.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
