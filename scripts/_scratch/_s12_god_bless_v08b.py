#!/usr/bin/env python3
"""S12-god-bless v08b — fix pull order: IMG_2811 first · v07 scene · Santa G0."""
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

DIR_REF = ROOT / "Images/styles1/IMG_2811.PNG"
SCENE = OUT / "v07" / "art.png"  # had correct pull order; keep house/moon/star
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Wide seamless Christmas FINAL STORY IMAGE. NO TEXT anywhere.

IMAGE 1 (PRIMARY — HARNESS / DIRECTION): Reindeer are AHEAD of the sleigh PULLING it.
Sleigh at the BACK. Team arcs upper-left toward house lower-right. Copy THIS pull order exactly.
ZERO reindeer behind the sleigh.

IMAGE 2 (SCENE): Keep moon left, North Star right with open dark sky below, Victorian house
lower-right warm windows, snowman, lamp, fence, evergreens, cream vignette, oil night magic.
Keep reindeer IN FRONT like this image (do not move them behind).

IMAGE 3: Santa G0 v2 LOCK — open red coat, cream striped shirt, brown suspenders, warm smile,
kind eyes, rosy cheeks, full white beard. Same Santa as every spread.

STYLE: OUR book oil painting (burgundy/gold, deep shadows, brushwork) — not photo-ref style.
Soft cream vignette dissolve.

REQUIREMENTS:
- Exactly NINE reindeer: 4 pairs + Rudolph solo in front. COUNT them.
- ALL nine AHEAD of the sleigh pulling via reins. Sleigh/Santa at rear.
- ONLY Rudolph: VERY FAINT soft warm red nose hint. Other noses brown, no glow.
- Santa larger, open coat G0 v2, presents in ornate red/gold sleigh.
- Curve toward house. Moon L. North Star R + open sky. House + snowman present.
NO baked text. NO duplicate Santa. NO deer behind sleigh.
"""

NEG = (
    "reindeer behind sleigh, deer behind Santa, trailing deer after sled, "
    "only 4 reindeer, deer following the sleigh, text, God bless, letters, "
    "bright laser nose, glowing noses on all deer, closed coat hiding shirt, "
    "duplicate Santa, missing house, missing moon, boy, hard white border"
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
    if not SCENE.is_file():
        raise SystemExit("missing v07")
    scene = Image.open(SCENE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-v08b-scene.png"
    scene.save(tmp)
    urls = [
        fal_client.upload_file(str(DIR_REF)),
        fal_client.upload_file(str(tmp)),
        fal_client.upload_file(str(SANTA)),
    ]
    print("=== Qwen S12 v08b · IMG_2811 first ===")
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
    tmp_q = OUT / "_tmp-v08b-qwen.png"
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
    except Exception as e:  # noqa: BLE001
        print("SeedVR fallback", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)
    tmp.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v08b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)

    (vdir / "RECIPE.md").write_text(
        f"# RECIPE — S12-god-bless / v08b\n\nIMG_2811 first (pull order) + v07 scene + G0 v2.\n\nseed={seed}\n{qurl}\n",
        encoding="utf-8",
    )
    (vdir / "meta.json").write_text(
        json.dumps({"version": "v08b", "seed": seed, "fal_url": qurl, "status": "working"}, indent=2),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v08b", "status": "working"}, indent=2),
        encoding="utf-8",
    )
    (OUT / "RECIPE.md").write_text((vdir / "RECIPE.md").read_text(encoding="utf-8"), encoding="utf-8")

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v08b-final-{DAY}.png",
        unit="S12-god-bless",
        version="v08b",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · IMG_2811 pull-first · v07 scene · G0 v2 · 9 deer",
        subtitle="Deer AHEAD pulling · faint Rudolph · open coat · NO text",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v08b · IMG_2811 pull-order FIRST + v07 scene + Santa G0 v2 · "
        "9 deer in front · faint Rudolph · board S12-god-bless-v08b-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v08b",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v08b",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v08b", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v08b", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v08b", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", seed)


if __name__ == "__main__":
    main()
