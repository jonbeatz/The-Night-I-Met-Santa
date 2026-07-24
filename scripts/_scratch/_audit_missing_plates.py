"""Audit FLOW plates + playbook optional gaps."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
flow = json.loads((ROOT / "Media/generated/mocks/_FLOW-CURRENT.json").read_text(encoding="utf-8"))

print("=== FLOW plates ===")
missing = []
present = []
for p in flow["plates"]:
    path = ROOT / p["path"]
    ok = path.is_file()
    status = p.get("status", "?")
    ver = p.get("version", "")
    flag = "OK" if ok else "MISSING"
    print(f"{p['id']:14} p{str(p.get('page','?')):6} {status:10} {ver:30} {flag}  {p['path']}")
    (present if ok else missing).append(p)

print(f"\npresent={len(present)} missing={len(missing)}")

# Extra playbook assets not always in FLOW
extras = {
    "back-cover": [
        ROOT / "Media/development/Cover/art-back.png",
        ROOT / "Media/approved/covers/cover-back.png",
        ROOT / "Media/generated/mocks/Cover-back/v01/art.png",
    ],
    "casewrap-burgundy": [
        ROOT / "Media/development/Cover/pastedown-burgundy.png",
        ROOT / "Media/generated/mocks/Cover-pastedown/v01/art.png",
    ],
    "p34-padding": [ROOT / "Media/development/P34-padding/art.png"],
    "p35-colophon": [ROOT / "Media/development/P35-colophon/art.png"],
    "p36-blank": [ROOT / "Media/development/P36-blank/art.png"],
    "copyright-solo": [
        ROOT / "Media/development/P02-copyright/art.png",
        # P01 now includes copyright on same page per Flow v2
    ],
}
print("\n=== Playbook extras (may be optional) ===")
for name, paths in extras.items():
    hits = [str(p.relative_to(ROOT)) for p in paths if p.is_file()]
    print(f"{name}: {' | '.join(hits) if hits else 'NONE'}")

print("\n=== development folders ===")
dev = ROOT / "Media/development"
for d in sorted(dev.iterdir()):
    if d.is_dir():
        arts = sorted(d.glob("art*.png"))
        print(f"  {d.name}: {[a.name for a in arts[:8]]}")
