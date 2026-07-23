#!/usr/bin/env python3
"""S3 Eyes Met v06 — keep v04 layout; open-coat Santa wardrobe lock (santa-G0)."""
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
V04 = DEV / "v04" / "art.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
SANTA = ROOT / "Media/approved/characters/santa-G0.png"  # standing wardrobe sheet Jon locked
DAY = "2026-07-22"
VERSION = "v06"
URLS_OUT = ROOT / "scripts/_scratch/_s03_v06_urls.json"

PROMPT = (
    "Edit image 1 ONLY — the S3 Eyes Met spread. KEEP everything identical except Santa's outfit: "
    "same room layout, fireplace FAR LEFT with stockings/garland, boy in oatmeal/taupe holly PJs "
    "on the left with mouth open in awe, Christmas tree FAR RIGHT, gift sea on the floor, deep "
    "burgundy walls, warm golden firelight and tree glow, rich oil-painting quality. "
    "KEEP eyes meeting — boy's gaze locked on Santa, Santa looking back warm and kind. "
    "Image 2 = watercolor/gouache paint style (style-lock). "
    "Image 3 = Santa wardrobe lock (santa-G0) — match this outfit EXACTLY. "
    "ONLY CHANGE: Santa's clothing. Red coat worn OPEN and unbuttoned — not closed, not a solid "
    "red block. Cream/off-white vertically striped button-down shirt clearly visible underneath. "
    "Brown leather suspenders over the striped shirt (NOT over the coat fabric). Red pants, black "
    "boots, white fur trim on cuffs and hem. Relaxed approachable grandfather-like — not a formal "
    "costume. Santa still on one knee among gifts holding a present. Art only — no text."
)

NEGATIVE = (
    "closed coat, buttoned coat, solid red block coat, suspenders over coat, black suspenders on coat, "
    "no shirt visible, formal costume Santa, eyes not meeting, looking away, cream walls, beige walls, "
    "moved characters, new layout, missing fireplace, missing tree, text, letters, watermark"
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
| **name** | S3 Eyes Met — open-coat Santa wardrobe lock |
| **unit** | S03-eyes-met |
| **book page** | Flow v2 p8\\|9 · FULL SPREAD |
| **version** | {VERSION} |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · edit v04 + style-lock-v2 + santa-G0.png |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **fal_url** | `{url}` |
| **status** | working — open coat · striped shirt · brown suspenders over shirt |
| **previous** | v04 |

## Change vs v04

Santa outfit only → open red coat, cream striped shirt, brown leather suspenders **over shirt** (santa-G0 lock).  
Keep: layout, fireplace, tree, gift sea, burgundy walls, boy holly PJs, eyes meeting.
""",
        encoding="utf-8",
    )


def build_board(im: Image.Image, out: Path) -> None:
    w, h = im.size
    mid = w // 2
    panel_h = 480
    sc = panel_h / h
    full = im.resize((int(w * sc), panel_h), Image.Resampling.LANCZOS)
    left = im.crop((0, 0, mid, h)).resize((int(mid * sc), panel_h), Image.Resampling.LANCZOS)
    right = im.crop((mid, 0, w, h)).resize((int(mid * sc), panel_h), Image.Resampling.LANCZOS)
    margin, gap, header, label = 28, 16, 72, 48
    sheet_w = margin * 2 + max(full.width, left.width * 2 + gap)
    sheet_h = margin * 2 + header + panel_h + label + gap + panel_h + label
    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S3 Eyes Met — {VERSION} ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 44),
        "Open-coat Santa lock · brown suspenders over striped shirt · layout from v04",
        fill=(110, 100, 90),
        font=font(13),
    )
    y = margin + header
    sheet.paste(full, (margin, y))
    d.text((margin, y + panel_h + 8), "FULL SPREAD", fill=(32, 28, 24), font=font(16))
    y2 = y + panel_h + label + gap
    sheet.paste(left, (margin, y2))
    sheet.paste(right, (margin + left.width + gap, y2))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)


def upload_refs() -> dict:
    load_env()
    urls = {
        "v04": upload(V04, "s03-v04-base.png", (2048, 1024)),
        "style": upload(STYLE, "style-lock-v2.png"),
        "santa": upload(SANTA, "santa-G0.png"),
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps(urls, indent=2))
    return urls


def save_result(url: str, seed: int, req_id: str) -> None:
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
                    "refs": ["v04", "style-lock-v2", "santa-G0.png"],
                    "santa_wardrobe": "open coat · striped shirt · brown suspenders over shirt",
                    "previous": "v04",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    im = Image.open(io.BytesIO(data)).convert("RGB")
    board = MOCKS / "_INDEX" / f"S03-eyes-met-comparison-spread-{VERSION}-{DAY}.png"
    build_board(im, board)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art.png")], check=False)
    print("saved", DEV / VERSION / "art.png", im.size)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "upload":
        upload_refs()
    elif sys.argv[1] == "save":
        save_result(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        raise SystemExit("upload | save <url> <seed> <req_id>")
