# InDesign UXP Production Workflow — The Night I Met Santa
**Date:** July 19, 2026 · **Tool:** InDesign UXP Bridge :19300/:19301
**Replaces:** Pillow compositing for final text-on-art
**Print target:** Lulu 8.5×8.5" casewrap hardcover · 35-40 pages · **sRGB**

---

## Final Delivery: 2 PDF Files

| File | What It Is | Lulu Upload |
|------|-----------|-------------|
| **1. Interior PDF** | Single PDF containing every page. Single-page layout (not spreads). Includes copyright, blank pages. 35-40 pages total. | Upload as "Interior" |
| **2. Cover PDF** | One-piece cover wrap: back cover + spine + front cover as a single wide page. Spine width calculated by Lulu after interior upload. | Upload as "Cover" |

> **Cover template comes AFTER interior upload.** Lulu generates an exact cover template with the correct spine width once it knows your page count.

---

## Full Resolution & Dimension Reference

| Element | Dimensions (inches) | Dimensions (pixels @ 300 DPI) | Notes |
|---------|---------------------|-------------------------------|-------|
| **Trim size** | 8.5 × 8.5" | 2550 × 2550 px | Final cut size |
| **Single page (with bleed)** | 8.75 × 8.75" | 2625 × 2625 px | What InDesign exports |
| **Single page art (full-bleed)** | 8.75 × 8.75" | 2625 × 2625 px | Illustration fills to bleed edge |
| **Spread (two facing pages)** | 17.5 × 8.75" | 5250 × 2625 px | For illustration generation. InDesign splits into single pages. |
| **Safety zone (per page)** | 7.5 × 7.5" | 2250 × 2250 px | 0.5" inset from trim. Text and critical content stay inside this. |
| **Extra gutter** | **0"** (none for under 60 pages) | 0 px | Per Lulu guide p.9 — do **not** add inner gutter for this book |

### Cover Dimensions (35-40 pages = 0.25" spine)

| Element | Dimensions (inches) | Dimensions (pixels @ 300 DPI) |
|---------|---------------------|-------------------------------|
| **Front cover** | 8.5 × 8.5" | 2550 × 2550 px |
| **Spine** | **0.25 × 8.5"** | 75 × 2550 px |
| **Back cover** | 8.5 × 8.5" | 2550 × 2550 px |
| **Cover wrap beyond trim** | 0.75" all sides | 225 px |
| **Total cover width (with bleed)** | **~19.5"** (8.5+0.25+8.5+0.125+0.125 wrap+bleed) | **~5850 px** |
| **Total cover height (with bleed)** | **~10.0"** (8.5+0.75+0.75 wrap+bleed) | **~3000 px** |
| **Cover safety margin** | 0.5" from trim | 150 px |

> **Exact cover template from Lulu after interior upload.** The above dimensions are calculated from the Lulu Book Creation Guide hardcover spine table (page 14) and bleed/wrap specs.

---

## Verified Lulu Print Specs (from official KB, Oct 2024)

| Spec | Exact Value |
|------|-------------|
| **Color space** | **sRGB preferred** (not CMYK). Lulu converts to rich CMYK internally. ICC: sRGB + Gracol. |
| **Trim size** | 8.5 × 8.5" |
| **Interior PDF page size** | 8.75 × 8.75" (trim + 0.125" bleed all sides) |
| **Bleed** | 0.125" on all edges |
| **Safety margin** | 0.50" from trim edge |
| **Extra gutter** | **None** for books under 60 pages (this title). Keep critical art/text out of the fold by composition, not by a forced inner margin. |
| **Resolution** | 300 DPI (cover: 300-600 DPI) |
| **PDF format** | Single-page (not spreads), no trim marks, no security, no passwords |
| **Fonts** | Embedded or converted to outlines |
| **PDF export** | sRGB PDF (not CMYK PDF/X-1a) |
| **Solid blacks** | 100% K only. TAC ≤ 270% |
| **Light tints** | Avoid builds under 20% |
| **Cover wrap** | 0.75" beyond trim on all sides |
| **Cover overhang** | 0.125" on 3 sides |
| **Cover hinge** | 0.25" from spine |
| **Cover stock** | 80# gloss laminated white |
| **Page count** | 35-40 pages (Lulu hardcover minimum: 24) |

---

## Locked Design Standards

| Element | Spec |
|---------|------|
| **Text alignment** | Centered — not justified, no first-line indent |
| **Text cloud** | Irregular feathered watercolor cloud PNG (custom, placed per spread) |
| **Typography** | Cormorant Garamond, 14pt, Dark Charcoal (#2C2C2C) |
| **Right page** | Full-bleed illustration (art fills to bleed edge) |
| **Left page** | Illustration as subtle background + centered cloud asset + centered poem text |

---

## InDesign Layer Stack (Per Page or Spread)

```
Layer 3: create_text_frame (Cormorant Garamond, centered, dark charcoal)
Layer 2: place_image (watercolor cloud PNG — feathered, custom position)
Layer 1: place_image (full-bleed illustration, 2625×2625 px, 300 DPI)
```

---

## Build Sequence

1. `create_document` — 8.5×8.5", 0.125" bleed, single-page layout
2. For each page pair in manifest:
   - `place_image` — left page art (2625×2625 px)
   - `place_image` — right page art (2625×2625 px)
   - `place_image` — watercolor cloud asset on left page
   - `create_text_frame` — centered poem text, left page
3. `export_pdf` — Load Lulu's PDF preset: `Lulu-Interior-Print-PDF.joboptions`
4. Upload interior PDF to Lulu → get cover template with exact spine
5. Build cover in InDesign:
   - Open `lulu-square-hardcover-template.idml` (or custom template from Lulu)
   - `place_image` — cover art on front, back, spine
   - `export_pdf` — Load Lulu's PDF preset: `Lulu-Cover-Print-PDF.joboptions`

### Lulu Adobe PDF Export Presets

Lulu provides `.joboptions` files that configure InDesign's PDF export with exact print specs. Load them once:

| File | For | How to Install |
|------|-----|----------------|
| `Lulu-Interior-Print-PDF.joboptions` | Interior page exports | InDesign: File → Adobe PDF Presets → Define → Load |
| `Lulu-Cover-Print-PDF.joboptions` | Cover spread exports | InDesign: File → Adobe PDF Presets → Define → Load |

**Location:** `Xtraz/Lulu-Templates/Square-Template/lulu-book-template-all-square/Adobe PDF Export Presets/`

These presets preserve document colors (`LeaveColorUnchanged`) and set 300 DPI / font embedding / bleed handling. **You must** set the InDesign document and linked RGB assets to **sRGB** — the preset does not convert CMYK→sRGB for you.

### Lulu Hard Cover Template

**Location:** `Xtraz/Lulu-Templates/Square-Template/lulu-book-template-all-square/Cover Templates/Hardcover/`

| Format | File | Use |
|--------|------|-----|
| InDesign | `InDesign/lulu-square-hardcover-template.indd` / `.idml` | Base cover design with guides |
| PDF | `PDF/lulu-square-hardcover-template.pdf` | Reference for dimensions |
| Photoshop | `Photoshop/lulu-square-hardcover-template.psd` | Alternative design tool |
| PNG guides | `PNG/lulu-square-hardcover-template-guides.png` | Layer as reference in any tool |

> The spine width in the bundled template is a minimum/default. **Replace with custom template from Lulu after interior upload** for exact spine width based on your page count.

### Lulu Interior Template

**Location:** `Xtraz/Lulu-Templates/Square-Template/lulu-book-template-all-square/Interior Templates/Single Pages/`

| Format | File | Use |
|--------|------|-----|
| InDesign | `InDesign/lulu-square-interior-template.indd` / `.idml` | Base interior with margins/bleed |
| Word | `Word/lulu-square-interior-template.dotx` | Alternative for simple layouts (if present) |

---

## What This Replaces

Old: Pillow composite_pages.py → flat JPEGs → Typst binder
New: InDesign UXP → live text frames → press-ready sRGB PDF

Pillow/Typst remains as fallback. InDesign is the production path.
