"""P01 title: quieter tree+fireplace, master watercolor (Banana edit). v09–v10."""
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

MASTER = (
    "Traditional children's Christmas picture-book illustration, heirloom storybook quality, "
    "heavily painted in rich gouache and soft watercolor with visible soft brushstrokes and "
    "gentle blended edges, NOT colored pencil NOT crayon NOT scratchy sketch lines, warm fireplace "
    "glow mixed with cool moonlight, golden ember highlights, deep crimson and forest green palette "
    "with warm cream and muted earth tones, nostalgic Golden Age painted realism, intimate cozy "
    "magical atmosphere, Charles Santore–inspired storybook painting, classic Clement C. Moore "
    "Christmas book feel, highly detailed but soft and painterly, print-ready composition, "
    "no text, no letters, no watermark"
)

SCENE = (
    "Square TITLE PAGE for a children's Christmas book. Soft quiet composition: stone fireplace "
    "on the LEFT with a gentle fire, one simple wreath, only TWO stockings max; decorated evergreen "
    "tree on the RIGHT with soft controlled lights and a few ornaments only — NOT crowded. "
    "Minimal gifts (2–3 small packages) or none. Large calm open space in the UPPER CENTER / cream "
    "ceiling wash for later typography. Soft watercolor washes, airy negative space, less busy, "
    "simplified decor, breatheable layout. No people, no faces, no text, no letters, no glyphs, "
    "no watermark, no logos."
)

REFS = [
    ROOT / "Images" / "styles1" / "p01-title.png",
    ROOT / "Media" / "approved" / "covers" / "cover-front.png",
    ROOT / "Media" / "approved" / "style-refs" / "covers" / "C-front-fireplace-stockings.png",
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


def run_edit(prompt: str, image_urls: list[str], seed: int | None = None) -> dict:
    body = {
        "prompt": prompt,
        "image_urls": image_urls,
        "num_images": 1,
        "output_format": "png",
        "aspect_ratio": "1:1",
        "resolution": "1K",
        "limit_generations": True,
        "safety_tolerance": "4",
    }
    if seed is not None:
        body["seed"] = seed
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
    print("Uploading style/composition refs…")
    urls = []
    for p in REFS:
        if not p.is_file():
            raise SystemExit(f"missing {p}")
        u = upload(p)
        print(f"  {p.name} -> {u}")
        urls.append(u)

    jobs = [
        {
            "v": "v09",
            "seed": 420091,
            "note": "Quieter fireplace+tree · watercolor master · airy upper text zone",
            "prompt": (
                f"{SCENE} Match the soft painted gouache/watercolor LOOK of the reference images "
                f"(especially the locked cover paint quality), but SIMPLIFY the busy title-room scene — "
                f"fewer objects, more empty painted space. {MASTER}"
            ),
        },
        {
            "v": "v10",
            "seed": 420092,
            "note": "Even quieter variant · fewer ornaments · softer washes",
            "prompt": (
                f"{SCENE} Even quieter and more minimal than a typical Christmas room: soft watercolor "
                f"washes, gentle vignette, sparse decorations, lots of cream/ivory negative space for a "
                f"title. Keep fireplace left + tree right. Match heirloom paint style of the refs. {MASTER}"
            ),
        },
        {
            "v": "v11",
            "seed": 420093,
            "note": "Mid quiet · soft moonlight window · restrained gifts",
            "prompt": (
                f"{SCENE} Soft night window with cool moonlight behind, warm hearth amber on the left, "
                f"tree glow on the right — balanced but NOT busy. Soft blended watercolor edges, "
                f"heirloom storybook paint. {MASTER}"
            ),
        },
    ]

    for job in jobs:
        print(f"== {job['v']} ==")
        result = run_edit(job["prompt"], urls, seed=job["seed"])
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
| **lane** | B look (quieter title dial) |
| **service** | fal.ai |
| **model** | `{ENDPOINT}` |
| **settings** | 1K · 1:1 · master watercolor · simplify busy |
| **refs** | `Images/styles1/p01-title.png` · `Media/approved/covers/cover-front.png` · `style-refs/covers/C-front-fireplace-stockings.png` |
| **concept** | {job['note']} |
| **seed** | **{job['seed']}** |
| **verdict** | pending Jon review |
| **promoted_to** | — |

## Prompt

{job['prompt']}
"""
        (OUT_BASE / job["v"] / "RECIPE.md").write_text(recipe, encoding="utf-8")
        print(f"  saved {out} ({out.stat().st_size} bytes)")
    print("DONE")


if __name__ == "__main__":
    main()
