#!/usr/bin/env python3
"""S12-god-bless v09 — FINAL dial on v08c: G0 face, 9 deer, faint Rudolph-only nose, even vignette."""
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

BASE = OUT / "v08c" / "art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0.png"  # user-attached face/wardrobe ref
SANTA_V2 = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Surgical edit of this Christmas FINAL STORY IMAGE spread. KEEP composition mostly:
sleigh at BACK, reindeer IN FRONT pulling, moon left, North Star right, Victorian house lower-right,
snowman, lamp, fence, deep blue night. NO TEXT anywhere.

IMAGE 1 = current v08c spread — keep flight pull-order (deer ahead, sleigh behind) and scene layout.
IMAGE 2 = Santa G0 character LOCK (face + open-coat wardrobe). Match his warm grandfatherly face
precisely — soft eyes with laugh lines, rosy cheeks, gentle smile. NOT stern. NOT angular.
Open red coat, cream striped shirt underneath, brown suspenders. Same Santa as every spread,
just at the flying-sleigh angle.
IMAGE 3 = Santa G0 v2 backup identity (open coat / suspenders) if needed for wardrobe consistency.

FIXES (critical):
1) SANTA FACE + WARDROBE: Replace Santa with G0 identity from the reference — warm kind smile,
laugh lines, rosy cheeks, open coat showing cream striped shirt + brown suspenders.
2) REINDEER COUNT = exactly NINE: four pairs + Rudolph leading solo at the front. COUNT them.
3) NOSES: ONLY Rudolph (front/smallest) has a VERY FAINT soft warm red nose glow — barely visible.
ALL other reindeer: plain brown noses, ZERO red glow. Fix any second/third glowing noses — remove them.
4) Curve arcs from upper-left TOWARD the house on the lower-right (descend toward house).
Rudolph furthest/smallest. Keep deer IN FRONT pulling; sleigh at BACK.
5) North Star right with OPEN dark sky below it (clear text pocket). No deer crowding under the star.
6) VIGNETTE: soft cream watercolor dissolve on ALL four edges evenly (left, right, top, bottom) —
the whole image breathes into cream. NOT one-sided.

STYLE: OUR book oil — burgundy/gold, deep atmospheric shadows, visible brushwork (S3 quality).
Ornate red/gold sleigh with presents. NO baked text. NO duplicate Santa/sleigh.
"""

NEG = (
    "text, letters, God bless, watermark, "
    "stern Santa, angular face, angry Santa, closed coat hiding shirt, "
    "two glowing red noses, three glowing noses, bright laser nose, neon nose, "
    "reindeer behind sleigh, only 8 reindeer, only 10 reindeer, "
    "one-sided vignette, hard white border, missing house, missing moon, boy, duplicate Santa"
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
    for p in (BASE, SANTA, SANTA_V2):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    base = Image.open(BASE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-v09-base.png"
    base.save(tmp)
    urls = [
        fal_client.upload_file(str(tmp)),
        fal_client.upload_file(str(SANTA)),
        fal_client.upload_file(str(SANTA_V2)),
    ]
    print("=== Qwen S12-god-bless v09 FINAL ===")
    print("refs: v08c · santa-G0.png · santa-G0-v2.png")
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
    tmp_q = OUT / "_tmp-v09-qwen.png"
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
    tmp.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v09"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v09

| Field | Value |
|-------|--------|
| **version** | **v09** |
| **date** | {DAY} |
| **status** | working |
| **base** | v08c |
| **refs** | santa-G0.png · santa-G0-v2.png |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |

## Fixes

G0 warm face + open coat · 9 deer · faint Rudolph-only nose · even cream vignette all sides · NO text.
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v09",
                "status": "working",
                "base": "v08c",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v09", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v09-final-{DAY}.png",
        unit="S12-god-bless",
        version="v09",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · v08c + Santa G0 · 9 deer · faint Rudolph-only · even vignette",
        subtitle="Warm G0 face · open coat · deer ahead · NO text",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v09 · v08c + Santa G0 face/wardrobe · 9 deer · faint Rudolph-only nose · "
        "even cream vignette · board S12-god-bless-v09-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v09",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v09",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update(
                {
                    "version": "merged-v09",
                    "status": "merged",
                    "date": DAY,
                    "notes": "Absorbed into S12-god-bless v09 — " + note,
                }
            )
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v09", "status": "working", "date": DAY, "notes": note, "unit": "S12-god-bless"})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v09", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
