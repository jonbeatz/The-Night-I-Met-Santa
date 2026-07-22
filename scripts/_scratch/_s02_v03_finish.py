#!/usr/bin/env python3
"""Save S02-threshold v03 spread, update FLOW, rebuild board preview."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/generated/mocks/S02-threshold"
DAY = "2026-07-22"
URL = "https://v3b.fal.media/files/b/0aa35216/_UVRyRaW-AFrlvZnTs_ck_UYiWwj12.png"
REQ = "019f8bb6-9063-7780-a40e-99b255304fca"
SEED = 79887063


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main() -> None:
    vdir = BASE / "v03"
    vdir.mkdir(parents=True, exist_ok=True)
    (BASE / "_INDEX").mkdir(parents=True, exist_ok=True)
    urlretrieve(URL, vdir / "art.png")
    im = Image.open(vdir / "art.png")
    print("v03", im.size)

    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S02-threshold / v03

| Field | Value |
|-------|--------|
| **name** | S2 Threshold — seamless enter / Santa at bag |
| **unit** | S02-threshold |
| **book page** | Flow v2 p6\\|7 · FULL SPREAD |
| **page role** | spread |
| **version** | v03 |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · refs: style-lock-v2 + boy-G0 + santa-G0-v2 |
| **seed** | {SEED} |
| **request_id** | `{REQ}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — first v2-flow Qwen spread dial |
| **tier** | dial_mock |

## Brief (Flow v2)

LEFT: boy entering slowly from doorway (over-shoulder).  
RIGHT: Santa going through bag, placing presents under tree (floor, suspenders over coat).  
Seamless continuous scene. Hard wardrobe append applied.

## Poem ref

L: I didn't know it when I entered the room / to surprise the amazement or even the shock.  
R: Now I'm usually calm… / But what do you say when you sneak up on Santa?
""",
        encoding="utf-8",
    )

    # Preview board: full spread + L/R chops
    w, h = im.size
    mid = w // 2
    left = im.crop((0, 0, mid, h)).convert("RGB")
    right = im.crop((mid, 0, w, h)).convert("RGB")
    left.save(BASE / "_INDEX" / "v03-LEFT-half.png")
    right.save(BASE / "_INDEX" / "v03-RIGHT-half.png")

    panel_h = 520
    sc = panel_h / h
    full_w = int(w * sc)
    full = im.convert("RGB").resize((full_w, panel_h), Image.Resampling.LANCZOS)
    half_w = int(mid * sc)
    left_r = left.resize((half_w, panel_h), Image.Resampling.LANCZOS)
    right_r = right.resize((half_w, panel_h), Image.Resampling.LANCZOS)

    margin, gap, header, label = 28, 16, 72, 56
    sheet_w = margin * 2 + max(full_w, half_w * 2 + gap)
    sheet_h = margin * 2 + header + panel_h + label + gap + panel_h + label
    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S2 Threshold SPREAD — v03 ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 44),
        "Full seamless · L enter doorway · R Santa at bag/tree · Qwen 2 Pro /edit · style-lock-v2 + G0s",
        fill=(110, 100, 90),
        font=font(13),
    )
    y = margin + header
    sheet.paste(full, (margin, y))
    d.text((margin, y + panel_h + 8), "FULL SPREAD (p6|7 continuous)", fill=(32, 28, 24), font=font(16))
    y2 = y + panel_h + label + gap
    sheet.paste(left_r, (margin, y2))
    sheet.paste(right_r, (margin + half_w + gap, y2))
    d.text((margin, y2 + panel_h + 8), "LEFT half (p6)", fill=(32, 28, 24), font=font(15))
    d.text((margin + half_w + gap, y2 + panel_h + 8), "RIGHT half (p7)", fill=(32, 28, 24), font=font(15))
    out = BASE / "_INDEX" / f"S02-threshold-comparison-spread-v03-{DAY}.png"
    sheet.save(out, "PNG")
    print("board", out)

    flow_path = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
    flow = json.loads(flow_path.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    for plate in flow["plates"]:
        if plate["id"] == "p06":
            plate.update(
                {
                    "path": "Media/generated/mocks/S02-threshold/v03/art.png",
                    "caption": "p6 · S2 Threshold L · v03 spread (enter)",
                    "version": "v03",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Seamless spread L half · boy entering · holly PJs · flipbook auto-splits wide",
                    "tier": "dial_mock",
                    "spread_side": "L",
                    "previous": "v02",
                }
            )
        if plate["id"] == "p07":
            plate.update(
                {
                    "path": "Media/generated/mocks/S02-threshold/v03/art.png",
                    "caption": "p7 · S2 Threshold R · v03 spread (Santa at bag)",
                    "version": "v03",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Seamless spread R half · Santa bag/tree · suspenders over coat · open collar",
                    "tier": "dial_mock",
                    "spread_side": "R",
                    "previous": "v02",
                }
            )
    for v in flow["verdicts"]:
        if v.get("beat") == "S2 Threshold":
            v.update(
                {
                    "version": "v03",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep-leaning",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "First v2-flow Qwen seamless spread · pending Jon eye",
                    "tier": "dial_mock",
                }
            )
            break
    else:
        flow.setdefault("verdicts", []).append(
            {
                "beat": "S2 Threshold",
                "version": "v03",
                "model": "Qwen 2 Pro /edit",
                "status": "keep-leaning",
                "decided_by": "Jon",
                "date": DAY,
                "notes": "First v2-flow Qwen seamless spread · pending Jon eye",
                "tier": "dial_mock",
            }
        )
    flow_path.write_text(json.dumps(flow, indent=2), encoding="utf-8")
    print("FLOW ok")


if __name__ == "__main__":
    main()
