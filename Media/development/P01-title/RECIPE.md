# RECIPE — P01-title / v25 KEEP @2625

| Field | Value |
|-------|--------|
| **name** | Winter Window — centered · full-bleed burgundy · tree right |
| **unit** | P01-title |
| **book page** | **1** · Title + Copyright · **RIGHT page of opening spread** (left = endpaper cream) |
| **page role** | `single` · opens book on **recto / page 1** |
| **version locked** | **v25** |
| **date** | 2026-07-28 |
| **lane** | Qwen 2 Pro Edit (mock/development) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **FRAME** | **OFF** — full-bleed burgundy `#4A0E17` to edges |
| **resolution** | **art.png 2625×2625** (LANCZOS from v25 2048; SeedVR optional later) |
| **seed** | 1723090123 |
| **status** | **keep** · tier **development** |
| **dashboard** | `Media/development/P01-title/` |
| **script_text** | *The Night I Met Santa* · Written by Jack Farrell · First illustrated edition, 2026 · Book design by Jon Farrell (**live InDesign** — not baked in art) |
| **type_zone** | Title/author on burgundy — light ink / live type in InDesign (no cream mat) |
| **source** | `Media/development/P01-title/v25/art.png` |
| **supersedes** | **v16** KEEP (cream walls + gold page frame) — backed up as `art-v16-keep-backup.png` |

## Book opening map (critical)

| Spread half | Content |
|-------------|---------|
| **LEFT** (verso / inside front endpaper) | Blank cream `#FDFBF7` — not this art |
| **RIGHT** (recto / **page 1**) | This plate — title art |

PSD: `Xtraz/Adobe-Photoshop/text-layout-master.psd` group **P01** · plate `_plates/P01.png` places art on **x=2625** (right half).

## Composition notes

Full-bleed house burgundy walls · winter window **centered** · Christmas tree + gifts to the **right** (right-edge crop OK) · moon/snow/sleigh in glass · holly on sill. Lineage: v23 burgundy+full tree → v24 no cream frame → **v25** centered window.

## Art file paths

- `Media/development/P01-title/art.png` — **2625²** current dashboard (**v25**)
- `Media/development/P01-title/art-2625.png` — same
- `Media/development/P01-title/v25/art.png` — locked version source (2048)
- `Media/development/P01-title/art-v16-keep-backup.png` — previous KEEP

## Notes

- Jon KEEP 2026-07-28.
- Do **not** promote to `Media/approved/` (characters + style-lock only).
- FLOW: `p01` → v25 keep · page **"1"**.
- Poem/copy: `scripts/book_poem_map.py` → `P01-title` · `page: 1`.
