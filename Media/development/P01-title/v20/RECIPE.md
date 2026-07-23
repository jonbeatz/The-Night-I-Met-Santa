# RECIPE — P01-title / v20

| Field | Value |
|-------|--------|
| **name** | Complete tree tip-to-base (star visible) |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v20 |
| **date** | 2026-07-22 |
| **lane** | Qwen 2 Pro Edit (treetop fix on v19) + Pillow page lock |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · full tree tip-to-base · rich colors · ~66% plate |
| **FRAME** | ON — warm gold page margins |
| **source** | `Media/development/P01-title/v19/art-scene.png` |
| **size** | 2048² |
| **seed** | 894831175 |
| **request_id** | `019f8cd7-eb85-7982-8409-d5fd3e80b8d6` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **type** | NONE |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Fix vs v19

Treetop / star-topper and uppermost branches fully visible with margin above. Presents still complete at base. Nothing cropped top or bottom.

## Prompt

Edit image 2 ONLY — almost everything is LOCKED. Image 1 = watercolor/gouache paint style. Image 2 is the title-page scene to preserve: rich deep-green Christmas TREE on the RIGHT with warm golden lights, red and gold ornaments, wrapped presents at the base; winter WINDOW on the LEFT with moon, falling snow, faint Santa sleigh silhouette, cream curtains, holly on sill; cream interior; soft vignette to cream. ONE FIX ONLY: the TREETOP is slightly cut off — make the Christmas tree COMPLETE from the VERY TOP to the presents at the base. The star or tree-topper and uppermost branches must be FULLY VISIBLE with a small margin of open cream/space ABOVE the treetop. Nothing cropped at the top. Nothing cropped at the bottom (presents fully visible). If needed, shift or scale the composition slightly taller / pull the camera back a touch so the entire tree fits inside the painted plate with breathing room above the tip. Keep rich traditional colors (deep greens, warm golds, soft reds) — NOT pastel. Do NOT change the window, moon, sleigh, presents richness, or overall layout otherwise. No people, no baked text.

## Negative

cropped treetop, cut-off star, missing topper, truncated tree tip, tree tip off-frame, cropped presents, faded tree, pastel tree, washed out, text, letters, people, faces, hands, photorealistic, blue wash behind art

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v19-v20-board.png`
- Script: `scripts/_scratch/_p01_v20_complete_treetop.py`
