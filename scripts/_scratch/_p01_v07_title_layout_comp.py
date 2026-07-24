#!/usr/bin/env python3
"""P01 title-page layout comps: v07 Winter Window + v08 Writing Desk side by side."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/P01-title"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
FONT_DIR = (
    ROOT
    / "Xtraz/Fonts/Allura,Cabin,Cinzel_Decorative,Cormorant_Garamond,Dancing_Script,etc"
    / "Cormorant_Garamond/static"
)

CREAM = (245, 240, 230)
INK = (44, 44, 44)  # #2C2C2C
PAGE = 2625
ART_FRAC = 0.66  # 60–70% page width
DAY = "2026-07-22"

TITLE = "The Night I Met Santa"
AUTHOR = "Written by Jack Farrell"
COPYRIGHT = (
    "First illustrated edition, 2026\n"
    "Book design by Jon Farrell"
)


def load_font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    name = {
        "regular": "CormorantGaramond-Regular.ttf",
        "medium": "CormorantGaramond-Medium.ttf",
        "semibold": "CormorantGaramond-SemiBold.ttf",
        "italic": "CormorantGaramond-Italic.ttf",
        "mediumitalic": "CormorantGaramond-MediumItalic.ttf",
    }[weight]
    return ImageFont.truetype(str(FONT_DIR / name), size)


def scrub_baked_text(im: Image.Image) -> Image.Image:
    """Paint cream over baked gibberish below the window (v07)."""
    out = im.convert("RGBA")
    w, h = out.size
    # Center band where Qwen baked "ANC PEM…" under the sill/presents
    blob = Image.new("L", (w, h), 0)
    bdraw = ImageDraw.Draw(blob)
    # Wide soft rectangle + ellipse covering lower open cream
    bdraw.rectangle(
        [int(w * 0.12), int(h * 0.72), int(w * 0.88), int(h * 0.98)],
        fill=255,
    )
    bdraw.ellipse(
        [int(w * 0.15), int(h * 0.68), int(w * 0.85), int(h * 0.92)],
        fill=255,
    )
    blob = blob.filter(ImageFilter.GaussianBlur(radius=55))
    cream = Image.new("RGBA", (w, h), (*CREAM, 255))
    cream.putalpha(blob)
    out = Image.alpha_composite(out, cream)
    # Extra bottom fade into page cream
    fade = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(fade)
    for y0 in range(int(h * 0.78), h):
        t = (y0 - int(h * 0.78)) / max(1, h - int(h * 0.78))
        fdraw.line([(0, y0), (w, y0)], fill=(*CREAM, int(255 * min(1.0, t * 1.35))))
    out = Image.alpha_composite(out, fade)
    return out.convert("RGB")


def soft_vignette_rgba(rgb: Image.Image, feather: int = 90) -> Image.Image:
    """Alpha mask: opaque center, soft fade to transparent at edges (FRAME ON)."""
    w, h = rgb.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    inset = max(8, feather // 3)
    draw.rounded_rectangle(
        [inset, inset, w - inset - 1, h - inset - 1],
        radius=int(min(w, h) * 0.06),
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


def center_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    cy: float,
    font: ImageFont.FreeTypeFont,
    fill=INK,
    spacing: int = 8,
) -> float:
    """Draw multi-line centered text; return bottom y of last line."""
    lines = text.split("\n")
    page_w = draw.im.size[0] if hasattr(draw, "im") else PAGE
    # Use bbox on a probe image size from font
    y = cy
    for line in lines:
        bbox = font.getbbox(line)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (PAGE - tw) // 2
        draw.text((x, int(y)), line, font=font, fill=fill)
        y += th + spacing
    return y


def compose_title_page(art_path: Path, scrub: bool, label: str) -> Image.Image:
    art = Image.open(art_path).convert("RGB")
    if scrub:
        art = scrub_baked_text(art)
        # Drop the lowest strip where glyphs lived; keep window/tree focus
        w, h = art.size
        art = art.crop((0, 0, w, int(h * 0.90)))
        # Square again from top-biased crop
        side = min(art.size)
        left = (art.width - side) // 2
        art = art.crop((left, 0, left + side, side))

    page = Image.new("RGB", (PAGE, PAGE), CREAM)
    art_w = int(PAGE * ART_FRAC)
    art_h = art_w  # square plate
    art_r = art.resize((art_w, art_h), Image.Resampling.LANCZOS)
    art_rgba = soft_vignette_rgba(art_r, feather=110)

    # Upper-middle placement: leave room for title above (~14% top), art starts ~16%
    ax = (PAGE - art_w) // 2
    ay = int(PAGE * 0.18)

    page_rgba = page.convert("RGBA")
    page_rgba.alpha_composite(art_rgba, (ax, ay))
    page = page_rgba.convert("RGB")
    draw = ImageDraw.Draw(page)

    title_font = load_font("medium", 92)
    author_font = load_font("italic", 42)
    copy_font = load_font("regular", 28)

    # Title above window — centered in the cream band
    title_top = int(PAGE * 0.055)
    # Two-line title reads better at this size
    title_lines = ["The Night I", "Met Santa"]
    y = title_top
    for line in title_lines:
        bbox = title_font.getbbox(line)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(((PAGE - tw) // 2, y), line, font=title_font, fill=INK)
        y += th + 6

    # Author + copyright below art
    below = ay + art_h + int(PAGE * 0.035)
    bbox = author_font.getbbox(AUTHOR)
    tw = bbox[2] - bbox[0]
    draw.text(((PAGE - tw) // 2, below), AUTHOR, font=author_font, fill=INK)

    copy_y = below + (bbox[3] - bbox[1]) + 28
    for line in COPYRIGHT.split("\n"):
        bbox = copy_font.getbbox(line)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(((PAGE - tw) // 2, copy_y), line, font=copy_font, fill=INK)
        copy_y += th + 10

    # Tiny mock label (not print)
    tiny = load_font("regular", 18)
    note = f"COMP · {label} · Cormorant mock type · not final"
    bbox = tiny.getbbox(note)
    draw.text(
        ((PAGE - (bbox[2] - bbox[0])) // 2, PAGE - 48),
        note,
        font=tiny,
        fill=(160, 150, 140),
    )
    return page


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def build_board(left: Image.Image, right: Image.Image) -> Path:
    panel = 900
    label_h, gap, margin, header = 110, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 28),
        "P01 Title Page Layout Comp — v07 vs v08",
        fill=(40, 30, 28),
        font=board_font(30),
    )
    draw.text(
        (margin, 68),
        "Cream page · art ~66% width upper-middle · Cormorant mock type · FRAME ON vignette · not final",
        fill=(90, 70, 60),
        font=board_font(15),
    )

    for i, (im, title, sub) in enumerate(
        [
            (left, "v07 — Winter Window LAYOUT", "Title above · window vignette · author + copyright below"),
            (right, "v08 — Writing Desk LAYOUT", "Same layout treatment for comparison"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        thumb = im.resize((panel, panel), Image.Resampling.LANCZOS)
        board.paste(thumb, (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(20))
        draw.text((x, y + panel + 44), sub, fill=(90, 70, 60), font=board_font(14))

    out = INDEX / "P01-title-v07-v08-layout-comp-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def write_recipe(ver: str, name: str, layout_path: Path) -> None:
    text = f"""# RECIPE — P01-title / {ver}-layout-comp

| Field | Value |
|-------|--------|
| **name** | {name} — title page layout comp |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | {ver}-layout-comp |
| **date** | {DAY} |
| **lane** | Pillow mock (Cormorant live-type preview) |
| **source art** | `Media/development/P01-title/{ver}/art.png` |
| **FRAME** | ON — soft vignette into cream page |
| **layout** | Art centered · ~66% page width · upper-middle |
| **type** | Cormorant Garamond Medium title · Italic author · Regular copyright |
| **script_text** | The Night I Met Santa / Written by Jack Farrell / First illustrated edition, 2026 / Book design by Jon Farrell |
| **output** | `{layout_path.relative_to(ROOT).as_posix()}` |
| **verdict** | pending |
| **status** | working · COMP only (not InDesign final) |
| **tier** | development |

## Notes

- Mock type for eye only — final live text in InDesign.
- v07 source had baked gibberish; soft cream scrub applied before layout.
- Sibling board: `Media/generated/mocks/_INDEX/P01-title-v07-v08-layout-comp-board.png`
"""
    out_dir = DEV / f"{ver}-layout-comp"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "RECIPE.md").write_text(text, encoding="utf-8")


def main() -> None:
    v07 = compose_title_page(DEV / "v07" / "art.png", scrub=True, label="v07 Winter Window")
    v08 = compose_title_page(DEV / "v08" / "art.png", scrub=False, label="v08 Writing Desk")

    out07 = DEV / "v07-layout-comp"
    out08 = DEV / "v08-layout-comp"
    out07.mkdir(parents=True, exist_ok=True)
    out08.mkdir(parents=True, exist_ok=True)
    p07 = out07 / "layout.png"
    p08 = out08 / "layout.png"
    v07.save(p07, "PNG")
    v08.save(p08, "PNG")
    write_recipe("v07", "Winter Window", p07)
    write_recipe("v08", "Writing Desk", p08)

    board = build_board(v07, v08)
    print(f"saved {p07}")
    print(f"saved {p08}")
    print(f"BOARD {board}")


if __name__ == "__main__":
    main()
