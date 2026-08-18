# BOOK-2-TEMPLATE.md — Startup Checklist for the Next Picture Book

**Purpose:** Clone-and-go checklist to start Book #2 from TNIMS project template  
**Based on:** "The Night I Met Santa" (Book #1) retrospective audit, 2026-08-03  
**Prerequisite:** Read BOOK-1-RETROSPECTIVE.md for full lessons learned

---

## Phase 0: Project Scaffold

- [ ] Create new project folder (e.g. `D:\Hermes\projects\{book-slug}/`)
- [ ] Initialize git + `package.json` with npm scripts from TNIMS
- [ ] Clone `.cursor/` skeleton with rules, prompts, and docs structure
- [ ] Set up Hermes profile or project-specific context

### Clone From TNIMS (Tier 1 — as-is)
```
Copy these files/folders directly:

.cursor/docs/PICTURE-BOOK-PRODUCTION-RULES.md
.cursor/docs/INDESIGN-PRODUCTION-WORKFLOW.md
.cursor/docs/PS-TO-ID-TYPE-HANDOFF.md
.cursor/docs/BACKUP-BOOK-TIERS.md         → update backup root path
.cursor/docs/RECIPE-TEMPLATE.md
AGENT-RUNBOOK.md                          → lives at REPO ROOT (not .cursor/docs/)
.cursor/docs/FINALS-CHECKLIST.md          → rebuild unit matrix
.cursor/docs/LULU-8.5-SQUARE-CHEATSHEET.md  → if same trim
.cursor/docs/LULU-WEBSITE-ORDER-PLAYBOOK.md
.cursor/rules/                            → clone rule set
.cursor/prompts/                          → clone session rituals

scripts/book_poem_map.py                  → update poem source
scripts/book_review_board.py
scripts/book-comparison-board.py
scripts/book-flipbook-assemble.py
scripts/project-backup.mjs                → update paths
scripts/export_merged_plates_from_psb.py

Xtraz/Adobe-Photoshop/spread-page-template.psd
Xtraz/Adobe-Photoshop/single-page-template.psd
Xtraz/Adobe-Photoshop/book-covers-template.psd
Xtraz/Lulu-Templates/

scripts/create_spread_page_template_psd.py   → regenerates spread-page-template.psd
scripts/create_ps_page_templates.py          → regenerates single-page + book-covers templates
```

> **PSD blanks note (2026-08-07):** the three template PSDs went missing when they were
> swept into `Hold-v1\` on Aug 1; they have been **restored** to `Xtraz\Adobe-Photoshop\`.
> They are gitignored binaries — if they ever vanish again, regenerate with the two
> creator scripts above (Photoshop open + adobepy broker :8766) or rebuild by hand from
> **`.cursor/docs/BOOK-2-TEMPLATE-PSD-SPEC.md`** (exact sizes, layer stacks, guide colors).

### Create Fresh (Tier 2 — clone + replace content)

| File | Replace With |
|------|-------------|
| `DESIGN-TOKENS.md` | New color palette, character tokens, typography, image rules for Book #2 |
| `BOOK-PRODUCTION-SYSTEM.md` | New book name, author, trim, dates, product decisions |
| `MASTER-PRODUCTION-DOCK.md` | New story prompts, page map, style tags, character blocks |
| `IMAGE-LANE-PROMPTS.md` | New style master block, Klein D2 tag if style changes |
| `IMAGE-LANE-SYSTEM-v2.md` | Update for current model landscape |
| `COVER-PROMPTS.md` | New title, author credit, cover concepts |
| `ILLUSTRATION-STYLE.md` | New style north stars, master prompt blocks |
| `FONT-CATALOG.md` | Rebuild if different fonts |

### Build From Scratch (Tier 3 — per-book)

| Doc | What It Needs |
|-----|--------------|
| `PAGE-MAP.md` | SINGLE source of truth: page→poem→art→frame→type assignment |
| `JON-BOOK-FLOW-vN-FINAL.md` | Page map, camera directions, design rhythm, wardrobe locks |
| `BOOK-COPY-DRAFTS.md` | About, Thank You, Dedication, edition credits |
| `PAGE-BUILD-WORKFLOW.md` | PS→ID build loop for this book |
| `CHARACTER-{name}.md` | Per-character reference sheets |

---

## Phase 1: Source Material Lock

- [ ] Finalize poem/manuscript text → `Transcription/poem-clean.txt`
- [ ] Lock trim size (8.5×8.5" or new dimensions)
- [ ] Lock page count target (32–40 range)
- [ ] Lock author/credit lines
- [ ] Set production deadline + proof order date

---

## Phase 2: Design System Lock (Day 1-3)

### Colors
- [ ] Create DESIGN-TOKENS.md from TNIMS template
- [ ] Lock primary palette: walls, characters, environment, text/background
- [ ] Lock character wardrobe tokens (outfit colors, trim, details)
- [ ] Define firelight/moonlight/ambient lighting tokens
- [ ] Define frame treatment policy (singles vs spreads)

### Typography
- [ ] Select and install fonts (OFL preferred; pack in `Xtraz/Fonts/`)
- [ ] Lock title font + size + weight (e.g. Cinzel Decorative 36pt)
- [ ] Lock body font + size + leading + tracking (e.g. Cormorant Garamond Medium 20/26 +5)
- [ ] Lock page number font + size
- [ ] Write FONT-CATALOG.md with exact PostScript names
- [ ] **Critical:** Use exact PostScript names from Day 1 (e.g. `Cormorant Garamond\tMedium`, NOT "Cormorant Garamond")

### Style North Stars
- [ ] Generate 2-3 hero style-ref frames (the equivalent of S3 Eyes Met v07)
- [ ] Lock ILLUSTRATION-STYLE.md with master prompt block + negatives
- [ ] Save style refs to `Media/approved/style-refs/style-lock-v2.png`
- [ ] Save quality bar to `Media/development/_quality-targets/`

---

## Phase 3: Model Lane Setup

- [ ] Create IMAGE-LANE-PROMPTS.md with lane priority:
  - **Lane A1 (Dial):** Klein 9B or equivalent (~$0.01/sq) — layout + vibe
  - **Lane A2 (Alt):** Qwen 2 Pro Edit or equivalent — second opinion
  - **Lane A3 (Light):** Klein 4B or equivalent — hi-res/low-detail only
  - **Lane B (Finals):** Gemini/Banana Pro or equivalent — production keepers
- [ ] Create Klein D2 style tag (or new equivalent)
- [ ] Create Master Style block for finals
- [ ] **Rule:** ONE doc is model authority (MASTER-PRODUCTION-DOCK). Kill lane doc duplication.
- [ ] **Rule:** Mocks = Qwen 2 Pro only. Finals = Gemini/Banana only. No cross-contamination.

---

## Phase 4: Page Map + Prompt Bible

- [ ] Write PAGE-MAP.md — the single authoritative page inventory:
  - Page number, LEFT/RIGHT assignment
  - Form: SINGLE / SPREAD / TEXT+IMAGE / SPLIT
  - Unit slug (e.g. S03-eyes-met)
  - Full poem text assignment per page
  - Image brief per page
  - Camera direction per page
  - Frame ON/OFF per page
  - Art status: NEED / HAS / LOCKED
- [ ] Write MASTER-PRODUCTION-DOCK.md with ready-to-paste prompts for every beat
- [ ] Define closing copy placement EARLY ("God bless."-type lines — where do they live?)
- [ ] **Rule:** PAGE-MAP.md is always the source of truth. When closing copy changes, update PAGE-MAP.md FIRST.

---

## Phase 5: Character Lock

- [ ] Create CHARACTER-{name}.md for each major character
- [ ] Generate G0 reference sheets (full body + face) for each character
- [ ] Save to `Media/approved/characters/{name}-G0.png` and `{name}-G0-face.png`
- [ ] Create hard-append text blocks for every generation prompt
- [ ] Lock wardrobe details with exact colors + patterns

---

## Phase 6: Cover Design

- [ ] Write COVER-PROMPTS.md with front/back/spine prompts
- [ ] Lock title treatment direction (e.g. ornate gold serif + flourishes)
- [ ] Lock author credit format (e.g. "Written by {Author}" live in InDesign)
- [ ] Generate cover concept batches
- [ ] **Rule:** Cover type from AI often misspells. Have a fallback: AI art-only + live type in InDesign.
- [ ] **Rule:** Back cover gets a dedicated TEXT-SCRUB pass before final review.

---

## Phase 7: Image Generation Pipeline

### Hardware/Infrastructure
- [ ] Set up fal.ai API key + OpenRouter backup
- [ ] Configure image generation npm scripts
- [ ] Verify model endpoints are accessible
- [ ] Set up upload/download workflow

### Generation Loop (per spread)
- [ ] Create batch folder under `Media/generated/mocks/{unit}/`
- [ ] Lane A1 dial (Klein 9B) → RECIPE.md
- [ ] Optional Lane A2 alt (Qwen) → comparison board
- [ ] Jon reviews comparison board → picks winner
- [ ] **TRIPLET RULE:** Every spread → `art.png` (5250×2625) + `art-left.png` (2625²) + `art-right.png` (2625²)
- [ ] **RESOLUTION RULE:** development art = print-sized. Never keep a sub-2625 dashboard `art.png`.
- [ ] **HYGIENE:** Never overwrite a locked KEEP for a test. Tests = new version numbers.

---

## Phase 8: InDesign Production

### Setup (one-time per book)
- [ ] Install/enable InDesign UXP bridge (:19300/:19301)
- [ ] Create InDesign document from Lulu template (8.5×8.5", 0.125" bleed, facing pages)
- [ ] Create paragraph/character style kit (one per type role)
- [ ] Load Lulu PDF export presets (`.joboptions` files)
- [ ] **Auto-save:** Enable InDesign auto-save backup every 5 minutes (Preferences → File Handling)

### Build Loop (per unit)
- [ ] PS MOCK: place art + MOCK type in PS (20/26, centered, #2C2C2C)
- [ ] Export `type-inventory.json` via `npm run book:type:export`
- [ ] Export Merged art plate (RGB opaque — NO alpha channel)
- [ ] Place art in InDesign frame at correct position
- [ ] Build live type from type-inventory → matching font/size/leading/tracking/color/bbox
- [ ] MOCK at ~35% → hide
- [ ] **Rule:** Seamless spreads = one `*-spread.png` (17.5×8.75") centered on spine. Text+image splits = separate L/R frames meeting at spine.
- [ ] **Rule:** No drop shadows on live type in cover INDD (forces CMYK flatten).

### Export
- [ ] Interior PDF: single pages, sRGB, 8.75×8.75" bleed, no trim marks
- [ ] Cover PDF: sRGB forced (`PDFColorSpace.RGB`), wrap dimensions from Lulu template
- [ ] Flipbook PDF: trim-only 8.5×8.5" (NOT bleed), for preview/review only
- [ ] Verify ALL pages @ effective 300 DPI

---

## Phase 9: Quality Gates

### Per-Unit Checklist (every locked spread)
- [ ] RES: singles 2625² · spreads 5250×2625 + L/R 2625²
- [ ] TRIP: triplet present
- [ ] FRAME: ON/OFF matches page map
- [ ] COAT: wardrobe matches G0 refs
- [ ] FACE: character identity doesn't drift
- [ ] GUTTER: no baked fold · faces clear of center
- [ ] TEXT: no baked letters · type zones open
- [ ] TYPE-INV: `type-inventory.json` present (if live type)
- [ ] POEM: copy matches poem map
- [ ] RECIPE+meta: unit-root RECIPE.md + meta.json both present

### Book-Level Checklist
- [ ] Even page count
- [ ] All art at 300 DPI print resolution
- [ ] 0.125" bleed on all edges
- [ ] 0.5" safety zone from trim for faces/text
- [ ] No gutter overlap on text+image splits
- [ ] Interior PDF: single-page, sRGB, bleed, no trim marks
- [ ] Cover PDF: sRGB, correct wrap dimensions, no drop shadows
- [ ] Flipbook PDF: trim-only 8.5×8.5", burgundy IFC/IBC if designed
- [ ] No watermarks on any print plate
- [ ] All fonts embedded or outlined

---

## Phase 10: Lulu Upload

- [ ] Upload interior PDF first → get exact cover template with spine width
- [ ] Build cover using Lulu-generated template
- [ ] Upload cover PDF
- [ ] Review print-ready preview (color check)
- [ ] Order one physical proof (softcover for cost; hardcover for gift)
- [ ] Lulu paper: Premium Color, heavier stock
- [ ] Lulu color: confirm sRGB (not CMYK)
- [ ] Document order process in LULU-WEBSITE-ORDER-PLAYBOOK.md

---

## Phase 11: Backup Discipline (START ON DAY 1)

- [ ] `npm run backup:quick` — daily / after dial sessions
- [ ] `npm run backup:full` — milestones / pre-proof
- [ ] `npm run backup:archive` — rare deep freeze
- [ ] Verify backup root path exists and has space
- [ ] **Rule:** Backup BEFORE and AFTER any major InDesign session.

---

## Phase 12: Ship + Retrospective

- [ ] Lulu order placed → track shipping
- [ ] Digital flipbook generated for preview/sharing
- [ ] Archive final PDFs to `Output/FINAL-Master-PDFs/`
- [ ] Write BOOK-N-RETROSPECTIVE.md (clone this template pattern)
- [ ] Update PICTURE-BOOK-PRODUCTION-RULES.md with new lessons
- [ ] Update fleet docs in `_core-scripts/`
- [ ] Commit + push all docs

---

## Quick Reference: Top 10 Lessons from Book #1

1. **Dashboard art.png = always print-scale** (2625² or 5250×2625)
2. **Use type-inventory pipeline from spread #1** (`npm run book:type:pipeline`)
3. **One doc for model lanes** — kill lane doc duplication
4. **Update ALL docs when a decision changes** — stale docs kill
5. **Spread triplet from Day 1** — art.png + art-left + art-right
6. **RGBA → RGB for print plates** — no alpha in InDesign links
7. **Multi-animal scenes = Photoshop composite** — not AI generation
8. **Frame treatment via Pillow, not AI regen** — deterministic, not stochastic
9. **Flipbook PDF ≠ Lulu PDF** — trim vs bleed, two different exports
10. **Backup on Day 1** — `npm run backup:quick` is a habit, not a task

---

## Folder Structure Template (clone for Book #2)

```
{book-slug}/
├── .cursor/
│   ├── docs/           ← clone Tier 1+2 docs here
│   ├── rules/          ← clone rule set
│   ├── prompts/        ← clone session rituals
│   ├── plans/          ← planning docs
│   └── skills/         ← project-specific skills
├── Media/
│   ├── approved/
│   │   ├── characters/     ← G0 refs
│   │   └── style-refs/     ← style-lock-v2
│   ├── development/
│   │   ├── _quality-targets/
│   │   ├── Cover/
│   │   ├── P01-title/
│   │   ├── S01-{slug}/
│   │   ├── S02-{slug}/
│   │   └── ...              ← one folder per unit
│   ├── finals/              ← Lulu-ready after InDesign
│   └── generated/
│       └── mocks/           ← dial batches + RECIPEs
├── Images/
│   ├── references/
│   │   ├── cover/
│   │   ├── layout/
│   │   └── style/
│   └── styles2/             ← frame refs etc.
├── Transcription/
│   └── poem-clean.txt
├── Output/
│   ├── interiors/
│   ├── covers/
│   ├── flipbooks/
│   └── FINAL-Master-PDFs/
├── Xtraz/
│   ├── Adobe-Photoshop/     ← PS templates + working PSDs
│   ├── Adobe-inDesign/      ← INDD working files
│   ├── Adobe-Finals/        ← final INDDs + PDFs
│   ├── Fonts/               ← OFL font files
│   └── Lulu-Templates/      ← Lulu templates
├── scripts/                 ← cloned scripts
├── tools/                   ← MCP bridges etc.
├── _archive/                ← rejected experiments
└── package.json             ← cloned npm scripts
```

---

*This template is a living document. After Book #2, update it with new lessons learned.*
