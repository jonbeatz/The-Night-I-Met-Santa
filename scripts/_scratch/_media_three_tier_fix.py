#!/usr/bin/env python3
"""Fix development/ naming + broken FLOW paths after three-tier reorg."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development"
ARCHIVE = ROOT / "Media/generated/mocks/archive"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"

# Flow id → development folder (beat-aligned)
FOLDER = {
    "cover": "Cover",
    "p01": "P01-title",
    "p02": "P02-about-spread",
    "p03": "P02-about-spread",
    "p04": "S01-approach",
    "p05": "S01-approach",
    "p06": "S02-threshold",
    "p07": "S02-threshold",
    "p08": "S03-eyes-met",
    "p09": "S03-eyes-met",
    "p10": "S04-sit-here",
    "p11": "S04-sit-here",
    "p12": "S05-chat",
    "p13": "S05-chat",
    "p14": "S06-cocoa",
    "p15": "S06-cocoa",
    "p16": "S07-proof",
    "p17": "S07-proof",
    "p18": "S08-gone",
    "p19": "S08-gone",
    "p20": "S09-search",
    "p21": "S09-search",
    "p22": "S10-note",
    "p23": "S10-note",
    "p24": "S11-wish",
    "p25": "S11-wish",
    "p26": "S12a-blessing",
    "p27": "S12a-blessing",
    "p28": "S12b-god-bless",
    "p29": "S12b-god-bless",
    "p30": "P-thank-you",
    "p31": "P-author",
    "p32": "P-quiet-close",
    "p33": "P-quiet-close",
}

# Resolve archived originals
ARCH_SPREADS = ARCHIVE / "approved-spreads-pre-v2"
ARCH_STYLE = ARCHIVE / "style-refs-pre-tier-reorg"


def resolve_legacy(path: str) -> Path | None:
    p = path.replace("\\", "/")
    candidates = [
        ROOT / p,
        ARCH_SPREADS / Path(p).name,
        ARCH_STYLE / "spread" / Path(p).name,
        ARCH_STYLE / "pages" / Path(p).name,
        ARCH_STYLE / "story" / Path(p).name,
        ARCH_STYLE / "covers" / Path(p).name,
    ]
    # also nested under approved-spreads
    if "spread-01-eyes-met" in p:
        candidates += [
            ARCH_SPREADS / "spread-01-eyes-met-LEFT.png",
            ARCH_SPREADS / "spread-01-eyes-met-RIGHT.png",
            ARCH_SPREADS / Path(p).name,
        ]
    if "spread-04-closing" in p:
        candidates += [
            ARCH_STYLE / "spread" / Path(p).name,
            ARCHIVE / "approved-spreads-pre-v2" / Path(p).name,
        ]
    for c in candidates:
        if c.is_file():
            return c
    # search by filename in archive
    name = Path(p).name
    for hit in ARCHIVE.rglob(name):
        if hit.is_file():
            return hit
    return None


def ensure(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def copy(src: Path, dest: Path) -> None:
    ensure(dest.parent)
    shutil.copy2(src, dest)
    print("copy", dest.relative_to(ROOT))


def main() -> None:
    data = json.loads(FLOW.read_text(encoding="utf-8"))

    # Remove misnamed P10–P33 folders (will rebuild under beat names)
    for child in list(DEV.iterdir()):
        if child.is_dir() and child.name.startswith("P") and child.name[1:].isdigit():
            print("remove misnamed", child.name)
            shutil.rmtree(child)

    # Also remove wrong stubs that duplicate
    for name in ("P-matter-thank-you", "P-quiet-close"):
        pass

    for plate in data["plates"]:
        pid = plate["id"]
        status = plate.get("status", "")
        if status not in ("keep", "locked", "locked-provisional", "keep-leaning"):
            continue

        folder = FOLDER.get(pid)
        if not folder:
            continue
        dest_dir = ensure(DEV / folder)

        # Character lock for author page — don't duplicate into development as "page art"
        if pid == "p31":
            plate["tier"] = "approved"
            plate["path"] = "Media/approved/characters/jack-farrell-portrait.png"
            plate["development_path"] = None
            (dest_dir / "README.md").write_text(
                "Author portrait lives in `Media/approved/characters/jack-farrell-portrait.png` (forever lock).\n"
                "No provisional page art here until an illustrated author page is dialed.\n",
                encoding="utf-8",
            )
            continue

        # p11 wrongly pointed at style-lock — find real S4 R art from mocks if possible
        src_path = plate.get("source_mock") or plate.get("path")
        if "style-lock-v2" in (src_path or ""):
            # try S04 mocks
            for cand in [
                ROOT / "Media/generated/mocks/S04-sit-here/v07/art.png",
                ROOT / "Media/generated/mocks/S04-sit-here/v11/art.png",
            ]:
                if cand.is_file():
                    src_path = str(cand.relative_to(ROOT)).replace("\\", "/")
                    break

        src = resolve_legacy(src_path) if src_path else None
        if src is None and plate.get("path"):
            src = resolve_legacy(plate["path"])
        # Prefer existing development art if already correct
        if pid in ("cover", "p01", "p02", "p03", "p04", "p05", "p06", "p07"):
            # already good
            pass

        # Destination filename
        if pid in ("p04", "p08", "p10", "p12", "p14", "p16", "p18", "p20", "p22", "p24", "p26", "p28", "p32"):
            dest_name = "art-left.png"
        elif pid in ("p05", "p09", "p11", "p13", "p15", "p17", "p19", "p21", "p23", "p25", "p27", "p29", "p33"):
            dest_name = "art-right.png"
        else:
            dest_name = "art.png"

        # Shared masters: p03/p07 use same as partner
        if pid in ("p03", "p07"):
            dest_name = "art.png"

        dest = dest_dir / dest_name

        if src and src.is_file():
            # Don't overwrite Cover/P01/S01/S02/P02 if already present and source was missing earlier
            if dest.exists() and pid in ("cover", "p01", "p02", "p04", "p05", "p06"):
                print("keep existing", dest.relative_to(ROOT))
            else:
                copy(src, dest)
        elif dest.exists():
            print("no src but dest ok", dest.relative_to(ROOT))
        else:
            print("STILL MISSING", pid, plate.get("path"))
            (dest_dir / "MISSING.md").write_text(
                f"Need regen for v2 flow. Legacy path: `{plate.get('path')}`\n",
                encoding="utf-8",
            )

        # Update FLOW
        rel_dest = str(dest.relative_to(ROOT)).replace("\\", "/")
        plate["tier"] = "development"
        if "source_mock" not in plate or "approved/" in plate.get("source_mock", ""):
            if src:
                try:
                    plate["source_mock"] = str(src.relative_to(ROOT)).replace("\\", "/")
                except ValueError:
                    plate["source_mock"] = plate.get("path")
        plate["path"] = rel_dest
        plate["development_path"] = rel_dest

        meta = {
            "flow_id": pid,
            "status": status,
            "tier": "development",
            "path": rel_dest,
            "source_mock": plate.get("source_mock"),
            "version": plate.get("version"),
            "beat": plate.get("beat"),
        }
        (dest_dir / f"meta-{pid}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # Cover + P01 meta
    for pid, folder in (("cover", "Cover"), ("p01", "P01-title")):
        plate = next(p for p in data["plates"] if p["id"] == pid)
        (DEV / folder / f"meta-{pid}.json").write_text(
            json.dumps(
                {
                    "flow_id": pid,
                    "status": plate.get("status"),
                    "tier": "development",
                    "path": plate.get("path"),
                    "notes": plate.get("notes"),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    # Empty stubs for beats with no art yet
    for name in (
        "S03-eyes-met",
        "S04-sit-here",
        "S05-chat",
        "S06-cocoa",
        "S07-proof",
        "S08-gone",
        "S09-search",
        "S10-note",
        "S11-wish",
        "S12a-blessing",
        "S12b-god-bless",
        "P-thank-you",
        "P-author",
        "P-quiet-close",
    ):
        ensure(DEV / name)

    data["plates"] = data["plates"]
    FLOW.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("\n=== development tree ===")
    for p in sorted(DEV.iterdir()):
        if p.is_dir():
            files = [f.name for f in p.iterdir() if f.is_file()]
            print(f"  {p.name}/  {files}")


if __name__ == "__main__":
    main()
