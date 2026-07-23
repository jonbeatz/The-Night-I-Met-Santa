# RECIPE — P01-title / v14

| Field | Value |
|-------|--------|
| **name** | Winter Window — tree restored · soft vertical rectangle |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v14 |
| **date** | 2026-07-22 |
| **lane** | A2 Qwen 2 Pro Edit |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · tree kept · vertical-rectangle plate · cool dissolve |
| **FRAME** | ON — soft rectangular watercolor edge (not blotch) |
| **source scene** | `Media/development/P01-title/v11/art.png` |
| **frame ref** | `Media/development/P01-title/v12/art.png` (glow/dissolve only) |
| **style** | `Media/approved/style-refs/style-lock-v2.png` |
| **size** | 2048² |
| **seed** | 304081763 |
| **request_id** | `019f8cac-812a-7633-b976-7dab3c4fb804` |
| **cost_note** | ~$0.08 |
| **output** | art.png (art-only for InDesign) |
| **type** | NONE — live Cormorant in InDesign |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Fixes vs v12

1. Christmas tree with warm lights restored on the right (from v11).
2. Overall plate shape = gentle vertical rectangle with organic soft edges — not amorphous blotch.

## Prompt

Create a SINGLE square children's-book TITLE PAGE painting — ART ONLY, no text. Image 1 = watercolor/gouache paint STYLE lock. Image 2 = COMPLETE SCENE to preserve (priority): winter WINDOW on the left/center AND Christmas TREE with warm lights and a few ornaments on the RIGHT side of the window — same as this reference. Also keep: full moon, faint tiny Santa sleigh+reindeer silhouette crossing the moon, falling snow, cream curtains tied back, optional holly on sill / presents. The tree is REQUIRED — do not crop it out, do not replace it with empty wash. Image 3 = QUIET FRAME treatment reference only (ignore its missing tree / blotchy outer shape): borrow only the soft off-white inner glow near the art and the cool winter-toned watercolor dissolve into cream paper — NOT a peachy blotch cloud. COMPOSITION SHAPE (critical): the overall art plate must read as a gentle VERTICAL RECTANGLE — taller than wide — a softly painted rectangular plate with organic irregular watercolor edges. NOT a random amorphous blotch, NOT a cloud, NOT a circle, NOT an oval splat. Window + tree form a natural vertical composition; the watercolor frame FOLLOWS that rectangular shape and bleeds softly into the cream page on all sides. Place the rectangular plate centered, upper-middle, about 60–70% of page width. Rich detailed art inside: window left/center, tree right, moon and sleigh above. Soft off-white/warm ivory inner glow around the scene; outward dissolve in cool soft winter tones into cream (pale blue-gray / cool ivory washes — quiet, not loud peach). Organic hand-painted soft edge = watercolor paint bleed only — NO bird feathers, NO plumes, NO hard border, NO geometric black frame, NO sticker cutout. Open luminous cream above and below for live title/copyright later. No people, no text.

## Negative

text, letters, typography, title, copyright, watermark, logo, missing Christmas tree, no tree, tree removed, empty right side, amorphous blotch, cloud shape, circular splat, oval blob, random wash blob, feathers, feather, plume, quill, feather wreath, hard border, black frame, geometric hard rectangle border, sticker cutout, loud peach blotch, neon wash, photorealistic, people, faces, hands, child

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v12-v14-board.png`
- Script: `scripts/_scratch/_p01_v14_tree_rect_plate.py`
