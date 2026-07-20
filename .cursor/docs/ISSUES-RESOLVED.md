# ISSUES-RESOLVED — The-Night-I-Met-Santa

Append-only log of **problems we hit** and **verified fixes**. Newest first.

**Operator trigger:** say **`log fixes`** or **`log fix`** — agent appends an entry here from the session (do not wait for interactive CLI).

**CLI (optional):** from repo root  
`npm run log:fix -- --issue "..." --cause "..." --solution "..."`

**Also promote** durable layout rules into `AGENT-RUNBOOK.md` when a fix becomes standard procedure.

---

## Playbook — Photoshop chops → InDesign (locked 2026-07-20)

Living “how we build spreads.” Dated entries below are the incident history; **this section is the operator cheat sheet.** Update when something sticks.

### 1) Default loop (Jon + agent)

| Step | Who | What |
|------|-----|------|
| 1 | Jon | Design in Photoshop at **spread 5250×2625** (continuous scenes) or **page 2625×2625** (singles) |
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
