# Lulu 8.5×8.5" square — cheatsheet (TNIMS)

**Target:** Casewrap hardcover · color · sRGB · gift for Jack · ~32 pages
**Sources:** `Xtraz/Lulu-Templates/lulu-book-creation-guide.pdf` + saved help HTML (2026-07-16)

---

## Interior page

| Spec | Value |
|------|--------|
| Trim | **8.5" × 8.5"** |
| Bleed (each side) | **0.125"** |
| Full-bleed art canvas | **8.75" × 8.75"** |
| Trim pixels @ 300 DPI | **2550 × 2550** |
| Full-bleed pixels @ 300 DPI | **2625 × 2625** |

**Correct DPI math:**
- Trim 8.5" @ 300 DPI = **2550 × 2550**
- With 0.125" bleed → 8.75" @ 300 = **2625 × 2625** ✓ (this is the full-bleed single page)

Project already uses **2625²** / spread **5250×2625** in `CONTINUITY-AND-PRINT-FINALS.md`.

| Safety | Keep critical text/faces **≥ 0.5"** inside trim |
| Gutter | Facing spreads: keep important art out of center fold |
| Color | **sRGB** (Lulu accepts RGB; do not force CMYK-first) |
| Page count | Even number (24–40 typical); we plan **32** |

---

## Cover (casewrap)

Lulu builds a **custom cover template PDF** after you upload the **interior PDF** (spine width depends on page count + paper).

Until then:
- Design front/back as separate 8.5×8.5 (or full-bleed 8.75) art
- Leave spine for Lulu template fill
- See help: *Creating Your Hardcover Casewrap Cover* (saved as `hardcover-casewrap.html`)

Credits (locked): back cover small type — *Illustrated edition designed by Jon Farrell · 2026*

---

## Affinity / InDesign document setup (manual start)

1. New document: **8.5 × 8.5 in**, facing pages ON for story spreads
2. Bleed: **0.125 in** all sides
3. Margins: start **0.5 in** (safety) — adjust per TEXT-OVERLAY-POLICY
4. Place Tier B art full-bleed; type = Cormorant Garamond (body) / Cinzel (titles)
5. Export: PDF/X-1a or high-quality print PDF · embed fonts · sRGB or convert per Lulu export preset

---

## Links

- [Book Creation Guide PDF](https://assets.lulu.com/media/guides/en/lulu-book-creation-guide.pdf)
- [Full bleed](https://help.lulu.com/en/support/solutions/articles/64000255584-what-is-full-bleed-)
- [Interior basics](https://help.lulu.com/en/support/solutions/articles/64000255590-interior-formatting-the-basics)
- [Casewrap cover](https://help.lulu.com/en/support/solutions/articles/64000308572-creating-your-hardcover-casewrap-cover)
- [Upload cover](https://help.lulu.com/en/support/solutions/articles/64000282777-upload-your-cover-file)

Local copies: `Xtraz/Lulu-Templates/`
