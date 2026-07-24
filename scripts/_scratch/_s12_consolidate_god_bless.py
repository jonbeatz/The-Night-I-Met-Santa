#!/usr/bin/env python3
"""Consolidate S12a / S12b / S12-closing → Media/development/S12-god-bless/."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development"
SRC = DEV / "S12-closing"
DST = DEV / "S12-god-bless"
OLD_A = DEV / "S12a-blessing"
OLD_B = DEV / "S12b-god-bless"
ARCHIVE = DEV / "_archive-s12-pre-consolidate-2026-07-23"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
POEM = ROOT / "scripts/book_poem_map.py"
BOARD = ROOT / "scripts/book_review_board.py"
DAY = "2026-07-23"


def main() -> None:
    if not SRC.is_dir():
        raise SystemExit(f"missing canonical source: {SRC}")

    # 1) Build destination from S12-closing (current truth)
    if DST.exists():
        # if leftover empty/wrong, park it
        if any(DST.iterdir()):
            bump = ARCHIVE / "S12-god-bless-preexisting"
            bump.parent.mkdir(parents=True, exist_ok=True)
            if bump.exists():
                shutil.rmtree(bump)
            shutil.move(str(DST), str(bump))
            print("parked preexisting", DST)
        else:
            DST.rmdir()

    shutil.copytree(SRC, DST)
    print("copied", SRC, "→", DST)

    # 2) Archive the three old folders
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for folder, name in ((OLD_A, "S12a-blessing"), (OLD_B, "S12b-god-bless"), (SRC, "S12-closing")):
        if not folder.exists():
            continue
        dest = ARCHIVE / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(folder), str(dest))
        print("archived", name, "→", dest)

    # 3) RECIPE at root of new folder
    (DST / "RECIPE.md").write_text(
        f"""# RECIPE — S12-god-bless

| Field | Value |
|-------|--------|
| **name** | S12 God Bless — epic closing FINAL STORY IMAGE |
| **pages** | **26\\|27** (former 28\\|29 absorbed) |
| **layout** | FULL SPREAD seamless · `art.png` + `art-left.png` + `art-right.png` |
| **version** | **v02d** (working) |
| **date** | {DAY} |
| **status** | working |
| **size** | 5250×2625 |

## Folder history

Consolidated {DAY} from `S12-closing` (merged S12a Blessing + S12b God Bless).  
Old trees archived under `Media/development/_archive-s12-pre-consolidate-2026-07-23/`.

## Current primary

- `art.png` / `art-left.png` / `art-right.png` = **v02d**
- Version dials: `v01/` … `v02d/`
""",
        encoding="utf-8",
    )
    (DST / "meta.json").write_text(
        json.dumps(
            {
                "unit": "S12-god-bless",
                "status": "working",
                "version": "v02d",
                "pages": "26|27",
                "absorbs_pages": "28|29",
                "former_units": ["S12a-blessing", "S12b-god-bless", "S12-closing"],
                "consolidated": DAY,
                "paths": {
                    "art": "Media/development/S12-god-bless/art.png",
                    "art_left": "Media/development/S12-god-bless/art-left.png",
                    "art_right": "Media/development/S12-god-bless/art-right.png",
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # 4) FLOW
    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v02d · ONE Santa · 8 reindeer (4 pairs; 9th lead pending) · "
        "moon L · North Star R · house+snowman · Media/development/S12-god-bless/ · "
        "consolidated from S12-closing {DAY}"
    ).replace("{DAY}", DAY)

    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "beat": f"S12 God Bless {'L' if side == 'left' else 'R'}",
                    "caption": (
                        "p26 · S12 God Bless L · v02d"
                        if p["id"] == "p26"
                        else "p27 · S12 God Bless R · v02d"
                    ),
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "unit": "S12-god-bless",
                    "version": "v02d",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                }
            )
        if p["id"] in ("p28", "p29"):
            side = "left" if p["id"] == "p28" else "right"
            p.update(
                {
                    "caption": f"{p['id']} · MERGED into S12-god-bless (p26|27)",
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "unit": "S12-god-bless",
                    "status": "merged",
                    "version": "merged-v02d",
                    "date": DAY,
                    "notes": "Absorbed into S12-god-bless on p26|27 — " + note,
                    "merged_into": "p26|27",
                }
            )

    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update(
                {
                    "beat": "S12 God Bless",
                    "version": "v02d",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "unit": "S12-god-bless",
                    "merges": ["S12a-blessing", "S12b-god-bless", "S12-closing"],
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                }
            )
        if d.get("page") == "28|29":
            d.update(
                {
                    "beat": "S12b God Bless (merged)",
                    "version": "merged-v02d",
                    "status": "merged",
                    "date": DAY,
                    "notes": "MERGED into S12-god-bless p26|27 — " + note,
                    "unit": "S12-god-bless",
                    "merged_into": "26|27",
                }
            )

    root["closing_merge_note"] = (
        f"{DAY} · Single folder Media/development/S12-god-bless/ "
        "(was S12a-blessing + S12b-god-bless → S12-closing → renamed). "
        "Book pages 26|27. Former 28|29 absorbed. "
        f"Old trees: Media/development/_archive-s12-pre-consolidate-{DAY}/"
    )
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(FLOW.read_text(encoding="utf-8"))
    print("FLOW OK")

    # 5) poem map — replace S12-closing / S12a / S12b with one S12-god-bless
    text = POEM.read_text(encoding="utf-8")
    # Remove the three old blocks and insert one clean block
    new_beat = '''    "S12-god-bless": {
        "unit": "S12-god-bless",
        "layout": "text_image",
        "left_page": 26,
        "right_page": 27,
        "left": (
            "He said I've had enough eggnogs, cider and soups. / "
            "My belt's getting harder to fit in the loops. / "
            "And one last thing, please do me a favor. / "
            "Always love Christmas, act like a kid and pray to your Savior."
        ),
        "right": "God bless. — under the North Star (text in InDesign).",
        "right_kind": "poem",
        "title": "S12 God Bless",
    },
'''
    # Strip S12-closing, S12a-blessing, S12b-god-bless entries
    text2 = re.sub(
        r'    "S12-closing": \{.*?\n    \},\n',
        "",
        text,
        count=1,
        flags=re.S,
    )
    text2 = re.sub(
        r'    "S12a-blessing": \{.*?\n    \},\n',
        "",
        text2,
        count=1,
        flags=re.S,
    )
    text2 = re.sub(
        r'    "S12b-god-bless": \{.*?\n    \},\n',
        new_beat,
        text2,
        count=1,
        flags=re.S,
    )
    if '"S12-god-bless"' not in text2:
        # fallback: insert before closing of BEATS
        text2 = text2.replace(
            "}\n\n\ndef resolve_unit",
            new_beat + "}\n\n\ndef resolve_unit",
            1,
        )

    # aliases
    text2 = text2.replace('"S12a": "S12a-blessing",', '"S12a": "S12-god-bless",')
    text2 = text2.replace('"S12b": "S12b-god-bless",', '"S12b": "S12-god-bless",')
    text2 = text2.replace('"S12c": "S12-closing",', '"S12c": "S12-god-bless",')
    text2 = text2.replace('"S12": "S12-closing",', '"S12": "S12-god-bless",')
    if '"S12-closing"' in text2 and "aliases" in text2:
        text2 = text2.replace('"S12-closing": "S12-closing",', '"S12-closing": "S12-god-bless",')
    # ensure S12-closing alias exists
    if '"S12-closing"' not in text2[text2.find("aliases") :]:
        text2 = text2.replace(
            '"S12": "S12-god-bless",',
            '"S12": "S12-god-bless",\n        "S12-closing": "S12-god-bless",',
            1,
        )

    POEM.write_text(text2, encoding="utf-8")
    # validate import
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    import importlib

    import book_poem_map

    importlib.reload(book_poem_map)
    assert "S12-god-bless" in book_poem_map.BEATS
    assert book_poem_map.resolve_unit("S12") == "S12-god-bless"
    assert book_poem_map.resolve_unit("S12-closing") == "S12-god-bless" or "S12-closing" in (
        book_poem_map.BEATS.get("S12-closing", {}) or {}
    ) or book_poem_map.resolve_unit("S12a") == "S12-god-bless"
    print("poem map OK", book_poem_map.captions("S12-god-bless")[1][:40])

    # 6) board tech map
    b = BOARD.read_text(encoding="utf-8")
    b2 = b.replace(
        '"S12a-blessing": "Qwen 2 Pro /edit · 2048×1024 · S3 v07 quality bar",\n'
        '    "S12b-god-bless": "Banana/GPT pillar · 2048×1024 · check FLOW gpt_pillar",',
        '"S12-god-bless": "Qwen 2 Pro /edit v06 · 5250×2625 · closing FINAL STORY IMAGE",',
    )
    if b2 == b:
        # looser replace
        if '"S12-god-bless"' not in b:
            b2 = b.replace(
                '"S12a-blessing":',
                '"S12-god-bless": "Qwen 2 Pro /edit v06 · 5250×2625 · closing FINAL STORY IMAGE",\n    "S12a-blessing":',
                1,
            )
    BOARD.write_text(b2, encoding="utf-8")
    print("board tech map updated")

    # 7) CONTINUE-HERE light touch
    cont = ROOT / ".cursor/docs/CONTINUE-HERE.md"
    if cont.is_file():
        t = cont.read_text(encoding="utf-8")
        t = t.replace("S12-closing", "S12-god-bless")
        t = t.replace("S12a + S12b", "S12-god-bless")
        cont.write_text(t, encoding="utf-8")

    # verify layout
    for name in ("art.png", "art-left.png", "art-right.png"):
        assert (DST / name).is_file(), name
    assert not SRC.exists()
    assert not OLD_A.exists()
    assert not OLD_B.exists()
    print("DONE — only", DST)


if __name__ == "__main__":
    main()
