#!/usr/bin/env python3
from pathlib import Path
import json
import shutil

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
src = ROOT / "Media/development/S12-god-bless/v15b"
dst = ROOT / "Media/development/S12-god-bless"
for n in ["art.png", "art-left.png", "art-right.png", "RECIPE.md", "meta.json"]:
    shutil.copy2(src / n, dst / n)
    print("copied", n)

FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
root = json.loads(FLOW.read_text(encoding="utf-8"))
note = (
    "S12-god-bless v15b LOOK LOCK preferred; "
    "v16–v16d attempts for 9th deer + moon raise still stuck at 8 deer"
)
for p in root["plates"]:
    if p["id"] in ("p26", "p27"):
        side = "left" if p["id"] == "p26" else "right"
        label = "L" if side == "left" else "R"
        p.update(
            {
                "version": "v15b",
                "status": "working",
                "date": "2026-07-23",
                "notes": note,
                "path": f"Media/development/S12-god-bless/art-{side}.png",
                "development_path": "Media/development/S12-god-bless/art.png",
                "caption": f"p{p['page']} · S12 God Bless {label} · v15b",
                "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                "unit": "S12-god-bless",
            }
        )
    if p["id"] in ("p28", "p29"):
        p.update({"version": "merged-v15b", "status": "merged", "date": "2026-07-23", "notes": "Absorbed — " + note})
for d in root["verdicts"]:
    if d.get("page") == "26|27":
        d.update({"version": "v15b", "status": "working", "date": "2026-07-23", "notes": note})
    if d.get("page") == "28|29":
        d.update({"version": "merged-v15b", "status": "merged", "date": "2026-07-23", "notes": "MERGED — " + note})
root["updated"] = "2026-07-23"
FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("FLOW -> v15b")
