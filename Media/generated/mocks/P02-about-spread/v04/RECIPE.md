# RECIPE — P02-about-spread / v04

| Field | Value |
|-------|--------|
| **name** | About + Dedication — LAST panorama · connect approved SPLIT plates |
| **unit** | P02-about-spread |
| **book page** | 2\|3 · About + Dedication · FULL SPREAD (attempt) |
| **page role** | spread |
| **spread side** | wide-master |
| **version** | v04 |
| **date** | 2026-07-22 |
| **lane** | Pillow connect prep → Qwen 2 Pro Edit |
| **service** | fal.ai + Pillow |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · refs: style-lock + widen prep + split collage |
| **FRAME** | ON |
| **concept** | One natural wide room from approved P02-fireplace/v01 + P03-tree/v01 · open center for text |
| **changes** | Last panorama try. If fail → lock SPLIT singles and abandon continuous About/Dedication art |
| **size** | 2048×1024 |
| **seed** | 956638903 |
| **request_id** | `019f8c33-a89b-7311-bdc4-917ae6467e89` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | About L-center · Dedication R-center |
| **type_zone** | Open burgundy near gutter on each half |
| **verdict** | keep — Jon LOCK 2026-07-22 (corner perspective) |
| **status** | locked-provisional |
| **promoted_to** | — (print promote later) |

## Refs

- `P02-fireplace/v01/art.png`
- `P03-tree/v01/art.png`
- `style-lock-v2.png`
- `_prep-connect-splits.png` · `_ref-split-collage.png`

## Prompt

Edit image 2 — KEEP this exact wide-room layout and full ceiling height. Image 1 = watercolor/gouache paint style only (style-lock). Image 3 = collage of the approved fireplace (left) and tree+door (right) for scene accuracy — match stockings, wreaths, presents, fire, door bow. ONE continuous living room at night: fireplace owns the LEFT page, Christmas tree + door own the RIGHT page. CENTER (page gutter): open soft burgundy wall + wooden floor + gentle golden firelight wash only — no furniture, no ornaments cluster, breathing room for About (left-center) and Dedication (right-center) text. Same burgundy walls, same warm golden light, same wood floor throughout. Ceiling and upper walls visible. Seamless — no gutter seam, no page fold, no hard join. Soft feathered vignette (FRAME ON). Art only — no letters, no title, no watermark, no people.

## Negative

text, letters, typography, watermark, people, gutter line, page fold, hard seam, duplicate fireplace, duplicate tree, busy center wall, furniture in middle, squished to bottom, cream top third only, pale walls

## Notes

- Jon: if this fails, lock SPLIT and move on.
- Script: `scripts/_scratch/_p02_about_spread_v04_connect_splits.py`
