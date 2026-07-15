#!/usr/bin/env python3
"""Improved text mocks — open-zone first, white-paint wash (not gray blobs), large title-ish serif.

Policy: .cursor/docs/TEXT-OVERLAY-POLICY.md
Output: Media/generated/test-batch-v3/text-mocks-v2/
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
import math

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "Media" / "generated" / "test-batch-v3"
OUT = BATCH / "text-mocks-v2"
PAGE = 2625
SAFE = 200

# Cover-adjacent display serif, but flat (not gold) — try several Windows fonts
def load_fonts():
    candidates = [
        ("C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/georgia.ttf"),
        ("C:/Windows/Fonts/Palatino Linotype Bold.ttf", "C:/Windows/Fonts/pala.ttf"),
        ("C:/Windows/Fonts/timesbd.ttf", "C:/Windows/Fonts/times.ttf"),
    ]
    for bold, reg in candidates:
        try:
            return (
                ImageFont.truetype(bold, 96),   # matter title
                ImageFont.truetype(bold, 78),   # poem display
                ImageFont.truetype(reg, 72),    # poem body
            )
        except OSError:
            continue
    f = ImageFont.load_default()
    return f, f, f


FONT_TITLE, FONT_POEM_B, FONT_POEM = load_fonts()
# Override sizes — picture-book body, not captions
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 110)
FONT_POEM_B = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 92)
FONT_POEM = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 86)

INK_DARK = (26, 22, 18)
INK_LIGHT = (255, 248, 240)
WHITE_PAINT = (255, 250, 242)

# Page recipes: open zones first (Jon feedback)
RECIPES = [
    {
        "id": "01-eyes-left-OPEN-WALL",
        "art": "p10-beat04-eyes-met-LEFT.png",
        "zone": "left-wall",  # entire wall left of fireplace
        "wash": "none",  # wall is already open cream
        "ink": "dark",
        "lines": [
            "My jaw dropped",
            "when our eyes finally met.",
            "I knew right then,",
            "it was a moment",
            "I would never forget.",
        ],
    },
    {
        "id": "02-eyes-right-OPEN-WALL",
        "art": "p11-beat04-eyes-met-RIGHT.png",
        "zone": "left-wall",  # quiet wall beside Santa / not on gifts
        "wash": "white-paint",  # mid wall may need soft paint
        "ink": "dark",
        "lines": [
            "For there he was",
            "in all his splendor,",
            "brilliant white hair,",
            "red coat with suspenders.",
        ],
    },
    {
        "id": "03-sneak-SIDE-BLEED",
        "art": "p07-beat01-the-sneak.png",
        "zone": "left-panel",
        "wash": "side-bleed-left",
        "ink": "dark",
        "lines": [
            "I searched and I peeked",
            "when I first heard the noise.",
            "Something or someone",
            "was in with the toys.",
            "",
            "I slithered and crawled",
            "for a peek of a glimpse.",
            "It must be some fairies",
            "or holiday imps.",
        ],
    },
    {
        "id": "04-sneak-DARK-WALL-LIGHT-INK",
        "art": "p07-beat01-the-sneak.png",
        "zone": "left-dark-wall",  # maroon hall wall — light ink, no gray blob
        "wash": "none",
        "ink": "light",
        "lines": [
            "I searched and I peeked",
            "when I first heard the noise.",
            "Something or someone",
            "was in with the toys.",
            "",
            "I slithered and crawled",
            "for a peek of a glimpse.",
            "It must be some fairies",
            "or holiday imps.",
        ],
    },
    {
        "id": "05-thank-you-OPEN-WALL",
        "art": "p27-thank-you.png",
        "zone": "left-wall",
        "wash": "white-paint",
        "ink": "dark",
        "title": "Thank You",
        "lines": [
            "Thank you to my family",
            "and loved ones —",
            "for keeping this poem,",
            "for believing in Christmas,",
            "and for sitting still long enough",
            "to hear a story about",
            "the night I met Santa.",
            "",
            "God bless.",
            "— Jack Farrell",
        ],
    },
    {
        "id": "06-cocoa-BOTTOM-MIST",
        "art": "p16-beat07-cocoa.png",
        "zone": "bottom",
        "wash": "bottom-mist",
        "ink": "dark",
        "lines": [
            "He spoke of many places,",
            "people and things.",
            "From toys to music",
            "to bright diamond rings.",
            "",
            "He even revealed his passion",
            "for hot cocoa",
            "instead of cold milk.",
        ],
    },
    {
        "id": "07-note-WHITE-PAINT",
        "art": "p21-beat12-13-note-LEFT.png",
        "zone": "left-panel",
        "wash": "white-paint",
        "ink": "dark",
        "lines": [
            "It wasn't a shoe,",
            "hat or a coat.",
            "I couldn't believe it,",
            "the old guy.",
            "He left me a note.",
        ],
    },
]


def fit_square(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    if im.size != (PAGE, PAGE):
        s = max(PAGE / im.width, PAGE / im.height)
        nw, nh = int(im.width * s), int(im.height * s)
        im = im.resize((nw, nh), Image.LANCZOS)
        left = (nw - PAGE) // 2
        top = (nh - PAGE) // 2
        im = im.crop((left, top, left + PAGE, top + PAGE))
    return im


def wrap_lines(lines, font, max_w):
    """Soft-wrap long lines so text stays inside the open zone width."""
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    out = []
    for line in lines:
        if line == "":
            out.append("")
            continue
        bb = d.textbbox((0, 0), line, font=font)
        if bb[2] - bb[0] <= max_w:
            out.append(line)
            continue
        words = line.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            tb = d.textbbox((0, 0), trial, font=font)
            if tb[2] - tb[0] <= max_w:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out


def measure(lines, font, title=None):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lh = int(getattr(font, "size", 86) * 1.28)
    max_w = 0
    for line in lines:
        if line:
            bb = d.textbbox((0, 0), line, font=font)
            max_w = max(max_w, bb[2] - bb[0])
    title_h = 0
    if title:
        bb = d.textbbox((0, 0), title, font=FONT_TITLE)
        max_w = max(max_w, bb[2] - bb[0])
        title_h = int(FONT_TITLE.size * 1.5)
    h = title_h + len(lines) * lh + 40
    return max_w + 40, h, lh, title_h


def zone_box(zone: str, tw: int, th: int):
    """Return top-left for text block inside open design area."""
    if zone == "left-wall":
        # Sit IN the open wall left of fireplace — upper third, not on gifts
        x = SAFE + 60
        y = SAFE + 180
        return x, y
    if zone == "left-panel":
        x = SAFE + 40
        y = SAFE + 160
        return x, y
    if zone == "left-dark-wall":
        x = SAFE + 50
        y = SAFE + 220
        return x, y
    if zone == "bottom":
        x = max(SAFE, (PAGE - tw) // 2)
        y = PAGE - th - SAFE - 20
        return x, y
    return SAFE, SAFE


def white_paint_wash(base: Image.Image, x, y, w, h) -> Image.Image:
    """Nearly opaque warm white paint with soft painterly fade — NOT gray mud."""
    out = base.convert("RGBA")
    overlay = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    pad = 90
    cx, cy = x + w // 2, y + h // 2
    rw, rh = int(w * 0.62) + pad, int(h * 0.62) + pad
    layer = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(*WHITE_PAINT, 255))
    for dx, dy, s in [(-0.32, -0.18, 0.75), (0.38, 0.12, 0.7), (-0.08, 0.38, 0.6), (0.18, -0.32, 0.65)]:
        lx = int(cx + dx * w)
        ly = int(cy + dy * h)
        lr = int(rw * s)
        lh = int(rh * s)
        ld.ellipse([lx - lr, ly - lh, lx + lr, ly + lh], fill=(*WHITE_PAINT, 255))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=52))
    # Reinstate opacity lost to blur (prevents gray mud)
    r, g, b, a = layer.split()
    a = a.point(lambda v: min(255, int(v * 1.45)) if v > 8 else v)
    layer = Image.merge("RGBA", (r.point(lambda _: WHITE_PAINT[0]),
                                 g.point(lambda _: WHITE_PAINT[1]),
                                 b.point(lambda _: WHITE_PAINT[2]), a))
    overlay = Image.alpha_composite(overlay, layer)
    return Image.alpha_composite(out, overlay)


def side_bleed_left(base: Image.Image, width=1200, peak=255) -> Image.Image:
    """White paint bleeding from left — solid paper on left, soft fade."""
    out = base.convert("RGBA")
    overlay = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(width):
        t = i / width
        if t < 0.42:
            a = peak
        else:
            a = int(peak * ((1 - (t - 0.42) / 0.58) ** 1.5))
        od.line([(i, 0), (i, PAGE)], fill=(*WHITE_PAINT, a))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=28))
    return Image.alpha_composite(out, overlay)


def bottom_mist(base: Image.Image, height=1100, peak=255) -> Image.Image:
    """White paint mist from bottom — solid near footer, soft fade up."""
    out = base.convert("RGBA")
    overlay = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    y0 = PAGE - height
    for y in range(height):
        t = y / height
        if t > 0.55:
            a = peak
        else:
            a = int(peak * ((t / 0.55) ** 1.4))
        od.line([(0, y0 + y), (PAGE, y0 + y)], fill=(*WHITE_PAINT, a))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=30))
    return Image.alpha_composite(out, overlay)


def draw_text(img: Image.Image, lines, x, y, lh, font, ink, title=None, title_h=0):
    d = ImageDraw.Draw(img)
    ty = y
    if title:
        d.text((x, ty), title, fill=ink, font=FONT_TITLE)
        ty += title_h
    for line in lines:
        if line == "":
            ty += int(lh * 0.55)
            continue
        d.text((x, ty), line, fill=ink, font=font)
        ty += lh
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for r in RECIPES:
        art = BATCH / r["art"]
        if not art.exists():
            print("SKIP missing", r["art"])
            continue
        base = fit_square(art)
        title = r.get("title")
        font = FONT_POEM_B if not title else FONT_POEM
        # Keep copy inside open wall (~38% page) so it never rides onto fireplace/gifts
        zone_max = int(PAGE * 0.38) if "left" in r["zone"] else int(PAGE * 0.72)
        lines = wrap_lines(r["lines"], font, zone_max - 80)
        tw, th, lh, title_h = measure(lines, font, title)
        tw = min(tw, zone_max)
        x, y = zone_box(r["zone"], tw, th)

        wash = r["wash"]
        if wash == "white-paint":
            composed = white_paint_wash(base, x, y, tw, th)
        elif wash == "side-bleed-left":
            composed = side_bleed_left(base)
        elif wash == "bottom-mist":
            composed = bottom_mist(base)
        else:
            composed = base.convert("RGBA")

        ink = INK_LIGHT if r["ink"] == "light" else INK_DARK
        composed = draw_text(composed, lines, x, y, lh, font, ink, title, title_h)
        out = OUT / f"{r['id']}.jpg"
        composed.convert("RGB").save(out, "JPEG", quality=93)
        print("OK", out.name, f"zone={r['zone']} wash={wash} ink={r['ink']}")

    # Also: 1 clean “compare” strip note
    note = OUT / "README.txt"
    note.write_text(
        "text-mocks-v2 — open design zones + white paint / side bleed / bottom mist\n"
        "See .cursor/docs/TEXT-OVERLAY-POLICY.md\n"
        "REJECTED: gray clouds, soft rectangles, tiny caption type\n",
        encoding="utf-8",
    )
    print("Done ->", OUT)


if __name__ == "__main__":
    main()
