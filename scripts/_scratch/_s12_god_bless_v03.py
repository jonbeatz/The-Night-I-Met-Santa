#!/usr/bin/env python3
"""S12-god-bless v03 — perspective fix, 9 reindeer + Rudolph, smile, house larger."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/development/S12-god-bless"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

BASE = OUT / "art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
HOUSE = ROOT / "Images/styles3/cover-front.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Wide seamless Christmas FINAL STORY IMAGE spread 5250x2625. Rich oil-painting quality.
NO fake gutter, NO spine shadow, NO baked text, NO boy, NO interior room.

IMAGE 1 = current closing composition (mood / house / sky language).
IMAGE 2 = Santa G0 v2 identity LOCK — open red coat, striped shirt, suspenders, warm face.
IMAGE 3 = Victorian decorative house reference — make the house LARGER and more prominent.

PERSPECTIVE (critical):
Santa and the sleigh are LARGER — flying TOWARD and slightly OVER the Victorian house.
Depth cue: reindeer get progressively SMALLER toward the FRONT of the team.
Santa (in sleigh) is CLOSEST to the viewer; the LEAD reindeer is FURTHEST away (smallest).
They fly LEFT → RIGHT across the sky. ONE continuous painted team. NO duplicate Santa. NO second sleigh.

REINDEER — exactly NINE (9): classic eight in pairs + Rudolph as LEAD (front, furthest, smallest).
Pairs two-by-two. Warm brown fur, visible antlers, full painted style — NOT silhouettes.
LEAD reindeer (Rudolph) has a glowing RED NOSE — soft warm glow, gentle, NOT a laser / not neon.

SANTA: open red coat (G0 v2), sitting in the detailed wooden sleigh (wood grain, runners, sack of gifts).
Looking DOWN toward the house with a warm SMILE — joyful, peaceful farewell.

MOON: full moon on the LEFT page, behind and above Santa — soft glow illuminating the scene.

NORTH STAR: RIGHT page, UPPER area. Bright golden-white gleam with soft cross-shaped shimmer and halo.
CRITICAL: OPEN SPACE of dark blue sky BELOW the North Star — clear breathing room where the words
"God bless." will be placed later in InDesign. Do NOT put reindeer, house roof, or clutter in that
text pocket. Star draws the eye; empty sky sits beneath it.

HOUSE: Victorian house BELOW — LARGER and more prominent than before. Warm golden light in windows,
snow on roof. Snowman with scarf in front yard. Snow-covered evergreens. The house is the anchor —
Santa flies toward it; the North Star shines above it.

Deep blues, warm golden window light, soft moonlight. Soft watercolor vignette frame on outer edges.
ONE Santa only. ONE sleigh only.
"""

NEG = (
    "duplicate Santa, second sleigh, ghost team over house, silhouette reindeer, black cutouts, "
    "laser red nose, neon nose, angry Santa, frowning Santa, closed buttoned coat only, "
    "tiny house, boy, child, baked text, God bless letters, watermark, fake gutter, "
    "reindeer blocking the sky under the North Star, clutter under North Star"
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


def download(url: str, tries: int = 4) -> Image.Image:
    last: Exception | None = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=180) as resp:
                return Image.open(io.BytesIO(resp.read())).convert("RGB")
        except Exception as e:  # noqa: BLE001
            last = e
            print("retry", i, e)
    assert last is not None
    raise last


def main() -> None:
    load_env()
    INDEX.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    if not BASE.is_file():
        raise SystemExit(f"missing base: {BASE}")
    refs = [BASE, SANTA]
    if HOUSE.is_file():
        refs.append(HOUSE)
    for p in refs:
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # Downscale base for edit input
    base_in = Image.open(BASE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_base = OUT / "_tmp-v03-base.png"
    base_in.save(tmp_base)
    urls = [fal_client.upload_file(str(tmp_base))]
    for p in refs[1:]:
        urls.append(fal_client.upload_file(str(p)))

    print("=== Qwen S12-god-bless v03 FINAL perspective ===")
    print("refs:", [Path(u).name if False else p.name for p in [tmp_base, *refs[1:]]])
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
    qurl = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(qurl)
    print("qwen", raw.size)
    tmp_q = OUT / "_tmp-v03-qwen.png"
    raw.save(tmp_q)

    try:
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
        u = up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"]
        final = download(u).resize(SPREAD, Image.Resampling.LANCZOS)
        print("seedvr ok")
    except Exception as e:  # noqa: BLE001
        print("SeedVR fallback", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)

    tmp_base.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v03"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v03

| Field | Value |
|-------|--------|
| **name** | S12 God Bless — perspective FINAL pass |
| **pages** | 26\\|27 |
| **version** | **v03** |
| **date** | {DAY} |
| **status** | working (Jon: FINAL dial) |
| **model** | `{QWEN}` → SeedVR×2 → **5250×2625** triplet |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |

## Intent

Larger Santa/sleigh toward house · depth (Santa near, lead far) · **9** reindeer + Rudolph red nose · \
warm smile looking down · moon L · North Star R with open sky for \"God bless.\" · larger Victorian house.
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v03",
                "status": "working",
                "unit": "S12-god-bless",
                "reindeer_count": 9,
                "rudolph": True,
                "perspective": "santa_near_lead_far_toward_house",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "unit": "S12-god-bless",
                "status": "working",
                "version": "v03",
                "pages": "26|27",
                "paths": {
                    "art": "Media/development/S12-god-bless/art.png",
                    "art_left": "Media/development/S12-god-bless/art-left.png",
                    "art_right": "Media/development/S12-god-bless/art-right.png",
                },
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
        INDEX / f"S12-god-bless-v03-perspective-{DAY}.png",
        unit="S12-god-bless",
        version="v03",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · larger Santa · 9 deer+Rudolph · North Star pocket",
        subtitle="Toward house · smile · open sky under star for God bless.",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v03 · larger Santa toward house · 9 reindeer+Rudolph red nose · "
        "smile looking down · moon L · North Star R + open sky for God bless · larger house · "
        "Media/development/S12-god-bless/ · board S12-god-bless-v03-perspective-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "beat": f"S12 God Bless {'L' if side == 'left' else 'R'}",
                    "caption": (
                        "p26 · S12 God Bless L · v03"
                        if p["id"] == "p26"
                        else "p27 · S12 God Bless R · v03"
                    ),
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "unit": "S12-god-bless",
                    "version": "v03",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                }
            )
        if p["id"] in ("p28", "p29"):
            side = "left" if p["id"] == "p28" else "right"
            p.update(
                {
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "unit": "S12-god-bless",
                    "version": "merged-v03",
                    "status": "merged",
                    "date": DAY,
                    "notes": "Absorbed into S12-god-bless v03 — " + note,
                }
            )
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update(
                {
                    "beat": "S12 God Bless",
                    "version": "v03",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "unit": "S12-god-bless",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                }
            )
        if d.get("page") == "28|29":
            d.update(
                {
                    "version": "merged-v03",
                    "status": "merged",
                    "date": DAY,
                    "notes": "MERGED into S12-god-bless v03 — " + note,
                    "unit": "S12-god-bless",
                }
            )
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(FLOW.read_text(encoding="utf-8"))
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
