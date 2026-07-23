#!/usr/bin/env python3
"""Point FLOW p08|p09 at S03-eyes-met v01 dial (needs Jon eye)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S03-eyes-met"
FLOW_PATH = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
DAY = "2026-07-22"

def main() -> None:
    src = DEV / "v01" / "art.png"
    shutil.copy2(src, DEV / "art.png")
    flow = json.loads(FLOW_PATH.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    for plate in flow["plates"]:
        if plate["id"] == "p08":
            plate.update(
                {
                    "path": "Media/development/S03-eyes-met/art.png",
                    "caption": "p8 · S3 Eyes Met L · v01 dial (Flow v2 regen)",
                    "version": "v01",
                    "model": "Qwen 2 Pro /edit",
                    "status": "working",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Flow v2 regen · boy awe L · quality bar S02-v05 · pending Jon eye · GPT pillar later",
                    "gpt_pillar": True,
                    "tier": "development",
                    "spread_side": "L",
                    "previous": "FINAL-TEST-A archive",
                    "development_path": "Media/development/S03-eyes-met/art.png",
                    "source_mock": "Media/generated/mocks/S03-eyes-met/v01/art.png",
                }
            )
        if plate["id"] == "p09":
            plate.update(
                {
                    "path": "Media/development/S03-eyes-met/art.png",
                    "caption": "p9 · S3 Eyes Met R · v01 dial (Flow v2 regen)",
                    "version": "v01",
                    "model": "Qwen 2 Pro /edit",
                    "status": "working",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Flow v2 regen · Santa looks back R · suspenders · quality bar S02-v05 · pending Jon eye",
                    "gpt_pillar": True,
                    "tier": "development",
                    "spread_side": "R",
                    "previous": "FINAL-TEST-A archive",
                    "development_path": "Media/development/S03-eyes-met/art.png",
                    "source_mock": "Media/generated/mocks/S03-eyes-met/v01/art.png",
                }
            )
    for v in flow["verdicts"]:
        if v.get("beat") == "S3 Eyes Met":
            v.update(
                {
                    "version": "v01",
                    "model": "Qwen 2 Pro /edit",
                    "status": "working",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Flow v2 first dial · quality bar S02-v05 · GPT pillar reserved for final after KEEP",
                    "tier": "dial_mock",
                }
            )
            break
    FLOW_PATH.write_text(json.dumps(flow, indent=2) + "\n", encoding="utf-8")
    print("FLOW S3 → v01 working")

if __name__ == "__main__":
    main()
