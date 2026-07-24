#!/usr/bin/env python3
"""S7 Proof v06 — clean burgundy wall smudge on locked v03. KEEP art.png untouched."""
from __future__ import annotations

import io
import json
import os
import sys
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
KEEP = ROOT / "Media/development/S07-proof/_LOCKED-v03/art.png"
OUT = ROOT / "Media/development/S07-proof/v06-clean-wall"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
TARGET = (5250, 2625)
PAGE = 2625
DAY = "2026-07-23"

PROMPT = """\
Edit image 1 ONLY. PRESERVE the exact composition, characters, camera, tree, fireplace, \
gifts, furniture, lighting, and burgundy walls everywhere.

ONE FIX: On the burgundy wall BETWEEN the Christmas tree and the boy (above the green sofa / \
middle-right wall), remove any faint pale smudge, ghost face, face-like blob, or weird light \
patch that looks like a face or figure. Repaint that area as clean continuous deep burgundy \
wall texture matching the surrounding wall paint — soft oil-painting grain, same color and value \
as the clean wall nearby. NO face, NO beard, NO Santa suggestion, NO pale oval, NO figure.

Do not change the boy, camera, tree, fireplace, gifts, sofa, bookshelf, or floor. No new objects. \
No text. Same cinematic spread framing.
"""

NEG = (
    "Santa, face on wall, ghost, apparition, beard on wall, pale oval, portrait on wall, "
    "text, letters, watermark, different composition, moved boy, second camera"
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


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def board(before: Image.Image, after: Image.Image, path: Path) -> None:
    w, h = 1400, 700
    a = before.resize((w, h), Image.Resampling.LANCZOS)
    b = after.resize((w, h), Image.Resampling.LANCZOS)
    margin, gap, header = 28, 24, 72
    sheet = Image.new("RGB", (margin * 2 + w * 2 + gap, margin + header + h + 40), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    try:
        f1, f2 = font(20), font(14)
    except Exception:
        f1 = f2 = ImageFont.load_default()
    d.text((margin, 14), "S7 Proof — KEEP v03  |  v06 clean-wall ALT", fill=(35, 28, 22), font=f1)
    d.text((margin, 42), "Qwen wall-only fix · KEEP untouched · remove face-like smudge on burgundy wall", fill=(100, 90, 75), font=f2)
    y = margin + header
    sheet.paste(a, (margin, y))
    sheet.paste(b, (margin + w + gap, y))
    d.text((margin, y + h + 8), "v03 KEEP (source)", fill=(50, 40, 35), font=f2)
    d.text((margin + w + gap, y + h + 8), "v06-clean-wall (preview ALT)", fill=(50, 40, 35), font=f2)
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, "PNG")


def main() -> None:
    load_env()
    keep = Image.open(KEEP).convert("RGB")
    if keep.size != TARGET:
        keep = keep.resize(TARGET, Image.Resampling.LANCZOS)

    # Work at Qwen-friendly size then upscale back
    work = keep.resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_in = OUT.parent / "_tmp-s07-clean-in.png"
    OUT.mkdir(parents=True, exist_ok=True)
    work.save(tmp_in)

    url_in = fal_client.upload_file(str(tmp_in))
    print("=== Qwen clean-wall edit ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": [url_in],
            "image_size": {"width": 2048, "height": 1024},
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checker": True,
            "enable_prompt_expansion": False,
        },
        with_logs=True,
    )
    print(result)
    fal_url = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(fal_url)
    tmp_in.unlink(missing_ok=True)

    tmp_raw = OUT.parent / "_tmp-s07-clean-raw.png"
    raw.save(tmp_raw)
    print("=== SeedVR ===")
    up_url = fal_client.upload_file(str(tmp_raw))
    up = fal_client.subscribe(
        SEEDVR,
        arguments={
            "image_url": up_url,
            "upscale_mode": "factor",
            "upscale_factor": 2,
            "noise_scale": 0.08,
            "output_format": "png",
        },
        with_logs=True,
    )
    up_im = download(up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"])
    final = up_im.resize(TARGET, Image.Resampling.LANCZOS)
    tmp_raw.unlink(missing_ok=True)

    final.save(OUT / "art.png", optimize=True)
    final.crop((0, 0, PAGE, PAGE)).save(OUT / "art-left.png", optimize=True)
    final.crop((PAGE, 0, TARGET[0], TARGET[1])).save(OUT / "art-right.png", optimize=True)

    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v06-clean-wall (ALT)

| Field | Value |
|-------|--------|
| **status** | **ALT** — clean wall pass · does **not** replace v03 KEEP |
| **base** | `_LOCKED-v03/art.png` |
| **model** | `{QWEN}` → SeedVR×2 → 5250×2625 |
| **seed** | {seed} |
| **fal_url** | `{fal_url}` |
| **date** | {DAY} |
| **fix** | Remove face-like pale smudge on burgundy wall between tree and boy |

KEEP remains: `Media/development/S07-proof/art.png` (= `_LOCKED-v03`).
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v06-clean-wall",
                "status": "preview_alt",
                "replaces_keep": False,
                "seed": seed,
                "fal_url": fal_url,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    board_path = INDEX / f"S07-proof-v03-KEEP-vs-v06-clean-wall-{DAY}.png"
    board(keep, final, board_path)
    print("ALT", OUT / "art.png")
    print("BOARD", board_path)
    print("KEEP untouched", KEEP)


if __name__ == "__main__":
    main()
