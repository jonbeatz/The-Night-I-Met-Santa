#!/usr/bin/env python3
"""S7 Proof v03 — composition lock from mocks/S07-proof/v06 → 5250×2625 Qwen."""
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
COMP = ROOT / "Media/generated/mocks/S07-proof/v06/art.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
DAY = "2026-07-23"

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD. PRESERVE the COMPOSITION of image 1 exactly \
as the layout guide: asymmetrical cinematic depth — vintage camera + gifts in FOREGROUND on the \
wooden floor (camera prominent, boy has NOT picked it up yet), Christmas tree full and decorated \
on the LEFT, boy on the RIGHT looking sharply UPWARD with strong dramatic gaze (heard reindeer on \
the roof), diagonal floorboards guiding the eye, clear layers foreground / middle / background. \
NO fake gutter, NO spine shadow, NO text, NO letters, NO readable book titles.

APPLY THIS BOOK'S STYLE (do not copy image 1's cream/beige walls or soft pastel look):
- Deep BURGUNDY walls throughout
- Fireplace with stockings on the FAR LEFT wall (add if missing from guide — still keep tree left, boy right)
- Rich oil-painting / painted gouache quality matching image 3 (S3 Eyes Met quality bar)
- Warm firelight + tree glow, polished wood floor with diagonal perspective lines
- Era-neutral classic film camera in foreground — NOT phone, NOT modern device, NO screen UI
- NO Santa visible (gone / out of frame)
- NO skylight, NO roof window
- Faces off the center fold

Image 1 = COMPOSITION LOCK (camera, tree, boy placement, depth, diagonals) — keep this staging.
Image 2 = Boy G0 character lock — match face/hair/pajamas exactly.
Image 3 = Quality / paint bar — rich oil-painting gift-book finish.

BOY G0 LOCK: oatmeal/taupe (warm beige) holly pajamas — NOT white, NOT bright cream; green holly \
leaves with red berries clearly visible; red trim on collar, cuffs, hems; red buttons; classic \
button-up set. Tousled light brown hair with golden highlights; large expressive brown eyes; rosy \
cheeks. Looking UP with surprise/urgency. Five fingers only per hand. Hands empty — not holding camera.
"""

NEG = (
    "text, letters, typography, watermark, signature, readable titles, ROLLS, skylight, "
    "roof window, glass ceiling, Santa, Santa Claus, red coat figure, second camera, "
    "holding camera, camera in hands, phone, smartphone, glowing screen, UI icons, "
    "beige walls, cream walls, pastel walls, fake gutter, spine shadow, six fingers, "
    "extra fingers, mutated hands"
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
    for p in list(UNIT.iterdir()):
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            if p.name.startswith("_tmp") or p.name in {
                "art.png",
                "art-left.png",
                "art-right.png",
            }:
                p.unlink(missing_ok=True)


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board  # type: ignore

    UNIT.mkdir(parents=True, exist_ok=True)
    if not COMP.is_file():
        raise SystemExit(f"missing composition ref: {COMP}")

    comp = fal_client.upload_file(str(COMP))
    boy = fal_client.upload_file(str(ROOT / "Media/approved/characters/boy-narrator-G0.png"))
    quality = fal_client.upload_file(str(ROOT / "Media/development/S03-eyes-met/v07/art.png"))
    print("refs uploaded")

    print("=== Qwen 2 Pro Edit v03 (comp lock v06) ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": [comp, boy, quality],
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

    wipe_pngs()
    tmp.unlink(missing_ok=True)
    art = UNIT / "art.png"
    final.save(art, optimize=True)
    final.crop((0, 0, 2625, 2625)).save(UNIT / "art-left.png", optimize=True)
    final.crop((2625, 0, 5250, 2625)).save(UNIT / "art-right.png", optimize=True)

    (UNIT / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v03

| Field | Value |
|-------|--------|
| **name** | S7 Proof — composition from v06 guide |
| **unit** | S07-proof |
| **book page** | Flow v2 p16\\|17 SPREAD |
| **version** | v03 |
| **date** | {DAY} |
| **model** | `{QWEN}` (v06) → SeedVR×2 → Lanczos **5250×2625** |
| **composition lock** | `Media/generated/mocks/S07-proof/v06/art.png` |
| **refs** | v06 comp · boy-narrator-G0 · S03-eyes-met/v07 quality |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **status** | working |

## Intent

Keep v06 staging (tree L · boy R look-up · camera foreground on floor · diagonal depth). Restyle: burgundy walls, fireplace+stockings far left, S3 v07 oil quality, Boy G0, no Santa, no skylight.
""",
        encoding="utf-8",
    )
    (UNIT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v03",
                "model": QWEN,
                "seed": seed,
                "fal_url": url,
                "composition_lock": "Media/generated/mocks/S07-proof/v06/art.png",
                "size": list(TARGET),
                "status": "working",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    board = INDEX / f"S07-proof-v03-spread-{DAY}.png"
    seamless_board(
        final,
        board,
        unit="S07-proof",
        version="v03",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · comp lock v06 · S3 v07 bar",
        subtitle="Tree L · boy R look-up · camera FG on floor · burgundy · no Santa",
    )
    print("BOARD", board)
    print("final", art, final.size)


if __name__ == "__main__":
    main()
