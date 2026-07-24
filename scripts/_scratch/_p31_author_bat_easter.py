#!/usr/bin/env python3
"""P-author-bio v03 — subtle baseball bat + ribbon Easter egg behind Jack."""
from __future__ import annotations

import io
import os
import textwrap
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/generated/mocks/P-author-bio/v03"
JACK = ROOT / "Media/approved/characters/jack-farrell-portrait.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
PAGE = 2625
CREAM = (252, 246, 238)
INK = (44, 44, 44)

PROMPT = """\
Edit this Christmas storybook author portrait carefully.

KEEP everything important identical:
- Same elderly man Jack Farrell — exact face, smile, white swept-back hair, cream cable-knit sweater
- Same floral armchair pose, hands in lap
- Same glowing Christmas tree on the LEFT with ornaments and warm lights
- Same cozy living-room mood, soft gouache/watercolor storybook paint
- Soft cream watercolor vignette edges (FRAME ON)

ADD only one subtle Easter egg:
In the BACK CORNER behind the man — to the RIGHT of the Christmas tree / behind the chair —
lean a wooden baseball bat quietly against the wall or in the shadowed corner.
Put a soft festive ribbon (red or deep green with a small bow) tied around the bat handle or mid-bat.
The bat should feel like a quiet gift detail — small in the frame, partially shadowed, NOT a hero prop.
Do NOT make the bat huge. Do NOT put it in the foreground. Do NOT cover his face or hands.

NO text, NO letters, NO watermark, NO logos.
Match the style-lock paint atmosphere (IMAGE 2).
"""

NEG = (
    "text, letters, watermark, logo, huge baseball bat in foreground, bat covering face, "
    "photoreal photo, CGI, wrong person, young face, heavy beard, Santa Claus, child"
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


def cream_vignette(art: Image.Image, pad_frac: float = 0.035) -> Image.Image:
    art = art.convert("RGB").resize((PAGE, PAGE), Image.Resampling.LANCZOS)
    cream = Image.new("RGB", (PAGE, PAGE), CREAM)
    mask = Image.new("L", (PAGE, PAGE), 0)
    d = ImageDraw.Draw(mask)
    pad = int(PAGE * pad_frac)
    d.rounded_rectangle([pad, pad, PAGE - pad, PAGE - pad], radius=int(PAGE * 0.07), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=int(PAGE * 0.03)))
    return Image.composite(art, cream, mask)


def cover_fill(src: Image.Image, scale_boost: float = 1.18) -> Image.Image:
    src = src.convert("RGB")
    w, h = src.size
    scale = max(PAGE / w, PAGE / h) * scale_boost
    nw, nh = int(round(w * scale)), int(round(h * scale))
    im = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - PAGE) // 2
    top = max(0, (nh - PAGE) // 2 - int(PAGE * 0.04))
    if top + PAGE > nh:
        top = nh - PAGE
    return im.crop((left, top, left + PAGE, top + PAGE))


def font(size: int, names: list[str]):
    for n in names:
        p = Path(r"C:\Windows\Fonts") / n
        if p.is_file():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                pass
    return ImageFont.load_default()


def soft_cloud(w: int, h: int, op: int = 155) -> Image.Image:
    cloud = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(cloud)
    d.ellipse([-w // 10, -h // 8, w + w // 10, h + h // 5], fill=(*CREAM, op))
    return cloud.filter(ImageFilter.GaussianBlur(26))


def draw_wrapped(draw, text, fnt, box, fill, spacing=1.35):
    x0, y0, x1, y1 = box
    max_w = x1 - x0
    cw = max(8, fnt.getbbox("M")[2] - fnt.getbbox("M")[0])
    chars = max(18, int(max_w / (cw * 0.52)))
    y = y0
    for line in textwrap.wrap(text, width=chars):
        bb = fnt.getbbox(line)
        lw, lh = bb[2] - bb[0], bb[3] - bb[1]
        draw.text((x0 + (max_w - lw) // 2, y), line, font=fnt, fill=fill)
        y += int(lh * spacing)
        if y > y1:
            break
    return y


def typed(art: Image.Image, dest: Path) -> None:
    im = art.convert("RGBA")
    cloud_h = int(PAGE * 0.30)
    cloud = soft_cloud(PAGE, cloud_h, 160)
    layer = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    layer.paste(cloud, (0, PAGE - cloud_h - int(PAGE * 0.02)), cloud)
    composed = Image.alpha_composite(im, layer)
    draw = ImageDraw.Draw(composed)
    title = font(64, ["georgia.ttf", "Georgia.ttf", "times.ttf"])
    body = font(34, ["georgia.ttf", "Georgia.ttf", "times.ttf"])
    credit = font(24, ["georgia.ttf", "Georgia.ttf", "times.ttf"])
    margin = int(PAGE * 0.10)
    y = PAGE - cloud_h + int(PAGE * 0.025)
    tb = title.getbbox(BIO_TITLE)
    draw.text(((PAGE - (tb[2] - tb[0])) // 2, y), BIO_TITLE, font=title, fill=INK)
    y2 = draw_wrapped(
        draw,
        BIO_BODY,
        body,
        (margin, y + int(PAGE * 0.04), PAGE - margin, PAGE - int(PAGE * 0.07)),
        INK,
    )
    draw_wrapped(
        draw,
        CREDITS,
        credit,
        (margin, min(y2 + 14, PAGE - int(PAGE * 0.05)), PAGE - margin, PAGE - int(PAGE * 0.03)),
        (70, 70, 70),
        1.25,
    )
    composed.convert("RGB").save(dest)
    print("mock", dest)


def main() -> None:
    load_env()
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)

    # Prep refs square
    for src, name in ((JACK, "jack.png"), (STYLE, "style.png")):
        im = Image.open(src).convert("RGB")
        side = 1536
        canvas = Image.new("RGB", (side, side), CREAM)
        scale = min(side / im.width, side / im.height)
        nw, nh = int(im.width * scale), int(im.height * scale)
        im2 = im.resize((nw, nh), Image.Resampling.LANCZOS)
        canvas.paste(im2, ((side - nw) // 2, (side - nh) // 2))
        canvas.save(tmp / name)

    urls = [
        fal_client.upload_file(str(tmp / "jack.png")),
        fal_client.upload_file(str(tmp / "style.png")),
    ]

    print("=== Qwen 2 Pro /edit — bat + ribbon Easter egg ===")
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
    raw = download(result["images"][0]["url"])
    raw_path = OUT / "art-raw.png"
    raw.save(raw_path)

    filled = cover_fill(raw, scale_boost=1.18)
    full = cream_vignette(filled)
    full_path = OUT / "art-full-page-bat.png"
    full.save(full_path)
    print("full", full_path)

    typed(full, OUT / "art-MOCK-TYPE-bat.png")

    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — P-author-bio / v03

| Field | Value |
|-------|--------|
| **name** | About Author — bat + ribbon Easter egg (fun alt) |
| **unit** | P-author-bio |
| **version** | v03 |
| **date** | 2026-07-23 |
| **lane** | Qwen 2 Pro /edit |
| **model** | `{QWEN}` |
| **seed** | {seed} |
| **base** | locked Jack portrait + style-lock-v2 |
| **easter egg** | wooden baseball bat + festive ribbon, back corner R of tree / behind chair |
| **output** | art-full-page-bat.png · art-MOCK-TYPE-bat.png |
| **verdict** | pending (fun alt — not replacing locked plate) |

## Prompt

{PROMPT}
""",
        encoding="utf-8",
    )
    print("DONE")


if __name__ == "__main__":
    main()
