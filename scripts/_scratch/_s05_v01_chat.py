#!/usr/bin/env python3
"""S5 Chat v01 — Flow v2 seamless spread p12|13 · happiest beat · quality bar S3 v07."""
from __future__ import annotations

import io
import json
import os
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S05-chat"
MOCKS = ROOT / "Media/generated/mocks/S05-chat"
QUALITY = ROOT / "Media/development/S03-eyes-met/v07/art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
DAY = "2026-07-22"
VERSION = "v01"
URLS_OUT = ROOT / "scripts/_scratch/_s05_v01_urls.json"

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

PROMPT = (
    "Image 1 = QUALITY BAR from locked S3 Eyes Met — match rich oil-painting warmth/depth, "
    "burgundy walls, warm golden firelight and tree glow, wide living-room continuity. "
    "Image 2 = Santa G0 wardrobe. Image 3 = Boy G0 pajamas/character. "
    "Create a NEW seamless wide children's-book SPREAD (2:1, pages 12|13) for S5 Chat — "
    "the HAPPIEST spread in the book: pure joy, pure connection, laughter crossing the gutter. "
    "LEFT half (p12): Santa Claus sitting on the floor BY THE FIREPLACE, jolly and laughing, "
    "storytelling with animated hands, warm firelight on his face — open joyful expression. "
    "RIGHT half (p13): the boy sitting on the floor Indian-style / cross-legged, so happy and "
    "excited, beaming, in front of presents and the Christmas tree. "
    "ROOM LAYOUT LOCK (same as S2/S3): fireplace / Santa energy on LEFT, tree / boy energy on RIGHT. "
    "Do NOT flip. One continuous burgundy living room across the gutter — seamless spread, "
    "not two separate panels. Both figures seated on the floor (NOT standing). "
    "Gift sea present but FEWER gifts than the busy S3 plate — clearer floor, space for joy. "
    "Intimate heirloom mood, animated friendly gestures, storytelling warmth. Art only — no text. "
    + SANTA_LOCK + " " + BOY_LOCK
)

NEGATIVE = (
    "standing portraits, stiff poses, sad faces, closed coat, suspenders over coat, shirtsleeves only, "
    "bright white pajamas, cream walls, flipped room, Santa on right, boy on left only, "
    "two Santas, twin Santa, boy in Santa suit, red coat on child, too many gifts, cluttered, "
    "text, letters, watermark, split panel border, white gutter line"
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


def write_recipe(vdir: Path, seed: int, req_id: str, url: str) -> None:
    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S05-chat / {VERSION}

| Field | Value |
|-------|--------|
| **name** | S5 Chat — happiest seamless spread |
| **unit** | S05-chat |
| **book page** | Flow v2 p12\\|13 · FULL SPREAD |
| **version** | {VERSION} |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · quality S03-v07 + santa-G0 + boy-G0 |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **fal_url** | `{url}` |
| **status** | working — Flow v2 L Santa hearth / R boy cross-legged |
| **tier** | dial_mock |
| **quality_bar** | S03-eyes-met v07 |

## Layout (Flow v2)

- **L (p12):** Santa on floor by fireplace · jolly laughing · animated storytelling hands · open-coat G0 v2
- **R (p13):** Boy Indian-style/cross-legged · beaming · holly PJs · tree + gifts
- Seamless burgundy room · laughter across gutter · fewer gifts than S3
""",
        encoding="utf-8",
    )


def build_board(art: Image.Image, out: Path) -> None:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        art,
        out,
        unit="S05-chat",
        version=VERSION,
        day=DAY,
        tech="Qwen 2 Pro /edit · 2048×1024 · S3 v07 quality bar",
        subtitle="L Santa hearth · R boy cross-legged · open-coat + Boy G0",
    )
    print("board", out)


def upload_phase() -> dict:
    load_env()
    urls = {
        "quality": upload(QUALITY, "s03-v07-quality-s05.png", (2048, 1024)),
        "santa": upload(SANTA, "santa-G0-s05.png"),
        "boy": upload(BOY, "boy-G0-s05.png"),
        "prompt": PROMPT,
        "negative": NEGATIVE,
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps({k: urls[k] for k in ("quality", "santa", "boy")}, indent=2))
    return urls


def save(url: str, seed: int, req_id: str) -> None:
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    for base in (DEV / VERSION, MOCKS / VERSION):
        base.mkdir(parents=True, exist_ok=True)
        (base / "art.png").write_bytes(data)
        write_recipe(base, seed, req_id, url)
        (base / "meta.json").write_text(
            json.dumps(
                {
                    "version": VERSION,
                    "layout": "seamless_spread",
                    "url": url,
                    "seed": seed,
                    "request_id": req_id,
                    "quality_bar": "S03-eyes-met/v07",
                    "model": "fal-ai/qwen-image-2/pro/edit",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    # working dashboard (not locked until Jon keeps)
    (DEV / "art.png").write_bytes(data)
    art = Image.open(io.BytesIO(data)).convert("RGB")
    # also split previews for page view
    w, h = art.size
    art.crop((0, 0, w // 2, h)).save(DEV / VERSION / "art-left.png")
    art.crop((w // 2, 0, w, h)).save(DEV / VERSION / "art-right.png")
    board = MOCKS / "_INDEX" / f"S05-chat-{VERSION}-seamless-{DAY}.png"
    build_board(art, board)
    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art.png")], check=False)
    print("saved", DEV / VERSION)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "upload":
        upload_phase()
    elif sys.argv[1] == "save":
        save(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        raise SystemExit("upload | save url seed req_id")
