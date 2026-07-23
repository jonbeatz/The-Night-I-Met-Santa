# RECIPE — P01-title / v25

| Field | Value |
|-------|--------|
| **name** | Victorian house title vignette · lamppost + fence bows |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE (right-hand) |
| **page role** | single |
| **spread side** | n/a (right-hand open after burgundy pastedown) |
| **version** | v25 |
| **date** | 2026-07-22 |
| **lane** | A2 alt / mock favorite look (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · enable_prompt_expansion=false · 3 image_urls (cap) |
| **FRAME** | ON |
| **concept** | First visual when opening cover — framed Victorian house night scene; cream upper-center for live Cormorant title |
| **changes** | New concept dial from openbookFront Refs 1–3 + style-lock-v2 (not from v22–v24 fireplace/tree path) |
| **size** | 2048² dial |
| **seed** | 718915094 |
| **request_id** | `019f8c01-d5c6-7f71-9e69-b7db24f1f7b0` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | Title / author / copyright placed later in InDesign — art only |
| **type_zone** | Upper-center cream wash (title) · lower cream for author/copyright |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- boy: n/a
- santa: n/a
- jack: n/a
- style / frame:
  - image 1: `Media/approved/style-refs/style-lock-v2.png`
  - image 2: `Media/generated/Ai-Image-Tests/openbookFront-Ref2.jpg` (Victorian house focal)
  - image 3: `Media/generated/Ai-Image-Tests/openbookFront-Ref3.jpg` (circular vignette)
  - prompt-only (3-URL cap): `openbookFront-Ref1.jpg` lamppost + wreath/magical feeling
- base / edit source: multi-ref edit (no prior P01 art)

## Prompt

Using image 1 for watercolor/gouache paint style and warm golden lighting only. Using image 2 for the Victorian house subject: snowy roof, warm golden light glowing from every window, Christmas wreath on the front door, white picket fence across the bottom with a red bow accent. Using image 3 for the contained soft circular vignette composition — scene as a framed painting that feathers into cream/white paper at the edges. Add a decorative foreground lamppost with a festive red bow and holly (from the open-book lamppost refs). Snow-covered evergreens frame left and right. Soft falling snow. Dreamy winter sky: deep purple-blue at top with burgundy undertones in shadows (match image 1 wall atmosphere), warming to golden-peach near the horizon. Leave open cream space in the UPPER CENTER for title text later. Art only — no letters, no title, no copyright, no watermark, no people, no animals. FRAME ON: soft irregular watercolor vignette edge into cream.

## Negative / constraints

text, letters, typography, title, watermark, logo, signature, people, faces, animals, photorealistic, hard crop edge, full-bleed edge-to-edge with no cream margin, double house

## Gotchas

- Qwen Pro Edit allows **max 3** `image_urls` — Ref1 composition cues (lamppost, red bow, special-place feeling) are prompt-only; Ref2 + Ref3 + style-lock take the three slots.
- No baked text — title/copyright are InDesign live type.

## Notes

- Pull burgundy into house shadows + sky undertones to connect with S1 / style-lock-v2 walls.
- Next: Jon eye · if keep-leaning, Banana Pro finals pass optional.

## Related

- Prev: v22–v24 fireplace/tree title path
- Flow v2 P01 · casewrap pastedowns = solid burgundy (not this page)
- Script: `scripts/_scratch/_p01_v25_victorian_house.py`
