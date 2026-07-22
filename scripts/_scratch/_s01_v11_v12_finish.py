#!/usr/bin/env python3
"""S01 v11/v12 save, recipes, 2-panel board, FLOW-CURRENT."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/generated/mocks/S01-approach"
DAY = "2026-07-22"

V11_URL = "https://v3b.fal.media/files/b/0aa35192/xQeOkA3JUZLbZI8Il3OAD_QowjIDx4.png"
V12_URL = "https://v3b.fal.media/files/b/0aa35192/8g0uy9sFkHCAgQfWd0jvp_IxdmmF2Z.png"
V11_REQ = "019f8ba2-4e98-7322-9bb6-ade5ab177995"
V12_REQ = "019f8ba2-4ef7-7882-8b36-68690495f4c2"
V11_SEED = 69849197
V12_SEED = 2043525606


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main() -> None:
    (BASE / "v11").mkdir(parents=True, exist_ok=True)
    (BASE / "v12").mkdir(parents=True, exist_ok=True)
    urlretrieve(V11_URL, BASE / "v11/art.png")
    if not (BASE / "v12/art.png").is_file():
        urlretrieve(V12_URL, BASE / "v12/art.png")
    print("v11", Image.open(BASE / "v11/art.png").size)
    print("v12", Image.open(BASE / "v12/art.png").size)

    (BASE / "v11/RECIPE.md").write_text(
        f"""# RECIPE — S01-approach / v11

| Field | Value |
|-------|--------|
| **name** | S1 Approach L — chiaroscuro crawl / open portal |
| **unit** | S01-approach |
| **book page** | Flow v2 p4 · SPLIT LEFT (journey) |
| **version** | v11 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: best-of L chiaroscuro + style-lock-v2 + boy-G0 |
| **seed** | {V11_SEED} |
| **request_id** | `{V11_REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — replaces v09 as current L dial |
| **tier** | dial_mock |

## Brief

Camera/lighting from best-of `page-07-06-S01-approach-L.jpg` (Klein v01 chop).
Wide-open doorway as portal · child crawl from behind · dramatic chiaroscuro · holly PJs.
""",
        encoding="utf-8",
    )

    (BASE / "v12/RECIPE.md").write_text(
        f"""# RECIPE — S01-approach / v12

| Field | Value |
|-------|--------|
| **name** | S1 Approach R — face-on door destination ajar |
| **unit** | S01-approach |
| **book page** | Flow v2 p5 · SPLIT RIGHT (destination) |
| **version** | v12 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: door quality target + style-lock-v2 + santa-G0-v2 |
| **seed** | {V12_SEED} |
| **request_id** | `{V12_REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — replaces v10 as current R dial |
| **tier** | dial_mock |

## Brief

Face-on centered single door · slightly ajar · wreath · tree peek R · rim both edges.
Same room/light language as v11 · different camera purpose (destination page-turn).
""",
        encoding="utf-8",
    )

    panel, label_h = 960, 110
    gap, margin, header = 28, 36, 96
    slots = [
        (BASE / "v11/art.png", "v11 LEFT p4 — JOURNEY", "chiaroscuro crawl · open portal · holly PJs"),
        (BASE / "v12/art.png", "v12 RIGHT p5 — DESTINATION", "face-on door · ajar · wreath · rim light"),
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
        d.text((14, panel + 74), "Qwen 2 Pro /edit · ~$0.08 · style-lock-v2", fill=(90, 82, 74), font=font(13))
        cols.append(canvas)

    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S1 Approach SPLIT — v11 | v12 ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 46),
        "L = approach (open portal + chiaroscuro)   ·   R = destination (face-on ajar door)   ·   same room / light language",
        fill=(110, 100, 90),
        font=font(13),
    )
    sheet.paste(cols[0], (margin, margin + header))
    sheet.paste(cols[1], (margin + panel + gap, margin + header))
    out = BASE / "_INDEX" / f"S01-approach-comparison-split-v11-v12-{DAY}.png"
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
                    "path": "Media/generated/mocks/S01-approach/v11/art.png",
                    "caption": "p4 · S1 Approach L · v11 chiaroscuro open portal",
                    "version": "v11",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Best-of L lighting target · wide-open portal · crawl POV · holly PJs",
                    "tier": "dial_mock",
                    "previous": "v09",
                }
            )
        if plate["id"] == "p05":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v12/art.png",
                    "caption": "p5 · S1 Approach R · v12 face-on ajar destination",
                    "version": "v12",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Face-on single door ajar · wreath · rim both edges · tree peek R",
                    "tier": "dial_mock",
                    "previous": "v10",
                }
            )
    for v in flow["verdicts"]:
        if v.get("beat") == "S1 Approach":
            v.update(
                {
                    "version": "v11|v12",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Journey vs destination · chiaroscuro L + face-on ajar R · pending Jon eye",
                    "tier": "dial_mock",
                }
            )
    flow_path.write_text(json.dumps(flow, indent=2), encoding="utf-8")
    print("FLOW ok")


if __name__ == "__main__":
    main()
