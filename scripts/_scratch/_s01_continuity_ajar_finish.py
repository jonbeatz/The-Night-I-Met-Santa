#!/usr/bin/env python3
"""Download S01 v07/v08, recipes, 4-panel board, FLOW-CURRENT update."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/generated/mocks/S01-approach"
DAY = "2026-07-22"

V07_URL = "https://v3b.fal.media/files/b/0aa350f3/_QLIh_kbPWvXFocWpsyL5_F3DwNBAS.png"
V08_URL = "https://v3b.fal.media/files/b/0aa350f3/yeH4Ky292JLvLqyj0FQxw_13OL9Yvc.png"
V07_REQ = "019f8b8a-2124-7e40-ad33-577abd8dc75b"
V08_REQ = "019f8b8a-21bd-7611-9a1a-c675489a98f9"
V07_SEED = 2097333023
V08_SEED = 55764007


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main() -> None:
    (BASE / "v07").mkdir(parents=True, exist_ok=True)
    (BASE / "v08").mkdir(parents=True, exist_ok=True)
    urlretrieve(V07_URL, BASE / "v07/art.png")
    print("v07", Image.open(BASE / "v07/art.png").size)
    if not (BASE / "v08/art.png").is_file():
        urlretrieve(V08_URL, BASE / "v08/art.png")
    print("v08", Image.open(BASE / "v08/art.png").size)

    (BASE / "v07/RECIPE.md").write_text(
        f"""# RECIPE — S01-approach / v07

| Field | Value |
|-------|--------|
| **name** | S1 Approach L — same door ajar (continuity) |
| **unit** | S01-approach |
| **book page** | Flow v2 p4 · SPLIT LEFT |
| **version** | v07 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: S01-R door quality target + style-lock-v2 + boy-G0 |
| **seed** | {V07_SEED} |
| **request_id** | `{V07_REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — continuity fix vs v05 |
| **tier** | dial_mock |

## Continuity (Option A)

Same decorated door as v08. Door slightly ajar 4–6 in — tree glow / gifts through gap.
Burgundy hall · holly PJs · wreath visible on door face · light under + through crack.

## Refs

1. `mockup-quality/S01-approach-R-quality-target.jpg` (door identity)
2. `style-lock-v2.png` (Krea atmosphere)
3. `boy-narrator-G0.png`
""",
        encoding="utf-8",
    )

    (BASE / "v08/RECIPE.md").write_text(
        f"""# RECIPE — S01-approach / v08

| Field | Value |
|-------|--------|
| **name** | S1 Approach R — same door ajar (continuity) |
| **unit** | S01-approach |
| **book page** | Flow v2 p5 · SPLIT RIGHT |
| **version** | v08 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: S01-R door quality target + style-lock-v2 |
| **seed** | {V08_SEED} |
| **request_id** | `{V08_REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — continuity fix vs v06 |
| **tier** | dial_mock |

## Continuity (Option A)

Same decorated door as v07, closer door-face view. Slightly ajar · rim light · tree peek R · presents at base · wreath + red bow.

## Refs

1. `mockup-quality/S01-approach-R-quality-target.jpg` (door identity)
2. `style-lock-v2.png` (Krea atmosphere)
""",
        encoding="utf-8",
    )

    # 4-panel: top v05|v06, bottom v07|v08
    panel, label_h, gap, margin, header = 720, 88, 20, 28, 86
    slots = [
        (BASE / "v05/art.png", "PREVIOUS v05 L", "wide-open doorway · continuity break"),
        (BASE / "v06/art.png", "PREVIOUS v06 R", "closed decorated door"),
        (BASE / "v07/art.png", "NEW v07 L", "same door · ajar 4–6 in · crawl"),
        (BASE / "v08/art.png", "NEW v08 R", "same door · ajar · rim light"),
    ]
    cols = []
    for path, title, sub in slots:
        im = Image.open(path).convert("RGB")
        box = panel - 12
        w, h = im.size
        sc = box / max(w, h)
        im = im.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (panel, panel + label_h), (245, 240, 232))
        canvas.paste(im, ((panel - im.width) // 2, 6 + (box - im.height) // 2))
        d = ImageDraw.Draw(canvas)
        d.text((12, panel + 10), title, fill=(32, 28, 24), font=font(18))
        d.text((12, panel + 42), sub, fill=(70, 64, 58), font=font(14))
        d.text((12, panel + 64), "Qwen 2 Pro /edit · ~$0.08", fill=(90, 82, 74), font=font(12))
        cols.append(canvas)

    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + (panel + label_h) * 2 + gap + 28
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text(
        (margin, 14),
        f"S1 Approach continuity — ajar door Option A ({DAY})",
        fill=(28, 24, 20),
        font=font(24),
    )
    d.text(
        (margin, 46),
        "TOP = previous v05|v06 (open hall vs closed door)   ·   BOTTOM = new v07|v08 (one door, two views, slightly ajar)",
        fill=(110, 100, 90),
        font=font(13),
    )
    d.text((margin, margin + header - 4), "PREVIOUS", fill=(140, 90, 70), font=font(14))
    sheet.paste(cols[0], (margin, margin + header + 18))
    sheet.paste(cols[1], (margin + panel + gap, margin + header + 18))
    y2 = margin + header + 18 + panel + label_h + gap
    d.text((margin, y2 - 22), "NEW — same door continuity", fill=(70, 110, 80), font=font(14))
    sheet.paste(cols[2], (margin, y2))
    sheet.paste(cols[3], (margin + panel + gap, y2))
    out = BASE / "_INDEX" / f"S01-approach-comparison-continuity-ajar-{DAY}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)

    # also 2-panel current pair
    panel2 = 900
    cols2 = []
    for path, title, sub in [
        (BASE / "v07/art.png", "v07 LEFT p4", "crawl · decorated door ajar"),
        (BASE / "v08/art.png", "v08 RIGHT p5", "same door · ajar · wreath · rim"),
    ]:
        im = Image.open(path).convert("RGB")
        box = panel2 - 16
        w, h = im.size
        sc = box / max(w, h)
        im = im.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (panel2, panel2 + 100), (245, 240, 232))
        canvas.paste(im, ((panel2 - im.width) // 2, 8 + (box - im.height) // 2))
        d = ImageDraw.Draw(canvas)
        d.text((12, panel2 + 10), title, fill=(32, 28, 24), font=font(20))
        d.text((12, panel2 + 42), sub, fill=(70, 64, 58), font=font(15))
        d.text((12, panel2 + 68), "Option A continuity · Qwen /edit", fill=(90, 82, 74), font=font(14))
        cols2.append(canvas)
    w2 = 36 * 2 + panel2 * 2 + 28
    h2 = 36 * 2 + 72 + panel2 + 100
    sheet2 = Image.new("RGB", (w2, h2), (252, 248, 240))
    d = ImageDraw.Draw(sheet2)
    d.text((36, 18), f"S1 Approach SPLIT — current dials v07|v08 ({DAY})", fill=(28, 24, 20), font=font(24))
    sheet2.paste(cols2[0], (36, 36 + 72))
    sheet2.paste(cols2[1], (36 + panel2 + 28, 36 + 72))
    out2 = BASE / "_INDEX" / f"S01-approach-comparison-split-v07-v08-{DAY}.png"
    sheet2.save(out2, "PNG")
    print("board2", out2)

    flow_path = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
    flow = json.loads(flow_path.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    for plate in flow["plates"]:
        if plate["id"] == "p04":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v07/art.png",
                    "caption": "p4 · S1 Approach L · v07 ajar door continuity",
                    "version": "v07",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Option A: same decorated door as p5, slightly ajar; replaces v05 open doorway",
                    "tier": "dial_mock",
                    "previous": "v05",
                }
            )
        if plate["id"] == "p05":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v08/art.png",
                    "caption": "p5 · S1 Approach R · v08 ajar door continuity",
                    "version": "v08",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Option A: same door as p4, slightly ajar + rim light; replaces v06 sealed door",
                    "tier": "dial_mock",
                    "previous": "v06",
                }
            )
    for v in flow["verdicts"]:
        if v.get("beat") == "S1 Approach":
            v.update(
                {
                    "version": "v07|v08",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Continuity Option A — one door two views, slightly ajar · pending Jon eye",
                    "tier": "dial_mock",
                }
            )
    flow_path.write_text(json.dumps(flow, indent=2), encoding="utf-8")
    print("FLOW ok")


if __name__ == "__main__":
    main()
