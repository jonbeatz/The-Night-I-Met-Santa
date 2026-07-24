#!/usr/bin/env python3
"""S7 Proof framed ALT — locked v03 pixels + spread frame look. Does NOT touch KEEP art.png.

Critical: mask is EDGE-ONLY from cream detection; center forced opaque so frame-ref
scene (Santa etc.) can never leak into the composite.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
KEEP = ROOT / "Media/development/S07-proof/_LOCKED-v03/art.png"
FRAME = ROOT / "Media/approved/style-refs/spread-frame-reference.png"
OUT = ROOT / "Media/development/S07-proof/v05-framed-alt"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
TARGET = (5250, 2625)
PAGE = 2625
CREAM = (252, 246, 238)
DAY = "2026-07-23"


def edge_mask_from_frame(frame: Image.Image) -> Image.Image:
    """Soft watercolor edge dissolve. Center always fully opaque (no ref content leak)."""
    fr = frame.convert("RGB").resize(TARGET, Image.Resampling.LANCZOS)
    arr = np.asarray(fr, dtype=np.float32)
    cream = np.array(CREAM, dtype=np.float32)
    dist = np.linalg.norm(arr - cream, axis=2)

    # Near cream → transparent; only use this at the perimeter
    lo, hi = 12.0, 42.0
    content = np.clip((dist - lo) / (hi - lo), 0.0, 1.0)
    content = content * content * (3.0 - 2.0 * content)

    # Soft rounded outer falloff (dreamy corners)
    outer = Image.new("L", TARGET, 0)
    d = ImageDraw.Draw(outer)
    pad = 48
    d.rounded_rectangle(
        [pad, pad, TARGET[0] - pad, TARGET[1] - pad],
        radius=280,
        fill=255,
    )
    outer = outer.filter(ImageFilter.GaussianBlur(radius=120))
    o = np.asarray(outer, dtype=np.float32) / 255.0

    # Center ellipse: force FULL opacity so wall/Santa in frame ref never matter
    yy, xx = np.mgrid[0 : TARGET[1], 0 : TARGET[0]]
    cy, cx = TARGET[1] / 2.0, TARGET[0] / 2.0
    # Inner safe zone (~82% of plate) always 1.0
    ell = 1.0 - np.clip(
        ((xx - cx) / (TARGET[0] * 0.42)) ** 2 + ((yy - cy) / (TARGET[1] * 0.40)) ** 2,
        0,
        1,
    )
    ell = ell * ell * (3 - 2 * ell)  # 1 at center → 0 toward edges

    # Edge band uses frame cream shape * outer roundness; center = locked art 100%
    edge_band = (1.0 - ell) * o * (0.55 + 0.45 * content)
    # Where ell is high (center), mask = 1. Where edge, mask = edge_band strength via o
    mask = np.clip(ell + (1.0 - ell) * o * np.maximum(content, 0.75), 0, 1)
    # Soften edge only
    m_img = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
    m_img = m_img.filter(ImageFilter.GaussianBlur(radius=14))
    # Re-boost center after blur
    m = np.asarray(m_img, dtype=np.float32) / 255.0
    m = np.clip(np.maximum(m, ell * 0.98), 0, 1)
    out = Image.fromarray((m * 255).astype(np.uint8), mode="L")
    return out.filter(ImageFilter.GaussianBlur(radius=6))


def apply(art: Image.Image, mask: Image.Image) -> Image.Image:
    base = Image.new("RGB", TARGET, CREAM)
    return Image.composite(art.convert("RGB"), base, mask)


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def board(v03: Image.Image, framed: Image.Image, path: Path) -> None:
    w, h = 1400, 700
    a = v03.resize((w, h), Image.Resampling.LANCZOS)
    b = framed.resize((w, h), Image.Resampling.LANCZOS)
    margin, gap, header = 28, 24, 72
    sheet = Image.new("RGB", (margin * 2 + w * 2 + gap, margin + header + h + 40), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), "S7 Proof — KEEP v03 (unframed)  |  v05 framed ALT (preview only)", fill=(35, 28, 22), font=font(20))
    d.text((margin, 42), "Same locked pixels · cream vignette from spread-frame-reference edges · KEEP untouched", fill=(100, 90, 75), font=font(14))
    y = margin + header
    sheet.paste(a, (margin, y))
    sheet.paste(b, (margin + w + gap, y))
    d.text((margin, y + h + 8), "v03 KEEP — hard edges", fill=(50, 40, 35), font=font(14))
    d.text((margin + w + gap, y + h + 8), "v05-framed-alt — watercolor dissolve (no KEEP overwrite)", fill=(50, 40, 35), font=font(14))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, "PNG")


def main() -> None:
    keep = Image.open(KEEP).convert("RGB")
    if keep.size != TARGET:
        keep = keep.resize(TARGET, Image.Resampling.LANCZOS)

    frame = Image.open(FRAME)
    mask = edge_mask_from_frame(frame)
    framed = apply(keep, mask)

    OUT.mkdir(parents=True, exist_ok=True)
    framed.save(OUT / "art.png", optimize=True)
    framed.crop((0, 0, PAGE, PAGE)).save(OUT / "art-left.png", optimize=True)
    framed.crop((PAGE, 0, TARGET[0], TARGET[1])).save(OUT / "art-right.png", optimize=True)

    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v05-framed-alt (PREVIEW ONLY)

| Field | Value |
|-------|--------|
| **status** | **ALT PREVIEW** — not a KEEP · does not replace v03 |
| **base** | Locked `_LOCKED-v03/art.png` (identical scene pixels) |
| **frame** | `Media/approved/style-refs/spread-frame-reference.png` (edge mask only) |
| **method** | Pillow composite · cream dissolve · **center forced opaque** (frame-ref Santa/scene cannot leak) |
| **date** | {DAY} |
| **size** | 5250×2625 + L/R chops |

Development current remains **v03 KEEP** at `Media/development/S07-proof/art.png`.
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v05-framed-alt",
                "status": "preview_alt",
                "replaces_keep": False,
                "base": "Media/development/S07-proof/_LOCKED-v03/art.png",
                "frame": "spread-frame-reference.png",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    board_path = INDEX / f"S07-proof-v03-KEEP-vs-v05-framed-alt-{DAY}.png"
    board(keep, framed, board_path)
    print("ALT", OUT / "art.png")
    print("KEEP untouched", KEEP)
    print("BOARD", board_path)


if __name__ == "__main__":
    main()
