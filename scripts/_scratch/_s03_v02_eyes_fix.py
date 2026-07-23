#!/usr/bin/env python3
"""S3 Eyes Met v02 — fix eyes meeting + suspenders over coat. Edit v01."""
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
V01 = DEV / "v01" / "art.png"
QUALITY = ROOT / "Media/development/S02-threshold/v05/art.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
DAY = "2026-07-22"
VERSION = "v02"
URLS_OUT = ROOT / "scripts/_scratch/_s03_v02_urls.json"

PROMPT = (
    "Edit image 1 ONLY — the S3 Eyes Met spread. KEEP composition, room, gift sea, "
    "burgundy walls, warm golden tree light, rich oil-painting quality, poses and positions. "
    "Image 2 = boy face/character reference. Image 3 = Santa G0 v2 wardrobe lock "
    "(black suspenders OVER red coat). "
    "TWO CRITICAL FIXES ONLY: "
    "(1) EYES MUST MEET — this is the emotional centerpiece. The boy's wide-eyed gaze locks "
    "DIRECTLY onto Santa's face. Santa looks BACK at the boy with a warm, kind expression. "
    "Their eyes connect across the spread — true eye contact, mutual recognition, the moment "
    "they see each other. Boy mouth still open in awe. Do NOT have either looking past or away. "
    "(2) Santa's black suspenders must sit ON TOP of the red coat fabric — visible over the coat, "
    "NOT under the coat on a shirt. Match image 3 exactly: red coat first, then black suspenders "
    "on top, open relaxed collar. "
    "Do not redesign the scene, move figures, change the gift sea, or flatten the lighting. Art only."
)

NEGATIVE = (
    "eyes not meeting, looking away, looking past, averted gaze, suspenders under coat, "
    "suspenders on shirt only, shirtsleeves only, no coat, redesign, new composition, "
    "flat lighting, text, letters, watermark"
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
| **name** | S3 Eyes Met — eye contact + suspenders-over-coat fix |
| **unit** | S03-eyes-met |
| **book page** | Flow v2 p8\\|9 · FULL SPREAD |
| **page role** | spread · emotional centerpiece |
| **version** | {VERSION} |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · edit v01 + boy-narrator-G0 + santa-G0-v2 |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **fal_url** | `{url}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — eyes meet + suspenders over coat |
| **tier** | dial_mock |
| **previous** | v01 |
| **gpt_pillar** | true (finals later) |

## Fixes vs v01

1. Eyes lock — boy gaze → Santa face; Santa looks back warm/kind (true eye contact across spread)
2. Black suspenders visible **over** red coat (santa-G0-v2)

Quality kept: oil-painting richness, burgundy walls, warm golden light, gift sea.
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
        "Fixes: true eye contact across gutter · suspenders OVER red coat (santa-G0-v2)",
        fill=(110, 100, 90),
        font=font(13),
    )
    y = margin + header
    sheet.paste(full, (margin, y))
    d.text((margin, y + panel_h + 8), "FULL SPREAD (p8|9)", fill=(32, 28, 24), font=font(16))
    y2 = y + panel_h + label + gap
    sheet.paste(left_r, (margin, y2))
    sheet.paste(right_r, (margin + half_w + gap, y2))
    d.text((margin, y2 + panel_h + 8), "LEFT (p8)", fill=(32, 28, 24), font=font(15))
    d.text((margin + half_w + gap, y2 + panel_h + 8), "RIGHT (p9)", fill=(32, 28, 24), font=font(15))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)


def upload_refs() -> dict:
    load_env()
    # Same character/quality family as v01, but v01 is composition base for the edit.
    # Max 3: v01 + boy + santa (quality already baked into v01).
    urls = {
        "v01": upload(V01, "s03-v01-base.png", (2048, 1024)),
        "boy": upload(BOY, "boy-narrator-G0.png"),
        "santa": upload(SANTA, "santa-G0-v2.png"),
        "quality_note": str(QUALITY),  # not uploaded — inherited via v01 paint
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in urls.items() if k != "quality_note"}, indent=2))
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
                    "refs": ["v01", "boy-narrator-G0", "santa-G0-v2"],
                    "previous": "v01",
                    "fixes": ["eyes meet", "suspenders over coat"],
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


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "upload":
        upload_refs()
    elif sys.argv[1] == "save":
        save_result(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        raise SystemExit("upload | save <url> <seed> <req_id>")
