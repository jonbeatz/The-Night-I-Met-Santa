#!/usr/bin/env python3
"""S7 Proof v08 — framed ALT with shallow vignette + wall ROI restored from clean base.

Root cause of 'ghost Santa' on framed alts: cream dissolve bleeding into burgundy wall
reads as a pale face. Fix: shallower edge frame + paste clean wall from unframed base.
KEEP untouched.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/development/S07-proof/v06-clean-wall/art.png"
KEEP = ROOT / "Media/development/S07-proof/_LOCKED-v03/art.png"
FRAME = ROOT / "Media/approved/style-refs/spread-frame-reference.png"
OUT = ROOT / "Media/development/S07-proof/v08-framed-alt"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
TARGET = (5250, 2625)
PAGE = 2625
CREAM = (252, 246, 238)
DAY = "2026-07-23"

# Wall between tree and boy — restore from clean base after frame
WALL_BOX = (2550, 80, 4000, 1100)  # left, top, right, bottom


def shallow_frame_mask(frame: Image.Image) -> Image.Image:
    """Softer outer dissolve — less intrusion into mid wall."""
    fr = frame.convert("RGB").resize(TARGET, Image.Resampling.LANCZOS)
    arr = np.asarray(fr, dtype=np.float32)
    cream = np.array(CREAM, dtype=np.float32)
    dist = np.linalg.norm(arr - cream, axis=2)
    content = np.clip((dist - 14.0) / 36.0, 0, 1)
    content = content * content * (3 - 2 * content)

    # Larger inner pad = vignette stays nearer the paper edge
    outer = Image.new("L", TARGET, 0)
    d = ImageDraw.Draw(outer)
    pad = 90
    d.rounded_rectangle(
        [pad, pad, TARGET[0] - pad, TARGET[1] - pad],
        radius=240,
        fill=255,
    )
    outer = outer.filter(ImageFilter.GaussianBlur(radius=85))
    o = np.asarray(outer, dtype=np.float32) / 255.0

    yy, xx = np.mgrid[0 : TARGET[1], 0 : TARGET[0]]
    cy, cx = TARGET[1] / 2.0, TARGET[0] / 2.0
    # Bigger safe ellipse — wall mid-field stays fully opaque
    ell = 1.0 - np.clip(
        ((xx - cx) / (TARGET[0] * 0.46)) ** 2 + ((yy - cy) / (TARGET[1] * 0.44)) ** 2,
        0,
        1,
    )
    ell = ell * ell * (3 - 2 * ell)

    mask = np.clip(ell + (1.0 - ell) * o * np.maximum(content, 0.8), 0, 1)
    m = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
    m = m.filter(ImageFilter.GaussianBlur(radius=10))
    arr_m = np.asarray(m, dtype=np.float32) / 255.0
    arr_m = np.clip(np.maximum(arr_m, ell), 0, 1)
    return Image.fromarray((arr_m * 255).astype(np.uint8), mode="L")


def restore_wall(framed: Image.Image, clean: Image.Image) -> Image.Image:
    """Paste clean wall ROI so cream bleed can't fake a face on burgundy."""
    out = framed.copy()
    l, t, r, b = WALL_BOX
    patch = clean.crop((l, t, r, b))
    # Soft feather mask for the patch
    pw, ph = patch.size
    feather = Image.new("L", (pw, ph), 0)
    d = ImageDraw.Draw(feather)
    inset = 40
    d.rounded_rectangle([inset, inset, pw - inset, ph - inset], radius=60, fill=255)
    feather = feather.filter(ImageFilter.GaussianBlur(radius=28))
    out.paste(patch, (l, t), feather)
    return out


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def board(keep: Image.Image, framed: Image.Image, path: Path) -> None:
    w, h = 1400, 700
    a = keep.resize((w, h), Image.Resampling.LANCZOS)
    b = framed.resize((w, h), Image.Resampling.LANCZOS)
    margin, gap, header = 28, 24, 78
    sheet = Image.new(
        "RGB", (margin * 2 + w * 2 + gap, margin + header + h + 44), (252, 248, 240)
    )
    d = ImageDraw.Draw(sheet)
    f1, f2 = font(20), font(14)
    d.text(
        (margin, 12),
        "S7 Proof — KEEP v03  |  v08 FRAMED ALT (shallow vignette + wall restore)",
        fill=(35, 28, 22),
        font=f1,
    )
    d.text(
        (margin, 42),
        "Cream frame without bleeding a pale 'face' onto burgundy · KEEP untouched",
        fill=(100, 90, 75),
        font=f2,
    )
    y = margin + header
    sheet.paste(a, (margin, y))
    sheet.paste(b, (margin + w + gap, y))
    d.text((margin, y + h + 8), "v03 KEEP — no frame", fill=(50, 40, 35), font=f2)
    d.text(
        (margin + w + gap, y + h + 8),
        "v08-framed-alt — watercolor frame (preview)",
        fill=(50, 40, 35),
        font=f2,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, "PNG")


def main() -> None:
    base = Image.open(BASE).convert("RGB")
    if base.size != TARGET:
        base = base.resize(TARGET, Image.Resampling.LANCZOS)
    keep = Image.open(KEEP).convert("RGB")
    if keep.size != TARGET:
        keep = keep.resize(TARGET, Image.Resampling.LANCZOS)

    mask = shallow_frame_mask(Image.open(FRAME))
    framed = Image.composite(base, Image.new("RGB", TARGET, CREAM), mask)
    framed = restore_wall(framed, base)

    OUT.mkdir(parents=True, exist_ok=True)
    framed.save(OUT / "art.png", optimize=True)
    framed.crop((0, 0, PAGE, PAGE)).save(OUT / "art-left.png", optimize=True)
    framed.crop((PAGE, 0, TARGET[0], TARGET[1])).save(OUT / "art-right.png", optimize=True)

    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v08-framed-alt (PREVIEW)

| Field | Value |
|-------|--------|
| **status** | **FRAMED ALT** · does not replace KEEP |
| **base** | v06-clean-wall |
| **frame** | shallow cream vignette from spread-frame-reference |
| **extra** | restore mid wall ROI from clean base (stops cream bleed looking like a face) |
| **date** | {DAY} |

KEEP: `Media/development/S07-proof/art.png`
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v08-framed-alt",
                "status": "preview_alt",
                "replaces_keep": False,
                "base": "v06-clean-wall",
                "note": "shallow frame + wall ROI restore",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # cleanup wallcheck temps
    for p in (ROOT / "Media/development/S07-proof").glob("_wallcheck_*"):
        p.unlink(missing_ok=True)

    board_path = INDEX / f"S07-proof-v03-KEEP-vs-v08-framed-alt-{DAY}.png"
    board(keep, framed, board_path)
    print("FRAMED", OUT / "art.png")
    print("BOARD", board_path)


if __name__ == "__main__":
    main()
