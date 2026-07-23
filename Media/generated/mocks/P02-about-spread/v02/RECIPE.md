# RECIPE — P02-about-spread / v02

| Field | Value |
|-------|--------|
| **name** | About + Dedication — pushed down · top cream text wash |
| **unit** | P02-about-spread |
| **book page** | 2\|3 · About + Dedication · FULL SPREAD |
| **page role** | spread |
| **version** | v02 |
| **date** | 2026-07-22 |
| **lane** | Pillow prep (push-down) → Qwen 2 Pro Edit polish |
| **service** | fal.ai + Pillow |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · scene in lower 68% · ~32% top cream · polish from prep |
| **FRAME** | ON |
| **concept** | Same v01 scene; top third open for About (L) / Dedication (R) text clouds |
| **changes** | vs v01: composition lower · burgundy fades to cream · glow may rise into wash |
| **seed** | 578599107 |
| **request_id** | `019f8c22-f3b6-7e41-b39b-f37004a04529` |
| **cost_note** | ~$0.08 polish (+ earlier failed fal-only attempt) |
| **output** | art.png |
| **type_zone** | Top ~1/3 cream wash across spread |
| **verdict** | pending |
| **status** | working |

## Refs

- style-lock-v2
- base: `../v01/art.png`
- prep: `_prep-push-down.png`
- failed fal-only: `art-fal-first-pass.png`

## Prompt (polish)

Edit image 2 — KEEP this exact camera and layout: large soft cream/ivory watercolor wash across the TOP THIRD for text; living room occupies only the BOTTOM two-thirds. Image 1 = paint style only. Preserve fireplace LEFT, tree center-right, presents, door with wreath RIGHT, burgundy walls below, golden firelight. Blend the upper fade so burgundy dissolves into cream; soft warm glow may rise into the wash. FRAME ON soft vignette. No text, no letters, no people. Do NOT stretch the room back to the top.

## Negative

text, letters, watermark, people, gutter, room filling full height, chimney at top edge, tree touching top, no cream band

## Gotchas

- Pure Qwen recompose from v01 did not open the top; Pillow forced layout first.
