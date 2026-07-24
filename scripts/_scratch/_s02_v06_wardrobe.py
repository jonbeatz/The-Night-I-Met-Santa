#!/usr/bin/env python3
"""S2 Threshold v06 — wardrobe-only: open-coat Santa G0 v2 on v05 composition."""
from __future__ import annotations

import io
import json
import os
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S02-threshold"
MOCKS = ROOT / "Media/generated/mocks/S02-threshold"
V05 = DEV / "v05" / "art.png"
SANTA = ROOT / "Media/approved/characters/santa-G0.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
DAY = "2026-07-22"
VERSION = "v06"
URLS_OUT = ROOT / "scripts/_scratch/_s02_v06_urls.json"

PROMPT = (
    "Edit image 1 ONLY — the locked S2 Threshold seamless spread (pages 6|7). "
    "KEEP everything identical: same layout, boy at doorway on LEFT with golden hallway spill, "
    "Santa on RIGHT at the tree placing gifts, burgundy walls, gift sea, one Christmas tree, "
    "warm oil-painting quality, same poses, same faces, same camera. "
    "Image 2 = Santa G0 wardrobe lock. Image 3 = paint style lock. "
    "ONE CHANGE ONLY: update Santa's wardrobe to G0 v2 open-coat look. "
    "Red coat worn OPEN and unbuttoned — hanging open at the sides, framing his torso — "
    "NOT closed, NOT a solid red block, NOT shirtsleeves alone. "
    "White fur trim clearly visible on coat cuffs and hem. "
    "UNDER the open coat: cream/off-white vertically striped button-down shirt clearly visible, "
    "with brown leather suspenders OVER the striped shirt (NOT over the coat fabric). "
    "Red pants and black boots unchanged. "
    "Do not move Santa, do not flip the room, do not change the boy or doorway. Art only — no text."
)

NEGATIVE = (
    "shirtsleeves only, no coat, missing coat, closed coat, buttoned coat, solid red block, "
    "suspenders over coat, coat covering shirt completely, flipped room, Santa on left, "
    "moved characters, new layout, cream walls, text, letters, watermark"
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
        f"""# RECIPE — S02-threshold / {VERSION}

| Field | Value |
|-------|--------|
| **name** | S2 Threshold — open-coat wardrobe fix on v05 |
| **unit** | S02-threshold |
| **book page** | Flow v2 p6\\|7 · FULL SPREAD |
| **version** | {VERSION} |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · edit v05 + santa-G0 + style-lock-v2 |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **fal_url** | `{url}` |
| **status** | working — wardrobe-only (open-coat Santa G0 v2) |
| **tier** | dial_mock |
| **previous** | v05 KEEP composition |

## Intent

KEEP v05 composition + doorway golden-spill quality.  
ONE CHANGE: Santa open red coat · cream striped shirt · brown suspenders over shirt.

## Refs

1. v05 art (composition lock)
2. santa-G0.png (wardrobe)
3. style-lock-v2.png
""",
        encoding="utf-8",
    )


def build_board(before: Image.Image, after: Image.Image, out: Path) -> None:
    # show right half (Santa) for wardrobe check
    def rh(im: Image.Image, w: int = 520, h: int = 520) -> Image.Image:
        im = im.convert("RGB")
        W, H = im.size
        crop = im.crop((W // 2, 0, W, H)).resize((w, h), Image.Resampling.LANCZOS)
        return crop

    b, a = rh(before), rh(after)
    margin, gap, header = 28, 20, 70
    sheet = Image.new("RGB", (margin * 2 + 520 * 2 + gap, margin * 2 + header + 520 + 48), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S2 Threshold — {VERSION} wardrobe fix ({DAY})", fill=(28, 24, 20), font=font(22))
    d.text((margin, 42), "R-half crop · v05 KEEP vs v06 open-coat · composition locked", fill=(110, 100, 90), font=font(13))
    y = margin + header
    sheet.paste(b, (margin, y))
    sheet.paste(a, (margin + 520 + gap, y))
    d.text((margin, y + 520 + 10), "v05 BEFORE (R half)", fill=(32, 28, 24), font=font(15))
    d.text((margin + 520 + gap, y + 520 + 10), "v06 AFTER open-coat", fill=(32, 28, 24), font=font(15))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)


def upload_phase() -> dict:
    load_env()
    urls = {
        "comp": upload(V05, "s02-v05-comp.png", (2048, 1024)),
        "santa": upload(SANTA, "santa-G0-s02.png"),
        "style": upload(STYLE, "style-lock-s02.png"),
        "prompt": PROMPT,
        "negative": NEGATIVE,
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps({k: urls[k] for k in ("comp", "santa", "style")}, indent=2))
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
                    "previous": "v05",
                    "task": "wardrobe_fix_open_coat",
                    "url": url,
                    "seed": seed,
                    "request_id": req_id,
                    "model": "fal-ai/qwen-image-2/pro/edit",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    # Do NOT promote dashboard art.png until Jon keeps — leave v05 as dashboard until lock
    before = Image.open(V05).convert("RGB")
    after = Image.open(io.BytesIO(data)).convert("RGB")
    board = MOCKS / "_INDEX" / f"S02-threshold-{VERSION}-wardrobe-{DAY}.png"
    build_board(before, after, board)
    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art.png")], check=False)
    print("saved", DEV / VERSION, "(dashboard art.png still v05 until KEEP)")


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "upload":
        upload_phase()
    elif sys.argv[1] == "save":
        save(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        raise SystemExit("upload | save url seed req_id")
