# ISSUES-RESOLVED — The-Night-I-Met-Santa

Append-only log of **problems we hit** and **verified fixes**. Newest first.

**Operator trigger:** say **`log fixes`** or **`log fix`** — agent appends an entry here from the session (do not wait for interactive CLI).

**CLI (optional):** from repo root  
`npm run log:fix -- --issue "..." --cause "..." --solution "..."`

**Also promote** durable layout rules into `AGENT-RUNBOOK.md` when a fix becomes standard procedure.

---

## 2026-07-20 — InDesign shows empty frame / red + but no title text (P01)

| | |
|---|---|
| **Symptom** | Photoshop MOCK title visible (Cinzel 36); InDesign shows a small green frame with **overset `+`** and no readable glyphs; Character panel may show Minion 12 defaults |
| **Root cause** | (1) `create_text_frame` UXP helper can drop an **orphan** off the page / pasteboard (story exists in Layers but not on page). (2) Frame too short for 36 pt → **overset**. (3) Earlier unit/placement mistakes made a tiny bottom-left box. (4) Selecting the frame with Type tool shows app defaults (Minion 12), not the story’s real Cinzel |
| **Resolution** | Never rely on `create_text_frame` alone. Use **`page.textFrames.add(Type layer)`** with rulers **inches**, full-width SAFETY frame (~**5.55–7.35 × 0.5–8.0 in** for P01), style characters explicitly (Cinzel **36** / Cormorant **18** / PoemCharcoal), `bringToFront`, confirm `overflows === false` + `parentPage` is the book page. Prefer **PS-first**; mirror into ID after MOCK is close |
| **Verify** | Jon sees title on art (2026-07-20) · Layers Type story on page 1 · no red `+` · PS Character 36 matches ID 36 |

---

## 2026-07-20 — Photoshop text API size wrong at 300 ppi (36 → 8.64)

| | |
|---|---|
| **Symptom** | Agent sets MOCK-TYPE to **36 pt** via `createTextLayer` / `set_character_style`; Character panel shows **~8.64 pt** (or glyphs look tiny vs InDesign 36) |
| **Root cause** | High-level Photoshop text API at **300 ppi** scales size by **72/300**. `36 × 72/300 = 8.64` |
| **Resolution** | Pass **`desired_pt × (300/72)`** to the high-level API (36 → **150**) **or** set size with batchPlay `pointsUnit: desired_pt`. Always read Character panel before matching InDesign. Never **Free Transform** type (breaks pt parity — can show 4 pt while glyphs look huge) |
| **Verify** | Character panel = intended pt · bounds height ~matches print size · ID live type same pt |

---

## 2026-07-20 — PS MOCK type vs InDesign live type look different (P01)

| | |
|---|---|
| **Symptom** | Title MOCK starts way top-left / wrong size vs InDesign; constant re-nudge between apps |
| **Root cause** | Agent defaulted MOCK to canvas origin; no shared title defaults; Free Transform; ID rebuilt at different pt/spot than MOCK |
| **Resolution** | Locked shared defaults: title **Cinzel Decorative 36/42** · author **Cormorant 18/24** · `#2C2C2C` · start **lower-center SAFETY** (~y **1729 px** on 2625) · **Move** only · **PS-first** design desk → ID print desk mirrors. Docs: `PAGE-BUILD-WORKFLOW.md` §1b + §7 |
| **Verify** | Side-by-side PS/ID · same band on page · Jon confirmed ID text visible after overset fix |

---

## 2026-07-20 — First create of PSD / INDD: Jon saves once, then agent edits

| | |
|---|---|
| **Symptom** | Agent hangs on InDesign “Save changes to Untitled…?”; or `book-interior-v1.indd` lands as **A4** instead of **8.5×8.5** while `p03-dedication-smoke.indd` looks correct |
| **Root cause** | Modal Save/Close dialogs **block** the UXP/COM bridge until dismissed. First `create_document` / Save As without a clear human save can attach the wrong Untitled (A4 leftover) or leave units ambiguous (picas vs inches) |
| **Resolution** | **Operator first-save rule:** Jon creates or confirms the blank (or agent opens template) → **Jon Save As** to the final path under `Xtraz/Adobe-Photoshop/` or `Xtraz/Adobe-inDesign/` → dismiss any dialog → say **ready** → agent then places art, type, resize, layers. Prefer verifying size against a known-good smoke (`p03-dedication-smoke.indd` = 8.5²) before filling the book doc |
| **Verify** | Active doc path is the intended filename · page **8.5×8.5 in** · bleed **0.125** · no blocking Adobe modal |

**Future:** If a Save/Close/font/link popup appears — **Jon clicks it**, then **ready**. Don’t leave modals open for the agent. Interrupt only if hung >1–2 min with a visible dialog.

---

## 2026-07-20 — Light project cleanup (docs + folders)

| | |
|---|---|
| **Symptom** | Stale maps (32-page/Pillow), duplicate Findings/Verdict, scratch scripts & Image noise cluttering creative area |
| **Root cause** | Fast iteration left superseded docs live; fleet + book docs mixed in reading lists |
| **Resolution** | Archived superseded → `_archive/docs/` with stubs; parked `scripts/_scratch/` + `_archive/images-scratch/`; `Pages/` marked deprecated; TRUTH/AGENTS/CONTINUE-HERE aligned to PAGE-BUILD + BOOK-PAGE; root Findings/Verdict kept as historical with banners |
| **Verify** | `Images/` = `references` + `chopz` only · AGENTS list has no BOOK-PLAN · stubs resolve |

---

## 2026-07-20 — PS ↔ InDesign size parity + docs triggers + Klein D2 / no fake gutter

| | |
|---|---|
| **Symptom** | Unclear if PS fonts/images match ID; risk of constant re-scale; MOCK type vs poem size confusion; unsure log fixes vs update docs |
| **Root cause** | 72 dpi metadata myth; MOCK defaults were matter-sized (30pt) while poem lock is 20/26; workflow harvest triggers not spelled out next to page map |
| **Resolution** | Locked **PAGE-BUILD-WORKFLOW.md §1b** (2625/5250 full-bleed = 300 DPI; pt sizes by role; full-canvas clouds). Poem MOCK = **20/26**; matter = **30**. Spreads: no fake gutter in art. Klein mocks = **4B + Dial D2 only**. Docs: **`update docs`** = system harvest · **`log fixes`** = ISSUES card · §11 |
| **Verify** | Side-by-side PS/ID at 100% on next poem page; RECIPE lists D2; exported spread has no center fold |

---

## Playbook — Page build loop (dialed 2026-07-20)

**Canonical doc:** `.cursor/docs/PAGE-BUILD-WORKFLOW.md`  
**Mocks home:** `Media/generated/mocks/{unit}/vNN/` + mandatory **`RECIPE.md`** (prompt · service · model · refs · verdict)  
**Scoreboard:** `Media/generated/mocks/_INDEX/README.md`

### Loop (short)

1. Generate art → `mocks/…/vNN/art.png` + RECIPE  
2. Duplicate blank PSD → `Xtraz/Adobe-Photoshop/{slug}.psd` · place on **ART** · guides on  
3. **Close source PNG tab** (keep tabs clean)  
4. Add **MOCK-TYPE** preview → Jon positions + cloud brush  
5. Save PSD → place into InDesign at correct book page  
6. Promote winner → `Media/approved/` + INDEX + recipe sidecar  

### MOCK-TYPE defaults (PSD preview — mirrors InDesign)

| Role | Spec |
|------|------|
| Poem | Cormorant Medium **20/26** · tracking +5 · `#2C2C2C` |
| Dedication / short matter | Cormorant Medium **30/~40** · `#2C2C2C` (p03 dial) |
| **Title (P01)** | Cinzel Decorative **36/42** · author Cormorant **18/24** · `#2C2C2C` · lower-center SAFETY (~y **1729** on 2625) |
| Layer | `MOCK-TYPE - {slug} (preview)` |
| Position | **Move** only — never Free Transform |
| PS API @300ppi | Pass `pt×(300/72)` to high-level API **or** batchPlay `pointsUnit` |

Do not ship raster MOCK-TYPE. Full-canvas cloud brush → RGBA export → full-bleed place = 1:1 with PS (`PAGE-BUILD-WORKFLOW.md` §1b).  
**PS-first:** dial MOCK in Photoshop → then mirror live type in InDesign.

### Size parity (PS ↔ ID)

| Art | Place in ID | Notes |
|-----|-------------|-------|
| **2625×2625** | 8.75″ bleed box | = 300 DPI; ignore PS 72 dpi tag |
| **5250×2625** | 17.5″ × 8.75″ (or L/R 2625² chops) | same |

### Spreads — no fake gutter

Art + exports: **seamless**. Orange FOLD guide = screen only. Klein/Banana prompts include gutter negatives (`IMAGE-LANE-PROMPTS.md`).

### Symptom → fix (this session + P01 dial)

| Symptom | Root cause | Resolution | Verify |
|---------|------------|------------|--------|
| PNG tabs pile up | Source art left open after place | Close PNG as soon as ART owns pixels | Only working PSD open |
| MOCK type tiny / wrong color | Agent used wrong size / not #2C2C2C | Poem **20/26** · matter **30** · title **36/18** · **#2C2C2C** | Eye-check vs ID |
| PS Character shows 8.64 not 36 | High-level API ×72/300 at 300ppi | Pass `pt×(300/72)` or batchPlay points | Character = intended pt |
| Type way top-left / hard to find | Agent placed at canvas origin | Default **lower-center SAFETY** | Glyphs inside magenta |
| Free Transform → weird pt | Scaled type layer | **Move** only | Panel pt = visual size |
| ID empty box + red `+` | Overset / orphan `create_text_frame` | `page.textFrames.add` on Type · full frame · check `overflows` | Jon sees live title |
| PS look ≠ ID | Wrong pixels, scaled place, or MOCK≠live size | Lock §1b · place full-bleed · match pt by role · **PS-first** | Side-by-side 100% |
| First PSD/INDD hang or A4 | Adobe modal / Untitled wrong size | **Jon Save As** once → **ready** → agent edits | Path + 8.5² + bleed 0.125 |
| Can’t recreate a liked mock | Prompt/model not recorded | Every `vNN` gets **RECIPE.md** + D2 vs master | Open recipe next to art.png |
| Character drift | Missing G0 refs on gen | Attach boy/santa locks every boy/Santa call | Compare to G0 side-by-side |
| Fake spine in spread art | Model drew mockup fold | Negatives + hide orange fold before export | No center line on plate |

---

## Playbook — Export each Photoshop layer as JPG (dialed 2026-07-20)

**Skill:** `.cursor/skills/Photoshop-Layer-Export/SKILL.md`  
**Script:** `scripts/ps-export-layers-jpg.py` · `npm run ps:export-layers`  
**Setup:** `tools/layout-mcp/PHOTOSHOP-SETUP.md`

### Method (solo eyeball)

1. Open source `.psd` / `.psb` in Photoshop (broker live)
2. Hide **all** layers
3. Starting from the **visible** layer (or `--start`), walk **up** the Layers panel
4. For each layer: show **only** that layer → `doc.export(..., format="jpg", as_copy=True)` → `{layer-name}.jpg`
5. Output folder: Jon’s path (example: `Images/references/Pugicorn-Book-Refrence/cropped/`)

### Verified

| Source | Out | Result |
|--------|-----|--------|
| `Pugicorn-Book-Refrence.psb` (1800×1466) | `…/cropped/Pugicorn-a.jpg` … `Pugicorn-r.jpg` | **18/18** |

### Symptom → fix

| Symptom | Resolution |
|---------|------------|
| Need every layer as a file | Run this playbook — not File → Export As once |
| Wrong walk order | Panel **up** = toward top = lower `doc.layers` index |
| Smart Object blank frame | Short settle after show; export composites doc pixels |
| Windows print Unicode crash | ASCII logs · `PYTHONIOENCODING=utf-8` |

---

## Playbook — Photoshop agent MCP (LIVE 2026-07-20)

**Path:** adobepy UXP + `dcc-mcp-photoshop` — **not** COM.  
**Doc:** `tools/layout-mcp/PHOTOSHOP-SETUP.md`

| | |
|---|---|
| Broker | `:47391` |
| MCP | `http://127.0.0.1:8766/mcp` |
| Plugin | `com.adobepy.bridge.photoshop` via UDT Load & Watch |
| Prefs | **Enable Developer Mode** only (Generator / Remote Connections off) |
| npm | `npm run layout:photoshop-mcp` |
| **Default save folder** | `Xtraz/Adobe-Photoshop/` (`D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop`) — agent saves PS files here |
| **PSD blanks** | `spread-page-template.psd` · `single-page-template.psd` · `book-covers-template.psd` — see playbooks below (**no** spine-only PSD) |

**Smoke PASS:** open `spread-01-eyes-met-5250x2625-v3.psd` → 5250×2625 · 9 layers · `sessions:1` · `dcc:true`.

**Cold-start gotcha (2026-07-20):** Cursor `photoshop` MCP **green** ≠ bridge live. Truth = broker `"sessions":≥1` + `/v1/readyz` `"dcc":true`. If UDT shows **Watching** + PS panel open but `sessions:0` → **UDT Reload** on Adobe Python Bridge (not full PS restart). Order: start `npm run layout:photoshop-mcp` **then** Reload plugin so WebSocket reattaches. After `load_skill`, Cursor tool picker can lag — use HTTP `/v1/call` if `CallMcpTool` 404s.

**Rejected:** loonghao / alisaitteke COM — `0x80080005` (same class as InDesign COM). Registry has PS **200.0**; ProgID OK; COM runtime broken. Lesson: new Adobe app automation on this PC → **UXP first**.

---

## Playbook — Photoshop PSD blanks (locked 2026-07-20)

All under `Xtraz/Adobe-Photoshop/`. **RGB @ 300 DPI.** Colors: **cyan = TRIM** · **magenta = SAFETY** · **orange = MOCK** (fold or hinge — hide for finals).

| File | Canvas | Layers (bottom → top) | Use |
|------|--------|----------------------|-----|
| **`spread-page-template.psd`** | 5250×2625 | white-bg → paper-base → ART → trim/safety → fold → cloud → type L/R | Facing spreads · hide orange fold for finals |
| **`single-page-template.psd`** | 2625×2625 | white-bg → paper-base → ART → TRIM → SAFETY → cloud → type | One interior page |
| **`book-covers-template.psd`** | 2625×2625 | white-bg → paper-base → ART → TRIM → SAFETY → hinge hints → TITLE / CREDITS | Front **or** back cover art · final wrap from Lulu after interior |
| ~~spine~~ | — | — | **Skipped:** spine width from Lulu casewrap after interior upload; not a separate working PSD |

**Shared use:** Duplicate → Save As · paint **ART** · type **live in InDesign** (Cormorant / Cinzel) — never bake poem/title into the PSD.

Also: `tools/layout-mcp/PHOTOSHOP-SETUP.md` · `Xtraz/Adobe-Photoshop/README.md` · `AGENT-RUNBOOK.md`

---

## Playbook — Photoshop chops → InDesign (locked 2026-07-20)

Living “how we build spreads.” Dated entries below are the incident history; **this section is the operator cheat sheet.** Update when something sticks.

### 1) Default loop (Jon + agent)

| Step | Who | What |
|------|-----|------|
| 1 | Jon/Agent | Start from **`spread-page-template.psd`** (spreads) or **`single-page-template.psd`** (singles); covers → **`book-covers-template.psd`** → Save As working `{slug}.psd` |
| 1b | Agent | Place art on **ART** → **close source PNG tab** immediately (see `PAGE-BUILD-WORKFLOW.md`) |
| 1c | Agent/Jon | Add **MOCK-TYPE** preview — poem **20/26** · matter **30pt** · `#2C2C2C` · Jon positions + **full-canvas** cloud brush |
| 2 | Jon | Export **MOCK** (full composite) + **chops** into `Images/chopz/` — see naming + export options below |
| 3 | Agent | Facing pages in InDesign → place chops → optional **MOCK-REF @ ~35%** to align → hide MOCK |
| 4 | Agent | Recreate poem as **live Cormorant Garamond Medium 20/26 tracking +5, centered, #2C2C2C** (never ship raster poem) |
| 5 | Jon | Eye-check vs MOCK (magenta margins = safety); nudge; approve → next spread |

**Why this split:** PS owns the look; InDesign owns print type, layers, Lulu PDF. Matches gift-book quality and keeps text editable.

### 2) Pixel sizes & “72 DPI” (don’t panic)

| Canvas | Pixels | Use |
|--------|--------|-----|
| Single page + bleed | **2625 × 2625** | One page of art @ 300 DPI when placed at 8.75″ |
| Full spread + bleed | **5250 × 2625** | Two-page continuous scene @ 300 DPI when placed at 17.5″ × 8.75″ |

Photoshop’s **72 dpi** tag is metadata only. **Pixel count** is what matters. Same 5250×2625 placed full-bleed = print-correct 300 DPI.

**Prefer PNG** for production links (art + overlays). JPG is fine for a quick MOCK; JPG art looks softer than PNG of the same pixels (pages 2–3 PNG vs 4–5 JPG was the crispness gap).

### 3) Where things must live on the page

```
BLEED 8.75″  →  art / paintFrame / clouds may go to the edge
TRIM  8.5″   →  final cut
SAFETY 7.5″  →  magenta/pink margin box = 0.5″ in from trim
                 KEEP: faces, poem glyphs, important details
```

- **No extra gutter** for this book (&lt;60 pages). Still keep eyes/faces off the fold by composition.
- **Safety = printed ink**, not empty text-frame padding. Center-aligned type OK if **letters** sit inside magenta box even when the green frame touches the margin line. (See safety entry below.)

### 4) Chop naming (in `Images/chopz/`)

| File pattern | Role |
|--------------|------|
| `spread-NN-…-MOCK-5250x2625…` | Full composite reference (align target) |
| `…-LEFT` / `…-RIGHT` (2625²) or `…-SPREAD` (5250×2625) | Art |
| `textCloud-…` | Soft wash under type (Cloud layer) |
| `paintFrame-…` | Painterly vignette over whole spread (Frame layer) |
| `text-…` / `text2-…` | **Guides only** — rebuild in InDesign |

### 5) textCloud / overlay export — two good options

The bug we hit: a **medium canvas** with the glow already in the top-left **plus** InDesign squeezing that file into a small inset = double positioning, match broken.

**Option A — Easiest (recommended)**  
Export at **full left-page 2625×2625** (or **full spread 5250×2625** if the wash spans both pages):

- Paint the cloud **exactly where it should sit** on that canvas  
- Leave everything else **transparent** (RGBA)  
- InDesign places it **full-bleed** on that page/spread → lands like the MOCK automatically  

**Option B — Tight crop**  
Export **only** the cloudy pixels (minimal empty margin). Agent places/scales that small piece to match the MOCK. More nudge work; fine if you prefer smaller files.

**Avoid:** Half-page file with cloud pre-positioned in a corner **and** asking InDesign to also shove it into a tiny inset box.

Same rule for other positioned overlays (glows, soft fades): either **full canvas with composition baked in**, or **tight crop + explicit place** — not both.

### 6) paintFrame (spread vignette) — design decision

- **Keep it** on strong emotional spreads (eyes-met, sit-here, note, blessing): gift-book plate feel, matches gouache, pairs with text cloud.  
- **Not required on every spread** — quiet pages can go full-bleed so the motif doesn’t get repetitive.  
- Export as **5250×2625 RGBA**; center transparent so art shows through. Place on **Frame** layer (top). Black in a thumbnail ≠ opaque — trust alpha.

### 6b) Gutter / “fake middle” line — LOCKED (Jon 2026-07-20)

**Final print art = seamless spread. No fake fold line.**

| Use | Fake vertical gutter/shadow down the center? |
|-----|-----------------------------------------------|
| **PS MOCK / screen preview** (optional) | OK — helps you *see* where the book will fold |
| **Final LEFT / RIGHT / SPREAD art for InDesign → Lulu** | **Never** — continuous painted scene across the gutter |

**Why:** The physical book already creates a real fold. A baked-in dark line + shadow prints as a second “gutter,” can misalign with the true spine, and looks like a mockup artifact. Keep gifts, garland, etc. continuous; place important faces/hands slightly off-center so the real fold doesn’t bisect eyes.

**Prompts (required on every spread gen):** append **SPREAD master add-on** + gutter negatives from `ILLUSTRATION-STYLE.md` / `IMAGE-LANE-PROMPTS.md` / `PAGE-PROMPT-BIBLE.md`. Agents must not run `image:fal:spread` without them.

**Agent check:** If a chop or SPREAD master shows a hard center rule/shadow that isn’t in the scene lighting, flag it and ask Jon for a seamless export before placing as final.

### 7) InDesign layer stack (top → bottom)

**Frame → Type → Cloud → Art**

If MCP can’t reorder layers, Jon drags **Frame** above **Type** once in the Layers panel.

### 8) Agent place recipe (fast path)

1. Facing pair (even left / odd right)  
2. Art L/R → place once → `resize_page_item` **630×630**  
3. textCloud → place once per **export option** (full-bleed if Option A; natural/MOCK match if Option B)  
4. Live poem type — **LOCKED defaults:**
   - Font: `Cormorant Garamond\tMedium`
   - Size / leading: `"20pt"` / `"26pt"`
   - Tracking: `5`
   - Align: center · Color: #2C2C2C / PoemCharcoal
5. paintFrame on **spread** → resize **1260×630**  
6. Optional MOCK-REF @ 35% → align → hide/delete  
7. `list_page_items` + save — **do not re-place** when unsure (duplicates)

**Points cheat sheet:** 8.75″ = 630 pt · spread 17.5″ = 1260 pt · always `CENTER_ANCHOR` or set `geometricBounds` in inches after place.

### 9) MCP gotchas (short)

| Prefer | Avoid |
|--------|--------|
| Place once + resize Image sibling | Retry-place / delete “empty” rect blindly |
| `list_page_items` to verify (`execute` often returns `null`) | Trusting place_image “success” alone |
| Live text via JSX on page | `create_text_frame` orphans on pasteboard |
| Inspect PNG / trust Jon on transparency | Inventing black backgrounds from thumbnails |

---

## 2026-07-20 — Photoshop MCP: Cursor green / UDT Watching but `sessions:0` / `dcc:false`

**Symptom:** Photoshop + UDT **Watching** (`com.adobepy.bridge.photoshop`) + Adobe Python Bridge panel open/checked + Cursor `photoshop` MCP green (~32 tools) — but agent smoke failed: broker `"sessions":0`, `/v1/readyz` → `dcc:false` (503).

**Root cause:** `npm run layout:photoshop-mcp` restarted the adobepy broker **after** the UXP plugin had already connected. Plugin UI stayed “loaded”; WebSocket to `:47391` did not reattach. Cursor green only means MCP HTTP `:8766` is up — not that DCC is ready.

**Resolution:**
1. Keep broker/MCP running (`layout:photoshop-mcp`).
2. In UDT → **Reload** on **Adobe Python Bridge for Photoshop** (leave InDesign alone). Full Photoshop restart usually unnecessary.
3. Confirm Plugins → Adobe Python Bridge still checked / panel open.
4. Re-smoke: `sessions≥1`, `dcc:true`, then `load_skill photoshop-document` + `get_document_info` (HTTP `/v1/call` OK if Cursor tools lag).

**Verify (PASS 2026-07-20):** `sessions:1` · `dcc:true` · active doc `spread-01-eyes-met-5250x2625-v3.psd` 5250×2625 · 9 layers.

---

## 2026-07-20 — `layout:photoshop-mcp` fails: PowerShell ParserError on em dash

**Symptom:** `npm run layout:photoshop-mcp` exits immediately with `Unexpected token 'extract'` at `start-photoshop-mcp.ps1` line with `Missing adobepy.exe — extract…`.

**Root cause:** Unicode em dash (`—`) in a `throw` string; PowerShell mis-parsed the file encoding and treated following words as code.

**Resolution:** Use ASCII hyphens only in that script’s throw messages (`Missing adobepy.exe - extract…`). Prefer ASCII in all PowerShell scripts under `tools/layout-mcp/`.

**Verify:** Script starts broker `:47391` + MCP `:8766`; log shows `MCP server started at http://127.0.0.1:8766/mcp`.

---

## 2026-07-20 — Safety zone: text **frame** vs actual **glyphs** (centered type OK)

**Symptom / question:** Page 4 poem text frame left edge was ~0.10″ from trim (outside the 0.5″ safety number from `geometricBounds`). Jon noted type is **center-aligned**, so the words sit inside the pink margin box even when the green frame touches the margin line. Screenshot confirmed magenta margins + centered ink.

**Root cause:** Agent/preflight was judging **frame bounds** only. Lulu safety cares about **printed ink** (letters, faces), not empty padding inside a text frame.

**Resolution (locked):**
1. **Magenta/pink margin rectangle** in InDesign = **0.5″ safety** from trim. Use the screenshot / eye-check when bounds look “out.”
2. For **center-aligned** (or right-aligned) poem frames: if the **leftmost/rightmost glyphs** sit **inside** the pink box → **acceptable**. Do **not** force a move solely because the frame edge hugs or crosses the margin.
3. Still flag / nudge if any **letter** sits outside the pink box, or if alignment might later change to **left-align** (then frame left edge = real risk).
4. Prefer keeping the frame inside safety when easy — but centered type with clear inset from the margin is print-OK.

**How to verify:** Look at the longest line’s first/last letter vs the magenta guide — not only `geometricBounds[1]` of the TextFrame.

**Related:** Safety = 0.5″ from trim (`INDESIGN-PRODUCTION-WORKFLOW.md`). Art may bleed; type/faces should not. See **Playbook §3**.

---

## 2026-07-20 — Locked workflow: PS MOCK + chops → InDesign match → live type

**Decision:** Default production loop for story spreads. **Full cheat sheet moved to Playbook at top of this file** (export options, paintFrame, sizes, safety, agent recipe).

**One-liner:** Jon PS MOCK + chops → agent InDesign match → live Cormorant → Jon approves.

**Pointers:** Playbook §§1–9 · `AGENT-RUNBOOK.md` placement section · `INDESIGN-PRODUCTION-WORKFLOW.md` for Lulu numbers.

---

## 2026-07-20 — Pages 4–5 mockup build still slow (chop → facing spread)

**Symptom:** Building pages 4–5 to match `Images/chopz` MOCK (LEFT/RIGHT art + textCloud + paintFrame + live Cormorant) took longer than a simple place should. Pages 2–3 left intact for comparison.

**What actually worked (keep this recipe):**
1. **Facing pages:** even/odd pair (4 left + 5 right). `add_page` once if needed.
2. **Art:** `execute_indesign_code` → rectangle on **Art** layer → `place(LEFT|RIGHT path)` with bleed bounds `[-0.125, -0.125, 8.625, 8.625]` (page-local). Then **`resize_page_item`** on the oversized **Image** sibling: `width/height: 630` (8.75″ × 72), `CENTER_ANCHOR`. Prefer **PNG** links for crispness.
3. **Cloud:** place once; match MOCK — prefer **full-page Option A** export, or natural asset size from top-left bleed. **Do not** squeeze a pre-composed cloud into a tiny inset (supersedes early 511×259 inset habit).
4. **Live text:** create text frame **via `execute_indesign_code` on the target page** (not `create_text_frame` alone — it can land off-page / orphan a story). Style: Cormorant Garamond 14pt, center OK, PoemCharcoal / `#2C2C2C`. Skip raster `text-*.png` chops. Safety = **glyphs** vs magenta margins.
5. **paintFrame:** place on **spread** (`page.parent`) with bounds `[-0.125, -0.125, 8.625, 17.125]`; resize Image to `1260 × 630` (17.5″ × 8.75″). Asset center is **RGBA transparent** (verified). Design: use on big emotional spreads; optional not every page.
6. **Verify with `list_page_items`** after each place — do not trust `execute_indesign_code` return (`null` is normal).

**What burned time (don’t repeat):**
| Slow path | Why |
|-----------|-----|
| `place_image` with negative mm bleed (`x: -3.175`) | “objects leave the pasteboard” — fails |
| Relying on `execute_indesign_code` `__result` objects / layer `.name` loops | Bridge often errors (`Cannot read properties of undefined`) or returns `null` |
| `create_text_frame` with `pageIndex` | Can create orphan story on pasteboard; page shows 0 text frames |
| `frame.fit(FitOptions…)` after place | Often no effect when Image lists as **sibling**; use **`resize_page_item`** |
| Fighting `LocationOptions` / layer reorder in JSX | Enum often undefined in UXP bridge; **ask Jon to drag Frame layer to top** (1 click) |
| Moving graphic **and** parent rectangle to a new layer | “Cannot move subselected items” — move **parent rectangle only** |
| Re-placing when unsure | Same duplicate trap as textCloud entry below |
| Judging safety from frame bounds only | Centered glyphs can be inside magenta while frame hugs margin |

**Point-size cheat sheet (resize_page_item uses points):**

| Target | inches | points (×72) |
|--------|--------|--------------|
| Single page + bleed | 8.75 × 8.75 | **630 × 630** |
| Full spread + bleed | 17.5 × 8.75 | **1260 × 630** |

**Layer ideal (top → bottom):** Frame → Type → Cloud → Art. If MCP can’t reorder, operator drags **Frame** above **Type** in Layers panel.

**Verify:** Spread matches MOCK; live text only; one of each linked chop; MOCK-REF hidden. See **Playbook** for export options + ongoing rules.

---

## 2026-07-20 — InDesign UXP: textCloud placed 3× / slow / “black background” assumption

**Symptom:** Placing `Images/chopz/textCloud-5250x2625-v1.png` on page 2 took many minutes; Cloud layer showed the PNG **three times**; agent wrongly claimed the PNG had a black background (it is transparent).

**Root cause:**
1. **`place_image` / `place_file_on_page` unreliable** — layer errors or “success” with nothing on the page.
2. **`frame.place(path)` splits into** an empty **Rectangle** at correct bounds **plus** a sibling **Image** with huge pasteboard bounds. `execute_indesign_code` often returns `null`, so agents re-place instead of verifying.
3. **Deleting the “empty” rectangle** can remove the linked graphic entirely → another place cycle → **duplicate Cloud-layer links**.
4. Thumbnail/description bias led to a false “black fill” diagnosis; asset is soft white on transparent.

**Resolution (verified):**
1. Clear **all** Cloud-layer duplicates first (`get_document_layers` → Cloud `pageItemCount` should drop to 0).
2. Place **once** via `execute_indesign_code`: rectangle on Cloud layer → `place(path)` → **do not delete** the placement rectangle blindly.
3. Resize the oversized **Image** with `resize_page_item` / set bounds to match MOCK (prefer full-page Option A export going forward — see Playbook §5).
4. Confirm Cloud layer has **one** linked PNG; save `.indd`.
5. Never invent asset fill from a description — open/inspect the PNG or trust Jon’s note.

**Do not:** retry-place when unsure; each retry stacks another Cloud copy.

**Verify:** Layers panel → Cloud → single `<textCloud-…png>`; poem text still above cloud; art still below.

---

## 2026-07-20 — Photoshop MCP: COM dead; UXP adobepy LIVE

**Symptom / goal:** Wire Cursor → Photoshop so agent can help with MOCK/chop setup. Guide listed loonghao / alisaitteke COM MCPs.

**Root cause:** On this PC, Photoshop **2026** COM fails (`0x80080005` Server execution failed / GetActiveObject unavailable) even though registry **200.0** and ProgIDs exist. Same failure class as InDesign COM. loonghao also lacks `PS_VERSION` map for 2026→200 (tops at 2025→190). alisaitteke Windows path is still COM (UXP plugin = Neural Filters only).

**Resolution (verified):**
1. Install **adobepy 0.5.2** + **dcc-mcp-photoshop 0.1.37** (UXP WebSocket).
2. Stage bridge → `tools/layout-mcp/photoshop-adobepy/bridges/photoshop/`.
3. Photoshop prefs: **Enable Developer Mode** only (not Generator / Remote Connections).
4. UDT Load & Watch `com.adobepy.bridge.photoshop` → panel open.
5. `npm run layout:photoshop-mcp` → broker `:47391` + MCP `:8766/mcp`.
6. Smoke: `sessions:1`, `dcc:true`, read `spread-01-eyes-met-5250x2625-v3.psd` (5250×2625, 9 layers).

**Do not:** add loonghao/alisaitteke COM to mcp.json on this PC. Prefer UXP for any new Adobe host.

**Docs:** `PHOTOSHOP-SETUP.md` · `ADOBE-CC-MCP-GUIDE.md` · `AGENT-RUNBOOK.md` §1

---

## 2026-07-20 — PSD blanks: spread / single / cover (no spine)

**Goal:** Match InDesign/Lulu geometry in Photoshop so MOCK→chop→InDesign stays consistent.

**Resolution (verified):**
1. `spread-page-template.psd` — 5250×2625 @ 300 RGB; cyan TRIM · magenta SAFETY · orange FOLD (MOCK).
2. `single-page-template.psd` — 2625×2625; cyan TRIM · magenta SAFETY (no fold).
3. `book-covers-template.psd` — 2625×2625 front **or** back art; hinge hints MOCK; TITLE/CREDITS zones.
4. **No** `book-spine-template.psd` — spine width from Lulu casewrap after interior upload.
5. Layer pattern: white-bg → paper-base → ART → overlays → type zones; Duplicate→Save As; type live in InDesign.
6. Scripts: `scripts/create_ps_page_templates.py` (+ earlier `finish_spread_page_template_psd.py`).

**Verify:** Files under `Xtraz/Adobe-Photoshop/` (gitignored binaries); docs in README + ISSUES playbook + `PHOTOSHOP-SETUP.md`.

---
