# Media/approved — FINAL KEEPERS (Jon selections)

**This folder is the single place to look for images you’ve approved.**  
Experiments stay under `Media/generated/…`. Sources/refs stay under `Images/`.

**Git:** tracked (Jon 2026-07-15) — unlike `Media/generated/`.

---

## Two-tier system (locked 2026-07-15)

| Tier | Folder | Meaning |
|------|--------|---------|
| **A — Moodboard / near-keepers** | `style-refs/` (+ themed subfolders) | Favorites, style ideas, shot references, cover *candidates*. Browse here to match vibe. **Not** automatically print-final. |
| **B — Composition locks** | `characters/` · `covers/` · `pages/` · `spreads/` | Clean kebab names. Jon-approved look/composition — often **dial/~1K**, not Lulu px yet. |
| **C — Print plates** | `print/` *(create at finals)* | Exact **2625²** / **5250×2625** / cover wrap. Remade from Tier B + recipes. |

**Rule:** Seeing a file under `style-refs/covers/` does **not** mean the cover is locked — promote to `covers/cover-front.png` when you pick the winner.  
**Print plan + continuity:** `.cursor/docs/CONTINUITY-AND-PRINT-FINALS.md`. Each Tier B file should get a **`.recipe.md`** sidecar (example: `covers/cover-front.recipe.md`).  
**Mock tries (before promote):** `Media/generated/mocks/{unit}/vNN/` + **`RECIPE.md`** — see `.cursor/docs/PAGE-BUILD-WORKFLOW.md` · scoreboard `Media/generated/mocks/_INDEX/`.

Jon’s 2026-07-15 organization under `style-refs/` is **kept** (good browsable moodboard). Do not flatten.

---

## How we use it

1. You pick a winner from a batch (e.g. `Media/generated/jack-likeness/v6d-…png`) **or** from `style-refs/…`.
2. Agent **copies** it into the right **Tier B** folder with a clean name + updates this INDEX.
3. Leave the moodboard copy in `style-refs/` for history / `/edit` reference uploads.

| Subfolder | What goes here |
|-----------|----------------|
| `characters/` | **Boy G0 + Santa G0 draft** (2026-07-15) · Jack locked |
| `style-refs/` | Moodboard — themed (see below) |
| `covers/` | Composition-locked front/back (+ `.recipe.md`) |
| `pages/` | Composition-locked singles |
| `spreads/` | Composition-locked spread masters |
| `print/` | Finals only — correct px for PDF/Lulu |

---

## style-refs layout (Jon org — keep)

```
style-refs/
├── covers/     Front candidates A–E (+ UUID scratch → rename when used)
├── back/       Back candidates A–E (+ jack-farrell-back)
├── jack/       Likeness keepers (v4c, v4f, v5d, WINNER-v6d)
├── santa/      Santa character / shush / suspenders refs
├── pages/      Single-page near-keepers + model-compare keepers
├── spread/     Wide + LEFT/RIGHT eyes-met / blessing / note variants
└── story/      Extra scene comps (cocoa square, camera portrait)
```

### Housekeeping suggestions (optional, when renaming)

| Issue | Suggestion |
|-------|------------|
| `covers/c2308d27-….png` | Rename to a descriptive kebab name |
| Multiple eyes-met variants (`06-` vs `spread-01-`) | When locking, pick **one** wide master → copy to `spreads/` |
| `pages/` named `p16-beat07-cocoa` etc. | Good pattern — promote matching bible beat into Tier B `pages/` when final |
| Duplicate Jack (`jack/WINNER…` + `characters/…`) | OK — Tier B is canonical for book; moodboard can keep WINNER |

---

## Inventory — Tier B locks

| Locked | Path | Source / notes | Date |
|--------|------|----------------|------|
| **Jack Farrell portrait** | `characters/jack-farrell-portrait.png` | v6d armchair+tree · `CHARACTER-JACK-FARRELL.md` | 2026-07-15 |
| **Boy G0 LOCKED** | `characters/boy-narrator-G0.png` + `boy-narrator-G0-face.png` | boy-solo-B + boy-solo-C | 2026-07-15 |
| **Santa G0 LOCKED** | `characters/santa-G0.png` | santa-solo-C | 2026-07-15 |
| **Eyes-met spread LOCKED** | `spreads/spread-eyes-met.png` | eyes-met-SPREAD-v3B | 2026-07-15 |
| **Front cover LOCKED** | `covers/cover-front.png` | Doorway peek + oatmeal holly PJs (beige-v2) · glove/bat Easter eggs | 2026-07-15 |
| **Cover title logo** | `covers/cover-title-logo.png` | Clean Cinzel path · clarity-upscaler · navy→alpha (no rembg) | 2026-07-20 |
| **P01 title art LOCKED (provisional)** | `pages/p01-title.png` | mocks `P01-title/v22` · simpler · scenery lower · top cream · FRAME ON | **2026-07-21** |
| Back cover | *(pending)* | Pick companion from `style-refs/back/` | — |
| Pages | *(P01 locked; rest empty)* | Promote per PAGE-PROMPT-BIBLE beat | — |
| Spreads | *(empty)* | Promote when one wide master wins | — |

## Inventory — Tier A moodboard (highlights)

Counts as of **2026-07-15** (~50+ files). Full browse in Explorer; table below is the **useful** set mapped to beats where possible.

### Covers / backs

| Folder | Files | Notes |
|--------|-------|-------|
| `style-refs/covers/` | A–E fronts + UUID scratch | Candidate fronts — **pick pending** |
| `style-refs/back/` | A–E backs + `jack-farrell-back.png` | Companion backs; Jack back for About/thanks vibe |

### Characters / style north stars

| Path | Role |
|------|------|
| `style-refs/jack/WINNER-jack-farrell-v6d.png` | Same as Tier B Jack lock (moodboard copy) |
| `style-refs/jack/v4c`, `v4f`, `v5d` | Face alts for `/edit` remix |
| `style-refs/santa/*` | Santa locks — suspenders, shush, cover Santa |
| `pages/style-sneak-02.png` etc. | Gouache north stars for Banana `/edit` |

### Story near-keepers ↔ poem beats

| File | Likely beat / page |
|------|--------------------|
| `pages/scene-01-the-sneak*.png` · `style-sneak-02` | Beat 1 — sneak |
| `pages/p08-beat02-the-door.png` | Beat 2 — door |
| `spread/*eyes-met*` | Beat 4 — eyes met **SPREAD** |
| `spread/spread-chat-laugh-WIDE.png` | Beat 6 — chat & laugh |
| `pages/p16-beat07-cocoa.png` · `story/scene-06-cocoa*` | Beat 7 — cocoa |
| `story/scene-07-camera-dash*` | Beat 8–9 — camera / dash |
| `pages/p20-beat11-flue-chair.png` | Beat 11 — flue & chair |
| `pages/p21` / `p22` note L/R · `spread-the-note-WIDE` | Beats 12–13 — note |
| `spread/*closing-blessing*` | Beat 15 — closing |
| `pages/p01-title` · `p03-copyright` · `p31` · `p32` | Front/back matter art |

**Full audit:** `.cursor/docs/BEAT-GAP-AUDIT.md`  
**Still thin / need dial or finals:** Beats **3, 5, 9, 10, 14** (MISSING) · **6, 8** (THIN). Prefer **Klein 9B** dial → Qwen alt if needed → Gemini/Banana `/edit` finals with style-refs.

### Model-lane evidence (also in pages/)

| File | Note |
|------|------|
| `pages/05-nano-banana-EDIT-refs-production.png` | Finals lane keep |
| `pages/07-qwen-image-2.png` | Fallback lane keep |

---

## Naming (Tier B)

- Prefer **kebab-case**, no `v2a-…` experiment prefixes once approved.
- Characters: `jack-farrell-portrait.png`
- Pages: `p07-beat01-the-sneak.png` (match PAGE map)
- Spreads: `spread-03-eyes-met.png` (one wide master)
- Covers: `cover-front.png` / `cover-back.png`

---

## Related docs

- Future books: repo-root **`BOOK-PLAYBOOK.md`**
- Living ops: `.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`
- Fonts: `.cursor/docs/FONT-CATALOG.md`
- Jack remake: `.cursor/docs/CHARACTER-JACK-FARRELL.md`
- Beats: `.cursor/docs/PAGE-PROMPT-BIBLE.md`
- Continue: `.cursor/docs/CONTINUE-HERE.md`
