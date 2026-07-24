#!/usr/bin/env python3
"""S12-god-bless v08 — FINAL: v06 scene style + IMG_2811 pull direction + Santa G0 v2."""
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

SCENE = OUT / "v06" / "art.png"  # liked scene (IGNORE deer behind sleigh)
DIR_REF = ROOT / "Images/styles1/IMG_2811.PNG"  # pull direction / curve toward house
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Wide seamless Christmas FINAL STORY IMAGE spread ~2:1. ONE continuous painted scene.
NO TEXT. NO LETTERS. NO \"God bless\". NO watermark. NO boy. NO duplicate Santa/sleigh.

IMAGE 1 = SCENE LOCK (our preferred artwork): keep the overall magic — moon, North Star with open
sky below, Victorian house lower-right with warm golden windows, snowman, lamp post, fence,
evergreens, deep blue night, cream vignette. IGNORE any incorrect reindeer positioned BEHIND the
sleigh in this image — those are wrong; do not copy that mistake.

IMAGE 2 = DIRECTION / HARNESS guide only: reindeer IN FRONT of the sleigh PULLING it; sleigh at the
BACK; team curves from upper-left toward the house lower-right. Use this for flight path + pull order
ONLY — do NOT copy this reference's art style or palette.

IMAGE 3 = Santa G0 v2 CHARACTER LOCK — same Santa as every spread: open red coat, cream/blue-white
striped shirt visible underneath, brown suspenders, warm smile, kind eyes, rosy cheeks, full white
beard. Must be clearly recognizable even in the flying sleigh angle.

STYLE LOCK (OUR BOOK — not the photo refs):
Rich oil-painting matching S3 Eyes Met quality. Burgundy + golden tones. Deep atmospheric shadows.
Visible brushwork. Soft watercolor vignette dissolving to cream at edges — no hard white border.

SANTA + SLEIGH:
Santa G0 v2 as above, warm smile. Ornate red sleigh with gold trim, filled with wrapped presents
(reds, greens, golds). Sleigh is at the BACK of the formation.

REINDEER (COUNT = exactly NINE before finishing):
Four pairs (two-by-two) + Rudolph leading SOLO at the FRONT.
ALL reindeer IN FRONT of the sleigh, pulling it via visible reins. Nothing behind the sleigh.
Dynamic curved formation arcing upper-left → house lower-right.
Rudolph = smallest/furthest. ONLY Rudolph has a VERY FAINT soft warm red nose glow — barely visible
hint, NOT a bright beacon. All other reindeer: plain brown noses, ZERO glow.
Warm brown fur, visible antlers, full painted — not silhouettes. Proper depth (front smaller).

SKY: Full moon LEFT soft glow behind Santa. North Star RIGHT golden-white cross shimmer + halo.
OPEN dark blue sky BELOW North Star for later InDesign text.
GROUND: Victorian house lower-right warm windows + snow; snowman with scarf; evergreens; lamp post;
wooden fence; rolling snowy landscape.
"""

NEG = (
    "text, letters, typography, God bless, watermark, "
    "reindeer behind the sleigh, deer trailing after sleigh, sleigh leading the team, "
    "bright red laser nose, neon nose, glowing noses on multiple reindeer, "
    "only 4 reindeer, only 6 reindeer, only 7 reindeer, only 8 reindeer, "
    "silhouette deer, duplicate Santa, second sleigh, missing house, missing moon, "
    "photo-real reference style, hard white border, boy, closed coat hiding striped shirt"
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
    for p in (SCENE, DIR_REF, SANTA):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # Downscale scene for edit input size consistency
    scene_in = Image.open(SCENE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_scene = OUT / "_tmp-v08-scene.png"
    scene_in.save(tmp_scene)

    urls = [
        fal_client.upload_file(str(tmp_scene)),
        fal_client.upload_file(str(DIR_REF)),
        fal_client.upload_file(str(SANTA)),
    ]
    print("=== Qwen S12-god-bless v08 FINAL ===")
    print("refs: v06 scene · IMG_2811 direction · santa-G0-v2")
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
    tmp_q = OUT / "_tmp-v08-qwen.png"
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

    tmp_scene.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v08"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v08

| Field | Value |
|-------|--------|
| **name** | S12 God Bless — FINAL dial |
| **version** | **v08** |
| **date** | {DAY} |
| **status** | working |
| **model** | `{QWEN}` → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **refs** | v06 scene (ignore rear deer) · IMG_2811 pull direction · santa-G0-v2 |
| **prompt_expansion** | off |

## Intent

Book oil style · Santa G0 v2 open coat · 9 deer in front pulling · faint Rudolph nose only · \
curve upper-L → house lower-R · moon/star/house locked · NO text.
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v08",
                "status": "working",
                "unit": "S12-god-bless",
                "reindeer_count_target": 9,
                "rudolph_nose": "very_faint",
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
                "version": "v08",
                "pages": "26|27",
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
        INDEX / f"S12-god-bless-v08-final-{DAY}.png",
        unit="S12-god-bless",
        version="v08",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · v06 scene + IMG_2811 direction · G0 v2 · 9 deer",
        subtitle="Deer pull in front · faint Rudolph · open coat Santa · NO text",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v08 · v06 scene lock + IMG_2811 pull direction + Santa G0 v2 · "
        "9 reindeer in front · faint Rudolph nose · NO baked text · "
        "board S12-god-bless-v08-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v08",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v08",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update(
                {
                    "version": "merged-v08",
                    "status": "merged",
                    "date": DAY,
                    "notes": "Absorbed into S12-god-bless v08 — " + note,
                }
            )
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v08", "status": "working", "date": DAY, "notes": note, "unit": "S12-god-bless"})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v08", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
