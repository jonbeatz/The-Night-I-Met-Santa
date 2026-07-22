# CONTINUE HERE — The Night I Met Santa

**Read this first after TRUTH + START-HERE.**  
Project root: `D:\Hermes\projects\The-Night-I-Met-Santa`  
Operator: Jon · Gift for **Jack Farrell** · Birthday **2026-08-15**

---

## One-line status (2026-07-21 night)

**Flow pass PROVED the book** · Klein dials **STOPPED**. Page count **36**.  
**INDEX:** `Media/generated/mocks/_INDEX/flow-pass-2026-07-21.md` · **Flipbook:** `Output/flow-pass-2026-07-21-flipbook.pdf`  
**Story keeps:** S1–S6 · **S7 v03** (look-up + holly PJs) · **S8 v02** · S9–S10 · S11 v02 · S12 · locks S3/P01/cover/Jack  
**Matter keeps:** P02 · P03 · P05 · P32 · P33 · Hard PJ append locked on all story gens  
**NEXT = InDesign production** via `PAGE-BUILD-WORKFLOW.md` + `AGENT-RUNBOOK.md` — start **P01 Title** (art locked → PSD ART → MOCK-TYPE upper cream → live ID).  
**Prompt SoT:** `MASTER-PRODUCTION-DOCK.md` · page map: `BOOK-PAGE-WORKFLOW.md`  
**Gotchas:** Jon first-Save As · PS-first · no Free Transform · don’t mid-paint-crop vignettes (`ISSUES-RESOLVED.md`).

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
| **`Media/approved/`** | Keepers — `style-refs/` moodboard · Tier B locks — `INDEX.md` |
| `Media/generated/` | Experiments · **`mocks/{unit}/vNN/`** + RECIPE |
| `Media/assets/` | Watercolor cloud PNGs + reusable layout assets |
| `Images/references/` | Jack/photos + Christmas book + **layout** north stars |
| `Images/chopz/` | Exports for InDesign (MOCK / L/R / textCloud) |
| `Xtraz/Fonts/` | Local OFL pack (gitignored) — `FONT-CATALOG.md` |
| **`Xtraz/Adobe-inDesign/`** | Working `.indd` |
| **`Xtraz/Adobe-Photoshop/`** | Working PSDs · blanks (`spread` / `single-page` / `book-covers`) |
| **`Xtraz/Affinity/`** | Optional Affinity working docs |
| `Output/interiors/` · `Output/covers/` | Lulu PDF exports |
| `Pages/` | **Deprecated / empty** — Pillow fallback only (`Pages/README.md`) |
| `_archive/docs/` · `_archive/images-scratch/` | Superseded docs + parked Image scratch |
| `scripts/_scratch/` | One-off `_ps_*` / `_tmp_*` scripts |
| `BOOK-PLAYBOOK.md` | Future-book master |
| `AGENT-RUNBOOK.md` | **Authoritative build runbook** |

**Do not** put working art under `.cursor/assets/` — root `Media/` / `Images/` / `Output/` only.  
**Do not** keep working `.indd` under `Output/` — edit in `Xtraz/Adobe-inDesign/`; export PDFs to `Output/`.  
**Do not** merge `Images/` into `Media/` — different jobs (refs/chops vs generated/approved).

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

### 0. Flow art is dial-complete — do **not** reopen Klein sweeps
Keepers live under `Media/generated/mocks/` (see flow INDEX). Optional later: Lane B paint unify / print px remakes — **not** blocking first InDesign pages.

### 1. InDesign cold start (Jon + agent)
Follow **`AGENT-RUNBOOK.md`** cold flow: CC Desktop → UDT + InDesign + bridges → Jon **Load & Watch** → Connected ✓.

### 2. First production unit = **P01 Title**
1. Duplicate `single-page-template.psd` → `p01-title.psd` (Jon first Save As if needed).
2. Place `Media/approved/pages/p01-title.png` on **ART** · **close source PNG**.
3. MOCK-TYPE in **upper cream** (Cinzel title / Cormorant author) — not lower-center.
4. Cloud if needed → chops → InDesign live type (same pt).
5. Then **P02 → P03 → 4|5 → S1…** sequential.

### 3. Spread loop (after front matter)
PS MOCK + chops (`Images/chopz/`) → InDesign → live Cormorant poem **20/26 +5**. Use keep dials as ART (promote to `Media/approved/` when Jon locks a plate).

### 4. Do **not** re-research print
`RESEARCH-VERDICT.md` — Lulu primary. Export via `Lulu-Interior-Print-PDF.joboptions` when pages ready.

### 5. Cover wrap + proof
Back cover still open · spine after page count final · proof order **~July 25–28**.

**Docs:** `AGENT-RUNBOOK.md` · `PAGE-BUILD-WORKFLOW.md` · `INDESIGN-PRODUCTION-WORKFLOW.md` · `MASTER-PRODUCTION-DOCK.md` · `FONT-CATALOG.md`

### Optional later (not blocking gift)
Lane B finals batch · web flipbook · Affinity polish · Mixam multi-copy
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
