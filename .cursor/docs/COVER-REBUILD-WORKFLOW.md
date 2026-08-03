# Cover rebuild workflow — Lulu 5700×3075

**When to use:** Jon repositions / swaps Front or Back art in the panel PSD, then wants Wrap + Cover INDD + flipbook covers refreshed.

**Geometry (locked):** BACK **2813** | SPINE **75** | FRONT **2812** → wrap **5700×3075** @ 300 = **19×10.25″**

## Preference (Jon 2026-08-02)

**Layered when possible.** Front · Back · Wrap keep full editable layer trees (groups, type, smart objects, frames).  
**Bake only when required** — e.g. Cover INDD `art-no-type.png` (no live author/credits/QR), flipbook FRONT/BACK PNGs (from Cover export), or a one-off flat for soft-proof. Never flatten the Wrap SoT “for convenience.”

## Lesson locked (Jon 2026-08-02) — size first

Wrong canvas size at the start (legacy 2625 / 5475 placeholder) forced a full remake into Lulu **5700×3075**. Worth the day to fix; do not repeat.

| Do | Don't |
|----|--------|
| Lock **Lulu wrap px** (or panel px) as soon as spine/page count is known | Build “final” cover PSDs on a placeholder spine/size |
| Keep **keeper art oversized** (extra margin all sides) so cover-fit / floor-extend / chair nudge are moves, not regenerations | Generate keepers already tight to final crop |
| Edit Front/Back masters → rebuild Wrap | Treat Wrap as the place to invent panel composition |

**Rule of thumb:** paint/generate **bigger than the panel**, place as Smart Object / oversized BG, nudge inside the Lulu frame. Outpaint only when you truly need new pixels beyond the painting.

**Recipes work.** Unit `RECIPE.md` + dial folders let us remake plates that land nearly identical (e.g. back burgundy lineage, front floor-extend from scrubbed art). Prefer regenerate-from-recipe over guessing when a keeper must be rebuilt at new size.

## Three working PSDs only

| File | Role |
|------|------|
| `Xtraz/Adobe-Photoshop/FINAL-Master-PSDs/5700x3075-version/TNIMS-Cover-FRONT-FINAL-5700x3075.psd` | Front master (layered) |
| `…/TNIMS-Cover-BACK-FINAL-5700x3075.psd` | Back master (layered) |
| `…/TNIMS-Cover-Wrap-FINAL-5700x3075.psd` | Wide wrap = BACK + SPINE + FRONT |

**Rules**
1. Edit **Front or Back only** → then rebuild Wrap (never treat Wrap as the panel master).
2. Photoshop should show **only these three** cover docs when working covers. Close scratch tabs (`*FROM-FRONT-BUILD*`, `art-no-type-build`, etc.) **without saving**.
3. Title logo + Frame stay in PSD art. **Author / credits / QR are live or linked in Cover INDD** — do not bake them into `art-no-type.png`.

## Option A — Full refresh after Front/Back edit (recommended)

### 1. Rebuild Wrap PSD
```powershell
# Local (TNIMS repo root) — Photoshop must be open
& "C:\Program Files\Adobe\Adobe Photoshop 2026\Photoshop.exe" -r "D:\Hermes\projects\The-Night-I-Met-Santa\scripts\cover-rebuild-wrap-5700.jsx"
```
- Saves Front, duplicates **full layered** Front/Back art groups into Wrap (canvas-origin placement + clipping bases so overhang doesn’t spill into spine), saves Wrap, reopens the three SoT PSDs.
- Wrap top level: `02-LULU-GUIDES` · `FRONT` (group) · `FRONT-clip` · `BACK` (group) · `BACK-clip` · `SPINE`
- Result log: `scripts/_scratch/_cover_rebuild_wrap_result.txt`

### 2. Export art-no-type flat (for Cover INDD)
```powershell
& "C:\Program Files\Adobe\Adobe Photoshop 2026\Photoshop.exe" -r "D:\Hermes\projects\The-Night-I-Met-Santa\scripts\cover-export-art-notype-panels-5700.jsx"
python scripts/cover-compose-art-notype-5700.py
```
Or: `npm run book:cover:art-notype`

**art-no-type hides:** Type layers · QR · guides  
**art-no-type keeps:** painting · Frame · `cover-title-logo`  
**Output:** `Xtraz/Adobe-inDesign/FINAL-Master-inDD/links/TNIMS-Cover-Wrap-FINAL-5700x3075-art-no-type.png`

### 3. Cover INDD
- Open `TNIMS-Cover-FINAL.indd` (19×10.25)
- Relink / update `…art-no-type.png`
- Confirm live frames still present: `TYPE - FRONT author` · `TYPE - BACK author` · `TYPE - BACK credits`
- Confirm linked QR on **QR** layer (`Jon-Beatz-QR1-print-1200.png`)
- Save

### 4. Rebake flipbook covers (same composition as Cover)
1. Export Cover page PNG @ 300ppi → `Images/chopz/flipbook/_cover-wrap-export-for-flipbook.png` (guides hidden)
2. Crop BACK / FRONT panels → square cover-fit **2551²** → `flipbook-FRONT.png` / `flipbook-BACK.png`
3. Relink in `TNIMS-Flipbook-FINAL.indd` (p1 / p34)
4. Do **not** invent a flipbook-only crop bias — Cover is SoT

## Option B — Floor / canvas extend (art only)

When feet need more floor under a square painting **before** cover-fit:

1. Start from **art-only** base (no baked title logo / frame) — e.g. `Media/development/Cover/v14-MyPhotosho-v1/Cover-art-v3.png`
2. Bria Expand (or similar) **down only**; paste original top back pixel-perfect
3. Jon places into Front PSD as BG layer (`art-New-BG-fix` etc.), nudges X/Y
4. Then run **Option A**

Dial folder example: `Media/generated/mocks/Cover-front/v15b-floor-extend-notype/`

## npm helpers

```powershell
npm run book:cover:rebuild-wrap   # Photoshop JSX rebuild Wrap + reopen 3 SoT
npm run book:cover:art-notype     # export panels JSX + compose PNG
```

## Gotchas

| Symptom | Cause / fix |
|---------|-------------|
| Wide PSD shows only BACK / blank FRONT | Looking at a **scratch** tab (`FROM-FRONT-BUILD`, `art-no-type-build`). Close without save; open saved `TNIMS-Cover-Wrap-FINAL-5700x3075.psd` |
| Front art shifted into spine | Placed by **layer bounds** instead of **canvas origin**. Rebuild uses `copyMerged` (canvas-clipped) — use Option A |
| Double byline / soft QR in print flat | Forgot to hide type/QR in art-no-type. Re-run step 2 |
| Flipbook ≠ Cover | Rebake from Cover INDD export (step 4), don’t crop panels ad-hoc |
| Flipbook back clips tree/QR on right | **Expected** — square cover-fit crop of wrap panel. Print SoT = Cover wrap, not flipbook |
| Back mantel/curtains changed | Edit Back PSD (`Merged-Back-Cover-BG` / `covers`) → Option A full refresh |
| Interior PDF ~120 DPI on some pages | Opaque **RGBA** PNGs → ID flattens to tiles. Convert chopz to **RGB** before Lulu export |
| “Tiny image @ 12 DPI” on Cover PDF | Often the **QR** — check effective DPI at **placed size**, not full wrap width |

## Silhouette / logo vector (2026-08-03)

For B&W marks (e.g. `Images/references/sled1.psd`):

1. Upscale + mild blur + hard threshold (smooth source)  
2. **Illustrator Image Trace** (B&W · lower path/corner fidelity) → expand → SVG/AI/EPS  
3. Place EPS/AI into Photoshop as Smart Object  

Photoshop Work Path→Shape is fine for simple logos; complex organic silhouettes → Illustrator. Judge at 400% in AI, not browser PNG previews.

## Related

- Panel README: `Xtraz/Adobe-Photoshop/FINAL-Master-PSDs/5700x3075-version/README.md`
- Print authority: `AGENT-RUNBOOK.md`
- Order gate: `.cursor/docs/LULU-ORDER-CHECKLIST.md`
