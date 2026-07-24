#!/usr/bin/env python3
"""S7 Proof v02 — Qwen 2 Pro Edit → 5250×2625. Fix fingers/cameras/Santa/skylight."""
from __future__ import annotations

import io
import json
import os
import shutil
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
Wide seamless Christmas living-room storybook SPREAD, ONE continuous burgundy-walled room across both pages, \
rich oil-painting / soft gouache quality matching image 3 quality bar. NO fake book gutter, NO center spine \
shadow, NO text, NO letters, NO watermark. Faces and heroes OFF the center fold.

LEFT half (p16 — room ONLY): full Christmas living-room establishing shot. Stone fireplace with firelight \
and stockings on the mantel. Tall decorated Christmas tree with warm lights and wrapped gifts at the base. \
Burgundy walls. Cozy rug. Warm golden firelight + tree glow. NO people on the left — no boy, no Santa, \
empty room scenery only.

RIGHT half (p17 — boy realization): young boy standing on the RIGHT side of the frame looking sharply UP \
toward a plain ceiling (hearing reindeer on the roof) with surprise and urgency. A single vintage \
era-neutral classic camera body sits on a nearby wooden table or shelf — catching his eye, giving him the \
idea for proof. He is NOT holding the camera — hands empty or at his sides. ONLY ONE camera in the entire \
spread. NO skylight, NO roof window, NO glass ceiling panel. NO Santa anywhere — Santa is gone / just out \
of frame, completely absent from the image.

Seamless continuous burgundy walls, floor, and warm lighting connecting left to right. Distinct left/right \
jobs: scenery establish vs boy look-up moment.

BOY G0 LOCK: oatmeal/taupe (warm beige) holly pajamas — NOT white, NOT cream, NOT bright; green holly \
leaves with red berries clearly visible; red trim on collar, cuffs, hems; red buttons; classic button-up \
set. Tousled light brown hair with golden highlights; large expressive brown eyes; rosy cheeks. Match \
image 2 exactly — five fingers only per hand, correct anatomy.
"""

NEG = (
    "text, letters, typography, watermark, signature, skylight, roof window, glass ceiling, "
    "Santa, Santa Claus, red coat figure, beard figure, second camera, two cameras, holding camera, "
    "camera in hands, phone, smartphone, glowing screen, UI icons, six fingers, extra fingers, "
    "mutated hands, fake gutter, spine shadow, boy on left, child on left half"
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


def wipe_pngs() -> None:
    UNIT.mkdir(parents=True, exist_ok=True)
    for p in list(UNIT.iterdir()):
        if p.name == ".gitkeep":
            continue
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            p.unlink()
        elif p.name.startswith("_tmp"):
            p.unlink(missing_ok=True)


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board  # type: ignore

    UNIT.mkdir(parents=True, exist_ok=True)

    style = fal_client.upload_file(str(ROOT / "Media/approved/style-refs/style-lock-v2.png"))
    boy = fal_client.upload_file(str(ROOT / "Media/approved/characters/boy-narrator-G0.png"))
    quality = fal_client.upload_file(str(ROOT / "Media/development/S05-chat/art.png"))
    print("refs uploaded")

    print("=== Qwen 2 Pro Edit v02 ===")
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
    up_im = download(up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"])
    print("seedvr", up_im.size)
    final = up_im.resize(TARGET, Image.Resampling.LANCZOS)

    # Replace keepers only after success; delete intermediates
    wipe_pngs()
    art = UNIT / "art.png"
    final.save(art, optimize=True)
    final.crop((0, 0, 2625, 2625)).save(UNIT / "art-left.png", optimize=True)
    final.crop((2625, 0, 5250, 2625)).save(UNIT / "art-right.png", optimize=True)
    tmp.unlink(missing_ok=True)

    (UNIT / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v02

| Field | Value |
|-------|--------|
| **name** | S7 Proof — seamless spread v02 |
| **unit** | S07-proof |
| **book page** | Flow v2 p16\\|17 SPREAD |
| **version** | v02 |
| **date** | {DAY} |
| **model** | `{QWEN}` (v06) → SeedVR×2 → Lanczos **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **refs** | style-lock-v2 · boy-narrator-G0 · S05-chat quality |
| **status** | working |
| **fixes vs v01** | L room-only · R boy look-up · camera on table (not held) · no skylight · no Santa · one camera · 5 fingers |

## Intent

L: fireplace + tree establish, no people. R: boy up-look urgency; vintage camera on table catching his eye; Santa gone; plain ceiling.
""",
        encoding="utf-8",
    )
    (UNIT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v02",
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
    board = INDEX / f"S07-proof-v02-spread-{DAY}.png"
    seamless_board(
        final,
        board,
        unit="S07-proof",
        version="v02",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · S5 quality bar",
        subtitle="L room only · R boy look-up + table camera · no Santa · no skylight",
    )
    print("BOARD", board)
    print("final", art, final.size)


if __name__ == "__main__":
    main()
