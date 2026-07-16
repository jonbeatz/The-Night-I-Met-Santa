# BOOK-PLAN.md — The Night I Met Santa

Living plan for Jack Farrell’s picture book gift.

## Goal

Ship **one beautiful 8.5×8.5" hardcover** (Lulu) by **2026-08-15**, with option to print more later.

## Specs

| Item | Choice |
|------|--------|
| Trim | 8.5 × 8.5 in square |
| Color | Full color interior — export PDF **sRGB** (Lulu native; not CMYK-first) |
| Bleed | 0.125 in |
| Safety | ≥ **0.5"** from trim for text/faces (≥ 0.625" from bleed edge) |
| Gutter extra | None needed @ 32 pages (< 60) — still keep faces off absolute center fold |
| Binding | Casewrap hardcover for gift; paperback optional for cheap proof |
| Paper / ink | Lulu **Premium Color** (heavier ~80# when available) for heirloom gift |
| Page count target | **32** (even; see v6 plan) |
| Single page art @ 300 DPI | **2625 × 2625 px** (8.75" with bleed) |
| Spread master @ 300 DPI | **5250 × 2625 px** → split L/R |
| POD | Lulu primary |
| v6 plan | `.cursor/plans/2026-07-14-book-v6-rebuild.plan.md` |

## Pipeline

> **Full dialed system:** `.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`  
> **Winner image path:** fal `nano-banana-pro/edit` + style refs (not Flux default).

```
poem-clean.txt
    ↓
PAGE-PROMPT-BIBLE + ILLUSTRATION-STYLE
    ↓
fal nano-banana-pro/edit (+ style refs) → Media/generated/…
    ↓
Jon approve → promote → Media/
    ↓
composite_pages.py  →  Pages/page-NN.jpg  (illustration + cloud wash + text)
    ↓
book-final.typ      →  Output/*-INTERIOR.pdf
    ↓
build_cover_v2.py   →  Output/*-COVER-*.pdf  (or AI-titled cover from test-covers)
    ↓
Lulu upload → proof → gift copy
```

## Stanza → illustration map (from composite_pages.py)

| # | Media file | Text placement hint |
|---|------------|---------------------|
| 1 | scene-01-the-sneak-LANDSCAPE | bl |
| 2 | scene-02-at-the-door | tr |
| 3 | scene-02b-sneak-up-santa-LANDSCAPE | bl |
| 4 | scene-04b-santas-splendor-LANDSCAPE | bl |
| 5 | scene-05-the-chat-PORTRAIT | br |
| 6 | scene-06-cocoa-reveal-SQUARE | tl |
| 7 | scene-06b-santas-stories-LANDSCAPE | bl |
| 8 | scene-07-camera-dash-PORTRAIT | bc |
| 9 | scene-08b-the-dash-santa-gone-PORTRAIT | tr |
| 10 | scene-08-the-search-PORTRAIT | bl |
| 11 | scene-10b-the-flue-and-chair-PORTRAIT | br |
| 12 | scene-09-the-note-LANDSCAPE | bl |
| 13 | scene-12b-tearing-open-PORTRAIT | br |
| 14 | scene-14b-what-he-wants-message-LANDSCAPE | tl |
| 15 | scene-10-santas-message-LANDSCAPE | bc |

Adjust placements after quiet-zone review against the actual art.

## Layout versions (history)

| Ver | Result | Keep? |
|-----|--------|-------|
| v1 fpdf | Separate text/image pages | Archive only |
| v2 Typst | Interpolation bugs | Archive |
| v3 Typst hard panel | Opaque white box | Reject |
| v4 Typst wash PNG | Checkerboard alpha | Reject |
| v5 Pillow soft rect | Soft rectangle fog | Reject shape; keep “pre-compose” idea |
| **v6 (next)** | Cloud mask / bleed spread | **Build this** |

## Print checklist (before upload)

- [ ] Even page count
- [ ] 300 DPI images
- [ ] Bleed on full-bleed art
- [ ] Text inside safety zone
- [ ] Fonts embedded / rasterized into page JPEGs OK
- [ ] Separate interior PDF + cover PDF
- [ ] Spine width = f(page count, paper) from Lulu template
- [ ] Digital proof reviewed on screen; physical proof if time

## Related docs

- `CONTINUE-HERE.md` — session handoff / next actions  
- `Book-Findings.md` — research detail  
- `IMAGE-WORKFLOW.md` — generation pipeline  
- `Images/references/layout/` — visual targets  
