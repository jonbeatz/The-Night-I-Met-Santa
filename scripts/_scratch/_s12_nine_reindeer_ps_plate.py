#!/usr/bin/env python3
"""S12 helper — nine v12-style reindeer on clean sky for Photoshop cutout."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/development/S12-god-bless/assets"
V12 = ROOT / "Media/development/S12-god-bless/v12/art.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
DAY = "2026-07-23"

PROMPT = """\
Create a CLEAN Photoshop cutout plate from IMAGE 1's reindeer style only.

Show exactly NINE reindeer flying through a simple deep blue night sky.
Same paint style, fur, antlers, and harness look as the reindeer in IMAGE 1.
All nine IN ONE connected team, harnessed, flying left-to-right in a gentle upward
curve: four pairs side-by-side + one lead Rudolph at the front (smallest).
ONLY Rudolph has a faint soft red nose. All other noses brown.
Count: 1-2-3-4-5-6-7-8-9.

NO Santa. NO sleigh. NO house. NO snowman. NO North Star. NO moon.
NO presents. NO text. NO vignette frame.
Just the nine reindeer clearly separated from a plain deep-blue night sky so they
are easy to cut out in Photoshop. Leave generous empty sky around the team.
Wide ~2:1 landscape.
"""

NEG = (
    "Santa, sleigh, house, snowman, moon, North Star, text, vignette, cream border, "
    "only 7 reindeer, only 8, 10 reindeer, reindeer on ground, two glowing noses, "
    "boy, watermark"
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
    if not V12.is_file():
        raise SystemExit(f"missing: {V12}")
    OUT.mkdir(parents=True, exist_ok=True)

    base = Image.open(V12).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-nine-deer-base.png"
    base.save(tmp)

    print("=== Qwen · nine v12-style reindeer PS plate ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": [fal_client.upload_file(str(tmp))],
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
    tmp_q = OUT / "_tmp-nine-deer-qwen.png"
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

    out_png = OUT / "nine-reindeer-v12-style-ps-plate.png"
    final.save(out_png, optimize=True)
    # also a tighter flight crop for easier select
    w, h = final.size
    final.crop((int(w * 0.05), int(h * 0.15), int(w * 0.95), int(h * 0.75))).save(
        OUT / "nine-reindeer-v12-style-ps-plate-crop.png", optimize=True
    )

    meta = {
        "purpose": "Photoshop cutout — nine reindeer in v12 paint style",
        "source_style": "Media/development/S12-god-bless/v12/art.png",
        "seed": seed,
        "fal_url": qurl,
        "size": list(SPREAD),
        "date": DAY,
        "note": "No Santa/sleigh/house — sky plate for compositing into S12",
    }
    (OUT / "nine-reindeer-v12-style-ps-plate.meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )
    (OUT / "RECIPE-nine-reindeer-ps-plate.md").write_text(
        f"""# Nine reindeer PS plate (v12 style)

| Field | Value |
|-------|--------|
| **file** | `nine-reindeer-v12-style-ps-plate.png` |
| **crop** | `nine-reindeer-v12-style-ps-plate-crop.png` |
| **style from** | S12-god-bless/v12 |
| **seed** | {seed} |
| **size** | 5250×2625 |
| **use** | Cut out the team and paste into your S12 Photoshop master |

Count heads before using — should be nine (4 pairs + Rudolph faint nose).
""",
        encoding="utf-8",
    )
    print("DONE", out_png, "seed", seed)


if __name__ == "__main__":
    main()
