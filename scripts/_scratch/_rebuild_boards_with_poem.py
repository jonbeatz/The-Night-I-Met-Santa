#!/usr/bin/env python3
"""Rebuild / annotate comparison boards with Flow v2 poem captions (Jon 2026-07-22)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
sys.path.insert(0, str(ROOT / "scripts"))

from PIL import Image  # noqa: E402

from book_poem_map import resolve_unit  # noqa: E402
from book_review_board import (  # noqa: E402
    annotate_existing_board,
    compare_two_board,
    seamless_board,
    split_board,
    text_image_board,
)

MOCKS = ROOT / "Media/generated/mocks"
DEV = ROOT / "Media/development"
DAY = "2026-07-22"


def rebuild_from_art() -> list[Path]:
    """Rebuild current keep/working boards from source art (full poem layout)."""
    out: list[Path] = []

    # S1 Approach keep — split v13|v14
    s1l = DEV / "S01-approach/art-left.png"
    s1r = DEV / "S01-approach/art-right.png"
    if not s1l.exists():
        s1l = MOCKS / "S01-approach/v13/art.png"
    if not s1r.exists():
        s1r = MOCKS / "S01-approach/v14/art.png"
    if s1l.exists() and s1r.exists():
        p = MOCKS / f"S01-approach/_INDEX/S01-approach-comparison-split-v13-v14-{DAY}.png"
        split_board(
            Image.open(s1l),
            Image.open(s1r),
            p,
            unit="S01-approach",
            version="v13|v14 KEEP",
            day=DAY,
            subtitle="SPLIT · journey L + destination R",
        )
        out.append(p)

    # S2 Threshold v06 wardrobe compare
    s2_before = DEV / "S02-threshold/v05/art.png"
    s2_after = DEV / "S02-threshold/v06/art.png"
    if s2_before.exists() and s2_after.exists():
        # R-half crops for wardrobe focus (same as original board intent)
        def rh(im: Image.Image) -> Image.Image:
            im = im.convert("RGB")
            w, h = im.size
            return im.crop((w // 2, 0, w, h))

        p = MOCKS / f"S02-threshold/_INDEX/S02-threshold-v06-wardrobe-{DAY}.png"
        compare_two_board(
            rh(Image.open(s2_before)),
            rh(Image.open(s2_after)),
            p,
            unit="S02-threshold",
            version="v06 wardrobe KEEP",
            day=DAY,
            before_label="v05 BEFORE (R half)",
            after_label="v06 AFTER open-coat",
            subtitle="Wardrobe-only · composition locked · poem for pages 6|7",
        )
        out.append(p)

    # S2 full seamless keep board
    s2 = DEV / "S02-threshold/art.png"
    if s2.exists():
        p = MOCKS / f"S02-threshold/_INDEX/S02-threshold-v06-seamless-{DAY}.png"
        seamless_board(
            Image.open(s2),
            p,
            unit="S02-threshold",
            version="v06 KEEP",
            day=DAY,
            subtitle="Open-coat Santa G0 v2 · doorway spill language",
        )
        out.append(p)

    # S3 Eyes Met keep
    s3 = DEV / "S03-eyes-met/art.png"
    if s3.exists():
        p = MOCKS / f"S03-eyes-met/_INDEX/S03-eyes-met-comparison-spread-v07-{DAY}.png"
        seamless_board(
            Image.open(s3),
            p,
            unit="S03-eyes-met",
            version="v07 KEEP · QUALITY BAR",
            day=DAY,
            subtitle="Open-coat · Boy G0 · prefer fewer gifts later",
        )
        out.append(p)

    # S4 Sit Here v13
    s4l = DEV / "S04-sit-here/v13/art-left.png"
    s4r = DEV / "S04-sit-here/v13/art-right.png"
    if s4l.exists() and s4r.exists():
        p = MOCKS / f"S04-sit-here/_INDEX/S04-sit-here-v13-text-image-{DAY}.png"
        text_image_board(
            Image.open(s4l),
            Image.open(s4r),
            p,
            unit="S04-sit-here",
            version="v13 KEEP",
            day=DAY,
            subtitle="TEXT+IMAGE · mistletoe L · Santa RIGHT beckons",
        )
        out.append(p)

    # S4 Sit Here v12 (prior dial)
    s4l12 = DEV / "S04-sit-here/v12/art-left.png"
    s4r12 = DEV / "S04-sit-here/v12/art-right.png"
    if not s4l12.exists():
        s4l12 = MOCKS / "S04-sit-here/v12/art-left.png"
    if not s4r12.exists():
        s4r12 = MOCKS / "S04-sit-here/v12/art-right.png"
    if s4l12.exists() and s4r12.exists():
        p = MOCKS / f"S04-sit-here/_INDEX/S04-sit-here-v12-text-image-{DAY}.png"
        text_image_board(
            Image.open(s4l12),
            Image.open(s4r12),
            p,
            unit="S04-sit-here",
            version="v12 (superseded by v13)",
            day=DAY,
            subtitle="Prior dial · poem captions added",
        )
        out.append(p)

    # S5 Chat v01
    s5 = DEV / "S05-chat/v01/art.png"
    if not s5.exists():
        s5 = DEV / "S05-chat/art.png"
    if s5.exists():
        p = MOCKS / f"S05-chat/_INDEX/S05-chat-v01-seamless-{DAY}.png"
        seamless_board(
            Image.open(s5),
            p,
            unit="S05-chat",
            version="v01 KEEP",
            day=DAY,
            subtitle="Happiest spread · open-coat · Boy G0",
        )
        out.append(p)

    # S6 Cocoa v01
    s6l = DEV / "S06-cocoa/v01/art-left.png"
    s6r = DEV / "S06-cocoa/v01/art-right.png"
    if s6l.exists() and s6r.exists():
        p = MOCKS / f"S06-cocoa/_INDEX/S06-cocoa-v01-text-image-{DAY}.png"
        text_image_board(
            Image.open(s6l),
            Image.open(s6r),
            p,
            unit="S06-cocoa",
            version="v01",
            day=DAY,
            subtitle="TEXT+IMAGE · snowman/coat-tie-ring · cocoa prop hero",
        )
        out.append(p)

    # P01 title keep
    p01 = DEV / "P01-title/art.png"
    if p01.exists():
        # single-page board: reuse annotate pattern via a simple canvas
        from book_review_board import font as _font
        from book_poem_map import captions as _cap

        art = Image.open(p01).convert("RGB")
        side = 640
        fitted = art.resize((side, side), Image.Resampling.LANCZOS)
        cap = _cap("P01-title")[0]
        margin, header, poem_h = 28, 56, 70
        sheet = Image.new("RGB", (margin * 2 + side, margin * 2 + header + side + poem_h), (252, 248, 240))
        from PIL import ImageDraw

        d = ImageDraw.Draw(sheet)
        d.text((margin, 14), f"P01 Title — v16 KEEP ({DAY})", fill=(28, 24, 20), font=_font(20))
        sheet.paste(fitted, (margin, margin + header))
        from book_review_board import _draw_poem_block

        _draw_poem_block(d, margin, margin + header + side + 10, side, cap)
        p = MOCKS / f"_INDEX/P01-title-v16-KEEP-poem-{DAY}.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(p, "PNG")
        out.append(p)

    return out


def annotate_remaining() -> list[Path]:
    """Append poem footer to other _INDEX boards that weren't fully rebuilt."""
    done_names = {
        "S01-approach-comparison-split-v13-v14-2026-07-22.png",
        "S02-threshold-v06-wardrobe-2026-07-22.png",
        "S02-threshold-v06-seamless-2026-07-22.png",
        "S03-eyes-met-comparison-spread-v07-2026-07-22.png",
        "S04-sit-here-v13-text-image-2026-07-22.png",
        "S04-sit-here-v12-text-image-2026-07-22.png",
        "S05-chat-v01-seamless-2026-07-22.png",
        "S06-cocoa-v01-text-image-2026-07-22.png",
        "P01-title-v16-KEEP-poem-2026-07-22.png",
    }
    skip_substrings = (
        "style-lock",
        "LEFT-half",
        "RIGHT-half",
        "walls-cream-test",
        "pre-poem",
        "lora-paper",
        "/art.png",
        "\\art.png",
        "art-2048",
    )
    out: list[Path] = []
    for path in MOCKS.rglob("*.png"):
        if "_INDEX" not in path.parts:
            continue
        if path.name in done_names:
            continue
        if path.name.endswith(".pre-poem.png"):
            continue
        s = str(path).replace("\\", "/")
        if any(x in s for x in skip_substrings):
            continue
        # skip raw art living under _INDEX/text-page-lora/vNN/
        if "/text-page-lora/v" in s:
            continue
        unit = resolve_unit(s)
        if not unit:
            print("skip (no unit)", path.relative_to(ROOT))
            continue
        try:
            annotate_existing_board(path, unit)
            out.append(path)
            print("annotated", path.relative_to(ROOT), "->", unit)
        except Exception as e:  # noqa: BLE001
            print("FAIL", path, e)
    return out


if __name__ == "__main__":
    rebuilt = rebuild_from_art()
    print("--- rebuilt from art ---")
    for p in rebuilt:
        print(p.relative_to(ROOT))
    annotated = annotate_remaining()
    print("--- annotated ---")
    print(f"{len(annotated)} boards")
    print("DONE")
