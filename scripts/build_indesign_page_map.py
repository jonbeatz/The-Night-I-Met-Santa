#!/usr/bin/env python3
"""Build indesign-page-map.json from master type-inventory (+ optional art paths).

Usage:
  python scripts/build_indesign_page_map.py
  python scripts/build_indesign_page_map.py --inventory PATH --out PATH
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.type_inventory_common import clean_text  # noqa: E402

DEFAULT_INV = (
    ROOT / "Xtraz/Adobe-Finals/FINAL-Master-Chopz/_type-inventory.json"
)
DEFAULT_OUT = (
    ROOT / "Xtraz/Adobe-Finals/FINAL-Master-Chopz/indesign-page-map.json"
)
DEFAULT_ART = (
    ROOT / "Xtraz/Adobe-Finals/FINAL-Master-Chopz/TNIMS-Interior-FINAL-Chopz"
)

# Book page map (TNIMS 34pp interior: p1 = first right after cover/blank rules vary)
# This mirrors the v7 builder: P01 right=1, P02=2|3, S01..=4.., thank-you 30|31
PAGE_PLAN = [
    ("P01", "right", 1),
    ("P02", "left", 2),
    ("P02", "right", 3),
]
_p = 4
for u in [f"S{i:02d}" for i in range(1, 13)]:
    PAGE_PLAN.append((u, "left", _p))
    PAGE_PLAN.append((u, "right", _p + 1))
    _p += 2
# pads 28|29 often blank in older maps — keep extensible
PAGE_PLAN += [
    ("P-author-thank-you", "left", 30),
    ("P-author-thank-you", "right", 31),
    ("Back-Page", "left", 32),
    ("Back-Page", "right", 33),
]


def pick_types(frames: list[dict], group: str, side: str) -> list[dict]:
    cands = [
        f
        for f in frames
        if f.get("group") == group
        and (f.get("page") or f.get("side")) == side
        and f.get("visible", True)
        and (f.get("text") or "").strip()
    ]

    def area(f):
        b = f.get("bbox_page_px") or [0, 0, 0, 0]
        if isinstance(b, dict):
            return max(0, (b["r"] - b["l"]) * (b["b"] - b["t"]))
        return max(0, (b[2] - b[0]) * (b[3] - b[1]))

    cands.sort(key=area, reverse=True)
    return cands


def art_for(unit: str, side: str, art_root: Path) -> str | None:
    candidates = [
        art_root / f"{unit}-{side}.png",
        art_root / f"{unit}-spread.png",
    ]
    # thank-you aliases
    if unit == "P-author-thank-you":
        candidates = [
            art_root / f"P-author-thank-you-{side}.png",
            art_root / "P-author-thank-you-spread.png",
        ] + candidates
    for c in candidates:
        if c.is_file():
            return str(c.resolve()).replace("\\", "/")
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inventory", type=Path, default=DEFAULT_INV)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--art-root", type=Path, default=DEFAULT_ART)
    args = ap.parse_args()

    if not args.inventory.is_file():
        print(f"ERROR: missing inventory {args.inventory}", file=sys.stderr)
        return 1

    data = json.loads(args.inventory.read_text(encoding="utf-8"))
    frames = data.get("frames") if isinstance(data, dict) else data
    frames = frames or []

    pages = []
    for group, side, pnum in PAGE_PLAN:
        types = pick_types(frames, group, side)
        type_payload = None
        if types:
            best = types[0]
            type_payload = {
                "text": clean_text(best.get("text") or ""),
                "bounds_in": best.get("bounds_in"),
                "bbox_page_px": best.get("bbox_page_px"),
                "font": best.get("font"),
                "size_pt": best.get("size_pt"),
                "leading_pt": best.get("leading_pt"),
                "tracking": best.get("tracking"),
                "color": best.get("color"),
                "align": best.get("align"),
                "paragraph_style": best.get("paragraph_style"),
                "frame_id": best.get("id"),
                "all_frame_ids": [t.get("id") for t in types],
            }
        pages.append(
            {
                "page": pnum,
                "unit": group,
                "side": side,
                "art": art_for(group, side, args.art_root),
                "type": type_payload,
            }
        )

    out = {
        "source_inventory": str(args.inventory).replace("\\", "/"),
        "pages": pages,
        "spec": {
            "trim_in": 8.5,
            "bleed_in": 0.125,
            "style_kit": [
                "Poem-Body",
                "Poem-Body-Tight",
                "Poem-Display",
                "Matter-Body",
                "Matter-Signoff",
                "Title-Main",
                "Poem-Emph",
                "Poem-Small",
            ],
            "effects": "none — live type; MOCK guide only",
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.out} ({len(pages)} pages)", flush=True)
    for pg in pages:
        t = pg.get("type")
        preview = (t["text"][:48].replace("\n", " / ") if t else "—")
        print(f"p{pg['page']:02d} {pg['unit']:22} {pg['side']:5} {preview}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
