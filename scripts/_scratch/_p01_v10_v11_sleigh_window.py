#!/usr/bin/env python3
"""P01 v10 (sleigh + mock type layout) / v11 (same art, cream plate, no text)."""
from __future__ import annotations

import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/P01-title"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
SRC = DEV / "v07" / "art.png"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048

FONT_DIR = (
    ROOT
    / "Xtraz/Fonts/Allura,Cabin,Cinzel_Decorative,Cormorant_Garamond,Dancing_Script,etc"
    / "Cormorant_Garamond/static"
)
CREAM = (245, 240, 230)
INK = (44, 44, 44)
PAGE = 2625
ART_FRAC = 0.66

AUTHOR = "Written by Jack Farrell"
COPYRIGHT = "First illustrated edition, 2026\nBook design by Jon Farrell"

PROMPT = (
    "Edit image 2 only — keep the SAME winter window title-page painting. "
    "Image 1 = watercolor/gouache paint style lock. "
    "Preserve: cream/ivory walls, four-pane window, soft blue-gray night with full moon and falling snow, "
    "light cream curtains tied back, Christmas tree edge with warm lights and ornaments, "
    "optional presents and tiny holly on sill, soft FRAME ON vignette fading to cream paper. "
    "ADD only this: through the window in the distant night sky, a VERY FAINT tiny silhouette of "
    "Santa's sleigh and reindeer crossing in front of / near the moon — subtle, easy to miss, "
    "distant and soft, not detailed, not large, not cartoon. The window still owns the frame. "
    "REMOVE any baked letters, titles, watermarks, or gibberish text completely — leave open cream. "
    "Do not add people, faces, or hands indoors. Art only — no text."
)
NEGATIVE = (
    "text, letters, typography, title, copyright, watermark, logo, signature, "
    "large sleigh, detailed santa face, close-up santa, people indoors, hands, "
    "clip art, sticker, flat icon, photorealistic, deep burgundy walls"
)


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


def fal_key() -> str:
    key = (os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY") or "").strip()
    if not key:
        raise SystemExit("Missing FAL_KEY")
    return key


def upload_bytes(key: str, name: str, data: bytes, content_type: str) -> str:
    req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps({"file_name": name, "content_type": content_type}).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        meta = json.loads(resp.read().decode())
    put = urllib.request.Request(
        meta["upload_url"], data=data, headers={"Content-Type": content_type}, method="PUT"
    )
    with urllib.request.urlopen(put, timeout=180) as resp:
        resp.read()
    return meta["file_url"]


def prepare_upload(path: Path, name: str, key: str) -> str:
    im = Image.open(path).convert("RGB")
    im.thumbnail((SIZE, SIZE), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return upload_bytes(key, Path(name).with_suffix(".png").name, buf.getvalue(), "image/png")


def fal_req(key: str, url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"Authorization": f"Key {key}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:2000]}") from e


def wait_result(key: str, submitted: dict) -> dict:
    for i in range(100):
        time.sleep(3 if i else 1)
        st = fal_req(key, submitted["status_url"])
        status = st.get("status") or st.get("queue_status")
        print(f"  [{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, submitted["response_url"])
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    raise SystemExit("timeout")


def download(url: str, dest: Path) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return Image.open(io.BytesIO(data)).convert("RGB")


def load_font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    name = {
        "regular": "CormorantGaramond-Regular.ttf",
        "medium": "CormorantGaramond-Medium.ttf",
        "italic": "CormorantGaramond-Italic.ttf",
    }[weight]
    return ImageFont.truetype(str(FONT_DIR / name), size)


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def soft_vignette_rgba(rgb: Image.Image, feather: int = 110) -> Image.Image:
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


def prep_window_plate(raw: Image.Image) -> Image.Image:
    """Prefer window focus; soft-scrub any residual bottom glyphs."""
    im = raw.convert("RGBA")
    w, h = im.size
    blob = Image.new("L", (w, h), 0)
    bdraw = ImageDraw.Draw(blob)
    bdraw.rectangle([int(w * 0.10), int(h * 0.78), int(w * 0.90), h], fill=255)
    blob = blob.filter(ImageFilter.GaussianBlur(radius=40))
    cream = Image.new("RGBA", (w, h), (*CREAM, 255))
    cream.putalpha(blob)
    im = Image.alpha_composite(im, cream)
    return im.convert("RGB")


def place_art_on_cream(raw: Image.Image) -> tuple[Image.Image, int, int, int]:
    """Return cream page + art placed; also ax, ay, art_w for type layout."""
    plate = prep_window_plate(raw)
    page = Image.new("RGB", (PAGE, PAGE), CREAM)
    art_w = int(PAGE * ART_FRAC)
    art_r = plate.resize((art_w, art_w), Image.Resampling.LANCZOS)
    art_rgba = soft_vignette_rgba(art_r, feather=110)
    ax = (PAGE - art_w) // 2
    ay = int(PAGE * 0.18)
    page_rgba = page.convert("RGBA")
    page_rgba.alpha_composite(art_rgba, (ax, ay))
    return page_rgba.convert("RGB"), ax, ay, art_w


def compose_v10_with_type(raw: Image.Image) -> Image.Image:
    page, ax, ay, art_w = place_art_on_cream(raw)
    draw = ImageDraw.Draw(page)
    title_font = load_font("medium", 92)
    author_font = load_font("italic", 42)
    copy_font = load_font("regular", 28)
    y = int(PAGE * 0.055)
    for line in ("The Night I", "Met Santa"):
        bbox = title_font.getbbox(line)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((PAGE - tw) // 2, y), line, font=title_font, fill=INK)
        y += th + 6
    below = ay + art_w + int(PAGE * 0.035)
    bbox = author_font.getbbox(AUTHOR)
    tw = bbox[2] - bbox[0]
    draw.text(((PAGE - tw) // 2, below), AUTHOR, font=author_font, fill=INK)
    copy_y = below + (bbox[3] - bbox[1]) + 28
    for line in COPYRIGHT.split("\n"):
        bbox = copy_font.getbbox(line)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((PAGE - tw) // 2, copy_y), line, font=copy_font, fill=INK)
        copy_y += th + 10
    tiny = load_font("regular", 18)
    note = "COMP · v10 Santa-in-window · Cormorant mock type · not final"
    bbox = tiny.getbbox(note)
    draw.text(((PAGE - (bbox[2] - bbox[0])) // 2, PAGE - 48), note, font=tiny, fill=(160, 150, 140))
    return page


def compose_v11_art_only(raw: Image.Image) -> Image.Image:
    page, _, _, _ = place_art_on_cream(raw)
    return page


def write_recipe(ver: str, name: str, seed, req_id: str, note: str) -> None:
    out = DEV / ver
    text = f"""# RECIPE — P01-title / {ver}

| Field | Value |
|-------|--------|
| **name** | {name} |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | {ver} |
| **date** | {DAY} |
| **lane** | A2 Qwen 2 Pro Edit + Pillow layout |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · cream/ivory · faint sleigh silhouette |
| **FRAME** | ON |
| **source** | `Media/development/P01-title/v07/art.png` |
| **size** | 2048² plate · 2625² layout page |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png (raw plate) · page.png (cream layout) |
| **type** | {note} |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Prompt

{PROMPT}

## Negative

{NEGATIVE}

## Related

- Sibling: v10 layout-with-type · v11 art-only cream plate (same Qwen plate)
- Board: `Media/generated/mocks/_INDEX/P01-title-v10-v11-board.png`
- Script: `scripts/_scratch/_p01_v10_v11_sleigh_window.py`
"""
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(v10_page: Image.Image, v11_page: Image.Image) -> Path:
    panel, label_h, gap, margin, header = 900, 110, 36, 40, 110
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text((margin, 28), "P01 Title — v10 (with type) vs v11 (art only)", fill=(40, 30, 28), font=board_font(28))
    draw.text(
        (margin, 68),
        "Same winter window + faint sleigh silhouette · cream page · ~66% vignette · Qwen 2 Pro Edit",
        fill=(90, 70, 60),
        font=board_font(15),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v10_page, "v10 — SANTA IN THE WINDOW", "Layout + Cormorant mock type"),
            (v11_page, "v11 — ART ONLY", "Clean cream plate for InDesign live text"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 12), title, fill=(40, 30, 28), font=board_font(20))
        draw.text((x, y + panel + 44), sub, fill=(90, 70, 60), font=board_font(14))
    out = INDEX / "P01-title-v10-v11-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    print("refs upload")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    src_url = prepare_upload(SRC, "v07-winter-window.png", key)

    print("submit v10 art (sleigh edit)")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, src_url],
            "image_size": {"width": SIZE, "height": SIZE},
            "num_images": 1,
            "output_format": "png",
        },
    )
    print("  request_id", submitted.get("request_id"))
    result = wait_result(key, submitted)
    images = result.get("images") or result.get("output", {}).get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:4000])
    url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    seed = result.get("seed") or result.get("output", {}).get("seed")
    req_id = submitted.get("request_id") or ""

    for ver in ("v10", "v11"):
        (DEV / ver).mkdir(parents=True, exist_ok=True)

    raw_path = DEV / "v10" / "art.png"
    raw = download(url, raw_path)
    # Identical plate for v11
    (DEV / "v11" / "art.png").write_bytes(raw_path.read_bytes())
    print(f"saved plate {raw.size} seed {seed}")

    v10_page = compose_v10_with_type(raw)
    v11_page = compose_v11_art_only(raw)
    p10 = DEV / "v10" / "page.png"
    p11 = DEV / "v11" / "page.png"
    v10_page.save(p10, "PNG")
    v11_page.save(p11, "PNG")

    meta = {
        "seed": seed,
        "request_id": req_id,
        "model": "fal-ai/qwen-image-2/pro/edit",
        "source": "v07/art.png",
        "prompt": PROMPT,
    }
    (DEV / "v10" / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (DEV / "v11" / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (DEV / "v10" / "result.json").write_text(json.dumps(result, indent=2)[:20000], encoding="utf-8")

    write_recipe(
        "v10",
        "Santa in the Window (WITH TEXT)",
        seed,
        req_id,
        "Cormorant mock type on page.png — art.png is clean Qwen plate",
    )
    write_recipe(
        "v11",
        "Winter Window ART ONLY (NO TEXT)",
        seed,
        req_id,
        "No mock type — page.png is cream plate for InDesign live text",
    )

    board = build_board(v10_page, v11_page)
    print(f"saved {p10}")
    print(f"saved {p11}")
    print(f"BOARD {board}")


if __name__ == "__main__":
    main()
