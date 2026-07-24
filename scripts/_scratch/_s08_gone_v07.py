#!/usr/bin/env python3
"""S8 Gone v07 — v05 composition; ONLY v02-left as swirl ref. Lock if match."""
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
V02L = UNIT / "v02" / "art-left.png"
V05 = UNIT / "v05" / "art.png"
V07 = UNIT / "v07"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
PAGE = 2625
DAY = "2026-07-23"

PROMPT = """\
Generate S8 Gone using the v05 composition (image 1) but replace the swirl with v02's EXACT swirl \
from image 2 — silvery-white, thin elegant wisps, same curve, same intensity, same transparency. \
No gold tones. No mist. No cloud. Match v02-left precisely.

Keep everything else from image 1 (v05): rug, fireplace glow with stockings, moonlit window with \
Santa sleigh silhouette, gift density, boy running pose with vintage camera, holly pajamas, \
Christmas tree, burgundy walls, interior door to dark hallway. Wide seamless spread 5250x2625. \
NO text. NO Santa inside the room. NO skylight. Rich oil-painting quality. Faces off the gutter.
"""

NEG = (
    "text, letters, watermark, Santa inside, skylight, gold swirl, golden trail, yellow motion "
    "blur, warm orange swirl, mist cloud, thick fog trail, heavy smoke swirl, vortex, cyclone, "
    "solid glowing blob, opaque swirl"
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


def promote_lock(src: Path) -> None:
    locked = UNIT / "_LOCKED-v07"
    locked.mkdir(parents=True, exist_ok=True)
    for name in ("art.png", "art-left.png", "art-right.png", "RECIPE.md", "meta.json"):
        s = src / name
        if s.is_file():
            shutil.copy2(s, UNIT / name)
            shutil.copy2(s, locked / name)
    print("PROMOTED v07 → primary + _LOCKED-v07/")


def update_flow_keep() -> None:
    import re

    text = FLOW.read_text(encoding="utf-8")
    text2, n = re.subn(
        r'("page": "18\|19",\s*"beat": "S8 Gone",\s*"version": ")[^"]+(",\s*"model": "[^"]+",\s*"status": ")[^"]+(",\s*"decided_by": "Jon",\s*"date": "[^"]+",\s*"notes": ")[^"]*(")',
        r'\1v07\2keep\3LOCKED v07 · silvery v02-left swirl on v05 room · Media/development/S08-gone/_LOCKED-v07/ · board S08-gone-v02L-vs-v07-'
        + DAY
        + r'.png\4',
        text,
        count=1,
    )
    text2 = text2.replace(
        '"caption": "p18 · S8 Gone L · v01 boy+camera"',
        '"caption": "p18 · S8 Gone L · v07 LOCK"',
    )
    text2 = text2.replace(
        '"caption": "p19 · S8 Gone R · v01 empty room"',
        '"caption": "p19 · S8 Gone R · v07 LOCK"',
    )
    text2 = text2.replace(
        '"caption": "p18 · S8 Gone L · v06 LOCK"',
        '"caption": "p18 · S8 Gone L · v07 LOCK"',
    )
    text2 = text2.replace(
        '"caption": "p19 · S8 Gone R · v06 LOCK"',
        '"caption": "p19 · S8 Gone R · v07 LOCK"',
    )
    text2 = re.sub(r'("id": "p18",[\s\S]*?"version": ")v\d+(")', r"\1v07\2", text2, count=1)
    text2 = re.sub(r'("id": "p19",[\s\S]*?"version": ")v\d+(")', r"\1v07\2", text2, count=1)
    text2 = re.sub(r'("id": "p18",[\s\S]*?"status": ")(?:working|keep)(")', r"\1keep\2", text2, count=1)
    text2 = re.sub(r'("id": "p19",[\s\S]*?"status": ")(?:working|keep)(")', r"\1keep\2", text2, count=1)
    FLOW.write_text(text2, encoding="utf-8")
    print("FLOW keep patch n=", n)


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board  # type: ignore

    for p in (V05, V02L):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    # ONLY two refs: v05 composition + v02-left swirl (no full v02)
    urls = [
        fal_client.upload_file(str(V05)),
        fal_client.upload_file(str(V02L)),
    ]
    print("refs: v05 composition + v02-left ONLY (swirl)")

    print("=== Qwen S8 Gone v07 ===")
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
            "enable_prompt_expansion": False,  # keep prompt tight
        },
        with_logs=True,
    )
    print(result)
    url = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(url)
    print("qwen raw", raw.size)
    tmp = UNIT / "_tmp-v07-qwen.png"
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

    save_triplet(final, V07)

    (V07 / "RECIPE.md").write_text(
        f"""# RECIPE — S08-gone / v07

| Field | Value |
|-------|--------|
| **name** | S8 Gone — FINAL (v05 room + exact silvery v02-left swirl) |
| **unit** | S08-gone |
| **book page** | Flow v2 p18\\|19 SPREAD |
| **version** | v07 |
| **date** | {DAY} |
| **status** | lock-if-swirl-matches |
| **model** | `{QWEN}` (v06) → SeedVR×2 → **5250×2625** |
| **seed** | {seed} |
| **fal_url** | `{url}` |
| **composition** | v05 |
| **swirl ref ONLY** | v02/art-left.png |

## Intent

Replace v05 swirl with silvery-white thin elegant wisps from v02-left. No gold. No mist. No cloud.
""",
        encoding="utf-8",
    )
    (V07 / "meta.json").write_text(
        json.dumps(
            {
                "version": "v07",
                "status": "lock_candidate",
                "composition": "v05",
                "swirl_ref_only": "v02/art-left.png",
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
        INDEX / f"S08-gone-v07-spread-{DAY}.png",
        unit="S08-gone",
        version="v07",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · v05 + v02-left swirl ONLY",
        subtitle="Silvery thin wisps · no gold · no mist",
    )

    from PIL import ImageDraw, ImageFont

    def font(sz: int):
        for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
            if Path(p).is_file():
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()

    ref = Image.open(V02L).convert("RGB")
    left = final.crop((0, 0, PAGE, PAGE))
    w, h = 900, 900
    a = ref.resize((w, h), Image.Resampling.LANCZOS)
    b = left.resize((w, h), Image.Resampling.LANCZOS)
    margin, gap, header = 24, 20, 70
    sheet = Image.new(
        "RGB", (margin * 2 + w * 2 + gap, margin + header + h + 40), (252, 248, 240)
    )
    d = ImageDraw.Draw(sheet)
    f1, f2 = font(18), font(13)
    d.text((margin, 14), "S8 Gone SWIRL — v02-left LOCK  |  v07 left", fill=(35, 28, 22), font=f1)
    d.text(
        (margin, 42),
        "Must be silvery-white thin wisps — no gold, no mist, no cloud",
        fill=(100, 90, 75),
        font=f2,
    )
    y = margin + header
    sheet.paste(a, (margin, y))
    sheet.paste(b, (margin + w + gap, y))
    d.text((margin, y + h + 8), "v02 art-left — swirl LOCK", fill=(50, 40, 35), font=f2)
    d.text((margin + w + gap, y + h + 8), "v07 left — candidate", fill=(50, 40, 35), font=f2)
    board = INDEX / f"S08-gone-v02L-vs-v07-{DAY}.png"
    sheet.save(board, "PNG")
    print("BOARD", board)
    print("V07", V07 / "art.png")


if __name__ == "__main__":
    main()
