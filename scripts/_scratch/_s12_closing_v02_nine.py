#!/usr/bin/env python3
"""S12-closing v02 — remove duplicate Santa; 9 reindeer (lead + 4 pairs)."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/development/S12-closing"
S12B = ROOT / "Media/development/S12b-god-bless"
S12A = ROOT / "Media/development/S12a-blessing"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

# Prefer latest primary (mirrored to S12b); fall back to S12-closing
BASE_CANDIDATES = [
    S12B / "art.png",
    OUT / "art.png",
    OUT / "v01b" / "art.png",
]
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Edit this seamless Christmas FINAL STORY IMAGE spread 5250x2625. KEEP the strong main Santa and sleigh.

TWO CRITICAL FIXES ONLY:

1) REMOVE the DUPLICATE small Santa + reindeer + sleigh floating over / above the Victorian house \
on the RIGHT. Delete that second set ENTIRELY. Only ONE Santa and ONE sleigh — the main large team \
crossing the upper sky from left toward the right. No second ghost team. Clean night sky above the house \
except for stars and the North Star.

2) REINDEER COUNT = exactly NINE (9). Classic team: one lead reindeer in front + four pairs behind \
(two-by-two). Clear antlers, warm brown fur, full painted oil-painting style — NOT silhouettes, \
NOT black cutouts. Harness lines connecting them to the single sleigh. Readable as nine animals.

KEEP UNCHANGED: deep blue night sky, detailed full moon upper LEFT, sacred North Star with golden \
cross/gleam upper RIGHT, Victorian house with warm golden windows below, snowman with scarf in yard, \
snow-covered evergreens, soft vignette frame, rich oil quality. Main Santa = open red coat over \
blue-and-white striped shirt with suspenders (Santa G0 v2), painted — not silhouette. Sleigh with gifts. \
Magic sparkle trail OK behind the ONE sleigh.

IMAGE 2 = Santa G0 v2 identity lock for the single Santa only.

NO boy. NO baked text. NO fake gutter. NO second Santa anywhere in the image.
"""

NEG = (
    "second Santa, duplicate sleigh, small ghost sleigh over house, twin teams, "
    "silhouette reindeer, black cutout deer, only 2 reindeer, only 4 reindeer, "
    "text, watermark, boy, fake gutter"
)


def load_env() -> None:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def download(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def main() -> None:
    load_env()
    base_path = next((p for p in BASE_CANDIDATES if p.is_file() and p.stat().st_size > 0), None)
    if not base_path:
        raise SystemExit("no base art")
    print("base:", base_path)

    base = Image.open(base_path).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    tmp_in = OUT / "_tmp-v02-in.png"
    base.save(tmp_in)

    urls = [fal_client.upload_file(str(tmp_in)), fal_client.upload_file(str(SANTA))]
    print("=== Qwen S12-closing v02 · 9 reindeer · no duplicate ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": urls,
            "image_size": {"width": 2048, "height": 1024},
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checker": True,
            "enable_prompt_expansion": True,
        },
        with_logs=True,
    )
    print(result)
    url = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(url)
    tmp_q = OUT / "_tmp-v02-qwen.png"
    raw.save(tmp_q)
    up = fal_client.subscribe(
        SEEDVR,
        arguments={
            "image_url": fal_client.upload_file(str(tmp_q)),
            "upscale_mode": "factor",
            "upscale_factor": 2,
            "noise_scale": 0.1,
            "output_format": "png",
        },
        with_logs=True,
    )
    up_im = download(up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"])
    final = up_im.resize(SPREAD, Image.Resampling.LANCZOS)
    tmp_in.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v02"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT, S12A, S12B):
        dest.mkdir(parents=True, exist_ok=True)
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-closing / v02

| Field | Value |
|-------|--------|
| **fix** | Remove duplicate Santa over house · **9 reindeer** (lead + 4 pairs) |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **base** | `{base_path.relative_to(ROOT).as_posix()}` |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v02",
                "status": "working",
                "reindeer_count": 9,
                "fix": ["remove_duplicate_santa", "nine_reindeer_pairs"],
                "seed": seed,
                "fal_url": url,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-closing-v02-nine-reindeer-{DAY}.png",
        unit="S12-closing",
        version="v02",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · NO duplicate · 9 reindeer (lead+4 pairs)",
        subtitle="One Santa · nine deer two-by-two · moon L · North Star R · house+snowman",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-closing v02 · ONE Santa only (duplicate removed) · 9 reindeer lead+4 pairs · "
        "moon L · North Star R · house+snowman · Media/development/S12-closing/ · "
        "board S12-closing-v02-nine-reindeer-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            p.update(
                {
                    "version": "v02",
                    "date": DAY,
                    "status": "working",
                    "notes": note,
                    "path": f"Media/development/S12-closing/art-{'left' if p['id']=='p26' else 'right'}.png",
                    "development_path": "Media/development/S12-closing/art.png",
                    "caption": (
                        "p26 · S12 Closing L · v02 · 9 reindeer"
                        if p["id"] == "p26"
                        else "p27 · S12 Closing R · v02 · North Star"
                    ),
                }
            )
        if p["id"] in ("p28", "p29"):
            p["notes"] = "Absorbed into S12-closing v02 — " + note
            p["date"] = DAY
            p["version"] = "merged-v02"
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update(
                {
                    "version": "v02",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                }
            )
        if d.get("page") == "28|29":
            d["notes"] = "MERGED into S12-closing v02 — " + note
            d["date"] = DAY
            d["version"] = "merged-v02"
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(FLOW.read_text(encoding="utf-8"))
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
