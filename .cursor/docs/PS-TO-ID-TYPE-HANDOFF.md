# Photoshop → InDesign type handoff (book 2+)

**Status:** LOCKED recommendation · **2026-08-03** (post-TNIMS order)  
**Why:** Matching PS type to live ID by eye was the biggest time sink on TNIMS. This doc is the fix for the next Hermes picture book.

**Authority:** Print type = **InDesign live**. Photoshop type = **design lock + MOCK guide**.  
**Related:** `AGENT-RUNBOOK.md` (PS→ID rules) · `MERGED-PLATE-EXPORT-WORKFLOW.md` · fleet `PICTURE-BOOK-PRODUCTION-RULES.md` §7

---

## 1 — Operating model (one sentence)

**Design type in Photoshop → export `type-inventory.json` + Merged art (glow shells OK as guides) → InDesign builds live frames from inventory → MOCK at ~35% for eye-check → hide MOCK.**

---

## 2 — What belongs where

| Content | Photoshop | InDesign |
|---------|-----------|----------|
| Illustration / atmosphere | **Yes** (Merged plate) | Linked PNG |
| Body poem / paragraphs | Design layers only | **Live** frames |
| Mixed bold / size runs | Separate type layers or named runs | Character styles |
| Logos / flourishes / “Merry Christmas” art | **Bake in art** if graphic | Or linked logo PNG |
| Soft glow under type | Fill-0 type shell on Merged OK | Prefer light ID effect or dark plate under type |
| Drop shadow / outer glow as **final** letter look | Avoid for body copy | Avoid / very light |

**Rule:** Atmosphere in the painting. Readability in live type.

---

## 3 — Type inventory schema (required on every keep)

When a unit locks for layout, write:

```
Media/development/{unit}/type-inventory.json
```

Also copy/sideload next to chops when exporting Merged:

```
Xtraz/Adobe-Finals/FINAL-Master-Chopz/.../{unit}-type-inventory.json
```

### Schema

```json
{
  "unit": "S04-sit-here",
  "canvas_px": [5250, 2625],
  "dpi": 300,
  "bleed_in": 0.125,
  "pages": {
    "left": { "book_page": 10, "role": "text" },
    "right": { "book_page": 11, "role": "image" }
  },
  "frames": [
    {
      "id": "stanza-1",
      "ps_layer": "Poem / stanza 1",
      "page": "left",
      "bbox_px": { "l": 420, "t": 780, "r": 2200, "b": 1180 },
      "font": "Cormorant Infant",
      "style": "Medium",
      "size_pt": 20,
      "leading_pt": 26,
      "tracking": 50,
      "color": "#2C1810",
      "align": "center",
      "space_before_pt": 0,
      "space_after_pt": 8,
      "paragraph_style": "Poem-Body",
      "text": "Full stanza text here…",
      "runs": [
        { "start": 12, "end": 18, "character_style": "Poem-Emph" }
      ]
    }
  ],
  "notes": "Optional: kerning pairs Jon forced by eye"
}
```

### Coordinate rule (spread canvas → ID)

1. Canvas is **full bleed** art (e.g. 5250×2625 @ 300).  
2. Convert bbox to inches: `value_in = px / 300`.  
3. Subtract bleed when mapping to **page** coordinates:  
   - Spread left page: `x_page = bbox.l/300 − bleed` (and clamp to page).  
   - Prefer measuring bbox relative to **page trim** in PS guides (cyan TRIM) so inventory is already page-local.  
4. Document units in ID must be **points** before setting `pointSize` / `leading` (pica gotcha).

### Layer naming convention (do this in PS)

| Layer name pattern | Meaning |
|--------------------|---------|
| `type/body-01` | Poem body frame 1 |
| `type/body-01-emph` | Optional separate emph layer (or use `runs`) |
| `type/title` | Title / display |
| `type/byline` | Author line |
| `guide/glow-shell` | Fill-0 effect shell — **not** live text |

Hide or prefix `guide/` so exporters skip shells as copy sources.

---

## 4 — InDesign style kit (create once per book)

Before page 1 of live type, create:

| Paragraph style | Typical use |
|-----------------|-------------|
| `Poem-Body` | Main stanza |
| `Poem-Body-Tight` | Dense pockets |
| `Poem-Display` | Large openers |
| `Matter-Body` | Dedication / thank-you |
| `Matter-Signoff` | *God bless. — Name* |
| `Title-Main` | Title page |

| Character style | Typical use |
|-----------------|-------------|
| `Poem-Emph` | Bold / heavier weight for selected words |
| `Poem-Small` | Smaller run inside a stanza |

Map inventory `paragraph_style` / `character_style` → these names.  
**Do not** invent one-off unnamed overrides unless Jon asks.

Fallback only (no inventory): Cormorant Medium **20/26** tracking **+5**, centered — never force this when inventory exists.

---

## 5 — MOCK workflow

1. Export Merged art (glow shells included if useful).  
2. Place Merged full-bleed / spine-centered per runbook.  
3. Place **MOCK** = same Merged (or PS flat export with type visible) @ **30–40%** opacity on a `MOCK` layer.  
4. Build live frames from inventory on a `TYPE` layer above MOCK.  
5. Eye-check vs MOCK (glyphs inside magenta safety).  
6. Hide or delete MOCK before PDF.

Baked type in Merged = **guide**, not final.

---

## 6 — Merged vs full layers

| Do | Don’t |
|----|--------|
| Dual stack: Layer-Comps + Merged-Comps | Place full PSB into InDesign |
| Export `*Merged*` via `psd_tools` `topil()` | Rely on `composite()` of hidden groups |
| Live type overlay | Bake all body copy into final plate |
| Bake logos / graphic words that aren’t editable copy | Fight Outer Glow as the only readability tool |

---

## 7 — Shadows / glows (print)

| Use | Guidance |
|-----|----------|
| Scene vignette / cast shadow | Prefer **painted into art** |
| Soft plate under type zone | OK — darken art or soft rectangle behind frame |
| Outer Glow / Drop Shadow on **live** body type | Avoid or keep very light |
| Fill-0 glow shells on Merged | OK as placement guide |

---

## 8 — Tooling (shipped 2026-08-03)

| Surface | Role |
|---------|------|
| InDesign UXP + exec MCP | Place frames, styles, export — **print authority** |
| Photoshop MCP / adobepy | Assist / inspect; cold-start fiddly |
| `scripts/export_merged_plates_from_psb.py` | Merged art dump SoT |
| **`npm run book:type:export`** | PSB → `_type-inventory.json` (metrics + runs) |
| **`npm run book:type:export:split`** | Also write `Media/development/{unit}/type-inventory.json` |
| **`npm run book:type:validate`** | Schema / required-field check |
| **`npm run book:type:page-map`** | Inventory → `indesign-page-map.json` |
| **`npm run book:type:apply`** | Emit JSX → `Xtraz/Adobe-inDesign/_generated/apply-type-inventory.jsx` |
| **`npm run book:type:styles`** | Emit JSX that only creates the style kit |
| **`npm run book:type:pipeline`** | export → page-map → validate → emit apply JSX |
| Schema | `scripts/schemas/type-inventory.schema.json` |
| Example | `Media/development/_templates/type-inventory.example.json` |
| Manual runner | `Xtraz/Adobe-inDesign/scripts/Apply-Type-Inventory.jsx` |

### Commands

```powershell
# From repo root — export all visible type from Book Master PSB
npm run book:type:export -- --visible-only
npm run book:type:export:split

# One unit
python scripts/export_type_inventory_from_psb.py --unit S04 --visible-only --split-units

# Validate + page map + emit apply JSX (uses active Interior INDD later)
npm run book:type:pipeline
npm run book:type:apply -- --group S04 --active-page
npm run book:type:apply -- --map-pages Xtraz/Adobe-Finals/FINAL-Master-Chopz/indesign-page-map.json --page 10,11

# Then: open Interior INDD → MCP run_jsx with generated file contents
# or File → Scripts → Apply-Type-Inventory.jsx
```

**Apply note:** generated JSX forces **POINTS** units, creates `TYPE` layer, labels frames `ti:{id}` (re-run replaces). Use MOCK @ 35% for eye-check, then hide MOCK.

---

## 9 — Book 2 upgrades (checklist)

### Process
- [x] Type inventory tooling (export / validate / page-map / apply JSX)
- [ ] Type inventory on every layout lock (same day as RECIPE/meta)
- [ ] Style kit created before first live page (`book:type:styles`)
- [ ] MOCK @ 35% until Jon OK
- [ ] Cap dials: max **3** alts → board → lock
- [ ] Use `Media/finals/` only after live type + bleed PDF
- [ ] Lulu: follow `LULU-WEBSITE-ORDER-PLAYBOOK.md` pattern (English + Children · `/cart` only)

### Org (keep TNIMS patterns)
- [x] `_FLOW-CURRENT.json` + three-tier Media
- [x] Unit RECIPE + meta on keep
- [x] Comparison boards one-per-decision
- [x] Flipbook for review only
- [x] Finals quartet: PSD/PSB · Chopz · INDD · PDFs

### Still optional
- [ ] Color-label export for Merged (`--color yellow`) when asked
- [ ] Direct HTTP apply (skip emit) if a stable ID bridge endpoint is added

---

## 10 — Agent rules

1. Never report “type done” if frames were eyeballed while an inventory exists — use the inventory.  
2. Never set bare `pointSize = N` without confirming **points** units.  
3. One PS type layer → one ID frame (unless `runs` say otherwise).  
4. Hide MOCK before calling anything Lulu-final.  
5. Update this doc if a book invents a better inventory field.

---

## Related

- Fleet: `_core-scripts/shared-profile-content/docs/PICTURE-BOOK-PRODUCTION-RULES.md` §7  
- TNIMS: `AGENT-RUNBOOK.md` · `MERGED-PLATE-EXPORT-WORKFLOW.md` · `LULU-WEBSITE-ORDER-PLAYBOOK.md`
