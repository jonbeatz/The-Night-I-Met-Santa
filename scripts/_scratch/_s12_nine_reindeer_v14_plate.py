#!/usr/bin/env python3
"""S12 helper — nine reindeer PS plate from v14 angle/style (full legs, toward house)."""
from __future__ import annotations

import io
import json
import os
import shutil
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/development/S12-god-bless/assets"
V14 = ROOT / "Media/development/S12-god-bless/v14/art.png"
V11 = ROOT / "Media/development/S12-god-bless/v11/art.png"  # 9-ahead curve toward house
S03 = ROOT / "Media/development/S03-eyes-met/v07/art.png"  # dialed book watercolor/oil feel

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
DAY = "2026-07-23"

PROMPT = """\
Photoshop cutout plate for a Christmas book spread. Wide ~2:1. NO text.

IMAGE 1 (v14) = REINDEER STYLE + CAMERA ANGLE LOCK (most important):
Match these exact reindeer — fur, antlers, harnesses, body proportions, and the SIDE-PROFILE
flying angle as if galloping through the air TOWARD the lower-right (toward a house off-frame).
Show FULL LEGS on every reindeer — no cropped hooves, no cut-off limbs at the frame edge.
Keep the same painterly v14 look.

IMAGE 2 (v11) = COUNT + FORMATION hint only:
Exactly NINE reindeer: four pairs side-by-side + Rudolph leading at the front.
All IN FRONT of where a sleigh would be, harnessed as one team, curved arc flying toward
the house direction. Count: 1-2-3-4-5-6-7-8-9.
ONLY Rudolph (frontmost) faint soft red nose. Brown noses on all others.

IMAGE 3 (S3 v07) = book LOOK & FEEL: rich soft oil / watercolor storybook paint quality
matching our dialed Christmas book art — warm, soft edges, not photoreal, not hard CGI.

SCENE FOR THE PLATE:
Deep blue night sky with soft painterly clouds. Optional faint snowy ground along the VERY
bottom only so perspective reads as flying above landscape — but keep sky mostly open for
easy masking. NO Santa. NO sleigh. NO house. NO snowman. NO moon. NO North Star. NO vignette
cream frame. Generous margin around the whole team so legs are never clipped.

Emphasize: same angle as IMAGE 1, nine deer, full visible legs, flying toward house/right.
"""

NEG = (
    "cropped legs, cut off hooves, truncated limbs, legs missing, "
    "Santa, sleigh, house, snowman, moon, North Star, cream vignette border, text, "
    "only 4 reindeer, only 5, only 6, only 7, only 8, 10 reindeer, "
    "reindeer facing camera head-on, reindeer on the ground walking, "
    "two glowing noses, three glowing noses, photoreal photo, hard CGI"
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
    for p in (V14, V11, S03):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")
    OUT.mkdir(parents=True, exist_ok=True)

    # Archive prior plate if present
    old = OUT / "nine-reindeer-v12-style-ps-plate.png"
    if old.is_file():
        shutil.copy2(old, OUT / "nine-reindeer-v12-style-ps-plate-archive.png")

    tmp14 = OUT / "_tmp-v14.png"
    tmp11 = OUT / "_tmp-v11.png"
    tmp03 = OUT / "_tmp-s03.png"
    Image.open(V14).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS).save(tmp14)
    Image.open(V11).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS).save(tmp11)
    Image.open(S03).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS).save(tmp03)

    # Start FROM v14 so angle/style are baked in
    urls = [
        fal_client.upload_file(str(tmp14)),
        fal_client.upload_file(str(tmp11)),
        fal_client.upload_file(str(tmp03)),
    ]
    print("=== Qwen · nine reindeer PS plate from v14 angle ===")
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
    tmp_q = OUT / "_tmp-deer-qwen.png"
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

    for t in (tmp14, tmp11, tmp03, tmp_q):
        t.unlink(missing_ok=True)

    out = OUT / "nine-reindeer-v14-angle-ps-plate.png"
    final.save(out, optimize=True)
    w, h = final.size
    final.crop((int(w * 0.02), int(h * 0.08), int(w * 0.98), int(h * 0.85))).save(
        OUT / "nine-reindeer-v14-angle-ps-plate-crop.png", optimize=True
    )

    meta = {
        "purpose": "PS cutout — nine reindeer matching v14 angle/style, flying toward house",
        "style_ref": "v14/art.png",
        "formation_ref": "v11/art.png",
        "look_ref": "S03-eyes-met/v07",
        "model": QWEN,
        "seed": seed,
        "fal_url": qurl,
        "size": list(SPREAD),
        "date": DAY,
    }
    (OUT / "nine-reindeer-v14-angle-ps-plate.meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )
    (OUT / "RECIPE-nine-reindeer-v14-plate.md").write_text(
        f"""# Nine reindeer PS plate — v14 angle

| Field | Value |
|-------|--------|
| **file** | `nine-reindeer-v14-angle-ps-plate.png` |
| **crop** | `nine-reindeer-v14-angle-ps-plate-crop.png` |
| **style/angle** | S12-god-bless/v14 |
| **formation hint** | v11 |
| **look** | S03-eyes-met/v07 |
| **model** | Qwen 2 Pro /edit |
| **seed** | {seed} |
| **size** | 5250×2625 |

Goals: 9 deer · full legs · side profile toward house · Rudolph faint only · book paint feel.
""",
        encoding="utf-8",
    )
    print("DONE", out, "seed", seed)


if __name__ == "__main__":
    main()
