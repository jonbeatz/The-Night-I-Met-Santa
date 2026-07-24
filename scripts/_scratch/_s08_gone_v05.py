#!/usr/bin/env python3
"""S8 Gone v05 — FINAL: exact v02 swirl + v03 room + rug + medium gifts."""
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
V05 = UNIT / "v05"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
PAGE = 2625
DAY = "2026-07-23"

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD 5250x2625 — FINAL plate.

CRITICAL SWIRL LOCK — IMAGE 1 (full v02) + IMAGE 2 (v02 left close detail):
Copy the MAGICAL MOTION SWIRL from these references EXACTLY — same style, same scale, same \
intensity, same drama. It must be the SUBTLE ELEGANT wispy translucent white/gold trail: thin \
painterly lines, light and airy, graceful spiral curving from the open doorway around the boy's \
waist and trailing leg — like wind/magic speed. NOT a massive white cyclone. NOT a huge circular \
storm vortex filling half the room. NOT the thick glowing blob from failed denser plates. Match \
image 1 / image 2 swirl LANGUAGE and SIZE precisely. The swirl originates from the dark hallway \
through the open interior door.

Also preserve from image 1: boy mid-stride RUNNING pose, forward lean, vintage film camera in both \
hands, Boy G0 oatmeal/taupe holly pajamas (green holly + red berries, red trim), tousled hair, \
burgundy walls, wooden floor with a WARM PATTERNED RUG back on the floor (wood showing around the \
edges — rug anchors the room like image 1).

IMAGE 3 = ROOM RICHNESS (v03) — take atmosphere only, not gift warehouse density:
- LEFT: fireplace with warm golden-orange firelight + stockings on mantel (garland OK)
- RIGHT: moonlit window, falling snow, soft moonlight, subtle Santa sleigh silhouette crossing \
the full moon OUTSIDE (tiny — NOT Santa in the room)
- Warm Christmas tree with lights, ornaments, glowing star

GIFTS — MEDIUM density (more than sparse, less than warehouse):
Most gifts concentrated under the tree. A few scattered across the rug naturally. IMPORTANT: \
several wrapped gifts near the fireplace (Santa was working there). Red/green/gold/blue wrapping \
with ribbons. Not wall-to-wall. Boy + swirl remain the focal points.

KEEP: interior door to dark hallway, NO Santa inside, NO skylight, NO text. Rich oil-painting \
quality. Faces off the gutter. Seamless burgundy room.
"""

NEG = (
    "text, letters, typography, watermark, Santa inside the room, skylight, cream walls, "
    "beige walls, blue striped pajamas, phone, smartphone, six fingers, fake gutter, "
    "spine shadow, gift warehouse, floor buried in presents, wall-to-wall gifts, "
    "massive vortex, giant cyclone swirl, huge circular storm swirl, thick white tornado, "
    "swirl filling half the room, oversized motion blur cloud, chaotic storm energy"
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


def crop_swirl_ref() -> Path:
    """Tight crop of v02 left swirl zone as extra visual lock."""
    im = Image.open(V02).convert("RGB")
    # Left ~45% of spread where door+boy+swirl live
    w, h = im.size
    crop = im.crop((0, int(h * 0.05), int(w * 0.48), int(h * 0.95)))
    out = UNIT / "_tmp-v02-swirl-crop.png"
    crop.save(out)
    return out


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board  # type: ignore

    for p in (V02, V02L, V03):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # Max 3 refs on Qwen: full v02 (swirl) + left detail + v03 room
    urls = [
        fal_client.upload_file(str(V02)),
        fal_client.upload_file(str(V02L)),
        fal_client.upload_file(str(V03)),
    ]
    print("refs: v02 + v02L + v03 (max 3)")

    print("=== Qwen S8 Gone v05 FINAL ===")
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
    tmp = UNIT / "_tmp-v05-qwen.png"
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

    save_triplet(final, V05)

    (V05 / "RECIPE.md").write_text(
        f"""# RECIPE — S08-gone / v05

| Field | Value |
|-------|--------|
| **name** | S8 Gone — FINAL (exact v02 swirl + v03 room + rug + medium gifts) |
| **unit** | S08-gone |
| **book page** | Flow v2 p18\\|19 SPREAD |
| **version** | v05 |
| **date** | {DAY} |
| **status** | working — lock candidate pending Jon |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **swirl lock** | v02 art.png + art-left.png + swirl crop |
| **room guide** | v03 fire/moon/sleigh |

## Intent

Elegant v02 wispy swirl (NOT v04 vortex). Fireplace + moon sleigh. Patterned rug. Medium gifts (tree + near fireplace).
""",
        encoding="utf-8",
    )
    (V05 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v05",
                "status": "working",
                "lock_candidate": True,
                "swirl_lock": "v02",
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
        INDEX / f"S08-gone-v05-spread-{DAY}.png",
        unit="S08-gone",
        version="v05",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · FINAL · exact v02 swirl",
        subtitle="Elegant swirl · fire+moon · rug · medium gifts near fireplace",
    )

    from PIL import ImageDraw, ImageFont

    def font(sz: int):
        for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
            if Path(p).is_file():
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()

    imgs = [
        (Image.open(V02).convert("RGB"), "v02 swirl LOCK"),
        (Image.open(UNIT / "v04" / "art.png").convert("RGB"), "v04 vortex (reject)"),
        (final, "v05 FINAL candidate"),
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
        "S8 Gone — v02 swirl lock  |  v04 vortex reject  |  v05 FINAL",
        fill=(35, 28, 22),
        font=f1,
    )
    d.text(
        (margin, 40),
        "Must match v02 elegant wispy swirl scale — not massive vortex",
        fill=(100, 90, 75),
        font=f2,
    )
    y = margin + header
    for i, (im, label) in enumerate(imgs):
        x = margin + i * (w + gap)
        sheet.paste(im.resize((w, h), Image.Resampling.LANCZOS), (x, y))
        d.text((x, y + h + 8), label, fill=(50, 40, 35), font=f2)
    board = INDEX / f"S08-gone-v02-v04-v05-{DAY}.png"
    sheet.save(board, "PNG")
    print("BOARD", board)
    print("V05", V05 / "art.png")


if __name__ == "__main__":
    main()
