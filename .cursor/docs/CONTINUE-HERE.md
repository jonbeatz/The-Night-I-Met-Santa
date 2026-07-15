# CONTINUE HERE — The Night I Met Santa

**Read this first after TRUTH + START-HERE.**  
Project root: `D:\Hermes\projects\The-Night-I-Met-Santa`  
Operator: Jon · Gift for **Jack Farrell** · Birthday **2026-08-15**

---

## One-line status (2026-07-15)

**G2 locked:** 32 pages · 5 cinematic spreads · About + Thank You Draft A locked.  
**Look locked:** painted gouache (not colored pencil) — `ILLUSTRATION-STYLE.md` · story keepers `Media/generated/test-batch-v2/`.  
**Covers:** `Media/generated/test-covers-v3/` — 5 titled front+back sets (Jon: spectacular; pick pending).  
**Playbook:** **`.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`** — tools, decisions, recreate-for-future-books (§9 model recipe).  
**Image lanes locked:** dial **Klein 4B** (~$0.01) → fallback **Qwen Image 2** (~$0.035) → finals **Banana `/edit` + refs** (~$0.15). Evidence: `Media/generated/model-compare-beat01/`. Ideogram skipped.  
**Full book art:** `Media/generated/test-batch-v3/` (32-page map + `reading-order/` + text/wash mocks).  
**Text overlay:** Jon mockup refs (`ref-text-jon-*.png`) · policy doc · mocks `text-mocks-v3/` (still refine before compositor ship).  
**Next:** review `text-mocks-v3` → golden page → rewrite `composite_pages.py` · pick cover · promote keepers.
---

## What we are building

An **8.5×8.5"** full-color children’s picture book from Jack’s Christmas poem *The Night I Met Santa*, illustrated in **painted gouache / soft watercolor** (Golden Age / Santore–adjacent — **not** colored pencil), printed as **1 hardcover gift** (Lulu), possibly more later.
Target printer: **[Lulu](https://www.lulu.com/)** — supports exact 8.5×8.5 casewrap hardcover, single copy OK.

---

## Folder map (canonical)

| Path | Role |
|------|------|
| `Transcription/poem-clean.txt` | Poem text of record |
| `Media/` | Scene + cover illustrations (keep; refine as needed) |
| `Images/references/` | Jack photos + Christmas book style refs |
| `Images/references/layout/` | **Jon’s layout north stars** (phone photos) |
| `Pages/` | Pre-composited poem page JPEGs (currently **empty** — rebuild) |
| `Output/` | Final interior + cover PDFs (currently **empty** — rebuild) |
| `composite_pages.py` | Pillow page compositor (rewrite wash logic next) |
| `book-final.typ` | Typst binder for front matter + `Pages/*.jpg` |
| `build_cover*.py` | Wrap cover builders |
| `Book-Findings.md` | Full research + failed iteration log |
| `_archive/layout-attempts/` | Rejected Typst v2–v4 sources (do not revive blindly) |
| `.cursor/docs/book/` | Preview PNGs + small v3/v4 PDF samples |

**Do not** put working art under `.cursor/assets/` — root `Media/` / `Pages/` / `Output/` only.

---

## Layout north star (Jon’s photos)

1. **`Images/references/layout/ref-overlay-cloud-text.png`**  
   Full-bleed art + soft irregular **translucent cloud/panel** under black text; short white lines OK on dark sky.

2. **`Images/references/layout/ref-spread-bleed-text.png`**  
   Left page mostly text/paper; illustration **bleeds in** from the right with painterly feathered edge.

**Rejected:** hard white boxes (v3), Typst PNG alpha checkerboards (v4), soft cream **rectangles** that still feel like boxes (v5).

**Engineering rule:** Pre-composite in **Pillow** (flat JPEG) → Typst only places images / front matter. Never stack transparent PNGs in Typst over full-page art.

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
Read **`RESEARCH-VERDICT.md`** — Lulu primary, KDP HC skipped, GitHub LaTeX links graded, timeline locked.

### 1. Confirm layout mode with Jon (30 seconds)
Default if no answer: **cloud-overlay on full-bleed art** (ref-overlay-cloud-text).  
Alt: left-text / right-bleed spread (ref-spread-bleed-text). Mix OK.

**Style (locked default):** `.cursor/docs/ILLUSTRATION-STYLE.md` — painted gouache, NOT colored pencil · refs in `test-batch-v2/_style-refs/`  
**Full playbook (recreate later):** `.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`  
**Per-page image prompts:** `.cursor/docs/PAGE-PROMPT-BIBLE.md` (stanza → fal prompt; text after)  
**Cover dial-in:** `.cursor/docs/COVER-PROMPTS.md` · sets in `Media/generated/test-covers-v3/`
### 2. Quiet-zone map
For each `Media/scene-*.png`, note where text can sit without covering faces.

### 3. Rewrite `composite_pages.py` (main build work)
- Soft **elliptical / irregular cloud** alpha (~50% cream), Gaussian blur  
- Poem text (Georgia or similar)  
- One **sample page** → Jon approves → batch all stanzas to `Pages/`

### 4. Typst front matter + export
`book-final.typ` → `Output/*-INTERIOR.pdf` (even page count).

### 5. Cover + Lulu
Spine from page count → `build_cover_v2.py` → Lulu upload. Proof by **~July 25–28**.

### Optional later (not blocking gift)
Affinity Publisher polish · fal style-lock · Lulu upload runbook skill · more copies via Mixam

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

# After art approved: Pillow overlay (text on cloud) then Typst and/or img2pdf
npm run book:composite
npm run book:typst
npm run book:pdf:doctor
npm run book:pdf:from-pages    # lossless Pages/*.jpg → Output/*-img2pdf.pdf
npm run book:pdf:verify        # pikepdf MediaBox QA
npm run book:pdf:verify:boxes  # write TrimBox/BleedBox for Lulu
```

Presets: **page** = 2625×2625 · **spread** = 5250×2625 · **cover** = 2048² draft  
Text is applied **after** art lock via `composite_pages.py` (cloud overlay → flat JPEG).  
Prepress: **img2pdf** + **pikepdf** IN USE (`requirements-book.txt`).

---

## Agent handshake

On Open Project / first message in this workspace:

> Ok Jon — The-Night-I-Met-Santa profile loaded, ready.

Then read: `TRUTH.md` → this file → `RESEARCH-VERDICT.md` → `ReCall.md` → `BOOK-PLAN.md`.
