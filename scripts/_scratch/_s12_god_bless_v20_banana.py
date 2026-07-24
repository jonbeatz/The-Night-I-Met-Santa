#!/usr/bin/env python3
"""S12-god-bless v20 — Gemini 3 Pro Image (Banana) edit: v17 nine + v18b look."""
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

V17 = OUT / "v17" / "art.png"  # nine deer ahead — canvas
V18B = OUT / "v18b" / "art.png"  # chuckling Santa / sleigh / reindeer paint look

# Different model from Qwen dial lane
BANANA = "fal-ai/gemini-3-pro-image-preview/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Combine these two Christmas book-spread references into ONE final oil-painting illustration.
Wide landscape ~2:1. NO text letters anywhere.

IMAGE 1 = LAYOUT / COUNT LOCK:
Keep exactly NINE reindeer harnessed IN FRONT of the sleigh, pulling it through the sky
(like horses pull a carriage). Formation: four pairs (rows of two) + Rudolph alone at the
very front. Count heads 1-2-3-4-5-6-7-8-9 before finishing. Sleigh behind the whole team.
Flying toward the Victorian house as if they will fly over it. Full moon LEFT. North Star
RIGHT — big golden gleam with cross rays; clear open dark sky BELOW the star for later
lettering. House lower-right with warm windows, snowman, lamp post, evergreens. Soft cream
vignette on all sides.

IMAGE 2 = LOOK LOCK:
Restyle Santa, sleigh, and reindeer paint quality to match this look — chuckling joyful Santa,
open red coat with striped shirt and suspenders, ornate red/gold sleigh with presents.
Make Santa and sleigh a little smaller than IMAGE 2. Place Santa/sleigh in front of the moon
(moon as backlight). Keep IMAGE 1's nine-deer positions — do not drop any deer.

ONLY Rudolph (frontmost) has a faint soft red nose. All other noses brown.
Rich storybook oil paint. One continuous scene. No duplicate Santa. No baked text.
"""


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
            with urllib.request.urlopen(url, timeout=240) as resp:
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

    # Upload full-res refs (Banana handles large refs better than forcing 2K)
    urls = [
        fal_client.upload_file(str(V17)),
        fal_client.upload_file(str(V18B)),
    ]
    print("=== Gemini/Banana S12-god-bless v20 · v17 nine + v18b look ===")
    result = fal_client.subscribe(
        BANANA,
        arguments={
            "prompt": PROMPT,
            "image_urls": urls,
            "num_images": 1,
            "aspect_ratio": "21:9",
            "resolution": "2K",
            "output_format": "png",
            "limit_generations": True,
            "safety_tolerance": "4",
        },
        with_logs=True,
    )
    print(result)
    images = result.get("images") or []
    if not images:
        raise SystemExit(f"no images: {result}")
    qurl = images[0]["url"] if isinstance(images[0], dict) else images[0]
    seed = result.get("seed")
    desc = result.get("description")
    if desc:
        print("model_description:", desc[:500])
    raw = download(qurl)
    print("banana", raw.size)
    tmp_q = OUT / "_tmp-v20-banana.png"
    raw.save(tmp_q)

    # Upscale / fit to print spread
    try:
        if max(raw.size) < 5000:
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
        else:
            final = raw.resize(SPREAD, Image.Resampling.LANCZOS)
            print("resize only")
    except Exception as e:  # noqa: BLE001
        print("SeedVR fallback", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)

    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v20"
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

    recipe = f"""# RECIPE — S12-god-bless / v20

| Field | Value |
|-------|--------|
| **version** | **v20** |
| **date** | {DAY} |
| **model** | fal-ai/gemini-3-pro-image-preview/edit (Nano Banana Pro) — NOT Qwen |
| **canvas** | v17 (nine deer lock) |
| **look** | v18b (chuckling Santa / sleigh) |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
| **note** | Alt model after Qwen count collapses (see ISSUES-RESOLVED) |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v20",
                "status": "working",
                "model": BANANA,
                "canvas": "v17",
                "look": "v18b",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v20", "status": "working", "pages": "26|27", "model": BANANA}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v20-final-{DAY}.png",
        unit="S12-god-bless",
        version="v20",
        day=DAY,
        tech="Gemini 3 Pro Image / Banana edit · v17 nine + v18b look · NOT Qwen",
        subtitle="4 pairs + Rudolph · over house · gleaming star · count check",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v20 · Banana/Gemini (not Qwen) · v17 nine + v18b look · "
        "board S12-god-bless-v20-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            label = "L" if side == "left" else "R"
            p.update(
                {
                    "version": "v20",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {label} · v20",
                    "model": "Gemini 3 Pro Image edit · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v20", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v20", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v20", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
