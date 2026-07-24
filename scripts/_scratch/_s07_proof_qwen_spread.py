#!/usr/bin/env python3
"""S7 Proof seamless spread — Qwen 2 Pro Edit v06 → 5250×2625. One art.png only."""
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
UNIT = ROOT / "Media/development/S07-proof"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
DAY = "2026-07-23"

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD, continuous single painting across both pages, \
NO fake book gutter, NO center spine shadow, NO text, NO letters, NO watermark.

LEFT half: full room establishing shot — decorated Christmas tree with warm glow, stone fireplace \
with bright firelight, burgundy walls, cozy living room, gifts present but not a gift-sea overload, \
rich oil-painting / soft gouache quality.

RIGHT half: young boy looking sharply UP toward the ceiling with surprise and urgency — he heard \
reindeer noise on the roof; the idea has struck him that he needs proof. Era-neutral classic camera \
body in his hand OR resting on a nearby side table — film/vintage camera, black or brown body with \
lens, NOT a phone, NOT a modern smartphone, NOT a tablet, NO glowing screen, NO UI icons. \
Holly pajamas. Santa Claus may be partly visible at the edge shifting away into shadow or already \
mostly gone — this beat is about the boy's realization, not a Santa portrait.

Same continuous floor, lighting, and room across the full width. Warm firelight + tree glow. \
Rich gift-book oil-painting quality matching image 3 quality bar.

BOY G0 LOCK: oatmeal/taupe (warm beige) holly pajamas — NOT white, NOT cream, NOT bright; green \
holly leaves with red berries clearly visible across the fabric; red trim on collar, sleeve cuffs, \
and pant hems; red buttons down the front; classic button-up pajama set. Tousled light brown hair \
with golden highlights; large expressive brown eyes; rosy cheeks. Match image 2 exactly — no drift.

SANTA WARDROBE LOCK (if Santa visible): red coat worn OPEN and unbuttoned; cream/off-white vertically \
striped shirt; brown leather suspenders over the striped shirt (NOT over the coat); red pants; black \
boots; white fur trim. Match santa-G0-v2 — partial figure only if shown.
"""

NEG = (
    "text, letters, typography, watermark, signature, phone, smartphone, iPhone, Android, "
    "tablet, glowing screen, UI icons, selfie stick, modern device, plastic CGI, photoreal photo, "
    "mirrored twin figures, two boys, two Santas, fake gutter, spine shadow"
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
    # wipe prior development clutter first
    for p in UNIT.iterdir():
        if p.name == ".gitkeep":
            continue
        if p.is_file():
            p.unlink()
        elif p.is_dir():
            import shutil

            shutil.rmtree(p)

    style = fal_client.upload_file(str(ROOT / "Media/approved/style-refs/style-lock-v2.png"))
    boy = fal_client.upload_file(str(ROOT / "Media/approved/characters/boy-narrator-G0.png"))
    # Prefer room quality from S5 chat seamless if present, else S3
    s5 = ROOT / "Media/development/S05-chat/art.png"
    s3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
    quality = fal_client.upload_file(str(s5 if s5.exists() else s3))
    print("refs uploaded")

    print("=== Qwen 2 Pro Edit (spread) ===")
    # Native Qwen max ~2048×1024 landscape under pixel budget; upscale to print then delete temp
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": [style, boy, quality],
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

    # Upscale toward print via SeedVR factor 2 → then Lanczos to exact 5250×2625
    print("=== SeedVR upscale ===")
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
    print(up)
    up_im = download(up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"])
    print("seedvr", up_im.size)
    final = up_im.resize(TARGET, Image.Resampling.LANCZOS)
    art = UNIT / "art.png"
    final.save(art, optimize=True)
    # also write chops for InDesign convenience? User said one final — art.png only for seamless
    # Optional left/right chops for FLOW paths that expect art-left/right — user Flow has art-left/right
    left = final.crop((0, 0, 2625, 2625))
    right = final.crop((2625, 0, 5250, 2625))
    left.save(UNIT / "art-left.png", optimize=True)
    right.save(UNIT / "art-right.png", optimize=True)

    # delete intermediates
    tmp.unlink(missing_ok=True)
    print("final", art, final.size)

    (UNIT / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v01

| Field | Value |
|-------|--------|
| **name** | S7 Proof — seamless spread |
| **unit** | S07-proof |
| **book page** | Flow v2 p16\\|17 SPREAD |
| **version** | v01 |
| **date** | {DAY} |
| **model** | `{QWEN}` (v06) → SeedVR×2 → Lanczos **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **refs** | style-lock-v2 · boy-narrator-G0 · S05-chat quality bar |
| **status** | working |
| **files** | `art.png` (master) · `art-left.png` / `art-right.png` (chops of same plate) |

## Intent

L: full room establish (tree + fireplace, burgundy walls). R: boy look-up urgency + era-neutral classic camera; Santa optional half-gone. Hard wardrobe append. No phones.
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
    board = INDEX / f"S07-proof-v01-spread-{DAY}.png"
    seamless_board(
        final,
        board,
        unit="S07-proof",
        version="v01",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · S5 quality bar",
        subtitle="L room establish · R boy look-up + classic camera · Santa optional half-gone",
    )
    print("BOARD", board)


if __name__ == "__main__":
    main()
