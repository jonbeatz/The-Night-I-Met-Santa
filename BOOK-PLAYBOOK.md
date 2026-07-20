# BOOK-PLAYBOOK.md — Complete Picture Book Production System

**Purpose:** A single document that enables starting ANY new children's picture book from scratch, using everything learned from *The Night I Met Santa* project.
**Designed for:** Hermes AI agent + human operator (Jon). Read this → build a book.
**Based on:** `D:\Hermes\projects\The-Night-I-Met-Santa` (the full project, not a summary)

> **2026-07-19 update (TNIMS):** Layout production for *this* title is **InDesign UXP** (`AGENT-RUNBOOK.md`). Pillow → Typst remains documented below as the **fallback / portable** recipe for future books without DTP. Prefer InDesign when Affinity/InDesign MCP cold-start is available. Page target for TNIMS: **35–40** (not the earlier ~32 estimate).

---

## 0. What This System Produces

An **8.5 × 8.5" square, full-color, illustrated children's picture book**, printed as a hardcover gift via Lulu print-on-demand, with:
- AI-generated painted gouache/watercolor illustrations (15+ scenes)
- Organic text overlay integrated into the art (not separate text pages)
- Professional wrap-around cover with spine
- Print-ready PDF with correct bleed, trim, and safety zones
- Proof copy delivered within ~2 weeks

**Total cost:** ~$25–40 for 1 hardcover proof (Lulu) + ~$5–15 in AI image generation credits (fal.ai)

---

## 1. Project Skeleton (What to Create)

### Bootstrap from the shared library

```powershell
powershell -File D:\Hermes\projects\_core-scripts\shared-profile-content\scripts\bootstrap-new-project.ps1 `
  -ProjectName "MyNewBook" `
  -ProjectRoot "D:\Hermes\projects\MyNewBook" `
  -ProjectSlug "mynewbook" `
  -ProjectDesc "A children's picture book"
```

This creates the standard Hermes sibling project structure with all shared skills, rules, prompts, docs, and MCP config.

### Essential folders (create these)

```
MyNewBook/
├── Audio/                  # Original recordings
├── Transcription/           # Cleaned poem/manuscript text
├── Images/references/       # Author photos, style refs, book layout refs
├── Images/references/style/ # Style north-star images
├── Images/references/layout/ # How text should sit on art (REFERENCE PHOTOS)
├── Media/                   # Working / legacy promoted illustrations
├── Media/approved/          # TWO-TIER keepers (git-tracked) — see INDEX.md
│   ├── style-refs/          # Tier A moodboard (covers/back/jack/pages/santa/spread/story)
│   ├── characters/          # Tier B print locks (people)
│   ├── covers|pages|spreads/# Tier B print locks (clean kebab names)
├── Media/generated/         # Experimental batches (test-batch-vN/, test-covers-vN/)
├── Xtraz/Fonts/             # Local OFL font pack (gitignored) — document in FONT-CATALOG.md
├── Pages/                   # Pre-composited print-ready JPEGs
├── Output/                  # Final interior + cover PDFs
├── _archive/                # Rejected experiments — do not auto-revive
└── .cursor/docs/            # All plans, prompts, and playbook docs
```

**Approved two-tier rule:** `style-refs/` = browsable favorites; `characters|covers|pages|spreads` = compositor/Typst source of truth after Jon says “lock.”

### Essential docs (create these)

| Doc | Purpose |
|-----|---------|
| `TRUTH.md` | Project constitution — what this IS and ISN'T |
| `.cursor/docs/START-HERE.md` | Daily ops, handshakes, session rituals |
| `.cursor/docs/CONTINUE-HERE.md` | Session resume — what's done, what's next |
| `.cursor/docs/BOOK-PRODUCTION-SYSTEM.md` | Reusable playbook (copy from this project) |
| `.cursor/docs/ILLUSTRATION-STYLE.md` | Locked art style, master prompt blocks, north stars |
| `.cursor/docs/TEXT-OVERLAY-POLICY.md` | How poem text sits on art (zones, rules, paint recipe) |
| `.cursor/docs/PAGE-PROMPT-BIBLE.md` | Every story beat → exact image prompt |
| `.cursor/docs/COVER-PROMPTS.md` | Cover generation prompts and title treatment |
| `.cursor/docs/BOOK-PLAN.md` | Specs, stanza map, print checklist |
| `RESEARCH-VERDICT.md` | POD comparison, GitHub grades, toolchain decisions |
| `Book-Findings.md` | Failed iterations log — what NOT to do |
| `BOOK-PLAYBOOK.md` | This file — complete system for future books |
| `.cursor/docs/FONT-CATALOG.md` | OFL font options + recommended cover/poem roles |

> Living day-to-day ops for *this* title also live in `.cursor/docs/BOOK-PRODUCTION-SYSTEM.md` — keep both in sync when a decision sticks.

---

## 2. Tools to Install

### Required (install before starting)

```powershell
# Book layout engine (10x faster than LaTeX, modern syntax)
winget install typst                    # → typst 0.15.0+

# Universal document converter
winget install JohnMacFarlane.Pandoc    # → pandoc 3.10+

# Python packages (into Hermes venv)
pip install pymupdf                     # PDF manipulation, text extraction
pip install cairosvg                    # SVG rendering (optional — needs libcairo)
uv pip install nano-pdf                 # NL PDF metadata editing
```

**Already installed in Hermes venv (verify):**
- `Pillow` — image compositing, text rendering
- `pypdf` — PDF merging, metadata
- `Jinja2` — HTML templating (optional)

### Skipped (don't waste time on these)

| Tool | Why Skip |
|------|----------|
| WeasyPrint | Needs GTK3 runtime on Windows — DLL dependency hell |
| LaTeX (MikTeX) | Wrong tool for full-bleed picture books; slow; complex |
| Scribus | GUI-only; not agent-automatable for bulk page generation |
| Affinity Publisher | ~$70; only if Jon buys it for manual polish pass |

---

## 3. Image Generation Pipeline

### Locked model lanes (from cost + quality testing)

| Priority | Model | Endpoint | ~Cost | When to Use |
|:--------:|-------|----------|------:|-------------|
| 1 | FLUX.2 Klein 4B | `fal-ai/flux-2/klein/4b` | ~$0.01/image | Default iterate — layout, vibe, text-zone probes |
| 2 | Qwen Image 2 | `fal-ai/qwen-image-2/text-to-image` | ~$0.035/image | Fallback when Klein misses the vibe |
| 3 | Nano Banana Pro /edit | `fal-ai/nano-banana-pro/edit` + refs | ~$0.15/image | Finals — approved pages/covers after dial |

**Skipped:** Ideogram V3/V4 (safety filter blocks Christmas child storybook scenes)

### How to prove a lane (do this once per book)

1. Pick ONE real story beat
2. Generate the same prompt through all 3 models
3. Save to `Media/generated/model-compare-beat01/`
4. Jon picks the winners → that becomes the lane lock for the book

### Prompt anatomy (reusable formula)

```
[SCENE: who, what, where, light, composition]
[QUIET ZONE: leave soft open area for later text — specify corner/side]
[STYLE: master block from ILLUSTRATION-STYLE.md]
[NEGATIVES: colored pencil, photoreal, text, letters, watermark, cartoon, CGI; for spreads also: fake gutter, center fold line, spine shadow, binding crease]
```

### Image sizes (at 300 DPI for 8.5×8.5" with bleed)

| Type | Dimensions | Aspect |
|------|-----------|--------|
| Single page | 2625 × 2625 px | 1:1 |
| Spread (cinematic) | 5250 × 2625 px | 2:1 → split L/R |
| Cover (wrap) | Per Lulu template after page count | Varies |

---

## 4. Art Style Lock

### Default aesthetic (one line)

> Heavily painted gouache / soft watercolor storybook — **NOT** colored pencil, **NOT** photoreal, **NOT** cartoon flat.

### Master style block (paste into every image prompt)

```
Traditional children's Christmas picture-book illustration, heirloom storybook quality, heavily painted in rich gouache and soft watercolor with visible soft brushstrokes and gentle blended edges, NOT colored pencil NOT crayon NOT scratchy sketch lines, warm fireplace glow mixed with cool moonlight, golden ember highlights, deep crimson and forest green palette with warm cream and muted earth tones, nostalgic Golden Age painted realism, intimate cozy magical atmosphere, Charles Santore–inspired storybook painting, classic Clement C. Moore Christmas book feel, highly detailed but soft and painterly, print-ready square page composition, no text, no letters, no watermark
```

### Negative block (what to REJECT)

```
colored pencil, crayon, scratchy sketch, pencil hatching, dry pastel sketch texture,
text, words, letters, typography, title, caption, watermark, logo, signature,
vector art, flat design, thick black outlines, cartoon sticker, comic book ink,
anime, manga, chibi, 3D CGI, Unreal Engine, plastic skin, photoreal photograph,
neon colors, cyberpunk purple, harsh flash lighting, cluttered composition,
modern UI, phone in frame, low detail, blurry faces
```

### North-star references (from The Night I Met Santa)

Keep 2–3 approved frames as style-ref uploads for future finals (also mirrored under `Media/approved/style-refs/`):
- Eyes-met spread — `Media/approved/style-refs/spread/style-spread-06-eyes-met.png` (or wide master)
- Peek/doorway — `Media/approved/style-refs/pages/style-sneak-02.png`
- Soft-painted Santa — `Media/approved/style-refs/santa/style-santa-01.png`

---

## 4b. Typography (fonts)

Pack lives under `Xtraz/Fonts/` (**gitignored**; install on the machine). Catalog: `.cursor/docs/FONT-CATALOG.md`.

| Role | Recommended |
|------|-------------|
| Poem body | **Cormorant Garamond** (alt: EB Garamond) |
| Cover title | **Cinzel Decorative** (alt: Mountains of Christmas) |
| Dedication / flourish | Allura · Great Vibes · Pinyon Script |
| Web flipbook UI only | Cabin · Quicksand |

Do **not** use Fredoka / Six Caps for long poem text. Prefer static TTFs in Pillow/Typst over variable fonts for print predictability.

---

## 5. Layout System (The Hard Part — Read Carefully)

### What NOT to do (all rejected)

| Approach | Tool | Problem | Verdict |
|----------|------|---------|---------|
| Separate text/image pages | fpdf | Feels like a textbook, not a picture book | ❌ |
| Hard white text boxes | Typst | Looks glued-on/scrapbook | ❌ |
| PNG wash overlays | Typst | PDF eats alpha → checkerboard transparency | ❌ |
| Soft cream rectangles | Pillow | Still rectilinear — not organic enough | ❌ |
| AI-generated "transparent" washes | FAL → Typst | FAL doesn't make true transparency; Typst PDF can't preserve alpha | ❌ |

### What TO do (engineering pattern)

**Pre-composite in Pillow → flat JPEG → Typst places images only (no layering)**

1. Illustration + text are baked into ONE flat JPEG per page using Pillow
2. Text sits on a soft organic cloud/paint-fade wash (not a rectangle)
3. Typst is used ONLY for front matter (half-title, title, copyright, dedication, author, closing)
4. Poem pages are pre-rendered JPEGs — Typst does `image("Pages/page-NN.jpg")` only

### Text overlay recipe (Pillow)

```python
# Paint-fade wash
color = (255, 250, 242)      # Warm white/ivory
opacity = 0.45–0.65           # Semi-transparent
blur = 80–160 px              # Gaussian-like feathered edge
shape = elliptical cloud       # NOT rectangle — organic irregular edge

# Text
font = "Cormorant Garamond"   # Prefer over Georgia — see FONT-CATALOG.md
size = 46–48 pt               # At 300 DPI
color = (26, 26, 26)          # Near-black
leading = 0.55 em             # Line spacing
```

### Text placement rules (TEXT-OVERLAY-POLICY)

| Rule | Detail |
|------|--------|
| Never cover faces | Child or Santa — or hero features (hands, note, eyes-meet) |
| Legibility first | Text sits on a soft white/ivory paint fade strong enough to read |
| Edges must fade | Smooth gradient — not a standout blob with hard outline |
| Use open design areas | Walls, side panels, bottom corners, side-bleeds |
| Placement per scene type | Busy figure left → text bottom-right; peek/doorway → left side bleed; dark halls → light ink with little wash |

### Preferred placements (from Jon's mockup feedback)

| Situation | Zone | Wash Type |
|-----------|------|-----------|
| Open cream wall (eyes-met left) | Upper/mid left wall | Soft corner fade or none if wall already light |
| Busy figure on left (Santa right page) | Bottom-right quiet area | White gradient from BR corner toward figure |
| Peek / doorway scenes | Left side bleed | Long soft vertical paint bleed |
| Note / chair pages | Lower quiet band/corner | Soft mist — not mid-window |
| Dark hall walls | Left dark wall | Light ink, little/no white wash |

---

## 6. Cover Design

### Specs

| Element | Detail |
|---------|--------|
| Format | Wrap-around (front + spine + back) |
| Dimensions | 17.33 × 8.75" at 300 DPI (for 8.5×8.5" book) |
| Bleed | 0.125" on all sides |
| Front | Full-bleed illustration + gold title + author name |
| Spine | Deep red with vertical gold text: "TITLE — AUTHOR" |
| Spine width | Calculated from page count: `sheets = pages/2; spine = max(0.08", sheets × 0.004")` |
| Back | Companion illustration + book description text |

### Cover rules

- Flat poster only — never 3D book mockup
- Title exactly: book title
- Credit exactly: `Written By <Author>`
- Prefer ornate gold display serif + flourishes
- Back cover: no baked blurb text preferred — leave soft empty region for ISBN/blurb later
- If AI can't spell the title correctly → use `build_cover_v2.py` to composite type in Pillow

---

## 7. Print Production

### Primary printer: Lulu

| Spec | Value |
|------|-------|
| URL | [lulu.com](https://www.lulu.com) |
| Trim | 8.5 × 8.5" square |
| Binding | Casewrap hardcover (gift) or paperback (proof) |
| Paper | Premium Color (heavier stock for heirloom feel) |
| Color | sRGB export (NOT CMYK-first — Lulu printers convert sRGB natively) |
| Min pages | 24 for HC |
| Cost (1 copy) | ~$25–40 HC + shipping |
| Proof timeline | Order ~2–3 weeks before deadline |

### Other printers (backup / future)

| Printer | Strengths | Limitations |
|---------|-----------|-------------|
| Mixam | 8.5×8.5 HC available | Min 25 copies |
| Blurb | Premium paper, photo books | Usually 7×7" square (resize needed) |
| IngramSpark | Bookstore/library distribution | Overkill for 1 gift |
| Amazon KDP | Free Amazon listing | NO 8.5×8.5 hardcover (PB only) |
| PrintNinja | Offset quality | Min 250 copies |

### Print-ready checklist (before uploading)

- [ ] Even page count (24–40)
- [ ] 300 DPI images throughout
- [ ] 0.125" bleed on full-bleed pages
- [ ] All text faces ≥ 0.5" from trim edge
- [ ] No critical faces on absolute center fold
- [ ] Interior PDF = single multi-page file; odd pages = right
- [ ] Cover PDF = separate wrap file (download Lulu template after page count is final)
- [ ] Color: sRGB (not CMYK)
- [ ] Flattened — no live transparency stacks
- [ ] Order 1 physical proof before any multi-copy run

---

## 8. Book Structure (32-Page Template)

### Front matter (pages 1–8)

| Page | Content |
|------|---------|
| 1 | Half-title (book title only) |
| 2 | Blank |
| 3 | Full title page (title + author + "Illustrations created with AI" + "First Edition, YEAR") |
| 4 | Copyright / colophon |
| 5 | Dedication ("For my family, with love. — Author") |
| 6 | Blank or illustration |
| 7 | About the Author (portrait + bio paragraph) |
| 8 | Blank or illustration |

### Body (pages 9–28) — varies by poem length

Pattern: 1 stanza = 1 page (full-bleed illustration with integrated text)
Aim for 15–20 poem pages to fill the body.

### Back matter (pages 29–32)

| Page | Content |
|------|---------|
| 29 | Closing page (key quote from the story) |
| 30 | Blank |
| 31 | Final message / "God bless" / author sign-off |
| 32 | Blank |

---

## 9. Full Workflow (Step by Step)

```
[1]  Poem/manuscript → Transcription/poem-clean.txt
[2]  Style direction → ILLUSTRATION-STYLE.md (lock north stars)
[3]  Layout reference photos → Images/references/layout/ (Jon's phone photos of real books)
[4]  Beat map → PAGE-PROMPT-BIBLE.md (every story beat → exact prompt)
[5]  Prove model lanes → Media/generated/model-compare-beat01/ (same prompt, 3 models)
[6]  Lock lanes → BOOK-PRODUCTION-SYSTEM.md §2
[7]  Seed style refs → 2–3 approved painted frames
[8]  Generate art batches → Media/generated/test-batch-vN/ (scene illustrations)
[9]  Generate cover batches → Media/generated/test-covers-vN/ (front+back sets)
[10] Jon reviews → promote to `Media/approved/style-refs/` (moodboard) then **lock** winners into `characters|covers|pages|spreads`
[11] Write TEXT-OVERLAY-POLICY.md from Jon's mockup feedback
[12] Quiet-zone map per illustration (where text won't cover faces)
[13] Rewrite composite_pages.py (cloud wash + text → Pages/*.jpg)
[14] Build one sample page → Jon approves → batch all stanzas
[15] Typst front matter + place page JPEGs → Output/*-INTERIOR.pdf
[16] Verify page count is even; spine width from page count
[17] Build cover → Output/*-COVER-*.pdf
[18] Upload interior PDF to Lulu → review print-ready preview
[19] Upload cover PDF to Lulu
[20] Order 1 physical proof → review → order gift copy
```

---

## 10. Commands Reference

```powershell
# Session management
npm run session:open                    # Resume — light probes only
npm run session:start -- -Full          # Cold boot — launch LM Studio + DeepSeek

# Image generation (fal.ai lanes)
npm run image:fal:page -- "<scene>. <MASTER STYLE>"
npm run image:fal:spread -- "<wide scene>. <MASTER STYLE>. seamless continuous spread, NO fake book gutter NO vertical fold line NO center spine shadow"
npm run image:fal:cover -- "<cover scene>. <MASTER STYLE>"

# Book assembly
npm run book:composite                  # Pillow: art + wash + text → Pages/*.jpg
npm run book:typst                      # Typst: front matter + Pages → PDF
npm run book:pdf:verify                 # Check print-readiness
npm run book:pdf:verify:boxes           # Apply TrimBox/BleedBox for Lulu

# PDF utilities
npm run book:pdf:from-pages             # img2pdf: Pages/*.jpg → PDF (lossless)
npm run book:pdf:doctor                 # Prepress diagnostic
```

### Agent reality (which model to actually use)

- **Dial:** Klein 4B (~$0.01/image) for layout, vibe, text-zone probes
- **Fallback:** Qwen Image 2 (~$0.035) when Klein misses
- **Finals:** Nano Banana Pro /edit + style refs (~$0.15) for approved pages/covers
- Do NOT default to Flux schnell for dial (weaker than Klein for gouache storybook look)

---

## 11. Rejection List (What NOT to Do — Hard-Won)

| Don't | Why | Where Documented |
|-------|-----|------------------|
| Use LaTeX for picture books | Wrong tool; slow; can't do full-bleed well | RESEARCH-VERDICT.md |
| Stack transparent PNGs in Typst over art | PDF eats alpha → checkerboard | v4 failure |
| Use hard white text boxes | Looks glued-on, not storybook | v3 failure |
| Use soft cream rectangles | Still feels like a box, not organic | v5 failure |
| Generate text IN the image | AI misspells; text overlay is Pillow's job | ILLUSTRATION-STYLE.md |
| Use WeasyPrint on Windows | GTK3 DLL dependency hell | Book-Findings.md §2 |
| Use Ideogram for child Christmas scenes | Safety filter blocks pajamas scenes | BOOK-PRODUCTION-SYSTEM.md §2 |
| Default to Flux schnell for dial | Weaker than Klein 4B for gouache style | Model compare beat01 |
| Put critical faces on center fold | Gutter swallows detail | BOOK-PLAN.md |
| Export CMYK for Lulu | Lulu converts sRGB natively; CMYK-first can hurt color | RESEARCH-VERDICT.md |
| Use Amazon KDP for square hardcover | KDP doesn't offer 8.5×8.5 HC | RESEARCH-VERDICT.md |
| Let AI bake title/author into cover art | AI misspells names; composit type in Pillow | Cover rules |

---

## 12. What to Swap for a New Book

| Keep (universal) | Swap (per book) |
|------------------|-----------------|
| Folder structure + skeleton | Poem/manuscript text |
| Tool stack (Typst, Pillow, pypdf, Pandoc) | Trim size (if not 8.5×8.5) |
| Image lanes (Klein → Qwen → Banana) | Style refs + ILLUSTRATION-STYLE.md |
| Layout pattern (Pillow cloud pre-composite → Typst binder) | Cover title + author name |
| Print specs (bleed, safety, 300 DPI, sRGB) | About/Thank You copy |
| Text overlay rules (faces, zones, paint recipe) | Character sheets |
| POD research (Lulu primary; others backup) | Deadline |
| Prompt anatomy + negative block | Page count + spread count |
| Rejection list | — |

---

## 13. Cost Estimate (per book)

| Item | ~Cost |
|------|-------|
| Image generation (fal.ai) | $5–15 (depends on finals count) |
| Lulu proof paperback | ~$4.50 + shipping |
| Lulu gift hardcover | ~$25–40 + shipping |
| Tools | $0 (all free/open source) |
| **Total** | **~$35–60** |

---

## 14. Timeline Template

| Phase | Duration | What |
|-------|----------|------|
| Research + style lock | 1–2 days | Reference photos, style north stars, model lane proof |
| Art generation | 2–4 days | Batch scenes + covers, Jon review, promote keepers |
| Layout + text overlay | 2–3 days | Quiet-zone map, composite_pages.py, sample → approve → batch |
| PDF assembly | 1 day | Typst binder, cover build, prepress verify |
| Lulu proof | 7–10 days | Upload → order → receive physical proof |
| **Total** | **~3 weeks** | Buffer 1 extra week for reprints |

---

*Generated from `D:\Hermes\projects\The-Night-I-Met-Santa` — the complete working project.*
*Last updated: 2026-07-15 (Media/approved two-tier + FONT-CATALOG)*
