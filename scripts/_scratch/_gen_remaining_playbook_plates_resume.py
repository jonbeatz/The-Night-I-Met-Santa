#!/usr/bin/env python3
"""Resume remaining plates after partial success (back+pastedown+p34 mock done)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
spec = importlib.util.spec_from_file_location(
    "gen", ROOT / "scripts/_scratch/_gen_remaining_playbook_plates.py"
)
assert spec and spec.loader
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

from PIL import Image

tmp = ROOT / "Media/generated/mocks/_tmp-remaining"
tmp.mkdir(parents=True, exist_ok=True)

# Promote p34 mock already generated
mock_p34 = ROOT / "Media/generated/mocks/P34-padding/v01/art.png"
dev_p34 = ROOT / "Media/development/P34-padding/art.png"
dev_p34.parent.mkdir(parents=True, exist_ok=True)
art_p34 = Image.open(mock_p34).convert("RGB")
if art_p34.size != (gen.PAGE, gen.PAGE):
    art_p34 = art_p34.resize((gen.PAGE, gen.PAGE), Image.Resampling.LANCZOS)
art_p34.save(dev_p34, "PNG")
gen.write_recipe("P34-padding", "v01", mock_p34, "749639044", gen.QWEN, gen.P34_PROMPT)
print("promoted p34")

# Ensure pastedown + back in development
mock_back = ROOT / "Media/generated/mocks/Cover-back/v01/art.png"
dev_back = ROOT / "Media/development/Cover/art-back.png"
Image.open(mock_back).convert("RGB").resize((gen.PAGE, gen.PAGE), Image.Resampling.LANCZOS).save(
    dev_back, "PNG"
)
if not (ROOT / "Media/development/Cover/pastedown-burgundy.png").is_file():
    gen.solid_burgundy(ROOT / "Media/development/Cover/pastedown-burgundy.png")

style_ref = gen.prep_square(gen.STYLE, tmp / "style.png")
frame_ref = gen.prep_square(gen.FRAME, tmp / "frame.png")

# p35
mock_p35 = ROOT / "Media/generated/mocks/P35-colophon/v01"
dev_p35 = ROOT / "Media/development/P35-colophon/art.png"
p30_ref = gen.prep_square(gen.P30, tmp / "p30.png")
art_p35, seed_p35 = gen.qwen_edit(
    gen.P35_PROMPT, [p30_ref, style_ref, frame_ref], mock_p35 / "art.png"
)
dev_p35.parent.mkdir(parents=True, exist_ok=True)
art_p35.save(dev_p35, "PNG")
gen.write_recipe("P35-colophon", "v01", mock_p35 / "art.png", seed_p35, gen.QWEN, gen.P35_PROMPT)

# p36
mock_p36 = ROOT / "Media/generated/mocks/P36-blank/v01/art.png"
dev_p36 = ROOT / "Media/development/P36-blank/art.png"
gen.blank_cream(mock_p36, soft_vignette=False)
gen.blank_cream(dev_p36, soft_vignette=False)
gen.write_recipe(
    "P36-blank",
    "v01",
    mock_p36,
    "n/a",
    f"Pillow cream RGB{gen.CREAM}",
    "Final blank — printer-friendly even end. No illustration.",
)

# SeedVR Cover + P01
cover_2625 = ROOT / "Media/development/Cover/art-2625.png"
p01_2625 = ROOT / "Media/development/P01-title/art-2625.png"
mock_cover_print = ROOT / "Media/generated/mocks/Cover-print/v01/art.png"
mock_p01_print = ROOT / "Media/generated/mocks/P01-print/v01/art.png"
c = gen.seedvr_square(gen.COVER, cover_2625, 2.56)
mock_cover_print.parent.mkdir(parents=True, exist_ok=True)
c.save(mock_cover_print, "PNG")
p = gen.seedvr_square(gen.P01, p01_2625, 1.28)
mock_p01_print.parent.mkdir(parents=True, exist_ok=True)
p.save(mock_p01_print, "PNG")
gen.write_recipe(
    "Cover-print",
    "v01",
    mock_cover_print,
    "n/a",
    gen.SEEDVR,
    "Print-scale of beige-v2 KEEP — art.png (1024) untouched.",
)
gen.write_recipe(
    "P01-print",
    "v01",
    mock_p01_print,
    "n/a",
    gen.SEEDVR,
    "Print-scale of P01 v16 KEEP — art.png (2048) untouched.",
)

DAY = gen.DAY
gen.upsert_flow_plates(
    [
        {
            "id": "back-cover",
            "page": "Back",
            "beat": "Back Cover",
            "caption": "Back cover · v01 working (Qwen companion to beige-v2)",
            "path": "Media/development/Cover/art-back.png",
            "version": "v01",
            "model": gen.QWEN,
            "status": "working",
            "decided_by": "pending",
            "date": DAY,
            "notes": "Open center/bottom for ISBN+blurb+credit in InDesign · no baked text",
            "gpt_pillar": False,
            "development_path": "Media/development/Cover/art-back.png",
            "tier": "development",
            "source_mock": "Media/generated/mocks/Cover-back/v01/art.png",
        },
        {
            "id": "pastedown",
            "page": "Casewrap",
            "beat": "Pastedown",
            "caption": "Casewrap pastedown · solid burgundy LOCKED fill",
            "path": "Media/development/Cover/pastedown-burgundy.png",
            "version": "v01",
            "model": f"Pillow RGB{gen.BURGUNDY}",
            "status": "keep",
            "decided_by": "Jon",
            "date": "2026-07-22",
            "notes": "Inside front+back · casewrap only · not interior",
            "gpt_pillar": False,
            "development_path": "Media/development/Cover/pastedown-burgundy.png",
            "tier": "development",
            "source_mock": "Media/generated/mocks/Cover-pastedown/v01/art.png",
        },
        {
            "id": "p34",
            "page": "34",
            "beat": "Padding",
            "caption": "p34 · Optional quiet ornament · v01 working",
            "path": "Media/development/P34-padding/art.png",
            "version": "v01",
            "model": gen.QWEN,
            "status": "working",
            "decided_by": "pending",
            "date": DAY,
            "notes": "Optional padding — cut if trimming · FRAME ON",
            "gpt_pillar": False,
            "development_path": "Media/development/P34-padding/art.png",
            "tier": "development",
            "source_mock": "Media/generated/mocks/P34-padding/v01/art.png",
        },
        {
            "id": "p35",
            "page": "35",
            "beat": "Colophon",
            "caption": "p35 · Optional colophon paper · v01 working",
            "path": "Media/development/P35-colophon/art.png",
            "version": "v01",
            "model": gen.QWEN,
            "status": "working",
            "decided_by": "pending",
            "date": DAY,
            "notes": "Open cream for tiny reprint note · optional",
            "gpt_pillar": False,
            "development_path": "Media/development/P35-colophon/art.png",
            "tier": "development",
            "source_mock": "Media/generated/mocks/P35-colophon/v01/art.png",
        },
        {
            "id": "p36",
            "page": "36",
            "beat": "Blank",
            "caption": "p36 · Final blank cream · v01",
            "path": "Media/development/P36-blank/art.png",
            "version": "v01",
            "model": f"Pillow cream RGB{gen.CREAM}",
            "status": "working",
            "decided_by": "pending",
            "date": DAY,
            "notes": "Printer-friendly even end · optional",
            "gpt_pillar": False,
            "development_path": "Media/development/P36-blank/art.png",
            "tier": "development",
            "source_mock": "Media/generated/mocks/P36-blank/v01/art.png",
        },
    ]
)

idx = ROOT / "Media/generated/mocks/_INDEX"
idx.mkdir(parents=True, exist_ok=True)
Image.open(dev_back).save(idx / "remaining-back-cover.png")
art_p34.save(idx / "remaining-p34.png")
art_p35.save(idx / "remaining-p35.png")
Image.open(ROOT / "Media/development/Cover/pastedown-burgundy.png").save(idx / "remaining-pastedown.png")
Image.open(dev_p36).save(idx / "remaining-p36.png")
Image.open(cover_2625).save(idx / "remaining-cover-2625.png")
Image.open(p01_2625).save(idx / "remaining-p01-2625.png")
print("RESUME DONE")
