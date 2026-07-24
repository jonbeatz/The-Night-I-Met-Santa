#!/usr/bin/env python3
"""S7 Proof v04 — apply spread-Frame-Style1 vignette to locked v03 (content unchanged)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
UNIT = ROOT / "Media/development/S07-proof"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
FRAME_REF = ROOT / "Images/styles2/spread-Frame-Style1.png"
APPROVED_FRAME = ROOT / "Media/approved/style-refs/spread-frame-reference.png"
TARGET = (5250, 2625)
CREAM = (252, 246, 238)
DAY = "2026-07-23"


def mask_from_frame(frame: Image.Image) -> Image.Image:
    """Soft rounded watercolor dissolve matching spread-Frame-Style1 cream edges."""
    fr = frame.convert("RGB").resize(TARGET, Image.Resampling.LANCZOS)
    arr = np.asarray(fr, dtype=np.float32)
    cream = np.array(CREAM, dtype=np.float32)
    dist = np.linalg.norm(arr - cream, axis=2)
    # Content strength from frame ref (cream corners → 0)
    lo, hi = 16.0, 48.0
    content = np.clip((dist - lo) / (hi - lo), 0.0, 1.0)
    content = content * content * (3.0 - 2.0 * content)

    # Dreamy rounded outer falloff (cloud-like corners)
    outer = Image.new("L", TARGET, 0)
    d = ImageDraw.Draw(outer)
    pad = 55
    d.rounded_rectangle(
        [pad, pad, TARGET[0] - pad, TARGET[1] - pad],
        radius=260,
        fill=255,
    )
    outer = outer.filter(ImageFilter.GaussianBlur(radius=110))
    o = np.asarray(outer, dtype=np.float32) / 255.0

    # Center stays full strength; edges follow dissolve
    yy, xx = np.mgrid[0 : TARGET[1], 0 : TARGET[0]]
    cy, cx = TARGET[1] / 2.0, TARGET[0] / 2.0
    ell = 1.0 - np.clip(((xx - cx) / (TARGET[0] * 0.50)) ** 2 + ((yy - cy) / (TARGET[1] * 0.48)) ** 2, 0, 1)
    ell = ell * ell * (3 - 2 * ell)

    # Prefer keeping locked art solid in center; vignette only at perimeter
    final = np.clip(o * (0.72 + 0.28 * content) * (0.35 + 0.65 * ell + 0.35), 0, 1)
    final = np.clip(np.maximum(final, ell * o), 0, 1)
    mask = Image.fromarray((final * 255).astype(np.uint8), mode="L")
    return mask.filter(ImageFilter.GaussianBlur(radius=12))


def apply_vignette(art: Image.Image, mask: Image.Image) -> Image.Image:
    base = Image.new("RGB", TARGET, CREAM)
    art = art.convert("RGB").resize(TARGET, Image.Resampling.LANCZOS)
    return Image.composite(art, base, mask)


def font(sz: int) -> ImageFont.ImageFont:
    for p in (
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def compare_board(v03: Image.Image, v04: Image.Image, out: Path) -> None:
    # Side by side full spreads scaled for review
    w, h = 1400, 700
    a = v03.convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
    b = v04.convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
    margin, gap, header, footer = 28, 24, 78, 36
    sheet = Image.new(
        "RGB",
        (margin * 2 + w * 2 + gap, margin * 2 + header + h + footer),
        (252, 248, 240),
    )
    d = ImageDraw.Draw(sheet)
    title = "S7 Proof — v03 LOCKED (no frame)  |  v04 + spread frame treatment"
    tech = "Pillow vignette from spread-Frame-Style1 · exact v03 pixels · 5250×2625"
    d.text((margin, 16), title, fill=(40, 30, 25), font=font(22))
    d.text((margin, 46), tech, fill=(110, 95, 80), font=font(16))
    y = margin + header
    sheet.paste(a, (margin, y))
    sheet.paste(b, (margin + w + gap, y))
    d.text((margin, y + h + 8), "v03 — composition KEEP (hard edges)", fill=(60, 50, 40), font=font(15))
    d.text(
        (margin + w + gap, y + h + 8),
        "v04 — + soft watercolor cream vignette (spread frame)",
        fill=(60, 50, 40),
        font=font(15),
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")


def main() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))

    art_path = UNIT / "art.png"
    if not art_path.is_file():
        raise SystemExit("missing S07 art.png (v03)")
    v03 = Image.open(art_path).convert("RGB")
    if v03.size != TARGET:
        v03 = v03.resize(TARGET, Image.Resampling.LANCZOS)

    frame = Image.open(FRAME_REF)
    # Save approved spread frame reference (canonical)
    APPROVED_FRAME.parent.mkdir(parents=True, exist_ok=True)
    frame.convert("RGBA").resize(TARGET, Image.Resampling.LANCZOS).save(APPROVED_FRAME)
    print("saved", APPROVED_FRAME)

    mask = mask_from_frame(frame)
    mask_path = UNIT / "_tmp-vignette-mask.png"
    mask.save(mask_path)
    v04 = apply_vignette(v03, mask)

    # Preserve v03 bytes for board, then write v04 as current
    v03_tmp = UNIT / "_tmp-v03-locked.png"
    v03.save(v03_tmp)

    # Clean prior pngs except we'll rewrite keepers
    for name in ("art.png", "art-left.png", "art-right.png"):
        (UNIT / name).unlink(missing_ok=True)

    v04.save(UNIT / "art.png", optimize=True)
    v04.crop((0, 0, 2625, 2625)).save(UNIT / "art-left.png", optimize=True)
    v04.crop((2625, 0, 5250, 2625)).save(UNIT / "art-right.png", optimize=True)

    INDEX.mkdir(parents=True, exist_ok=True)
    board = INDEX / f"S07-proof-v03-vs-v04-frame-{DAY}.png"
    compare_board(Image.open(v03_tmp), v04, board)

    # delete temps (no duplicates rule)
    v03_tmp.unlink(missing_ok=True)
    mask_path.unlink(missing_ok=True)

    (UNIT / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v04

| Field | Value |
|-------|--------|
| **name** | S7 Proof — v03 composition + spread frame vignette |
| **unit** | S07-proof |
| **book page** | Flow v2 p16\\|17 SPREAD |
| **version** | v04 |
| **date** | {DAY} |
| **status** | working — frame pass on LOCKED v03 composition |
| **composition** | **LOCKED v03** — identical pixels under vignette |
| **frame** | `Images/styles2/spread-Frame-Style1.png` → `Media/approved/style-refs/spread-frame-reference.png` |
| **method** | Pillow composite · cream dissolve mask from frame ref + rounded outer bleed |
| **size** | **5250 × 2625** |

## Intent

Exact v03 scene (boy, tree, fireplace, camera, burgundy). Add standard **spread** soft watercolor vignette: edges dissolve to warm cream, rounded corners, dreamy bleed — not hard rectangle.
""",
        encoding="utf-8",
    )
    (UNIT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v04",
                "composition_lock": "v03",
                "frame": "spread-Frame-Style1 / spread-frame-reference.png",
                "method": "pillow_vignette",
                "size": list(TARGET),
                "status": "working",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("BOARD", board)
    print("v04", UNIT / "art.png", v04.size)


if __name__ == "__main__":
    main()
