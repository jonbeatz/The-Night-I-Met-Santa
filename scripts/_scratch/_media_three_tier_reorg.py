#!/usr/bin/env python3
"""Reorganize Media/ into three-tier: approved (locks) | development (current best) | finals (Lulu)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
APPROVED = ROOT / "Media/approved"
DEV = ROOT / "Media/development"
FINALS = ROOT / "Media/finals"
ARCHIVE = ROOT / "Media/generated/mocks/archive"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"

# Keep forever under approved/
KEEP_APPROVED_FILES = {
    "style-refs/style-lock-v2.png",
    "style-refs/style-lock-v2.recipe.md",
}


def ensure(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def move_tree(src: Path, dest: Path) -> None:
    if not src.exists():
        print("skip missing", src)
        return
    ensure(dest.parent)
    if dest.exists():
        # merge: move children
        for child in src.iterdir():
            target = dest / child.name
            if target.exists():
                if target.is_dir() and child.is_dir():
                    move_tree(child, target)
                else:
                    print("exists, skip", target)
            else:
                shutil.move(str(child), str(target))
        try:
            src.rmdir()
        except OSError:
            pass
    else:
        shutil.move(str(src), str(dest))
    print("moved", src.relative_to(ROOT), "->", dest.relative_to(ROOT))


def copy_file(src: Path, dest: Path) -> None:
    ensure(dest.parent)
    shutil.copy2(src, dest)
    print("copy", src.relative_to(ROOT), "->", dest.relative_to(ROOT))


def archive_style_refs() -> None:
    """Move everything in style-refs except style-lock-v2 (+ recipe) to archive."""
    sr = APPROVED / "style-refs"
    arch = ensure(ARCHIVE / "style-refs-pre-tier-reorg")
    for child in list(sr.iterdir()):
        rel = f"style-refs/{child.name}"
        if child.name in ("style-lock-v2.png", "style-lock-v2.recipe.md"):
            continue
        dest = arch / child.name
        if dest.exists():
            print("archive exists", dest)
            continue
        shutil.move(str(child), str(dest))
        print("archive", child.name)


def write_readme(path: Path, text: str) -> None:
    ensure(path.parent)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def plate_dev_folder(plate: dict) -> str:
    """Map FLOW plate id → development/ folder name."""
    pid = plate["id"]
    beat = (plate.get("beat") or "").lower()
    mapping = {
        "cover": "Cover",
        "p01": "P01-title",
        "p02": "P02-about-spread",
        "p03": "P02-about-spread",  # same master
        "p04": "S01-approach",
        "p05": "S01-approach",
        "p06": "S02-threshold",
        "p07": "S02-threshold",
    }
    if pid in mapping:
        return mapping[pid]
    # generic from beat
    if "s3" in beat or "eyes" in beat:
        return "S03-eyes-met"
    if pid.startswith("p"):
        return pid.upper().replace("P0", "P0") if False else f"P{pid[1:].zfill(2) if pid[1:].isdigit() else pid[1:]}"
    return pid


def populate_development(plates: list[dict]) -> dict:
    """Copy keep/locked/keep-leaning plates into development/."""
    include = {"keep", "locked", "locked-provisional", "keep-leaning"}
    written: dict[str, list[str]] = {}

    for plate in plates:
        status = plate.get("status", "")
        if status not in include:
            continue
        path = ROOT / plate["path"]
        if not path.is_file():
            # try after moves - cover path may still be old
            print("MISSING source", plate["id"], plate["path"])
            continue

        folder = plate_dev_folder(plate)
        dest_dir = ensure(DEV / folder)

        # filename strategy for multi-page units
        if plate["id"] in ("p04",):
            dest = dest_dir / "art-left.png"
        elif plate["id"] in ("p05",):
            dest = dest_dir / "art-right.png"
        elif plate["id"] in ("p02", "p06"):
            dest = dest_dir / "art.png"
        elif plate["id"] in ("p03", "p07"):
            # same master as partner — skip duplicate unless different path
            if plate["path"] == next(
                (x["path"] for x in plates if x["id"] == ("p02" if plate["id"] == "p03" else "p06")),
                None,
            ):
                # write SOURCE.txt note only
                note = dest_dir / "SOURCE.md"
                if not note.exists() or plate["id"] == "p03":
                    pass
                dest = None  # don't duplicate
            else:
                dest = dest_dir / "art.png"
        elif plate["id"] == "cover":
            dest = dest_dir / "art.png"
        elif plate["id"] == "p01":
            dest = dest_dir / "art.png"
        else:
            dest = dest_dir / "art.png"

        if dest is None:
            # still record meta for p03
            meta = {
                "flow_id": plate["id"],
                "status": status,
                "source_mock": plate["path"],
                "version": plate.get("version"),
                "shared_with": "p02" if plate["id"] == "p03" else "p06",
                "note": "Same wide master as partner page — see art.png",
            }
            (dest_dir / f"meta-{plate['id']}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
            written.setdefault(folder, []).append(f"meta-{plate['id']}.json")
            continue

        copy_file(path, dest)
        meta = {
            "flow_id": plate["id"],
            "page": plate.get("page"),
            "beat": plate.get("beat"),
            "status": status,
            "version": plate.get("version"),
            "source_mock": plate["path"].replace("\\", "/"),
            "model": plate.get("model"),
            "date": plate.get("date"),
            "notes": plate.get("notes"),
            "tier": "development",
        }
        (dest_dir / f"meta-{plate['id']}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        # also a simple SOURCE pointer
        written.setdefault(folder, []).append(dest.name)

    return written


def stub_empty_folders() -> None:
    """Create empty development folders for remaining Flow v2 units."""
    stubs = [
        "S03-eyes-met",
        "S04-sit-here",
        "S05-chat",
        "S06-cocoa",
        "S07-camera",
        "S08-story",
        "S09-laugh",
        "S10-note",
        "S11-flue",
        "S12-window",
        "S12b-god-bless",
        "P-matter-thank-you",
        "P-quiet-close",
    ]
    for name in stubs:
        d = ensure(DEV / name)
        marker = d / ".gitkeep"
        if not any(d.iterdir()) or not list(d.glob("art*")):
            if not marker.exists():
                marker.write_text("", encoding="utf-8")


def update_flow(plates: list[dict]) -> None:
    """Add tier field; fix paths that moved into development for dashboard (keep mock path as source_of_truth)."""
    # Path remaps for files that left approved/
    remaps = {
        "Media/approved/style-refs/covers/WINNER-cover-front-beige-pj-v2.png": "Media/development/Cover/art.png",
        "Media/approved/pages/p01-title.png": "Media/development/P01-title/art.png",
    }

    for plate in plates:
        status = plate.get("status", "")
        old = plate.get("path", "").replace("\\", "/")

        # machine SoT: prefer development path when we copied there for keep/locked
        if status in ("keep", "locked", "locked-provisional", "keep-leaning"):
            folder = plate_dev_folder(plate)
            if plate["id"] == "p04":
                plate["development_path"] = f"Media/development/{folder}/art-left.png"
            elif plate["id"] == "p05":
                plate["development_path"] = f"Media/development/{folder}/art-right.png"
            elif plate["id"] in ("p03", "p07"):
                plate["development_path"] = f"Media/development/{folder}/art.png"
            else:
                plate["development_path"] = f"Media/development/{folder}/art.png"

            # Character/style north stars stay approved
            if old.startswith("Media/approved/characters/") or "style-lock-v2" in old:
                plate["tier"] = "approved"
            else:
                plate["tier"] = "development"
                # Update path to development for flipbook human dashboard consistency
                # Keep mock path in source_mock
                if "source_mock" not in plate:
                    plate["source_mock"] = old
                if old in remaps:
                    plate["path"] = remaps[old]
                elif (ROOT / plate.get("development_path", "")).is_file():
                    # Point path at development copy for keep pages (flipbook)
                    plate["path"] = plate["development_path"]
        elif status == "final" or status == "lulu-ready":
            plate["tier"] = "finals"
        else:
            # working / pending dials stay in mocks
            plate["tier"] = "development" if status in ("working",) else "mocks"
            if "path" in plate and plate["path"].startswith("Media/approved/") and "characters" not in plate["path"] and "style-lock" not in plate["path"]:
                # remap orphaned approved paths to archive if needed
                pass

    # Explicit: cover + p01 after move
    for plate in plates:
        if plate["id"] == "cover":
            plate["tier"] = "development"
            plate["source_mock"] = plate.get("source_mock") or "Media/generated/mocks/archive/style-refs-pre-tier-reorg/covers/WINNER-cover-front-beige-pj-v2.png"
            plate["path"] = "Media/development/Cover/art.png"
            plate["status"] = "keep"  # still locked-ish but not approved-forever
            # Keep caption noting beige-v2
        if plate["id"] == "p01":
            plate["tier"] = "development"
            plate["source_mock"] = plate.get("source_mock") or "Media/generated/mocks/P01-title/v22/"
            plate["path"] = "Media/development/P01-title/art.png"


def main() -> None:
    data = json.loads(FLOW.read_text(encoding="utf-8"))
    plates = data["plates"]

    ensure(DEV)
    ensure(FINALS)
    ensure(ARCHIVE)
    write_readme(
        FINALS / "README.md",
        """# Media/finals — Lulu-ready

Empty until a page has been through **InDesign** with live text, bleed, and export ready for Lulu.

Nothing is final until it graduates here from `Media/development/`.
""",
    )
    write_readme(
        DEV / "README.md",
        """# Media/development — current best (visual dashboard)

When Jon says **keep** / **lock it (for now)** — **copy** the plate here under the page/spread folder.

- One folder per Flow unit
- `art.png` (or `art-left.png` / `art-right.png` for splits)
- `meta-*.json` points back to mock RECIPE / FLOW

**Not Lulu-final.** Live type → `Media/finals/`.
**Not forever locks.** Characters + style-lock stay in `Media/approved/`.
""",
    )
    write_readme(
        APPROVED / "README.md",
        """# Media/approved — LOCKED FOREVER (north stars)

**Only:**
- `characters/` — Boy G0, Santa G0-v2, Jack Farrell portrait
- `style-refs/style-lock-v2.png` (+ recipe)

Nothing else belongs here. Page art → `Media/development/`. Lulu exports → `Media/finals/`.
""",
    )

    # --- Archive / move out of approved ---
    # Spreads → archive
    move_tree(APPROVED / "spreads", ARCHIVE / "approved-spreads-pre-v2")
    # Pages → will copy to development then archive remainder
    pages = APPROVED / "pages"
    if pages.exists():
        p01 = pages / "p01-title.png"
        if p01.is_file():
            copy_file(p01, DEV / "P01-title" / "art.png")
            recipe = pages / "p01-title.recipe.md"
            if recipe.is_file():
                copy_file(recipe, DEV / "P01-title" / "art.recipe.md")
        move_tree(pages, ARCHIVE / "approved-pages-pre-tier-reorg")
    # Covers folder
    covers = APPROVED / "covers"
    if covers.exists():
        # Prefer WINNER from style-refs if present for development Cover
        winner = APPROVED / "style-refs/covers/WINNER-cover-front-beige-pj-v2.png"
        if winner.is_file():
            copy_file(winner, DEV / "Cover" / "art.png")
        elif (covers / "cover-front.png").is_file():
            copy_file(covers / "cover-front.png", DEV / "Cover" / "art.png")
        move_tree(covers, ARCHIVE / "approved-covers-pre-tier-reorg")

    # Style refs (except lock) — copy winner first if Cover empty
    winner2 = APPROVED / "style-refs/covers/WINNER-cover-front-beige-pj-v2.png"
    if winner2.is_file() and not (DEV / "Cover" / "art.png").is_file():
        copy_file(winner2, DEV / "Cover" / "art.png")
    # mockup-quality: copy to development/_quality-targets before archive (still useful dials)
    mq = APPROVED / "style-refs/mockup-quality"
    if mq.is_dir():
        dest_mq = ensure(DEV / "_quality-targets")
        for f in mq.iterdir():
            if f.is_file():
                copy_file(f, dest_mq / f.name)
    archive_style_refs()

    # INDEX.md in approved root — rewrite
    write_readme(
        APPROVED / "INDEX.md",
        """# approved/ index

| Path | Role |
|------|------|
| `characters/` | Boy G0 · Santa G0-v2 · Jack portrait — **never regen without Jon** |
| `style-refs/style-lock-v2.png` | Sole active style north star |

See `Media/development/` for current-best page art. See `Media/finals/` for Lulu-ready.
""",
    )

    # Populate from FLOW (after cover/p01 seeded)
    written = populate_development(plates)
    stub_empty_folders()

    # Also copy split stepping stones note into P02 folder
    split_note = DEV / "P02-about-spread" / "SPLIT-REFS.md"
    split_note.write_text(
        "Stepping-stone identity refs (status keep):\n"
        "- `Media/generated/mocks/P02-fireplace/v01/art.png`\n"
        "- `Media/generated/mocks/P03-tree/v01/art.png`\n"
        "Keeper spread: `art.png` (= mocks/P02-about-spread/v04)\n",
        encoding="utf-8",
    )

    update_flow(plates)
    data["updated"] = "2026-07-22"
    data["media_tiers"] = {
        "approved": "Media/approved/ — characters + style-lock-v2 ONLY (forever)",
        "development": "Media/development/ — current-best page art (pre-InDesign)",
        "finals": "Media/finals/ — Lulu-ready after InDesign live text",
        "mocks": "Media/generated/mocks/ — dials / RECIPE versions",
        "archive": "Media/generated/mocks/archive/ — old approved pages/covers/spreads/style-refs",
    }
    data["plates"] = plates
    FLOW.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("FLOW updated")

    # Summary tree
    print("\n=== development/ ===")
    for p in sorted(DEV.rglob("*")):
        if p.is_file() and p.name != ".gitkeep":
            print(" ", p.relative_to(DEV))
    print("\n=== approved/ remaining ===")
    for p in sorted(APPROVED.rglob("*")):
        if p.is_file():
            print(" ", p.relative_to(APPROVED))
    print("\nwritten folders", sorted(written.keys()))


if __name__ == "__main__":
    main()
