# RECIPE — P02-fireplace / v01

| Field | Value |
|-------|--------|
| **name** | About — hearth single (SPLIT L) |
| **unit** | P02-fireplace |
| **book page** | 2 · About This Story · SINGLE LEFT |
| **page role** | single |
| **spread side** | left |
| **version** | v01 |
| **date** | 2026-07-22 |
| **lane** | A2 mock favorite (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · refs: style-lock-v2 + crop from P02-about-spread/v01 |
| **FRAME** | ON |
| **concept** | SPLIT layout pivot — same room as partner page, separate composition (like S1 Approach) |
| **changes** | Replaces failed continuous About/Dedication panorama (P02-about-spread v01–v03) |
| **size** | 2048² dial |
| **seed** | 1917477456 |
| **request_id** | `019f8c2d-01ec-79e0-8ac0-1bfe41d9d330` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | About This Story — InDesign later |
| **type_zone** | Open burgundy wall (right of fireplace / upper soft wall) for About text cloud |
| **verdict** | keep — stepping stone for About/Dedication v04 corner spread |
| **status** | keep |
| **promoted_to** | — (identity ref for `P02-about-spread/v04`) |

## Character / style refs used

- style: `Media/approved/style-refs/style-lock-v2.png`
- identity crop: `_ref-crop.png` from `Media/generated/mocks/P02-about-spread/v01/art.png`
- partner: P03-tree/v01

## Prompt

Create a SINGLE square children's-book page painting (not a half-spread). Image 1 = watercolor/gouache style, burgundy walls, warm golden light. Image 2 = fireplace identity — remake as a full standalone page. Stone fireplace with crackling fire, green garland on mantel, three stockings, wreath on the chimney. Deep burgundy wall behind with generous open soft wall space for About text (keep some quiet wall — do not fill the frame with stone). Warm golden firelight casting soft shadows. Wooden floor visible. Soft feathered watercolor vignette into cream (FRAME ON). Art only — no letters, no title, no watermark, no people, no Christmas tree, no door.

## Negative / constraints

text, letters, typography, watermark, logo, people, faces, panorama, double page, gutter line, half-spread crop, photorealistic, pale cream walls, white walls

## Notes

- Jon pivot 2026-07-22: continuous fireplace+tree spread failed (dense / squished / stretched). SPLIT like S1.
- Continuity: same burgundy walls, golden light, wooden floor language across both singles.

## Related

- Board: `Media/generated/mocks/_INDEX/P02-P03-split-hearth-tree-board.png`
- Script: `scripts/_scratch/_p02_p03_split_hearth_tree.py`
