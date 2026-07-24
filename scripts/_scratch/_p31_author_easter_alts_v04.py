#!/usr/bin/env python3
"""P-author-bio v04 — two quick Easter egg alts: upside-down bat knob + lefty golf bag."""
from __future__ import annotations

import io
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/generated/mocks/P-author-bio/v04"
JACK = ROOT / "Media/approved/characters/jack-farrell-portrait.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
QWEN = "fal-ai/qwen-image-2/pro/edit"
PAGE = 2625
CREAM = (252, 246, 238)

KEEP = """\
KEEP everything important identical:
- Same elderly man Jack Farrell — exact face, smile, white swept-back hair, cream cable-knit sweater
- Same floral armchair pose, hands in lap
- Same glowing Christmas tree on the LEFT
- Same cozy living-room mood, soft gouache/watercolor storybook paint
- Soft cream watercolor vignette edges (FRAME ON)
NO text, NO letters, NO watermark, NO logos.
Match the style-lock paint atmosphere (IMAGE 2).
"""

NEG = (
    "text, letters, watermark, logo, huge prop in foreground covering face, "
    "photoreal photo, CGI, wrong person, young face, heavy beard, Santa Claus, child"
)

PROMPTS = {
    "bat-knob": """\
Edit this Christmas storybook author portrait carefully.

"""
    + KEEP
    + """
ADD only one subtle Easter egg:
In the BACK CORNER behind the man — to the RIGHT of the Christmas tree / behind the chair —
a wooden baseball bat standing UPSIDE DOWN (inverted): the KNOB / handle-butt end is UP and
clearly visible near the top of the bat, barrel end down toward the floor.
Tie a soft festive ribbon (red or deep green bow) around the knob/handle area at the top.
Quiet shadowed corner detail — small in frame, NOT a hero prop. Do NOT cover his face or hands.
""",
    "golf-bag": """\
Edit this Christmas storybook author portrait carefully.

"""
    + KEEP
    + """
ADD only one subtle Easter egg:
In the BACK CORNER behind the man — to the RIGHT of the Christmas tree / behind the chair —
a glimpse of a LEFT-HANDED golf bag standing quietly in the shadows.
You can just see the top of the bag and a few club heads peeking out — drivers and irons —
subtle, partially obscured by the chair/tree edge. Not a full bag portrait; a quiet corner hint.
Do NOT make the bag huge. Do NOT put it in the foreground. Do NOT cover his face or hands.
No readable brand logos on the bag or clubs.
""",
}


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


def prep_refs(tmp: Path) -> list[str]:
    for src, name in ((JACK, "jack.png"), (STYLE, "style.png")):
        im = Image.open(src).convert("RGB")
        side = 1536
        canvas = Image.new("RGB", (side, side), CREAM)
        scale = min(side / im.width, side / im.height)
        nw, nh = int(im.width * scale), int(im.height * scale)
        im2 = im.resize((nw, nh), Image.Resampling.LANCZOS)
        canvas.paste(im2, ((side - nw) // 2, (side - nh) // 2))
        canvas.save(tmp / name)
    return [
        fal_client.upload_file(str(tmp / "jack.png")),
        fal_client.upload_file(str(tmp / "style.png")),
    ]


def gen(slug: str, prompt: str, urls: list[str]) -> Path:
    print(f"=== Qwen {slug} ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": prompt,
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
    raw = download(result["images"][0]["url"])
    (OUT / f"art-raw-{slug}.png").write_bytes(b"")  # placeholder touch
    raw.save(OUT / f"art-raw-{slug}.png")
    full = cream_vignette(cover_fill(raw, 1.18))
    dest = OUT / f"art-full-{slug}.png"
    full.save(dest)
    print("saved", dest)
    return dest


def main() -> None:
    load_env()
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)
    urls = prep_refs(tmp)

    paths = {}
    for slug, prompt in PROMPTS.items():
        paths[slug] = gen(slug, prompt, urls)

    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — P-author-bio / v04

| Field | Value |
|-------|--------|
| **name** | About Author Easter alts — upside-down bat knob · lefty golf bag |
| **version** | v04 |
| **date** | 2026-07-23 |
| **lane** | Qwen 2 Pro /edit |
| **model** | `{QWEN}` |
| **base** | locked Jack + style-lock-v2 |
| **outputs** | `art-full-bat-knob.png` · `art-full-golf-bag.png` |
| **verdict** | pending fun alts |

## Variants
1. **bat-knob** — bat upside down, knob up with ribbon
2. **golf-bag** — subtle left-handed golf bag glimpse (drivers + irons)
""",
        encoding="utf-8",
    )
    # rename to clearer names
    paths["bat-knob"].replace(OUT / "art-full-bat-knob.png")
    paths["golf-bag"].replace(OUT / "art-full-golf-bag.png")
    print("DONE", OUT)


if __name__ == "__main__":
    main()
