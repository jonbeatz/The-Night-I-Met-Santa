# RECIPE — P01-title / v02

| Field | Value |
|-------|--------|
| **name** | Snowman lantern circular vignette |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE (right-hand) |
| **page role** | single |
| **spread side** | n/a |
| **version** | v02 |
| **date** | 2026-07-22 |
| **lane** | A2 mock favorite (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · enable_prompt_expansion=false · 2 refs only (no blend of concept refs) |
| **FRAME** | ON |
| **concept** | One-ref reimagine — do not blend other openbook refs |
| **changes** | Openbook concept dial set (archived prior v02 → `_archive-pre-openbook-concepts/`) |
| **size** | 2048² |
| **seed** | 38708630 |
| **request_id** | `019f8c08-a3cd-79d0-a684-3762ba384384` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | InDesign later — art only |
| **type_zone** | Cream open area for title (wreath interior / upper sky / top-center) |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- boy: n/a
- santa: n/a (optional distant sleigh silhouette on v01 only)
- jack: n/a
- style / frame:
  - image 1: `Media/approved/style-refs/style-lock-v2.png` (https://v3b.fal.media/files/b/0aa3543e/R4egMO-9QOZI_pWW1DlmI_style-lock-v2.png)
  - image 2: `openbookFront-Ref3.jpg (user Image 2 — snowman)` (https://v3b.fal.media/files/b/0aa35430/cAj4YSMmHEsI3CGUBNrUm_openbookFront-Ref3.jpg)
- base / edit source: single-concept reimagine (not blended with sibling refs)

## Prompt

Reimagine ONLY image 2 as a children's book title-page painting. Use image 1 solely for watercolor/gouache paint style, warm golden light, and burgundy in deep shadows. KEY idea: contained soft CIRCULAR vignette — intimate winter night scene. Center: cheerful snowman with black top hat (holly), striped scarf, stick arms, glowing lantern as the warm golden focal light. Snow-covered evergreens flank left and right. Full moon and soft starry night sky. Snowman + lantern light are the clear focus. Feathered circular wash fading to cream paper (FRAME ON). Art only — no letters, no title, no copyright, no watermark, no people.

## Negative / constraints

text, letters, typography, title, watermark, logo, signature, people, faces, photorealistic, hard crop, full-bleed with no cream margin, baked words

## Gotchas

- Do **not** attach sibling openbook refs — one concept image only + style-lock.
- Filename vs user Image #: Ref2→v01 wreath · Ref3→v02 snowman · Ref1→v03 landscape.

## Notes

- Comparison board: `Media/generated/mocks/_INDEX/P01-title-openbook-v01-v03-board.png`

## Related

- Script: `scripts/_scratch/_p01_openbook_v01_v03.py`
- Sibling dials: P01-title v01 / v02 / v03 (this set)
