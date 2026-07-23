#!/usr/bin/env python3
"""Lock S3 Eyes Met v07 KEEP as quality bar; refresh wardrobe queue."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S03-eyes-met"
MOCKS = ROOT / "Media/generated/mocks/S03-eyes-met"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
DAY = "2026-07-22"


def main() -> None:
    src = DEV / "v07" / "art.png"
    shutil.copy2(src, DEV / "art.png")

    for p in (DEV / "v07" / "RECIPE.md", MOCKS / "v07" / "RECIPE.md"):
        if not p.is_file():
            continue
        t = p.read_text(encoding="utf-8")
        t = t.replace(
            "working — open coat + striped shirt + brown suspenders visible",
            "KEEP — QUALITY BAR (Jon 2026-07-22) · prefer slightly fewer gifts on future plates",
        )
        if "## Lock" not in t:
            t = t.rstrip() + (
                "\n\n## Lock\n\n"
                "**KEEP 2026-07-22** — pages 8|9 done. **QUALITY BAR** for all subsequent plates.\n\n"
                "Match: oil-painting warmth/depth · burgundy walls · golden fire + tree glow · "
                "wide room (fireplace, tree, gift sea) · Santa G0 open coat / striped shirt / "
                "brown suspenders over shirt · Boy G0 oatmeal holly PJs (red trim/buttons) · "
                "eye contact when story calls for it.\n\n"
                "**Note:** Keep gift sea, but prefer **a few less gifts** than this plate "
                "(less clutter for quiet zones / text clouds).\n"
            )
        p.write_text(t, encoding="utf-8")

    flow = json.loads(FLOW.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    flow["quality_reference"] = {
        "unit": "S03-eyes-met",
        "version": "v07",
        "path": "Media/development/S03-eyes-met/art.png",
        "source": "Media/development/S03-eyes-met/v07/art.png",
        "locked": DAY,
        "decided_by": "Jon",
        "supersedes": "S02-threshold/v05 (still quality for doorway spill language)",
        "notes": (
            "QUALITY BAR: rich oil-painting warmth/depth; burgundy walls; warm golden "
            "firelight + tree glow; wide room with fireplace, tree, gift sea; "
            "Santa G0 v2 open coat + cream striped shirt + brown suspenders over shirt; "
            "Boy G0 oatmeal/taupe holly PJs with visible holly, red trim, red buttons; "
            "eye contact when story calls for it. NOTE: prefer a few LESS gifts than this "
            "plate on future gens (keep gift sea, reduce clutter)."
        ),
        "doorway_spill_language": "Also retain S2 Threshold v05 doorway + golden hallway spill when doorways appear.",
    }

    for plate in flow["plates"]:
        if plate["id"] in ("p08", "p09"):
            side = "L" if plate["id"] == "p08" else "R"
            plate.update(
                {
                    "path": "Media/development/S03-eyes-met/art.png",
                    "caption": f"p{plate['page']} · S3 Eyes Met {side} · v07 KEEP (quality bar)",
                    "version": "v07",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": (
                        "KEEP · QUALITY BAR · open-coat Santa · Boy G0 · eyes meet · "
                        "prefer fewer gifts on later plates"
                    ),
                    "tier": "development",
                    "spread_side": side,
                    "development_path": "Media/development/S03-eyes-met/art.png",
                    "source_mock": "Media/generated/mocks/S03-eyes-met/v07/art.png",
                    "quality_reference": True,
                    "wardrobe_fix": "done",
                }
            )
        if plate["id"] in ("p06", "p07"):
            plate["wardrobe_fix"] = "queued"
            plate["quality_reference"] = False  # S3 is now primary bar; S2 still doorway language
        if plate["id"] in ("p10", "p11"):
            plate["wardrobe_fix"] = "queued"
            plate["notes"] = (
                (plate.get("notes") or "")
                + " · QUEUED: Flow v2 TEXT+IMAGE regen + Santa G0 open-coat lock"
            ).strip(" ·")

    for v in flow["verdicts"]:
        if v.get("beat") == "S3 Eyes Met":
            v.update(
                {
                    "version": "v07",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": (
                        "KEEP · QUALITY BAR for all plates · open-coat Santa · Boy G0 · "
                        "prefer fewer gifts going forward · Jon 2026-07-22"
                    ),
                    "tier": "development",
                    "wardrobe_fix": "done",
                }
            )
        if v.get("beat") == "S2 Threshold":
            v["wardrobe_fix"] = "queued"
            notes = v.get("notes") or ""
            if "wardrobe fix queued" not in notes.lower():
                v["notes"] = f"{notes} · wardrobe fix queued (open-coat Santa G0)".strip(" ·")
        if v.get("beat") == "S4 Sit Here":
            v.update(
                {
                    "wardrobe_fix": "queued",
                    "notes": (
                        "QUEUED: Flow v2 TEXT+IMAGE regen (L mistletoe text page · R Santa beckons) "
                        "+ Santa G0 open-coat lock · quality bar S03-v07"
                    ),
                }
            )

    flow["wardrobe_fix_queue"] = [
        {
            "beat": "S2 Threshold",
            "plate": "S02-threshold",
            "version": "v05",
            "pages": "6|7",
            "status": "queued",
            "priority": 1,
            "reason": "Santa needs G0 v2 open-coat update (keep composition)",
            "date": DAY,
        },
        {
            "beat": "S4 Sit Here",
            "plate": "S04-sit-here",
            "version": "pre-v2 keep → regen",
            "pages": "10|11",
            "status": "in_progress",
            "priority": 0,
            "reason": "Flow v2 TEXT+IMAGE regen + Santa G0 open-coat · quality bar S03-v07",
            "date": DAY,
        },
    ]
    flow["wardrobe_fix_skip"] = [
        {"beat": "S1 Approach", "reason": "no Santa"},
        {"beat": "P02 About", "reason": "no characters"},
        {"beat": "S3 Eyes Met", "reason": "v07 KEEP — wardrobe done"},
    ]

    FLOW.write_text(json.dumps(flow, indent=2) + "\n", encoding="utf-8")
    print("S3 v07 KEEP locked · quality bar set · wardrobe queue refreshed")


if __name__ == "__main__":
    main()
