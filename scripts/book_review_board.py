#!/usr/bin/env python3
"""Review / comparison boards with Flow v2 poem captions + glanceable tech cue.

Locked rule (Jon 2026-07-22): every board shows poem (or image context) under each side.

  LEFT p12 — "Oh, what a feeling..."
  RIGHT p13 — "But with laughs..."

Glanceable tech line (Jon 2026-07-22): under the title, e.g.
  Qwen 2 Pro /edit · 2048×1024 · S3 v07 quality bar

Use for TEXT+IMAGE, seamless spreads, and split pages. Poem source: book_poem_map.py
(from JON-BOOK-FLOW-v2-FINAL.md).
"""
from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from book_poem_map import BEATS, captions, footer_lines, resolve_unit

# Default glanceable cues when RECIPE not passed (model · size · quality bar)
DEFAULT_TECH = {
    "P01-title": "Pillow structure + Qwen polish · 8.5×8.5 · v16 KEEP",
    "P02-about-spread": "Qwen 2 Pro /edit · seamless · P02 v04 KEEP",
    "S01-approach": "Qwen 2 Pro /edit · split pages · S1 KEEP",
    "S02-threshold": "Qwen 2 Pro /edit · 2048×1024 · open-coat wardrobe",
    "S03-eyes-met": "Qwen 2 Pro /edit · 2048×1024 · QUALITY BAR",
    "S04-sit-here": "Qwen 2 Pro /edit · square · S3 v07 quality bar",
    "S05-chat": "Qwen 2 Pro /edit · 2048×1024 · S3 v07 quality bar",
    "S06-cocoa": "Banana Pro /edit · 2K→2625² · S3 v07 quality bar",
    "S07-proof": "Qwen 2 Pro /edit v06 · 5250×2625 · S5 quality bar",
    "S08-gone": "Qwen 2 Pro /edit · 2048×1024 · S3 v07 quality bar",
    "S09-search": "Qwen 2 Pro /edit · split pages · S3 v07 quality bar",
    "S10-note": "Qwen 2 Pro /edit · square · S3 v07 quality bar",
    "S11-wish": "Qwen 2 Pro /edit · 2048×1024 · S3 v07 quality bar",
    "S12-god-bless": "Qwen 2 Pro /edit v06 · 5250×2625 · closing FINAL STORY IMAGE",
}


def tech_line(unit: str, override: str = "") -> str:
    return (override or DEFAULT_TECH.get(unit, "see RECIPE.md")).strip()


def font(sz: int) -> ImageFont.ImageFont:
    for p in (
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
    ):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, max_w: int, f: ImageFont.ImageFont) -> list[str]:
    # greedy wrap by character width
    words = text.split(" ")
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = w if not cur else f"{cur} {w}"
        bbox = draw.textbbox((0, 0), trial, font=f)
        if bbox[2] - bbox[0] <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def _draw_poem_block(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    max_w: int,
    text: str,
    *,
    title_fill=(32, 28, 24),
    body_fill=(70, 64, 58),
) -> int:
    """Draw wrapped poem caption; return height used."""
    f_title = font(14)
    f_body = font(12)
    # Split "LEFT p12 — \"...\"" into label + quote when possible
    if " — " in text:
        label, rest = text.split(" — ", 1)
        draw.text((x, y), label, fill=title_fill, font=f_title)
        y += 18
        lines = _wrap(draw, rest, max_w, f_body)
    else:
        lines = _wrap(draw, text, max_w, f_body)
    for line in lines:
        draw.text((x, y), line, fill=body_fill, font=f_body)
        y += 16
    return y


def _draw_header(
    draw: ImageDraw.ImageDraw,
    margin: int,
    title: str,
    *,
    tech: str = "",
    subtitle: str = "",
) -> None:
    """Title + glanceable tech cue (+ optional mood note)."""
    draw.text((margin, 12), title, fill=(28, 24, 20), font=font(20))
    y = 38
    if tech:
        draw.text((margin, y), tech, fill=(90, 82, 74), font=font(13))
        y += 18
    if subtitle:
        draw.text((margin, y), subtitle, fill=(130, 120, 110), font=font(11))


def _header_h(tech: str = "", subtitle: str = "") -> int:
    h = 44
    if tech:
        h += 18
    if subtitle:
        h += 16
    return max(h, 56)


def text_image_board(
    left: Image.Image,
    right: Image.Image,
    out: Path,
    *,
    unit: str,
    version: str,
    day: str,
    tech: str = "",
    subtitle: str = "",
    side: int = 520,
) -> Path:
    """Two separate pages side-by-side with poem captions + tech cue."""
    left_c, right_c = captions(unit)
    tech = tech_line(unit, tech)
    title = f"{BEATS[unit]['title']} — {version} TEXT+IMAGE ({day})"
    l = left.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
    r = right.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
    margin, gap = 28, 20
    header = _header_h(tech, subtitle)
    poem_h = 110
    w = margin * 2 + side * 2 + gap
    h = margin * 2 + header + side + poem_h
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    _draw_header(d, margin, title, tech=tech, subtitle=subtitle)
    y = margin + header
    sheet.paste(l, (margin, y))
    sheet.paste(r, (margin + side + gap, y))
    py = y + side + 10
    _draw_poem_block(d, margin, py, side - 8, left_c)
    _draw_poem_block(d, margin + side + gap, py, side - 8, right_c)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    return out


def seamless_board(
    art: Image.Image,
    out: Path,
    *,
    unit: str,
    version: str,
    day: str,
    tech: str = "",
    subtitle: str = "",
    width: int = 1040,
) -> Path:
    """Full seamless spread board with L/R poem captions under halves."""
    left_c, right_c = captions(unit)
    tech = tech_line(unit, tech)
    title = f"{BEATS[unit]['title']} — {version} seamless ({day})"
    h_img = int(width * art.height / art.width)
    fitted = art.convert("RGB").resize((width, h_img), Image.Resampling.LANCZOS)
    margin = 28
    header = _header_h(tech, subtitle)
    poem_h = 110
    sheet = Image.new("RGB", (margin * 2 + width, margin * 2 + header + h_img + poem_h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    _draw_header(d, margin, title, tech=tech, subtitle=subtitle)
    y = margin + header
    sheet.paste(fitted, (margin, y))
    mid = margin + width // 2
    d.line([(mid, y), (mid, y + h_img)], fill=(220, 210, 200), width=1)
    py = y + h_img + 10
    half = width // 2 - 8
    _draw_poem_block(d, margin, py, half, left_c)
    _draw_poem_block(d, mid + 4, py, half, right_c)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    return out


def split_board(
    left: Image.Image,
    right: Image.Image,
    out: Path,
    *,
    unit: str,
    version: str,
    day: str,
    tech: str = "",
    subtitle: str = "",
    side: int = 520,
) -> Path:
    """Two separate compositions with poem captions (S1 / S9)."""
    left_c, right_c = captions(unit)
    tech = tech_line(unit, tech)
    title = f"{BEATS[unit]['title']} — {version} SPLIT ({day})"
    l = left.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
    r = right.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
    margin, gap = 28, 20
    header = _header_h(tech, subtitle)
    poem_h = 110
    w = margin * 2 + side * 2 + gap
    h = margin * 2 + header + side + poem_h
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    _draw_header(d, margin, title, tech=tech, subtitle=subtitle)
    y = margin + header
    sheet.paste(l, (margin, y))
    sheet.paste(r, (margin + side + gap, y))
    py = y + side + 10
    _draw_poem_block(d, margin, py, side - 8, left_c)
    _draw_poem_block(d, margin + side + gap, py, side - 8, right_c)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    return out


def compare_two_board(
    before: Image.Image,
    after: Image.Image,
    out: Path,
    *,
    unit: str,
    version: str,
    day: str,
    before_label: str,
    after_label: str,
    tech: str = "",
    subtitle: str = "",
    side: int = 520,
) -> Path:
    """Before/after (e.g. wardrobe) with shared poem strip under both."""
    left_c, right_c = captions(unit)
    tech = tech_line(unit, tech)
    title = f"{BEATS[unit]['title']} — {version} ({day})"
    b = before.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
    a = after.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
    margin, gap = 28, 20
    header = _header_h(tech, subtitle)
    poem_h = 130
    w = margin * 2 + side * 2 + gap
    h = margin * 2 + header + side + 28 + poem_h
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    _draw_header(d, margin, title, tech=tech, subtitle=subtitle)
    y = margin + header
    sheet.paste(b, (margin, y))
    sheet.paste(a, (margin + side + gap, y))
    d.text((margin, y + side + 6), before_label, fill=(32, 28, 24), font=font(13))
    d.text((margin + side + gap, y + side + 6), after_label, fill=(32, 28, 24), font=font(13))
    py = y + side + 28
    full_w = w - margin * 2
    y2 = _draw_poem_block(d, margin, py, full_w, left_c)
    _draw_poem_block(d, margin, y2 + 4, full_w, right_c)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    return out


def annotate_existing_board(board_path: Path, unit: str | None = None, *, backup: bool = True) -> Path:
    """Append poem footer strip under an existing board PNG (retroactive)."""
    unit = unit or resolve_unit(str(board_path))
    if not unit or unit not in BEATS:
        raise SystemExit(f"Cannot resolve poem unit for {board_path}")
    im = Image.open(board_path).convert("RGB")
    # skip if already annotated
    if im.info.get("poem_annotated") == "1":
        return board_path
    lines = footer_lines(unit)
    margin = 24
    poem_h = 24 + 18 * sum(max(2, len(textwrap.wrap(t, 110))) for t in lines) + 12
    sheet = Image.new("RGB", (im.width, im.height + poem_h), (252, 248, 240))
    sheet.paste(im, (0, 0))
    d = ImageDraw.Draw(sheet)
    d.rectangle([(0, im.height), (im.width, im.height + poem_h)], fill=(245, 240, 232))
    d.line([(margin, im.height + 2), (im.width - margin, im.height + 2)], fill=(210, 200, 190), width=1)
    y = im.height + 10
    for line in lines:
        y = _draw_poem_block(d, margin, y, im.width - margin * 2, line) + 6
    if backup:
        bak = board_path.with_suffix(".pre-poem.png")
        if not bak.exists():
            im.save(bak, "PNG")
    sheet.save(board_path, "PNG")
    return board_path


__all__ = [
    "text_image_board",
    "seamless_board",
    "split_board",
    "compare_two_board",
    "annotate_existing_board",
    "captions",
    "font",
    "tech_line",
    "DEFAULT_TECH",
]
