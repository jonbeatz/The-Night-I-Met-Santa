#!/usr/bin/env python3
"""S4 Sit Here v13 — Flow v2 TEXT+IMAGE: L mistletoe whisper · R Santa RIGHT beckons."""
from __future__ import annotations

import io
import json
import os
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S04-sit-here"
MOCKS = ROOT / "Media/generated/mocks/S04-sit-here"
QUALITY = ROOT / "Media/development/S03-eyes-met/v07/art.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
SANTA = ROOT / "Media/approved/characters/santa-G0.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
DAY = "2026-07-22"
VERSION = "v13"
URLS_OUT = ROOT / "scripts/_scratch/_s04_v13_urls.json"

SANTA_LOCK = (
    "SANTA WARDROBE LOCK: red coat worn OPEN and unbuttoned — not closed, not a solid red block; "
    "cream/off-white vertically striped button-down shirt visible underneath; brown leather "
    "suspenders over the striped shirt (NOT over the coat fabric); red pants; black boots; "
    "white fur trim on cuffs and hem; relaxed approachable grandfather-like. Match santa-G0."
)
BOY_LOCK = (
    "BOY G0 LOCK: oatmeal/taupe (warm beige) holly pajamas — NOT white, NOT cream; green holly "
    "leaves with red berries clearly visible; red trim on collar, cuffs, pant hems; red buttons "
    "down the front; classic button-up set. Tousled light brown hair with golden highlights; "
    "brown eyes; rosy cheeks. Match boy-narrator-G0."
)

PROMPT_R = (
    "Image 1 = QUALITY BAR from locked S3 Eyes Met — match rich oil-painting warmth/depth, "
    "burgundy walls, warm golden firelight and tree glow, wide living-room context. "
    "Image 2 = Santa G0 wardrobe. Image 3 = Boy G0 pajamas/character. "
    "Create a SINGLE square children's-book IMAGE PAGE (1:1) for S4 Sit Here RIGHT (p11). "
    "ROOM LAYOUT LOCK (same as S2 and S3): Santa is on the RIGHT side of the frame / room. "
    "Do NOT flip or mirror — Santa stays RIGHT. Boy approaches from the LEFT side of the frame. "
    "LOW ANGLE among a gift sea: Santa Claus sitting on the floor among boxes, gifts, and ribbons "
    "galore on the RIGHT, gesturing warmly beckoning the boy to come sit beside him — kind smile, "
    "open invitation, beckoning hand. The boy in holly pajamas approaches from LEFT, still in awe. "
    "Warm intimate invitation mood. ONE Christmas tree soft in background, fireplace glow optional. "
    "Gift sea present but FEWER gifts than the busy S3 plate — clearer floor, less clutter, "
    "quiet space near figures. Art only — no text, no letters. "
    + SANTA_LOCK + " " + BOY_LOCK
)

NEG_R = (
    "Santa on left, flipped room, mirrored composition, shirtsleeves only, closed coat, "
    "suspenders over coat, bright white pajamas, cream walls, too many gifts, cluttered floor, "
    "standing formal portrait, text, letters, watermark, two Santas, phone"
)

PROMPT_L = (
    "Image 1 = soft watercolor paper STYLE only (atmosphere of gentle washes — not a scene). "
    "Create a SINGLE square children's-book TEXT PAGE (1:1) for S4 Sit Here LEFT (p10). "
    "This is NOT an illustration page. Almost entirely BLANK soft ivory/cream watercolor paper "
    "with gentle subtle paper texture only. Vast open empty center, left, bottom for poem text. "
    "The ONLY visual element: a tiny sprig of mistletoe with one small red berry, barely peeking "
    "in from the TOP-RIGHT corner of the page — whisper-small, delicate, decorative hint. "
    "Everything else is open cream space. NO Santa. NO boy. NO room. NO furniture. NO gifts. "
    "NO burgundy walls. NO tree. NO fireplace. NO soft bleed of a room scene. "
    "Heirloom storybook blank paper feel. Art only — no letters, no poem text, no watermark."
)

NEG_L = (
    "full scene, people, faces, Santa, child, boy, room, furniture, gifts, ribbons, burgundy walls, "
    "fireplace, Christmas tree, busy illustration, vignette scene, soft bleed of living room, "
    "large mistletoe, wreath filling corner, dark colors, text, letters, watermark, clutter"
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


def upload(path: Path, name: str, size: tuple[int, int] | None = None) -> str:
    key = fal_key()
    im = Image.open(path).convert("RGB")
    if size:
        im = im.resize(size, Image.Resampling.LANCZOS)
    else:
        im.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps({"file_name": name, "content_type": "image/png"}).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        meta = json.loads(resp.read().decode())
    put = urllib.request.Request(
        meta["upload_url"], data=buf.getvalue(), headers={"Content-Type": "image/png"}, method="PUT"
    )
    with urllib.request.urlopen(put, timeout=180) as resp:
        resp.read()
    return meta["file_url"]


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(vdir: Path, meta: dict) -> None:
    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S04-sit-here / {VERSION}

| Field | Value |
|-------|--------|
| **name** | S4 Sit Here — Flow v2 TEXT+IMAGE |
| **unit** | S04-sit-here |
| **book page** | Flow v2 p10\\|11 · TEXT L + IMAGE R |
| **version** | {VERSION} |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **quality_bar** | S03-eyes-met v07 KEEP |
| **R request_id** | `{meta.get("req_r", "")}` |
| **R seed** | {meta.get("seed_r", "")} |
| **L request_id** | `{meta.get("req_l", "")}` |
| **L seed** | {meta.get("seed_l", "")} |
| **status** | working — quieter mistletoe L · Santa RIGHT |
| **tier** | dial_mock |

## Layout (Flow v2)

- **L (p10):** Almost blank cream watercolor text page · tiny mistletoe + one berry top-right only
- **R (p11):** Low-angle gift sea · Santa on RIGHT beckoning · boy from LEFT · open-coat Santa G0 · Boy G0

## Notes

Two separate files (`art-left.png`, `art-right.png`). Fewer gifts than S3. Poem text in InDesign later.
""",
        encoding="utf-8",
    )


def build_board(left: Image.Image, right: Image.Image, out: Path) -> None:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import text_image_board

    text_image_board(
        left,
        right,
        out,
        unit="S04-sit-here",
        version=VERSION,
        day=DAY,
        tech="Qwen 2 Pro /edit · square · S3 v07 quality bar",
        subtitle="cream + mistletoe TR · Santa RIGHT beckons",
    )
    print("board", out)


def upload_phase1() -> dict:
    load_env()
    q = Image.open(QUALITY).convert("RGB")
    w, h = q.size
    side = min(w, h)
    x0 = w - side
    crop = q.crop((x0, 0, w, side)) if w >= h else q.crop((0, 0, w, w))
    crop_path = ROOT / "scripts/_scratch/_s04_v13_quality_crop.png"
    crop.resize((1536, 1536), Image.Resampling.LANCZOS).save(crop_path, "PNG")
    # Cream paper base for L so edit has a blank page to start from (not a scene)
    cream = Image.new("RGB", (1536, 1536), (250, 244, 232))
    # faint watercolor noise via noise-ish soft vignette corners only
    overlay = Image.new("RGBA", (1536, 1536), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(40):
        a = 4 + (i % 3)
        od.ellipse((-80 + i, -80 + i, 220 - i, 220 - i), fill=(236, 226, 210, a))
        od.ellipse((1536 - 220 + i, -80 + i, 1536 + 80 - i, 220 - i), fill=(236, 226, 210, a))
    cream = Image.alpha_composite(cream.convert("RGBA"), overlay).convert("RGB")
    cream_path = ROOT / "scripts/_scratch/_s04_v13_cream_base.png"
    cream.save(cream_path, "PNG")
    urls = {
        "quality_crop": upload(crop_path, "s03-v07-quality-crop-v13.png", (1536, 1536)),
        "santa": upload(SANTA, "santa-G0-v13.png"),
        "boy": upload(BOY, "boy-narrator-G0-v13.png"),
        "style": upload(STYLE, "style-lock-v2-v13.png"),
        "cream": upload(cream_path, "cream-text-base-v13.png", (1536, 1536)),
        "prompt_r": PROMPT_R,
        "neg_r": NEG_R,
        "prompt_l": PROMPT_L,
        "neg_l": NEG_L,
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in urls.items() if k in ("quality_crop", "santa", "boy", "style", "cream")}, indent=2))
    return urls


def save_pair(url_r: str, seed_r: int, req_r: str, url_l: str, seed_l: int, req_l: str) -> None:
    def dl(url: str) -> bytes:
        with urllib.request.urlopen(url, timeout=180) as resp:
            return resp.read()

    data_r, data_l = dl(url_r), dl(url_l)
    for base in (DEV / VERSION, MOCKS / VERSION):
        base.mkdir(parents=True, exist_ok=True)
        (base / "art-right.png").write_bytes(data_r)
        (base / "art-left.png").write_bytes(data_l)
        write_recipe(base, {"req_r": req_r, "seed_r": seed_r, "req_l": req_l, "seed_l": seed_l})
        (base / "meta.json").write_text(
            json.dumps(
                {
                    "version": VERSION,
                    "layout": "text_plus_image",
                    "right": {"url": url_r, "seed": seed_r, "request_id": req_r},
                    "left": {"url": url_l, "seed": seed_l, "request_id": req_l},
                    "quality_bar": "S03-eyes-met/v07",
                    "model": "fal-ai/qwen-image-2/pro/edit",
                    "notes": "Santa RIGHT; L mistletoe top-right only",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    (DEV / "art-right.png").write_bytes(data_r)
    (DEV / "art-left.png").write_bytes(data_l)

    left = Image.open(io.BytesIO(data_l)).convert("RGB")
    right = Image.open(io.BytesIO(data_r)).convert("RGB")
    board = MOCKS / "_INDEX" / f"S04-sit-here-{VERSION}-text-image-{DAY}.png"
    build_board(left, right, board)
    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    print("saved", DEV / VERSION)
    print("board", board)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "upload":
        upload_phase1()
    elif sys.argv[1] == "save":
        save_pair(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7])
    else:
        raise SystemExit("upload | save url_r seed_r req_r url_l seed_l req_l")
