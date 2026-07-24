#!/usr/bin/env python3
"""S8 Gone v03 — enrich locked v02 energy with gift sea, fireplace glow, moonlight."""
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
V02 = UNIT / "v02" / "art.png"
V03 = UNIT / "v03"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
S03 = ROOT / "Media/development/S03-eyes-met/art.png"
S05 = ROOT / "Media/development/S05-chat/art.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
PAGE = 2625
DAY = "2026-07-23"

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD 5250x2625. Image 1 is the LOCKED COMPOSITION \
AND ENERGY — preserve EXACTLY: boy RUNNING mid-stride through open interior doorway (dark hallway \
behind), vintage film camera clutched in both hands, magical white/gold motion swirl trailing from \
the doorway, forward lean and childhood urgency, Christmas tree on the RIGHT with warm lights and \
star, window with falling snow on the far right, deep BURGUNDY walls throughout, wooden floor, \
NO Santa in the room, NO skylight, NO text. Do not move the boy, do not change his pose, do not \
remove the swirl, do not change the tree placement or window placement.

ENRICH richness only — Christmas exploded in this room:

1) GIFT SEA density matching images 2 and 3: MANY wrapped presents scattered across the WHOLE floor \
— all sizes (tiny to large), red/green/gold/blue wrapping papers, ribbons and bows. Not only under \
the tree — gifts strewn left-to-right across the room floor around the boy's path (leave clear \
running path so he still reads), under the tree, and toward the window. Matching S3/S5 gift-sea \
abundance.

2) FIREPLACE GLOW from the LEFT: warm golden-orange firelight washing that side of the room even \
if the fireplace is partially off-frame or just at the left edge. Soft stockings on the mantel if \
the mantel peeks in. Warm amber bounce on floorboards and burgundy wall on the left.

3) WINDOW moonlight on the RIGHT: soft cool moonlight spilling through the snowy window, mixing \
with warm tree lights. Optional subtle silhouette of Santa's sleigh crossing the moon OUTSIDE the \
window — tiny, distant, quiet detail only (NOT Santa inside the room).

Keep Boy G0: oatmeal/taupe holly pajamas with green holly + red berries, red trim/collar/cuffs, \
tousled light-brown hair, vintage camera. Rich oil-painting quality. Faces off the gutter. \
Seamless burgundy room connecting both pages.
"""

NEG = (
    "text, letters, typography, watermark, Santa inside the room, Santa Claus in interior, "
    "skylight, cream walls, beige walls, blue striped pajamas, phone, smartphone, "
    "six fingers, fake gutter, spine shadow, empty bare floor, sparse gifts only under tree"
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


def save_triplet(final: Image.Image, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    final.save(folder / "art.png", optimize=True)
    final.crop((0, 0, PAGE, PAGE)).save(folder / "art-left.png", optimize=True)
    final.crop((PAGE, 0, TARGET[0], TARGET[1])).save(folder / "art-right.png", optimize=True)


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board  # type: ignore

    if not V02.is_file():
        raise SystemExit(f"missing lock: {V02}")

    # Prefer print-size S05; fall back to left panel if only halves exist
    gift_ref = S05 if S05.is_file() else (ROOT / "Media/development/S05-chat/art-left.png")
    if not S03.is_file():
        raise SystemExit(f"missing S03: {S03}")
    if not gift_ref.is_file():
        raise SystemExit(f"missing gift density ref: {gift_ref}")

    lock = fal_client.upload_file(str(V02))
    s3 = fal_client.upload_file(str(S03))
    s5 = fal_client.upload_file(str(gift_ref))
    print("refs uploaded: v02 lock + S03 +", gift_ref.name)

    print("=== Qwen S8 Gone v03 ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": [lock, s3, s5],
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
    tmp = UNIT / "_tmp-v03-qwen.png"
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

    save_triplet(final, V03)
    # Do NOT overwrite primary art.png

    (V03 / "RECIPE.md").write_text(
        f"""# RECIPE — S08-gone / v03

| Field | Value |
|-------|--------|
| **name** | S8 Gone — richer gift sea + fire + moonlight |
| **unit** | S08-gone |
| **book page** | Flow v2 p18\\|19 SPREAD |
| **version** | v03 |
| **date** | {DAY} |
| **status** | working — energy locked from v02 |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **composition lock** | `Media/development/S08-gone/v02/art.png` |
| **density refs** | S03-eyes-met · S05-chat |
| **primary** | still v01 at `Media/development/S08-gone/art.png` until Jon promotes |

## Intent

Keep v02 run + swirl + tree + snow window. Add gift-sea density, left fireplace glow, right moonlight (+ subtle sleigh silhouette if present).
""",
        encoding="utf-8",
    )
    (V03 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v03",
                "status": "working",
                "replaces_primary": False,
                "energy_lock": "v02",
                "seed": seed,
                "fal_url": url,
                "size": list(TARGET),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    seamless_board(
        final,
        INDEX / f"S08-gone-v03-spread-{DAY}.png",
        unit="S08-gone",
        version="v03",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · v02 energy lock · gift sea + fire + moon",
        subtitle="Richer Christmas · presents everywhere · fireplace glow L · moonlight R",
    )

    # v02 vs v03 compare
    from PIL import ImageDraw, ImageFont

    def font(sz: int):
        for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
            if Path(p).is_file():
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()

    v02_im = Image.open(V02).convert("RGB")
    w, h = 1400, 700
    a = v02_im.resize((w, h), Image.Resampling.LANCZOS)
    b = final.resize((w, h), Image.Resampling.LANCZOS)
    margin, gap, header = 28, 24, 72
    sheet = Image.new(
        "RGB", (margin * 2 + w * 2 + gap, margin + header + h + 40), (252, 248, 240)
    )
    d = ImageDraw.Draw(sheet)
    f1, f2 = font(20), font(14)
    d.text((margin, 14), "S8 Gone — v02 ENERGY LOCK  |  v03 richer Christmas", fill=(35, 28, 22), font=f1)
    d.text(
        (margin, 42),
        "Same run/swirl · gift sea + fireplace glow L · moonlight (+ sleigh?) R",
        fill=(100, 90, 75),
        font=f2,
    )
    y = margin + header
    sheet.paste(a, (margin, y))
    sheet.paste(b, (margin + w + gap, y))
    d.text((margin, y + h + 8), "v02 — locked energy", fill=(50, 40, 35), font=f2)
    d.text((margin + w + gap, y + h + 8), "v03 — gifts / fire / moon", fill=(50, 40, 35), font=f2)
    board = INDEX / f"S08-gone-v02-vs-v03-{DAY}.png"
    sheet.save(board, "PNG")
    print("BOARD", board)
    print("V03", V03 / "art.png")


if __name__ == "__main__":
    main()
