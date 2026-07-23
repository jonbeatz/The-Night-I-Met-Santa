# RECIPE — P02-about-spread / v03

| Field | Value |
|-------|--------|
| **name** | About + Dedication — wide L/R · open center text wall |
| **unit** | P02-about-spread |
| **book page** | 2\|3 · About + Dedication · FULL SPREAD |
| **page role** | spread |
| **spread side** | wide-master |
| **version** | v03 |
| **date** | 2026-07-22 |
| **lane** | Pillow widen prep → Qwen 2 Pro Edit polish |
| **service** | fal.ai + Pillow |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · refs: style-lock + widen prep + v01 identity |
| **FRAME** | ON |
| **concept** | Full room height; fireplace owns left third; tree+door own right third; soft burgundy center for text |
| **changes** | vs v02: **not** push-down / cream top. vs v01: recompose wider with open gutter wall |
| **size** | 2048×1024 dial |
| **seed** | 956237476 |
| **request_id** | `019f8c28-3bf0-71a3-8ba2-af0efcfaff91` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | About (L-center) · Dedication (R-center) — InDesign later |
| **type_zone** | Soft burgundy wall near spread center on each page half |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- image 1: `Media/approved/style-refs/style-lock-v2.png`
- image 2: `_prep-widen-center.png` (this folder) — forced L/R geometry
- image 3: `../v01/art.png` — keep scene detail
- base: v01 (not v02 squish)

## Prompt

Image 1 = paint style. Image 2 = LAYOUT to keep… Image 3 = detail identity…

Edit image 2 — KEEP this exact wide layout and full room height. Image 1 = watercolor/gouache style only. LEFT third: stone fireplace with green garland, stockings, fire — owns the left page. RIGHT third: Christmas tree with warm lights + presents + wooden door with wreath — owns the right page. CENTER (where pages meet): open soft burgundy wall with gentle golden firelight glow only — NO furniture, NO ornaments cluster, NO dense detail — breathing room for text clouds (About on left-center, Dedication on right-center). Ceiling and upper walls stay visible — full room, not cropped or squished down. Deep burgundy walls, wooden floor continuous across the spread, soft feathered vignette (FRAME ON). Unify seams so it reads as one seamless living room. Art only — no letters, no title, no watermark, no people.

## Negative / constraints

text, letters, typography, watermark, people, gutter line, page fold, scene pushed to bottom, cream top third wash, squished room, fireplace in center, tree in center, busy middle wall, dense detail at gutter

## Gotchas

- v02 push-down felt too squished — Jon rejected that text strategy.
- Geometry-first again (Pillow widen) so Qwen doesn’t ignore the open center.

## Related

- Script: `scripts/_scratch/_p02_about_spread_v03.py`
