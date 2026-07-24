#!/usr/bin/env python3
"""S8 Gone v01 — Qwen 2 Pro Edit → 5250×2625 seamless spread."""
from __future__ import annotations

import io
import json
import os
import sys
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
UNIT = ROOT / "Media/development/S08-gone"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
DAY = "2026-07-23"

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD, continuous burgundy-walled room, rich oil-painting \
quality matching image 3 (S3 Eyes Met / S7 Proof quality bar). NO fake gutter, NO spine shadow, NO text, \
NO letters. Faces off the center fold.

LEFT half (p18): Young boy CENTER-LEFT standing in front of the fireplace, vintage era-neutral film camera \
IN HIS HANDS with strap around his neck (camera is the prop hero now — he picked it up). Looking slightly \
nervously UP toward the ceiling — he just missed the moment / heard roof noise. Behind him to the right of \
his figure, a wooden door stands AJAR with warm spill or night beyond. Holly pajamas. Urgency and \
disappointment — he flew out and came back too late.

RIGHT half (p19): Continuous same room — Christmas tree, boxes, gifts, and ribbons. The room WITHOUT Santa. \
Empty gift landscape · Santa's absence felt. Warm tree glow, burgundy walls. No people on the right half \
(or only a tiny distant hint of the boy at the far left edge of the right page if seamless requires — prefer \
empty room focus).

NO Santa visible anywhere. NO skylight. NO phone / modern device / screen UI.

BOY G0 LOCK: oatmeal/taupe (warm beige) holly pajamas — NOT white, NOT bright cream; green holly leaves with \
red berries clearly visible; red trim on collar, cuffs, hems; red buttons; classic button-up set. Tousled \
light brown hair with golden highlights; large expressive brown eyes; rosy cheeks. Match image 2 exactly. \
Five fingers only per hand.
"""

NEG = (
    "text, letters, typography, watermark, Santa, Santa Claus, red coat figure, skylight, "
    "roof window, phone, smartphone, glowing screen, UI icons, six fingers, extra fingers, "
    "fake gutter, spine shadow, two boys, mirrored figures"
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


def download(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board  # type: ignore

    UNIT.mkdir(parents=True, exist_ok=True)

    # Continuity: locked S7 room + boy + quality
    s7 = fal_client.upload_file(str(ROOT / "Media/development/S07-proof/_LOCKED-v03/art.png"))
    boy = fal_client.upload_file(str(ROOT / "Media/approved/characters/boy-narrator-G0.png"))
    quality = fal_client.upload_file(str(ROOT / "Media/development/S03-eyes-met/v07/art.png"))
    print("refs uploaded")

    print("=== Qwen S8 Gone v01 ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": [s7, boy, quality],
            "image_size": {"width": 2048, "height": 1024},
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checker": True,
            "enable_prompt_expansion": True,
        },
        with_logs=True,
    )
    print(result)
    url = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(url)
    print("qwen raw", raw.size)
    tmp = UNIT / "_tmp-qwen-raw.png"
    raw.save(tmp)

    print("=== SeedVR ===")
    up_url = fal_client.upload_file(str(tmp))
    up = fal_client.subscribe(
        SEEDVR,
        arguments={
            "image_url": up_url,
            "upscale_mode": "factor",
            "upscale_factor": 2,
            "noise_scale": 0.1,
            "output_format": "png",
        },
        with_logs=True,
    )
    up_im = download(up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"])
    final = up_im.resize(TARGET, Image.Resampling.LANCZOS)
    tmp.unlink(missing_ok=True)

    for name in ("art.png", "art-left.png", "art-right.png"):
        (UNIT / name).unlink(missing_ok=True)

    final.save(UNIT / "art.png", optimize=True)
    final.crop((0, 0, 2625, 2625)).save(UNIT / "art-left.png", optimize=True)
    final.crop((2625, 0, 5250, 2625)).save(UNIT / "art-right.png", optimize=True)

    (UNIT / "RECIPE.md").write_text(
        f"""# RECIPE — S08-gone / v01

| Field | Value |
|-------|--------|
| **name** | S8 Gone — missed him |
| **unit** | S08-gone |
| **book page** | Flow v2 p18\\|19 SPREAD |
| **version** | v01 |
| **date** | {DAY} |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **refs** | S07 v03 KEEP room continuity · boy-narrator-G0 · S03 v07 quality |
| **status** | working |

## Intent

L: boy + camera in hand, strap on neck, fireplace, door ajar, look-up (missed the moment). R: empty room / tree + gifts — Santa gone. No Santa figure.
""",
        encoding="utf-8",
    )
    (UNIT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v01",
                "model": QWEN,
                "seed": seed,
                "fal_url": url,
                "size": list(TARGET),
                "status": "working",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    board = INDEX / f"S08-gone-v01-spread-{DAY}.png"
    seamless_board(
        final,
        board,
        unit="S08-gone",
        version="v01",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · S7 room continuity · S3 v07 bar",
        subtitle="L boy+camera door ajar · R empty room Santa gone",
    )
    print("BOARD", board)
    print("final", UNIT / "art.png", final.size)


if __name__ == "__main__":
    main()
