#!/usr/bin/env python3
"""S12-god-bless v24 — one Qwen polish pass on locked v23 (oil warmth toward S3, keep layout)."""
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
V23 = OUT / "v23" / "art.png"
S3 = ROOT / "Media/development/S03-eyes-met/art.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625
DAY = "2026-07-27"

PROMPT = """\
POLISH ONLY — keep IMAGE 1 composition almost identical.

IMAGE 1 is the LOCKED closing spread: Santa in ornate burgundy-gold sleigh with CLOSED jacket for cold night flight, gift sack + lantern, exactly NINE reindeer harnessed in a flying line (four pairs + Rudolph leading with ONE glowing red nose only), full moon UPPER LEFT, brilliant North Star UPPER RIGHT with OPEN clear sky under the star for text, warm lit Victorian house LOWER RIGHT (boy implied by glowing windows — no boy figure), snowman + lamp, soft cream vignette frame on all sides, painted gouache/watercolor storybook, deep blue night + burgundy palette. Wide ~2:1 seamless spread. NO baked text, letters, or words.

KEEP from IMAGE 1 (do not redesign):
- Exact layout, camera, moon/star/house/sleigh positions
- Exactly 9 reindeer — count 1-2-3-4-5-6-7-8-9 — all flying ahead of sleigh
- Rudolph-only red nose; other noses brown
- Closed Santa coat (outdoor cold) — do NOT open the coat
- Cream vignette frame weight similar to IMAGE 1
- Clear empty sky pocket under the North Star (critical for InDesign type)

CHANGE / IMPROVE (subtle polish only):
- Match IMAGE 2 oil-painting richness and warm Christmas glow (S3 quality bar) — deeper brushwork, richer color, less flat digital sky
- Match IMAGE 3 atmospheric paint language (style lock) — soft blended edges, luminous controlled lights
- Slightly more airborne deer spacing/depth (not a stiff string) while keeping count at nine
- Soften thick magic snow-trail if present — finer crystalline shimmer
- Warm golden rim light on sleigh/deer from moon and North Star without blowing highlights
- Keep house warm and inviting but not competing with the star text pocket

NO TEXT. NO "God bless." NO watermark.
"""

NEG = (
    "open coat, open jacket, suspenders, striped shirt, "
    "8 reindeer, 7 reindeer, 6 reindeer, 10 reindeer, deer behind sleigh, "
    "two red noses, covering North Star, boy outside, "
    "photoreal, CGI, cartoon, text, letters, God bless, watermark, fake gutter"
)
assert len(NEG) <= 500, len(NEG)


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
    for p in (V23, S3, STYLE):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    tmp_dir = OUT / "_tmp-v24"
    tmp_dir.mkdir(exist_ok=True)

    # Qwen edit canvas ~2:1
    canvas = Image.open(V23).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    p_canvas = tmp_dir / "canvas.png"
    canvas.save(p_canvas)

    # Quality bar — crop warm interior feel as style target (full spread resized)
    s3 = Image.open(S3).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    p_s3 = tmp_dir / "s3-quality.png"
    s3.save(p_s3)

    style = Image.open(STYLE).convert("RGB")
    # fit style lock into 1024 square then pad? Qwen accepts; use 1024x1024
    style = style.resize((1024, 1024), Image.Resampling.LANCZOS)
    p_style = tmp_dir / "style-lock.png"
    style.save(p_style)

    urls = [
        fal_client.upload_file(str(p_canvas)),
        fal_client.upload_file(str(p_s3)),
        fal_client.upload_file(str(p_style)),
    ]
    print("uploaded", len(urls), "refs")
    print("=== Qwen S12-god-bless v24 · polish v23 toward S3 oil + style-lock ===")
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
    print(json.dumps({k: result.get(k) for k in ("seed", "timings")}, default=str))
    qurl = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(qurl)
    p_raw = tmp_dir / "qwen-raw.png"
    raw.save(p_raw)

    try:
        up = fal_client.subscribe(
            SEEDVR,
            arguments={
                "image_url": fal_client.upload_file(str(p_raw)),
                "upscale_mode": "factor",
                "upscale_factor": 2,
                "noise_scale": 0.1,
                "output_format": "png",
            },
            with_logs=True,
        )
        u = up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"]
        final = download(u).resize(SPREAD, Image.Resampling.LANCZOS)
        up_note = "SeedVR×2"
        print("seedvr ok")
    except Exception as e:  # noqa: BLE001
        print("SeedVR fallback", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)
        up_note = f"Pillow resize (SeedVR failed: {e})"

    vdir = OUT / "v24"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    final.save(vdir / "art.png", optimize=True)
    left.save(vdir / "art-left.png", optimize=True)
    right.save(vdir / "art-right.png", optimize=True)
    # flight crop for deer count eye
    w, h = final.size
    final.crop((int(w * 0.08), int(h * 0.02), int(w * 0.95), int(h * 0.55))).resize(
        (1800, 650), Image.Resampling.LANCZOS
    ).save(vdir / "_flight-crop.png")

    # side-by-side board v23 | v24
    a = Image.open(V23).convert("RGB").resize((1200, 600), Image.Resampling.LANCZOS)
    b = final.resize((1200, 600), Image.Resampling.LANCZOS)
    board = Image.new("RGB", (1200 * 2 + 24, 600 + 48), (252, 248, 240))
    board.paste(a, (0, 36))
    board.paste(b, (1200 + 24, 36))
    board.save(vdir / "_compare-v23-v24.png")

    recipe = f"""# RECIPE — S12-god-bless / v24

| Field | Value |
|-------|--------|
| **version** | **v24** (one polish pass — do not auto-replace locked v23) |
| **date** | {DAY} |
| **base** | v23 LOCKED composition |
| **model** | `{QWEN}` → {up_note} → 5250×2625 |
| **refs (3)** | v23 art · S03-eyes-met quality bar · style-lock-v2 |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 + L/R 2625² |
| **status** | working — Jon compare vs v23 |
| **intent** | Oil warmth toward S3 · airborne deer spacing · softer magic trail · protect North Star text pocket · KEEP closed coat + 9 deer + cream vignette |

## Prompt intent

Polish-only edit of locked v23. Do not redesign layout. Match S3 oil richness + style-lock atmosphere.

## Paths

- `Media/development/S12-god-bless/v24/art.png`
- `Media/development/S12-god-bless/v24/art-left.png`
- `Media/development/S12-god-bless/v24/art-right.png`
- Compare: `v24/_compare-v23-v24.png`
- Flight crop: `v24/_flight-crop.png`

## Note

Unit-root dashboard stays **v23 LOCKED** until Jon picks v24.
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "unit": "S12-god-bless",
                "version": "v24",
                "status": "working",
                "date": DAY,
                "model": QWEN,
                "resolution": "5250x2625",
                "seed": seed,
                "fal_url": qurl,
                "base": "v23",
                "refs": [
                    "Media/development/S12-god-bless/v23/art.png",
                    "Media/development/S03-eyes-met/art.png",
                    "Media/approved/style-refs/style-lock-v2.png",
                ],
                "paths": {
                    "art": "Media/development/S12-god-bless/v24/art.png",
                    "left": "Media/development/S12-god-bless/v24/art-left.png",
                    "right": "Media/development/S12-god-bless/v24/art-right.png",
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    for f in tmp_dir.glob("*"):
        f.unlink(missing_ok=True)
    tmp_dir.rmdir()

    print("DONE v24")
    print("seed", seed)
    print("url", qurl)
    print("saved", vdir)


if __name__ == "__main__":
    main()
