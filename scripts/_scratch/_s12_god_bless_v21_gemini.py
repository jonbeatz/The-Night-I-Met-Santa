#!/usr/bin/env python3
"""S12-god-bless v21 — Gemini 3 Pro Image edit with operator's exact FINAL prompt."""
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

FACE = ROOT / "Images/styles1/santa-G0-face.png"
G0V2 = ROOT / "Images/styles1/santa-G0-v2.png"
S03 = ROOT / "Media/development/S03-eyes-met/v07/art.png"

BANANA = "fal-ai/gemini-3-pro-image-preview/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

# Operator exact prompt (model line swapped to Gemini per this request)
PROMPT = """\
S12 God Bless — FINAL. FULL SPREAD at 5250×2625. This is a fresh start with all requirements in one clear prompt.

IMAGE 1 = Santa G0 face lock. IMAGE 2 = Santa G0 v2 wardrobe (open coat, striped shirt, suspenders).
IMAGE 3 = S3 eyes-met v07 oil-painting quality / storybook style lock.

A simple, beautiful Christmas Eve scene. Santa Claus flies across the night sky in his sleigh, pulled by nine reindeer, over a snowy house below. The full moon glows on the left. The North Star gleams on the right. A snowman stands in the yard. Snow-covered evergreens frame the peaceful winter landscape.

THE REINDEER — MOST IMPORTANT:
Nine reindeer TOTAL. All nine are HARNESSED TOGETHER as one connected team, every single one IN FRONT OF the sleigh, PULLING it through the sky. Think of horses pulling a carriage — the horses lead, the carriage follows. The reindeer lead, the sleigh follows behind. They are arranged: four pairs flying side by side, plus one lead reindeer (Rudolph) at the very front of the formation. The entire team curves gracefully in a dynamic arc across the sky toward the house. Count them before saving: 1-2-3-4-5-6-7-8-9. Only Rudolph (the very first one, smallest, at the front) has a FAINT soft red glow on his nose — barely visible, a subtle warm hint. No other reindeer has any red nose. Brown noses only.

SANTA:
Santa G0 v2 — the same Santa from every spread in this book. Open red coat with cream striped shirt visible underneath, brown suspenders over the shirt. Warm, kind, grandfatherly face — soft eyes with laugh lines, rosy cheeks, gentle smile. Eyes open, looking back toward the house with warmth. Sitting in an ornate red sleigh with gold decorative trim. The sleigh is filled with wrapped presents in reds, greens, and golds. A small lantern hangs from the sleigh with a warm golden glow.

SKY:
Deep blue night sky. Full moon on the LEFT — large, luminous, casting soft light across the scene. North Star on the RIGHT — bright golden-yellow gleam with soft shimmering cross-shaped rays and a gentle halo. CLEAR OPEN dark blue sky directly below the star — this is where "God bless" will be placed in InDesign. The text area must be unobstructed.

GROUND:
Victorian house in the lower-right — larger and prominent. Warm golden-yellow light glowing from multiple windows. Snow on the roof. Snowman with a scarf standing in the front yard. Snow-covered evergreen trees framing the scene. A traditional lamp post near the house with a warm glow. Rolling snowy hills. Simple, peaceful, clean.

STYLE AND RULES:
Rich oil-painting quality matching S3 v07. Standard watercolor vignette — soft dissolve to cream on ALL sides evenly. NO baked text anywhere — "God bless" goes in InDesign. NO duplicate Santa or sleigh. ONE continuous painted scene across both pages. This is the final story image of the book.

Gemini 3 Pro Image edit (Nano Banana Pro). Save all three files (art.png, art-left.png, art-right.png).
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
    for p in (FACE, G0V2, S03):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    urls = [
        fal_client.upload_file(str(FACE)),
        fal_client.upload_file(str(G0V2)),
        fal_client.upload_file(str(S03)),
    ]
    print("=== Gemini S12-god-bless v21 · exact FINAL prompt ===")
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
    raw = download(qurl)
    print("banana", raw.size)
    tmp_q = OUT / "_tmp-v21-banana.png"
    raw.save(tmp_q)

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

    vdir = OUT / "v21"
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

    recipe = f"""# RECIPE — S12-god-bless / v21

| Field | Value |
|-------|--------|
| **version** | **v21** |
| **date** | {DAY} |
| **model** | fal-ai/gemini-3-pro-image-preview/edit |
| **prompt** | Operator exact FINAL brief |
| **refs** | santa-G0-face · santa-G0-v2 · S03-eyes-met/v07 |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v21",
                "status": "working",
                "model": BANANA,
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps({"unit": "S12-god-bless", "version": "v21", "status": "working", "pages": "26|27", "model": BANANA}, indent=2),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v21-final-{DAY}.png",
        unit="S12-god-bless",
        version="v21",
        day=DAY,
        tech="Gemini 3 Pro Image edit · exact FINAL prompt · G0 + S3 v07",
        subtitle="Nine ahead · Rudolph faint · star text pocket · open coat",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v21 · Gemini exact FINAL prompt · "
        "board S12-god-bless-v21-final-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            label = "L" if side == "left" else "R"
            p.update(
                {
                    "version": "v21",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {label} · v21",
                    "model": "Gemini 3 Pro Image edit · 5250×2625",
                    "unit": "S12-god-bless",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update({"version": "merged-v21", "status": "merged", "date": DAY, "notes": "Absorbed — " + note})
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v21", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v21", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
