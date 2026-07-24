#!/usr/bin/env python3
"""Finish S6 full-res: save L from completed Banana job; run R; board 2625²."""
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
UNIT = ROOT / "Media/development/S06-cocoa"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
PAGE = 2625
DAY = "2026-07-22"
BANANA = "fal-ai/nano-banana-pro/edit"

L_RID = "019f8d9a-4691-7fc3-892c-6df929c8dfff"
L_URL = "https://v3b.fal.media/files/b/0aa35e78/K_6DS6K-h3_0tLc3uKFz5_x23W9xy0.png"
R_COMP = "https://v3b.fal.media/files/b/0aa35dfa/xlfRd02Tj--ibj7I6dEjb_rz6lRbr0.png"

# From prior upload this session
SANTA = "https://v3b.fal.media/files/b/0aa35e78/uXEarERYNM1vzDy3UiP-__santa-G0-v2.png"
STYLE = "https://v3b.fal.media/files/b/0aa35e78/HJbTKN721IV03KJPcVWy3_style-lock-v2.png"

R_PROMPT = """\
Children's picture-book IMAGE PAGE illustration, square 1:1, ART ONLY — no text, no letters.

PRESERVE the exact composition of image 1 (layout lock): Santa holding a steaming cocoa mug \
with marshmallows as the prop hero — firelight and Christmas-tree glow, warm living-room mood.

Image 2 = Santa character lock (open coat, cream striped shirt, brown suspenders over shirt, \
kind face — match wardrobe and likeness).
Image 3 = painted gouache / soft watercolor quality + palette bar (warm firelight, rich but soft).

Keep the same frame treatment: soft dissolve vignette to cream edges. Same gift-book quality. \
Fewer gifts than a gift-sea plate. Cocoa mug readable with steam + marshmallows.
Output a clean high-resolution square plate ready for print.
"""


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


def to_page(im: Image.Image) -> Image.Image:
    if im.size == (PAGE, PAGE):
        return im
    return im.resize((PAGE, PAGE), Image.Resampling.LANCZOS)


def save_plate(ver: str, side: str, url: str, rid: str, seed=None) -> Path:
    out_dir = UNIT / ver
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = download(url)
    page = to_page(raw)
    stem = f"art-{side}"
    raw.save(out_dir / f"{stem}-banana-2k.png")
    page_path = out_dir / f"{stem}.png"
    page.save(page_path, optimize=True)
    meta = {
        "version": ver,
        "side": side,
        "model": BANANA,
        "resolution_setting": "2K",
        "raw_size": list(raw.size),
        "page_size": list(page.size),
        "request_id": rid,
        "fal_url": url,
        "seed": seed,
        "upscale": f"Lanczos -> {PAGE}x{PAGE}",
    }
    (out_dir / f"meta-{side}.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )
    print("saved", page_path, page.size)
    return page_path


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import text_image_board  # type: ignore

    # L v03 from completed job
    save_plate("v03", "left", L_URL, L_RID)
    (UNIT / "v03" / "RECIPE.md").write_text(
        f"""# RECIPE — S06-cocoa / v03 LEFT

| Field | Value |
|-------|--------|
| **name** | S6 Cocoa L — faint village whisper (print res) |
| **unit** | S06-cocoa |
| **book page** | Flow v2 p14 TEXT |
| **version** | v03 (LEFT) |
| **date** | {DAY} |
| **model** | `{BANANA}` @ 2K → Lanczos **2625×2625** |
| **composition lock** | v02 L (village whisper + cream vignette) |
| **refs** | E-back-village-snow · frame-reference |
| **request_id** | `{L_RID}` |
| **fal_url** | `{L_URL}` |
| **raw → page** | 2048² → 2625² |
| **status** | working — full-res print plate |
| **paired_right** | v02 art-right |

## Intent

Same composition as v02 L: distant snowy village whisper + soft dissolve-to-cream vignette; open center for poem. Resolution lock: no low-res dials.
""",
        encoding="utf-8",
    )

    print("=== R v02 Banana Pro /edit @ 2K ===")
    result = fal_client.subscribe(
        BANANA,
        arguments={
            "prompt": R_PROMPT,
            "image_urls": [R_COMP, SANTA, STYLE],
            "num_images": 1,
            "output_format": "png",
            "resolution": "2K",
            "aspect_ratio": "1:1",
            "limit_generations": True,
            "safety_tolerance": "4",
            "seed": 916278999,
        },
        with_logs=True,
    )
    print(result)
    images = result.get("images") or []
    url = images[0]["url"]
    # request id may be in logs; fal_client.subscribe may not return rid — store url
    rid = result.get("request_id") or "see-fal-history"
    save_plate("v02", "right", url, rid, seed=result.get("seed"))
    (UNIT / "v02" / "RECIPE-right.md").write_text(
        f"""# RECIPE — S06-cocoa / v02 RIGHT

| Field | Value |
|-------|--------|
| **name** | S6 Cocoa R — cocoa prop hero (print res) |
| **unit** | S06-cocoa |
| **book page** | Flow v2 p15 IMAGE |
| **version** | v02 (RIGHT) |
| **date** | {DAY} |
| **model** | `{BANANA}` @ 2K → Lanczos **2625×2625** |
| **composition lock** | v01 R KEEP (cocoa mug hero) |
| **refs** | santa-G0-v2 · style-lock-v2 |
| **seed** | {result.get("seed")} |
| **request_id** | `{rid}` |
| **fal_url** | `{url}` |
| **raw → page** | 2048² → 2625² |
| **status** | working — full-res print plate |
| **paired_left** | v03 art-left |

## Intent

Same composition as v01 R: Santa holding steaming cocoa with marshmallows; firelight + tree glow; open-coat wardrobe; standard frame treatment. Resolution lock: no low-res dials.
""",
        encoding="utf-8",
    )

    left = Image.open(UNIT / "v03" / "art-left.png")
    right = Image.open(UNIT / "v02" / "art-right.png")
    INDEX.mkdir(parents=True, exist_ok=True)
    board_path = INDEX / f"S06-cocoa-L-v03-R-v02-fullres-{DAY}.png"
    text_image_board(
        left,
        right,
        board_path,
        unit="S06-cocoa",
        version="L v03 + R v02 FULL RES",
        day=DAY,
        tech="Banana Pro /edit · 2K→2625² · S3 v07 quality bar · resolution lock",
        subtitle="LEFT p14 village whisper · RIGHT p15 cocoa hero · 2625²",
    )
    print("BOARD", board_path)

    Image.open(UNIT / "v03" / "art-left.png").save(UNIT / "art-left.png")
    Image.open(UNIT / "v02" / "art-right.png").save(UNIT / "art-right.png")
    print("promoted unit art-left / art-right")
    print("L", left.size, "R", right.size)


if __name__ == "__main__":
    main()
