#!/usr/bin/env python3
"""Queue Santa wardrobe fixes on S2 + S4 in FLOW; note S3 v07 working."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
DAY = "2026-07-22"

QUEUE_NOTE = (
    "QUEUED 2026-07-22: Santa wardrobe fix — open red coat over cream striped shirt + "
    "brown leather suspenders OVER SHIRT (not over coat). Match santa-G0 / santa-G0-v2. "
    "Keep composition; outfit only."
)


def main() -> None:
    flow = json.loads(FLOW.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    flow.setdefault("wardrobe_fix_queue", [])
    # replace prior queue entries for these beats
    flow["wardrobe_fix_queue"] = [
        q
        for q in flow["wardrobe_fix_queue"]
        if q.get("beat") not in ("S2 Threshold", "S4 Sit Here", "S3 Eyes Met")
    ]
    flow["wardrobe_fix_queue"].extend(
        [
            {
                "beat": "S2 Threshold",
                "plate": "S02-threshold",
                "version": "v05",
                "status": "queued",
                "priority": 1,
                "reason": "Santa closed coat + suspenders over coat — needs open-coat lock",
                "date": DAY,
            },
            {
                "beat": "S4 Sit Here",
                "plate": "S04-sit-here",
                "version": "v11 / santa-G0-v2",
                "status": "queued",
                "priority": 2,
                "reason": "Built under prior suspenders-over-coat language — needs open-coat lock",
                "date": DAY,
            },
            {
                "beat": "S3 Eyes Met",
                "plate": "S03-eyes-met",
                "version": "v07",
                "status": "in_progress",
                "priority": 0,
                "reason": "Hero wardrobe pass — open coat over v06 shirt/suspenders",
                "date": DAY,
            },
        ]
    )

    for plate in flow["plates"]:
        if plate["id"] in ("p06", "p07"):
            notes = plate.get("notes") or ""
            if "QUEUED" not in notes:
                plate["notes"] = f"{notes} · {QUEUE_NOTE}".strip(" ·")
            plate["wardrobe_fix"] = "queued"
        if plate["id"] in ("p10", "p11") or (
            plate.get("beat", "").startswith("S4")
        ):
            # S4 sit here plates
            if "Sit Here" in plate.get("beat", "") or plate["id"] in ("p10", "p11"):
                notes = plate.get("notes") or ""
                if "QUEUED" not in notes and "wardrobe" not in notes.lower():
                    plate["notes"] = f"{notes} · {QUEUE_NOTE}".strip(" ·")
                plate["wardrobe_fix"] = "queued"
        if plate["id"] in ("p08", "p09"):
            plate.update(
                {
                    "path": "Media/development/S03-eyes-met/v07/art.png",
                    "version": "v07",
                    "model": "Qwen 2 Pro /edit",
                    "status": "working",
                    "date": DAY,
                    "caption": plate["caption"].replace("v01", "v07").replace("v04", "v07").replace("v06", "v07")
                    if "v0" in plate.get("caption", "")
                    else f"p{plate['page']} · S3 Eyes Met · v07 open-coat pass",
                    "notes": "v07 · open red coat over striped shirt + brown suspenders · pending Jon eye",
                    "development_path": "Media/development/S03-eyes-met/v07/art.png",
                    "source_mock": "Media/generated/mocks/S03-eyes-met/v07/art.png",
                    "wardrobe_fix": "in_progress",
                }
            )

    for v in flow["verdicts"]:
        if v.get("beat") == "S2 Threshold":
            v["wardrobe_fix"] = "queued"
            notes = v.get("notes") or ""
            if "QUEUED" not in notes:
                v["notes"] = f"{notes} · {QUEUE_NOTE}".strip(" ·")
        if v.get("beat") == "S4 Sit Here":
            v["wardrobe_fix"] = "queued"
            notes = v.get("notes") or ""
            if "QUEUED" not in notes:
                v["notes"] = f"{notes} · {QUEUE_NOTE}".strip(" ·")
        if v.get("beat") == "S3 Eyes Met":
            v.update(
                {
                    "version": "v07",
                    "model": "Qwen 2 Pro /edit",
                    "status": "working",
                    "date": DAY,
                    "notes": "v07 open-coat over shirt/suspenders · pending Jon eye · GPT pillar later",
                    "wardrobe_fix": "in_progress",
                }
            )

    # skip list
    flow["wardrobe_fix_skip"] = [
        {"beat": "S1 Approach", "reason": "no Santa"},
        {"beat": "P02 About", "reason": "no characters"},
    ]

    FLOW.write_text(json.dumps(flow, indent=2) + "\n", encoding="utf-8")
    print("FLOW wardrobe queue updated")


if __name__ == "__main__":
    main()
