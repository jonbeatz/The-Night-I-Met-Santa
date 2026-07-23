#!/usr/bin/env python3
"""S3 Eyes Met v01 — Flow v2 regen at S2-v05 quality bar. Qwen 2 Pro Edit."""
from __future__ import annotations

import io
import json
import os
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S03-eyes-met"
MOCKS = ROOT / "Media/generated/mocks/S03-eyes-met"
QUALITY = ROOT / "Media/development/S02-threshold/v05/art.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
DAY = "2026-07-22"
VERSION = "v01"
URLS_OUT = ROOT / "scripts/_scratch/_s03_v01_urls.json"

HARD_WARDROBE = (
    "HARD WARDROBE LOCK: Child wears oatmeal/taupe holly pajamas ONLY — warm beige/taupe with "
    "green holly leaves and red berries — match image 2. NOT bright white, NOT a red coat, "
    "NOT a Santa suit. Santa wears FULL red coat with black suspenders clearly visible ON TOP "
    "OF the red coat fabric, open relaxed collar — match image 3 (santa-G0-v2). NOT shirtsleeves alone."
)

PROMPT = (
    "Image 1 = QUALITY BAR and room DNA from the locked S2 Threshold spread — match its rich "
    "oil-painting saturation (deep burgundy walls, warm golds, luminous highlights), dramatic "
    "lighting contrast, deep atmospheric corner shadows, and heirloom storybook paint depth. "
    "Image 2 = boy character + oatmeal/taupe holly pajamas. "
    "Image 3 = Santa character + red coat with black suspenders over coat. "
    "Create a wide seamless TWO-PAGE Christmas storybook SPREAD (2:1) for S3 Eyes Met — "
    "the emotional centerpiece of the book. "
    "LEFT (p8): the boy facing toward Santa across the spread, mouth wide open in awe and wonder — "
    "jaw dropped — looking at Santa; eyes locked toward the right. "
    "RIGHT (p9): Santa on one knee on the floor among boxes, gifts, and ribbons, still near the "
    "presents under the Christmas tree, looking back at the boy — eyes meeting the boy's across "
    "the gutter. Warm, kind, magical. Suspenders visible over red coat. "
    "CONNECTION: eyes meet across the center fold — face-to-face hero moment. Continuous burgundy "
    "living room; wood floor and gift sea cross the middle; faces OFF the exact center fold but "
    "gazing toward each other. ONE Christmas tree. Same room world as image 1 quality. "
    "Paint quality MUST match image 1: rich oil-painting color, luminous tree glow, deep shadows "
    "in corners, warm intimate interior. Traditional children's Christmas picture-book, heavily "
    "painted gouache/soft watercolor with oil-painting richness, NOT colored pencil. Art only — no text. "
    + HARD_WARDROBE
)

NEGATIVE = (
    "flat lighting, washed out, pale walls, shirtsleeves Santa, no coat, bright white pajamas, "
    "Santa suit on child, two trees, eyes not meeting, looking away, text, letters, watermark, "
    "colored pencil, crayon, phone, modern UI, profile backs only, boy facing away from Santa"
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
        f"""# RECIPE — S03-eyes-met / {VERSION}

| Field | Value |
|-------|--------|
| **name** | S3 Eyes Met — face-to-face across gutter (Flow v2 regen) |
| **unit** | S03-eyes-met |
| **book page** | Flow v2 p8\\|9 · FULL SPREAD |
| **page role** | spread · emotional centerpiece |
| **version** | {VERSION} |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · refs: S02-v05 quality bar + boy-narrator-G0 + santa-G0-v2 |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **fal_url** | `{url}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — first Flow v2 Eyes Met dial at S2-v05 quality bar |
| **tier** | dial_mock |
| **gpt_pillar** | true (finals later — this is dial) |

## Brief (Flow v2)

LEFT: boy mouth wide open in awe, looking at Santa.  
RIGHT: Santa on one knee among gifts/ribbons, looking back at boy.  
Eyes meet across the gutter. Red coat + suspenders · holly PJs.  
Paint quality matches S2 Threshold v05 KEEP (quality bar).

## Poem ref

L: My jaw dropped when our eyes finally met…  
R: For there he was in all his splendor, brilliant white hair, red coat with suspenders.
""",
        encoding="utf-8",
    )


def build_board(im: Image.Image, out: Path) -> None:
    w, h = im.size
    mid = w // 2
    left = im.crop((0, 0, mid, h))
    right = im.crop((mid, 0, w, h))
    panel_h = 520
    sc = panel_h / h
    full_w = int(w * sc)
    full = im.resize((full_w, panel_h), Image.Resampling.LANCZOS)
    half_w = int(mid * sc)
    left_r = left.resize((half_w, panel_h), Image.Resampling.LANCZOS)
    right_r = right.resize((half_w, panel_h), Image.Resampling.LANCZOS)
    margin, gap, header, label = 28, 16, 72, 56
    sheet_w = margin * 2 + max(full_w, half_w * 2 + gap)
    sheet_h = margin * 2 + header + panel_h + label + gap + panel_h + label
    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S3 Eyes Met SPREAD — {VERSION} ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 44),
        "Flow v2 regen · eyes across gutter · quality bar = S2 Threshold v05",
        fill=(110, 100, 90),
        font=font(13),
    )
    y = margin + header
    sheet.paste(full, (margin, y))
    d.text((margin, y + panel_h + 8), "FULL SPREAD (p8|9 continuous)", fill=(32, 28, 24), font=font(16))
    y2 = y + panel_h + label + gap
    sheet.paste(left_r, (margin, y2))
    sheet.paste(right_r, (margin + half_w + gap, y2))
    d.text((margin, y2 + panel_h + 8), "LEFT half (p8) — awe", fill=(32, 28, 24), font=font(15))
    d.text((margin + half_w + gap, y2 + panel_h + 8), "RIGHT half (p9) — Santa looks back", fill=(32, 28, 24), font=font(15))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)


def upload_refs() -> dict:
    load_env()
    for p in (QUALITY, BOY, SANTA):
        if not p.is_file():
            raise SystemExit(f"missing {p}")
    urls = {
        "quality_s02_v05": upload(QUALITY, "s02-v05-quality-bar.png", (2048, 1024)),
        "boy": upload(BOY, "boy-narrator-G0.png"),
        "santa": upload(SANTA, "santa-G0-v2.png"),
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps(urls, indent=2))
    return urls


def save_result(url: str, seed: int, req_id: str) -> Path:
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    for vdir in (DEV / VERSION, MOCKS / VERSION):
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / "art.png").write_bytes(data)
        write_recipe(vdir, seed, req_id, url)
        (vdir / "meta.json").write_text(
            json.dumps(
                {
                    "version": VERSION,
                    "seed": seed,
                    "request_id": req_id,
                    "url": url,
                    "model": "fal-ai/qwen-image-2/pro/edit",
                    "refs": ["S02-v05-quality-bar", "boy-narrator-G0", "santa-G0-v2"],
                    "gpt_pillar": True,
                    "note": "dial pass — GPT pillar reserved for approved final later",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    im = Image.open(io.BytesIO(data)).convert("RGB")
    board = MOCKS / "_INDEX" / f"S03-eyes-met-comparison-spread-{VERSION}-{DAY}.png"
    build_board(im, board)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art.png")], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    print("saved", DEV / VERSION / "art.png", im.size)
    return DEV / VERSION / "art.png"


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "upload":
        upload_refs()
    elif len(sys.argv) > 1 and sys.argv[1] == "save":
        save_result(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        print("usage: upload | save <url> <seed> <req_id>")
