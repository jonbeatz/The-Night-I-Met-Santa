#!/usr/bin/env python3
"""S12-god-bless v12 — art6 PRIMARY quality + art11 DIRECTION (deer ahead)."""
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

ART6 = ROOT / "Images/styles1/art6.png"  # PRIMARY — style/Santa/quality
ART11 = ROOT / "Images/styles1/art11.png"  # DIRECTION — deer in front, sleigh angle
FACE = ROOT / "Media/approved/characters/santa-G0-face.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Create the Christmas FINAL STORY IMAGE spread by COMBINING two references. Wide ~2:1. NO TEXT.

IMAGE 1 = PRIMARY (art-six): STYLE, QUALITY, and CHARACTER target.
Keep this image's rich painterly atmosphere, Santa face and sleigh quality (warm, detailed,
correctly sized), Santa eyes OPEN looking back toward us with a gentle smile, best reindeer
artwork quality, warm yellow-tinted North Star with gleaming cross rays and perfect open sky
below for later \"God bless\", Victorian house warm windows, snowman, lamp post, snow evergreens.
Use IMAGE 1 as the visual quality baseline — our book oil look.

IMAGE 2 = DIRECTION (art-eleven): Fix FORMATION and PATH only.
Reindeer must be IN FRONT of the sleigh PULLING it — NOT behind. Sleigh at the BACK.
Sleigh direction/angle toward the house (like IMAGE 2). Dynamic curved formation.
Do NOT copy IMAGE 2's wrong rear-deer layout if any — take the correct ahead-pulling path.

IMAGE 3 = Santa G0 face lock — soft kind open eyes with crow's feet, rosy cheeks, warm gentle smile,
round grandfatherly face. Eyes OPEN (not squinted shut).

COMBINED RESULT:
- Art quality / Santa / sleigh / atmosphere / North Star / house of IMAGE 1
- Reindeer DIRECTION of IMAGE 2: nine reindeer IN FRONT pulling toward house
- Exactly NINE reindeer: 4 pairs + Rudolph leading solo (front, smallest). COUNT them.
- ONLY Rudolph has a faint soft red nose glow. NO other nose glow.
- Full moon left. North Star right with open dark sky below. Deep blue sky.
- Soft cream vignette on ALL four sides evenly. NO baked text. NO duplicate Santa.
"""

NEG = (
    "reindeer behind the sleigh, deer trailing after sled, eyes closed, squinted shut eyes, "
    "only 8 reindeer, two glowing noses, three glowing noses, laser nose, neon nose, "
    "text, God bless, letters, watermark, hard white border, boy, duplicate Santa"
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
    for p in (ART6, ART11, FACE):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # Start from art6 (primary quality) at edit resolution
    base = Image.open(ART6).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp6 = OUT / "_tmp-v12-art6.png"
    base.save(tmp6)
    dir11 = Image.open(ART11).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp11 = OUT / "_tmp-v12-art11.png"
    dir11.save(tmp11)

    urls = [
        fal_client.upload_file(str(tmp6)),
        fal_client.upload_file(str(tmp11)),
        fal_client.upload_file(str(FACE)),
    ]
    print("=== Qwen S12-god-bless v12 · art6 + art11 ===")
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
    tmp_q = OUT / "_tmp-v12-qwen.png"
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

    for t in (tmp6, tmp11, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v12"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v12

| Field | Value |
|-------|--------|
| **version** | **v12** |
| **date** | {DAY} |
| **primary** | Images/styles1/art6.png (style/Santa/quality) |
| **direction** | Images/styles1/art11.png (deer ahead / sleigh angle) |
| **face** | santa-G0-face.png |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v12",
                "status": "working",
                "primary_ref": "Images/styles1/art6.png",
                "direction_ref": "Images/styles1/art11.png",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v12", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v12-final-{DAY}.png",
        unit="S12-god-bless",
        version="v12",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · art6 quality + art11 direction · 9 deer ahead · G0 face",
        subtitle="Eyes open looking back · Rudolph faint only · North Star text pocket",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v12 · art6 PRIMARY + art11 DIRECTION · 9 deer in front · "
        "eyes open looking back · board S12-god-bless-v12-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v12",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v12",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v12", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v12", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v12", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
