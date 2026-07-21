"""P01 v21: from v20 — scenery a bit lower, NO chair. ONE file."""
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
OUT_DIR = ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v21"
OUT_FILE = OUT_DIR / "art-P01-title-gemini-fal.png"

REFS = [
    OUT_DIR.parent / "v20" / "art-P01-title-gemini-fal.png",
    ROOT / "Images" / "styles1" / "matter-about-story.png",
    ROOT / "Images" / "styles1" / "p21-beat12-13-note-LEFT.png",
]

PROMPT = """Edit this title-page illustration carefully.

KEEP: soft cream watercolor paper frame / vignette (p21 style), heirloom painted look,
fireplace with stockings, Christmas tree with a few presents, warm glow.

CHANGES:
1) Move the ENTIRE scenic vignette DOWN a little more so the TOP has MORE open cream/white
   watercolor space for title typography (more top margin than the input).
2) REMOVE the armchair / wingback chair completely — do not replace it with other furniture.
3) Gently adjust the composition so the fireplace + tree still feel balanced without the chair
   (maybe slightly more breathing room on the right, or a bit more tree/gifts presence).

Still NOT full-bleed. Soft irregular watercolor edges into cream paper.
No people, no faces, no text, no letters, no watermark. Square 1:1.
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
    urls = [upload(p) for p in REFS if p.is_file() or (_ for _ in ()).throw(SystemExit(f"missing {p}"))]
    for p, u in zip(REFS, urls):
        print("uploaded", p.name)
    body = {
        "prompt": PROMPT,
        "image_urls": urls,
        "num_images": 1,
        "output_format": "png",
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "limit_generations": True,
        "safety_tolerance": "4",
        "seed": 721201,
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
        f"""# RECIPE — P01-title / v21

| Field | Value |
|-------|--------|
| **base** | v20 |
| **model** | `{ENDPOINT}` |
| **changes** | scenery lower · **no chair** · more top cream for title |
| **output** | **one file:** `{OUT_FILE.name}` |
| **seed** | 721201 |
""",
        encoding="utf-8",
    )
    print(json.dumps({"success": True, "file": str(OUT_FILE), "bytes": OUT_FILE.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
