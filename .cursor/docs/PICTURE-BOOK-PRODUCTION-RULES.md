# Picture Book Production Rules — Locked Workflow

**Status:** LOCKED · **Date:** 2026-07-23 · **Applies to:** all Hermes children's picture-book projects  
**Canonical home:** `_core-scripts/shared-profile-content/docs/PICTURE-BOOK-PRODUCTION-RULES.md`  
**Project mirrors:** `.cursor/docs/PICTURE-BOOK-PRODUCTION-RULES.md` (via `npm run sync:docs -- -Write -AddMissing`)

> These rules keep model picks visual, book-order reviewable, and verdicts durable across sessions.  
> **2026-07-23:** Added §5 FINALS-CHECKLIST gate + matter audit-first / multi-count / closing-copy rules.

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

**Poem captions (LOCKED 2026-07-22):** every board must show Flow script text under each side.

| Layout | Footer format |
|--------|----------------|
| LEFT/RIGHT spread or split | `LEFT pN — "poem…"` · `RIGHT pN — "poem…"` |
| Single page | `pN — "poem / title text…"` |
| TEXT + IMAGE | `LEFT pN — "poem…"` · `RIGHT pN — "poem…"` or `RIGHT pN — IMAGE — "context…"` when Flow says no text |

**Glanceable tech cue (LOCKED 2026-07-22):** one quiet line under the title — model · size · quality bar.  
Example: `Qwen 2 Pro /edit · 2048×1024 · S3 v07 quality bar`  
No seeds / request IDs on the board (those stay in RECIPE.md).

Poem source: project Flow doc via `scripts/book_poem_map.py`.  
Board helpers: `scripts/book_review_board.py` (`text_image_board` · `seamless_board` · `split_board` · `tech=`).  
Three-panel model tests: `scripts/book-comparison-board.py --unit <beat>` (adds poem strip).

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
5. Before Banana / InDesign batch? → run **FINALS-CHECKLIST** (RES · TRIPLET · FRAME · wardrobe · face · gutter · baked text · poem).  
6. Matter pages wrong size/frame only? → **audit-first** (frame/upscale) — don’t regen content by default.  
7. Multi-count subjects collapsing? → bake count into canvas first; stop dial burns after 2 fails → PS or finals model.

---

## 5. Pre-finals quality gate (2026-07-23)

Every book keeps a **`FINALS-CHECKLIST.md`** (copy pattern from TNIMS). Grade plates **HIGH / MED / LOW** before spending Banana or assembling print.

| Check | Meaning |
|-------|---------|
| **RES** | Singles 2625² · spreads 5250×2625 + L/R 2625² |
| **TRIP** | Seamless units always have `art.png` + `art-left` + `art-right` |
| **FRAME** | Singles/text FRAME ON · story-spread cream frames = **finals only** |
| **COAT / wardrobe** | Match G0 refs (written lock must equal pixels) |
| **FACE** | Character drift vs G0 |
| **GUTTER** | No baked fold · faces off bisect |
| **TEXT** | No baked letters |
| **POEM** | Matches `book_poem_map` / Flow |

**Closing copy:** poem blessing / last story line lives on the **story closing** text pocket — do not duplicate onto quiet back-matter pages unless the book map explicitly says so.

---

*Status date: 2026-07-23 (section 5 + agent checklist items 5–7).*
