#!/usr/bin/env python3
"""P31 About-the-Author MOCKUP — Qwen 2 Pro /edit + Pillow typed preview.

Uses locked Jack portrait + style-lock-v2 + frame-reference (3-URL cap).
Art plate: NO baked text. Typed mock shows Draft About the Author + credits.
"""
from __future__ import annotations

import io
import os
import textwrap
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/generated/mocks/P-author-bio"
DEV = ROOT / "Media/development/P-author"
JACK = ROOT / "Media/approved/characters/jack-farrell-portrait.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
FRAME = ROOT / "Media/approved/style-refs/frame-reference.png"
EXISTING = ROOT / "Media/development/P-author/art.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
PAGE = 2625
CREAM = (252, 246, 238)
INK = (44, 44, 44)  # #2C2C2C

PROMPT = """\
About the Author page art for a children's Christmas picture book (single square plate).

IMAGE 1 = LOCKED Jack Farrell portrait — KEEP his exact face, smile, white swept-back hair,
cream cable-knit sweater, floral armchair, Christmas tree glow, mug on side table.
Do NOT change who he is. Preserve likeness carefully.

IMAGE 2 = style-lock paint atmosphere — rich gouache / soft watercolor heirloom storybook
paint quality (Santore-adjacent). Match this warmth and brush feel.

IMAGE 3 = cream watercolor FRAME language — soft irregular cream vignette dissolving at edges
(FRAME ON), like other matter pages in this book.

COMPOSITION for author BIO page mockup:
- Keep Jack portrait as the clear hero, seated warmly in the Christmas living room.
- Soft cream watercolor paper vignette on ALL sides (feathered painted edges).
- Leave a generous OPEN cream band in the LOWER third (and quiet margins) for later
  typography: page title, short author bio, and small credits — do NOT paint text.
- Calm, intimate, heirloom gift-book mood — not photoreal, not CGI.
- NO letters, NO words, NO watermark, NO logos, NO signature.

Output: square Christmas storybook illustration, FRAME ON, print-ready composition.
"""

NEG = (
    "text, letters, words, About the Author, Written by, watermark, logo, signature, "
    "photoreal photo, CGI, 3D render, wrong person, young face, heavy beard, "
    "brown age spots, hard rectangle crop, full-bleed edge with no cream vignette, "
    "Santa Claus, child in pajamas"
)

BIO_TITLE = "About the Author"
BIO_BODY = (
    "Jack Farrell is a father and grandfather who wrote The Night I Met Santa "
    "for the people he loves. His poem has been treasured by his family for years. "
    "This first illustrated edition (2026) was made so his words — and Santa's reminder "
    "to love Christmas, act like a kid, and keep faith — can stay close at hand every year."
)
CREDITS = "Written by Jack Farrell.  Design and produced by Jon Farrell  © DigitalStudioz 2026"


def load_env() -> None:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def download(url: str, tries: int = 4) -> Image.Image:
    last: Exception | None = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=180) as resp:
                return Image.open(io.BytesIO(resp.read())).convert("RGB")
        except Exception as e:  # noqa: BLE001
            last = e
            print("retry", i, e)
    assert last is not None
    raise last


def find_font(size: int, prefer: list[str]) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates: list[Path] = []
    pack = ROOT / "Xtraz" / "Fonts"
    if pack.is_dir():
        for p in pack.rglob("*.ttf"):
            candidates.append(p)
        for p in pack.rglob("*.otf"):
            candidates.append(p)
    win = Path(r"C:\Windows\Fonts")
    for name in prefer:
        candidates.append(win / name)
    for c in candidates:
        if c.is_file():
            try:
                return ImageFont.truetype(str(c), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def soft_cloud(size: tuple[int, int], opacity: int = 165) -> Image.Image:
    """Soft irregular translucent wash under MOCK type (layout north star)."""
    w, h = size
    cloud = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(cloud)
    # layered soft ellipses
    cream = (252, 246, 238, opacity)
    d.ellipse([-w // 8, -h // 10, w + w // 8, h + h // 6], fill=cream)
    d.ellipse([w // 10, h // 20, w - w // 10, h - h // 15], fill=(255, 252, 248, opacity - 20))
    return cloud.filter(ImageFilter.GaussianBlur(28))


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int],
    line_spacing: float = 1.35,
    align: str = "center",
) -> int:
    x0, y0, x1, y1 = box
    max_w = x1 - x0
    # estimate char width
    sample = font.getbbox("M")
    cw = max(8, sample[2] - sample[0])
    chars = max(20, int(max_w / (cw * 0.55)))
    lines = textwrap.wrap(text, width=chars)
    y = y0
    for line in lines:
        bb = font.getbbox(line)
        lw = bb[2] - bb[0]
        lh = bb[3] - bb[1]
        if align == "center":
            x = x0 + (max_w - lw) // 2
        else:
            x = x0
        draw.text((x, y), line, font=font, fill=fill)
        y += int(lh * line_spacing)
        if y > y1:
            break
    return y


def make_typed_mock(art: Image.Image, dest: Path) -> None:
    """Preview: portrait art + soft cloud + About the Author type (Cormorant-ish)."""
    im = art.convert("RGBA").resize((PAGE, PAGE), Image.Resampling.LANCZOS)
    # lower-third cloud for type
    cloud_h = int(PAGE * 0.42)
    cloud = soft_cloud((PAGE, cloud_h), opacity=175)
    layer = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    layer.paste(cloud, (0, PAGE - cloud_h - int(PAGE * 0.04)), cloud)
    composed = Image.alpha_composite(im, layer)

    draw = ImageDraw.Draw(composed)
    title_font = find_font(
        72,
        [
            "CinzelDecorative-Regular.ttf",
            "Cinzel-Regular.ttf",
            "georgia.ttf",
            "Georgia.ttf",
            "times.ttf",
        ],
    )
    body_font = find_font(
        42,
        [
            "CormorantGaramond-Medium.ttf",
            "CormorantGaramond-Regular.ttf",
            "EBGaramond-Medium.ttf",
            "georgia.ttf",
            "Georgia.ttf",
            "times.ttf",
        ],
    )
    credit_font = find_font(
        28,
        [
            "CormorantGaramond-Medium.ttf",
            "georgia.ttf",
            "Georgia.ttf",
            "times.ttf",
        ],
    )

    margin = int(PAGE * 0.12)
    y_title = PAGE - cloud_h + int(PAGE * 0.04)
    # Title
    tb = title_font.getbbox(BIO_TITLE)
    tw = tb[2] - tb[0]
    draw.text(((PAGE - tw) // 2, y_title), BIO_TITLE, font=title_font, fill=INK)

    y_body = y_title + int(PAGE * 0.055)
    y_after = draw_wrapped(
        draw,
        BIO_BODY,
        body_font,
        (margin, y_body, PAGE - margin, PAGE - int(PAGE * 0.10)),
        INK,
        line_spacing=1.45,
        align="center",
    )
    # Credits
    cb = credit_font.getbbox(CREDITS)
    # may need wrap
    y_cred = min(y_after + int(PAGE * 0.025), PAGE - int(PAGE * 0.07))
    draw_wrapped(
        draw,
        CREDITS,
        credit_font,
        (margin, y_cred, PAGE - margin, PAGE - int(PAGE * 0.04)),
        (70, 70, 70),
        line_spacing=1.3,
        align="center",
    )

    composed.convert("RGB").save(dest, "PNG")
    print("typed mock:", dest)


def write_recipe(ver: str, art_path: Path, seed: object) -> None:
    path = OUT / ver / "RECIPE.md"
    path.write_text(
        f"""# RECIPE — P-author-bio / {ver}

| Field | Value |
|-------|--------|
| **name** | About the Author — Qwen 2 Pro mockup (portrait + open cream for bio) |
| **unit** | P-author-bio |
| **book page** | 31 · Author (bio mockup test) |
| **page role** | `single` |
| **version** | {ver} |
| **date** | 2026-07-23 |
| **lane** | Development mock — **Qwen 2 Pro /edit ONLY** |
| **service** | fal.ai |
| **model** | `{QWEN}` |
| **settings** | 2048² edit → resize 2625² · FRAME ON · no baked text |
| **FRAME** | ON |
| **concept** | Author bio page look-test using locked Jack + style-lock + frame language |
| **changes** | Fresh mock for Jon walk review — does not replace FLOW locked `P-author/art.png` |
| **size** | 2625×2625 |
| **seed** | {seed} |
| **output** | art.png · art-MOCK-TYPE.png |
| **script_text** | About the Author · bio Draft · credits (MOCK only) |
| **type_zone** | Lower cream band |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- `Media/approved/characters/jack-farrell-portrait.png` (LOCKED)
- `Media/approved/style-refs/style-lock-v2.png`
- `Media/approved/style-refs/frame-reference.png`

## Prompt

{PROMPT}

## Negative

{NEG}

## Copy used on MOCK-TYPE (not baked into art.png)

**Title:** {BIO_TITLE}

**Body (BOOK-COPY-DRAFTS About the Author):**
{BIO_BODY}

**Credits (Flow p31):**
{CREDITS}

## Notes

- Flow still lists p31 as portrait-led image page; this mock tests bio+credits overlay look.
- Live type in InDesign later — MOCK is preview only.
- Approved Jack source untouched.
""",
        encoding="utf-8",
    )


def main() -> None:
    load_env()
    OUT.mkdir(parents=True, exist_ok=True)
    ver = "v01"
    ver_dir = OUT / ver
    ver_dir.mkdir(parents=True, exist_ok=True)

    for p in (JACK, STYLE, FRAME):
        if not p.is_file():
            raise SystemExit(f"missing ref: {p}")

    # Prep square refs @ ~2K for Qwen
    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)
    refs = []
    for src, name in ((JACK, "jack.png"), (STYLE, "style.png"), (FRAME, "frame.png")):
        im = Image.open(src).convert("RGB")
        # contain into square cream for frame ref if wide
        side = 1536
        canvas = Image.new("RGB", (side, side), CREAM)
        scale = min(side / im.width, side / im.height)
        nw, nh = int(im.width * scale), int(im.height * scale)
        im2 = im.resize((nw, nh), Image.Resampling.LANCZOS)
        canvas.paste(im2, ((side - nw) // 2, (side - nh) // 2))
        dest = tmp / name
        canvas.save(dest)
        refs.append(dest)

    urls = [fal_client.upload_file(str(p)) for p in refs]
    print("=== Qwen 2 Pro /edit — About the Author mockup ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": urls,
            "image_size": {"width": 2048, "height": 2048},
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checker": True,
            "enable_prompt_expansion": False,
        },
        with_logs=True,
    )
    seed = result.get("seed")
    art = download(result["images"][0]["url"]).resize((PAGE, PAGE), Image.Resampling.LANCZOS)
    art_path = ver_dir / "art.png"
    art.save(art_path, "PNG")
    print("art:", art_path, art.size)

    mock_path = ver_dir / "art-MOCK-TYPE.png"
    make_typed_mock(art, mock_path)

    # Also typed mock on CURRENT locked framed plate for A/B
    if EXISTING.is_file():
        make_typed_mock(
            Image.open(EXISTING),
            ver_dir / "art-MOCK-TYPE-on-locked-framed.png",
        )

    write_recipe(ver, art_path, seed)

    # Convenience copies for quick open
    preview = OUT / "_INDEX"
    preview.mkdir(exist_ok=True)
    art.save(preview / "author-bio-art.png")
    Image.open(mock_path).save(preview / "author-bio-MOCK-TYPE.png")
    print("DONE — open", mock_path)


if __name__ == "__main__":
    main()
