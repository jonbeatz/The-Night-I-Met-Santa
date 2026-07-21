"""P01 title: Pugicorn-like spot layout (centered tree+gifts) · our watercolor style."""
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

OUT = ROOT / "Media" / "generated" / "mocks" / "P01-title"
ENDPOINT = "fal-ai/nano-banana-pro/edit"

# Style + subject first; Pugicorn last = layout only
REFS = [
    ROOT / "Images" / "styles1" / "p21-beat12-13-note-LEFT.png",
    ROOT / "Images" / "styles1" / "B-back-gifts-tree.png",
    ROOT / "Images" / "references" / "Pugicorn-Book-Refrence" / "Pugicorn-b.jpg",
    ROOT / "Images" / "references" / "Pugicorn-Book-Refrence" / "Pugicorn-c.jpg",
]

LAYOUT = (
    "LAYOUT ONLY from the Pugicorn reference pages: clean SPOT ILLUSTRATION on a plain "
    "open background — NOT a full-bleed room, NOT wall-to-wall scene, NOT edge-to-edge painting. "
    "Large calm negative space around a single centered graphic (like a title page with one "
    "illustration floating in the middle). Soft solid or very light watercolor wash background "
    "(cream, soft ivory, or pale warm wash) — simple and airy."
)

STYLE = (
    "PAINT STYLE from our heirloom Christmas storybook refs (p21 / gifts-tree): soft watercolor "
    "and gouache, warm amber glow, visible gentle brush, blended edges, NOT flat cartoon, "
    "NOT thick comic outlines, NOT the Pugicorn character art style — only borrow their CLEAN LAYOUT."
)

SUBJECT = (
    "SUBJECT: one decorated Christmas tree centered on the page with a small cluster of wrapped "
    "presents under the tree. Soft controlled tree lights, a few ornaments, quiet magical mood. "
    "No fireplace, no furniture, no people, no pets, no unicorns, no pugs, no shop buildings. "
    "No text, no letters, no glyphs, no watermark, no logos. Square title-page composition."
)


def fal_headers(json_body: bool = False) -> dict:
    h = {"Authorization": f"Key {KEY}"}
    if json_body:
        h["Content-Type"] = "application/json"
    return h


def upload(path: Path) -> str:
    ctype = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
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
            raise RuntimeError(f"PUT failed {r.status}")
    return meta["file_url"]


def run_edit(prompt: str, urls: list[str], seed: int) -> dict:
    body = {
        "prompt": prompt,
        "image_urls": urls,
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
    print("Uploading refs…")
    urls = []
    for p in REFS:
        if not p.is_file():
            raise SystemExit(f"missing {p}")
        u = upload(p)
        print(f"  {p.name} -> {u}")
        urls.append(u)

    jobs = [
        {
            "v": "v15",
            "seed": 601101,
            "note": "Spot tree+gifts center · cream open field · p21 paint",
            "extra": "Cream/ivory open background. Tree slightly above center; gifts at base. Plenty of margin on all sides for title type above or below.",
        },
        {
            "v": "v16",
            "seed": 601102,
            "note": "Spot tree · softer pale wash · more negative space",
            "extra": "Even more negative space — smaller centered tree graphic, soft pale wash only, gifts minimal (2–3 boxes). Very clean title-page feel.",
        },
        {
            "v": "v17",
            "seed": 601103,
            "note": "Spot tree · soft warm glow pool under tree · open margins",
            "extra": "Gentle warm glow under the tree on the floor wash only — still a floating spot, not a full room. Keep wide empty margins.",
        },
    ]

    for job in jobs:
        prompt = f"{LAYOUT} {STYLE} {SUBJECT} {job['extra']}"
        print(f"== {job['v']} ==")
        result = run_edit(prompt, urls, job["seed"])
        imgs = result.get("images") or []
        if not imgs:
            print("  FAIL", result)
            continue
        img_url = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
        out = OUT / job["v"] / "art-P01-title-dial.png"
        download(img_url, out)
        recipe = f"""# RECIPE — P01-title / {job['v']}

| Field | Value |
|-------|--------|
| **unit** | P01-title |
| **version** | {job['v']} |
| **date** | 2026-07-20 |
| **lane** | B Banana edit |
| **model** | `{ENDPOINT}` |
| **layout ref** | Pugicorn-b / Pugicorn-c (spot / clean margins ONLY) |
| **style ref** | `p21-beat12-13-note-LEFT` · `B-back-gifts-tree` |
| **concept** | {job['note']} |
| **seed** | {job['seed']} |
| **verdict** | pending |

## Prompt

{prompt}
"""
        (OUT / job["v"] / "RECIPE.md").write_text(recipe, encoding="utf-8")
        print(f"  saved {out} ({out.stat().st_size} bytes)")
    print("DONE")


if __name__ == "__main__":
    main()
