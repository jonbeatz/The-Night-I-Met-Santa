# RECIPE — P01-title / v01

| Field | Value |
|-------|--------|
| **name** | Wreath-framed title page reimagine |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE (right-hand) |
| **page role** | single |
| **spread side** | n/a |
| **version** | v01 |
| **date** | 2026-07-22 |
| **lane** | A2 mock favorite (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · enable_prompt_expansion=false · 2 refs only (no blend of concept refs) |
| **FRAME** | ON |
| **concept** | One-ref reimagine — do not blend other openbook refs |
| **changes** | Openbook concept dial set (archived prior v01 → `_archive-pre-openbook-concepts/`) |
| **size** | 2048² |
| **seed** | 773229463 |
| **request_id** | `019f8c08-9ed3-74a0-8c87-493b4e3a3bcf` |
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
  - image 2: `openbookFront-Ref2.jpg (user Image 1 — wreath/title)` (https://v3b.fal.media/files/b/0aa35430/WQYKVwnQrnKqNzRrV8mM3_openbookFront-Ref2.jpg)
- base / edit source: single-concept reimagine (not blended with sibling refs)

## Prompt

Reimagine ONLY image 2 as a children's book title-page painting. Use image 1 solely for watercolor/gouache paint style, warm golden light, and burgundy shadow undertones. KEY idea: a large decorative Christmas wreath (evergreen, holly, red berries, soft red ribbon) frames the CENTER of the page — open cream space INSIDE the wreath for title text later. Behind/through the wreath: soft snowy village or winter landscape with warm window lights. Keep a decorative lamppost with a festive red bow in the foreground. Optional tiny Santa sleigh silhouette in the distant glow — no detail. Soft feathered watercolor vignette into cream paper (FRAME ON). Art only — no letters, no title, no copyright, no watermark, no people.

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


## Text scrub (pass 2)

| Field | Value |
|-------|--------|
| **why** | First bake baked title into wreath center |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **seed** | 871000635 |
| **request_id** | `019f8c0a-b446-7b93-9097-d25b80b37a4a` |
| **kept** | `art-with-baked-text.png` (pre-scrub) |
| **output** | `art.png` (no text) |

### Scrub prompt

Edit image 2 only: remove ALL text, letters, titles, typography, and signatures completely. Leave open soft cream watercolor space in the center of the wreath where the title was — ready for live type later. Keep the wreath, village glow, lamppost with red bow, optional sleigh silhouette, soft feathered vignette, and watercolor/gouache style from image 1. Do not add new objects. Art only — no letters anywhere.
