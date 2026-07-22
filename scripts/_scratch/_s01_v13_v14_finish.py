#!/usr/bin/env python3
"""S01 v13/v14 cracked-door dial — save, recipes, board, FLOW."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/generated/mocks/S01-approach"
DAY = "2026-07-22"

V13_URL = "https://v3b.fal.media/files/b/0aa351e0/0C1kJAwPEJlDIa5hpHysm_UqJPO3cb.png"
V14_URL = "https://v3b.fal.media/files/b/0aa351e0/_UcD5NPNSXFqtjdZInbHz_c4HGL97e.png"
V13_REQ = "019f8bae-507c-7440-aa35-11c0afa1d050"
V14_REQ = "019f8bae-50b0-7a02-bb38-39592ce57c5b"
V13_SEED = 2805836
V14_SEED = 670028878


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main() -> None:
    (BASE / "v13").mkdir(parents=True, exist_ok=True)
    (BASE / "v14").mkdir(parents=True, exist_ok=True)
    urlretrieve(V13_URL, BASE / "v13/art.png")
    urlretrieve(V14_URL, BASE / "v14/art.png")
    print("v13", Image.open(BASE / "v13/art.png").size)
    print("v14", Image.open(BASE / "v14/art.png").size)

    (BASE / "v13/RECIPE.md").write_text(
        f"""# RECIPE — S01-approach / v13

| Field | Value |
|-------|--------|
| **name** | S1 Approach L — narrow crack journey |
| **unit** | S01-approach |
| **book page** | Flow v2 p4 · SPLIT LEFT |
| **version** | v13 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: v11 (camera/chiaroscuro) + v12 (door/wreath) + boy-G0 |
| **seed** | {V13_SEED} |
| **request_id** | `{V13_REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — replaces v11 |
| **tier** | dial_mock |

## Brief

Keep v11 low crawl + chiaroscuro. Door cracked **4–6 in only**. Narrow beam through crack.
Wreath visible in dark door face. Holly PJs. Light teases — does not reveal all.
""",
        encoding="utf-8",
    )

    (BASE / "v14/RECIPE.md").write_text(
        f"""# RECIPE — S01-approach / v14

| Field | Value |
|-------|--------|
| **name** | S1 Approach R — face-on wider crack destination |
| **unit** | S01-approach |
| **book page** | Flow v2 p5 · SPLIT RIGHT |
| **version** | v14 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: v12 face-on + style-lock-v2 + door quality target |
| **seed** | {V14_SEED} |
| **request_id** | `{V14_REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — replaces v12 |
| **tier** | dial_mock |

## Brief

Face-on centered single door. Crack **6–8 in** (slightly wider than v13) · more floor spill.
Same wreath / tree peek / presents · rim both edges · light is the star.
""",
        encoding="utf-8",
    )

    panel, label_h = 960, 110
    gap, margin, header = 28, 36, 96
    slots = [
        (BASE / "v13/art.png", "v13 LEFT p4 — JOURNEY", "4–6 in crack · narrow beam · wreath in dark"),
        (BASE / "v14/art.png", "v14 RIGHT p5 — DESTINATION", "6–8 in crack · face-on · wider spill · rim"),
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
        d.text((14, panel + 12), title, fill=(32, 28, 24), font=font(20))
        d.text((14, panel + 46), sub, fill=(70, 64, 58), font=font(15))
        d.text((14, panel + 74), "Qwen 2 Pro /edit · ~$0.08 · crack is the story", fill=(90, 82, 74), font=font(13))
        cols.append(canvas)

    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S1 Approach SPLIT — v13 | v14 ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 46),
        "Same door / wreath / crack story   ·   L = narrow beam crawl   ·   R = face-on wider spill",
        fill=(110, 100, 90),
        font=font(13),
    )
    sheet.paste(cols[0], (margin, margin + header))
    sheet.paste(cols[1], (margin + panel + gap, margin + header))
    out = BASE / "_INDEX" / f"S01-approach-comparison-split-v13-v14-{DAY}.png"
    sheet.save(out, "PNG")
    print("board", out)

    flow_path = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
    flow = json.loads(flow_path.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    for plate in flow["plates"]:
        if plate["id"] == "p04":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v13/art.png",
                    "caption": "p4 · S1 Approach L · v13 narrow crack journey",
                    "version": "v13",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "v11 camera/chiaroscuro + 4–6in crack · wreath in dark · narrow beam",
                    "tier": "dial_mock",
                    "previous": "v11",
                }
            )
        if plate["id"] == "p05":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v14/art.png",
                    "caption": "p5 · S1 Approach R · v14 face-on wider crack",
                    "version": "v14",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Face-on · 6–8in crack · more spill · same wreath/door as v13",
                    "tier": "dial_mock",
                    "previous": "v12",
                }
            )
    for v in flow["verdicts"]:
        if v.get("beat") == "S1 Approach":
            v.update(
                {
                    "version": "v13|v14",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Crack is the story · narrow L / wider R · pending Jon eye",
                    "tier": "dial_mock",
                }
            )
    flow_path.write_text(json.dumps(flow, indent=2), encoding="utf-8")
    print("FLOW ok")


if __name__ == "__main__":
    main()
