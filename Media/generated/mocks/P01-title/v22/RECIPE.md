# RECIPE — P01-title / v22

| Field | Value |
|-------|--------|
| **name** | Framed fireplace+tree · simpler · open top cream |
| **unit** | P01-title |
| **book page** | 1 · Title · SINGLE (right / front-matter) |
| **page role** | `single` |
| **spread side** | `n/a` |
| **version** | v22 |
| **date** | 2026-07-21 |
| **lane** | B finals |
| **service** | fal.ai |
| **model** | `fal-ai/gemini-3-pro-image-preview/edit` |
| **settings** | resolution **2K** · aspect `1:1` · `num_images` 1 · `limit_generations` true · `safety_tolerance` 4 · `output_format` png |
| **FRAME** | **ON** |
| **concept** | Reimagine styles2 title plate — softer vignette, simpler décor, empty top for typography, no hard ceiling |
| **changes** | vs styles2/p01-title: simpler ornaments/gifts · scene slightly lower · open cream TOP · no hard ceiling/crown molding · watercolor frame matching styles2 |
| **size** | 2K square (print remake → 2625² later if needed) |
| **seed** | **722101** |
| **request_id** | n/a (not captured at generate) |
| **cost_note** | ~Lane B edit |
| **output** | `art-P01-title-gemini-fal.png` *(one file only)* |
| **script_text** | Title: *The Night I Met Santa* · Author: *Jack Farrell* (live type — not baked into art) |
| **type_zone** | **Upper cream** open wash (not lower-center default) |
| **verdict** | **keep** — Jon lock |
| **status** | **locked-provisional** (2026-07-21; corrected from brief v21 mis-promote) |
| **promoted_to** | `Media/approved/pages/p01-title.png` |

## Character / style refs used

- boy: n/a (quiet title vignette — no child)
- santa: n/a
- jack: n/a
- style / frame:
  - `Images/styles2/p01-title.png` (base scene)
  - `Images/styles2/spread-Frame-Style1.png`
  - `Images/styles2/p21-beat12-13-note-LEFT.png`
  - `Media/approved/covers/cover-front.png` (paint quality)
- base / edit source: `Images/styles2/p01-title.png`

## Prompt

Reimagine this Christmas TITLE PAGE illustration.

KEEP the cozy mood: stone fireplace LEFT with stockings, decorated Christmas tree RIGHT,
warm heirloom gouache/watercolor storybook paint (match locked cover paint quality).

SIMPLIFY: fewer ornaments, fewer gifts (2–4 packages), less clutter on the mantel,
calmer room — still festive, not busy.

COMPOSITION:
- Move the WHOLE scene slightly DOWNWARD so the TOP has generous empty cream/soft wash
  space for later title typography.
- NO hard ceiling lines, NO crown molding, NO sharp architectural ceiling edge —
  soft blended watercolor wash into open paper at the top (no ruled room box).
- Soft night window / moon OK but keep it quiet.

WATERCOLOR FRAME ON: soft irregular white/cream watercolor paper vignette around the scene —
feathered painted edges bleeding into open paper, hand-painted storybook plate (not a hard
rectangle crop, not full-bleed edge-to-edge). Match styles2 frame refs (spread-Frame-Style1 / p21).

Traditional children's Christmas picture-book illustration, rich gouache and soft watercolor,
NOT colored pencil, Charles Santore–inspired, no people, no faces, no text, no letters,
no watermark. Square 1:1.

## Negative / constraints

- No people, no faces, no text, no letters, no glyphs, no watermark, no logos
- No hard ceiling line / crown molding / ruled room box
- Not full-bleed edge-to-edge (FRAME ON)
- Not colored pencil / crayon / flat cartoon
- Do not bake title typography into the PNG

## Gotchas

- Thin early RECIPE omitted Prompt — restored from `scripts/_scratch/_p01_v22_framed_simple.py`
- Do **not** mid-paint-crop this plate to “center” scenery (shears soft crown → hard top). See ISSUES-RESOLVED 2026-07-21
- Alts v23 (scene top) / v24 (centered) kept for reference — not locked

## Notes

- Jon favorite for P01 title art (provisional lock)
- MOCK/ID type: Cinzel Decorative **36/42** title · Cormorant **18/24** author · `#2C2C2C` · place in **upper cream**
- Next: place into `Xtraz/Adobe-Photoshop/p01-title.psd` ART when Jon says ready
- Print-res remake later if needed (`CONTINUITY-AND-PRINT-FINALS.md`) — still not “final”

## Related

- Scratch: `scripts/_scratch/_p01_v22_framed_simple.py`
- Approved: `Media/approved/pages/p01-title.png` + `p01-title.recipe.md`
- Prev dials: v21 (alt) · Template: `Media/generated/mocks/_RECIPE-TEMPLATE.md`
