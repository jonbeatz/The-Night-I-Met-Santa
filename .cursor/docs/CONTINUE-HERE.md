# CONTINUE HERE — The Night I Met Santa

**Read this first after TRUTH + START-HERE.**  
Project root: `D:\Hermes\projects\The-Night-I-Met-Santa`  
Operator: Jon · Gift for **Jack Farrell** · Birthday **2026-08-15**

---

## One-line status (2026-07-20)

**InDesign production locked** · page count **35–40** · `AGENT-RUNBOOK.md` authoritative.  
**Creative loop dial-in:** **`.cursor/docs/PAGE-BUILD-WORKFLOW.md`** — PS↔ID size parity · Klein Dial D2 · no fake gutter · mocks+RECIPE · close PNG · MOCK-TYPE by role (poem 20/26 · matter 30).  
**Docs habit:** **`update docs`** = harvest workflow into playbooks · **`log fixes`** = ISSUES-RESOLVED card · see PAGE-BUILD §11.  
**Smoke:** `p03-dedication.psd` + `p03-dedication-smoke.indd` · mocks `Media/generated/mocks/P03-dedication/v01/`.  
**Page map draft:** **`.cursor/docs/BOOK-PAGE-WORKFLOW.md`** — confirm ~36-page plan.  
**Spread loop:** Jon PS MOCK + `Images/chopz/` → InDesign **live Cormorant** (poem 20/26 +5 #2C2C2C).  
**Continuity:** Boy G0 + Santa G0 in `Media/approved/characters/` — attach on every boy/Santa gen.  
**Eyes-met:** prototype **4–5** (= story **S3** → book **10|11**).  
**Photoshop MCP LIVE:** adobepy UXP — `PHOTOSHOP-SETUP.md`.  
**Next:** Confirm page map → next unit with full RECIPE + tab hygiene.  
**Playbook:** `ISSUES-RESOLVED.md` · `BOOK-PRODUCTION-SYSTEM.md` · `PAGE-BUILD-WORKFLOW.md`.

---

## What we are building

An **8.5×8.5"** full-color children’s picture book from Jack’s Christmas poem *The Night I Met Santa*, illustrated in **painted gouache / soft watercolor** (Golden Age / Santore–adjacent — **not** colored pencil), printed as **1 hardcover gift** (Lulu), possibly more later.  
**Target length:** **35–40 pages**. Target printer: **[Lulu](https://www.lulu.com/)** — exact 8.5×8.5 casewrap hardcover, single copy OK.  
**Build authority:** repo-root **`AGENT-RUNBOOK.md`**.

---

## Folder map (canonical)

| Path | Role |
|------|------|
| `Transcription/poem-clean.txt` | Poem text of record |
| `Media/` | Scene + cover illustrations (keep; refine as needed) |
| **`Media/approved/`** | **Two-tier keepers** — `style-refs/` moodboard · Tier B locks — see `INDEX.md` |
| `Xtraz/Fonts/` | Local OFL pack (gitignored) — roles in `FONT-CATALOG.md` |
| **`Xtraz/Adobe-inDesign/`** | **Working InDesign docs** (`.indd`) — current: `eyes-met-prototype-v1.indd` |
| **`Xtraz/Adobe-Photoshop/`** | Working PSDs · blanks: **`spread-page-template`** · **`single-page-template`** · **`book-covers-template`** (no spine PSD) |
| **`Xtraz/Affinity/`** | Optional Affinity working docs |
| `BOOK-PLAYBOOK.md` | Future-book master playbook (repo root) |
| `Media/generated/` | Experiments / batches (not the source of truth for “what we picked”) |
| `Images/references/` | Jack photos + Christmas book style refs |
| `Images/references/layout/` | **Jon’s layout north stars** (phone photos) |
| `Pages/` | Optional fallback composites (empty — InDesign is production) |
| `Output/interiors/` | Exported interior PDFs for Lulu |
| `Output/covers/` | Exported cover PDFs for Lulu |
| `Media/assets/` | Watercolor cloud PNGs + reusable layout assets |
| `AGENT-RUNBOOK.md` | **Authoritative build runbook** (DTP, print, design, never-dos) |
| `composite_pages.py` | Pillow compositor — **fallback only** |
| `book-final.typ` | Typst binder — **fallback only** |
| `build_cover*.py` | Legacy wrap builders — prefer InDesign + Lulu cover template |
| `Book-Findings.md` | Full research + failed iteration log |
| `_archive/layout-attempts/` | Rejected Typst v2–v4 sources (do not revive blindly) |
| `.cursor/docs/book/` | Preview PNGs + small v3/v4 PDF samples |

**Do not** put working art under `.cursor/assets/` — root `Media/` / `Pages/` / `Output/` only.  
**Do not** keep working `.indd` under `Output/` — edit in `Xtraz/Adobe-inDesign/`; export PDFs to `Output/`.

---

## Layout north star (Jon’s photos)

1. **`Images/references/layout/ref-overlay-cloud-text.png`**  
   Full-bleed art + soft irregular **translucent cloud/panel** under black text; short white lines OK on dark sky.

2. **`Images/references/layout/ref-spread-bleed-text.png`**  
   Left page mostly text/paper; illustration **bleeds in** from the right with painterly feathered edge.

**Rejected:** hard white boxes (v3), Typst PNG alpha checkerboards (v4), soft cream **rectangles** that still feel like boxes (v5).

**Engineering rule:** InDesign production — art → cloud PNG → Cormorant text. Export PDFs to `Output/`. Working `.indd` in `Xtraz/Adobe-inDesign/`.

---

## What’s done

- [x] Audio transcribed → `poem-clean.txt`
- [x] Style direction (painterly Christmas storybook)
- [x] Scene illustrations in `Media/` (15+ scenes; not all final)
- [x] Cover art options in `Media/`
- [x] POD research → Lulu primary
- [x] Hermes fleet skeleton (skills, IMAGE-WORKFLOW, session scripts)
- [x] Project moved to `D:\Hermes\projects\The-Night-I-Met-Santa`

## What’s NOT done / wiped on purpose

- [ ] Poem page layouts Jon likes (Pages empty — start fresh)
- [ ] Print-ready interior PDF with bleed
- [ ] Lulu cover wrap with correct spine
- [ ] Proof order + gift hardcover
- [ ] Some Media assets may still need consistency pass (faces, style lock)

---

## Start next (priority order)

### 0. Confirm page workflow
Review **`BOOK-PAGE-WORKFLOW.md`** — poem → imagery → temp filenames → full page list (About, Thank You, Jack portrait). Confirm ~36 pages + spread-first story (S1–S12).

### 0b. Do **not** re-research print from scratch
Read **`RESEARCH-VERDICT.md`** — Lulu primary, KDP HC skipped, timeline locked.

### 1. Beat gap → approval sprint (print path)
1. Open `Media/approved/INDEX.md` + `BOOK-PAGE-WORKFLOW.md` + `PAGE-PROMPT-BIBLE.md`.
2. Generate missing spreads per workflow checklist (S1, S2, S4…); keep S3 eyes-met as north star.
3. **Pick cover** A–E if back still open → Tier B `covers/`.
4. Lane A Klein dial → Jon pick → Lane B Gemini/Banana finals → watermark check → promote.

### 2. Quiet-zone map (after Tier B art locks)
For each locked page/spread, note where text sits without covering faces (policy: `TEXT-OVERLAY-POLICY.md`). Jon places cloud PNG per spread.

### 3. InDesign build (production path)
Follow **`AGENT-RUNBOOK.md`** + **`INDESIGN-PRODUCTION-WORKFLOW.md`**:
- Doc: 8.5×8.5", 0.125" bleed, single-page, **35–40** pages, sRGB
- Layer stack: art → watercolor cloud PNG → **Cormorant Garamond Medium 20/26 tracking +5**, centered #2C2C2C
- Export: `Lulu-Interior-Print-PDF.joboptions` → upload interior → download Lulu cover template → cover export

### 4. Fallback only (if InDesign blocked)
`composite_pages.py` + `book-final.typ` / img2pdf — emergency path, not the gift default.

### 5. Cover + Lulu proof
After interior upload → Lulu custom cover template (exact spine) → InDesign cover → order proof by **~July 25–28**.

**Docs:** `AGENT-RUNBOOK.md` · `INDESIGN-PRODUCTION-WORKFLOW.md` · `BOOK-PRODUCTION-SYSTEM.md` · `PAGE-PROMPT-BIBLE.md` · `FONT-CATALOG.md`

### Optional later (not blocking gift)
Web flipbook (`DIGITAL-FLIPBOOK-WATCH.md`) · Affinity polish · Mixam multi-copy
---

## Commands (from this project root)

```powershell
# Session
npm run session:open

# Image pipeline (paid fal + HF drafts) — saves to Media/generated/
npm run image:doctor
npm run image:fal:page -- "Christmas Eve living room, painterly Santore style..."
npm run image:fal:spread -- "Santa and child on floor among gifts, wide cinematic..."
npm run image:fal:cover -- "hero holiday cover scene..."
npm run image:gen:page -- "cheap draft..."   # HF — optional

# DTP production (READY 2026-07-19) — see AGENT-RUNBOOK.md §1
npm run layout:indesign-bridge   # InDesign UXP HTTP/WS :19300/:19301 — keep running
npm run layout:photoshop-mcp     # Photoshop adobepy broker :47391 + MCP :8766 (LIVE 2026-07-20)
# Affinity MCP :6767 when Affinity open + MCP toggles ON (optional polish)
# Full how-to: tools/layout-mcp/SETUP.md · PHOTOSHOP-SETUP.md

# Fallback only (Pillow/Typst — not gift default)
npm run book:composite
npm run book:typst
npm run book:pdf:doctor
npm run book:pdf:from-pages
npm run book:pdf:verify
npm run book:pdf:verify:boxes
```

Presets: **page** = 2625×2625 · **spread** = 5250×2625 · **cover** = 2048² draft  
Text on art: **InDesign** (cloud PNG + Cormorant). Pillow compositing = fallback only.

---

## Agent handshake

On Open Project / first message in this workspace:

> Ok Jon — The-Night-I-Met-Santa profile loaded, ready.

Then read: `TRUTH.md` → **`AGENT-RUNBOOK.md`** → this file → `ReCall.md`.
