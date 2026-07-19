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
| 6 | Verify | InDesign Bridge Panel → **Connected to bridge ✓** |
| 7 | Agent | Reload Cursor MCP → confirm indesign-uxp tools appear (~135 tools) |

**Do NOT** launch UDT before Jon confirms CC is signed in. Web login at adobe.com doesn't count — must be Creative Cloud Desktop app.
**Do NOT** uninstall Creative Cloud Desktop — InDesign needs it for licensing.
**OK to** disable CC from startup. Only launch it for DTP sessions.

Full cold-start details: `tools/layout-mcp/SETUP.md`

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
| **Safety margin** | 0.5" from trim edge = 7.5 × 7.5" safe zone | Lulu spec |
| **Gutter** | **0"** — none needed for under 60 pages | Lulu guide p.9 |
| **Color space** | **sRGB** (not CMYK) | Lulu KB Oct 2024 |
| **PDF format** | Single-page layout (not spreads) | Lulu requirement |
| **Fonts** | Embedded or outlined | Lulu requirement |
| **Spine** | 0.25" for 24–84 pages | Lulu guide p.14 |
| **Cover wrap** | 0.75" beyond trim all sides | Lulu spec |
| **Cover overhang** | 0.125" on 3 sides | Lulu spec |
| **Page count** | 35–40 pages | Project target |
| **Cover spine text** | **Skip** — under 80 pages | Lulu guide p.17 |

---

## 5. Design Standards

| Element | Spec |
|---------|------|
| **Text alignment** | CENTERED — not justified, no indent |
| **Font** | Cormorant Garamond, 14pt |
| **Text color** | Dark Charcoal #2C2C2C |
| **Text cloud** | Custom watercolor cloud PNG — irregular feathered edges, translucent — Jon creates this |
| **Cloud position** | Placed per spread by Jon — avoids faces and focal points |
| **Right page** | Full-bleed illustration to bleed edge |
| **Left page** | Illustration as background + centered cloud + centered poem text |

---

## 6. InDesign Build — Per Spread

### Layer Stack (bottom to top)
```
Layer 3: create_text_frame — Cormorant Garamond, centered, dark charcoal
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

### Export Presets
Load these once in InDesign (File → Adobe PDF Presets → Define → Load):
- `Xtraz/Lulu-Templates/Square-Template/lulu-book-template-all-square/Adobe PDF Export Presets/Lulu-Interior-Print-PDF.joboptions`
- `Xtraz/Lulu-Templates/Square-Template/lulu-book-template-all-square/Adobe PDF Export Presets/Lulu-Cover-Print-PDF.joboptions`

---

## 7. Cover Build — AFTER Interior is Uploaded

1. Upload interior PDF to Lulu
2. Lulu generates custom cover template with exact spine width
3. Download the custom template
4. Build cover in InDesign using `Lulu-Cover-Print-PDF.joboptions`
5. Export as one-piece spread PDF (back + spine + front)

Hardcover cover template reference files in: `Xtraz/Lulu-Templates/Square-Template/lulu-book-template-all-square/Cover Templates/Hardcover/`

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

For detailed stanza-to-page mapping, image prompts per beat, and beat gap audit: `PAGE-PROMPT-BIBLE.md` and `BEAT-GAP-AUDIT.md`

---

## 10. Image Generation Commands

```powershell
# From project root:
npm run image:fal:page -- "Christmas Eve bedroom, painterly Santore style..."
npm run image:fal:spread -- "Santa and child by fireplace, wide cinematic..."
npm run image:fal:cover -- "hero holiday cover scene..."
npm run image:gen:page -- "cheap draft..."   # HF free fallback
```

**Presets:** page = 2625×2625 · spread = 5250×2625 · cover = 2048² draft
**Output:** Files land in `Media/generated/` — review, then promote approved art to `Media/approved/`
**Lane A → B workflow:** Generate Lane A compositions → Jon picks one → Generate Lane B final → Jon approves → Lock

---

## 11. Backup & Recovery

| What | How |
|------|-----|
| **Snapshots before big writes** | Save-as in InDesign: `book-v1.indd`, `book-v2.indd` |
| **Lulu upload rollback** | Lulu keeps version history — you can revert uploaded files |
| **Project backup** | `git add -A && git commit -m "pre-batch backup"` before batch operations |

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
| `Pages/` | Pre-composited page images (build output) |
| `Output/` | Final PDFs for Lulu |
| `Xtraz/Lulu-Templates/` | Lulu Book Creation Guide + templates + .joboptions |
| `Xtraz/Fonts/` | Cormorant Garamond + Cinzel (OFL, gitignored) |
| `tools/layout-mcp/SETUP.md` | Cold-start pipeline instructions |
| `.cursor/docs/INDESIGN-PRODUCTION-WORKFLOW.md` | Full specs reference |
| `.cursor/docs/CONTINUE-HERE.md` | Session resume + next actions |
| `BOOK-PLAYBOOK.md` | Reusable system for future books |

---

## 10. What NOT To Do

- ❌ Generate more than one spread at a time
- ❌ Call anything "final"
- ❌ Use CMYK color space
- ❌ Add gutter margins (not needed under 60 pages)
- ❌ Put text on spine (book is under 80 pages)
- ❌ Launch UDT before Creative Cloud sign-in
- ❌ Regenerate G0 locked art
- ❌ Use Pillow compositing (InDesign is production path)
- ❌ Leave TL;DR notes in chat — Jon prefers full reports
