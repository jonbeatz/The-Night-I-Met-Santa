# RECIPE.md — standard template (LOCKED 2026-07-21)

**Copy this file into every** `Media/generated/mocks/{unit}/vNN/RECIPE.md`  
**Canonical also:** `.cursor/docs/PAGE-BUILD-WORKFLOW.md` §6

**Rules**
- One image file per `vNN/` (+ this RECIPE). No twin `art.png` + dial name.
- Fill **every** table row — use `n/a` or `—` when unknown (never omit the row).
- **Prompt is mandatory** — paste the full prompt / edit brief used. If reconstructed later, mark `(reconstructed)`.
- Record **FRAME ON/OFF**, lane **A1 / A2 / B**, exact model id, seed, refs.
- On promote: copy/adapt into `Media/approved/.../{name}.recipe.md` and set `promoted_to` + `status`.

---

```markdown
# RECIPE — {unit} / v{NN}

| Field | Value |
|-------|--------|
| **name** | Short human label (e.g. framed fireplace+tree · open top) |
| **unit** | P01-title / P03-dedication / S01-sneak / … |
| **book page** | N · Title / Dedication / Beat-XX · SINGLE or SPREAD |
| **page role** | `single` \| `spread` |
| **spread side** | `n/a` \| `left` \| `right` \| `wide-master` |
| **version** | vNN |
| **date** | YYYY-MM-DD |
| **lane** | A1 dial (Klein 9B) \| A2 alt (Qwen) \| A3 light (Klein 4B) \| B finals \| local composite |
| **service** | fal.ai \| OpenRouter \| Pillow \| Photoshop \| … |
| **model** | exact id (e.g. `fal-ai/gemini-3-pro-image-preview/edit`) |
| **settings** | res · aspect · steps · safety · limit_generations · other knobs |
| **FRAME** | ON \| OFF |
| **concept** | One-line intent (what this version is testing) |
| **changes** | vs previous version / vs base ref (bullets OK in Notes) |
| **size** | e.g. 1024² dial · 2K · 2625² print target |
| **seed** | number or n/a |
| **request_id** | provider job id or n/a |
| **cost_note** | optional ~$ or elapsed |
| **output** | exact filename in this folder (one file only) |
| **script_text** | Poem / title / dedication lines for this page — or n/a |
| **type_zone** | Where MOCK/live type sits (e.g. upper cream · lower-center SAFETY) |
| **verdict** | pending \| keep \| maybe \| reject \| locked-provisional |
| **status** | working \| locked-provisional \| superseded |
| **promoted_to** | `Media/approved/…` path or — |

## Character / style refs used

- boy: path or n/a
- santa: path or n/a
- jack: path or n/a
- style / frame: paths (styles2, cover, beat refs…)
- base / edit source: path if image-to-image

## Prompt

(paste FULL prompt or edit brief — do not summarize away)

## Negative / constraints

- No people / no text / no watermark / …
- Spread: no fake gutter / fold line / …
- Other hard negatives

## Gotchas

- Provider quirks, moderation, crop traps, twin-file mistakes, etc.

## Notes

- What worked · what to try next · PSD/ID follow-ups

## Related

- Prev/next versions · approved lock · scratch script path
```

### Approved sidecar (`*.recipe.md`)

Same fields when practical; minimum must include: `approved_file`, `source` (mock path), `status`, `model`, `seed`, `FRAME`, **Prompt** (or clear link: “full prompt in mocks/…/RECIPE.md”), `promoted` date, `type_zone`, `script_text` if any.
