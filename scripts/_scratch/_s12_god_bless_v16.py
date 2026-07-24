#!/usr/bin/env python3
"""S12-god-bless v16 — v15b lock + 9th deer + raise Santa/sleigh over moon."""
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

V15B = OUT / "v15b" / "art.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Surgical edit of this Christmas spread. KEEP the same look, feel, paint style, house,
North Star, snowman, lamp, vignette, and overall mood. Wide ~2:1. NO TEXT.

CHANGE ONLY:
1) REINDEER COUNT = exactly NINE (currently eight). ADD one more reindeer into the same
   flying harnessed curve IN FRONT of the sleigh so the team is 4 pairs + Rudolph leading.
   All nine clearly countable, FLYING (not on ground), sleigh behind them.
   ONLY the frontmost Rudolph has a faint soft red nose. NO other nose glow.

2) RAISE Santa, the sleigh, and the reindeer team UPWARD so Santa's head and the sleigh
   sit more in FRONT OF the full moon — moon behind them as a backlight. Keep them flying
   toward the house/North Star direction. Adjust the curve slightly as needed so the
   composition still works.

KEEP LOCKED:
- Open dark sky BELOW the North Star for text — do NOT cover the star or fill that pocket.
- Warm painterly look of this image. Santa eyes open looking back with warm smile.
- Victorian house lower-right, moon left (now partially behind raised sleigh/Santa).
- Soft cream vignette all sides. NO baked text. NO boy.
"""

NEG = (
    "only 8 reindeer, only 7 reindeer, 10 reindeer, reindeer on ground, "
    "reindeer covering North Star, no open sky under star, two glowing noses, "
    "three glowing noses, laser nose, sleigh still low below moon, text, God bless, letters"
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
    if not V15B.is_file():
        raise SystemExit(f"missing: {V15B}")

    base = Image.open(V15B).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-v16-base.png"
    base.save(tmp)

    urls = [fal_client.upload_file(str(tmp))]
    print("=== Qwen S12-god-bless v16 · 9 deer + raise over moon ===")
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
    tmp_q = OUT / "_tmp-v16-qwen.png"
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

    for t in (tmp, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v16"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v16

| Field | Value |
|-------|--------|
| **version** | **v16** |
| **date** | {DAY} |
| **base** | v15b (look locked) |
| **fix** | exactly 9 deer · raise Santa/sleigh in front of moon · keep star text pocket |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v16",
                "status": "working",
                "base": "v15b",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v16", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v16-final-{DAY}.png",
        unit="S12-god-bless",
        version="v16",
        day=DAY,
        tech="Qwen 2 Pro /edit · v15b + 9th deer + raise over moon",
        subtitle="Moon behind Santa/sleigh · open sky under North Star · Rudolph only",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v16 · v15b look · 9 deer · Santa/sleigh raised over moon · "
        "star text pocket · board S12-god-bless-v16-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v16",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v16",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v16", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v16", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v16", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
