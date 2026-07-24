#!/usr/bin/env python3
"""S12-god-bless v06 — FINAL dial with styles1 composition refs."""
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

REF_CURVE = ROOT / "Images/styles1/IMG_2811.PNG"
REF_LAYOUT = ROOT / "Images/styles1/15862F89-0D70-4832-B724-7EFA3278B63E.png"
# alt curve if needed: IMG_2810_b.jpg
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Wide seamless Christmas FINAL STORY IMAGE spread — epic closing departure. Aspect ~2:1.
NO TEXT. NO LETTERS. NO \"God bless\" painted anywhere. NO boy. NO interior room.
NO duplicate Santa. NO second sleigh. ONE continuous painted scene.

IMAGE 1 = COMPOSITION guide for the REINDEER CURVE — dynamic arcing team through the sky
(NOT a flat horizontal line). Copy this curved flight energy.
IMAGE 2 = LAYOUT guide — Victorian house lower-right with warm windows + snowman, full moon left,
North Star upper-right with open sky beneath it. Keep this story layout.
IMAGE 3 = Santa G0 v2 identity LOCK — open red coat over striped shirt/suspenders, warm smiling face.

COMPOSITION (must match the guides):
Nine (9) reindeer in a DYNAMIC CURVED formation arcing gracefully through the sky —
sweeps from UPPER-LEFT, through the center, TOWARD the house on the LOWER-RIGHT.
Pairs two-by-two: four pairs + Rudolph leading SOLO at the FRONT of the curve.
Rudolph = smallest, furthest, soft subtle warm RED nose glow (NOT a laser / NOT neon).
Reindeer get progressively SMALLER toward the front of the curve — proper depth/perspective.
Full painted warm brown fur + visible antlers — NOT silhouettes.

Santa clearly visible in an ornate red/golden wooden sleigh, LARGER in frame, flying TOWARD the house
(not merely across the sky). Angled slightly toward the viewer with a warm SMILE.
Open red coat (G0 v2). Sleigh filled with wrapped presents — reds, greens, golds. Wood grain + runners.

SKY:
Deep blue night, scattered stars.
Full moon LEFT behind/slightly above Santa — dramatic soft backlighting.
North Star RIGHT upper — bright golden-white cross shimmer + gentle halo.
OPEN dark blue EMPTY sky BELOW the North Star for later InDesign text (no clutter there).

GROUND:
Victorian house LOWER-RIGHT — larger, prominent. Warm golden windows, snow on roof. Cozy anchor.
Snowman with scarf in front yard. Snow-covered evergreens. Rolling snow landscape.

STYLE:
Rich oil-painting. Strong cool-blue vs warm-golden contrast. Soft cream vignette dissolve at edges —
NO hard white border. Full painted characters.

COUNT THE REINDEER — must be exactly NINE before finishing.
"""

NEG = (
    "text, letters, typography, words, God bless, watermark, caption, "
    "flat horizontal reindeer line, only 2 reindeer, only 4 reindeer, only 5 reindeer, only 6 reindeer, "
    "only 7 reindeer, only 8 reindeer, silhouette deer, black cutout, laser red nose, neon nose, "
    "duplicate Santa, second sleigh, missing house, no house, missing moon, no moon, "
    "boy, child, interior room, hard white border, hard rectangular matte"
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

    refs = [REF_CURVE, REF_LAYOUT, SANTA]
    for p in refs:
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    urls = [fal_client.upload_file(str(p)) for p in refs]
    print("=== Qwen S12-god-bless v06 FINAL ===")
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
            "enable_prompt_expansion": False,
        },
        with_logs=True,
    )
    print(result)
    qurl = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(qurl)
    print("qwen", raw.size)
    tmp_q = OUT / "_tmp-v06-qwen.png"
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

    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v06"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v06

| Field | Value |
|-------|--------|
| **name** | S12 God Bless — curved team FINAL dial |
| **pages** | 26\\|27 (28\\|29 merged) |
| **version** | **v06** |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **refs** | IMG_2811 (curve) · 15862F89… (house/moon/star layout) · santa-G0-v2 |
| **prompt_expansion** | off (no baked text) |

## Intent

9 reindeer curved upper-L → house lower-R · Rudolph soft nose · larger Santa open coat smile · \
moon L · North Star R + open sky · Victorian house + snowman · cream vignette · NO text.
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v06",
                "status": "working",
                "unit": "S12-god-bless",
                "reindeer_count_target": 9,
                "refs": [p.name for p in refs],
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
                "no_baked_text": True,
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
                "version": "v06",
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
        INDEX / f"S12-god-bless-v06-curve-{DAY}.png",
        unit="S12-god-bless",
        version="v06",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · styles1 curve+layout refs · 9 deer · NO text",
        subtitle="Curved team upper-L → house lower-R · moon L · North Star R · Rudolph soft nose",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v06 · styles1 IMG_2811 curve + 15862F89 layout · 9 reindeer curved toward house · "
        "Rudolph soft nose · moon L · North Star R open sky · Victorian house+snowman · NO baked text · "
        "Media/development/S12-god-bless/ · board S12-god-bless-v06-curve-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v06",
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "unit": "S12-god-bless",
                    "version": "v06",
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
                    "version": "merged-v06",
                    "status": "merged",
                    "date": DAY,
                    "notes": "Absorbed into S12-god-bless v06 — " + note,
                }
            )
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update(
                {
                    "beat": "S12 God Bless",
                    "version": "v06",
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
                    "version": "merged-v06",
                    "status": "merged",
                    "date": DAY,
                    "notes": "MERGED into S12-god-bless v06 — " + note,
                    "unit": "S12-god-bless",
                }
            )
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
