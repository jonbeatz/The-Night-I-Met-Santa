#!/usr/bin/env python3
"""S8 Gone v08 — FINAL candidate: v03 quality + v02-left swirl energy + S3 bar."""
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
V03 = UNIT / "v03" / "art.png"
V02L = UNIT / "v02" / "art-left.png"
S3 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
V08 = UNIT / "v08"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
PAGE = 2625
DAY = "2026-07-23"

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD 5250x2625 — FINAL plate.

IMAGE 1 = QUALITY + ROOM BASE (v03): Start from these quality parameters — richest color, \
sharpest detail, best overall look. Keep the warm golden atmosphere, fireplace with warm glow \
and stockings on the LEFT, moonlit window with Santa's sleigh silhouette crossing the moon on \
the RIGHT, Christmas tree with warm lights, burgundy walls. Deep color saturation, crisp detail, \
warm golden glow. NOT soft. NOT muted.

Rich oil-painting quality matching S3 v07 (image 3 reinforces this finish).

IMAGE 2 = SWIRL ENERGY (v02-left): Magical motion swirl — silvery-white thin elegant wisps, \
sweeping curve from the dark hallway through the open interior doorway trailing the running boy. \
Match as closely as possible; energy and drama matter more than pixel-perfect copy. Prefer \
silvery-white thin wisps over thick gold cloud or vortex.

SCENE:
- Boy running mid-stride through interior doorway, vintage film camera in both hands, oatmeal/taupe \
holly pajamas with green holly + red berries and red trim, expression of wonder and urgency, \
tousled light-brown hair, barefoot
- Patterned rug on the floor (wood showing at edges)
- Medium gift density — scattered under the tree AND near the fireplace (Santa was working there); \
not wall-to-wall warehouse
- Santa GONE from the room — only the sleigh silhouette in the window outside
- NO skylight, NO text, faces off the gutter
"""

NEG = (
    "text, letters, watermark, Santa inside the room, Santa Claus in interior, skylight, "
    "soft muted washed out, blurry soft focus, cream walls, blue striped pajamas, phone, "
    "gift warehouse, wall-to-wall presents, massive vortex, thick gold cloud swirl"
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

    for p in (V03, V02L, S3):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    urls = [
        fal_client.upload_file(str(V03)),
        fal_client.upload_file(str(V02L)),
        fal_client.upload_file(str(S3)),
    ]
    print("refs: v03 quality/room + v02-left swirl + S3 v07 bar")

    print("=== Qwen S8 Gone v08 FINAL ===")
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
            "enable_prompt_expansion": True,
        },
        with_logs=True,
    )
    print(result)
    url = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(url)
    print("qwen raw", raw.size)
    tmp = UNIT / "_tmp-v08-qwen.png"
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

    save_triplet(final, V08)

    (V08 / "RECIPE.md").write_text(
        f"""# RECIPE — S08-gone / v08

| Field | Value |
|-------|--------|
| **name** | S8 Gone — FINAL candidate (v03 quality + v02-left swirl energy) |
| **unit** | S08-gone |
| **book page** | Flow v2 p18\\|19 SPREAD |
| **version** | v08 |
| **date** | {DAY} |
| **status** | working — lock on Jon approval |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **quality base** | v03 + S3 v07 ("Rich oil-painting quality matching S3 v07") |
| **swirl** | v02/art-left.png (energy > perfect match) |

## Intent

v03 richness/sharpness. Silvery swirl energy from v02-left. Fireplace L · moon+sleigh R · rug · medium gifts · boy run. Lock on approval.
""",
        encoding="utf-8",
    )
    (V08 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v08",
                "status": "working",
                "lock_on_approval": True,
                "quality_base": "v03",
                "swirl_ref": "v02/art-left.png",
                "quality_bar": "S03-eyes-met/v07",
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
        INDEX / f"S08-gone-v08-spread-{DAY}.png",
        unit="S08-gone",
        version="v08",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · v03 quality · S3 v07 bar",
        subtitle="Rich saturated · swirl energy · fire+moon · lock on approval",
    )

    from PIL import ImageDraw, ImageFont

    def font(sz: int):
        for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
            if Path(p).is_file():
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()

    imgs = [
        (Image.open(V03).convert("RGB"), "v03 quality LOCK"),
        (Image.open(V02L).convert("RGB"), "v02-left swirl energy"),
        (final, "v08 FINAL candidate"),
    ]
    # v02L is square — letterbox to wide for compare
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
        "S8 Gone — v03 quality  |  v02-left swirl  |  v08 FINAL",
        fill=(35, 28, 22),
        font=f1,
    )
    d.text(
        (margin, 40),
        "Rich oil-painting quality matching S3 v07 · lock on Jon approval",
        fill=(100, 90, 75),
        font=f2,
    )
    y = margin + header
    for i, (im, label) in enumerate(imgs):
        x = margin + i * (w + gap)
        # fit into w x h
        fitted = Image.new("RGB", (w, h), (40, 30, 28))
        scale = min(w / im.width, h / im.height)
        nw, nh = int(im.width * scale), int(im.height * scale)
        resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
        fitted.paste(resized, ((w - nw) // 2, (h - nh) // 2))
        sheet.paste(fitted, (x, y))
        d.text((x, y + h + 8), label, fill=(50, 40, 35), font=f2)
    board = INDEX / f"S08-gone-v03-v02L-v08-{DAY}.png"
    sheet.save(board, "PNG")
    print("BOARD", board)
    print("V08", V08 / "art.png")


if __name__ == "__main__":
    main()
