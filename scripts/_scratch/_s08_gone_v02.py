#!/usr/bin/env python3
"""S8 Gone v02 — composition from styles2/09-beat09-santa-gone. Does NOT replace v01 primary."""
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
UNIT = ROOT / "Media/development/S08-gone"
V01 = UNIT / "v01"
V02 = UNIT / "v02"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
COMP = ROOT / "Images/styles2/09-beat09-santa-gone.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
PAGE = 2625
DAY = "2026-07-23"

PROMPT = """\
Wide seamless Christmas living-room storybook SPREAD 5250x2625 energy. PRESERVE the COMPOSITION \
AND MOTION ENERGY of image 1: boy RUNNING mid-stride through an open doorway, body leaning forward, \
pure childhood urgency — he flew out and was back in a flash; motion blur / magical speed swirls \
showing haste; dynamic diagonal from doorway into the room; RIGHT side Christmas tree with gifts; \
a WINDOW with snow falling outside (breaks static room layouts). NO fake gutter, NO spine shadow, \
NO text, NO letters.

APPLY THIS BOOK'S STYLE (do not copy image 1 cream walls or blue striped PJs):
- Deep BURGUNDY walls throughout
- Rich oil-painting / painted gouache quality matching image 3
- Interior wooden door into a DARK HALLWAY (not outdoors) — door open behind the running boy
- Vintage era-neutral classic film camera clutched in the boy's hands (NOT phone, NOT modern)
- NO Santa anywhere — he is gone; absence fills the room
- NO skylight

LEFT half (p18): Boy bursting through interior doorway mid-run, camera in hand, motion blur/urgency, \
expression of realization that Santa already left; open door shows dark hallway behind.

RIGHT half (p19): Christmas tree warm lights and ornaments, wrapped presents; empty space where Santa \
was; window with night snow outside. Distinct L/R jobs; faces off the gutter.

Image 1 = COMPOSITION + ENERGY LOCK (running pose, doorway, tree side, window, motion swirls).
Image 2 = Boy G0 character lock — match face/hair/pajamas exactly.
Image 3 = Quality bar — S3 Eyes Met rich oil-painting finish.

BOY G0 LOCK: oatmeal/taupe (warm beige) holly pajamas — NOT white, NOT blue stripes, NOT bright cream; \
green holly leaves with red berries clearly visible; red trim on collar, cuffs, hems; red buttons; \
classic button-up set. Tousled light brown hair with golden highlights; large expressive brown eyes; \
rosy cheeks. Five fingers only per hand.
"""

NEG = (
    "text, letters, typography, watermark, Santa, Santa Claus, blue striped pajamas, "
    "cream walls, beige walls, exterior door to outdoors, skylight, phone, smartphone, "
    "glowing screen, six fingers, fake gutter, spine shadow"
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


def ensure_v01_archive() -> None:
    """Park current primary as v01 without changing root art.png."""
    V01.mkdir(parents=True, exist_ok=True)
    for name in ("art.png", "art-left.png", "art-right.png", "RECIPE.md", "meta.json"):
        src = UNIT / name
        dest = V01 / name
        if src.is_file() and not dest.is_file():
            shutil.copy2(src, dest)
            print("archived", name, "→ v01/")


def save_triplet(final: Image.Image, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    final.save(folder / "art.png", optimize=True)
    final.crop((0, 0, PAGE, PAGE)).save(folder / "art-left.png", optimize=True)
    final.crop((PAGE, 0, TARGET[0], TARGET[1])).save(folder / "art-right.png", optimize=True)


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board  # type: ignore

    ensure_v01_archive()

    # Prefer S3 quality bar at development root if print-sized, else v07
    s3_root = ROOT / "Media/development/S03-eyes-met/art.png"
    s3_v07 = ROOT / "Media/development/S03-eyes-met/v07/art.png"
    quality_path = s3_root if s3_root.is_file() else s3_v07

    comp = fal_client.upload_file(str(COMP))
    boy = fal_client.upload_file(str(ROOT / "Media/approved/characters/boy-narrator-G0.png"))
    quality = fal_client.upload_file(str(quality_path))
    print("refs uploaded", quality_path.name)

    print("=== Qwen S8 Gone v02 ===")
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
    tmp = UNIT / "_tmp-v02-qwen.png"
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

    save_triplet(final, V02)
    # Do NOT overwrite UNIT/art.png — v01 stays primary

    (V02 / "RECIPE.md").write_text(
        f"""# RECIPE — S08-gone / v02

| Field | Value |
|-------|--------|
| **name** | S8 Gone — running back (comp lock beat09) |
| **unit** | S08-gone |
| **book page** | Flow v2 p18\\|19 SPREAD |
| **version** | v02 |
| **date** | {DAY} |
| **status** | working — pending Jon vs v01 primary |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **composition** | `Images/styles2/09-beat09-santa-gone.png` |
| **refs** | boy-narrator-G0 · S3 quality bar |
| **primary** | **v01 remains** `Media/development/S08-gone/art.png` until Jon promotes v02 |

## Intent

Boy mid-run through interior doorway with camera; motion energy; burgundy walls; tree + gifts R; snow window; Santa gone.
""",
        encoding="utf-8",
    )
    (V02 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v02",
                "status": "working",
                "replaces_primary": False,
                "seed": seed,
                "fal_url": url,
                "composition": "Images/styles2/09-beat09-santa-gone.png",
                "size": list(TARGET),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    INDEX.mkdir(parents=True, exist_ok=True)
    board = INDEX / f"S08-gone-v01-vs-v02-{DAY}.png"
    # Compare primary v01 vs new v02
    v01_art = Image.open(UNIT / "art.png").convert("RGB")
    seamless_board(
        final,
        INDEX / f"S08-gone-v02-spread-{DAY}.png",
        unit="S08-gone",
        version="v02",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · comp lock beat09 · S3 bar",
        subtitle="Running doorway · motion · snow window · Santa gone · v01 still primary",
    )
    # Side-by-side compare board
    from PIL import ImageDraw, ImageFont

    def font(sz: int):
        for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
            if Path(p).is_file():
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()

    w, h = 1400, 700
    a = v01_art.resize((w, h), Image.Resampling.LANCZOS)
    b = final.resize((w, h), Image.Resampling.LANCZOS)
    margin, gap, header = 28, 24, 72
    sheet = Image.new(
        "RGB", (margin * 2 + w * 2 + gap, margin + header + h + 40), (252, 248, 240)
    )
    d = ImageDraw.Draw(sheet)
    f1, f2 = font(20), font(14)
    d.text((margin, 14), "S8 Gone — v01 PRIMARY  |  v02 running-comp ALT", fill=(35, 28, 22), font=f1)
    d.text(
        (margin, 42),
        "v01 stays art.png until Jon promotes · v02 from beat09 energy guide",
        fill=(100, 90, 75),
        font=f2,
    )
    y = margin + header
    sheet.paste(a, (margin, y))
    sheet.paste(b, (margin + w + gap, y))
    d.text((margin, y + h + 8), "v01 — current primary", fill=(50, 40, 35), font=f2)
    d.text((margin + w + gap, y + h + 8), "v02 — doorway run + snow window", fill=(50, 40, 35), font=f2)
    sheet.save(board, "PNG")
    print("BOARD", board)
    print("V02", V02 / "art.png")
    print("PRIMARY still", UNIT / "art.png")


if __name__ == "__main__":
    main()
