#!/usr/bin/env python3
"""S12-god-bless v10 — smaller Santa in sleigh · angle behind team · 9 reindeer."""
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

V09 = OUT / "v09" / "art.png"
V08C = OUT / "v08c" / "art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Surgical edit of this Christmas FINAL STORY IMAGE. KEEP the scene: moon left, North Star right with
OPEN dark sky below, Victorian house lower-right warm windows, snowman, lamp, fence, cream vignette
on ALL sides, deep blue night. NO TEXT. NO baked letters.

IMAGE 1 = v09 preferred (warm G0 Santa face, open coat, scene lock) — base to edit.
IMAGE 2 = v08c composition reference for sleigh/team proportions and pull order.
IMAGE 3 = Santa G0 v2 face/wardrobe lock — warm grandfatherly smile, open coat, striped shirt, suspenders.

THREE FIXES ONLY:

FIX 1 — SANTA SCALE: Santa is TOO BIG. Make him SMALLER so he sits properly IN the sleigh, not
dominating it. The sleigh must feel SUBSTANTIAL and LARGER in proportion to him. He sits
comfortably holding the reins. Presents still visible in the sleigh.

FIX 2 — SLEIGH ANGLE: Turn the sleigh more to the LEFT so it is clearly BEHIND the reindeer team
(deer still IN FRONT pulling). Santa angled slightly AWAY from us — glancing back over his shoulder
with a warm goodbye smile toward the house / reader. NOT facing the camera directly. Not a front portrait.

FIX 3 — REINDEER COUNT: exactly NINE. Four pairs + Rudolph leading solo at the front. COUNT them
before finishing. ALL nine IN FRONT of the sleigh pulling. Rudolph furthest/smallest with ONLY a
VERY FAINT soft red nose glow. All other noses brown — no second glowing nose.

KEEP LOCKED: Santa G0 warm face identity (just smaller / different angle), open coat wardrobe,
house/moon/star/snowman, even cream vignette all sides, rich oil book style. NO duplicate Santa.
"""

NEG = (
    "giant Santa filling the sleigh, Santa too big, Santa facing camera directly, front portrait Santa, "
    "reindeer behind sleigh, only 8 reindeer, only 7 reindeer, two glowing red noses, laser nose, "
    "text, God bless, letters, watermark, hard white border, one-sided vignette, boy, duplicate Santa"
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
    for p in (V09, V08C, SANTA):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    base = Image.open(V09).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-v10-base.png"
    base.save(tmp)
    ref08 = Image.open(V08C).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp08 = OUT / "_tmp-v10-v08c.png"
    ref08.save(tmp08)

    urls = [
        fal_client.upload_file(str(tmp)),
        fal_client.upload_file(str(tmp08)),
        fal_client.upload_file(str(SANTA)),
    ]
    print("=== Qwen S12-god-bless v10 ===")
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
    tmp_q = OUT / "_tmp-v10-qwen.png"
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

    for t in (tmp, tmp08, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v10"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v10

| Field | Value |
|-------|--------|
| **version** | **v10** |
| **date** | {DAY} |
| **fixes** | Smaller Santa in sleigh · sleigh angled behind team · 9 reindeer |
| **base** | v09 (+ v08c proportion ref) |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps({"version": "v10", "status": "working", "seed": seed, "fal_url": qurl, "size": list(SPREAD)}, indent=2),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v10", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v10-final-{DAY}.png",
        unit="S12-god-bless",
        version="v10",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · smaller Santa · sleigh behind team · 9 deer",
        subtitle="Glance-back goodbye · substantial sleigh · Rudolph faint nose only",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v10 · smaller Santa IN sleigh · angled behind team glancing back · "
        "9 reindeer · board S12-god-bless-v10-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v10",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v10",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v10", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v10", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v10", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
