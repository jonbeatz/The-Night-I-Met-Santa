# CONTINUE HERE — The Night I Met Santa

**Read this first after TRUTH + START-HERE.**  
Project root: `D:\Hermes\projects\The-Night-I-Met-Santa`  
Operator: Jon · Gift for **Jack Farrell** · Birthday **2026-08-15**

---

## One-line status (2026-07-15 late night)

**Page-by-page production** (Jon direction) — Klein full-book batches (`test-book-v1` / `v2`) **rejected** as layout feel; too samey / not usable.  
**Do not** batch-generate the whole book on Klein again for approval.  
**Process:** one page (or one open L→R) at a time · **Lane B Gemini / Banana finals** + locked G0s · Jon approve → next.  
**Locks still good:** cover beige-v2 · boy G0 (style-match-A) · santa-G0 (paint north star) · Jack portrait (style-match-B) · eyes-met FINAL-TEST-A.  
**Next:** pick first interior page with Jon · recommend **S01 Approach LEFT** (or re-lock eyes-met open if preferred).

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
| **`Media/approved/`** | **Two-tier keepers** — `style-refs/` moodboard · Tier B locks — see `INDEX.md` |
| `Xtraz/Fonts/` | Local OFL pack (gitignored) — roles in `FONT-CATALOG.md` |
| `BOOK-PLAYBOOK.md` | Future-book master playbook (repo root) |
| `Media/generated/` | Experiments / batches (not the source of truth for “what we picked”) |
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
Read **`RESEARCH-VERDICT.md`** — Lulu primary, KDP HC skipped, timeline locked.

### 1. Beat gap → approval sprint (print path)
1. Open `Media/approved/INDEX.md` + `PAGE-PROMPT-BIBLE.md`.
2. For each beat **1–15**: mark **keeper candidates** already in `style-refs/` vs **missing / weak**.
3. **Pick cover** A–E (`style-refs/covers/` + `back/`) → copy winners to Tier B `covers/cover-front.png` + `cover-back.png`.
4. For missing/weak beats: Klein 4B dial → Jon pick → Banana `/edit` + style-refs finals → promote to Tier B `pages/` / `spreads/`.
5. Thin beats to fill first: **3, 5, 8–10, 14** (and re-check any near-keeper that isn’t heirloom-final).

### 2. Quiet-zone map (after Tier B art locks)
For each locked page/spread, note where text sits without covering faces (policy: `TEXT-OVERLAY-POLICY.md`).

### 3. Rewrite `composite_pages.py` (main build work)
- Soft **elliptical / irregular cloud** alpha (~50% cream), Gaussian blur  
- Poem text: **Cormorant Garamond** (see `FONT-CATALOG.md`; Georgia OK fallback)  
- One **sample page** → Jon approves → batch all stanzas to `Pages/`

### 4. Typst front matter + export
`book-final.typ` → `Output/*-INTERIOR.pdf` (even page count). Place Jack portrait on About / Thank You.

### 5. Cover + Lulu
Spine from page count → `build_cover_v2.py` (Cinzel for title) → Lulu upload. Proof by **~July 25–28**.

**Docs:** `BOOK-PRODUCTION-SYSTEM.md` · `BOOK-PLAYBOOK.md` · `PAGE-PROMPT-BIBLE.md` · `COVER-PROMPTS.md` · `FONT-CATALOG.md`

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
