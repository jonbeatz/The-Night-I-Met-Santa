#!/usr/bin/env python3
"""S12-god-bless v15 — v14 look/feel + v11 flying path; exactly 9 deer, Rudolph only."""
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

V11 = OUT / "v11" / "art.png"  # scene / flight path toward house + open sky under star
V14 = OUT / "v14" / "art.png"  # look & feel lock
FACE = ROOT / "Images/styles1/santa-G0-face.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Combine two Christmas spreads into one FINAL. Wide ~2:1. NO TEXT.

IMAGE 1 = SCENE / FLIGHT PATH (v11): KEEP this composition.
Santa's sleigh and reindeer are FLYING in the sky — NOT on the ground, NOT walking in snow.
They fly UPWARD toward the North Star / house direction (upper-right path), clearly ABOVE
the treeline and ABOVE the Victorian house. Reindeer IN FRONT of the sleigh pulling it.
North Star stays upper-right with OPEN dark sky BELOW it for later text — do NOT cover
the star with reindeer. Full moon left. House lower-right with snowman, lamp, evergreens.
Cream vignette all sides.

IMAGE 2 = LOOK & FEEL (v14): Restyle paint quality to match v14 — Santa face/sleigh
richness, reindeer fur/antler quality, warm painterly atmosphere, color richness. Santa
eyes OPEN looking back toward us with a warm gentle smile.

IMAGE 3 = Santa G0 face lock — warm smile, open eyes, rosy cheeks.

REINDEER RULE (mandatory):
- Exactly NINE reindeer visible and countable: 4 pairs + Rudolph leading solo at front.
- ALL nine FLYING AHEAD of the sleigh, harnessed, pulling like horses. Sleigh behind them.
- NOT on the ground. Clear air under their hooves above the house/trees.
- ONLY Rudolph (frontmost) has a faint soft red nose. NO other nose glow.
- Do not hide deer so the count drops below nine — show all nine clearly.

NO baked text. NO boy. NO duplicate Santa.
"""

NEG = (
    "reindeer on the ground, walking on snow, galloping on snow, sleigh on the ground, "
    "tracks in snow under hooves, reindeer covering the North Star, "
    "reindeer behind the sleigh, only 5 reindeer, only 6 reindeer, only 7 reindeer, "
    "only 8 reindeer, 10 reindeer, two glowing noses, laser nose, neon nose, "
    "eyes closed, text, God bless, letters, boy"
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
    for p in (V11, V14, FACE):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # Start FROM v11 so flying altitude / star pocket are baked in
    base = Image.open(V11).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp11 = OUT / "_tmp-v15-v11.png"
    base.save(tmp11)
    style = Image.open(V14).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp14 = OUT / "_tmp-v15-v14.png"
    style.save(tmp14)

    urls = [
        fal_client.upload_file(str(tmp11)),
        fal_client.upload_file(str(tmp14)),
        fal_client.upload_file(str(FACE)),
    ]
    print("=== Qwen S12-god-bless v15 · v14 look + v11 flight ===")
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
    tmp_q = OUT / "_tmp-v15-qwen.png"
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

    for t in (tmp11, tmp14, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v15"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v15

| Field | Value |
|-------|--------|
| **version** | **v15** |
| **date** | {DAY} |
| **look** | v14 (Santa, sleigh, reindeer paint, atmosphere) |
| **scene / flight** | v11 (flying toward house/star, open sky under North Star) |
| **face** | Images/styles1/santa-G0-face.png |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
| **note** | Fix v14 ground-level + short deer count |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v15",
                "status": "working",
                "look": "v14",
                "scene": "v11",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v15", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v15-final-{DAY}.png",
        unit="S12-god-bless",
        version="v15",
        day=DAY,
        tech="Qwen 2 Pro /edit · v14 look + v11 flight · 9 ahead · Rudolph only",
        subtitle="Flying toward house/star · open sky under North Star for text",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v15 · v14 look + v11 flight path · 9 ahead · Rudolph only · "
        "board S12-god-bless-v15-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v15",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v15",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v15", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v15", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v15", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
