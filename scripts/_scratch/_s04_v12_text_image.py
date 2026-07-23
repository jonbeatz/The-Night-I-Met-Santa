#!/usr/bin/env python3
"""S4 Sit Here v12 — Flow v2 TEXT+IMAGE: L mistletoe text page · R Santa beckons."""
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
VERSION = "v12"
URLS_OUT = ROOT / "scripts/_scratch/_s04_v12_urls.json"

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
    "LOW ANGLE among a gift sea: Santa Claus down on the floor between boxes, gifts, and ribbons, "
    "gesturing warmly to invite the boy to sit beside him — beckoning hand, kind smile, open invitation. "
    "The boy stands or hesitates nearby in holly pajamas, still in awe, about to sit. "
    "Warm intimate invitation mood. ONE Christmas tree soft in background, fireplace glow optional. "
    "IMPORTANT: gift sea present but FEWER gifts than the busy S3 plate — clearer floor, less clutter, "
    "quiet space near figures. Art only — no text. "
    + SANTA_LOCK + " " + BOY_LOCK
)

NEG_R = (
    "shirtsleeves only, closed coat, suspenders over coat, bright white pajamas, cream walls, "
    "too many gifts, cluttered floor, eyes not engaged, standing formal portrait, text, letters, "
    "watermark, two Santas, phone"
)

PROMPT_L = (
    "Image 1 = watercolor/gouache paper STYLE (style-lock atmosphere, soft washes). "
    "Image 2 = the facing RIGHT image page — for a subtle soft bleed of color/mood from the right "
    "edge only (not a full copy of the scene). "
    "Create a SINGLE square children's-book TEXT PAGE (1:1) for S4 Sit Here LEFT (p10). "
    "Almost blank soft cream/ivory watercolor paper for poem text. "
    "Maybe a hint of mistletoe leaf peeking in from the RIGHT edge only — soft, subtle, decorative. "
    "Mostly open quiet center and left for live text later. Soft design connection to facing page "
    "via gentle warm wash bleed from the right — NOT a full scene, NOT people, NOT Santa, NOT a boy. "
    "Heirloom storybook paper feel. Art only — no letters, no poem text, no watermark."
)

NEG_L = (
    "full scene, people, faces, Santa, child, busy illustration, dark burgundy full bleed, "
    "text, letters, watermark, cluttered decoration, large tree filling page"
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
| **status** | working — Flow v2 regen + open-coat Santa |
| **tier** | dial_mock |

## Layout (Flow v2)

- **L (p10):** Almost blank watercolor text page · mistletoe hint from right edge · soft bleed from facing image
- **R (p11):** Low-angle gift sea · Santa on floor beckoning boy to sit · open-coat Santa G0 · Boy G0

## Notes

Fewer gifts than S3 quality bar (clearer floor). Poem text live in InDesign later.
""",
        encoding="utf-8",
    )


def build_board(left: Image.Image, right: Image.Image, out: Path) -> None:
    side = 520
    l = left.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
    r = right.convert("RGB").resize((side, side), Image.Resampling.LANCZOS)
    margin, gap, header = 28, 20, 70
    sheet = Image.new("RGB", (margin * 2 + side * 2 + gap, margin * 2 + header + side + 48), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S4 Sit Here — {VERSION} TEXT+IMAGE ({DAY})", fill=(28, 24, 20), font=font(22))
    d.text(
        (margin, 42),
        "L = mistletoe text page · R = Santa beckons (open coat) · quality bar S3 v07 · fewer gifts",
        fill=(110, 100, 90),
        font=font(13),
    )
    y = margin + header
    sheet.paste(l, (margin, y))
    sheet.paste(r, (margin + side + gap, y))
    d.text((margin, y + side + 10), "LEFT p10 — TEXT PAGE", fill=(32, 28, 24), font=font(15))
    d.text((margin + side + gap, y + side + 10), "RIGHT p11 — IMAGE PAGE", fill=(32, 28, 24), font=font(15))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)


def upload_phase1() -> dict:
    load_env()
    # Crop quality bar to square-ish room for R page DNA (use right half of S3 as room DNA)
    q = Image.open(QUALITY).convert("RGB")
    w, h = q.size
    # Use full spread resized to square for atmosphere, or center crop
    side = min(w, h)
    # Prefer right-biased crop (Santa/tree side) for sit-here DNA
    x0 = w - side
    crop = q.crop((x0, 0, w, side)) if w >= h else q.crop((0, 0, w, w))
    crop_path = ROOT / "scripts/_scratch/_s04_v12_quality_crop.png"
    crop.resize((1536, 1536), Image.Resampling.LANCZOS).save(crop_path, "PNG")
    urls = {
        "quality_crop": upload(crop_path, "s03-v07-quality-crop.png", (1536, 1536)),
        "santa": upload(SANTA, "santa-G0.png"),
        "boy": upload(BOY, "boy-narrator-G0.png"),
        "style": upload(STYLE, "style-lock-v2.png"),
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps(urls, indent=2))
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
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    # Promote development pointers
    (DEV / "art-right.png").write_bytes(data_r)
    (DEV / "art-left.png").write_bytes(data_l)

    left = Image.open(io.BytesIO(data_l)).convert("RGB")
    right = Image.open(io.BytesIO(data_r)).convert("RGB")
    board = MOCKS / "_INDEX" / f"S04-sit-here-{VERSION}-text-image-{DAY}.png"
    build_board(left, right, board)
    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art-right.png")], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art-left.png")], check=False)
    print("saved", DEV / VERSION)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "upload":
        upload_phase1()
    elif sys.argv[1] == "save":
        # save <url_r> <seed_r> <req_r> <url_l> <seed_l> <req_l>
        save_pair(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7])
    else:
        raise SystemExit("upload | save url_r seed_r req_r url_l seed_l req_l")
