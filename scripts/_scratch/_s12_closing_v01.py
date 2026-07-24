#!/usr/bin/env python3
"""S12-closing v01 — merged S12a+S12b epic FINAL STORY IMAGE. 5250×2625."""
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
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
HOUSE = ROOT / "Images/styles3/cover-front.png"
S12B = ROOT / "Media/development/S12b-god-bless/v01/art.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Wide seamless Christmas storybook SPREAD 5250x2625 — FINAL STORY IMAGE / epic closing departure.
NO fake gutter, NO spine shadow, NO baked text, NO boy, NO interior room, NO child.

IMAGE 1 = Santa G0 v2 identity LOCK — open red coat, white beard, warm painted Santa (NOT a black silhouette).
IMAGE 2 = decorative Victorian Christmas house / snow exterior reference from the title world.
IMAGE 3 = prior exterior night closing mood (house + sky) — keep oil-painting Christmas night atmosphere.

ONE continuous painted exterior night scene across both pages. Rich oil-painting quality matching S3 Eyes Met.
Soft watercolor vignette frame on the outer edges.

SKY / FLIGHT (primary story action):
Santa and his reindeer sweeping across the sky LEFT → RIGHT. FULLY PAINTED characters — same style as every \
other spread — NOT silhouettes, NOT cutout black shapes. Santa wears the open red coat (Santa G0 v2). \
Reindeer have warm brown fur with soft moonlight modeling. Sleigh has visible painted detail (runners, \
curves, soft gifts/glow optional). Softly lit by moonlight. They are flying AWAY — the sleigh is larger \
on the left half and becomes SMALLER toward the right edge, receding into the distance (the departure).

LEFT half (p26): Bright full moon glowing in deep blue night sky (upper left). Santa+sleigh+reindeer \
entering/crossing this half — clearly readable painted figures. Scattered stars. Below: snow-covered \
evergreens and the left side of the decorative Victorian house world.

RIGHT half (p27): The sleigh continues smaller, receding toward the far right. Deep blue sky with stars.
THE NORTH STAR (critical): upper RIGHT area — brighter than every other star. Distinct warm golden-white \
gleam with a soft cross-shaped shimmer or gentle sacred halo. Guiding light / promise. Clear hierarchy \
so "God bless." can sit beneath it in InDesign later. Do NOT bake any text.

BELOW across the spread: Decorative Victorian house from the title page — warm golden light in the windows, \
snow on the roof. Medium distance — not tiny, not dominating. Snow-covered evergreens. A snowman with a \
scarf in the front yard. Grounds the image in the story world.

Composition hierarchy: moon left · painted Santa flight L→R · North Star right upper · house+snowman below.
Deep blues, warm golden window light, soft moonlight. Peaceful sacred farewell. Continuous scene.
"""

NEG = (
    "silhouette Santa, black cutout sleigh, black blob reindeer, boy, child, interior room, window from inside, "
    "text, letters, typography, God bless baked in, watermark, fake gutter, spine shadow, "
    "identical mirrored halves, cartoon flat clipart, tiny unreadable house, empty sky with no Santa"
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

    # Upsert S12-closing beat; retarget S12a; mark S12b merged
    closing_block = '''    "S12-closing": {
        "unit": "S12-closing",
        "layout": "text_image",
        "left_page": 26,
        "right_page": 27,
        "left": (
            "He said I've had enough eggnogs, cider and soups. / "
            "My belt's getting harder to fit in the loops. / "
            "And one last thing, please do me a favor. / "
            "Always love Christmas, act like a kid and pray to your Savior."
        ),
        "right": "God bless. — under the North Star (IMAGE hierarchy · text in InDesign).",
        "right_kind": "poem",
        "title": "S12 Closing — God Bless",
    },
'''

    if '"S12-closing"' not in text:
        # insert before S12a or after S11
        anchor = '    "S12a-blessing": {'
        if anchor not in text:
            raise SystemExit("cannot find S12a for poem map insert")
        text = text.replace(anchor, closing_block + anchor, 1)
        print("poem map inserted S12-closing")
    else:
        print("poem map S12-closing already present")

    # Update S12a to point at merge note
    old_a = '''    "S12a-blessing": {
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
    new_a = '''    "S12a-blessing": {
        "unit": "S12a-blessing",
        "layout": "text_image",
        "left_page": 26,
        "right_page": 27,
        "left": (
            "He said I've had enough eggnogs, cider and soups. / "
            "My belt's getting harder to fit in the loops. / "
            "And one last thing, please do me a favor. / "
            "Always love Christmas, act like a kid and pray to your Savior."
        ),
        "right": "God bless. — under the North Star (merged closing · text in InDesign).",
        "right_kind": "poem",
        "title": "S12 Closing — God Bless",
        "alias_of": "S12-closing",
    },'''
    if old_a in text:
        text = text.replace(old_a, new_a)
        print("poem map S12a → merged closing captions")

    # aliases
    if '"S12-closing"' not in text.split("aliases")[-1] if "aliases" in text else True:
        pass
    if '"S12c"' not in text and "S12-closing" not in text[text.find("aliases") : text.find("aliases") + 800] if "aliases" in text else True:
        text = text.replace(
            '"S12b": "S12b-god-bless",',
            '"S12b": "S12b-god-bless",\n        "S12c": "S12-closing",\n        "S12": "S12-closing",',
            1,
        )

    path.write_text(text, encoding="utf-8")


def main() -> None:
    load_env()
    update_poem_map()
    INDEX.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    # Prefer house + santa + exterior mood (3 refs)
    refs = [SANTA, HOUSE, S12B if S12B.is_file() else STYLE]
    for p in refs:
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    urls = [fal_client.upload_file(str(p)) for p in refs]
    print("=== Qwen S12-closing epic v01 ===")
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

    tmp = OUT / "_tmp-v01-qwen.png"
    raw.save(tmp)
    up = fal_client.subscribe(
        SEEDVR,
        arguments={
            "image_url": fal_client.upload_file(str(tmp)),
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

    v01 = OUT / "v01"
    v01.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (v01, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    # Mirror into S12a primary as the live closing plate (merged)
    s12a = ROOT / "Media/development/S12a-blessing"
    for name in ("art.png", "art-left.png", "art-right.png"):
        (s12a / name).write_bytes((OUT / name).read_bytes())
    # Also mirror chops into S12b so flipbook paths don't orphan (marked merged in FLOW)
    s12b = ROOT / "Media/development/S12b-god-bless"
    for name in ("art.png", "art-left.png", "art-right.png"):
        (s12b / name).write_bytes((OUT / name).read_bytes())

    recipe = f"""# RECIPE — S12-closing / v01

| Field | Value |
|-------|--------|
| **name** | Epic closing — Santa departure + North Star (S12a+S12b MERGED) |
| **book pages** | **26\\|27** (absorbs former 28\\|29) |
| **layout** | FULL SPREAD seamless · FINAL STORY IMAGE |
| **version** | v01 |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **5250×2625** triplet |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **refs** | santa-G0-v2 · cover-front house · S12b v01 exterior |

## Intent

Painted Santa G0 v2 (open coat) + reindeer L→R receding. Moon left. Sacred North Star right (God bless under). \
Victorian house + snowman below. No boy. No interior.
"""
    (v01 / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (v01 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v01",
                "status": "working",
                "unit": "S12-closing",
                "merges": ["S12a-blessing", "S12b-god-bless"],
                "pages": "26|27",
                "absorbs_pages": "28|29",
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

    # Prefer S12-closing unit if registered; else S12a captions (updated)
    try:
        from book_poem_map import BEATS

        unit = "S12-closing" if "S12-closing" in BEATS else "S12a-blessing"
    except Exception:
        unit = "S12a-blessing"

    seamless_board(
        final,
        INDEX / f"S12-closing-v01-epic-{DAY}.png",
        unit=unit,
        version="v01",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · MERGED S12a+b · painted Santa G0 v2 · North Star",
        subtitle="FINAL STORY IMAGE · moon L · flight L→R · North Star R · house+snowman",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "MERGED S12a+S12b → S12-closing v01 FINAL STORY IMAGE · painted Santa G0 v2 open coat L→R · "
        "moon L · sacred North Star R (God bless under) · Victorian house + snowman · NO boy · "
        "Media/development/S12-closing/ · board S12-closing-v01-epic-2026-07-23.png"
    )

    for pid, side, caption in (
        ("p26", "L", "p26 · S12 Closing L · v01 epic flight"),
        ("p27", "R", "p27 · S12 Closing R · v01 North Star"),
    ):
        for p in root["plates"]:
            if p["id"] != pid:
                continue
            p.update(
                {
                    "beat": f"S12 Closing {side}",
                    "caption": caption,
                    "path": f"Media/development/S12-closing/art-{'left' if side=='L' else 'right'}.png",
                    "version": "v01",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "development_path": "Media/development/S12-closing/art.png",
                    "unit": "S12-closing",
                    "layout": "text_image_defacto",
                    "pixel_size": "2625x2625",
                    "spread_side": side,
                    "gpt_pillar": True if side == "R" else False,
                }
            )
            if side == "L":
                p["text_role"] = "closing_poem_block"
            else:
                p["text_role"] = "god_bless_under_north_star"
            p.pop("source_mock", None)
            p.pop("concept", None)

    for pid in ("p28", "p29"):
        for p in root["plates"]:
            if p["id"] != pid:
                continue
            p.update(
                {
                    "caption": f"{pid} · MERGED into S12-closing (p26|27)",
                    "path": f"Media/development/S12-closing/art-{'left' if pid=='p28' else 'right'}.png",
                    "version": "merged-v01",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "status": "merged",
                    "date": DAY,
                    "notes": "Absorbed into S12-closing epic on p26|27 — " + note,
                    "development_path": "Media/development/S12-closing/art.png",
                    "unit": "S12-closing",
                    "merged_into": "p26|27",
                }
            )
            p.pop("source_mock", None)

    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update(
                {
                    "page": "26|27",
                    "beat": "S12 Closing — God Bless",
                    "version": "v01",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "status": "working",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": note,
                    "unit": "S12-closing",
                    "merges": ["S12a-blessing", "S12b-god-bless"],
                }
            )
        if d.get("page") == "28|29":
            d.update(
                {
                    "page": "28|29",
                    "beat": "S12b God Bless",
                    "version": "merged-v01",
                    "model": "—",
                    "status": "merged",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "MERGED into S12-closing on p26|27 — " + note,
                    "merged_into": "26|27",
                    "unit": "S12-closing",
                }
            )

    root["updated"] = DAY
    if "closing_merge_note" not in root:
        root["closing_merge_note"] = (
            "2026-07-23 · S12a Blessing + S12b God Bless merged into one epic FINAL STORY IMAGE "
            "at Media/development/S12-closing/ (book pages 26|27). Former 28|29 absorbed."
        )
    else:
        root["closing_merge_note"] = (
            "2026-07-23 · S12a Blessing + S12b God Bless merged into one epic FINAL STORY IMAGE "
            "at Media/development/S12-closing/ (book pages 26|27). Former 28|29 absorbed."
        )

    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(FLOW.read_text(encoding="utf-8"))
    print("FLOW OK")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
