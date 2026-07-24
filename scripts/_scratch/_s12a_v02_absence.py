#!/usr/bin/env python3
"""S12a Blessing v02 — exterior absence/departure spread. No boy. No full interior."""
from __future__ import annotations

import io
import json
import os
import shutil
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
S12A = ROOT / "Media/development/S12a-blessing"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

S11L = ROOT / "Media/development/S11-wish/art-left.png"
HOUSE = ROOT / "Images/styles3/cover-front.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
S8L = ROOT / "Media/development/S08-gone/art-left.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Wide seamless Christmas storybook SPREAD 5250x2625. NO fake gutter, NO spine shadow, NO text.
ABSENCE / DEPARTURE beat — NO boy, NO child, NO person inside the room, NO figure reading a letter.
Breaks interior boy-repetition. Atmosphere and departure only.

IMAGE 1 = moonlit window from inside (burgundy room language, frosted panes, moonlight beams).
IMAGE 2 = decorative snow house exterior for the outside view on the right half.
IMAGE 3 = soft watercolor vignette / page-edge frame reference — use a quiet soft vignette edge.

Rich oil-painting quality. Deep blue night sky continuity across BOTH pages. Soft vignette frame.

LEFT half (p26) — FROM INSIDE looking OUT through the night window:
Frosted multi-pane window frame. Moonlight streams in through the glass (beams across dark floor).
Beyond the glass: deep blue night sky, bright full moon, and a TINY silhouette of Santa's sleigh and \
reindeer flying away into the distance (the departure — small, distant).
Interior is dark and quiet — only window frame, moonlight beams on floorboards, suggestion of \
burgundy walls in deep shadow. Empty room. No furniture focus. No boy. No Christmas tree dominating.
Quiet, still, watching Santa leave.

RIGHT half (p27) — PURE EXTERIOR continuing the same night:
Deep blue sky, scattered stars, glowing moon. Santa's sleigh is FURTHER away now — a distant speck, \
almost gone. Snow-covered evergreen trees below. The house seen from outside — warm golden light in \
ONE window. Peaceful, silent world. Magic lingering. No boy outdoors. No close Santa portrait.

Continuous sky / mood across the gutter. Soft vignette. Faces and subjects off the hard center line.
"""

NEG = (
    "boy, child, kid, person sitting, person reading, letter in hands, glowing envelope, "
    "interior living room wide shot with furniture, Christmas tree dominating left, "
    "text, letters, typography, watermark, fake gutter, spine shadow, identical mirrored halves, "
    "close-up Santa face, large Santa in room"
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


def update_poem_map() -> None:
    path = ROOT / "scripts/book_poem_map.py"
    text = path.read_text(encoding="utf-8")
    old = '''    "S12a-blessing": {
        "unit": "S12a-blessing",
        "layout": "seamless",
        "left_page": 26,
        "right_page": 27,
        "left": (
            "He said I've had enough eggnogs, cider and soups. / "
            "My belt's getting harder to fit in the loops."
        ),
        "right": "Boy still reading the letter — wide peaceful room shot.",
        "right_kind": "context",
        "title": "S12a Blessing",
    },'''
    new = '''    "S12a-blessing": {
        "unit": "S12a-blessing",
        "layout": "text_image",
        "left_page": 26,
        "right_page": 27,
        "left": (
            "He said I've had enough eggnogs, cider and soups. / "
            "My belt's getting harder to fit in the loops."
        ),
        "right": "IMAGE ONLY — pure exterior night · sleigh almost gone · absence / departure.",
        "right_kind": "context",
        "title": "S12a Blessing",
    },'''
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")
        print("poem map S12a → text_image absence")
    elif "absence / departure" in text:
        print("poem map S12a already updated")
    else:
        raise SystemExit("S12a poem map block not found")


def main() -> None:
    load_env()
    update_poem_map()
    INDEX.mkdir(parents=True, exist_ok=True)

    # Keep v01 archived in place; overwrite primary with v02
    refs = [S11L, HOUSE if HOUSE.is_file() else S8L, FRAME]
    for p in refs:
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    urls = [fal_client.upload_file(str(p)) for p in refs]
    print("=== Qwen S12a Blessing v02 absence ===")
    print("refs:", [p.name for p in refs])
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
    print("qwen raw", raw.size)

    tmp = S12A / "_tmp-v02-qwen.png"
    S12A.mkdir(parents=True, exist_ok=True)
    raw.save(tmp)
    up_url = fal_client.upload_file(str(tmp))
    up = fal_client.subscribe(
        SEEDVR,
        arguments={
            "image_url": up_url,
            "upscale_mode": "factor",
            "upscale_factor": 2,
            "noise_scale": 0.1,
            "output_format": "png",
        },
        with_logs=True,
    )
    up_im = download(up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"])
    final = up_im.resize(SPREAD, Image.Resampling.LANCZOS)
    tmp.unlink(missing_ok=True)

    v02 = S12A / "v02"
    v02.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (v02, S12A):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12a-blessing / v02

| Field | Value |
|-------|--------|
| **name** | S12a Blessing — absence / departure (no boy) |
| **layout** | FULL SPREAD seamless · TEXT+IMAGE de facto (poem all on p26) |
| **version** | v02 |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **5250×2625** triplet |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **refs** | S11 L window · cover-front house · frame-reference |

## Intent

Breaks S10/S11 boy-interior repetition. L: inside looking OUT through frosted window — tiny sleigh departure. \
R: pure exterior — sleigh almost gone, snow evergreens, warm house window. No boy. Absence.
"""
    (v02 / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (v02 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v02",
                "status": "working",
                "layout": "seamless_spread_text_image_defacto",
                "concept": "absence_departure_no_boy",
                "size": list(SPREAD),
                "seed": seed,
                "fal_url": url,
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
        INDEX / f"S12a-blessing-v02-absence-{DAY}.png",
        unit="S12a-blessing",
        version="v02",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · NO boy · absence/departure",
        subtitle="Window looking OUT L · pure exterior sky/house R · poem all on p26",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "v02 absence · NO boy · L window looking OUT tiny sleigh · R pure exterior sleigh speck + warm house window · "
        "poem ALL on p26 · board S12a-blessing-v02-absence-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] == "p26":
            p.update(
                {
                    "caption": "p26 · S12a Blessing L · v02 window OUT",
                    "path": "Media/development/S12a-blessing/art-left.png",
                    "version": "v02",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "status": "working",
                    "date": DAY,
                    "notes": "Looking OUT frosted window · tiny sleigh departure · ALL poem text · " + note,
                    "development_path": "Media/development/S12a-blessing/art.png",
                    "layout": "text_image_defacto",
                    "text_role": "all_poem_text",
                    "concept": "absence_departure",
                    "pixel_size": "2625x2625",
                    "spread_side": "L",
                }
            )
            p.pop("source_mock", None)
        if p["id"] == "p27":
            p.update(
                {
                    "caption": "p27 · S12a Blessing R · v02 exterior absence",
                    "path": "Media/development/S12a-blessing/art-right.png",
                    "version": "v02",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "status": "working",
                    "date": DAY,
                    "notes": "IMAGE ONLY · pure exterior · sleigh almost gone · warm house window · " + note,
                    "development_path": "Media/development/S12a-blessing/art.png",
                    "layout": "text_image_defacto",
                    "text_role": "none",
                    "concept": "absence_departure",
                    "pixel_size": "2625x2625",
                    "spread_side": "R",
                }
            )
            p.pop("source_mock", None)
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update(
                {
                    "page": "26|27",
                    "beat": "S12a Blessing",
                    "version": "v02",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "status": "working",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": note,
                    "layout": "text_image_defacto",
                    "concept": "absence_departure_no_boy",
                }
            )
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(FLOW.read_text(encoding="utf-8"))
    print("FLOW OK")
    print("DONE", S12A / "art.png")


if __name__ == "__main__":
    main()
