#!/usr/bin/env python3
"""S6 Cocoa v01 — Flow v2 TEXT+IMAGE: L decorative text page · R cocoa prop hero."""
from __future__ import annotations

import io
import json
import os
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S06-cocoa"
MOCKS = ROOT / "Media/generated/mocks/S06-cocoa"
QUALITY = ROOT / "Media/development/S03-eyes-met/v07/art.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
SANTA = ROOT / "Media/approved/characters/santa-G0.png"
DAY = "2026-07-22"
VERSION = "v01"
URLS_OUT = ROOT / "scripts/_scratch/_s06_v01_urls.json"

SANTA_LOCK = (
    "SANTA WARDROBE LOCK: red coat worn OPEN and unbuttoned — not closed, not a solid red block; "
    "cream/off-white vertically striped button-down shirt visible underneath; brown leather "
    "suspenders over the striped shirt (NOT over the coat fabric); red pants; black boots; "
    "white fur trim on cuffs and hem; relaxed approachable grandfather-like. Match santa-G0."
)

PROMPT_R = (
    "Image 1 = QUALITY BAR from locked S3 Eyes Met — match rich oil-painting warmth/depth, "
    "burgundy walls, warm golden firelight. Image 2 = Santa G0 wardrobe. Image 3 = style lock. "
    "Create a SINGLE square children's-book IMAGE PAGE (1:1) for S6 Cocoa RIGHT (p15). "
    "PROP HERO SHOT: the steaming mug of hot cocoa is the STAR — large clear mug with "
    "marshmallows and visible curling steam catching warm firelight. "
    "Santa holds the mug happily and joyfully, mid-storytelling, warm smile, open joyful mood. "
    "Close-to-medium intimate framing so the mug reads clearly as the hero prop. "
    "Soft fireplace glow behind/beside him; tree glow optional and soft. "
    "Not a full busy room — focus on Santa + mug + steam. Art only — no text, no letters. "
    + SANTA_LOCK
)

NEG_R = (
    "closed coat, suspenders over coat, shirtsleeves only, tiny mug, no steam, no marshmallows, "
    "standing lineup, busy gift sea dominating, boy in Santa suit, text, letters, watermark, phone"
)

PROMPT_L = (
    "Image 1 = blank cream watercolor paper base. Image 2 = soft watercolor STYLE atmosphere. "
    "Create a SINGLE square children's-book TEXT PAGE (1:1) for S6 Cocoa LEFT (p14). "
    "This is a decorative TEXT PAGE — not a full illustration scene. Soft ivory/cream watercolor paper. "
    "LARGE OPEN CENTER for poem text (empty quiet band across the middle). "
    "ABOVE the text band: a simple, artistic outside snow scene with a friendly snowman — "
    "small vignette at the top, soft and decorative, framing the page, not competing with text. "
    "BELOW the text band: simple artistic still-life hints of a wool coat, a silk tie, and a "
    "diamond ring — elegant watercolor props as decorative border elements, not literal product shots. "
    "These frame the poem space rather than fill it. Soft heirloom storybook ornament feel. "
    "NO Santa. NO boy. NO living-room scene. Art only — no letters, no poem text, no watermark."
)

NEG_L = (
    "full room scene, Santa, child, boy, fireplace, Christmas tree indoor, busy illustration, "
    "literal product photography, catalog shots, text, letters, watermark, cluttered center, "
    "dark burgundy full bleed, competing focal points in the middle"
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
        f"""# RECIPE — S06-cocoa / {VERSION}

| Field | Value |
|-------|--------|
| **name** | S6 Cocoa — Flow v2 TEXT+IMAGE |
| **unit** | S06-cocoa |
| **book page** | Flow v2 p14\\|15 · TEXT L + IMAGE R |
| **version** | {VERSION} |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **quality_bar** | S03-eyes-met v07 |
| **R request_id** | `{meta.get("req_r", "")}` |
| **R seed** | {meta.get("seed_r", "")} |
| **L request_id** | `{meta.get("req_l", "")}` |
| **L seed** | {meta.get("seed_l", "")} |
| **status** | working — decorative text L · cocoa prop hero R |
| **tier** | dial_mock |

## Layout (Flow v2)

- **L (p14):** Cream text page · snowman snow vignette above · coat/tie/ring ornaments below · open center for poem
- **R (p15):** Prop hero · Santa holding steaming cocoa with marshmallows · open-coat G0 v2
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
        unit="S06-cocoa",
        version=VERSION,
        day=DAY,
        tech="Qwen 2 Pro /edit · square · S3 v07 quality bar",
        subtitle="snowman + coat/tie/ring · cocoa prop hero",
    )
    print("board", out)


def upload_phase() -> dict:
    load_env()
    # quality crop for R — prefer left/fire side of S3 for hearth mood
    q = Image.open(QUALITY).convert("RGB")
    w, h = q.size
    side = min(w, h)
    crop = q.crop((0, 0, side, side))  # left/fire bias
    crop_path = ROOT / "scripts/_scratch/_s06_v01_quality_crop.png"
    crop.resize((1536, 1536), Image.Resampling.LANCZOS).save(crop_path, "PNG")
    cream = Image.new("RGB", (1536, 1536), (250, 244, 232))
    cream_path = ROOT / "scripts/_scratch/_s06_v01_cream_base.png"
    cream.save(cream_path, "PNG")
    urls = {
        "quality_crop": upload(crop_path, "s03-v07-s06-crop.png", (1536, 1536)),
        "santa": upload(SANTA, "santa-G0-s06.png"),
        "style": upload(STYLE, "style-lock-s06.png"),
        "cream": upload(cream_path, "cream-s06.png", (1536, 1536)),
        "prompt_r": PROMPT_R,
        "neg_r": NEG_R,
        "prompt_l": PROMPT_L,
        "neg_l": NEG_L,
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps({k: urls[k] for k in ("quality_crop", "santa", "style", "cream")}, indent=2))
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
    (DEV / "art-right.png").write_bytes(data_r)
    (DEV / "art-left.png").write_bytes(data_l)
    left = Image.open(io.BytesIO(data_l)).convert("RGB")
    right = Image.open(io.BytesIO(data_r)).convert("RGB")
    board = MOCKS / "_INDEX" / f"S06-cocoa-{VERSION}-text-image-{DAY}.png"
    build_board(left, right, board)
    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    print("saved", DEV / VERSION)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "upload":
        upload_phase()
    elif sys.argv[1] == "save":
        save_pair(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7])
    else:
        raise SystemExit("upload | save url_r seed_r req_r url_l seed_l req_l")
