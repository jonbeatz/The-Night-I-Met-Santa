#!/usr/bin/env python3
"""S12-god-bless v04 — angled perspective toward house · 9 reindeer pairs+Rudolph."""
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

BASE = OUT / "v03" / "art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Edit this seamless Christmas FINAL STORY IMAGE spread into a stronger PERSPECTIVE composition.
5250x2625 feel. Rich oil-painting. NO baked text. NO boy. NO duplicate Santa. NO second sleigh.

IMAGE 1 = current v03 closing scene (house, moon, North Star, Santa language).
IMAGE 2 = Santa G0 v2 LOCK — open red coat, striped shirt, warm smiling face toward viewer.
IMAGE 3 = soft watercolor vignette / frame reference — soft dissolve to cream edges, NOT a hard white border.

PERSPECTIVE (critical rewrite of flight path):
Santa and the sleigh are CLOSER to us — LARGER in the frame. They fly TOWARD the house at an ANGLE —
NOT a flat horizontal left-to-right parade across the page.
Flight path: from UPPER-LEFT toward the house in the LOWER-RIGHT.
Depth: reindeer LEAD AWAY from us into the distance — front reindeer SMALLER, reindeer near Santa
(back of team) LARGER. Proper foreshortening / depth.
Santa is angled slightly TOWARD the viewer — we clearly see his face and warm SMILE (joyful, peaceful).
Open red coat (G0 v2). Detailed wooden sleigh with wood grain, runners, sack/gifts.

REINDEER — exactly NINE (9):
Four pairs (two-by-two) plus Rudolph leading SOLO in front.
Warm brown fur, visible antlers, full painted style — NOT silhouettes.
Rudolph = front, smallest (furthest), with a SOFT subtle warm RED GLOW on his nose —
gentle, not a bright laser / not neon / not a lightbulb.

NORTH STAR: RIGHT page, UPPER area. Golden-white gleam with soft cross-shaped shimmer + halo.
OPEN dark blue sky BELOW the star — clear breathing room for InDesign text \"God bless.\"
Do not put reindeer or roof clutter in that text pocket.

HOUSE: Victorian house LOWER-RIGHT — LARGER, more prominent. Warm golden windows, snow on roof.
Snowman with scarf in yard. Snow-covered evergreens. House is the destination Santa flies toward.

MOON: Full moon on the LEFT, behind Santa — soft glow.

Frame: standard soft vignette dissolve to cream — NO hard white rectangular border / NO hard cut edge.
ONE continuous painted scene. Deep blues, warm golden window light, soft moonlight.
"""

NEG = (
    "hard white border, hard rectangular frame, thick white matte edge, "
    "flat horizontal parade of reindeer, duplicate Santa, second sleigh, "
    "silhouette deer, laser red nose, neon nose, lightbulb nose, angry Santa, "
    "closed coat only, tiny house, boy, text, God bless letters, watermark, fake gutter, "
    "reindeer blocking sky under North Star"
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
    if not BASE.is_file():
        BASE2 = OUT / "art.png"
        if not BASE2.is_file():
            raise SystemExit("missing base art")
        base_path = BASE2
    else:
        base_path = BASE

    refs = [base_path, SANTA]
    if FRAME.is_file():
        refs.append(FRAME)

    base_in = Image.open(base_path).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_base = OUT / "_tmp-v04-base.png"
    base_in.save(tmp_base)
    urls = [fal_client.upload_file(str(tmp_base))]
    for p in refs[1:]:
        urls.append(fal_client.upload_file(str(p)))

    print("=== Qwen S12-god-bless v04 perspective ===")
    print("base:", base_path.name, "refs:", [p.name for p in refs[1:]])
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
    tmp_q = OUT / "_tmp-v04-qwen.png"
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

    vdir = OUT / "v04"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v04

| Field | Value |
|-------|--------|
| **name** | S12 God Bless — angled perspective toward house |
| **version** | **v04** |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **base** | v03 |

## Intent

Santa larger / closer, flying upper-left → house lower-right at an angle. Face+smile toward viewer. \
9 reindeer (4 pairs + Rudolph soft red nose). North Star + open sky. Soft cream vignette (no hard border).
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    meta = {
        "version": "v04",
        "status": "working",
        "unit": "S12-god-bless",
        "reindeer_count": 9,
        "rudolph": True,
        "perspective": "upper_left_toward_house_lower_right",
        "seed": seed,
        "fal_url": qurl,
        "size": list(SPREAD),
    }
    (vdir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "unit": "S12-god-bless",
                "status": "working",
                "version": "v04",
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
        INDEX / f"S12-god-bless-v04-perspective-{DAY}.png",
        unit="S12-god-bless",
        version="v04",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · angled toward house · 9 deer+Rudolph · soft vignette",
        subtitle="Santa closer · face+smile · upper-L → house lower-R · open sky under star",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v04 · Santa larger angled toward house · 9 reindeer (4 pairs+Rudolph soft nose) · "
        "smile to viewer · moon L · North Star R + open sky · soft cream vignette · "
        "Media/development/S12-god-bless/ · board S12-god-bless-v04-perspective-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v04",
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "unit": "S12-god-bless",
                    "version": "v04",
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
                    "version": "merged-v04",
                    "status": "merged",
                    "date": DAY,
                    "notes": "Absorbed into S12-god-bless v04 — " + note,
                }
            )
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update(
                {
                    "beat": "S12 God Bless",
                    "version": "v04",
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
                    "version": "merged-v04",
                    "status": "merged",
                    "date": DAY,
                    "notes": "MERGED into S12-god-bless v04 — " + note,
                    "unit": "S12-god-bless",
                }
            )
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
