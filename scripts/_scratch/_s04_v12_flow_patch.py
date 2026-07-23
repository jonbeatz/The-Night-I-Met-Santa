#!/usr/bin/env python3
"""Point FLOW p10|p11 at S04-sit-here v12 TEXT+IMAGE dial."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
DAY = "2026-07-22"


def main() -> None:
    flow = json.loads(FLOW.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    for plate in flow["plates"]:
        if plate["id"] == "p10":
            plate.update(
                {
                    "path": "Media/development/S04-sit-here/art-left.png",
                    "caption": "p10 · S4 Sit Here L · v12 text page (mistletoe)",
                    "version": "v12",
                    "model": "Qwen 2 Pro /edit",
                    "status": "working",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Flow v2 TEXT page · mistletoe hint · soft bleed · pending Jon eye",
                    "tier": "development",
                    "development_path": "Media/development/S04-sit-here/art-left.png",
                    "source_mock": "Media/generated/mocks/S04-sit-here/v12/art-left.png",
                    "wardrobe_fix": "n/a",
                }
            )
        if plate["id"] == "p11":
            plate.update(
                {
                    "path": "Media/development/S04-sit-here/art-right.png",
                    "caption": "p11 · S4 Sit Here R · v12 Santa beckons (open coat)",
                    "version": "v12",
                    "model": "Qwen 2 Pro /edit",
                    "status": "working",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Flow v2 IMAGE · low-angle gift sea · open-coat Santa · Boy G0 · fewer gifts · pending Jon eye",
                    "tier": "development",
                    "development_path": "Media/development/S04-sit-here/art-right.png",
                    "source_mock": "Media/generated/mocks/S04-sit-here/v12/art-right.png",
                    "wardrobe_fix": "in_progress",
                }
            )
    for v in flow["verdicts"]:
        if v.get("beat") == "S4 Sit Here":
            v.update(
                {
                    "version": "v12",
                    "model": "Qwen 2 Pro /edit",
                    "status": "working",
                    "date": DAY,
                    "notes": "Flow v2 TEXT+IMAGE dial · quality bar S03-v07 · open-coat Santa · fewer gifts",
                    "wardrobe_fix": "in_progress",
                }
            )
    for q in flow.get("wardrobe_fix_queue", []):
        if q.get("beat") == "S4 Sit Here":
            q["status"] = "in_progress"
            q["version"] = "v12"
    FLOW.write_text(json.dumps(flow, indent=2) + "\n", encoding="utf-8")
    print("FLOW S4 -> v12 working")


if __name__ == "__main__":
    main()
