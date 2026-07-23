# RECIPE — P01-title / v16

| Field | Value |
|-------|--------|
| **name** | Winter Window — clean cream + warm gold PAGE-edge frame |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | v16 |
| **date** | 2026-07-22 |
| **lane** | Pillow structure lock + Qwen 2 Pro Edit polish |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · cream center · warm gold page-perimeter only |
| **FRAME** | ON — page margins (~1″), NOT around art vignette |
| **source scene** | `Media/development/P01-title/v11/art.png` |
| **compare** | v15 framed the art; v16 frames the page |
| **size** | 2048² |
| **seed** | 1271918122 |
| **request_id** | `019f8cbd-b30c-79c2-868b-ec14f2dc6c07` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **type** | NONE — open cream above/below for InDesign |
| **verdict** | **keep** |
| **status** | **keep** |
| **tier** | development |
| **note** | Jon KEEP 2026-07-22 — dashboard copy at `Media/development/P01-title/art.png`. Qwen polish replaced scene → Pillow page-structure lock is the plate. |

## Prompt

Edit image 2 ONLY — the LAYOUT is LOCKED and already correct. Image 1 = paint style. Image 2 structure (do not change): (1) Winter WINDOW + Christmas TREE vignette floating on CLEAN CREAM in the upper-middle. (2) Wide open CLEAN CREAM above the window for a title and below the tree for copyright. (3) A barely-there WARM GOLD / soft amber watercolor whisper ONLY on the outermost PAGE margins (top, bottom, left, right edges of the full square page) — like a soft picture-frame border for the whole 8.5x8.5 page. The gold must stay at the extreme outer edges and must NOT form a second frame around the window+tree. YOUR JOB: only soften the outer-edge gold so it looks like quiet hand-painted watercolor bleeding into cream (fireplace / tree-light warmth). Keep it extremely subtle. FORBIDDEN: blue frame, cool wash, any colored wash behind or around the art vignette, moving gold inward into the title/copyright cream fields, hard borders, text, people.

## Negative

blue frame, cool gray frame, wash behind window, wash behind tree, frame around art vignette, halo around window, colored background under scene, loud gold, thick ornate frame, hard border, text, letters, people

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v15-v16-board.png`
- Script: `scripts/_scratch/_p01_v16_page_gold_frame.py`
