#!/usr/bin/env python3
"""TNIMS retroactive apply: S4 comparison boards + Flow v2 flipbook + verdict card."""
from __future__ import annotations

import json
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHARED = Path(r"D:\Hermes\projects\_core-scripts\shared-profile-content\scripts")
DAY = "2026-07-22"

import importlib.util


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


board_mod = _load("book_comparison_board", SHARED / "book-comparison-board.py")
flip_mod = _load("book_flipbook_assemble", SHARED / "book-flipbook-assemble.py")

# Copy helpers into project scripts for local npm wiring
for name in ("book-comparison-board.py", "book-flipbook-assemble.py"):
    shutil.copy2(SHARED / name, ROOT / "scripts" / name)


def boards() -> list[Path]:
    base = ROOT / "Media/generated/mocks/S04-sit-here"
    idx = base / "_INDEX"
    outs = []

    outs.append(
        board_mod.build(
            left=base / "v01/art.png",
            center=base / "v02/art.png",
            right=base / "v03/art.png",
            left_label="Klein 9B|v01|~$0.01|1536²|baseline control · punchy Dial D2",
            center_label="Krea 2 Medium|v02|~$0.03|1536²|painterly style-lock candidate",
            right_label="Qwen Image 2 Pro|v03|~$0.08|1536²|alt detail / prior favorite lane",
            out=idx / f"S04-sit-here-comparison-plain-{DAY}.png",
            title=f"S4 Sit Here — plain T2I style-lock ({DAY})",
        )
    )
    outs.append(
        board_mod.build(
            left=base / "v04/art.png",
            center=base / "v05/art.png",
            right=base / "v06/art.png",
            left_label="Klein 9B /edit|v04|~$0.01+|1536²|control + styles2 refs",
            center_label="Krea 2 Medium|v05|~$0.03|1536²|refs · style-lock WINNER",
            right_label="Qwen 2 Pro /edit|v06|~$0.08|1536²|refs · higher face/gift detail",
            out=idx / f"S04-sit-here-comparison-refs-{DAY}.png",
            title=f"S4 Sit Here — with styles2 refs ({DAY})",
        )
    )
    outs.append(
        board_mod.build(
            left=base / "v04/art.png",
            center=base / "v07/art.png",
            right=base / "v05/art.png",
            left_label="Klein 9B /edit|v04|~$0.01+|1536²|Klein control (refs round)",
            center_label="Krea blend|v07|~$0.03|1536²|v05@0.92+v06@0.48 · CURRENT FAVORITE",
            right_label="Krea 2 Medium|v05|~$0.03|1536²|previous winner · promoted style-lock-v2",
            out=idx / f"S04-sit-here-comparison-blend-{DAY}.png",
            title=f"S4 Sit Here — blend pass v05·v06·v07 ({DAY}) · Qwen v06 = detail guide",
        )
    )
    # Also emit the exact v05|v06|v07 visual Jon asked for (center=new, right=Qwen, left=prior fav)
    # Rule requires Klein on left — already done above. Extra labeled trio for the blend trio itself:
    outs.append(
        board_mod.build(
            left=base / "v05/art.png",
            center=base / "v07/art.png",
            right=base / "v06/art.png",
            left_label="Krea 2 Medium|v05|~$0.03|1536²|prior favorite entering blend",
            center_label="Krea blend|v07|~$0.03|1536²|NEW · atmosphere+detail blend",
            right_label="Qwen 2 Pro /edit|v06|~$0.08|1536²|detail donor for blend",
            out=idx / f"S04-sit-here-comparison-blend-trio-{DAY}.png",
            title=f"S4 blend trio v05 | v07 | v06 ({DAY}) — note: Klein control board is *-comparison-blend-*",
        )
    )
    return outs


def flipbook() -> Path:
    paper = "Media/generated/mocks/_INDEX/text-page-lora/v03-scale035/art.png"
    pages = [
        {"caption": "Cover · beige-v2 LOCKED", "path": "Media/approved/style-refs/covers/WINNER-cover-front-beige-pj-v2.png", "beat": "Cover"},
        {"caption": "p1 · Title · P01 v22 LOCKED", "path": "Media/approved/pages/p01-title.png", "beat": "Title"},
        {"caption": "p2 · About (mock stand-in)", "path": "Media/generated/mocks/P05-about-vignette/v01/art.png", "beat": "About"},
        {"caption": "p3 · Dedication (mock stand-in)", "path": "Media/generated/mocks/P03-dedication/v01/art.png", "beat": "Dedication"},
        {"caption": "p4 · S1 Approach L (split — single dial for now)", "path": "Media/generated/mocks/S01-approach/v01/art.png", "beat": "S1 L"},
        {"caption": "p5 · S1 Approach R · door hero (style-ref)", "path": "Media/approved/style-refs/pages/p08-beat02-the-door.png", "beat": "S1 R"},
        {"caption": "p6 · S2 Threshold L (v02 dial — needs L/R split later)", "path": "Media/generated/mocks/S02-threshold/v02/art.png", "beat": "S2 L"},
        {"caption": "p7 · S2 Threshold R (same dial placeholder)", "path": "Media/generated/mocks/S02-threshold/v02/art.png", "beat": "S2 R"},
        {"caption": "p8 · S3 Eyes Met L · LOCKED", "path": "Media/approved/spreads/spread-01-eyes-met-LEFT.png", "beat": "S3 L"},
        {"caption": "p9 · S3 Eyes Met R · LOCKED", "path": "Media/approved/spreads/spread-01-eyes-met-RIGHT.png", "beat": "S3 R"},
        {"caption": "p10 · S4 Sit Here L · text paper (LoRA v03)", "path": paper, "beat": "S4 L"},
        {"caption": "p11 · S4 Sit Here R · style-lock-v2 / v07", "path": "Media/approved/style-refs/style-lock-v2.png", "beat": "S4 R"},
        {"caption": "p12 · S5 Chat L (v02 dial placeholder)", "path": "Media/generated/mocks/S05-chat/v02/art.png", "beat": "S5 L"},
        {"caption": "p13 · S5 Chat R (same dial placeholder)", "path": "Media/generated/mocks/S05-chat/v02/art.png", "beat": "S5 R"},
        {"caption": "p14 · S6 Cocoa L · text paper", "path": paper, "beat": "S6 L"},
        {"caption": "p15 · S6 Cocoa R · cocoa reveal", "path": "Media/approved/style-refs/story/scene-06-cocoa-reveal-SQUARE.png", "beat": "S6 R"},
        {"caption": "p16 · S7 Proof L (v07 dial placeholder)", "path": "Media/generated/mocks/S07-proof/v07/art.png", "beat": "S7 L"},
        {"caption": "p17 · S7 Proof R (same dial placeholder)", "path": "Media/generated/mocks/S07-proof/v07/art.png", "beat": "S7 R"},
        {"caption": "p18 · S8 Gone L (v02 dial placeholder)", "path": "Media/generated/mocks/S08-gone/v02/art.png", "beat": "S8 L"},
        {"caption": "p19 · S8 Gone R (same dial placeholder)", "path": "Media/generated/mocks/S08-gone/v02/art.png", "beat": "S8 R"},
        {"caption": "p20 · S9 Search L (v01 dial)", "path": "Media/generated/mocks/S09-search/v01/art.png", "beat": "S9 L"},
        {"caption": "p21 · S9 Search R · chair/note (style-ref)", "path": "Media/approved/style-refs/pages/p20-beat11-flue-chair.png", "beat": "S9 R"},
        {"caption": "p22 · S10 Note L · text paper", "path": paper, "beat": "S10 L"},
        {"caption": "p23 · S10 Note R", "path": "Media/approved/style-refs/pages/p22-beat12-13-note-RIGHT.png", "beat": "S10 R"},
        {"caption": "p24 · S11 Wish L (v02 dial placeholder)", "path": "Media/generated/mocks/S11-wish/v02/art.png", "beat": "S11 L"},
        {"caption": "p25 · S11 Wish R (same dial placeholder)", "path": "Media/generated/mocks/S11-wish/v02/art.png", "beat": "S11 R"},
        {"caption": "p26 · S12a Blessing L (approved chop)", "path": "Media/approved/style-refs/spread/spread-04-closing-blessing-LEFT.png", "beat": "S12a L"},
        {"caption": "p27 · S12a Blessing R (approved chop)", "path": "Media/approved/style-refs/spread/spread-04-closing-blessing-RIGHT.png", "beat": "S12a R"},
        {"caption": "p28 · S12b God Bless L · GPT High 4K (split)", "path": "Media/generated/mocks/S12b-god-bless/v01-gpt4k/art.png", "beat": "S12b L", "split": "L"},
        {"caption": "p29 · S12b God Bless R · GPT High 4K (split)", "path": "Media/generated/mocks/S12b-god-bless/v01-gpt4k/art.png", "beat": "S12b R", "split": "R"},
        {"caption": "p30 · Thank You L · text paper", "path": paper, "beat": "TY L"},
        {"caption": "p31 · Author portrait · LOCKED", "path": "Media/approved/characters/jack-farrell-portrait.png", "beat": "Author"},
        {"caption": "p32 · Quiet Close L", "path": "Media/generated/mocks/P32-quiet-close/v01/art.png", "beat": "Close L"},
        {"caption": "p33 · Quiet Close R", "path": "Media/generated/mocks/P33-merry-christmas/v01/art.png", "beat": "Close R"},
    ]

    verdicts = [
        {"page": "Cover", "beat": "Cover", "version": "beige-v2", "model": "locked", "status": "locked", "notes": "oatmeal holly PJs · Santa face hidden"},
        {"page": "1", "beat": "Title", "version": "v22", "model": "Gemini/Banana", "status": "locked", "notes": "provisional P01 · Media/approved/pages/p01-title.png"},
        {"page": "2|3", "beat": "About+Dedication", "version": "mocks", "model": "various", "status": "keep-leaning", "notes": "need Flow v2 combined fireplace/window spread"},
        {"page": "4|5", "beat": "S1 Approach", "version": "v01+ref", "model": "Klein + style-ref", "status": "keep-leaning", "notes": "SPLIT required · regenerate as two plates"},
        {"page": "6|7", "beat": "S2 Threshold", "version": "v02", "model": "Klein 9B", "status": "keep-leaning", "notes": "single dial · needs seamless L/R"},
        {"page": "8|9", "beat": "S3 Eyes Met", "version": "locked", "model": "—", "status": "locked", "notes": "Do not regen G0 lock · Flow wants floor-level redo later"},
        {"page": "10|11", "beat": "S4 Sit Here", "version": "v07 / lock", "model": "Krea blend", "status": "keep", "notes": "style-lock-v2 · holly PJs · TEXT L = LoRA paper @0.35"},
        {"page": "12|13", "beat": "S5 Chat", "version": "v02", "model": "Klein 9B", "status": "keep-leaning", "notes": "needs L Santa / R boy split per Flow"},
        {"page": "14|15", "beat": "S6 Cocoa", "version": "style-ref", "model": "prior", "status": "keep-leaning", "notes": "R cocoa OK as mood · L decorative text page TBD"},
        {"page": "16|17", "beat": "S7 Proof", "version": "v07", "model": "Klein 9B", "status": "keep-leaning", "notes": "wardrobe check · look-up angle"},
        {"page": "18|19", "beat": "S8 Gone", "version": "v02", "model": "Klein 9B", "status": "keep-leaning", "notes": "camera prop hero · empty room R"},
        {"page": "20|21", "beat": "S9 Search", "version": "v01+ref", "model": "Klein + style-ref", "status": "keep-leaning", "notes": "SPLIT search vs chair discovery"},
        {"page": "22|23", "beat": "S10 Note", "version": "style-ref", "model": "prior", "status": "keep", "notes": "R note read strong · L paper LoRA"},
        {"page": "24|25", "beat": "S11 Wish", "version": "v02", "model": "Klein 9B", "status": "keep-leaning", "notes": "moon window L / boy reading R"},
        {"page": "26|27", "beat": "S12a Blessing", "version": "approved chops", "model": "locked-ish", "status": "keep", "notes": "closing blessing chops · verify Flow camera"},
        {"page": "28|29", "beat": "S12b God Bless", "version": "v01-gpt4k", "model": "GPT Image 2 High", "status": "keep-leaning", "notes": "epic clarity · style drift vs lock · Jon hero call pending · Krea dial alt v02"},
        {"page": "30|31", "beat": "Thank You+Author", "version": "portrait lock", "model": "—", "status": "locked", "notes": "Jack portrait LOCKED · L paper LoRA"},
        {"page": "32|33", "beat": "Quiet Close", "version": "v01", "model": "various", "status": "keep-leaning", "notes": "optional trim if cutting pages"},
    ]

    manifest = {
        "title": "The Night I Met Santa — Flow Flipbook",
        "date": DAY,
        "flow_doc": "JON-BOOK-FLOW-v2-FINAL.md",
        "models": "Klein 9B · Krea 2 · Qwen 2 Pro · GPT Image 2 High · FLUX.2 LoRA paper",
        "root": str(ROOT),
        "pages": pages,
        "verdicts": verdicts,
    }
    man_path = ROOT / "Output" / f"flipbook-{DAY}-manifest.json"
    man_path.parent.mkdir(parents=True, exist_ok=True)
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    out_pdf = ROOT / "Output" / f"flipbook-{DAY}.pdf"
    out_json = ROOT / "Output" / f"flipbook-{DAY}-verdicts.json"
    flip_mod.assemble(manifest, out_pdf, out_json)
    return out_pdf


def main() -> int:
    print("=== Comparison boards ===")
    for p in boards():
        print(" ", p)
    print("=== Flipbook ===")
    print(" ", flipbook())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
