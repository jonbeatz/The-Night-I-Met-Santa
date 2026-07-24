#!/usr/bin/env python3
"""FULL AUDIT FIX — unit RECIPE.md + meta.json, FLOW S12 dedup, quality target."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
DAY = "2026-07-24"
QWEN = "fal-ai/qwen-image-2/pro/edit"


def size_of(rel: str) -> str:
    p = ROOT / rel
    if not p.is_file():
        return "n/a"
    w, h = Image.open(p).size
    return f"{w}x{h}"


def dims(rel: str) -> list[int] | None:
    p = ROOT / rel
    if not p.is_file():
        return None
    return list(Image.open(p).size)


def write_recipe(unit: str, body: str) -> None:
    path = DEV / unit / "RECIPE.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")
    print("RECIPE", path.relative_to(ROOT))


def write_meta(unit: str, data: dict) -> None:
    path = DEV / unit / "meta.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("meta ", path.relative_to(ROOT))


def recipe_block(
    *,
    title: str,
    unit: str,
    pages: str,
    version: str,
    model: str,
    resolution: str,
    seed: str,
    date: str,
    status: str,
    composition: str,
    paths: list[str],
    notes: str = "",
) -> str:
    path_lines = "\n".join(f"- `{p}`" for p in paths)
    return f"""# RECIPE — {title}

| Field | Value |
|-------|--------|
| **unit** | {unit} |
| **book pages** | {pages} |
| **version locked** | {version} |
| **model** | `{model}` |
| **resolution** | {resolution} |
| **seed** | {seed} |
| **date** | {date} |
| **status** | {status} |
| **dashboard** | `Media/development/{unit}/` |

## Composition notes

{composition}

## Art file paths

{path_lines}

## Notes

{notes or "Unit-root recipe for current FLOW keep / working plate. Version subfolders may hold dial history."}
"""


def build_docs() -> None:
    # --- S01 ---
    write_recipe(
        "S01-approach",
        recipe_block(
            title="S01-approach / current KEEP",
            unit="S01-approach",
            pages="p4|p5 · S1 Approach (split)",
            version="v13 L + v14 R",
            model=QWEN,
            resolution=f"master {size_of('Media/development/S01-approach/art.png')} · singles {size_of('Media/development/S01-approach/art-left.png')}",
            seed="n/a (see mocks S01-approach/v13|v14)",
            date="2026-07-22",
            status="keep",
            composition=(
                "Crack-is-the-story continuity. LEFT: narrow 4–6in crack · chiaroscuro crawl · holly PJs. "
                "RIGHT: face-on wider 6–8in crack · same door/wreath. Split images (not seamless)."
            ),
            paths=[
                "Media/development/S01-approach/art.png",
                "Media/development/S01-approach/art-left.png",
                "Media/development/S01-approach/art-right.png",
            ],
        ),
    )
    write_meta(
        "S01-approach",
        {
            "unit": "S01-approach",
            "version": "v13|v14",
            "status": "keep",
            "date": "2026-07-22",
            "model": QWEN,
            "resolution": size_of("Media/development/S01-approach/art.png"),
            "dimensions": {
                "art.png": dims("Media/development/S01-approach/art.png"),
                "art-left.png": dims("Media/development/S01-approach/art-left.png"),
                "art-right.png": dims("Media/development/S01-approach/art-right.png"),
            },
            "paths": {
                "master": "Media/development/S01-approach/art.png",
                "left": "Media/development/S01-approach/art-left.png",
                "right": "Media/development/S01-approach/art-right.png",
            },
            "pages": {"left": 4, "right": 5},
        },
    )

    # --- S02 ---
    write_recipe(
        "S02-threshold",
        recipe_block(
            title="S02-threshold / v06 KEEP",
            unit="S02-threshold",
            pages="p6|p7 · S2 Threshold (seamless)",
            version="v06",
            model=QWEN,
            resolution=size_of("Media/development/S02-threshold/art.png"),
            seed="381681017",
            date="2026-07-22",
            status="keep",
            composition=(
                "Boy in doorway · golden spill L · open-coat Santa G0 v2 at tree R · "
                "striped shirt · suspenders over shirt. Seamless spread."
            ),
            paths=[
                "Media/development/S02-threshold/art.png",
                "Media/development/S02-threshold/art-left.png",
                "Media/development/S02-threshold/art-right.png",
            ],
            notes="Dial history: v04/v05/v06 under unit folder. Seed/request from v06/RECIPE.md.",
        ),
    )
    write_meta(
        "S02-threshold",
        {
            "unit": "S02-threshold",
            "version": "v06",
            "status": "keep",
            "date": "2026-07-22",
            "model": QWEN,
            "resolution": size_of("Media/development/S02-threshold/art.png"),
            "seed": 381681017,
            "request_id": "019f8d79-604f-7a63-b235-f0eb6a89ab2e",
            "dimensions": {
                "art.png": dims("Media/development/S02-threshold/art.png"),
                "art-left.png": dims("Media/development/S02-threshold/art-left.png"),
                "art-right.png": dims("Media/development/S02-threshold/art-right.png"),
            },
            "paths": {
                "master": "Media/development/S02-threshold/art.png",
                "left": "Media/development/S02-threshold/art-left.png",
                "right": "Media/development/S02-threshold/art-right.png",
            },
            "pages": {"left": 6, "right": 7},
        },
    )

    # --- S03 ---
    write_recipe(
        "S03-eyes-met",
        recipe_block(
            title="S03-eyes-met / v07 KEEP — QUALITY BAR",
            unit="S03-eyes-met",
            pages="p8|p9 · S3 Eyes Met (seamless)",
            version="v07",
            model=QWEN,
            resolution=size_of("Media/development/S03-eyes-met/art.png"),
            seed="1762521583",
            date="2026-07-22",
            status="keep · QUALITY BAR",
            composition=(
                "Oil warmth · burgundy walls · fire/tree gold · wide room · open-coat Santa · "
                "Boy G0 holly PJs · eyes meet. Prefer fewer gifts on later plates."
            ),
            paths=[
                "Media/development/S03-eyes-met/art.png",
                "Media/development/S03-eyes-met/art-left.png",
                "Media/development/S03-eyes-met/art-right.png",
                "Media/development/_quality-targets/S03-eyes-met-v07-quality-bar.jpg",
            ],
            notes="Canonical dial RECIPE also at v07/RECIPE.md. Quality target copy for finals pass.",
        ),
    )
    write_meta(
        "S03-eyes-met",
        {
            "unit": "S03-eyes-met",
            "version": "v07",
            "status": "keep",
            "date": "2026-07-22",
            "model": QWEN,
            "resolution": size_of("Media/development/S03-eyes-met/art.png"),
            "seed": 1762521583,
            "request_id": "019f8d46-96c9-73a2-927b-96b413086a94",
            "quality_bar": True,
            "dimensions": {
                "art.png": dims("Media/development/S03-eyes-met/art.png"),
                "art-left.png": dims("Media/development/S03-eyes-met/art-left.png"),
                "art-right.png": dims("Media/development/S03-eyes-met/art-right.png"),
            },
            "paths": {
                "master": "Media/development/S03-eyes-met/art.png",
                "left": "Media/development/S03-eyes-met/art-left.png",
                "right": "Media/development/S03-eyes-met/art-right.png",
                "quality_target": "Media/development/_quality-targets/S03-eyes-met-v07-quality-bar.jpg",
            },
            "pages": {"left": 8, "right": 9},
        },
    )

    # --- S04 ---
    write_recipe(
        "S04-sit-here",
        recipe_block(
            title="S04-sit-here / v13 KEEP",
            unit="S04-sit-here",
            pages="p10|p11 · S4 Sit Here (TEXT+IMAGE)",
            version="v13",
            model=QWEN,
            resolution=f"master {size_of('Media/development/S04-sit-here/art.png')} · singles {size_of('Media/development/S04-sit-here/art-left.png')}",
            seed="L 739714616 · R 1422180652",
            date="2026-07-22",
            status="keep",
            composition=(
                "LEFT: cream watercolor text page · tiny mistletoe upper-right. "
                "RIGHT: Santa RIGHT open-coat beckons · Boy LEFT holly PJs · gift sea · burgundy."
            ),
            paths=[
                "Media/development/S04-sit-here/art.png",
                "Media/development/S04-sit-here/art-left.png",
                "Media/development/S04-sit-here/art-right.png",
            ],
        ),
    )
    write_meta(
        "S04-sit-here",
        {
            "unit": "S04-sit-here",
            "version": "v13",
            "status": "keep",
            "date": "2026-07-22",
            "model": QWEN,
            "resolution": size_of("Media/development/S04-sit-here/art.png"),
            "seeds": {"left": 739714616, "right": 1422180652},
            "dimensions": {
                "art.png": dims("Media/development/S04-sit-here/art.png"),
                "art-left.png": dims("Media/development/S04-sit-here/art-left.png"),
                "art-right.png": dims("Media/development/S04-sit-here/art-right.png"),
            },
            "paths": {
                "master": "Media/development/S04-sit-here/art.png",
                "left": "Media/development/S04-sit-here/art-left.png",
                "right": "Media/development/S04-sit-here/art-right.png",
            },
            "pages": {"left": 10, "right": 11},
            "layout": "text_plus_image",
        },
    )

    # --- S05 ---
    write_recipe(
        "S05-chat",
        recipe_block(
            title="S05-chat / v01 KEEP",
            unit="S05-chat",
            pages="p12|p13 · S5 Chat (seamless)",
            version="v01",
            model=QWEN,
            resolution=size_of("Media/development/S05-chat/art.png"),
            seed="n/a (see v01/meta.json)",
            date="2026-07-22",
            status="keep",
            composition=(
                "Santa by hearth laughing · open-coat L · boy cross-legged beaming holly PJs R · "
                "fireplace + tree · gift clutter. Watch: Santa arm near gutter."
            ),
            paths=[
                "Media/development/S05-chat/art.png",
                "Media/development/S05-chat/art-left.png",
                "Media/development/S05-chat/art-right.png",
            ],
        ),
    )
    write_meta(
        "S05-chat",
        {
            "unit": "S05-chat",
            "version": "v01",
            "status": "keep",
            "date": "2026-07-22",
            "model": QWEN,
            "resolution": size_of("Media/development/S05-chat/art.png"),
            "dimensions": {
                "art.png": dims("Media/development/S05-chat/art.png"),
                "art-left.png": dims("Media/development/S05-chat/art-left.png"),
                "art-right.png": dims("Media/development/S05-chat/art-right.png"),
            },
            "paths": {
                "master": "Media/development/S05-chat/art.png",
                "left": "Media/development/S05-chat/art-left.png",
                "right": "Media/development/S05-chat/art-right.png",
            },
            "pages": {"left": 12, "right": 13},
        },
    )

    # --- S06 ---
    write_recipe(
        "S06-cocoa",
        recipe_block(
            title="S06-cocoa / KEEP (v04 L + v03 R)",
            unit="S06-cocoa",
            pages="p14|p15 · S6 Cocoa (TEXT+IMAGE)",
            version="v04 L + v03 R",
            model=QWEN,
            resolution=f"master {size_of('Media/development/S06-cocoa/art.png')} · singles {size_of('Media/development/S06-cocoa/art-left.png')}",
            seed="n/a",
            date="2026-07-23",
            status="keep",
            composition=(
                "LEFT: village dissolve · deep blue sky · warm golden windows · cream vignette (text page). "
                "RIGHT: Santa solo cocoa · open coat · striped shirt · fireplace + tree · NO boy · cream vignette."
            ),
            paths=[
                "Media/development/S06-cocoa/art.png",
                "Media/development/S06-cocoa/art-left.png",
                "Media/development/S06-cocoa/art-right.png",
            ],
        ),
    )
    write_meta(
        "S06-cocoa",
        {
            "unit": "S06-cocoa",
            "version": "v04|v03",
            "status": "keep",
            "date": "2026-07-23",
            "model": QWEN,
            "resolution": size_of("Media/development/S06-cocoa/art.png"),
            "dimensions": {
                "art.png": dims("Media/development/S06-cocoa/art.png"),
                "art-left.png": dims("Media/development/S06-cocoa/art-left.png"),
                "art-right.png": dims("Media/development/S06-cocoa/art-right.png"),
            },
            "paths": {
                "master": "Media/development/S06-cocoa/art.png",
                "left": "Media/development/S06-cocoa/art-left.png",
                "right": "Media/development/S06-cocoa/art-right.png",
            },
            "pages": {"left": 14, "right": 15},
            "layout": "text_plus_image",
        },
    )

    # --- Cover ---
    write_recipe(
        "Cover",
        recipe_block(
            title="Cover / beige-v2 KEEP",
            unit="Cover",
            pages="Cover (front) · back · pastedown",
            version="beige-v2",
            model="locked (beige-v2)",
            resolution=f"art.png {size_of('Media/development/Cover/art.png')} · art-2625 {size_of('Media/development/Cover/art-2625.png')}",
            seed="n/a",
            date="2026-07-18",
            status="keep",
            composition=(
                "Front: oatmeal holly PJs · Santa face HIDDEN. "
                "Also present: art-back.png (v02 working), pastedown-burgundy.png, art-2625 print-scale (KEEP art.png untouched)."
            ),
            paths=[
                "Media/development/Cover/art.png",
                "Media/development/Cover/art-2625.png",
                "Media/development/Cover/art-back.png",
                "Media/development/Cover/pastedown-burgundy.png",
            ],
        ),
    )
    write_meta(
        "Cover",
        {
            "unit": "Cover",
            "version": "beige-v2",
            "status": "keep",
            "date": "2026-07-18",
            "model": "locked",
            "resolution": size_of("Media/development/Cover/art.png"),
            "dimensions": {
                "art.png": dims("Media/development/Cover/art.png"),
                "art-2625.png": dims("Media/development/Cover/art-2625.png"),
                "art-back.png": dims("Media/development/Cover/art-back.png"),
                "pastedown-burgundy.png": dims("Media/development/Cover/pastedown-burgundy.png"),
            },
            "paths": {
                "front": "Media/development/Cover/art.png",
                "front_2625": "Media/development/Cover/art-2625.png",
                "back": "Media/development/Cover/art-back.png",
                "pastedown": "Media/development/Cover/pastedown-burgundy.png",
            },
        },
    )

    # --- P01 ---
    write_recipe(
        "P01-title",
        recipe_block(
            title="P01-title / v16 KEEP",
            unit="P01-title",
            pages="p1 · Title",
            version="v16",
            model="Pillow structure lock (+ Qwen polish rejected)",
            resolution=f"art.png {size_of('Media/development/P01-title/art.png')} · art-2625 {size_of('Media/development/P01-title/art-2625.png')}",
            seed="1271918122 (v16 Qwen attempt; Pillow base kept)",
            date="2026-07-22",
            status="keep",
            composition=(
                "Winter window + tree on clean cream · warm gold page-edge whisper · "
                "open cream above/below for live title/copyright. FRAME ON. art-2625 = SeedVR print-scale; KEEP art.png."
            ),
            paths=[
                "Media/development/P01-title/art.png",
                "Media/development/P01-title/art-2625.png",
                "Media/development/P01-title/v16/art.png",
            ],
            notes="Full dial history under v01–v22. See also art.recipe.md.",
        ),
    )
    write_meta(
        "P01-title",
        {
            "unit": "P01-title",
            "version": "v16",
            "status": "keep",
            "date": "2026-07-22",
            "model": "Pillow + fal-ai/qwen-image-2/pro/edit (polish rejected)",
            "resolution": size_of("Media/development/P01-title/art.png"),
            "seed": 1271918122,
            "dimensions": {
                "art.png": dims("Media/development/P01-title/art.png"),
                "art-2625.png": dims("Media/development/P01-title/art-2625.png"),
            },
            "paths": {
                "art": "Media/development/P01-title/art.png",
                "art_2625": "Media/development/P01-title/art-2625.png",
                "locked_version": "Media/development/P01-title/v16/art.png",
            },
            "page": 1,
        },
    )

    # --- P02 ---
    write_recipe(
        "P02-about-spread",
        recipe_block(
            title="P02-about-spread / v04 KEEP",
            unit="P02-about-spread",
            pages="p2|p3 · About + Dedication",
            version="v04",
            model=QWEN,
            resolution=size_of("Media/development/P02-about-spread/art.png"),
            seed="n/a",
            date="2026-07-22",
            status="keep",
            composition=(
                "Corner living room · fireplace L wall (About) · tree+door R wall (Dedication) · "
                "open burgundy for type · continuous across gutter."
            ),
            paths=[
                "Media/development/P02-about-spread/art.png",
                "Media/development/P02-about-spread/art-left.png",
                "Media/development/P02-about-spread/art-right.png",
            ],
            notes="SPLIT stepping-stone refs: mocks P02-fireplace/v01 + P03-tree/v01.",
        ),
    )
    write_meta(
        "P02-about-spread",
        {
            "unit": "P02-about-spread",
            "version": "v04",
            "status": "keep",
            "date": "2026-07-22",
            "model": QWEN,
            "resolution": size_of("Media/development/P02-about-spread/art.png"),
            "dimensions": {
                "art.png": dims("Media/development/P02-about-spread/art.png"),
                "art-left.png": dims("Media/development/P02-about-spread/art-left.png"),
                "art-right.png": dims("Media/development/P02-about-spread/art-right.png"),
            },
            "paths": {
                "master": "Media/development/P02-about-spread/art.png",
                "left": "Media/development/P02-about-spread/art-left.png",
                "right": "Media/development/P02-about-spread/art-right.png",
            },
            "pages": {"left": 2, "right": 3},
        },
    )

    # --- P34 ---
    write_recipe(
        "P34-padding",
        recipe_block(
            title="P34-padding / v01 working",
            unit="P34-padding",
            pages="p34 · Optional quiet ornament",
            version="v01",
            model=QWEN,
            resolution=size_of("Media/development/P34-padding/art.png"),
            seed="n/a",
            date="2026-07-23",
            status="working (optional — cut if trimming)",
            composition="Quiet ornament padding page · FRAME ON · Jon eye pending.",
            paths=["Media/development/P34-padding/art.png"],
        ),
    )
    write_meta(
        "P34-padding",
        {
            "unit": "P34-padding",
            "version": "v01",
            "status": "working",
            "date": "2026-07-23",
            "model": QWEN,
            "resolution": size_of("Media/development/P34-padding/art.png"),
            "dimensions": {"art.png": dims("Media/development/P34-padding/art.png")},
            "paths": {"art": "Media/development/P34-padding/art.png"},
            "page": 34,
            "optional": True,
        },
    )

    # --- P35 ---
    write_recipe(
        "P35-colophon",
        recipe_block(
            title="P35-colophon / v01 working",
            unit="P35-colophon",
            pages="p35 · Optional colophon",
            version="v01",
            model=QWEN,
            resolution=size_of("Media/development/P35-colophon/art.png"),
            seed="n/a",
            date="2026-07-23",
            status="working (optional)",
            composition="Open cream paper for tiny reprint / colophon note · Jon eye pending.",
            paths=["Media/development/P35-colophon/art.png"],
        ),
    )
    write_meta(
        "P35-colophon",
        {
            "unit": "P35-colophon",
            "version": "v01",
            "status": "working",
            "date": "2026-07-23",
            "model": QWEN,
            "resolution": size_of("Media/development/P35-colophon/art.png"),
            "dimensions": {"art.png": dims("Media/development/P35-colophon/art.png")},
            "paths": {"art": "Media/development/P35-colophon/art.png"},
            "page": 35,
            "optional": True,
        },
    )

    # --- P36 ---
    write_recipe(
        "P36-blank",
        recipe_block(
            title="P36-blank / v01 working",
            unit="P36-blank",
            pages="p36 · Final blank",
            version="v01",
            model="Pillow cream RGB(252, 246, 238)",
            resolution=size_of("Media/development/P36-blank/art.png"),
            seed="n/a",
            date="2026-07-23",
            status="working (optional printer-friendly even end)",
            composition="Solid cream blank page · no illustration.",
            paths=["Media/development/P36-blank/art.png"],
        ),
    )
    write_meta(
        "P36-blank",
        {
            "unit": "P36-blank",
            "version": "v01",
            "status": "working",
            "date": "2026-07-23",
            "model": "Pillow cream RGB(252,246,238)",
            "resolution": size_of("Media/development/P36-blank/art.png"),
            "dimensions": {"art.png": dims("Media/development/P36-blank/art.png")},
            "paths": {"art": "Media/development/P36-blank/art.png"},
            "page": 36,
            "optional": True,
        },
    )

    # --- P-author ---
    write_recipe(
        "P-author",
        recipe_block(
            title="P-author / closer-zoom FAVORITE",
            unit="P-author",
            pages="p31 · Author",
            version="closer-zoom-v02",
            model="locked portrait cover-fill + cream vignette (Pillow)",
            resolution=size_of("Media/development/P-author/art.png"),
            seed="n/a",
            date="2026-07-23",
            status="keep (FAVORITE)",
            composition=(
                "Jack Farrell portrait · page-fill closer zoom · thin cream FRAME ON. "
                "Source: Media/approved/characters/jack-farrell-portrait.png (untouched)."
            ),
            paths=[
                "Media/development/P-author/art.png",
                "Media/development/P-author/art-closer-zoom-LOCKED-favorite.png",
                "Media/approved/characters/jack-farrell-portrait.png",
            ],
            notes="Previous framed plate: art-PREV-framed-before-closer-zoom.png · v01-framed/RECIPE.md",
        ),
    )
    write_meta(
        "P-author",
        {
            "unit": "P-author",
            "version": "closer-zoom-v02",
            "status": "keep",
            "date": "2026-07-23",
            "model": "locked portrait + Pillow cream vignette",
            "resolution": size_of("Media/development/P-author/art.png"),
            "dimensions": {"art.png": dims("Media/development/P-author/art.png")},
            "paths": {
                "art": "Media/development/P-author/art.png",
                "favorite_lock": "Media/development/P-author/art-closer-zoom-LOCKED-favorite.png",
                "approved_source": "Media/approved/characters/jack-farrell-portrait.png",
            },
            "page": 31,
        },
    )

    # --- P-quiet-close ---
    write_recipe(
        "P-quiet-close",
        recipe_block(
            title="P-quiet-close / v02-upscale-framed",
            unit="P-quiet-close",
            pages="p32|p33 · Quiet Close",
            version="v02-upscale-framed",
            model="SeedVR + Pillow cream dissolve",
            resolution=size_of("Media/development/P-quiet-close/art-left.png"),
            seed="n/a",
            date="2026-07-23",
            status="working (Jon eye)",
            composition=(
                "LEFT (p32): quiet room / chair / fire / tree — InDesign: Merry Christmas. only. "
                "RIGHT (p33): mantel ornament — InDesign: May the magic… God bless. stays on S12 R."
            ),
            paths=[
                "Media/development/P-quiet-close/art-left.png",
                "Media/development/P-quiet-close/art-right.png",
                "Media/development/P-quiet-close/v02-upscale-framed/art-left.png",
                "Media/development/P-quiet-close/v02-upscale-framed/art-right.png",
            ],
            notes="Archive 1024 sources under _archive-1024-v01/.",
        ),
    )
    write_meta(
        "P-quiet-close",
        {
            "unit": "P-quiet-close",
            "version": "v02-upscale-framed",
            "status": "working",
            "date": "2026-07-23",
            "model": "SeedVR + Pillow cream dissolve",
            "resolution": size_of("Media/development/P-quiet-close/art-left.png"),
            "dimensions": {
                "art-left.png": dims("Media/development/P-quiet-close/art-left.png"),
                "art-right.png": dims("Media/development/P-quiet-close/art-right.png"),
            },
            "paths": {
                "left": "Media/development/P-quiet-close/art-left.png",
                "right": "Media/development/P-quiet-close/art-right.png",
            },
            "pages": {"left": 32, "right": 33},
            "text": {
                "p32": "Merry Christmas.",
                "p33": "May the magic of this night stay in your heart, long after the season has gone.",
            },
        },
    )

    # --- P-thank-you ---
    write_recipe(
        "P-thank-you",
        recipe_block(
            title="P-thank-you / lora-v03 KEEP",
            unit="P-thank-you",
            pages="p30 · Thank You",
            version="lora-v03",
            model="FLUX.2 LoRA",
            resolution=size_of("Media/development/P-thank-you/art.png"),
            seed="n/a",
            date="2026-07-22",
            status="keep",
            composition="Cream watercolor paper · soft warm edge vignette · open center for Thank You Draft A (InDesign).",
            paths=["Media/development/P-thank-you/art.png"],
            notes="PASS Phase-1 audit 2026-07-23 · no content regen.",
        ),
    )
    write_meta(
        "P-thank-you",
        {
            "unit": "P-thank-you",
            "version": "lora-v03",
            "status": "keep",
            "date": "2026-07-22",
            "model": "FLUX.2 LoRA",
            "resolution": size_of("Media/development/P-thank-you/art.png"),
            "dimensions": {"art.png": dims("Media/development/P-thank-you/art.png")},
            "paths": {"art": "Media/development/P-thank-you/art.png"},
            "page": 30,
        },
    )


def dedup_flow() -> None:
    root = json.loads(FLOW.read_text(encoding="utf-8"))
    before = len(root["plates"])
    # Drop merged p28/p29 duplicates (same art-left/art-right as p26/p27)
    root["plates"] = [p for p in root["plates"] if p.get("id") not in ("p28", "p29")]

    # Ensure one unique path plate for S12 art.png master + shorten notes
    has_master = any(
        (p.get("path") or "").replace("\\", "/") == "Media/development/S12-god-bless/art.png"
        for p in root["plates"]
    )
    for p in root["plates"]:
        if p.get("id") == "p26":
            p["notes"] = "S12 L · v22 working · Jon PS master next (9 deer + open coat)"
            p["caption"] = "p26 · S12 God Bless L · v22"
            p["unit"] = "S12-god-bless"
            p["path"] = "Media/development/S12-god-bless/art-left.png"
            p["development_path"] = "Media/development/S12-god-bless/art-left.png"
        if p.get("id") == "p27":
            p["notes"] = "S12 R · v22 working · North Star text pocket for God bless."
            p["caption"] = "p27 · S12 God Bless R · v22"
            p["unit"] = "S12-god-bless"
            p["path"] = "Media/development/S12-god-bless/art-right.png"
            p["development_path"] = "Media/development/S12-god-bless/art-right.png"
            p["gpt_pillar"] = True

    if not has_master:
        # Insert after p25 (before p26)
        idx = next((i for i, p in enumerate(root["plates"]) if p.get("id") == "p26"), len(root["plates"]))
        master = {
            "id": "s12",
            "page": "26|27",
            "beat": "S12 God Bless",
            "caption": "S12 · God Bless · v22 master art.png",
            "path": "Media/development/S12-god-bless/art.png",
            "version": "v22",
            "model": "fal-ai/qwen-image-2/pro/edit",
            "status": "working",
            "decided_by": "Jon",
            "date": "2026-07-23",
            "notes": "Seamless master 5250x2625 · triplet with art-left/art-right · Jon PS next",
            "gpt_pillar": True,
            "development_path": "Media/development/S12-god-bless/art.png",
            "tier": "development",
            "pixel_size": "5250x2625",
            "unit": "S12-god-bless",
            "layout": "text_image_defacto",
        }
        root["plates"].insert(idx, master)

    # Verdicts: drop merged 28|29; keep single 26|27
    new_verdicts = []
    for v in root.get("verdicts", []):
        page = str(v.get("page", ""))
        beat = str(v.get("beat", ""))
        if page in ("28|29", "28", "29") or "merged" in str(v.get("status", "")).lower() and "S12" in beat:
            continue
        if "S12b" in beat:
            continue
        if page == "26|27" or ("S12" in beat and "God Bless" in beat):
            v["page"] = "26|27"
            v["beat"] = "S12 God Bless"
            v["version"] = "v22"
            v["status"] = "working"
            v["notes"] = "p26|27 only · art.png + art-left + art-right · Jon PS master next"
            v["model"] = QWEN
            # avoid duplicate 26|27 verdicts
            if any(x.get("page") == "26|27" and x.get("beat") == "S12 God Bless" for x in new_verdicts):
                continue
        new_verdicts.append(v)
    root["verdicts"] = new_verdicts
    root["updated"] = DAY
    root["s12_note"] = (
        "S12 = p26|27 only. One plate per file: s12→art.png, p26→art-left, p27→art-right. "
        "Former p28|p29 merged pages removed from plates list."
    )

    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    after = len(root["plates"])
    text = FLOW.read_text(encoding="utf-8")
    print(f"FLOW plates {before} -> {after}; S12 string count {text.count('S12')}; god-bless {text.lower().count('god-bless')}")


def quality_target() -> None:
    src = DEV / "S03-eyes-met" / "art.png"
    dest_dir = DEV / "_quality-targets"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "S03-eyes-met-v07-quality-bar.jpg"
    im = Image.open(src).convert("RGB")
    im.save(dest, quality=95, optimize=True)
    # small pointer recipe
    (dest_dir / "README.md").write_text(
        """# Quality targets

| File | Role |
|------|------|
| `S03-eyes-met-v07-quality-bar.jpg` | **QUALITY BAR** for finals — copy of `S03-eyes-met/art.png` (v07 KEEP) |

Do not regenerate from this JPG; source of truth remains the PNG dashboard + FLOW.
""",
        encoding="utf-8",
    )
    print("quality target", dest.relative_to(ROOT), list(im.size))


def main() -> None:
    build_docs()
    dedup_flow()
    quality_target()
    # verify recipes exist
    units = [
        "S01-approach",
        "S02-threshold",
        "S03-eyes-met",
        "S04-sit-here",
        "S05-chat",
        "S06-cocoa",
        "Cover",
        "P01-title",
        "P02-about-spread",
        "P34-padding",
        "P35-colophon",
        "P36-blank",
        "P-author",
        "P-quiet-close",
        "P-thank-you",
    ]
    missing = []
    for u in units:
        if not (DEV / u / "RECIPE.md").is_file() or not (DEV / u / "meta.json").is_file():
            missing.append(u)
    # verify S12 path uniqueness
    flow = json.loads(FLOW.read_text(encoding="utf-8"))
    s12_paths = [
        (p["id"], p.get("path"))
        for p in flow["plates"]
        if "S12" in str(p.get("unit", "")) or "god-bless" in str(p.get("path", "")).lower() or p.get("id") in ("s12", "p26", "p27", "p28", "p29")
    ]
    print("S12 plates:", s12_paths)
    print("MISSING", missing or "none")
    print("DONE audit fix")


if __name__ == "__main__":
    main()
