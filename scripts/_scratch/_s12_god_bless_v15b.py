#!/usr/bin/env python3
"""S12-god-bless v15b — add to 9 deer + restore North Star; keep v15 flight/look."""
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

V15 = OUT / "v15" / "art.png"
V11 = OUT / "v11" / "art.png"  # 9-deer flight + North Star pocket

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Surgical edit. KEEP IMAGE 1 look, Santa, sleigh, flying altitude, house, moon, vignette.
Wide ~2:1. NO TEXT.

FIX ONLY:
1) REINDEER COUNT = exactly NINE. IMAGE 1 is short — ADD reindeer in the same flying
   harnessed curve IN FRONT of the sleigh until there are 4 pairs + Rudolph leading = 9.
   All FLYING (clear air under hooves), none on the ground, none behind the sleigh.
   Show all nine clearly countable. ONLY Rudolph (frontmost) faint soft red nose.
2) Restore a bright warm yellow North Star upper-RIGHT with gleaming cross rays, like
   IMAGE 2. Keep OPEN dark sky BELOW the star for text — reindeer must NOT cover the star.

IMAGE 2 = reference for nine-deer flight path + North Star placement only.
Keep IMAGE 1 painterly look/feel. Santa eyes open looking back. NO baked text.
"""

NEG = (
    "only 7 reindeer, only 8 reindeer, 6 reindeer, reindeer on ground, "
    "reindeer covering North Star, no North Star, missing star, "
    "two glowing noses, reindeer behind sleigh, text, God bless, letters"
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
    for p in (V15, V11):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    base = Image.open(V15).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp15 = OUT / "_tmp-v15b-base.png"
    base.save(tmp15)
    ref = Image.open(V11).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp11 = OUT / "_tmp-v15b-v11.png"
    ref.save(tmp11)

    urls = [
        fal_client.upload_file(str(tmp15)),
        fal_client.upload_file(str(tmp11)),
    ]
    print("=== Qwen S12-god-bless v15b · 9 deer + North Star ===")
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
    tmp_q = OUT / "_tmp-v15b-qwen.png"
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

    for t in (tmp15, tmp11, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v15b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v15b

| Field | Value |
|-------|--------|
| **version** | **v15b** |
| **date** | {DAY} |
| **base** | v15 (v14 look + v11 flight) |
| **fix** | exactly 9 deer + North Star with open sky below |
| **ref** | v11 |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v15b",
                "status": "working",
                "base": "v15",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v15b", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v15b-final-{DAY}.png",
        unit="S12-god-bless",
        version="v15b",
        day=DAY,
        tech="Qwen 2 Pro /edit · v15 + 9 deer + North Star pocket",
        subtitle="Flying · open sky under star for God bless · Rudolph only",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v15b · v14 look + v11 flight · 9 ahead · North Star text pocket · "
        "board S12-god-bless-v15b-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v15b",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v15b",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v15b", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v15b", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v15b", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
