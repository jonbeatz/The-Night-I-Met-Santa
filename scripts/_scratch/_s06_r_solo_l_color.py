#!/usr/bin/env python3
"""S6 Cocoa: R v03 Santa-solo KEEP @ 2625 + L v04 richer village color @ 2625."""
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

# Composition locks
R_SOLO = UNIT / "v01" / "art-right.png"  # Santa solo cocoa hero (512) — KEEP concept
L_COMP = UNIT / "v03" / "art-left.png"  # village whisper full-res composition
VILLAGE = ROOT / "Images/styles3/E-back-village-snow.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"

R_PROMPT = """\
Children's picture-book IMAGE PAGE, square 1:1, ART ONLY — no text, no letters.

PRESERVE composition of image 1: SANTA SOLO holding a steaming cocoa mug with marshmallows \
as the prop hero — firelight left, Christmas-tree glow right, warm burgundy living room. \
CLOSE / intimate cocoa portrait — NOT a wide gift-sea floor scene.

CRITICAL: NO child, NO boy, NO second figure anywhere. Santa alone with cocoa only.

Image 2 = Santa character lock (open coat, cream striped shirt, brown suspenders OVER shirt).
Image 3 = painted gouache quality / warm firelight palette.

Standard frame treatment: soft dissolve vignette to cream edges.
Rich gift-book color — deep warm reds, golden firelight, readable steam + marshmallows.
High-resolution print plate.
"""

L_PROMPT = """\
Children's picture-book TEXT PAGE, square 1:1, ART ONLY — no text, no letters.

PRESERVE exact composition of image 1: faint distant snowy village in soft dissolve-to-cream \
vignette, generous open cream center/bottom for poem type. Same layout, same camera, same \
village placement — DO NOT recompose.

COLOR DEPTH ONLY (fix washout):
- Night sky: deeper blue like image 2 (rich twilight blue, not washed grey)
- Windows: warmer golden glow (richer amber/gold light from cottage windows)
- Snow: subtle cool blue shadows in banks and under trees (not flat chalk white)
- Keep soft watercolor/gouache — richer chroma, not neon or photoreal

Image 2 = village snow COLOR reference (deeper night blues + warm windows).
Image 3 = soft vignette dissolve → cream edges (frame treatment only).

Still a quiet whisper atmosphere — richer color, not a loud full scene.
High-resolution print plate.
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


def upload(path: Path) -> str:
    url = fal_client.upload_file(str(path))
    print("uploaded", path.name, "->", url[:90])
    return url


def download(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def to_page(im: Image.Image) -> Image.Image:
    if im.size == (PAGE, PAGE):
        return im
    return im.resize((PAGE, PAGE), Image.Resampling.LANCZOS)


def run_edit(prompt: str, urls: list[str], seed: int | None = None) -> dict:
    args = {
        "prompt": prompt,
        "image_urls": urls,
        "num_images": 1,
        "output_format": "png",
        "resolution": "2K",
        "aspect_ratio": "1:1",
        "limit_generations": True,
        "safety_tolerance": "4",
    }
    if seed is not None:
        args["seed"] = seed
    print("subscribe", BANANA, "...")
    result = fal_client.subscribe(BANANA, arguments=args, with_logs=True)
    return result


def save_side(ver: str, side: str, result: dict) -> tuple[Path, dict]:
    out = UNIT / ver
    out.mkdir(parents=True, exist_ok=True)
    images = result.get("images") or []
    url = images[0]["url"]
    raw = download(url)
    page = to_page(raw)
    stem = f"art-{side}"
    raw.save(out / f"{stem}-banana-2k.png")
    dest = out / f"{stem}.png"
    page.save(dest, optimize=True)
    meta = {
        "version": ver,
        "side": side,
        "model": BANANA,
        "raw_size": list(raw.size),
        "page_size": list(page.size),
        "fal_url": url,
        "seed": result.get("seed"),
        "upscale": f"Lanczos -> {PAGE}x{PAGE}",
    }
    (out / f"meta-{side}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("saved", dest, page.size)
    return dest, meta


def main() -> None:
    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import text_image_board  # type: ignore

    r_comp = upload(R_SOLO)
    l_comp = upload(L_COMP)
    village = upload(VILLAGE)
    frame = upload(FRAME)
    santa = upload(SANTA)
    style = upload(STYLE)

    # --- R v03 Santa solo KEEP ---
    print("\n=== R p15 v03 Santa solo KEEP ===")
    r_result = run_edit(R_PROMPT, [r_comp, santa, style], seed=916278999)
    print(r_result)
    r_path, meta_r = save_side("v03", "right", r_result)
    (UNIT / "v03" / "RECIPE-right.md").write_text(
        f"""# RECIPE — S06-cocoa / v03 RIGHT (KEEP)

| Field | Value |
|-------|--------|
| **name** | S6 Cocoa R — Santa solo cocoa hero KEEP |
| **unit** | S06-cocoa |
| **book page** | Flow v2 p15 IMAGE |
| **version** | v03 (RIGHT) |
| **date** | {DAY} |
| **status** | **KEEP / LOCKED** — Santa solo · no boy |
| **model** | `{BANANA}` @ 2K → Lanczos **2625×2625** |
| **composition lock** | v01 art-right (solo cocoa portrait) |
| **refs** | santa-G0-v2 · style-lock-v2 |
| **seed** | {meta_r.get("seed")} |
| **fal_url** | `{meta_r["fal_url"]}` |
| **raw → page** | {meta_r["raw_size"]} → 2625² |

## Intent

Santa alone holding steaming cocoa with marshmallows; firelight + tree glow; open-coat wardrobe. NO child. Print-res lock.
""",
        encoding="utf-8",
    )

    # --- L v04 color depth ---
    print("\n=== L p14 v04 richer color ===")
    l_result = run_edit(L_PROMPT, [l_comp, village, frame], seed=2038430340)
    print(l_result)
    l_path, meta_l = save_side("v04", "left", l_result)
    (UNIT / "v04" / "RECIPE.md").write_text(
        f"""# RECIPE — S06-cocoa / v04 LEFT

| Field | Value |
|-------|--------|
| **name** | S6 Cocoa L — village whisper + richer color |
| **unit** | S06-cocoa |
| **book page** | Flow v2 p14 TEXT |
| **version** | v04 (LEFT) |
| **date** | {DAY} |
| **status** | working — color depth pass |
| **model** | `{BANANA}` @ 2K → Lanczos **2625×2625** |
| **composition lock** | v03 L (same village dissolve) |
| **refs** | E-back-village-snow (color) · frame-reference |
| **seed** | {meta_l.get("seed")} |
| **fal_url** | `{meta_l["fal_url"]}` |
| **raw → page** | {meta_l["raw_size"]} → 2625² |
| **paired_right** | v03 art-right KEEP |

## Intent

Same composition as v03 L. Color only: deeper night blue sky, warmer golden windows, subtle blue snow shadows. Soft dissolve vignette retained.
""",
        encoding="utf-8",
    )

    Image.open(l_path).save(UNIT / "art-left.png")
    Image.open(r_path).save(UNIT / "art-right.png")

    INDEX.mkdir(parents=True, exist_ok=True)
    board = INDEX / f"S06-cocoa-L-v04-R-v03-KEEP-{DAY}.png"
    text_image_board(
        Image.open(l_path),
        Image.open(r_path),
        board,
        unit="S06-cocoa",
        version="L v04 + R v03 KEEP",
        day=DAY,
        tech="Banana Pro /edit · 2K→2625² · R Santa-solo KEEP · L color depth",
        subtitle="LEFT p14 richer village · RIGHT p15 Santa solo cocoa LOCKED",
    )
    print("BOARD", board)
    print("L", Image.open(l_path).size, "R", Image.open(r_path).size)


if __name__ == "__main__":
    main()
