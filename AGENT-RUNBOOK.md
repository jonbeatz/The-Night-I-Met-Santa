# 🎅 Cursor Agent Runbook — The Night I Met Santa
**Give this to Cursor on first open. It's the single source of truth for building this book.**
**Version:** FINAL · July 19, 2026 · **Project:** D:\Hermes\projects\The-Night-I-Met-Santa

---

## What We're Building

An **8.5×8.5" hardcover children's picture book** of Jack Farrell's Christmas poem *The Night I Met Santa*. Painted gouache / watercolor style. One gift copy for Jack's birthday **August 15, 2026**. Printed via **Lulu**.

---

## 1. Cold Start — Launch DTP Pipeline First

Before any book work, launch the tools. Follow this EXACT order:

| Step | Who | Action |
|------|-----|--------|
| 1 | Agent | `Start-Process "C:\Program Files\Adobe\Adobe Creative Cloud\ACC\Creative Cloud.exe"` |
| 2 | **Jon** | Sign in to Creative Cloud Desktop until home screen shows. Reply "logged in." |
| 3 | Agent | **WAIT** — do NOT start UDT until Jon confirms sign-in complete. |
| 4 | Agent | `Start-Process "C:\Program Files\Adobe\Adobe UXP Developer Tools\Adobe UXP Developer Tools.exe"` |
| 4b | Agent | `Start-Process "C:\Program Files\Adobe\Adobe InDesign 2026\InDesign.exe"` |
| 4c | Agent | `npm run layout:indesign-bridge` (from project root, starts :19300/:19301) |
| 5 | **Jon** | In UXP Developer Tools → Load & Watch on InDesign Bridge (`com.ads.indesign-bridge`) |
| 5b | Agent *(when PS agent help needed)* | `npm run layout:photoshop-mcp` → broker `:47391` + MCP `:8766` (**before** trusting an already-Watching PS plugin) |
| 5c | **Jon** *(PS)* | UDT → Load & Watch **or Reload** **Adobe Python Bridge for Photoshop** (`com.adobepy.bridge.photoshop`) — prefs: **Enable Developer Mode** only |
| 6 | Verify | InDesign Bridge Panel → **Connected to bridge ✓** |
| 6b | Verify *(PS)* | `curl.exe http://127.0.0.1:47391/health` → `"sessions":≥1` · `…/8766/v1/readyz` → `"dcc":true` — Cursor green alone is **not** enough |
| 7 | Agent | Reload Cursor MCP → confirm indesign-uxp tools appear (~135 tools); photoshop URL green when PS stack up |

**PS gotchas:**
- Cursor Settings **photoshop red / Error / Logout** usually means **`:8766` down** — run `npm run layout:photoshop-mcp`, then clear stuck auth if needed, then **UDT Reload** so `"sessions":≥1`. PS open + UDT Loaded alone is not enough.
- If broker restarts while UDT still shows Watching/Loaded → **UDT Reload** on the Photoshop bridge (full PS restart usually unnecessary).
- `start-photoshop-mcp.ps1` must stay **ASCII-only** (em dashes break PowerShell).

**Do NOT** launch UDT before Jon confirms CC is signed in. Web login at adobe.com doesn't count — must be Creative Cloud Desktop app.
**Do NOT** uninstall Creative Cloud Desktop — InDesign needs it for licensing.
**Do NOT** use Photoshop COM MCPs (loonghao / alisaitteke) on this PC — COM `0x80080005`; use **adobepy UXP** only (`tools/layout-mcp/PHOTOSHOP-SETUP.md`).
**OK to** disable CC from startup. Only launch it for DTP sessions.

Full cold-start: `tools/layout-mcp/SETUP.md` · Photoshop: `tools/layout-mcp/PHOTOSHOP-SETUP.md` · Adobe watchlist: `.cursor/docs/ADOBE-CC-MCP-GUIDE.md`

---

## 2. Production Rules (READ CAREFULLY)

### CRITICAL: Page-by-Page Only
- **Generate ONE page/spread at a time.**
- **Jon MUST approve each one before moving to the next.**
- Do NOT batch-generate the whole book. Klein full-book batches were REJECTED.
- Process: Generate → Jon reviews → Jon approves → Lock → Next page.

### CRITICAL: Never Say "Final"
- Jon decides when something is final, not the agent.
- Say "ready for review" or "awaiting your approval."
- Never "this is the final version."

### CRITICAL: Art Generation Lanes
| Lane | Model | Cost | When To Use |
|------|-------|------|-------------|
| A (dial) | Klein 4B via FAL | ~$0.01 | Initial concepts, exploring compositions |
| B (finals) | Gemini / nano-banana-pro | ~$0.15 | After Jon approves composition — generate final art |
| G0 (locks) | Locked approved images | $0 | Already approved, do NOT regenerate |

Lane B is for FINAL artwork only — AFTER Jon says the Lane A composition is good.

### CRITICAL: No watermarks on print plates
- Before promoting any image to **Pass B / `Media/approved/print/`** or linking it into InDesign for Lulu: **check for AI / service watermarks, logos, or corner badges**.
- Agent flags them on review; **Jon removes them in Photoshop** if present (working files: `Xtraz/Adobe-Photoshop/`).
- Do **not** ship watermarked art into `Output/` PDFs or Tier B print keepers.

---

## 3. Approved Art (G0 Locks — DO NOT REGENERATE)

These are locked. Reference them, don't recreate them:

| Lock | Description | Location |
|------|-------------|----------|
| Cover | beige-v2 — oatmeal holly PJs, Santa face hidden | `Media/approved/covers/` |
| Boy narrator | G0 — style-match-A | `Media/approved/characters/` |
| Santa | G0 — paint north star | `Media/approved/characters/` |
| Jack portrait | style-match-B | `Media/approved/characters/` |
| Eyes-met spread | FINAL-TEST-A | `Media/approved/spreads/` |

---

## 4. Exact Print Specifications

| Spec | Value | Source |
|------|-------|--------|
| **Trim** | 8.5 × 8.5" | Lulu |
| **Interior PDF page size** | **8.75 × 8.75"** (with 0.125" bleed) | Lulu Book Creation Guide |
| **Art resolution** | **300 DPI** = 2625 × 2625 px | Lulu spec |
| **Spread art resolution** | **5250 × 2625 px** | For generation only |
| **Safety margin** | 0.5" from trim edge = 7.5 × 7.5" safe zone | Lulu spec — **ink** (glyphs/faces), not empty text-frame padding. Center-aligned type OK if letters sit inside magenta margins. |
| **Gutter** | **0"** — none needed for under 60 pages | Lulu guide p.9 |
| **Color space** | **sRGB** — confirm PDF is exported in sRGB, not CMYK (Lulu 2026 full-color requirement) | Lulu help Jun 2026 |
| **PDF format** | Single-page layout (not spreads) | Lulu requirement |
| **Fonts** | Embedded or outlined | Lulu requirement |
| **Spine** | 0.25" for 24–84 pages | Lulu guide p.14 |
| **Cover wrap (delivery · v82ejwq)** | **19 × 10.25″** = **5700 × 3075** @ 300 · spine **75 px** | Lulu template after interior upload |
| **Cover wrap (legacy working PSDs)** | 5475 × 2625 · 0.75″ spine placeholder | Soft-proof until native rebuild |
| **Page count** | **34** (gift HC) | Locked for spine; was 35–40 target earlier |
| **Cover spine text** | **Skip** on ≤0.25″ / under ~80 pp HC | Color/art strip only — type illegible at 75 px |
| **Casewrap pastedowns** | **Lulu supplies white endsheets** (not in interior PDF; not customizable) | [Hardcover Endsheets](https://help.lulu.com/en/support/solutions/articles/64000272836-hardcover-endsheets) · flipbook may simulate burgundy |

### Casewrap pastedowns / endsheets (LOCKED — Lulu 2026)

Lulu **adds** endsheets when binding casewrap hardcovers. They glue the book block to the cover boards.

- Endsheets/flyleaves **cannot be customized**; Lulu’s are **white** ([Hardcover Endsheets](https://help.lulu.com/en/support/solutions/articles/64000272836-hardcover-endsheets)). Do **not** try to replace printer pastedowns in the PDF.
- **Design burgundy pages in the interior are OK** — they are book pages, not a substitute for Lulu endsheets. Open still reads: white endsheet → interior.
- **Interior v2 (candidate 2026-07-31):** `TNIMS-Interior-FINAL-v2-burgundy-open` — **32 pp** with two `#4A0E17` pages before title so title stays **RIGHT** (PDF p1 is always right; +1 alone breaks every spread). Rollback: `TNIMS-Interior-FINAL` **30 pp**. README: `Xtraz/Adobe-Finals/TNIMS-Interior-FINAL-v2-burgundy-open-README.md`.
- **Flipbook:** blank burgundy IFC/IBC = **`#4A0E17`** RGB(74,14,23) — `Media/development/Cover/pastedown-burgundy.png` · `TNIMS-FLIPBOOK.indd` / `TNIMS-FLIPBOOK-trim.pdf` (LOCKED 2026-07-31).
- Cover wrap: still fill the **0.75″ wrap** on the cover PDF; that tucks under the endsheet on the inside board.
- **S04 text+image (p12|13 on 34-pp FINAL):** Prefer **spine-meet** frames (no facing bleed overlap) + normal PDF export. Isolate hide/merge is legacy fallback only — see Text+image placement below.

---

## 5. Design Standards

| Element | Spec |
|---------|------|
| **Text alignment** | **CENTERED** — not justified, no indent |
| **Font** | **Cormorant Garamond Medium** |
| **Size** | **20 pt** (Jon UI: 20px) |
| **Leading** | **26 pt** (Jon: “26px vertical kern” = line spacing) |
| **Tracking** | **+5** (Jon: “5px horizontal kern” — InDesign Tracking) |
| **Text color** | Dark Charcoal **#2C2C2C** / PoemCharcoal |
| **Text cloud** | Custom watercolor cloud PNG — irregular feathered edges, translucent — Jon creates this · **alt:** FLUX.2 LoRA paper @ scale ~**0.35** (`Media/generated/mocks/_INDEX/text-page-lora/`) after seed lock; retrain on paper-only crops before scale 1.0 |
| **Cloud position** | Placed per spread by Jon — avoids faces and focal points |
| **Right page** | Full-bleed illustration to bleed edge |
| **Left page** | Illustration as background + centered cloud + centered poem text |

> **Locked 2026-07-20 (Jon):** poem defaults above. Agents must use these when creating new text frames. In JSX set strings when rulers are inches: `pointSize = "20pt"`, `leading = "26pt"`, `tracking = 5`, font `Cormorant Garamond\tMedium`.

---

## 6. InDesign Build — Per Spread

### Layer Stack (bottom to top)
```
Layer 3: create_text_frame — Cormorant Garamond Medium 20/26 tracking +5, centered, #2C2C2C
Layer 2: place_image — watercolor cloud PNG (Jon's custom asset)
Layer 1: place_image — full-bleed illustration, 2625×2625 px, 300 DPI
```

### Build Sequence
1. `create_document` — 8.5×8.5", 0.125" bleed, single-page
2. For each spread:
   - `place_image` — left page art
   - `place_image` — right page art
   - `place_image` — Jon's cloud PNG on left page at Jon's coordinates
   - `create_text_frame` — poem text on left page
3. When all pages are done: `export_pdf` — use **Lulu-Interior-Print-PDF.joboptions**

### Placement gotchas (UXP MCP — 2026-07-20)

Full write-ups: **`.cursor/docs/ISSUES-RESOLVED.md`**. Operator says **`log fixes`** to append new ones.

**First-create rule (LOCKED):** Jon **Save As** new `.psd` / `.indd` to final path **once** → click any Adobe dialog → say **ready** → agent places art/type. Detail: `PAGE-BUILD-WORKFLOW.md` §3b.

| Prefer | Avoid |
|--------|--------|
| Jon first-saves to final path under `Xtraz/Adobe-*` | Agent first-saving Untitled while a Save/Close modal is open (bridge hangs; wrong Untitled → A4) |
| Verify **8.5×8.5 in** vs `p03-dedication-smoke.indd` | Trusting `create_document` defaults without checking |
| Jon clicks Adobe Save/Close/font/link dialogs → **ready** | Leaving modals open for the agent |
| One place cycle + `list_page_items` / Layers check | Retry-placing when unsure (stacks Cloud duplicates) |
| `execute_indesign_code` rectangle → `place(path)` → `resize_page_item` on the Image | Blind `place_image` / `place_file_on_page` as sole path |
| Keep placement rectangle + sized Image until Layers shows **one** cloud | Deleting the “empty” rectangle without confirming the link |
| Inspect PNG / trust Jon on transparency | Assuming black fill from a thumbnail description |
| Live text via JSX on the **target page** (`page.textFrames.add`) | `create_text_frame` alone (orphan pasteboard / empty page — text “missing”) |
| `resize_page_item` in **points** (8.75″=630, spread=1260×630) | Negative-mm `place_image`; hoping `fit()` fixes sibling Image |
| Jon drags **Frame** layer to top if needed | Long JSX fights with `LocationOptions` in UXP bridge |
| **PS MOCK + chops → InDesign match → live type** (default) | Raster poem PNGs as finals; placing without a MOCK |
| textCloud at **natural size** from page top-left (match MOCK) | Squeezing cloud into a tight inset box |

### Default spread workflow (Jon + agent)

1. Jon: start from **`spread-page-template.psd`** (spreads) or **`single-page-template.psd`** (singles) in `Xtraz/Adobe-Photoshop/` (**Duplicate → Jon Save As** to final slug) → paint → export **MOCK** + chops to `Images/chopz/` (PNG preferred)
2. Agent: facing pages → **place seamless art as ONE `*-spread.png` centered on the spine** (see § Seamless spread placement) → cloud if separate → optional MOCK @ 35% → **live type matching each PS type layer’s size/leading/tracking/color/position** → hide MOCK
3. Jon: eye-check vs MOCK (glyphs inside magenta); approve

### Seamless spread placement (LOCKED 2026-07-30 — v9/v10)

**Do not** place left/right half PNGs each with full 0.125″ bleed on all four sides. That makes both frames cross the gutter and **overlap by 0.25″**, so seamless art does not meet at the fold.

| Rule | Detail |
|------|--------|
| **Master** | `5250 × 2625` @ 300 DPI = **17.5″ × 8.75″** (PSB fold = canvas midpoint) |
| **Place** | One linked `*-spread.png` spanning the facing spread |
| **Align** | Frame midpoint **= InDesign spine** (left page’s right edge, usually **8.5″**) |
| **Bounds** | `top/bottom = ±0.125″` from trim; `left = spine − 8.75″` (−0.25); `right = spine + 8.75″` (17.25) |
| **Fit** | `CONTENT_TO_FRAME` after place; re-assert bounds |
| **Singles** | Page 1 / true single pages still use `*-right.png` / `2625²` in the page bleed box |
| **Verify** | Facing-pages view · midX of spread frame == spine · delta **0** |

Half exports (`*-left.png` / `*-right.png`) remain useful for chops/MOCK; **print facing art uses the full spread file**.

### Text+image placement (UPDATED 2026-08-01 — S04)

**Exception to seamless one-file placement.** When facing pages are **not** one continuous scene (cream text page \| full illustration — S04 Sit Here, and any similar text+image pair):

| Rule | Detail |
|------|--------|
| **Do not** | Place one spanning `*-spread.png` for Lulu single-page PDF — spine bleed pulls the facing half into each page (obvious on hard color splits) |
| **Place** | Separate `*-left.png` / `*-right.png` · **outer** bleeds 0.125″ · frames **meet at the spine** (no facing-page invasion) |
| **PDF export (preferred)** | Normal Lulu Interior export with both frames visible — spine-meet prevents gutter crosstalk |
| **PDF export (legacy fallback)** | If frames still overlap at spine: hide facing art per page, export, merge (`_merge_s04_interior_pdf_v2.py`) |
| **Why** | Full 0.125″ bleed on **all four** sides of each half → ~0.25″ overlap at gutter → cream page shows burgundy sliver (and vice versa) |
| **Seamless image spreads** | Unchanged — still one `*-spread.png` centered on the spine |

Chops: finals under `FINAL-Master-Chopz/` (`S04-left` / `S04-right`). Spread file OK for PS/MOCK only.

### PS → InDesign live type (LOCKED 2026-07-30)

Defaults (Cormorant Medium 20/26 +5) are a **fallback only**. When building from a master PSB/PSD:

1. Read **each visible type layer** — size, leading, tracking, color, justification, and **bbox**
2. Create live frames at that **exact page position** (bbox px ÷ 300 − bleed)
3. Apply **that layer’s** formatting — do **not** force every stanza to 20/26 if the PS layer differs
4. Prefer one frame per PS type layer (Jon often splits stanzas across multiple layers)
5. No baked letter FX unless Jon asks — v7+ masters ship type without Drop Shadow / Outer Glow
6. **Match PSD fidelity:** font, size, leading, tracking, **alignment**, color, box — center stays center
7. **Pica rulers gotcha (2026-07-31):** if document units are **picas**, switch viewPreferences to **POINTS** before setting `pointSize`/`leading` (or use `"14pt"` strings). Bare `pointSize = 14` = **14 picas** ≈ 132 pt → fake overset. See `ISSUES-RESOLVED.md`.

#### PSD blanks (locked — matches InDesign / Lulu)

| File | Size | Guides | Notes |
|------|------|--------|-------|
| `spread-page-template.psd` | 5250×2625 | cyan TRIM · magenta SAFETY · orange FOLD | Hide fold for finals |
| `single-page-template.psd` | 2625×2625 | cyan TRIM · magenta SAFETY | One interior page |
| `book-covers-template.psd` | 2625×2625 | same + orange hinge hints | Front **or** back art; final wrap from Lulu |
| *(no spine PSD)* | — | — | Spine width set by Lulu after interior upload |

**Shared:** Duplicate → Save As · paint **ART** · type live in InDesign. Full key: `Xtraz/Adobe-Photoshop/README.md`.

**textCloud export (pick one):**
- **A (recommended):** full page **2625²** or spread **5250×2625**, cloud painted in place, rest transparent → place full-bleed  
- **B:** tight crop of cloud only → place/scale to MOCK  

**paintFrame:** keep on big emotional spreads; optional not every page.

Full playbook: **`.cursor/docs/ISSUES-RESOLVED.md`** (top “Playbook” section).

### Fast chop → facing-spread recipe

1. **Spread art** → place **`*-spread.png` once** · bounds **17.5″ × 8.75″** · midpoint on spine (not L/R halves with full bleed)  
2. textCloud → Option A full-bleed **or** match MOCK (never squeeze pre-composed cloud into a tiny inset) — skip if cloud already baked in spread plate  
3. Live type → **match each PS type layer** (size/leading/tracking/color/bbox); fallback only: Cormorant Medium **20/26** tracking **+5**, centered  
4. paintFrame on **spread** → resize **1260×630** (optional)  
5. Optional: MOCK-REF @ ~35% → align → hide  
6. `list_page_items` + save — do not re-place

### Export Presets
Load these once in InDesign (File → Adobe PDF Presets → Define → Load):
- `Xtraz/Lulu-Templates/Square-Template/lulu-book-template-all-square/Adobe PDF Export Presets/Lulu-Interior-Print-PDF.joboptions`
- `Xtraz/Lulu-Templates/Square-Template/lulu-book-template-all-square/Adobe PDF Export Presets/Lulu-Cover-Print-PDF.joboptions`

---

## 7. Cover Build — AFTER Interior is Uploaded

**Best plan (TNIMS + future Hermes print books):** Start from a **ballpark** trim/binding/page range — you do **not** need Lulu’s exact template to begin art. Lock the exact wrap size **before final cover PDF / order**.

1. Ballpark trim · binding · rough page range; generate keepers at print res  
2. When page count is stable enough: upload interior → download cover template + guides  
3. Fit wrap to **exact** template px (this book: **5700 × 3075**)  
4. Optional Front / Back / Spine solos = panel crops of that wrap (matched guides)  
5. Soft-proof → Cover PDF (`Lulu-Cover-Print-PDF.joboptions`) · **sRGB**  
6. **Do not order** until Jon explicitly says so  

**Spine type:** skip on 0.25″ (75 px) — use art/color only.  
**Interior book master (`TNIMS-Book-Master-FINAL.psb`):** **5250 × 2625** @ 300 (= two **8.75″** bleed pages). That is the correct interior size — **do not** resize the PSB to cover-wrap dimensions.

**Art + Photoshop (cover and pages):**
- Generate / keep masters at the **highest useful print res** the lane allows (never low-res dials for keepers) so we can downscale cleanly.  
- Prefer **upscale to exact target** if the API returns short — don’t ship undersized plates.  
- **Oversize keepers for covers:** leave extra margin beyond panel/wrap crop so reposition (chair, feet, cover-fit) is a transform — not a full regen. Lock Lulu wrap px before treating cover PSDs as delivery SoT (lesson 2026-08-02).  
- In Photoshop: place logos, plate art, and reusable assets as **Smart Objects** so transforms stay non-destructive. When replacing SO contents, **preserve layer styles** on the parent (Edit Contents / paste into SO — don’t rebuild the layer cold unless you copy effects).

Hardcover guides / templates: `Xtraz/Lulu-Templates/` · delivery SoT PSDs: `FINAL-Master-PSDs/5700x3075-version/` (Front · Back · Wrap only) · rebuild after panel edit: **`.cursor/docs/COVER-REBUILD-WORKFLOW.md`** (`npm run book:cover:rebuild-wrap` → `book:cover:art-notype` → Cover INDD → flipbook bake) · checklist: `.cursor/docs/LULU-ORDER-CHECKLIST.md`

---

## 8. Two Delivery Files

| File | Content | Upload |
|------|---------|--------|
| **Interior PDF** | 35-40 single pages, 8.75×8.75", sRGB, fonts embedded | Lulu → Interior |
| **Cover PDF** | One-piece spread: back + spine + front | Lulu → Cover |

---

## 9. Poem Text Reference

The poem lives in `Transcription/poem-clean.txt`. All 15 stanzas. Map:

| Stanza | What Happens | Page |
|--------|-------------|------|
| S01 | House quiet, fire glow, Tommy nestled in bed | Left page 1 + right page illustration |
| S02-S15 | Remaining stanzas — see `PAGE-PROMPT-BIBLE.md` for full mapping |

For detailed stanza-to-page mapping: `BOOK-PAGE-WORKFLOW.md`. For image prompts: `MASTER-PRODUCTION-DOCK.md` (`POEM-IMAGE-PROMPT-DOCK.md` / `PAGE-PROMPT-BIBLE.md` are stubs).

---

## 10. Image Generation Commands

```powershell
# From project root:
npm run image:fal:page -- "Christmas Eve bedroom, painterly Santore style..."
npm run image:fal:spread -- "Santa and child by fireplace, wide cinematic... seamless continuous spread, NO fake book gutter NO vertical fold line NO center spine shadow"
npm run image:fal:cover -- "hero holiday cover scene..."
npm run image:gen:page -- "cheap draft..."   # HF free fallback
```

**Presets:** page = 2625×2625 · spread = 5250×2625 · cover draft may be square dial — **keeper / final cover art = Lulu wrap or panel size (up to 5700×3075 / panel ~2812×3075), never undersized**
**Output:** Files land in `Media/generated/` — review, then promote approved art to `Media/approved/`
**Lane A → B workflow:** Generate Lane A compositions → Jon picks one → Generate Lane B final → Jon approves → Lock

---

## 11. Backup & Recovery

| What | How |
|------|-----|
| **Snapshots before big writes** | Save-as in InDesign under `Xtraz/Adobe-inDesign/`: `book-v1.indd`, `book-v2.indd` |
| **Lulu upload rollback** | Lulu keeps version history — you can revert uploaded files |
| **Project backup** | `git add -A && git commit -m "pre-batch backup"` before batch operations (docs only; `.indd` is gitignored under `Xtraz/`) |

---

## 12. Proofing Step (Before Birthday)

1. Upload interior + cover PDFs to Lulu
2. **Order ONE proof copy** (~$13-15 + shipping)
3. Review physical copy — check color, bleed, binding, text readability
4. Fix any issues, re-upload corrected PDFs
5. Order final copy for August 15 birthday

**Timeline:** Proof ordered by ~**July 25-28** to arrive before August 15.

---

## 13. Project File Map

| Path | What |
|------|------|
| `poem-clean.txt` | Poem text of record |
| `Media/approved/INDEX.md` | Two-tier approval tracking |
| `Media/assets/` | Cloud PNGs and other reusable assets |
| `Pages/` | Fallback composites only (not gift default) |
| **`Xtraz/Adobe-inDesign/`** | **Working InDesign docs** (`.indd` / `.idml`) — edit here |
| **`Xtraz/Adobe-Photoshop/`** | **Working Photoshop docs** — blanks: `spread-page-template.psd` · `single-page-template.psd` · `book-covers-template.psd` (no spine PSD) |
| **`Xtraz/Affinity/`** | Optional Affinity working docs |
| `Xtraz/Lulu-Templates/` | Lulu Book Creation Guide + templates + .joboptions |
| `Xtraz/Fonts/` | Cormorant Garamond + Cinzel (OFL, gitignored) |
| **`Output/interiors/`** | Exported interior PDFs for Lulu |
| **`Output/covers/`** | Exported cover PDFs for Lulu |
| `tools/layout-mcp/SETUP.md` | Cold-start pipeline instructions |
| `.cursor/docs/INDESIGN-PRODUCTION-WORKFLOW.md` | Full specs reference |
| `.cursor/docs/CONTINUE-HERE.md` | Session resume + next actions |
| `.cursor/docs/ReCall.md` | Session focus / leave-off (after START-HERE) |
| `BOOK-PLAYBOOK.md` | Reusable system for future books |

**Rule:** Edit in `Xtraz/Adobe-inDesign/` (or `Xtraz/Affinity/`). Photoshop working files → `Xtraz/Adobe-Photoshop/`. Export press PDFs only to `Output/`. Do not keep long-lived `.indd` under `Output/`.

---

## 14. Digital Flipbook — Family Review Tool

After the book is done, create a viewable flipbook for family and friends:

**Plugin:** [3D FlipBook by iberezansky](https://wordpress.org/plugins/interactive-3d-flipbook-powered-physics-engine/) (free, no limits, no watermark)

- WebGL 3D rendering with real physics page bending
- Unlimited pages and file size — perfect for a 35-40 page picture book
- Upload to DigitalStudioz WP site (or any WordPress install)
- Shortcode: `[3d-flip-book id="1"]` → private page → share link with family
- Also works standalone via [GitHub repo](https://github.com/iberezansky/flip-book-jquery) (GPL — forkable for future projects)
- Source code: [SVN browser](https://plugins.trac.wordpress.org/browser/interactive-3d-flipbook-powered-physics-engine/)

**Setup (post-production):**
1. Export viewing PDF from InDesign (spreads view, 8.5×8.5" trim, sRGB)
2. Install 3D FlipBook on WordPress
3. Create new flipbook → paste PDF URL
4. Shortcode on private/family page
5. Share link — they see a gorgeous 3D page-turning book on any device

---

## 15. What NOT To Do

- ❌ Generate more than one spread at a time
- ❌ Call anything "final"
- ❌ Export CMYK for Lulu — confirm PDF is **sRGB**, not CMYK (per Lulu’s current print requirements; old “CMYK for print” does not apply)
- ❌ Add gutter margins (not needed under 60 pages)
- ❌ Bake a **fake center fold / gutter shadow line** into final spread art (MOCK preview only; print art must be seamless)
- ❌ Crop through **mid-paint** to recenter a soft watercolor vignette (shears the soft crown → hard top edge). Reposition/scale the **whole** soft vignette, or choose a text-zone layout that matches how the plate was painted. See `ISSUES-RESOLVED.md` 2026-07-21 P01 v24
- ❌ Say **“feathered”** to Qwen/fal for vignette edges — models draw **bird feathers**. Say *watercolor bleed / soft dissolve / organic paint edge* (`ISSUES-RESOLVED.md` 2026-07-22)
- ❌ Ask Qwen alone for a **page-margin watercolor frame** — it frames the **art vignette**. Pillow-lock cream page + outer-margin wash first; polish optional; fall back if subject swaps (`ISSUES-RESOLVED.md` 2026-07-22 P01 v16)
- ❌ **Overwrite a LOCKED KEEP** to run a frame/color test — use a new version folder (`vNN-framed-alt/`); archive `_LOCKED-vNN/` (`ISSUES-RESOLVED.md` 2026-07-23)
- ❌ Apply **deep cream vignette** into burgundy mid-walls without protecting opacity / restoring wall ROI — cream bleed reads as a “ghost face” (`ISSUES-RESOLVED.md` 2026-07-23)
- ❌ Ship a spread without the **triplet** (`art.png` 5250×2625 + `art-left.png` + `art-right.png` 2625²) — automatic on every spread gen
- ❌ Hand-roll `_INDEX` comparison boards without poem captions — always use `scripts/book_review_board.py` (`seamless_board` / `split_board` / `text_image_board`); poem source `book_poem_map.py` (`ISSUES-RESOLVED.md` 2026-07-23)
- ❌ Ship a mock `vNN/` with a **thin RECIPE** (no full Prompt / missing lane·model·FRAME·script_text). Copy `Media/generated/mocks/_RECIPE-TEMPLATE.md`
- ❌ Put text on spine (book is under 80 pages)
- ❌ Launch UDT before Creative Cloud sign-in
- ❌ Regenerate G0 locked art
- ❌ Use Pillow for **gift poem/title type** or press PDF (InDesign is production path). Pillow **is** OK for mock geometry: text-band push-down, page-margin frame structure, comparison boards
- ❌ Store working `.indd` files under `Output/` (use `Xtraz/Adobe-inDesign/`)
- ❌ Leave TL;DR notes in chat — Jon prefers full reports
