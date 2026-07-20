# CONTINUE HERE — The Night I Met Santa

**Read this first after TRUTH + START-HERE.**  
Project root: `D:\Hermes\projects\The-Night-I-Met-Santa`  
Operator: Jon · Gift for **Jack Farrell** · Birthday **2026-08-15**

---

## One-line status (2026-07-20 night)

**InDesign production locked** · page count **35–40** · `AGENT-RUNBOOK.md` authoritative.  
**Spread loop locked:** Jon PS MOCK + `Images/chopz/` → agent matches InDesign → **live Cormorant** (Medium 20/26 +5 centered #2C2C2C).  
**Eyes-met:** pages **4–5** MOCK-matched (art L/R + textCloud + paintFrame + live poem); pages **2–3** earlier prototype.  
**Working file:** `Xtraz/Adobe-inDesign/eyes-met-prototype-v1.indd` · PDFs → `Output/interiors/` + `Output/covers/`.  
**Print finals:** **2625×2625** / **5250×2625** = full **300 DPI** (Pass B remake; dial may be smaller). No fake gutter on plates.  
**Photoshop MCP LIVE:** adobepy UXP (`:47391`/`:8766`) — COM rejected; agent can drive PS for MOCK/chops. Doc: `tools/layout-mcp/PHOTOSHOP-SETUP.md`.  
**PSD blanks:** `spread` / `single-page` / `book-covers` templates in `Xtraz/Adobe-Photoshop/` (cyan TRIM · magenta SAFETY · orange MOCK). **No** spine-only PSD — Lulu sets spine after interior upload.  
**Tomorrow:** (1) one-page design → InDesign (2) poem storyboard real imagery (3) PS solo-layer + chop export tests.  
**Playbook:** `ISSUES-RESOLVED.md` (PSD blanks + chopz→InDesign + PS MCP) + `BOOK-PRODUCTION-SYSTEM.md`.

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

### 0. Do **not** re-research print from scratch
Read **`RESEARCH-VERDICT.md`** — Lulu primary, KDP HC skipped, timeline locked.

### 1. Beat gap → approval sprint (print path)
1. Open `Media/approved/INDEX.md` + `PAGE-PROMPT-BIBLE.md`.
2. For each beat **1–15**: mark **keeper candidates** already in `style-refs/` vs **missing / weak**.
3. **Pick cover** A–E (`style-refs/covers/` + `back/`) → copy winners to Tier B `covers/cover-front.png` + `cover-back.png`.
4. For missing/weak beats: Klein 4B dial → Jon pick → Banana `/edit` + style-refs finals → promote to Tier B `pages/` / `spreads/`.
5. Thin beats to fill first: **3, 5, 8–10, 14** (and re-check any near-keeper that isn’t heirloom-final).

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
