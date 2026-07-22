#!/usr/bin/env python3
"""Save S01 v10 face-on redo, board with kept v09, update FLOW."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/generated/mocks/S01-approach"
DAY = "2026-07-22"
V10_URL = "https://v3b.fal.media/files/b/0aa35159/dDRLWo9gr8Dm1faYxjUaX_bC0X9K8U.png"
V10_REQ = "019f8b99-b312-7ea0-94e6-4478d2dc24ef"
V10_SEED = 1694605690


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main() -> None:
    urlretrieve(V10_URL, BASE / "v10/art.png")
    print("v10", Image.open(BASE / "v10/art.png").size)

    (BASE / "v10/RECIPE.md").write_text(
        f"""# RECIPE — S01-approach / v10

| Field | Value |
|-------|--------|
| **name** | S1 Approach R — face-on door destination |
| **unit** | S01-approach |
| **book page** | Flow v2 p5 · SPLIT RIGHT |
| **version** | v10 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 1536² · refs: door quality target (face-on) + continuity crawl ref + style-lock-v2 |
| **seed** | {V10_SEED} |
| **request_id** | `{V10_REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — face-on destination; v09 L kept |
| **tier** | dial_mock |

## Composition (Flow SPLIT)

RIGHT page = door destination. Camera square to the door, centered, full door face-on.
Wreath centered · red bow · bolt/latch · burgundy walls both sides · slightly ajar ·
warm light through crack + under door · tree peek R · presents · rim light both frame edges.

LEFT stays **v09** (child crawl POV). Same door / wreath / light — different camera = page-turn.
""",
        encoding="utf-8",
    )

    # Mark v09 kept in recipe if not already clear
    v09 = BASE / "v09/RECIPE.md"
    if v09.is_file():
        text = v09.read_text(encoding="utf-8")
        if "KEEP" not in text:
            text = text.replace(
                "| **status** | working — replaces v07 |",
                "| **status** | **KEEP** — Jon locked camera/composition 2026-07-22 |",
            )
            v09.write_text(text, encoding="utf-8")

    panel, label_h = 960, 110
    gap, margin, header = 28, 36, 90
    slots = [
        (BASE / "v09/art.png", "v09 LEFT p4 — KEEP", "child POV · low crawl · ajar door ahead"),
        (BASE / "v10/art.png", "v10 RIGHT p5 — NEW", "face-on centered door destination"),
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
        d.text((14, panel + 74), "SPLIT: approach → destination · Qwen /edit ~$0.08", fill=(90, 82, 74), font=font(13))
        cols.append(canvas)

    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    sheet = Image.new("RGB", (w, h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S1 Approach SPLIT — v09 KEEP | v10 face-on ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 48),
        "L = child approaching  ·  R = door itself (square / centered)  ·  same wreath · same light · page-turn",
        fill=(110, 100, 90),
        font=font(14),
    )
    sheet.paste(cols[0], (margin, margin + header))
    sheet.paste(cols[1], (margin + panel + gap, margin + header))
    out = BASE / "_INDEX" / f"S01-approach-comparison-split-v09-v10-{DAY}.png"
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
                    "caption": "p4 · S1 Approach L · v09 KEEP (crawl POV)",
                    "version": "v09",
                    "status": "keep",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "KEEP — low crawl angle, child approaching ajar decorated door",
                    "previous": "v07",
                }
            )
        if plate["id"] == "p05":
            plate.update(
                {
                    "path": "Media/generated/mocks/S01-approach/v10/art.png",
                    "caption": "p5 · S1 Approach R · v10 face-on door destination",
                    "version": "v10",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Face-on centered door · square to door · rim both edges · pending Jon eye",
                    "tier": "dial_mock",
                    "previous": "v10-angled-attempt",
                }
            )
    for v in flow["verdicts"]:
        if v.get("beat") == "S1 Approach":
            v.update(
                {
                    "version": "v09|v10",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "v09 KEEP · v10 face-on destination redo · pending Jon eye on R",
                }
            )
    flow_path.write_text(json.dumps(flow, indent=2), encoding="utf-8")
    print("FLOW ok")


if __name__ == "__main__":
    main()
