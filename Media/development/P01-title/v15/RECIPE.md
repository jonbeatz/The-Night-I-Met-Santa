# RECIPE — P01-title / v15

| Field | Value |
|-------|--------|
| **name** | Winter Window — clean cream center + page-perimeter frame |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v15 |
| **date** | 2026-07-22 |
| **lane** | A2 Qwen 2 Pro Edit |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · clean cream behind art · cool perimeter frame only |
| **FRAME** | ON — page-edge watercolor border (~1–2 in), not background wash |
| **source** | `Media/development/P01-title/v14/art.png` |
| **style** | `Media/approved/style-refs/style-lock-v2.png` |
| **size** | 2048² |
| **seed** | 759917994 |
| **request_id** | `019f8cb0-40da-7253-9ab8-ef4a9364ce03` |
| **cost_note** | ~$0.08 |
| **output** | art.png (art-only for InDesign) |
| **type** | NONE — live Cormorant in InDesign |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Fixes vs v14

- REMOVE bluish/peach wash filling behind window+tree → clean cream paper.
- ADD soft cool watercolor frame only along page perimeter (decorative border).
- KEEP window + moon/snow/sleigh + tree + vertical rectangular scene plate.

## Prompt

Create a SINGLE square children's-book TITLE PAGE painting — ART ONLY, no text. Image 1 = watercolor/gouache paint STYLE lock. Image 2 = the SCENE to preserve: winter WINDOW (moon, snow, faint Santa sleigh silhouette) plus Christmas TREE with warm lights, ornaments, and presents on the RIGHT. Keep that vertical rectangular window+tree composition as the focal plate, centered upper-middle on the page (~60–70% width). Image 3 = LAYOUT GUIDE ONLY: clean cream open center + soft watercolor wash ONLY along the outer page perimeter (a quiet picture-frame border). Copy that STRUCTURE — do not copy any extra objects from image 3. CRITICAL LAYOUT: 1) Area BEHIND and AROUND the window+tree must be CLEAN CREAM PAPER — no bluish wash, no peachy glow, no colored background fill behind the art. The artwork floats on clean cream. 2) ADD a soft watercolor FRAME only along the EDGES / MARGINS of the entire page — like a decorative painted picture frame around the whole page. About 1–2 inches wide (roughly 8–15% of the page edge). The frame does NOT fill the background behind the window and tree. 3) Frame tones: very subtle quiet cool winter — soft gray-blue, pale silver, faintest winter green. Organic hand-painted soft edges bleeding into cream. Not loud, not dark, not peach. Window + tree centered on clean cream. Watercolor frame around page perimeter only. Nothing colored behind the art. No people, no baked text. Soft edge = watercolor bleed — NOT bird feathers.

## Negative

text, letters, typography, title, copyright, watermark, bluish wash behind art, blue background fill, peach glow behind art, colored wash under scene, full-page colored background, blotch behind window, cloud wash center, missing Christmas tree, no tree, feathers, feather, plume, hard black border, thick ornate baroque frame, photorealistic, people, faces, hands, child

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v14-v15-board.png`
- Script: `scripts/_scratch/_p01_v15_cream_perimeter_frame.py`
