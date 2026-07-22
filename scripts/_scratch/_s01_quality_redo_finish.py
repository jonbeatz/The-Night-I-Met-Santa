#!/usr/bin/env python3
"""Save S01 v05/v06 recipes, boards, update FLOW-CURRENT."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/generated/mocks/S01-approach"
DAY = "2026-07-22"


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main() -> None:
    urlretrieve(
        "https://v3b.fal.media/files/b/0aa350aa/jtmAM0srZfL8r_5rYQLCG_6EgbTBqs.png",
        BASE / "v05/art.png",
    )
    print("v05", Image.open(BASE / "v05/art.png").size)

    (BASE / "v05/RECIPE.md").write_text(
        """# RECIPE — S01-approach / v05

| Field | Value |
|-------|--------|
| **name** | S1 Approach L — quality-target redo |
| **unit** | S01-approach |
| **book page** | Flow v2 p4 · SPLIT LEFT |
| **version** | v05 |
| **date** | 2026-07-22 |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: S01-L quality target + style-lock-v2 + boy-G0 |
| **seed** | 1827399533 |
| **request_id** | `019f8b7e-ed1f-76d0-b454-41b176b31460` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — replaces v03 as current dial |
| **tier** | dial_mock |

## Quality target source

`Media/approved/style-refs/mockup-quality/S01-approach-L-quality-target.jpg`

From best-of chop of **S01-approach/v01** — **Klein 9B** · 1536x768 dial · 2026-07-21 flow keep.

## Notes

Composition/lighting match quality target; atmosphere from style-lock-v2; boy from G0.
""",
        encoding="utf-8",
    )

    (BASE / "v06/RECIPE.md").write_text(
        """# RECIPE — S01-approach / v06

| Field | Value |
|-------|--------|
| **name** | S1 Approach R — door quality-target redo |
| **unit** | S01-approach |
| **book page** | Flow v2 p5 · SPLIT RIGHT |
| **version** | v06 |
| **date** | 2026-07-22 |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: S01-R door quality target + style-lock-v2 + santa-G0-v2 |
| **seed** | 884662663 |
| **request_id** | `019f8b7e-ed01-7172-bc7b-3805bd97ebc8` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — replaces v04 as current dial |
| **tier** | dial_mock |

## Quality target source

`Media/approved/style-refs/mockup-quality/S01-approach-R-quality-target.jpg`

From best-of chop of **S01-approach/v01** — **Klein 9B** · 1536x768 dial · 2026-07-21 flow keep.

Target traits: fuller wreath · tree peek right · presents at base · dramatic rim lighting on door frame.

## Notes

Jon preferred this door look over v04. Use this quality target on future Qwen mock-ups.
""",
        encoding="utf-8",
    )

    # 4-panel board
    panel, label_h, gap, margin, header = 640, 96, 18, 28, 78
    slots = [
        (
            ROOT / "Media/approved/style-refs/mockup-quality/S01-approach-L-quality-target.jpg",
            "QUALITY TARGET L",
            "Klein 9B v01 chop · best-of",
        ),
        (BASE / "v05/art.png", "v05 NEW L", "Qwen /edit · ~$0.08"),
        (
            ROOT / "Media/approved/style-refs/mockup-quality/S01-approach-R-quality-target.jpg",
            "QUALITY TARGET R",
            "Klein 9B v01 chop · door hero",
        ),
        (BASE / "v06/art.png", "v06 NEW R", "Qwen /edit · ~$0.08"),
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
        d.text((10, panel + 8), title, fill=(32, 28, 24), font=font(16))
        d.text((10, panel + 36), sub, fill=(70, 64, 58), font=font(13))
        d.text((10, panel + 58), "quality target vs new dial", fill=(90, 82, 74), font=font(12))
        cols.append(canvas)

    w = margin * 2 + panel * 4 + gap * 3
    h = margin * 2 + header + panel + label_h
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 16), f"S1 Approach — quality-target redo ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 46),
        "Target = Klein 9B v01 best-of chops  ·  New = Qwen 2 Pro /edit + style-lock-v2 + G0",
        fill=(110, 100, 90),
        font=font(13),
    )
    x = margin
    for c in cols:
        sheet.paste(c, (x, margin + header))
        x += panel + gap
    out = BASE / "_INDEX" / f"S01-approach-comparison-quality-redo-{DAY}.png"
    sheet.save(out, "PNG")
    print("board", out)

    # 2-panel current pair
    panel2 = 900
    cols2 = []
    for path, title, sub in [
        (BASE / "v05/art.png", "v05 LEFT p4", "hall crawl · quality-target match"),
        (BASE / "v06/art.png", "v06 RIGHT p5", "door · wreath · tree peek · rim light"),
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
        d.text((12, panel2 + 68), "Qwen 2 Pro /edit · ~$0.08 · style-lock-v2", fill=(90, 82, 74), font=font(14))
        cols2.append(canvas)
    w2 = 36 * 2 + panel2 * 2 + 28
    h2 = 36 * 2 + 72 + panel2 + 100
    sheet2 = Image.new("RGB", (w2, h2), (252, 248, 240))
    d = ImageDraw.Draw(sheet2)
    d.text((36, 18), f"S1 Approach SPLIT — current dials v05|v06 ({DAY})", fill=(28, 24, 20), font=font(24))
    sheet2.paste(cols2[0], (36, 36 + 72))
    sheet2.paste(cols2[1], (36 + panel2 + 28, 36 + 72))
    out2 = BASE / "_INDEX" / f"S01-approach-comparison-split-v05-v06-{DAY}.png"
    sheet2.save(out2, "PNG")
    print("board2", out2)

    flow_path = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
    flow = json.loads(flow_path.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    flow["mockup_quality_targets"] = {
        "S01_L": "Media/approved/style-refs/mockup-quality/S01-approach-L-quality-target.jpg",
        "S01_R": "Media/approved/style-refs/mockup-quality/S01-approach-R-quality-target.jpg",
        "source": "S01-approach/v01 Klein 9B 1536x768 dial · 2026-07-21 flow keep · best-of chops",
        "use": "Attach as composition/lighting quality refs on Qwen mock-up /edit gens alongside style-lock-v2",
    }
    for plate in flow["plates"]:
        if plate["id"] == "p04":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v05/art.png",
                    "caption": "p4 · S1 Approach L · v05 Qwen (quality-target redo)",
                    "version": "v05",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Redo toward Klein v01 best-of L look · holly PJs · style-lock-v2",
                    "tier": "dial_mock",
                    "previous": "v03",
                }
            )
        if plate["id"] == "p05":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v06/art.png",
                    "caption": "p5 · S1 Approach R · v06 Qwen (door quality-target)",
                    "version": "v06",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Door hero · fuller wreath · tree peek R · rim light · replaces v04",
                    "tier": "dial_mock",
                    "previous": "v04",
                }
            )
    for v in flow["verdicts"]:
        if v.get("beat") == "S1 Approach":
            v.update(
                {
                    "version": "v05|v06",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Quality-target redo from Klein v01 best-of · pending Jon eye vs targets",
                    "tier": "dial_mock",
                }
            )
    flow_path.write_text(json.dumps(flow, indent=2), encoding="utf-8")
    print("FLOW ok")


if __name__ == "__main__":
    main()
