# Book-Findings.md — "The Night I Met Santa"

Research, tools, development process, and printing services for Jack Farrell's Christmas poem book.
Project folder: `D:\Hermes\projects\The-Night-I-Met-Santa\`  
(Moved from `F:\My Projects\Dad\The-Night-I-Met-Santa` on 2026-07-14)

---

## 1. Research: Children's Book Layout Standards

### Professional Conventions (from IngramSpark 2026 guide)
- **Trim sizes:** 8.5×8.5" square (recommended), 8×10", 10×8", 8×8"
- **Page count:** 32 pages minimum; 32–40 is industry sweet spot for picture books
- **Margins:** 0.5" minimum all sides
- **Bleed:** 0.125" beyond trim on all edges
- **No content on inside covers**
- **For poetry books:** poem-on-left / illustration-on-right is classic; full-spread illustrations with integrated text is premium

### Reference Sources
- IngramSpark PDF File Creation Guide (42 pages, extracted via vision analysis)
- Lulu.com help center and toolkit
- CTAN (LaTeX package archive)

---

## 2. Tools Installed

### Working ✅

| Tool | Version | Purpose | How Installed |
|---|---|---|---|
| **Typst** | 0.15.0 | Modern LaTeX alternative — book layout engine | `winget install typst` |
| **Pandoc** | 3.10 | Universal doc converter (Markdown → PDF, EPUB, DOCX) | `winget install JohnMacFarlane.Pandoc` |
| **PyMuPDF (fitz)** | 1.28.0 | PDF manipulation, text extraction, page counting | `pip install pymupdf` (to Hermes venv) |
| **pypdf** | 6.14.2 | PDF splitting, merging, metadata | Already installed |
| **Pillow** | 12.2.0 | Image compositing, text rendering, bleed calculation | Already installed |
| **Jinja2** | 3.1.6 | HTML templating | Already installed |
| **nano-pdf** | 0.2.1 | Natural language PDF title/metadata editing | `uv pip install nano-pdf` |
| **CairoSVG** | 2.9.0 | SVG rendering (installed but not used — needs libcairo) | `pip install cairosvg` |

### Installed but Skipped ❌

| Tool | Issue |
|---|---|
| **WeasyPrint** | Needs GTK3 runtime on Windows — DLL hell. Not worth the pain. |
| **CairoSVG** | Needs libcairo-2.dll — same GTK dependency issue. |
| **nano-pdf** | CLI works but Python import fails in venv. |

### Key Decision
**Typst** replaces both WeasyPrint and LaTeX. It's 10x faster, has modern syntax, handles full-bleed images, custom fonts, and precise typography. One `winget install` away. No dependency hell.

---

## 3. Available Hermes Skills (for Book Design)

| Skill | Relevance | How Used |
|---|---|---|
| **`image_generate`** (FAL FLUX 2 Klein 9B) | ⭐⭐⭐⭐⭐ | Generated 6 new book illustrations + cover art + watercolor washes |
| **`comfyui`** | ⭐⭐⭐⭐⭐ | Local illustration generation at `H:\AI_Models\ComfyUI :8188` |
| **`claude-design`** | ⭐⭐⭐⭐ | HTML prototype spreads before committing to PDF |
| **`nano-pdf`** | ⭐⭐⭐⭐ | Final PDF metadata polish |
| **`design-md`** | ⭐⭐⭐⭐ | Formal DESIGN.md for book's visual identity |
| **`google-workspace`** | ⭐⭐⭐⭐ | Upload PDFs to Google Drive for review |
| **`powerpoint`** | ⭐⭐⭐ | Book proposal / pitch decks |
| **`excalidraw`** | ⭐⭐ | Page layout diagrams |
| **`popular-web-designs`** | ⭐⭐ | Cover color palette inspiration |

---

## 4. GitHub Repos Found

### Book Templates
- **[talal/ilm](https://github.com/talal/ilm)** (⭐231) — Typst non-fiction book template
- **[flavio20002/typst-orange-template](https://github.com/flavio20002/typst-orange-template)** (⭐150) — Legrand Orange Book in Typst
- **[peterfriese/eightbyten](https://github.com/peterfriese/eightbyten)** — Tufte-style book template for Typst
- **[zsudo/medievalMurderMistery](https://github.com/zsudo/medievalMurderMistery)** — LaTeX medieval children's book template

### PDF Automation
- **[tilacog/booklet-imposition](https://github.com/tilacog/booklet-imposition)** — Python booklet imposition with bleed + signature support
- **[YUSAKRU/bindery-desktop](https://github.com/YUSAKRU/bindery-desktop)** — A4 → booklet imposition sheets
- **[opd-ai/bookie](https://github.com/opd-ai/bookie)** — Markdown → professional PDF books (Go)

### AI-Assisted Book Creation
- **[darshil0/colorjoy-ai](https://github.com/darshil0/colorjoy-ai)** — AI children's coloring book generator
- **[Ming-H/tech-book-generator](https://github.com/Ming-H/tech-book-generator)** — Markdown → HTML/PDF with layouts

---

## 5. Development Process & Iterations

### Phase 1: Audio → Text
- Dad's WAV file transcribed using Whisper (local, on VADER's RTX 5060 Ti)
- Output: `Transcription/poem-clean.txt` — 15 stanzas, 77 lines

### Phase 2: Initial Illustrations (Session 1 — July 14 morning)
- Generated 10 illustrations via FAL Flux + ComfyUI
- Style: Traditional children's Christmas book, painterly gouache/watercolor, Charles Santore / Golden Age feel
- 3 author portrait variants of Jack Farrell at different ages
- Files: `Media/scene-01` through `scene-10`, covers, portraits

### Phase 3: First Book Build (v1)
- **Tool:** fpdf (Python)
- **Layout:** Text on left page, illustration on right page
- **Issues:** Basic PDF quality, 6 stanzas missing art, no professional typography
- **Output:** `Output/The-Night-I-Met-Santa-INTERIOR.pdf` (35 pages, 20 MB)

### Phase 4: Research & Tool Installation
- Researched professional children's book standards
- Installed Typst, Pandoc, PyMuPDF, CairoSVG, nano-pdf
- WeasyPrint skipped (GTK3 dependency hell on Windows)
- Full POD service comparison completed

### Phase 5: Typst Layout v2
- **Tool:** Typst 0.15.0
- **Layout:** Text page → Illustration page → repeat (40 pages)
- **Issue:** Text rendered as literal "line line line" — Typst variable interpolation bug
- **Fix:** `[``line``]` → `[#line]`
- **Output:** `Output/The-Night-I-Met-Santa-INTERIOR-v2.pdf` (40 pages)

### Phase 6: Missing Illustrations (6 new)
- Generated 6 additional illustrations to cover all 15 stanzas:
  - `scene-02b-sneak-up-santa-LANDSCAPE.png` — Child peeking at Santa
  - `scene-06b-santas-stories-LANDSCAPE.png` — Santa telling stories
  - `scene-08b-the-dash-santa-gone-PORTRAIT.png` — Santa gone, child with camera
  - `scene-10b-the-flue-and-chair-PORTRAIT.png` — Looking up flue, note on chair
  - `scene-12b-tearing-open-PORTRAIT.png` — Tearing open letter
  - `scene-14b-what-he-wants-message-LANDSCAPE.png` — Santa writing + child reading

### Phase 7: Integrated Layout v3
- **Goal:** Text on illustration, not separate pages
- **Approach:** Full-bleed illustration with text in semi-transparent cream panel + gold border
- **Issue:** Hard square box looked wrong for a children's book
- **Output:** 24 pages

### Phase 8: Watercolor Washes v4
- **Goal:** Replace hard box with organic watercolor bleed
- **Approach:** Generated 5 watercolor wash textures, positioned per-page
- **Issue 1:** Washes had white backgrounds that blocked illustrations
- **Issue 2:** Typst PDF rendering doesn't handle PNG transparency correctly (checkerboard)
- **Attempted fix:** Converted washes to transparent PNGs via Pillow alpha processing
- **Result:** Still broken — PDF transparency layering unreliable

### Phase 9: Pre-Composited Pages v5 (Current)
- **Approach:** Pillow composites illustration + feathered wash + text into one flat JPEG per page
- **Method:** 30 concentric rectangles with decreasing opacity create 120px feathered edge
- **Advantage:** Zero transparency issues — one flat image per page, no layering
- **Output:** 24 pages, 20 MB PDF
- **Typst role:** Only used for front matter (half-title, title, copyright, dedication, author, closing) — poem pages are pre-rendered JPEGs

### Cover Design
- **Tool:** Pillow + Typst (v2 attempt), Pillow only (current)
- **Design:** Wrap-around cover (front + spine + back), 17.33×8.75" at 300 DPI
- **Front:** House lights + snowman illustration with gold title "The Night I Met Santa"
- **Spine:** Deep red with vertical gold text, width calculated from page count
- **Back:** Empty chair illustration with book description text
- **Paperback:** 0.080" spine | **Hardcover:** 0.205" spine

---

## 6. Print-On-Demand Services

### Comparison (for 1 copy, 8.5×8.5" square, ~24–40 pages, full color)

| Rank | Service | Paperback | Hardcover | Setup Fee | Best For | Link |
|---|---|---|---|---|---|---|
| 🥇 | **Lulu** | **~$4.45** | **~$13.27** | $0 | Cheapest proof, 8.5×8.5" ready | [lulu.com](https://www.lulu.com) |
| 🥈 | **Amazon KDP** | ~$4.50–$6 | ~$13.50–$17 | $0 | Amazon distribution, author copies | [kdp.amazon.com](https://kdp.amazon.com) |
| 🥉 | **IngramSpark** | ~$5–$8 | ~$14–$18 | $0 | Bookstore/library distribution | [ingramspark.com](https://www.ingramspark.com) |
| 4 | **Blurb** | ~$12–$18 | ~$20–$30 | $0 | Photo books, premium feel | [blurb.com](https://www.blurb.com) |
| ❌ | Mixam | Min 25 copies | Min 25 copies | N/A | Bulk only | [mixam.com](https://mixam.com) |
| ❌ | PrintNinja | Min 250 copies | Min 250 copies | N/A | Offset bulk only | [printninja.com](https://www.printninja.com) |

### Recommended Strategy
1. **Proof:** Lulu — 1 copy, ~$10–15 shipped
2. **Amazon listing:** KDP — free to list, print-on-demand
3. **Bookstore/libraries:** IngramSpark — wider distribution
4. **Bulk reprints:** Mixam at 25+ copies

### SaaS Design Tools (Not Automatable)
- **Reedsy Book Editor** — [reedsy.com](https://reedsy.com) — Free, professional book formatting
- **Atticus** — [atticus.io](https://atticus.io) — $147, cross-platform book formatting
- **Scribus** — [scribus.net](https://www.scribus.net) — Free, open-source desktop publishing, scriptable via Python
- **Canva** — [canva.com](https://www.canva.com) — Book cover templates, basic API
- **Book Brush** — [bookbrush.com](https://bookbrush.com) — Cover creator, ad graphics

---

## 7. Current File Inventory

### Project Root: `D:\Hermes\projects\The-Night-I-Met-Santa\`

| Path | Description |
|---|---|
| `Audio/` | Dad's original WAV recording |
| `Transcription/` | Whisper output, cleaned poem text |
| `Images/` | Reference photos of Jack Farrell |
| `Media/` | All 15 scene illustrations + covers + watercolor washes |
| `Pages/` | Pre-composited JPEGs (v5 — illustration + wash + text) |
| `Output/` | All generated PDFs + covers |
| `build_book.py` | Original fpdf builder (v1) |
| `build_cover.py` | Original fpdf cover builder |
| `build_cover_v2.py` | Pillow cover builder |
| `composite_pages.py` | Pillow page compositor — illustration + wash + text |
| `process_washes.py` | Alpha channel processor for watercolor PNGs |
| `book.typ` | Typst layout v2 (text + image separate) |
| `book-v3.typ` | Typst layout v3 (integrated with hard panel) |
| `book-v4.typ` | Typst layout v4 (watercolor wash overlays) |
| `book-final.typ` | Typst layout v5 (pre-composited JPEG pages) |
| `cover.typ` | Typst cover attempt (abandoned — syntax issues) |
| `Book-Findings.md` | This document |
| `Poem-Book-Plan-v1.md` | Original project plan |

---

## 8. Key Lessons Learned

1. **Typst is excellent for book layout** — but PDF transparency (alpha channels in PNGs) doesn't survive the Typst→PDF pipeline reliably
2. **Pre-compositing is the safe path** — Pillow composites everything into flat JPEGs, Typst just places them
3. **Windows + GTK = pain** — WeasyPrint and CairoSVG aren't worth the DLL dependency hell; Typst + Pillow covers everything
4. **FAL Flux images don't have true transparency** — backgrounds come back white; need Pillow post-processing
5. **Watercolor wash approach:** Generating textures via AI then processing alpha in Pillow works, but simpler to just draw feathered rectangles in Pillow directly
6. **Lulu is the clear winner for single-copy proofs** — $4.45 paperback, $13.27 hardcover, 8.5×8.5" square is their #1 children's format
7. **Three image lanes beat one-model-for-everything** — Klein 4B dial → Qwen fallback → Banana `/edit`+refs finals; Ideogram is a poor fit when safety blocks child Christmas pajamas scenes
8. **Text legibility = Pillow problem, not fal model** — overpowered paper glow rejects; use mid-opacity fade and never cover faces (`TEXT-OVERLAY-POLICY.md`)

---

## 9. Cursor session diagnosis (2026-07-14 evening)

Jon rejected Hermes layout versions. Target layouts are the phone photos of real kids’ books (saved under `Images/references/layout/`).

### What each interior actually looks like

| Version | Tool | What happened | Verdict |
|---|---|---|---|
| **v3** | Typst + cream panel | Hard **opaque white square** with a parchment “stain” trapped *inside* the box | Looks glued-on / scrapbook — reject |
| **v4** | Typst + PNG wash overlays | Typst→PDF ate alpha → **checkerboard transparency** over most of the art | Broken — reject |
| **v5** | Pillow concentric soft rects → flat JPEG | Soft cream fog rectangle, readable text, no checkerboard — still **rectilinear**, not organic | Closest effort, still not the references |

### What Jon’s references actually do (two patterns)

1. **`ref-overlay-cloud-text.png`** — Full-bleed art + soft **cloud / irregular translucent panel** under black text; short lines can sit as **white type on dark sky** with no panel at all.
2. **`ref-spread-bleed-text.png`** — True **spread**: left page mostly paper/white for the poem; illustration bleeds from the right with a **painterly feathered edge** into the text area (not a rectangle floated on top).

### Why the “transparent light watercolor” failed

1. AI wash PNGs came back with **white backgrounds** → looked like cardboard sheets.
2. **Typst PDF** does not reliably preserve PNG alpha when stacking over a full-page image.
3. Brightness→alpha hacks (`process_washes.py`) punched wrong holes and did not create organic shapes.
4. v5’s concentric rectangles = soft **rectangle**, not a **cloud / painted bleed**.

### Correct engineering path (Pillow pre-composite — keep Typst only for front matter)

Do **not** layer transparent PNGs in Typst for poem pages. Bake once in Pillow:

1. Soft **elliptical / irregular cloud alpha mask** (Gaussian blur 80–160px) — not rectangles.
2. Fill cream at **~45–65% opacity** so wood grain / snow still shows through.
3. Draw poem text after the wash (Georgia or a rounded display for titles).
4. Export **flat RGB JPEG** per page → Typst/`image()` place only.
5. For busy dark scenes: prefer **white text on sky** (ref pattern) over a heavy panel.
6. Optional second mode: true **left-text / right-art bleed spread** matching `ref-spread-bleed-text.png`.

### Still needed (plenty of work)

- [ ] Pick layout mode per page (cloud overlay vs bleed-from-right spread)
- [ ] Quiet-zone map per illustration (where text won’t cover faces)
- [ ] Rewrite `composite_pages.py` cloud-mask wash
- [ ] Typography pass (line breaks, size, page numbers)
- [ ] Bleed/safety for Lulu; cover spine from final page count
- [ ] Proof order (~late July buffer for Aug 15)

---

## 10. fal model lanes (locked 2026-07-15)

Beat-1 real-scene shootout (same prompt/seed): `Media/generated/model-compare-beat01/`.

| Priority | Lane | Endpoint | ~Cost | Role |
|:--------:|------|----------|------:|------|
| 1 | Dial / dev | `fal-ai/flux-2/klein/4b` | ~$0.009/MP | Default iterate for layout & vibe |
| 2 | Fallback | `fal-ai/qwen-image-2/text-to-image` | ~$0.035/img | When Klein misses before spending Banana |
| 3 | Finals | `fal-ai/nano-banana-pro/edit` + style refs | ~$0.15/img | Approved pages / covers |

**Also tried / rejected for this book:**

| Model | Outcome |
|-------|---------|
| FLUX.1 [schnell] | Usable cheap scratch; weaker than Klein for gouache sneak beat |
| FLUX.2 [klein] 9B | Not clearly better than 4B at ~similar cost |
| Nano Banana Pro txt2img (no refs) | Strong prompt-only; still use **/edit + refs** for finals continuity |
| Ideogram V3 / V4 | Skip — fal safety filter blocked Christmas child / pajamas storybook Beat 1 (even softened prompt) |
| Qwen Image 2 | Good painted look; adopted as **fallback only** (cost between Klein and Banana) |

**Lesson for next book:** Prove lanes with one **real beat** folder before locking. Prefer MCP `user-fal-ai` over default `npm run image:fal*` (Flux schnell). See playbook **BOOK-PRODUCTION-SYSTEM.md** §2 + §9.

**Wallet note:** fal dashboard balance can lag; “exhausted” mid-session may clear after top-up / refresh (~$9+ after this session’s Banana-heavy burn).
