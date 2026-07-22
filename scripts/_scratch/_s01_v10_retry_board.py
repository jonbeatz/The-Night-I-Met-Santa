#!/usr/bin/env python3
"""Rebuild v09|v10 board after v10 single-door retry."""
from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/generated/mocks/S01-approach"
DAY = "2026-07-22"
V10_URL = "https://v3b.fal.media/files/b/0aa3512b/viIliNg2UqYj70KEdCu6__T2fkNg9i.png"


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main() -> None:
    urlretrieve(V10_URL, BASE / "v10/art.png")
    print("v10", Image.open(BASE / "v10/art.png").size)

    (BASE / "v10/RECIPE.md").write_text(
        """# RECIPE — S01-approach / v10

| Field | Value |
|-------|--------|
| **name** | S1 Approach R — single solid door ajar |
| **unit** | S01-approach |
| **book page** | Flow v2 p5 · SPLIT RIGHT |
| **version** | v10 |
| **date** | 2026-07-22 |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: door quality target + v07 ajar + style-lock-v2 |
| **seed** | 851286933 |
| **request_id** | `019f8b92-9c75-7012-9032-4f92b211819d` |
| **cost_note** | ~$0.08 (retry; first attempt still double-door from v08 ref) |
| **output** | art.png |
| **status** | working — replaces v08 |
| **tier** | dial_mock |

## Fix

ONE solid single-panel door. Wreath centered unbroken. Ajar on latch/right edge only.
Rim light · tree peek R · presents. Avoided v08 as ref (it taught the center split).
""",
        encoding="utf-8",
    )

    panel, label_h = 960, 100
    gap, margin, header = 28, 36, 78
    slots = [
        (BASE / "v09/art.png", "v09 LEFT p4", "v05 low crawl angle + v07 ajar wreath door"),
        (BASE / "v10/art.png", "v10 RIGHT p5", "single solid door · ajar latch edge · rim light"),
    ]
    cols = []
    for path, title, sub in slots:
        im = Image.open(path).convert("RGB")
        box = panel - 16
        w, h = im.size
        sc = box / max(w, h)
        im = im.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (panel, panel + label_h), (245, 240, 232))
        canvas.paste(im, ((panel - im.width) // 2, 8 + (box - im.height) // 2))
        d = ImageDraw.Draw(canvas)
        d.text((14, panel + 12), title, fill=(32, 28, 24), font=font(22))
        d.text((14, panel + 46), sub, fill=(70, 64, 58), font=font(15))
        d.text((14, panel + 72), "Qwen 2 Pro /edit · ~$0.08 · continuity Option A", fill=(90, 82, 74), font=font(13))
        cols.append(canvas)

    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 16), f"S1 Approach SPLIT — v09 | v10 ({DAY})", fill=(28, 24, 20), font=font(26))
    d.text(
        (margin, 48),
        "L: v05 camera + v07 ajar door   ·   R: single solid door retry (quality target + v07)",
        fill=(110, 100, 90),
        font=font(14),
    )
    sheet.paste(cols[0], (margin, margin + header))
    sheet.paste(cols[1], (margin + panel + gap, margin + header))
    out = BASE / "_INDEX" / f"S01-approach-comparison-split-v09-v10-{DAY}.png"
    sheet.save(out, "PNG")
    print("board", out)


if __name__ == "__main__":
    main()
