#!/usr/bin/env python3
"""S8 Gone v04 — FINAL candidate: v02 swirl/run + v03 fire/moon, gifts halved."""
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
V02L = UNIT / "v02" / "art-left.png"
V03 = UNIT / "v03" / "art.png"
V04 = UNIT / "v04"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
PAGE = 2625
DAY = "2026-07-23"

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD 5250x2625 — FINAL plate.

IMAGE 1 = ENERGY LOCK (full spread v02). Preserve EXACTLY the boy's mid-stride RUNNING pose, \
forward lean, childhood urgency, vintage film camera clutched in both hands, and especially the \
DRAMATIC MAGICAL MOTION SWIRL — same intensity, same white/gold luminous vortex drama trailing \
from the open doorway behind him. That swirl and run are the focal point. Do not weaken, thin, \
or quiet the swirl.

IMAGE 2 = CLOSE-UP ENERGY DETAIL (v02 left): reinforce the swirl thickness, luminous edges, and \
boy's pose/pajamas/camera.

IMAGE 3 = ROOM RICHNESS GUIDE (v03): take ONLY the warm atmosphere upgrades —
- LEFT: fireplace with warm golden-orange firelight wash + stockings on the mantel (garland OK)
- RIGHT: moonlit window with falling snow, soft cool moonlight mixing with tree lights, subtle \
Santa's sleigh silhouette crossing the full moon OUTSIDE (tiny, magical — NOT Santa in the room)
- Christmas tree warm lights, ornaments, glowing star
Do NOT copy v03's dense gift warehouse floor.

GIFT FIX (critical): REDUCE presents to about HALF of image 3. Concentrate most wrapped gifts \
UNDER THE TREE. Only a few gifts scattered naturally across the floor — Christmas morning, NOT \
a gift warehouse. Boy + swirl must read as the heroes; presents are supporting atmosphere only. \
Red/green/gold/blue wrapping with ribbons, varied sizes, restrained count.

KEEP: deep burgundy walls throughout, wooden floor, interior wooden door open to DARK HALLWAY \
(not outdoors), Boy G0 oatmeal/taupe holly pajamas with green holly + red berries and red trim, \
tousled light-brown hair, NO Santa inside, NO skylight, NO text. Rich oil-painting quality. \
Faces off the gutter. Seamless room across the spread.
"""

NEG = (
    "text, letters, typography, watermark, Santa inside the room, skylight, cream walls, "
    "beige walls, blue striped pajamas, phone, smartphone, six fingers, fake gutter, "
    "spine shadow, gift warehouse, floor buried in presents, excessive gifts, dense gift sea "
    "covering whole floor, weak thin swirl, missing motion blur, quiet swirl"
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

    for p in (V02, V02L, V03):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    u1 = fal_client.upload_file(str(V02))
    u2 = fal_client.upload_file(str(V02L))
    u3 = fal_client.upload_file(str(V03))
    print("refs: v02 spread + v02 left swirl + v03 richness")

    print("=== Qwen S8 Gone v04 FINAL ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": [u1, u2, u3],
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
    tmp = UNIT / "_tmp-v04-qwen.png"
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

    save_triplet(final, V04)

    (V04 / "RECIPE.md").write_text(
        f"""# RECIPE — S08-gone / v04

| Field | Value |
|-------|--------|
| **name** | S8 Gone — FINAL candidate (v02 swirl + v03 fire/moon, gifts halved) |
| **unit** | S08-gone |
| **book page** | Flow v2 p18\\|19 SPREAD |
| **version** | v04 |
| **date** | {DAY} |
| **status** | working — lock candidate pending Jon |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **energy lock** | v02 art.png + art-left.png (swirl intensity) |
| **room guide** | v03 (fire + moon + sleigh; gifts reduced) |

## Intent

Dramatic v02 swirl/run as hero. v03 fireplace L + moonlit sleigh window R. Gifts ~half, mostly under tree.
""",
        encoding="utf-8",
    )
    (V04 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v04",
                "status": "working",
                "lock_candidate": True,
                "energy_lock": "v02",
                "room_guide": "v03",
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
        INDEX / f"S08-gone-v04-spread-{DAY}.png",
        unit="S08-gone",
        version="v04",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · FINAL candidate",
        subtitle="v02 swirl LOCK · v03 fire+moon · gifts halved under tree",
    )

    from PIL import ImageDraw, ImageFont

    def font(sz: int):
        for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
            if Path(p).is_file():
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()

    # Triple compare: v02 | v03 | v04
    imgs = [
        (Image.open(V02).convert("RGB"), "v02 swirl lock"),
        (Image.open(V03).convert("RGB"), "v03 rich (warehouse)"),
        (final, "v04 FINAL candidate"),
    ]
    w, h = 900, 450
    margin, gap, header = 24, 16, 68
    sheet = Image.new(
        "RGB",
        (margin * 2 + w * 3 + gap * 2, margin + header + h + 36),
        (252, 248, 240),
    )
    d = ImageDraw.Draw(sheet)
    f1, f2 = font(18), font(12)
    d.text(
        (margin, 12),
        "S8 Gone — v02 energy  |  v03 richness  |  v04 FINAL (swirl + fire/moon, gifts half)",
        fill=(35, 28, 22),
        font=f1,
    )
    d.text(
        (margin, 40),
        "Lock if Jon OKs · primary unchanged until promote",
        fill=(100, 90, 75),
        font=f2,
    )
    y = margin + header
    for i, (im, label) in enumerate(imgs):
        x = margin + i * (w + gap)
        sheet.paste(im.resize((w, h), Image.Resampling.LANCZOS), (x, y))
        d.text((x, y + h + 8), label, fill=(50, 40, 35), font=f2)
    board = INDEX / f"S08-gone-v02-v03-v04-{DAY}.png"
    sheet.save(board, "PNG")
    print("BOARD", board)
    print("V04", V04 / "art.png")


if __name__ == "__main__":
    main()
