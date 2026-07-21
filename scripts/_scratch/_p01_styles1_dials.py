"""Upload styles1 refs + Klein 4B edit → P01 title dials v05–v08 (no art.png twin)."""
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

STYLES = ROOT / "Images" / "styles1"
OUT_BASE = ROOT / "Media" / "generated" / "mocks" / "P01-title"
ENDPOINT = "fal-ai/flux-2/klein/4b/edit"

D2 = (
    "KLEIN STYLE (mockups only): deep shadowed areas vs warm glow, strong punchy contrast, "
    "opaque gouache feel. Christmas lights warm and luminous but CONTROLLED — soft bloom, "
    "ornaments readable, NOT blown-out white glare. Soft blended edges. "
    "NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated."
)

JOBS = [
    {
        "v": "v05",
        "ref": "p01-title.png",
        "concept": "Fresh title alt from styles1 p01-title (fireplace + tree + moon window)",
        "prompt": (
            "Create a NEW alternate square children's Christmas TITLE PAGE illustration inspired by "
            "this reference's painterly gouache/watercolor look, colors, and cozy heirloom mood — "
            "do not copy the reference exactly. Quiet Christmas Eve living room: stone fireplace with "
            "stockings, decorated evergreen tree with controlled warm lights, night window with moon, "
            "calm open upper area for later typography. No people, no faces, no text, no letters, no glyphs, "
            "no watermark, no white text bar. " + D2
        ),
    },
    {
        "v": "v06",
        "ref": "matter-dedication.png",
        "concept": "Fresh title alt from styles1 matter-dedication (soft vignette frame)",
        "prompt": (
            "Create a NEW alternate square children's Christmas TITLE PAGE illustration inspired by "
            "this reference's soft watercolor vignette framing, warm cream center, stocking and tree "
            "ornament mood — do not copy exactly. Leave a large calm open center/upper zone for later "
            "title typography. Soft painted edges, heirloom gift-book feel. No people, no faces, no text, "
            "no letters, no glyphs, no watermark. " + D2
        ),
    },
    {
        "v": "v07",
        "ref": "D-back-living-room.png",
        "concept": "Fresh title alt from styles1 D-back-living-room (tree + doorway glow)",
        "prompt": (
            "Create a NEW alternate square children's Christmas TITLE PAGE illustration inspired by "
            "this reference's watercolor living-room look: glowing Christmas tree, wrapped gifts, "
            "open doorway into a darker hallway — do not copy exactly. Full painted scene (no blank white "
            "text slab). Leave quiet lower-center or upper wall space for later typography. No people, "
            "no faces, no text, no letters, no glyphs, no watermark. " + D2
        ),
    },
    {
        "v": "v08",
        "ref": "cover-front-house.png",
        "concept": "Fresh title alt from styles1 cover-front-house (snowy house night)",
        "prompt": (
            "Create a NEW alternate square children's Christmas TITLE PAGE illustration inspired by "
            "this reference's painterly snowy night house mood, warm glowing windows, cool blue night — "
            "do not copy exactly. Quiet exterior Christmas Eve vignette; keep sky or soft snow area calm "
            "for later typography. Optional distant sleigh silhouette OK but subtle. No close faces, "
            "no text, no letters, no glyphs, no watermark. " + D2
        ),
    },
]


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


def run_edit(prompt: str, image_url: str) -> dict:
    body = {
        "prompt": prompt,
        "image_urls": [image_url],
        "num_inference_steps": 8,
        "num_images": 1,
        "output_format": "png",
        "image_size": "square_hd",
        "enable_safety_checker": True,
    }
    req = urllib.request.Request(
        f"https://fal.run/{ENDPOINT}",
        data=json.dumps(body).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as r:
        dest.write_bytes(r.read())


def main() -> None:
    for job in JOBS:
        ref_path = STYLES / job["ref"]
        if not ref_path.is_file():
            raise SystemExit(f"missing ref {ref_path}")
        print(f"== {job['v']} upload {job['ref']} ==")
        url = upload(ref_path)
        print("  ref_url", url)
        result = run_edit(job["prompt"], url)
        img = result["images"][0]["url"]
        seed = result.get("seed")
        out_dir = OUT_BASE / job["v"]
        dial = out_dir / "art-P01-title-dial.png"
        download(img, dial)
        # intentionally NO art.png twin — user prefers dial name only
        recipe = f"""# RECIPE — P01-title / {job['v']}

| Field | Value |
|-------|--------|
| **unit** | P01-title |
| **book page** | 1 (Title · SINGLE · right) |
| **version** | {job['v']} |
| **date** | 2026-07-20 |
| **lane** | A dial (edit) |
| **service** | fal.ai |
| **model** | `{ENDPOINT}` |
| **settings** | `num_inference_steps` **8** · Dial D2 · `square_hd` 1024² |
| **style ref** | `Images/styles1/{job['ref']}` |
| **concept** | {job['concept']} |
| **seed** | **{seed}** |
| **verdict** | pending Jon review |
| **promoted_to** | — |

## Prompt

{job['prompt']}
"""
        (out_dir / "RECIPE.md").write_text(recipe, encoding="utf-8")
        print(f"  saved {dial} ({dial.stat().st_size} bytes) seed={seed}")
    print("DONE")


if __name__ == "__main__":
    main()
