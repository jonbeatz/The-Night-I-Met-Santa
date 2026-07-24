#!/usr/bin/env python3
"""S7 Proof v07 — framed ALT from v06 clean-wall. KEEP untouched."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
# Prefer clean-wall base (no ghost smudge); fall back to locked v03
BASE = ROOT / "Media/development/S07-proof/v06-clean-wall/art.png"
FALLBACK = ROOT / "Media/development/S07-proof/_LOCKED-v03/art.png"
FRAME = ROOT / "Media/approved/style-refs/spread-frame-reference.png"
OUT = ROOT / "Media/development/S07-proof/v07-framed-alt"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
TARGET = (5250, 2625)
PAGE = 2625
CREAM = (252, 246, 238)
DAY = "2026-07-23"


def edge_mask_from_frame(frame: Image.Image) -> Image.Image:
    """Watercolor edge dissolve; center forced opaque (no frame-ref scene leak)."""
    fr = frame.convert("RGB").resize(TARGET, Image.Resampling.LANCZOS)
    arr = np.asarray(fr, dtype=np.float32)
    cream = np.array(CREAM, dtype=np.float32)
    dist = np.linalg.norm(arr - cream, axis=2)
    lo, hi = 10.0, 38.0
    content = np.clip((dist - lo) / (hi - lo), 0.0, 1.0)
    content = content * content * (3.0 - 2.0 * content)

    outer = Image.new("L", TARGET, 0)
    d = ImageDraw.Draw(outer)
    pad = 40
    d.rounded_rectangle(
        [pad, pad, TARGET[0] - pad, TARGET[1] - pad],
        radius=300,
        fill=255,
    )
    outer = outer.filter(ImageFilter.GaussianBlur(radius=130))
    o = np.asarray(outer, dtype=np.float32) / 255.0

    yy, xx = np.mgrid[0 : TARGET[1], 0 : TARGET[0]]
    cy, cx = TARGET[1] / 2.0, TARGET[0] / 2.0
    ell = 1.0 - np.clip(
        ((xx - cx) / (TARGET[0] * 0.40)) ** 2 + ((yy - cy) / (TARGET[1] * 0.38)) ** 2,
        0,
        1,
    )
    ell = ell * ell * (3 - 2 * ell)

    # Stronger edge dissolve than v05 for a clearer "framed" read
    mask = np.clip(ell + (1.0 - ell) * o * np.maximum(content, 0.70), 0, 1)
    m_img = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
    m_img = m_img.filter(ImageFilter.GaussianBlur(radius=16))
    m = np.asarray(m_img, dtype=np.float32) / 255.0
    m = np.clip(np.maximum(m, ell * 0.99), 0, 1)
    return Image.fromarray((m * 255).astype(np.uint8), mode="L").filter(
        ImageFilter.GaussianBlur(radius=8)
    )


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
        "S7 Proof — KEEP v03 (unframed)  |  v07 FRAMED ALT (clean wall + vignette)",
        fill=(35, 28, 22),
        font=f1,
    )
    d.text(
        (margin, 42),
        "Base: v06 clean-wall · cream watercolor dissolve · KEEP art.png untouched",
        fill=(100, 90, 75),
        font=f2,
    )
    y = margin + header
    sheet.paste(a, (margin, y))
    sheet.paste(b, (margin + w + gap, y))
    d.text((margin, y + h + 8), "v03 KEEP — no frame", fill=(50, 40, 35), font=f2)
    d.text(
        (margin + w + gap, y + h + 8),
        "v07-framed-alt — watercolor frame (preview)",
        fill=(50, 40, 35),
        font=f2,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, "PNG")


def main() -> None:
    src_path = BASE if BASE.is_file() else FALLBACK
    base = Image.open(src_path).convert("RGB")
    if base.size != TARGET:
        base = base.resize(TARGET, Image.Resampling.LANCZOS)

    keep = Image.open(FALLBACK).convert("RGB")
    if keep.size != TARGET:
        keep = keep.resize(TARGET, Image.Resampling.LANCZOS)

    mask = edge_mask_from_frame(Image.open(FRAME))
    cream = Image.new("RGB", TARGET, CREAM)
    framed = Image.composite(base, cream, mask)

    OUT.mkdir(parents=True, exist_ok=True)
    framed.save(OUT / "art.png", optimize=True)
    framed.crop((0, 0, PAGE, PAGE)).save(OUT / "art-left.png", optimize=True)
    framed.crop((PAGE, 0, TARGET[0], TARGET[1])).save(OUT / "art-right.png", optimize=True)

    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v07-framed-alt (PREVIEW)

| Field | Value |
|-------|--------|
| **status** | **FRAMED ALT** — preview only · does **not** replace v03 KEEP |
| **base** | `{src_path.relative_to(ROOT).as_posix()}` (clean wall) |
| **frame** | `spread-frame-reference.png` (edge mask only · center opaque) |
| **date** | {DAY} |
| **size** | 5250×2625 + L/R |

KEEP remains unframed at `Media/development/S07-proof/art.png`.
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "version": "v07-framed-alt",
                "status": "preview_alt",
                "replaces_keep": False,
                "base": str(src_path.relative_to(ROOT)).replace("\\\\", "/"),
                "frame": "spread-frame-reference.png",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    board_path = INDEX / f"S07-proof-v03-KEEP-vs-v07-framed-alt-{DAY}.png"
    board(keep, framed, board_path)
    print("FRAMED ALT", OUT / "art.png")
    print("BOARD", board_path)
    print("base used", src_path)


if __name__ == "__main__":
    main()
