#!/usr/bin/env python3
"""Validate type-inventory.json against handoff schema (no external deps)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_TOP = ("frames",)
REQUIRED_FRAME = ("id", "text")
RECOMMENDED_FRAME = (
    "font",
    "size_pt",
    "leading_pt",
    "align",
    "paragraph_style",
    "bbox_px",
    "bounds_in",
)


def validate(path: Path) -> list[str]:
    errs: list[str] = []
    warns: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"JSON parse error: {e}"]

    if isinstance(data, list):
        frames = data
        warns.append("legacy flat array — prefer schema tnims-type-inventory/v1 object")
    elif isinstance(data, dict):
        for k in REQUIRED_TOP:
            if k not in data:
                errs.append(f"missing top-level key: {k}")
        frames = data.get("frames") or []
        if data.get("schema") != "tnims-type-inventory/v1":
            warns.append("schema field missing or not tnims-type-inventory/v1")
    else:
        return ["root must be object or array"]

    if not frames:
        errs.append("frames[] is empty")

    for i, f in enumerate(frames):
        if not isinstance(f, dict):
            errs.append(f"frames[{i}] not an object")
            continue
        for k in REQUIRED_FRAME:
            if not f.get(k) and f.get(k) != 0:
                errs.append(f"frames[{i}] missing {k}")
        for k in RECOMMENDED_FRAME:
            if f.get(k) in (None, "", {}):
                warns.append(f"frames[{i}] ({f.get('id')}) missing recommended {k}")
        bbox = f.get("bbox_px") or {}
        if bbox and None in (bbox.get("l"), bbox.get("t"), bbox.get("r"), bbox.get("b")):
            errs.append(f"frames[{i}] bbox_px has nulls")
        bi = f.get("bounds_in")
        if bi:
            for k in ("top", "left", "bottom", "right"):
                if k not in bi:
                    errs.append(f"frames[{i}] bounds_in missing {k}")

    out = [f"ERROR: {e}" for e in errs] + [f"WARN: {w}" for w in warns]
    if not errs:
        out.insert(0, f"OK: {path.name} — {len(frames)} frames ({len(warns)} warnings)")
    else:
        out.insert(0, f"FAIL: {path.name} — {len(errs)} errors, {len(warns)} warnings")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", type=Path)
    args = ap.parse_args()
    code = 0
    for p in args.paths:
        if not p.is_file():
            print(f"FAIL: not found {p}")
            code = 1
            continue
        lines = validate(p)
        print("\n".join(lines))
        if lines[0].startswith("FAIL"):
            code = 1
    return code


if __name__ == "__main__":
    raise SystemExit(main())
