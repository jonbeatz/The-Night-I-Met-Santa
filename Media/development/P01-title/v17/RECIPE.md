# RECIPE — P01-title / v17

| Field | Value |
|-------|--------|
| **name** | Winter Window — full tree (no dissolve) |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v17 |
| **date** | 2026-07-22 |
| **lane** | Qwen 2 Pro Edit (tree complete) · v16 layout lock |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · same page frame as v16 · tree fully opaque |
| **FRAME** | ON — warm gold page margins (unchanged from v16) |
| **source** | `Media/development/P01-title/v16/art.png` |
| **size** | 2048² |
| **seed** | 1489470457 |
| **request_id** | `019f8cc7-107c-7b40-bff6-dad566bafa32` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **type** | NONE — open cream above/below for InDesign |
| **verdict** | pending |
| **status** | working |
| **tier** | development |
| **note** | Qwen completed tree on v11 plate → Pillow recompose (v16 page geometry + gold margins, right-opaque vignette) |

## Change vs v16

Christmas tree + presents on the right fully rendered — no fading / soft dissolve into cream. Everything else identical.

## Prompt

Edit image 2 ONLY — almost everything is LOCKED. Image 1 = watercolor/gouache paint style. Image 2 is the title page to preserve: warm gold watercolor whisper on the OUTER PAGE edges only, clean cream center, winter WINDOW with moon / falling snow / faint Santa sleigh silhouette, cream curtains, holly on sill, open cream above and below for text. ONE CHANGE ONLY: the Christmas TREE on the RIGHT must be FULLY rendered — complete evergreen, all warm lights lit and clear, all ornaments visible and solid, all wrapped presents underneath clearly visible and opaque. NO fading, NO soft dissolve, NO transparent edges on the tree or presents — they must be as solid, detailed, and present as the window itself. The soft cream paper can meet the finished tree edge cleanly, but the tree itself must not ghost away. Do NOT change the window, moon, sleigh, gold page-edge frame, cream fields, or layout. Do NOT add people, blue wash, or text. Art only.

## Negative

faded tree, dissolving tree, transparent tree, ghost tree, soft-edge tree wash-out, missing presents, incomplete ornaments, missing lights, blue frame, wash behind art, people, faces, hands, text, letters, different window, moved layout, new scene, santa indoors

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v16-v17-board.png`
- Script: `scripts/_scratch/_p01_v17_full_tree.py`
