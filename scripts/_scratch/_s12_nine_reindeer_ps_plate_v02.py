#!/usr/bin/env python3
"""Bump PS plate from ~7 to exactly 9 reindeer."""
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
BASE = OUT / "nine-reindeer-v12-style-ps-plate.png"
V12 = ROOT / "Media/development/S12-god-bless/v12/art.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)

PROMPT = """\
ONE CHANGE ONLY. IMAGE 1 is a Photoshop reindeer cutout plate that is SHORT on count.
ADD exactly TWO more reindeer into the same flying harnessed team so the total is NINE.
Keep the same style as IMAGE 1 / IMAGE 2. Formation: four pairs + Rudolph leading.
ONLY Rudolph faint red nose. NO Santa, NO sleigh, NO house. Plain deep blue sky only.
Count heads: 1-2-3-4-5-6-7-8-9. Wide ~2:1.
"""

NEG = "Santa, sleigh, house, only 7, only 8, 10 reindeer, two glowing noses, text, vignette"


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
    base = Image.open(BASE).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp = OUT / "_tmp-nine-b.png"
    base.save(tmp)
    ref = Image.open(V12).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp12 = OUT / "_tmp-nine-v12.png"
    ref.save(tmp12)

    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": [fal_client.upload_file(str(tmp)), fal_client.upload_file(str(tmp12))],
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
    tmp_q = OUT / "_tmp-nine-bq.png"
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
    except Exception as e:  # noqa: BLE001
        print("SeedVR fallback", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)

    for t in (tmp, tmp12, tmp_q):
        t.unlink(missing_ok=True)

    import shutil

    v1 = OUT / "nine-reindeer-v12-style-ps-plate-v01-7deer.png"
    if BASE.is_file():
        shutil.copy2(BASE, v1)

    out = OUT / "nine-reindeer-v12-style-ps-plate.png"
    final.save(out, optimize=True)
    w, h = final.size
    final.crop((int(w * 0.05), int(h * 0.15), int(w * 0.95), int(h * 0.75))).save(
        OUT / "nine-reindeer-v12-style-ps-plate-crop.png", optimize=True
    )
    (OUT / "nine-reindeer-v12-style-ps-plate.meta.json").write_text(
        json.dumps({"version": "v02-add-to-nine", "seed": seed, "fal_url": qurl, "size": list(SPREAD)}, indent=2),
        encoding="utf-8",
    )
    print("DONE", out, "seed", seed)


if __name__ == "__main__":
    main()
