#!/usr/bin/env python3
"""Text mocks v3 — Jon mockup direction: soft paint fades, never cover faces.

Policy: .cursor/docs/TEXT-OVERLAY-POLICY.md
Refs: Images/references/layout/ref-text-jon-*.png
Out: Media/generated/test-batch-v3/text-mocks-v3/
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "Media" / "generated" / "test-batch-v3"
OUT = BATCH / "text-mocks-v3"
PAGE = 2625
SAFE = 200
WHITE = (255, 250, 242)
INK_DARK = (30, 24, 18)
INK_LIGHT = (255, 248, 240)

FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 108)
FONT_POEM = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 86)

RECIPES = [
    {
        "id": "01-eyes-left-SOFT-FADE",
        "art": "p10-beat04-eyes-met-LEFT.png",
        "wash": "side-bleed-left",
        "zone": "left",
        "ink": "dark",
        "lines": [
            "My jaw dropped",
            "when our eyes",
            "finally met.",
            "I knew right then",
            "it was a moment",
            "I would never",
            "forget.",
        ],
    },
    {
        "id": "02-eyes-right-BOTTOM-RIGHT",
        "art": "p11-beat04-eyes-met-RIGHT.png",
        "wash": "corner-br",  # from bottom-right toward Santa — not over face
        "zone": "br",
        "ink": "dark",
        "lines": [
            "For there he was",
            "in all his",
            "splendor,",
            "brilliant white",
            "hair,",
            "red coat with",
            "suspenders.",
        ],
    },
    {
        "id": "03-sneak-SIDE-BLEED",
        "art": "p07-beat01-the-sneak.png",
        "wash": "side-bleed-left",
        "zone": "left",
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
        "id": "07-note-LOWER-SOFT",
        "art": "p21-beat12-13-note-LEFT.png",
        "wash": "corner-bl",  # lower, soft — not mid-window
        "zone": "bl",
        "ink": "dark",
        "lines": [
            "It wasn't a shoe,",
            "hat or a coat.",
            "I couldn't believe it,",
            "the old guy.",
            "He left me a note.",
        ],
    },
    {
        "id": "05-thank-you-SIDE-BLEED",
        "art": "p27-thank-you.png",
        "wash": "side-bleed-left",
        "zone": "left",
        "ink": "dark",
        "title": "Thank You",
        "lines": [
            "Thank you to my family",
            "and loved ones —",
            "for keeping this poem,",
            "for believing in Christmas.",
            "",
            "God bless.",
            "— Jack Farrell",
        ],
    },
]


def fit_square(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    if im.size != (PAGE, PAGE):
        s = max(PAGE / im.width, PAGE / im.height)
        nw, nh = int(im.width * s), int(im.height * s)
        im = im.resize((nw, nh), Image.LANCZOS)
        l = (nw - PAGE) // 2
        t = (nh - PAGE) // 2
        im = im.crop((l, t, l + PAGE, t + PAGE))
    return im


def wrap_lines(lines, font, max_w):
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
    lh = int(font.size * 1.28)
    max_w = 0
    for line in lines:
        if line:
            bb = d.textbbox((0, 0), line, font=font)
            max_w = max(max_w, bb[2] - bb[0])
    th = 0
    if title:
        bb = d.textbbox((0, 0), title, font=FONT_TITLE)
        max_w = max(max_w, bb[2] - bb[0])
        th = int(FONT_TITLE.size * 1.45)
    return max_w + 20, th + len(lines) * lh + 30, lh, th


def place(zone, tw, th):
    if zone == "left":
        return SAFE + 50, SAFE + 160
    if zone == "br":
        return PAGE - tw - SAFE - 40, PAGE - th - SAFE - 60
    if zone == "bl":
        return SAFE + 60, PAGE - th - SAFE - 80
    return SAFE, SAFE


def paint_swipes(alpha_img: Image.Image, region: tuple[int, int, int, int], strength=110) -> Image.Image:
    """Faint elongated brush-swipe texture into an alpha mask."""
    from PIL import ImageChops
    x0, y0, x1, y1 = region
    swipe = Image.new("L", (PAGE, PAGE), 0)
    sd = ImageDraw.Draw(swipe)
    w, h = x1 - x0, y1 - y0
    for i in range(5):
        cx = x0 + int(w * (0.15 + 0.18 * i))
        cy = y0 + int(h * (0.2 + 0.15 * (i % 3)))
        rw = int(w * 0.55)
        rh = int(h * 0.22)
        sd.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=strength)
    swipe = swipe.filter(ImageFilter.GaussianBlur(radius=48))
    return ImageChops.lighter(alpha_img, swipe)


def text_soft_glow(base: Image.Image, x: int, y: int, tw: int, th: int, pad=160) -> Image.Image:
    """Subtle soft white behind text — readable but not an opaque panel.
    Strong fade-out; faint paint swipes. (Jon: prior version too overpowering.)"""
    out = base.convert("RGBA")
    gx0 = max(0, x - pad)
    gy0 = max(0, y - pad)
    gx1 = min(PAGE, x + tw + pad)
    gy1 = min(PAGE, y + th + pad)
    cx, cy = (gx0 + gx1) // 2, (gy0 + gy1) // 2
    gw, gh = gx1 - gx0, gy1 - gy0

    alpha = Image.new("L", (PAGE, PAGE), 0)
    ad = ImageDraw.Draw(alpha)
    # Softer core (~mid opacity paper, not solid white sheet)
    ad.ellipse([cx - gw // 2, cy - gh // 2, cx + gw // 2, cy + gh // 2], fill=165)
    ad.ellipse([gx0 + 40, gy0 + gh // 6, gx1 - 40, gy1 - gh // 6], fill=140)
    alpha = paint_swipes(alpha, (gx0, gy0, gx1, gy1), strength=70)
    # Larger blur = longer, nicer fade into art
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius=95))
    # Mild boost only — keep fade-out; don’t reinflate to solid white
    alpha = alpha.point(lambda v: min(200, int(v * 1.15)) if v > 10 else v)

    glow = Image.new("RGBA", (PAGE, PAGE), (*WHITE, 255))
    glow.putalpha(alpha)
    return Image.alpha_composite(out, glow)


def side_bleed_left(base: Image.Image, solid_frac=0.40, fade_frac=0.30) -> Image.Image:
    """Jon sneak mockup: solid left paper → long soft paint fade into art."""
    out = base.convert("RGBA")
    overlay = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    solid_w = int(PAGE * solid_frac)
    fade_w = int(PAGE * fade_frac)
    total = solid_w + fade_w
    for i in range(total):
        if i < solid_w:
            a = 255
        else:
            t = (i - solid_w) / max(1, fade_w)
            a = int(255 * (1 - t) ** 1.8)
        od.line([(i, 0), (i, PAGE)], fill=(*WHITE, a))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=42))
    swipe = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(swipe)
    for k, y0 in enumerate(range(100, PAGE, 240)):
        x0 = solid_w - 100 + (k % 3) * 35
        sd.ellipse([x0, y0, x0 + fade_w + 260, y0 + 150], fill=(*WHITE, 100))
    swipe = swipe.filter(ImageFilter.GaussianBlur(radius=55))
    overlay = Image.alpha_composite(overlay, swipe)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=14))
    return Image.alpha_composite(out, overlay)


def corner_gradient(base: Image.Image, corner: str, radius=2100, core=0.42) -> Image.Image:
    """Smooth radial paint from a corner — larger so it reaches full text stacks."""
    from PIL import ImageChops
    out = base.convert("RGBA")
    if corner == "br":
        ox, oy = PAGE - 1, PAGE - 1
    elif corner == "bl":
        ox, oy = 0, PAGE - 1
    elif corner == "tl":
        ox, oy = 0, 0
    else:
        ox, oy = PAGE - 1, 0

    step = 3
    small_w = PAGE // step
    small_h = PAGE // step
    alpha = Image.new("L", (small_w, small_h), 0)
    ap = alpha.load()
    sox, soy = ox / step, oy / step
    r = radius / step
    core_r = r * core
    for y in range(small_h):
        for x in range(small_w):
            d = math.hypot(x - sox, y - soy)
            if d <= core_r:
                a = 255
            elif d >= r:
                a = 0
            else:
                t = (d - core_r) / (r - core_r)
                a = int(255 * (1 - t) ** 1.85)
            ap[x, y] = a
    alpha = alpha.resize((PAGE, PAGE), Image.BILINEAR)
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius=60))
    swipe = Image.new("L", (PAGE, PAGE), 0)
    sd = ImageDraw.Draw(swipe)
    if corner == "br":
        pts = [(PAGE - 180, PAGE - 80), (PAGE - 1000, PAGE - 420), (PAGE - 620, PAGE - 980), (PAGE - 400, PAGE - 700)]
    else:
        pts = [(180, PAGE - 80), (1000, PAGE - 400), (520, PAGE - 920), (380, PAGE - 650)]
    for cx, cy in pts:
        sd.ellipse([cx - 420, cy - 180, cx + 420, cy + 180], fill=150)
    swipe = swipe.filter(ImageFilter.GaussianBlur(radius=75))
    alpha = ImageChops.lighter(alpha, swipe)

    color = Image.new("RGBA", (PAGE, PAGE), (*WHITE, 255))
    color.putalpha(alpha)
    return Image.alpha_composite(out, color)


def draw_text(img, lines, x, y, lh, font, ink, title=None, title_h=0):
    d = ImageDraw.Draw(img)
    ty = y
    if title:
        d.text((x, ty), title, fill=ink, font=FONT_TITLE)
        ty += title_h
    for line in lines:
        if line == "":
            ty += int(lh * 0.5)
            continue
        d.text((x, ty), line, fill=ink, font=font)
        ty += lh
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for r in RECIPES:
        art = BATCH / r["art"]
        if not art.exists():
            print("SKIP", r["art"])
            continue
        base = fit_square(art)
        font = FONT_POEM
        max_w = int(PAGE * 0.36) if r["zone"] == "left" else int(PAGE * 0.42)
        lines = wrap_lines(r["lines"], font, max_w)
        title = r.get("title")
        tw, th, lh, title_h = measure(lines, font, title)
        tw = min(tw, max_w + 40)
        x, y = place(r["zone"], tw, th)

        wash = r["wash"]
        if wash == "side-bleed-left":
            composed = side_bleed_left(base)
        elif wash == "corner-br":
            composed = corner_gradient(base, "br")
        elif wash == "corner-bl":
            composed = corner_gradient(base, "bl", radius=2000)
        else:
            composed = base.convert("RGBA")

        # Always seat text on a soft glow sized to the block (fixes short gradients)
        composed = text_soft_glow(composed, x, y, tw, th, pad=160)

        ink = INK_LIGHT if r["ink"] == "light" else INK_DARK
        composed = draw_text(composed, lines, x, y, lh, font, ink, title, title_h)
        out = OUT / f"{r['id']}.jpg"
        composed.convert("RGB").save(out, "JPEG", quality=93)
        print("OK", out.name)

    (OUT / "README.txt").write_text(
        "text-mocks-v3 matching Jon soft-fade / side-bleed refs.\n"
        "Never cover faces. Soft paint fades only.\n"
        "See TEXT-OVERLAY-POLICY.md\n",
        encoding="utf-8",
    )
    print("Done ->", OUT)


if __name__ == "__main__":
    main()
