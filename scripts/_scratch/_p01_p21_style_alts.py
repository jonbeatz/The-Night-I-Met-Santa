"""P01 title alts from styles1 B + p21 + matter-about; lock paint style to p21."""
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

OUT_BASE = ROOT / "Media" / "generated" / "mocks" / "P01-title"
ENDPOINT = "fal-ai/nano-banana-pro/edit"
STYLES = ROOT / "Images" / "styles1"

REFS = [
    STYLES / "p21-beat12-13-note-LEFT.png",  # PRIMARY style lock
    STYLES / "B-back-gifts-tree.png",
    STYLES / "matter-about-story.png",
]

STYLE_LOCK = (
    "CRITICAL: match the exact paint STYLE of the first reference image "
    "(p21-beat12-13-note-LEFT) — soft watercolor/gouache fireplace scene, "
    "warm amber hearth glow, deep maroon/burgundy walls, creamy soft washes, "
    "gentle paper texture, blended wet edges, heirloom storybook look. "
    "Do NOT use flat digital or Klein punchy contrast."
)

SCENE = (
    "Square children's Christmas TITLE PAGE illustration. Quiet composition: "
    "stone or cream fireplace on the LEFT with gentle fire; evergreen Christmas tree "
    "on the RIGHT with soft controlled lights (inspired by the gifts-tree reference). "
    "Keep decor SIMPLE — not crowded. Large calm open cream/ivory painted space "
    "(center or lower third) for later title typography — soft feathered watercolor edge "
    "into open space is OK (like the about-story reference's quiet text zone). "
    "No people, no faces, no text, no letters, no glyphs, no watermark, no logos."
)


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
            raise RuntimeError(f"PUT failed {r.status}")
    return meta["file_url"]


def run_edit(prompt: str, image_urls: list[str], seed: int) -> dict:
    body = {
        "prompt": prompt,
        "image_urls": image_urls,
        "num_images": 1,
        "output_format": "png",
        "aspect_ratio": "1:1",
        "resolution": "1K",
        "limit_generations": True,
        "safety_tolerance": "4",
        "seed": seed,
    }
    req = urllib.request.Request(
        f"https://fal.run/{ENDPOINT}",
        data=json.dumps(body).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode())


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as r:
        dest.write_bytes(r.read())


def main() -> None:
    print("Uploading refs (p21 style lock first)…")
    urls = []
    for p in REFS:
        if not p.is_file():
            raise SystemExit(f"missing {p}")
        u = upload(p)
        print(f"  {p.name} -> {u}")
        urls.append(u)

    jobs = [
        {
            "v": "v12",
            "seed": 512001,
            "note": "p21 paint lock · fireplace L + tree R · open cream center",
            "extra": (
                "Combine the cozy fireplace warmth of p21 with a softer tree presence on the right "
                "(from B-back-gifts-tree), but leave generous quiet wall space like a title page."
            ),
        },
        {
            "v": "v13",
            "seed": 512002,
            "note": "p21 paint lock · quieter · soft lower text wash like matter-about",
            "extra": (
                "Even quieter: fewer mantel objects (clock optional), 2 stockings max, sparse tree ornaments, "
                "soft painted fade into cream lower or center zone for typography (matter-about vibe)."
            ),
        },
        {
            "v": "v14",
            "seed": 512003,
            "note": "p21 paint lock · tree-weighted right · open left cream wall",
            "extra": (
                "Weight the Christmas tree and a few gifts toward the right (B-back mood); "
                "keep a quieter fireplace glow on the left; large pale cream open area for title."
            ),
        },
    ]

    for job in jobs:
        prompt = f"{STYLE_LOCK} {SCENE} {job['extra']}"
        print(f"== {job['v']} ==")
        result = run_edit(prompt, urls, seed=job["seed"])
        imgs = result.get("images") or []
        if not imgs:
            print("  FAIL", result)
            continue
        img_url = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
        out = OUT_BASE / job["v"] / "art-P01-title-dial.png"
        download(img_url, out)
        recipe = f"""# RECIPE — P01-title / {job['v']}

| Field | Value |
|-------|--------|
| **unit** | P01-title |
| **book page** | 1 (Title · SINGLE · right) |
| **version** | {job['v']} |
| **date** | 2026-07-20 |
| **lane** | B (Banana edit · p21 style lock) |
| **service** | fal.ai |
| **model** | `{ENDPOINT}` |
| **settings** | 1K · 1:1 · seed {job['seed']} |
| **style lock** | `Images/styles1/p21-beat12-13-note-LEFT.png` |
| **other refs** | `B-back-gifts-tree.png` · `matter-about-story.png` |
| **concept** | {job['note']} |
| **verdict** | pending Jon review |
| **promoted_to** | — |

## Prompt

{prompt}
"""
        (OUT_BASE / job["v"] / "RECIPE.md").write_text(recipe, encoding="utf-8")
        print(f"  saved {out} ({out.stat().st_size} bytes)")
    print("DONE")


if __name__ == "__main__":
    main()
