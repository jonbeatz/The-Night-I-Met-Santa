#!/usr/bin/env python3
"""S01 v09/v10 download, recipes, 2-panel board, FLOW-CURRENT."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/generated/mocks/S01-approach"
DAY = "2026-07-22"

V09_URL = "https://v3b.fal.media/files/b/0aa3511b/a-oG83LJD7Y1qmqE_abFn_uYqbc2QU.png"
V10_URL = "https://v3b.fal.media/files/b/0aa3511b/bvsi1TF7dfuH45SNLgILi_o1lzoiUN.png"
V09_REQ = "019f8b90-3f09-72b3-bfb0-de3fa3459386"
V10_REQ = "019f8b90-3f54-7250-b0cf-dcb594ad4b09"
V09_SEED = 1952326451
V10_SEED = 1492024998


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main() -> None:
    (BASE / "v09").mkdir(parents=True, exist_ok=True)
    (BASE / "v10").mkdir(parents=True, exist_ok=True)
    if not (BASE / "v09/art.png").is_file():
        urlretrieve(V09_URL, BASE / "v09/art.png")
    urlretrieve(V10_URL, BASE / "v10/art.png")
    print("v09", Image.open(BASE / "v09/art.png").size)
    print("v10", Image.open(BASE / "v10/art.png").size)

    (BASE / "v09/RECIPE.md").write_text(
        f"""# RECIPE — S01-approach / v09

| Field | Value |
|-------|--------|
| **name** | S1 Approach L — v05 angle + v07 ajar door |
| **unit** | S01-approach |
| **book page** | Flow v2 p4 · SPLIT LEFT |
| **version** | v09 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: v05 (camera) + v07 (door) + boy-G0 |
| **seed** | {V09_SEED} |
| **request_id** | `{V09_REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — replaces v07 |
| **tier** | dial_mock |

## Fix

Combine **v05 L camera** (low behind-the-child crawl POV) with **v07 door state** (single decorated door ajar 4–6 in, light through gap, wreath). Burgundy walls · holly PJs.
""",
        encoding="utf-8",
    )

    (BASE / "v10/RECIPE.md").write_text(
        f"""# RECIPE — S01-approach / v10

| Field | Value |
|-------|--------|
| **name** | S1 Approach R — single solid door ajar |
| **unit** | S01-approach |
| **book page** | Flow v2 p5 · SPLIT RIGHT |
| **version** | v10 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: v08 (lighting/comp) + door quality target + style-lock-v2 |
| **seed** | {V10_SEED} |
| **request_id** | `{V10_REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — replaces v08 |
| **tier** | dial_mock |

## Fix

Keep v08 rim light / tree peek / presents. **ONE solid single-panel door** (not double doors). Wreath centered. Slightly ajar with warm light through crack + under door.
""",
        encoding="utf-8",
    )

    panel, label_h = 960, 100
    gap, margin, header = 28, 36, 78
    slots = [
        (BASE / "v09/art.png", "v09 LEFT p4", "v05 low crawl angle + v07 ajar wreath door"),
        (BASE / "v10/art.png", "v10 RIGHT p5", "single solid door · ajar · rim light · tree peek"),
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
        "L: v05 camera + v07 ajar door   ·   R: single solid door (not double) + v08 lighting",
        fill=(110, 100, 90),
        font=font(14),
    )
    sheet.paste(cols[0], (margin, margin + header))
    sheet.paste(cols[1], (margin + panel + gap, margin + header))
    out = BASE / "_INDEX" / f"S01-approach-comparison-split-v09-v10-{DAY}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)

    flow_path = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
    flow = json.loads(flow_path.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    for plate in flow["plates"]:
        if plate["id"] == "p04":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v09/art.png",
                    "caption": "p4 · S1 Approach L · v09 (v05 angle + v07 ajar)",
                    "version": "v09",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Low behind-child crawl POV from v05 + ajar wreath door from v07",
                    "tier": "dial_mock",
                    "previous": "v07",
                }
            )
        if plate["id"] == "p05":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v10/art.png",
                    "caption": "p5 · S1 Approach R · v10 single solid door",
                    "version": "v10",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "v08 lighting/comp but ONE solid door ajar — not double doors",
                    "tier": "dial_mock",
                    "previous": "v08",
                }
            )
    for v in flow["verdicts"]:
        if v.get("beat") == "S1 Approach":
            v.update(
                {
                    "version": "v09|v10",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Angle+single-door polish · pending Jon eye",
                    "tier": "dial_mock",
                }
            )
    flow_path.write_text(json.dumps(flow, indent=2), encoding="utf-8")
    print("FLOW ok")


if __name__ == "__main__":
    main()
