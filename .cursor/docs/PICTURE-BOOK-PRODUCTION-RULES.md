# Picture Book Production Rules — Locked Workflow

**Status:** LOCKED · **Date:** 2026-07-22 · **Applies to:** all Hermes children's picture-book projects  
**Canonical home:** `_core-scripts/shared-profile-content/docs/PICTURE-BOOK-PRODUCTION-RULES.md`  
**Project mirrors:** `.cursor/docs/PICTURE-BOOK-PRODUCTION-RULES.md` (via `npm run sync:docs -- -Write -AddMissing`)

> These rules keep model picks visual, book-order reviewable, and verdicts durable across sessions.

---

## 0. Current-plate pointer (required)

Every book project maintains:

```
Media/generated/mocks/_FLOW-CURRENT.json
```

Maps every page/beat → **path · version · model · status · decided_by · date · notes** (and `gpt_pillar` when used).  
**Flipbook reads this file only.** Agents must not guess “best” art from folder browsing.

---

## 1. Three-Panel Comparison Boards — one per decision

| Panel | Role |
|-------|------|
| **Left** | Klein 9B baseline (**always**) |
| **Center** | The new model being tested |
| **Right** | The current favorite / previous winner |

Label: model · version · cost · resolution · strengths.  
Save: `Media/generated/mocks/{unit}/_INDEX/{unit}-comparison-{YYYY-MM-DD}.png`

**Poem captions (LOCKED 2026-07-22):** every board must show Flow v2 script text under each side.

| Layout | Footer format |
|--------|----------------|
| LEFT/RIGHT spread or split | `LEFT pN — "poem…"` · `RIGHT pN — "poem…"` |
| Single page | `pN — "poem / title text…"` |
| TEXT + IMAGE | `LEFT pN — "poem…"` · `RIGHT pN — "poem…"` or `RIGHT pN — IMAGE — "context…"` when Flow says no text |

**Glanceable tech cue (LOCKED 2026-07-22):** one quiet line under the title — model · size · quality bar.  
Example: `Qwen 2 Pro /edit · 2048×1024 · S3 v07 quality bar`  
No seeds / request IDs on the board (those stay in RECIPE.md).

Poem source: `JON-BOOK-FLOW-v2-FINAL.md` via `scripts/book_poem_map.py`.  
Board helpers: `scripts/book_review_board.py` (`text_image_board` · `seamless_board` · `split_board` · `tech=`).  
Three-panel model tests: `scripts/book-comparison-board.py` (still add poem via `book_poem_map` when the unit is a story beat).

**Going forward:** one prompt → **one board** → one lock.  
Multi-round catch-up boards are **archive**, not active decision noise.

---

## 2. Full-Book Flipbook PDF

After every flow pass / batch:

```
npm run book:flipbook
# → Output/flipbook-{YYYY-MM-DD}.pdf
```

| Spec | Value |
|------|--------|
| Source | **`_FLOW-CURRENT.json` only** |
| Size | 8.5 × 8.5" · sRGB · full bleed · no crop marks |
| Cover | date · source · flow doc · models · plate count |
| Role | **Review only** — not the Lulu print PDF |

**Helper:** `scripts/book-flipbook-assemble.py`

---

## 3. Verdict Card

Last flipbook page. Statuses: `keep` · `keep-leaning` · `reject` · `locked`.

Every verdict **must** include:

- `decided_by` (usually `Jon`)
- `date` (`YYYY-MM-DD`) — required so August reopen is not mush

---

## 4. Hero spend (when using GPT Image 2 High 4K)

GPT High 4K (~$0.40) **only** for spreads Jon marks as pillars in the flow doc **and** `gpt_pillar: true` in `_FLOW-CURRENT.json`.  
**Default finals** = style-lock path (Krea/Qwen + style lock), not GPT.

---

## Always-open doc kit (per book)

Keep the always-open stack thin:

1. Flow / page map  
2. Master production dock (prompts)  
3. Image lane system  
4. Agent runbook (DTP / print)

Everything else = reference.

---

## Agent checklist

1. Plate or verdict changed? → update `_FLOW-CURRENT.json` (`decided_by` + `date`).  
2. Style/model decision? → **one** comparison board → lock.  
3. Flow pass / batch done? → `book:flipbook`.  
4. GPT run? → confirm `gpt_pillar` first.
