#!/usr/bin/env python3
"""Mock poem pages + alternate white-blend / cloud text integrations for test-batch-v3."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "Media" / "generated" / "test-batch-v3"
MOCK = BATCH / "text-mocks"
WASH = BATCH / "wash-variants"
PAGE = 2625
SAFE = 190

try:
    FONT = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 48)
    FONT_SM = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 36)
    FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 64)
except OSError:
    FONT = ImageFont.load_default()
    FONT_SM = FONT
    FONT_TITLE = FONT

# Sample poem blocks for mocks (from poem-clean.txt)
SAMPLES = [
    {
        "art": "p07-beat01-the-sneak.png",
        "pos": "bl",
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
        "art": "p10-beat04-eyes-met-LEFT.png",
        "pos": "bl",
        "lines": [
            "My jaw dropped",
            "when our eyes finally met.",
            "I knew right then,",
            "it was a moment",
            "I would never forget.",
        ],
    },
    {
        "art": "p11-beat04-eyes-met-RIGHT.png",
        "pos": "br",
        "lines": [
            "For there he was",
            "in all his splendor,",
            "brilliant white hair,",
            "red coat with suspenders.",
        ],
    },
    {
        "art": "p16-beat07-cocoa.png",
        "pos": "tl",
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
        "art": "p21-beat12-13-note-LEFT.png",
        "pos": "bl",
        "lines": [
            "It wasn't a shoe,",
            "hat or a coat.",
            "I couldn't believe it,",
            "the old guy.",
            "He left me a note.",
        ],
    },
    {
        "art": "p27-thank-you.png",
        "pos": "center",
        "lines": [
            "Thank You",
            "",
            "Thank you to my family",
            "and loved ones —",
            "for keeping this poem,",
            "for believing in Christmas.",
            "",
            "God bless.",
            "— Jack Farrell",
        ],
        "matter": True,
    },
]


def measure(lines, font):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lh = 56
    max_w = 0
    for line in lines:
        if line:
            bb = d.textbbox((0, 0), line, font=font)
            max_w = max(max_w, bb[2] - bb[0])
    h = len(lines) * lh + 50
    return max_w + 90, h, lh


def place(pos, tw, th):
    m = SAFE
    if pos == "bl":
        return m, PAGE - th - m
    if pos == "br":
        return PAGE - tw - m, PAGE - th - m
    if pos == "tl":
        return m, m
    if pos == "tr":
        return PAGE - tw - m, m
    if pos == "bc":
        return (PAGE - tw) // 2, PAGE - th - m
    # center
    return (PAGE - tw) // 2, (PAGE - th) // 2


def wash_rect_soft(base: Image.Image, x, y, w, h, cream=(252, 248, 240), feather=130, peak=200):
    """v5-style soft rectangle (legacy compare)."""
    out = base.convert("RGBA")
    for i in range(28):
        a = int(peak * (1 - i / 28))
        exp = int(feather * i / 28)
        ov = Image.new("RGBA", (w + 2 * exp, h + 2 * exp), (0, 0, 0, 0))
        ImageDraw.Draw(ov).rectangle([0, 0, w + 2 * exp - 1, h + 2 * exp - 1], fill=(*cream, a))
        out.paste(ov, (x - exp, y - exp), ov)
    return out


def wash_ellipse_cloud(base: Image.Image, x, y, w, h, cream=(252, 248, 240), peak=195):
    """Irregular multi-ellipse cloud (organic)."""
    out = base.convert("RGBA")
    overlay = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    rng = random.Random(42)
    # Base big ellipse
    blobs = [(x + w // 2, y + h // 2, int(w * 0.72), int(h * 0.62))]
    for _ in range(7):
        cx = x + rng.randint(w // 8, 7 * w // 8)
        cy = y + rng.randint(h // 8, 7 * h // 8)
        rw = rng.randint(w // 3, int(w * 0.55))
        rh = rng.randint(h // 3, int(h * 0.55))
        blobs.append((cx, cy, rw, rh))
    for cx, cy, rw, rh in blobs:
        layer = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(*cream, peak))
        layer = layer.filter(ImageFilter.GaussianBlur(radius=55))
        overlay = Image.alpha_composite(overlay, layer)
    # soften whole
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=8))
    return Image.alpha_composite(out, overlay)


def wash_side_bleed(base: Image.Image, side="left", cream=(252, 248, 240), width=980, peak=210):
    """Paper bleeding in from left or right (layout ref B)."""
    out = base.convert("RGBA")
    overlay = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    if side == "left":
        for i in range(width):
            t = i / width
            a = int(peak * (1 - t) ** 1.6)
            od.line([(i, 0), (i, PAGE)], fill=(*cream, a))
    else:
        for i in range(width):
            t = i / width
            a = int(peak * (1 - t) ** 1.6)
            x = PAGE - 1 - i
            od.line([(x, 0), (x, PAGE)], fill=(*cream, a))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=18))
    return Image.alpha_composite(out, overlay)


def wash_bottom_mist(base: Image.Image, height=900, cream=(252, 248, 240), peak=200):
    """Snow/mist rising from bottom."""
    out = base.convert("RGBA")
    overlay = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    y0 = PAGE - height
    for y in range(height):
        t = y / height
        a = int(peak * (t ** 1.35))
        od.line([(0, y0 + y), (PAGE, y0 + y)], fill=(*cream, a))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=22))
    return Image.alpha_composite(out, overlay)


def wash_snow_panel(base: Image.Image, x, y, w, h):
    """Bright soft snow field with scalloped top edge."""
    out = base.convert("RGBA")
    overlay = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    cream = (255, 252, 245)
    # scalloped top
    points = [(x - 40, y + h + 40), (x - 40, y + 40)]
    steps = 12
    for i in range(steps + 1):
        px = x + int(w * i / steps)
        wave = int(36 * math.sin(i * 0.9))
        points.append((px, y + 30 + wave))
    points += [(x + w + 40, y + 40), (x + w + 40, y + h + 40)]
    od.polygon(points, fill=(*cream, 200))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=28))
    return Image.alpha_composite(out, overlay)


def draw_text(img: Image.Image, lines, x, y, lh, font, fill=(26, 26, 26)):
    d = ImageDraw.Draw(img)
    ty = y + 28
    tx = x + 40
    for line in lines:
        if line == "":
            ty += 28
            continue
        # title-ish first line if short heading
        f = FONT_TITLE if (line in ("Thank You", "About This Story") and ty < y + 100) else font
        d.text((tx, ty), line, fill=fill, font=f)
        ty += lh if f == font else lh + 10
    return img


def fit_square(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    if im.size != (PAGE, PAGE):
        # cover crop
        s = max(PAGE / im.width, PAGE / im.height)
        nw, nh = int(im.width * s), int(im.height * s)
        im = im.resize((nw, nh), Image.LANCZOS)
        left = (nw - PAGE) // 2
        top = (nh - PAGE) // 2
        im = im.crop((left, top, left + PAGE, top + PAGE))
    return im


def main():
    MOCK.mkdir(parents=True, exist_ok=True)
    WASH.mkdir(parents=True, exist_ok=True)
    random.seed(7)

    # --- Wash variants on one hero sneak page ---
    sneak = BATCH / "p07-beat01-the-sneak.png"
    if sneak.exists():
        base = fit_square(sneak)
        tw, th, lh = measure(SAMPLES[0]["lines"], FONT)
        x, y = place("bl", tw, th)
        variants = {
            "wash-A-soft-rect": lambda b: wash_rect_soft(b, x, y, tw, th),
            "wash-B-ellipse-cloud": lambda b: wash_ellipse_cloud(b, x, y, tw, th),
            "wash-C-bottom-mist": lambda b: wash_bottom_mist(b),
            "wash-D-side-bleed-left": lambda b: wash_side_bleed(b, "left"),
            "wash-E-snow-panel": lambda b: wash_snow_panel(b, x - 20, y - 20, tw + 40, th + 40),
        }
        for name, fn in variants.items():
            composed = fn(base.copy())
            # text position: mist/side use custom
            if "bottom-mist" in name:
                tx, ty = place("bc", tw, th)
            elif "side-bleed" in name:
                tx, ty = SAFE + 40, SAFE + 80
            else:
                tx, ty = x, y
            composed = draw_text(composed, SAMPLES[0]["lines"], tx, ty, lh, FONT)
            out = WASH / f"{name}.png"
            composed.convert("RGB").save(out, "PNG")
            print("WASH", out.name)
    else:
        print("SKIP wash variants — sneak art missing")

    # --- Full mock pages ---
    for i, sample in enumerate(SAMPLES, 1):
        art = BATCH / sample["art"]
        if not art.exists():
            print("SKIP mock — missing", sample["art"])
            continue
        base = fit_square(art)
        lines = sample["lines"]
        font = FONT_SM if sample.get("matter") else FONT
        tw, th, lh = measure(lines, font)
        pos = sample["pos"]
        x, y = place(pos, tw, th)
        # default mock uses organic cloud
        if pos == "center":
            composed = wash_ellipse_cloud(base, x, y, tw, th, peak=210)
        else:
            composed = wash_ellipse_cloud(base, x, y, tw, th)
        composed = draw_text(composed, lines, x, y, lh, font)
        out = MOCK / f"mock-{i:02d}-{art.stem}.jpg"
        composed.convert("RGB").save(out, "JPEG", quality=92)
        print("MOCK", out.name)

    print("Done mocks + wash variants")


if __name__ == "__main__":
    main()
