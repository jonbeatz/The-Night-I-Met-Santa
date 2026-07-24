#!/usr/bin/env python3
"""S12-god-bless v19b — START from v17 (9 deer locked); restyle Santa/sleigh from v18b only."""
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

V17 = OUT / "v17" / "art.png"  # NINE deer baked in — edit start
V18B = OUT / "v18b" / "art.png"  # Santa chuckling / sleigh / reindeer paint look

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
CRITICAL: IMAGE 1 already has the correct NINE reindeer. Do NOT remove, merge, or hide any.
Keep all nine heads countable: four pairs (rows of two) + Rudolph leading at the front.
ONLY Rudolph faint soft red nose. Wide ~2:1. NO TEXT.

IMAGE 1 = BASE (locked team): Keep the nine-reindeer formation IN FRONT of the sleigh
pulling toward the house. Keep house, snowman, lamp, vignette structure.

IMAGE 2 = LOOK reference: Restyle ONLY Santa and the sleigh (and optionally reindeer paint
quality) to match IMAGE 2 — chuckling joyful Santa, open coat, ornate gold sleigh.
Make Santa/sleigh a little SMALLER than IMAGE 2. Keep them over/in front of the moon.

Also ensure:
- Big gleaming North Star TOP-RIGHT with open sky BELOW for text.
- Team flight path toward the house as if flying over it.
- Same reindeer LOOK quality as IMAGE 2 if possible, but NEVER drop below nine deer.

Count before finishing: 1-2-3-4-5-6-7-8-9. If you would output fewer than nine, stop and
keep IMAGE 1's deer instead.
"""

NEG = (
    "only 5 reindeer, only 6, only 7, only 8, removed reindeer, merged reindeer, "
    "reindeer behind sleigh, two glowing noses, tiny North Star, covering North Star, "
    "text, God bless, letters, oversized Santa"
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
    for p in (V17, V18B):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # START FROM v17 so nine deer are in the pixels
    base = Image.open(V17).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp17 = OUT / "_tmp-v19b-v17.png"
    base.save(tmp17)
    look = Image.open(V18B).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp18 = OUT / "_tmp-v19b-v18b.png"
    look.save(tmp18)

    urls = [
        fal_client.upload_file(str(tmp17)),
        fal_client.upload_file(str(tmp18)),
    ]
    print("=== Qwen S12-god-bless v19b · v17 nine locked + v18b Santa ===")
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
    tmp_q = OUT / "_tmp-v19b-qwen.png"
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

    for t in (tmp17, tmp18, tmp_q):
        t.unlink(missing_ok=True)

    vdir = OUT / "v19b"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    w, h = final.size
    final.crop((int(w * 0.08), int(h * 0.05), int(w * 0.95), int(h * 0.62))).resize(
        (1800, 700), Image.Resampling.LANCZOS
    ).save(vdir / "_flight-crop.png")

    recipe = f"""# RECIPE — S12-god-bless / v19b

| Field | Value |
|-------|--------|
| **version** | **v19b** |
| **date** | {DAY} |
| **canvas** | v17 (nine deer locked) |
| **look** | v18b Santa/sleigh restyle only |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {"version": "v19b", "status": "working", "canvas": "v17", "look": "v18b", "seed": seed, "fal_url": qurl, "size": list(SPREAD)},
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v19b", "status": "working", "pages": "26|27"}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v19b-final-{DAY}.png",
        unit="S12-god-bless",
        version="v19b",
        day=DAY,
        tech="Qwen 2 Pro /edit · v17 nine locked + v18b Santa restyle",
        subtitle="4 pairs + Rudolph · over house · gleaming star · smaller Santa",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v19b · v17 nine-deer canvas + v18b Santa look · "
        "board S12-god-bless-v19b-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            label = "L" if side == "left" else "R"
            p.update(
                {
                    "version": "v19b",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {label} · v19b",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v19b", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v19b", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v19b", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
