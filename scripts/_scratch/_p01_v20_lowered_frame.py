"""P01 v20: matter-about scene lowered + p21 white watercolor frame. ONE file."""
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
OUT_DIR = ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v20"
OUT_FILE = OUT_DIR / "art-P01-title-gemini-fal.png"

REFS = [
    ROOT / "Images" / "styles1" / "matter-about-story.png",
    ROOT / "Images" / "styles1" / "p21-beat12-13-note-LEFT.png",
    ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v19" / "art-P01-title-gemini-fal.png",
]

PROMPT = """Create a square children's Christmas TITLE PAGE illustration.

COMPOSITION (critical):
- Move the WHOLE scenic illustration DOWNWARD in the frame so the TOP third is mostly open cream/white watercolor wash for title typography.
- Use a soft WHITE / cream WATERCOLOR FRAME / vignette on all sides — soft irregular painted edges bleeding into paper white — like the p21-beat12-13-note-LEFT reference. NOT full-bleed edge-to-edge. NOT a hard rectangle crop. The scene should feel floating on watercolor paper with airy margins.
- Bottom can also have soft cream wash like matter-about-story.

SCENE content (inspired by matter-about-story):
- Cozy Christmas living room: fireplace with stockings on the LEFT, decorated Christmas tree, warm wingback chair OK, soft armchair throw, a few presents.
- Keep the heirloom soft watercolor/gouache paint of the references.
- Warm hearth glow, deep warm walls, gentle brushwork.

Do NOT place any text, letters, or glyphs in the image. No people, no faces, no watermark, no logos.
Square 1:1, print-ready painted storybook quality.
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
        meta["upload_url"],
        data=path.read_bytes(),
        method="PUT",
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
        u = upload(p)
        print(f"uploaded {p.name}")
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
        "seed": 720101,
    }
    print("calling fal Gemini…")
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
        raise SystemExit(json.dumps(result)[:1500])
    img_url = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(img_url) as r:
        OUT_FILE.write_bytes(r.read())

    for twin in ("art.png", "art-P01-title-dial.png", "art-P01-title-gemini.png"):
        t = OUT_DIR / twin
        if t.exists():
            t.unlink()

    (OUT_DIR / "RECIPE.md").write_text(
        f"""# RECIPE — P01-title / v20

| Field | Value |
|-------|--------|
| **version** | v20 |
| **model** | `{ENDPOINT}` |
| **resolution** | 2K |
| **concept** | matter-about scene · scenery LOWERED · top open for title · p21 white watercolor frame |
| **refs** | matter-about-story · p21 · v19 |
| **output** | **one file:** `{OUT_FILE.name}` |
| **seed** | 720101 |

## Prompt

{PROMPT}
""",
        encoding="utf-8",
    )
    print(json.dumps({"success": True, "file": str(OUT_FILE), "bytes": OUT_FILE.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
