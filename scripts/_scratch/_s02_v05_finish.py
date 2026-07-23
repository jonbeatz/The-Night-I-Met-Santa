#!/usr/bin/env python3
"""Save S02 v05 + v04 vs v05 comparison board."""
from __future__ import annotations

import io
import json
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S02-threshold"
MOCKS = ROOT / "Media/generated/mocks/S02-threshold"
DAY = "2026-07-22"
VERSION = "v05"
URL = "https://v3b.fal.media/files/b/0aa35ab6/uStcL2zNjTvsOUEgbRBK6_k1MhQ8or.png"
REQ = "019f8d05-4687-7c72-b547-793bc1b63642"
SEED = 1535542168
URLS = json.loads((ROOT / "scripts/_scratch/_s02_v05_urls.json").read_text(encoding="utf-8"))


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(vdir: Path) -> None:
    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S02-threshold / {VERSION}

| Field | Value |
|-------|--------|
| **name** | S2 Threshold — cover oil-painting light/depth on v04 layout |
| **unit** | S02-threshold |
| **book page** | Flow v2 p6\\|7 · FULL SPREAD |
| **page role** | spread |
| **version** | {VERSION} |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · edit v04 + style-lock-v2 + cover beige-v2 |
| **seed** | {SEED} |
| **request_id** | `{REQ}` |
| **fal_url** | `{URL}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — atmosphere pass on kept v04 composition |
| **tier** | dial_mock |
| **previous** | v04 |

## Intent

KEEP v04 composition (boy door L · Santa tree R · burgundy · holly PJs · red coat).  
ADD cover oil-painting richness: deeper corner shadows, luminous golden tree + hallway glow, richer burgundy, firelight/Christmas-light warmth.

## Refs used

1. v04 art (composition lock)
2. style-lock-v2
3. cover beige-v2 (`00-cover-front-APPROVED-beige-v2.png`)

Character wardrobe inherited from v04 (boy G0 + santa-G0-v2 already locked there).
""",
        encoding="utf-8",
    )


def build_compare(v04: Image.Image, v05: Image.Image, out: Path) -> None:
    panel_h = 480
    sc = panel_h / v04.height
    w = int(v04.width * sc)
    a = v04.convert("RGB").resize((w, panel_h), Image.Resampling.LANCZOS)
    b = v05.convert("RGB").resize((w, panel_h), Image.Resampling.LANCZOS)
    margin, gap, header, label = 28, 20, 70, 40
    sheet_w = margin * 2 + w
    sheet_h = margin * 2 + header + panel_h + label + gap + panel_h + label
    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S2 Threshold — v04 vs v05 ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 44),
        "v05 = same composition · cover oil-painting depth / glow / richer burgundy",
        fill=(110, 100, 90),
        font=font(13),
    )
    y = margin + header
    sheet.paste(a, (margin, y))
    d.text((margin, y + panel_h + 8), "v04 — KEEP composition", fill=(32, 28, 24), font=font(16))
    y2 = y + panel_h + label + gap
    sheet.paste(b, (margin, y2))
    d.text((margin, y2 + panel_h + 8), "v05 — atmosphere / oil richness pass", fill=(32, 28, 24), font=font(16))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)


def main() -> None:
    with urllib.request.urlopen(URL, timeout=180) as resp:
        data = resp.read()
    for vdir in (DEV / VERSION, MOCKS / VERSION):
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / "art.png").write_bytes(data)
        write_recipe(vdir)
        (vdir / "meta.json").write_text(
            json.dumps(
                {
                    "version": VERSION,
                    "seed": SEED,
                    "request_id": REQ,
                    "url": URL,
                    "model": "fal-ai/qwen-image-2/pro/edit",
                    "refs": ["v04", "style-lock-v2", "cover-beige-v2"],
                    "upload_urls": URLS,
                    "previous": "v04",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    v04 = Image.open(DEV / "v04" / "art.png").convert("RGB")
    v05 = Image.open(io.BytesIO(data)).convert("RGB")
    print("v05", v05.size)
    board = MOCKS / "_INDEX" / f"S02-threshold-v04-vs-v05-{DAY}.png"
    build_compare(v04, v05, board)
    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / "v04" / "art.png")], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art.png")], check=False)
    print("DONE")


if __name__ == "__main__":
    main()
