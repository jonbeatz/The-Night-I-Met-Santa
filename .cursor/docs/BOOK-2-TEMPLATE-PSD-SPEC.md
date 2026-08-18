# BOOK-2-TEMPLATE-PSD-SPEC.md — The Three Template PSD Blanks

**Why this file exists:** `BOOK-2-TEMPLATE.md` (Tier-1 clone list) says to copy
`spread-page-template.psd`, `single-page-template.psd`, and `book-covers-template.psd`
from `Xtraz\Adobe-Photoshop\`. On 2026-08-01 those blanks were swept into `Hold-v1\`
and the clone list silently broke. They were **restored on 2026-08-07** (hash-verified
copies back from `Hold-v1\`). Because they are gitignored binaries, this spec is the
insurance policy: the authoritative recipe to regenerate them if they ever go missing
again, so Book #2 can always materialize them on day 1.

*Created 2026-08-07 (Fable 5 audit implementation). Sources: `scripts/create_ps_page_templates.py`,
`scripts/create_spread_page_template_psd.py`, `AGENT-RUNBOOK.md` §PS templates,
`ISSUES-RESOLVED.md` §PSD blanks (2026-07-20 entries).*

---

## Fastest path — regenerate with the existing scripts

Prerequisites: **Photoshop open** + adobepy broker + dcc-mcp-photoshop on **:8766**.

```powershell
# from D:\Hermes\projects\The-Night-I-Met-Santa (or the Book #2 clone with paths updated)
python scripts\create_spread_page_template_psd.py   # → spread-page-template.psd
python scripts\create_ps_page_templates.py          # → single-page-template.psd + book-covers-template.psd
```

Both scripts write to `Xtraz\Adobe-Photoshop\`. For Book #2, update `OUT_DIR` (and any
trim-size constants if the new book is not 8.5" square) before running.

There is deliberately **no** `book-spine-template.psd` — Lulu supplies the casewrap
with exact spine width after the interior upload.

---

## Exact structure (build by hand in Photoshop if the scripts can't run)

Shared geometry — Lulu 8.5" square @ 300 DPI:

| Constant | Value | Meaning |
|---|---|---|
| PAGE | 2625 px | 8.75" full-bleed page |
| TRIM | 37.5 px | 0.125" bleed inset (cyan) |
| SAFE | 150 px | 0.5" safety inside trim (magenta) |
| Color mode | RGB 8-bit, sRGB | Lulu wants sRGB, not CMYK |
| Guides | at TRIM, TRIM+SAFE, PAGE−TRIM−SAFE, PAGE−TRIM (both axes, per page) | |

### 1. `single-page-template.psd` — 2625 × 2625 @ 300 DPI

Layer stack (bottom → top):

1. `white-bg` (renamed Background)
2. `paper-base` — full-canvas fill RGB (252, 250, 245)
3. `ART - full-bleed scene here` — empty
4. `TRIM 8.5in` — 3 px **cyan (0,180,220)** border box at 37.5 px inset, opacity 85%
5. `SAFETY 0.5in from trim` — 3 px **magenta (220,40,160)** border box at 187.5 px inset, opacity 85%
6. `CLOUD - watercolor wash optional` — empty
7. `TYPE zone - live Cormorant in InDesign` — empty (type is LIVE in InDesign, never baked)

### 2. `spread-page-template.psd` — 5250 × 2625 @ 300 DPI

Same stack as single-page, but across a facing spread (17.5 × 8.75"), plus:

- Guides + trim/safety boxes drawn **per page half** (left canvas 0–2625, right canvas 2625–5250)
- `FOLD (MOCK only — hide for finals)` — 2 px **orange** vertical line at x=2625 (center fold)
- Info text layer: "TNIMS spread template | 5250x2625 px @ 300 DPI | 17.5 x 8.75 in | sRGB |
  Lulu 8.5sq + 0.125 bleed | Cyan=TRIM | Magenta=SAFETY 0.5in | Orange=FOLD (hide on finals)"
- Type zones L and R (live type in InDesign)

### 3. `book-covers-template.psd` — 2625 × 2625 @ 300 DPI

Front **or** back cover art blank (same geometry as interior page):

1. `white-bg`
2. `paper-base` — RGB (252, 250, 245)
3. `ART - cover scene here (front OR back)` — empty
4. `TRIM 8.5in` — cyan border, opacity 85%
5. `SAFETY 0.5in from trim` — magenta border, opacity 85%
6. `HINGE hint 0.25in - mock only hide for finals` — two 2 px **orange (255,140,0)** vertical lines
   at 75 px inside trim on both left and right edges (covers either orientation), opacity 85%
7. `TITLE zone FRONT - Cinzel live in InDesign (hide on back)` — empty
8. `CREDITS zone BACK - live type in InDesign (hide on front)` — empty
9. `NOTE - final wrap+spine from Lulu after interior upload` — empty

---

## Usage rules (unchanged from Book #1)

- **Never edit the template.** Duplicate → Save As the working slug (e.g. `S03-eyes-met.psd`).
- Cyan/magenta/orange overlay layers are **MOCK-only** — hide before exporting plates.
- Export plates as **opaque RGB** (no alpha) for InDesign.
- Type stays **live in InDesign**; PS type layers are mock/position reference only.
