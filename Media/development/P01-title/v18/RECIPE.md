# RECIPE — P01-title / v18

| Field | Value |
|-------|--------|
| **name** | Winter Window — complete pastel Christmas tree |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v18 |
| **date** | 2026-07-22 |
| **lane** | Qwen 2 Pro Edit scene + Pillow page lock (v16 geometry, wider plate) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · full tree priority · pastel/light watercolor · ~64% plate width |
| **FRAME** | ON — warm gold page margins (same as v16) |
| **source** | `Media/development/P01-title/v11/art.png` (DNA) · page lock from v16 |
| **size** | 2048² |
| **seed** | 120435498 |
| **request_id** | `019f8cca-78e2-73a3-b25f-33070b0409df` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **type** | NONE — open cream above/below for InDesign |
| **verdict** | pending |
| **status** | working |
| **tier** | development |
| **note** | Baked gibberish scrubbed → `art.png`; pre-scrub saved as `art-with-baked-text.png` |

## Change vs v16

Complete traditional Christmas tree fully visible (not cropped/faded). Pastel greens, warm golden lights, muted ornaments — soft luminous watercolor matching the window. Composition may shift slightly wider to fit.

## Prompt

Create a SINGLE square children's-book TITLE PAGE scene — ART ONLY, no text. Image 1 = soft watercolor/gouache paint STYLE (luminous, light, gentle). Image 2 = composition DNA to keep: winter WINDOW with cream curtains, full moon, falling snow, faint tiny Santa sleigh+reindeer silhouette on the moon, holly on sill, cream/ivory interior, soft FRAME ON into cream. PRIORITY CHANGE — the Christmas TREE on the RIGHT must be a COMPLETE traditional Christmas tree, FULLY VISIBLE inside the painted plate: full cone silhouette from tip to base, warm golden string lights, a few soft ornaments, wrapped presents clearly visible underneath. NOT cropped, NOT cut off at the edge, NOT fading/dissolving into the background, NOT a partial peek. If needed, shift the composition slightly WIDER so window + FULL tree both fit comfortably (window left-of-center, complete tree right). STYLE for the tree: soft watercolor/gouache, LIGHTER tones — pastel greens, warm golden lights, muted ornament colors. NOT dark, NOT heavily saturated, NOT muddy. Translucent gentle luminous watercolor that belongs in the same soft world as the window. Open soft cream around the vignette for title above / copyright below later. No people, no faces, no baked text.

## Negative

cropped tree, cut-off tree, partial tree, tree peek only, faded tree, dissolving tree, transparent ghost tree, dark saturated tree, muddy green, heavy opaque tree, neon ornaments, photorealistic, people, faces, hands, child, text, letters, blue wash behind art, hard black border

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v16-v18-board.png`
- Script: `scripts/_scratch/_p01_v18_full_pastel_tree.py`
