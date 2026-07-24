#!/usr/bin/env python3
"""S12-god-bless v16b — force 9th deer + stronger raise over moon (from v16)."""
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

V16 = OUT / "v16" / "art.png"
V11 = OUT / "v11" / "art.png"  # nine-deer count reference

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Edit IMAGE 1. Keep the SAME beautiful look/feel. Wide ~2:1. NO TEXT.

CRITICAL FIX A — COUNT NINE REINDEER:
IMAGE 1 still has only eight. You MUST add ONE more reindeer into the flying harnessed
team in front of the sleigh. Final count = 9 = four pairs + Rudolph leading.
Count the reindeer heads before finishing: 1 2 3 4 5 6 7 8 9. All flying ahead of sleigh.
ONLY Rudolph (frontmost) faint red nose. Use IMAGE 2 only as a count/formation hint for nine.

CRITICAL FIX B — RAISE OVER THE MOON:
Move Santa, sleigh, AND the whole reindeer team CLEARLY HIGHER so the full moon sits
BEHIND them as a backlight. Santa's head and the sleigh body should overlap the moon disk
more strongly (moon behind Santa/sleigh, not mostly empty sky above them).

KEEP:
- Open dark sky BELOW the North Star for text (do not cover the star).
- House, snowman, lamp, vignette, painterly look of IMAGE 1.
- Flying toward house/star. NO baked text.
"""

NEG = (
    "only 8 reindeer, eight reindeer, only 7, reindeer on ground, "
    "Santa below the moon, sleigh under the moon with empty moon above, "
    "reindeer covering North Star, two glowing noses, text, God bless, letters"
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
    for p in (V16, V11):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    base = Image.open(V16).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp16 = OUT / "_tmp-v16b-base.png"
    base.save(tmp16)
    ref = Image.open(V11).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp11 = OUT / "_tmp-v16b-v11.png"
    ref.save(tmp11)

    urls = [
        fal_client.upload_file(str(tmp16)),
        fal_client.upload_file(str(tmp11)),
    ]
    print("=== Qwen S12-god-bless v16b · force 9 + moon backlight ===")
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
    tmp_q = OUT / "_tmp-v16b-qwen.png"
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

    for t in (tmp16, tmp11, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v16b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v16b

| Field | Value |
|-------|--------|
| **version** | **v16b** |
| **date** | {DAY} |
| **base** | v16 |
| **ref** | v11 (9-count hint) |
| **fix** | force 9th deer · stronger raise over moon · star text pocket |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v16b",
                "status": "working",
                "base": "v16",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v16b", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v16b-final-{DAY}.png",
        unit="S12-god-bless",
        version="v16b",
        day=DAY,
        tech="Qwen 2 Pro /edit · v16 + force 9 deer + moon backlight",
        subtitle="Santa/sleigh over moon · open sky under North Star · Rudolph only",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v16b · 9 deer · Santa/sleigh raised over moon · star text pocket · "
        "board S12-god-bless-v16b-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v16b",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v16b",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v16b", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v16b", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v16b", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
