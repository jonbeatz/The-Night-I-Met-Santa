#!/usr/bin/env python3
"""
Build plate PNGs for text-layout-master:
- Spreads: copy art.png
- rightSingle (P01 title): 2625 art on RIGHT half — page 1 opens on right; LEFT = cream endpaper #FDFBF7
- leftSingle (P-thank-you): 2625 art on LEFT half of cream canvas
Also write poem lookup cheat sheet from book_poem_map.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
sys.path.insert(0, str(ROOT))
from scripts.book_poem_map import BEATS  # noqa: E402

OUT = ROOT / "Xtraz" / "Adobe-Photoshop" / "text-layout-master"
PLATES = OUT / "_plates"
PLATES.mkdir(parents=True, exist_ok=True)
MEDIA = ROOT / "Media" / "development"
SPREAD = (5250, 2625)
PAGE = 2625
CREAM = (253, 251, 247)  # #FDFBF7

UNITS = [
    ("P01", "P01-title", "P01-title", "rightSingle"),
    ("P02", "P02-about-spread", "P02-about-spread", "spread"),
    ("S01", "S01-approach", "S01-approach", "spread"),
    ("S02", "S02-threshold", "S02-threshold", "spread"),
    ("S03", "S03-eyes-met", "S03-eyes-met", "spread"),
    ("S04", "S04-sit-here", "S04-sit-here", "spread"),
    ("S05", "S05-chat", "S05-chat", "spread"),
    ("S06", "S06-cocoa", "S06-cocoa", "spread"),
    ("S07", "S07-proof", "S07-proof", "spread"),
    ("S08", "S08-gone", "S08-gone", "spread"),
    ("S09", "S09-search", "S09-search", "spread"),
    ("S10", "S10-note", "S10-note", "spread"),
    ("S11", "S11-wish", "S11-wish", "spread"),
    ("S12", "S12-god-bless", "S12-god-bless", "spread"),
    ("P-thank-you", "P-thank-you", "P-thank-you", "leftSingle"),
    ("P32-33", "P-quiet-close", "P-quiet-close", "spread"),
]


def plate_for(folder: str, mode: str, label: str) -> Path:
    src = MEDIA / folder / "art.png"
    if not src.is_file():
        raise SystemExit(f"missing {src}")
    dest = PLATES / f"{label}.png"
    if mode == "spread":
        shutil.copy2(src, dest)
    else:
        canvas = Image.new("RGB", SPREAD, CREAM)
        art = Image.open(src).convert("RGB")
        if art.size != (PAGE, PAGE):
            art = art.resize((PAGE, PAGE), Image.Resampling.LANCZOS)
        x = PAGE if mode == "rightSingle" else 0
        canvas.paste(art, (x, 0))
        canvas.save(dest, optimize=True)
    return dest


def write_poem_sheet() -> None:
    lines = [
        "# Poem / copy lookup — text-layout-master",
        "",
        "When Jon says a page or group name, Cursor reads `scripts/book_poem_map.py`.",
        "",
        "| Group | Unit folder | Pages | LEFT / single | RIGHT |",
        "|-------|-------------|-------|---------------|-------|",
    ]
    for label, folder, beat_key, _mode in UNITS:
        b = BEATS[beat_key]
        if b.get("layout") == "single":
            left = b.get("single", "")
            right = "—"
            pages = f"p{b['page']}"
        else:
            left = b.get("left", "")
            right = b.get("right", "")
            pages = f"p{b['left_page']}|{b['right_page']}"
        # escape pipes
        left = left.replace("|", "/")
        right = right.replace("|", "/")
        lines.append(f"| **{label}** | `{folder}` | {pages} | {left} | {right} |")

    lines += [
        "",
        "## Cursor rule",
        "",
        "When Jon says e.g. “I’m on S04” or “page 26”:",
        "1. Resolve via `scripts/book_poem_map.py` (`resolve_unit` / `BEATS`).",
        "2. Quote the exact LEFT / RIGHT (or single) strings for InDesign / MOCK-TYPE.",
        "3. Art: `Media/development/{folder}/art.png` (+ L/R if present).",
        "",
        f"Generated for PSD build. Master file: `Xtraz/Adobe-Photoshop/text-layout-master.psd`",
        "",
    ]
    (OUT / "POEM-LOOKUP.md").write_text("\n".join(lines), encoding="utf-8")
    # machine JSON for agents
    payload = []
    for label, folder, beat_key, mode in UNITS:
        b = dict(BEATS[beat_key])
        payload.append({"group": label, "folder": folder, "beat": beat_key, "mode": mode, **b})
    (OUT / "poem-lookup.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    for label, folder, _beat, mode in UNITS:
        p = plate_for(folder, mode, label)
        print("plate", label, Image.open(p).size)
    write_poem_sheet()
    print("wrote POEM-LOOKUP.md + poem-lookup.json")


if __name__ == "__main__":
    main()
