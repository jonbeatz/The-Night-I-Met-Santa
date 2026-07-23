# RECIPE — P01-title / v03

| Field | Value |
|-------|--------|
| **name** | Quiet watercolor winter landscape |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE (right-hand) |
| **page role** | single |
| **spread side** | n/a |
| **version** | v03 |
| **date** | 2026-07-22 |
| **lane** | A2 mock favorite (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · enable_prompt_expansion=false · 2 refs only (no blend of concept refs) |
| **FRAME** | ON |
| **concept** | One-ref reimagine — do not blend other openbook refs |
| **changes** | Openbook concept dial set (archived prior v03 → `_archive-pre-openbook-concepts/`) |
| **size** | 2048² |
| **seed** | 34022363 |
| **request_id** | `019f8c08-a88c-7ae2-b27f-fece012f0a07` |
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
  - image 2: `openbookFront-Ref1.jpg (user Image 3 — landscape)` (https://v3b.fal.media/files/b/0aa35430/Zb-K6llGBlnm6NyfNG7Gm_openbookFront-Ref1.jpg)
- base / edit source: single-concept reimagine (not blended with sibling refs)

## Prompt

Reimagine ONLY image 2 as a children's book title-page painting. Use image 1 solely for watercolor/gouache paint style and burgundy undertones in distant shadows. KEY idea: peaceful quiet winter landscape — mood over decoration. Snow-covered evergreens, white picket fence with ONE red bow accent (only bright color pop), soft winter sky peach-to-lavender. Large open cream space across TOP and CENTER for title. Visible brushstrokes, soft feathered vignette edges into cream (FRAME ON). No lamppost clutter, no wreath, no snowman, no sleigh, no village. Art only — no letters, no title, no copyright, no watermark, no people.

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
