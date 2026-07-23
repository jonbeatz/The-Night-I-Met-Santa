#!/usr/bin/env python3
"""Lock S2 Threshold v05 as KEEP + quality bar; promote art.png; patch FLOW."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S02-threshold"
MOCKS = ROOT / "Media/generated/mocks/S02-threshold"
FLOW_PATH = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
DAY = "2026-07-22"


def main() -> None:
    src = DEV / "v05" / "art.png"
    if not src.is_file():
        raise SystemExit(f"missing {src}")
    shutil.copy2(src, DEV / "art.png")
    print("promoted", DEV / "art.png")

    # meta pointers
    for name, page in (("meta-p06.json", "6"), ("meta-p07.json", "7")):
        meta = {
            "page": page,
            "unit": "S02-threshold",
            "version": "v05",
            "status": "keep",
            "quality_reference": True,
            "path": "Media/development/S02-threshold/art.png",
            "source": "Media/development/S02-threshold/v05/art.png",
            "date": DAY,
        }
        (DEV / name).write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    flow = json.loads(FLOW_PATH.read_text(encoding="utf-8"))
    flow["updated"] = DAY
    flow["quality_reference"] = {
        "unit": "S02-threshold",
        "version": "v05",
        "path": "Media/development/S02-threshold/art.png",
        "source": "Media/development/S02-threshold/v05/art.png",
        "locked": DAY,
        "decided_by": "Jon",
        "notes": (
            "QUALITY BAR for all spreads going forward: rich oil-painting saturation "
            "(deep burgundy, warm golds, luminous highlights); dramatic lighting contrast "
            "(bright hallway behind boy vs warm intimate room); deep atmospheric corner shadows; "
            "doorway + golden light spill language wherever a doorway appears."
        ),
    }

    for plate in flow["plates"]:
        if plate["id"] == "p06":
            plate.update(
                {
                    "path": "Media/development/S02-threshold/art.png",
                    "caption": "p6 · S2 Threshold L · v05 KEEP (quality bar)",
                    "version": "v05",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Seamless L · boy at doorway · golden hallway spill · holly PJs · QUALITY BAR",
                    "tier": "development",
                    "spread_side": "L",
                    "previous": "v04",
                    "development_path": "Media/development/S02-threshold/art.png",
                    "source_mock": "Media/generated/mocks/S02-threshold/v05/art.png",
                    "quality_reference": True,
                }
            )
        if plate["id"] == "p07":
            plate.update(
                {
                    "path": "Media/development/S02-threshold/art.png",
                    "caption": "p7 · S2 Threshold R · v05 KEEP (quality bar)",
                    "version": "v05",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "Seamless R · Santa coat+suspenders · placing under ONE tree · QUALITY BAR",
                    "tier": "development",
                    "spread_side": "R",
                    "previous": "v04",
                    "development_path": "Media/development/S02-threshold/art.png",
                    "source_mock": "Media/generated/mocks/S02-threshold/v05/art.png",
                    "quality_reference": True,
                }
            )

    for v in flow["verdicts"]:
        if v.get("beat") == "S2 Threshold":
            v.update(
                {
                    "version": "v05",
                    "model": "Qwen 2 Pro /edit",
                    "status": "keep",
                    "decided_by": "Jon",
                    "date": DAY,
                    "notes": "KEEP · QUALITY BAR for all spreads · oil richness + doorway golden spill · Jon 2026-07-22",
                    "tier": "development",
                }
            )
            break

    FLOW_PATH.write_text(json.dumps(flow, indent=2) + "\n", encoding="utf-8")
    print("FLOW updated")

    lock_blurb = (
        "\n\n## Lock\n\n"
        "**KEEP 2026-07-22** — pages 6|7 done. Visual **QUALITY BAR** for all subsequent spreads: "
        "rich oil-painting saturation, dramatic hallway-vs-room lighting, deep corner shadows, "
        "doorway golden-spill language.\n"
    )
    for p in (DEV / "v05" / "RECIPE.md", MOCKS / "v05" / "RECIPE.md"):
        t = p.read_text(encoding="utf-8")
        t = t.replace(
            "working — atmosphere pass on kept v04 composition",
            "KEEP — QUALITY BAR for all spreads (Jon 2026-07-22)",
        )
        if "## Lock" not in t:
            t = t.rstrip() + lock_blurb
        p.write_text(t, encoding="utf-8")
    print("RECIPE stamped KEEP")


if __name__ == "__main__":
    main()
