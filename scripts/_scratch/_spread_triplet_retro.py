#!/usr/bin/env python3
"""Retroactive spread triplet: ensure art.png + art-left.png + art-right.png.

- If art.png is wide (spread): split midline → L/R at half width, resize each to 2625² if needed.
- If only L+R exist: stitch → art.png (side-by-side), normalize sizes.
Does not overwrite existing L/R when already present unless --force-resplit.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Media\development")
PAGE = 2625
SPREAD = (5250, 2625)

# Two-page / spread units that must have the triplet
SPREAD_UNITS = {
    "P02-about-spread",
    "S01-approach",
    "S02-threshold",
    "S03-eyes-met",
    "S04-sit-here",
    "S05-chat",
    "S06-cocoa",
    "S07-proof",
    "S08-gone",
    "S09-search",
    "S10-note",
    "S11-wish",
    "S12a-blessing",
    "S12b-god-bless",
}


def to_page(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    if im.size == (PAGE, PAGE):
        return im
    return im.resize((PAGE, PAGE), Image.Resampling.LANCZOS)


def to_spread(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    if im.size == SPREAD:
        return im
    return im.resize(SPREAD, Image.Resampling.LANCZOS)


def split_from_art(art: Image.Image) -> tuple[Image.Image, Image.Image]:
    art = to_spread(art)
    mid = art.width // 2
    left = art.crop((0, 0, mid, art.height))
    right = art.crop((mid, 0, art.width, art.height))
    return to_page(left), to_page(right)


def stitch(left: Image.Image, right: Image.Image) -> Image.Image:
    l = to_page(left)
    r = to_page(right)
    out = Image.new("RGB", SPREAD)
    out.paste(l, (0, 0))
    out.paste(r, (PAGE, 0))
    return out


def process(unit: Path) -> list[str]:
    notes: list[str] = []
    art_p = unit / "art.png"
    left_p = unit / "art-left.png"
    right_p = unit / "art-right.png"

    has_art = art_p.is_file()
    has_l = left_p.is_file()
    has_r = right_p.is_file()

    if has_art:
        art = Image.open(art_p)
        w, h = art.size
        is_wide = w >= int(h * 1.5)
        if is_wide:
            # Normalize master to print spread if needed
            if art.size != SPREAD:
                art = to_spread(art)
                art.save(art_p, optimize=True)
                notes.append(f"resized art.png → {SPREAD[0]}x{SPREAD[1]}")
            if not (has_l and has_r):
                left, right = split_from_art(art)
                left.save(left_p, optimize=True)
                right.save(right_p, optimize=True)
                notes.append("split art.png → art-left + art-right")
            else:
                # Ensure chops are 2625²
                for p, label in ((left_p, "L"), (right_p, "R")):
                    im = Image.open(p)
                    if im.size != (PAGE, PAGE):
                        to_page(im).save(p, optimize=True)
                        notes.append(f"resized art-{label.lower()} → 2625²")
        else:
            notes.append(f"skip split (art is square {w}x{h} — single-page unit?)")
    elif has_l and has_r:
        left = Image.open(left_p)
        right = Image.open(right_p)
        # Normalize chops
        if left.size != (PAGE, PAGE):
            left = to_page(left)
            left.save(left_p, optimize=True)
            notes.append("resized art-left → 2625²")
        else:
            left = left.convert("RGB")
        if right.size != (PAGE, PAGE):
            right = to_page(right)
            right.save(right_p, optimize=True)
            notes.append("resized art-right → 2625²")
        else:
            right = right.convert("RGB")
        spread = stitch(left, right)
        spread.save(art_p, optimize=True)
        notes.append("stitched L+R → art.png 5250×2625")
    else:
        notes.append("incomplete — missing art and/or L/R")

    return notes


def main() -> None:
    for name in sorted(SPREAD_UNITS):
        unit = ROOT / name
        if not unit.is_dir():
            print(f"{name}: MISSING DIR")
            continue
        notes = process(unit)
        print(f"{name}: {'; '.join(notes) if notes else 'OK (triplet present)'}")


if __name__ == "__main__":
    main()
