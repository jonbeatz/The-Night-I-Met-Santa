# PAGE BUILD WORKFLOW — Image → PSD → InDesign

**Status:** Living dial-in **2026-07-20** (evolve as we build pages)  
**Purpose:** Repeatable creative loop for every book page/spread — mocks, versions, PSD, type preview, InDesign place.  
**Master for future books:** promote polished rules into repo-root **`BOOK-PLAYBOOK.md`** + this title’s **`BOOK-PRODUCTION-SYSTEM.md`**.  
**Page map:** `BOOK-PAGE-WORKFLOW.md` · **Fix/playbook log:** `ISSUES-RESOLVED.md` · **Continuity:** `CONTINUITY-AND-PRINT-FINALS.md` · **Lanes/prompts:** `IMAGE-LANE-PROMPTS.md`

> Jon rule: tighten this file whenever a step sticks. Chat is ephemeral; this doc + recipes are the recreate path.

---

## 0) Goals

| Goal | How we hit it |
|------|----------------|
| Clean Photoshop tabs | After art is in the page PSD → **close the source PNG** (and unused templates) |
| Predictable MOCK type | Agent defaults match dialed PSD preview (not tiny / wrong color) |
| Recreate winners | Every mock version has a **`RECIPE.md`** (prompt + service + model + refs) |
| Character continuity | Boy + Santa always keyed off **`Media/approved/characters/`** G0 locks |
| Organized versions | Try 4–5 looks under `Media/generated/mocks/{unit}/vNN/` before promote |
| Print truth | Live type in **InDesign**; PSD MOCK-TYPE is **preview only** — never bake poem into finals |
| PS mirrors ID | Same **pixel counts** + same **point sizes** for the role → no constant re-scale (see §1b) |
| No fake gutter | Spread **art** is seamless — orange fold guide is MOCK-only, never baked into pixels |

---

## 1b) Photoshop ↔ InDesign size parity (LOCKED)

**Short answer:** Images and type **can** match 1:1 if we use the locked pixel counts and the right point sizes for the role. Mismatch usually means wrong canvas, wrong place scale, or MOCK type set to a different size than InDesign.

### Images (pixel count is truth)

| Unit | Pixels | Physical place in InDesign | Effective DPI |
|------|--------|----------------------------|---------------|
| Single page (+ bleed) | **2625 × 2625** | Full bleed box **8.75″ × 8.75″** | **300** |
| Spread master (+ bleed) | **5250 × 2625** | Full bleed **17.5″ × 8.75″** (or L/R chops **2625²** each) | **300** |

- Photoshop’s **“72 dpi”** label is **metadata only** — ignore it. Do **not** resample to “fix” DPI.
- Place art **full-bleed at those inches** → **no resize dance**. If ID looks different, the link was scaled, cropped, or the file wasn’t 2625/5250.
- Prefer **PNG** links (JPG of same pixels looks softer).

### Type (points = physical size)

**1 pt is the same in Photoshop and InDesign** when both docs are the real page size (trim **8.5″**, bleed **8.75″**). Viewing zoom does not change print size.

| Role | PSD MOCK-TYPE (preview) | InDesign live type (ships) |
|------|-------------------------|----------------------------|
| **Poem stanzas** | Cormorant Medium **20 / 26** · tracking **+5** · `#2C2C2C` | **Same** — rebuild live; do not rasterize |
| **Dedication / short matter** | Cormorant Medium **30 / ~40** · `#2C2C2C` (dialed p03) | Match ~30 pt unless Jon picks otherwise |
| **Title page (P01)** | Cinzel Decorative · title **36 pt** · author **18 pt** Cormorant · `#2C2C2C` · start **lower-center inside SAFETY** | **Same pt + position** live |
| Cover title | Cinzel Decorative (display) | Live Cinzel in cover doc |

**Agent rule:** For poem pages, set MOCK-TYPE to **20/26**, not 30. Use 30 only for short matter (dedication, thank-you lines). That way your PS fit + cloud brush previews what ID will print.

**Keep PS ↔ ID type locked (2026-07-20):**

| Do | Don’t |
|----|--------|
| Set size in the **Character** panel (pt) in both apps | **Free Transform** (Ctrl/Cmd+T) on type in Photoshop — panel can show **4 pt** while glyphs look huge |
| **Move** tool only to reposition MOCK-TYPE | Scale text by dragging corner handles |
| Place MOCK-TYPE inside the **SAFETY** square (not canvas 0,0 / top-left bleed) | Drop type at document origin (looks “barely on screen”) |
| Match the **same family + same pt** when rebuilding live in InDesign | Trust a wrong Character panel readout (e.g. Minion 12) when another frame/tool is selected |
| After Jon dials a winner, update this table + RECIPE | Freestyle a different size in ID than the approved MOCK |

### Watercolor text cloud (brushes)

| Do | Don’t |
|----|--------|
| Paint on **CLOUD** layer of the **same** 2625² or 5250×2625 PSD | Paint on a tiny crop then scale up in ID |
| Export **full-canvas RGBA** (transparent elsewhere) → place full-bleed in ID | Half-page file + inset frame (double positioning) |
| Soft mid-opacity wash — readable type, not a solid blob | Overpowered glow (rejected earlier) |

If the cloud is painted where it belongs on the full canvas, InDesign placement mirrors Photoshop **without** re-nudging. See chops playbook in `ISSUES-RESOLVED.md` § textCloud.

### Spread fold / “middle spine” line

| Layer / export | Fake vertical gutter / spine shadow? |
|----------------|--------------------------------------|
| Orange **FOLD** guide in PSD | OK for **screen MOCK** only — **hide** before art/cloud export |
| Generative **art** (Klein or Banana) | **Never** — prompt negatives required (`IMAGE-LANE-PROMPTS.md`) |
| Print / InDesign plates | **Never** — seamless scene across gutter |

---

## 1) Canonical loop (do this every page)

```
① GENERATE art (Lane A dial / Lane B finals) → save under mocks/vNN/
② WRITE RECIPE.md for that version (mandatory)
③ NEW PSD = Duplicate blank template → Save As page slug
④ PLACE art on ART layer (guides: cyan TRIM · magenta SAFETY)
⑤ CLOSE source PNG tab immediately
⑥ ADD MOCK-TYPE layer (preview) — **defaults §7** (visible inside SAFETY) · Jon positions + cloud brush
⑦ SAVE PSD when MOCK is close
⑧ PLACE art + rebuild **same pt/position** live type into InDesign
⑨ Jon approves → promote winner to Media/approved/ (+ recipe sidecar)
```

| Step | Who | Detail |
|------|-----|--------|
| 1 Image | Agent | See §3 lanes · naming §4 · continuity §5 |
| 2 Recipe | Agent | Template §6 — **no version without RECIPE.md** |
| 3 PSD | Agent + **Jon** | From blank template → **Jon Save As** `{slug}.psd` first (see §3b) → then place ART |
| 4 Place art | Agent | Soft center / full-bleed as briefed · respect SAFETY for faces |
| 5 Close PNG | Agent | **Hard rule** — keep only working PSD (+ reopen template when needed) |
| 6 MOCK-TYPE | Agent then Jon | Defaults §7 · Jon nudges + paints **CLOUD** wash for readable type |
| 7 Save | Agent/Jon | PSD already named; agent Save after edits |
| 8 InDesign | Agent + **Jon** | **Jon Save As** `book-interior-v1.indd` (or page smoke) at **8.5×8.5** first → then agent places art/type |
| 9 Promote | Jon says lock | Copy to Tier B / later `print/` · update `Media/approved/INDEX.md` |

### 3b) First file creation — Jon saves once (LOCKED 2026-07-20)

Adobe **Save / Close** modals block the agent bridge. Wrong Untitled can also save as **A4** instead of **8.5×8.5**.

| Step | Who | What |
|------|-----|------|
| 1 | Agent or Jon | Open blank: `single-page-template.psd` / `spread-page-template.psd` · or new InDesign square |
| 2 | **Jon** | **File → Save As** to final path (`Xtraz/Adobe-Photoshop/p01-title.psd`, `Xtraz/Adobe-inDesign/book-interior-v1.indd`, etc.) · click through any dialog |
| 3 | Jon | Confirm rulers/size (**8.5×8.5 in**, bleed **0.125**, margins **0.5**) — compare to `p03-dedication-smoke.indd` if unsure |
| 4 | Jon | Say **ready** |
| 5 | Agent | Place art, MOCK/live type, layers, nudges — **Save** (not first-create) |

**Do not** rely on the agent to dismiss “Save changes to Untitled…?” or to pick among multiple Untitled tabs.

---

## 2) Folder system (clean creative area)

```
Media/generated/mocks/
  _INDEX/README.md          ← running scoreboard of units + chosen vNN
  P03-dedication/
    v01/
      art.png               ← candidate art (2625² or 5250×2625)
      RECIPE.md             ← prompt / model / service / refs / verdict
      notes.md              ← optional Jon notes
    v02/ …
  S03-eyes-met/
    v01/ …

Media/approved/             ← keepers only (git-tracked)
  characters/               ← Boy G0 · Santa G0 · Jack (LOCKED)
  covers/ · pages/ · spreads/
  print/                    ← Lulu pixel finals after Pass B
  style-refs/               ← moodboard (not print locks)

Xtraz/Adobe-Photoshop/
  *-template.psd            ← blanks — do not paint keepers here
  p03-dedication.psd        ← one working PSD per page/spread unit
  working/                  ← optional scratch PSDs

Xtraz/Adobe-inDesign/       ← page/spread .indd smoke + full book doc
Images/chopz/               ← exports for InDesign (MOCK / LEFT / RIGHT / textCloud)
```

**Hygiene**

- Experiments stay under `Media/generated/` — never pretend they are approved.
- No `* copy.png` in approved folders.
- Open in PS: **one working PSD** per task. Close source PNGs and idle templates.
- `spread-page-template-v2.psd` — treat as experimental; prefer **`spread-page-template.psd`** until v2 is locked.
- **`Images/`** = `references/` + `chopz/` only (scratch → `_archive/images-scratch/`). Do not merge with `Media/`.
- **`Pages/`** = deprecated empty slot. Superseded docs → `_archive/docs/` (stubs remain under `.cursor/docs/`).
- One-off scripts → `scripts/_scratch/`.

---

## 3) Image lanes (what service / model)

| Lane | When | Service / model | Prompt block | Doc |
|------|------|-----------------|--------------|-----|
| **A1 — Dial primary** | Default mockup / testing | **Klein 9B** — fal `flux-2/klein/9b` (~$0.011) | **Dial D2** | `IMAGE-LANE-PROMPTS.md` |
| **A2 — Dial alt** | Second opinion | fal `qwen-image-2/text-to-image` (~$0.035) | Short master OK | same |
| **A3 — Dial light** | Hi-res batch / low-detail only | **Klein 4B** — fal `flux-2/klein/4b` (~$0.009) | **Dial D2** | same |
| **Frame** | Vignette vs bleed | — | **FRAME ON/OFF** + `Images/styles2/` | Default ON matter/title · OFF print spreads |
| **B — Finals** | Production-ready plates | fal **`gemini-3-pro-image-preview/edit`** (± OpenRouter Gemini) | **ILLUSTRATION-STYLE master** + G0/cover refs | same |
| **Style refs** | Mood / scene only | Upload from `Media/approved/style-refs/` | Tier A | — |
| **Character refs** | Any boy / Santa / Jack face | **Always** attach G0 locks from `characters/` | Tier B | — |

**Hard rules**

1. Default dial = **Klein 9B + Dial D2**. Qwen = alt compare. Klein **4B** only for hi-res volume or low-detail. Do **not** paste the long Gemini master onto Klein (or D2 onto Banana).
2. Every **spread** gen (A or B): append seamless-spread language + **negatives** for fake gutter / center spine / fold line (`IMAGE-LANE-PROMPTS.md` § Spreads) when **FRAME OFF** / print bleed.
3. **Watercolor frame:** say **with frame** / **full bleed** — append FRAME ON/OFF from `IMAGE-LANE-PROMPTS.md`. Refs: `Images/styles2/`.
4. RECIPE must record: lane · provider · **exact model id** · seed if known · ref paths · D2 vs master · verdict.

Never call a plate “final” until Jon promotes + watermark check (`CONTINUITY-AND-PRINT-FINALS.md`).

---

## 4) Naming

| Kind | Pattern | Example |
|------|---------|---------|
| Mock unit folder | `{P\|S}{NN}-{slug}` | `P03-dedication` · `S03-eyes-met` |
| Version | `v01` … `v99` | try several before lock |
| Art file in version | `art.png` (plus optional `art-from-psd.png`) | keep simple inside `vNN/` |
| Temp export name | `art-P{NN}-{slug}-2625.png` / `art-S{NN}-…-SPREAD-…` | `BOOK-PAGE-WORKFLOW.md` |
| Working PSD | `{slug}.psd` or `p{NN}-{slug}.psd` | `p03-dedication.psd` |
| InDesign smoke | `{slug}-smoke.indd` | until full book doc exists |
| Tier B promote | kebab under `pages/` / `spreads/` / `covers/` | + `.recipe.md` sidecar |

---

## 5) Continuity locks (non-negotiable)

| Character | Lock files | Must stay consistent |
|-----------|------------|----------------------|
| **Boy narrator** | `Media/approved/characters/boy-narrator-G0.png` (+ face crop) | Age, face, **oatmeal/taupe holly pajamas** |
| **Santa** | `Media/approved/characters/santa-G0.png` | Face, beard, suit language |
| **Jack (portrait pages)** | `…/jack-farrell-portrait.png` | Style-match-B lock |
| **Cover look** | `covers/cover-front.png` | beige-v2 · Santa face hidden on front |

- Pages **without** boy/Santa (e.g. quiet fireplace dedication) may use style-refs only — still note that in RECIPE.
- Any scene with the child or Santa: **attach G0 refs** on every generate/edit call.
- Detail: `CONTINUITY-AND-PRINT-FINALS.md` · `ILLUSTRATION-STYLE.md` · `Media/approved/INDEX.md`

---

## 6) RECIPE.md template (mandatory — complete form)

**Canonical copy-paste:** [`Media/generated/mocks/_RECIPE-TEMPLATE.md`](../../Media/generated/mocks/_RECIPE-TEMPLATE.md) · mirror [`.cursor/docs/RECIPE-TEMPLATE.md`](./RECIPE-TEMPLATE.md)  
**Gold example (locked):** `Media/generated/mocks/P01-title/v22/RECIPE.md`

**Going forward (2026-07-21):** every new `vNN/RECIPE.md` uses the **full** template — same fields every time. Use `n/a` / `—` when unknown; **never omit Prompt**. Thin recipes are outdated.

| Always include | Why |
|----------------|-----|
| name · unit · book page · version · date | Identity |
| page role · spread side | single vs spread L/R/wide |
| lane · service · model · settings · FRAME | Reproduce the call |
| concept · changes | What this version tests |
| size · seed · request_id · output | One file + regen |
| script_text · type_zone | Poem/title lines + where type sits |
| verdict · status · promoted_to | Review / lock trail |
| Character/style refs · **Prompt** · Negative · Gotchas · Notes · Related | Remake fidelity |

```markdown
# RECIPE — {unit} / v{NN}

| Field | Value |
|-------|--------|
| **name** | Short label |
| **unit** | P01-title |
| **book page** | 1 · Title · SINGLE |
| **page role** | `single` \| `spread` |
| **spread side** | `n/a` \| `left` \| `right` \| `wide-master` |
| **version** | v01 |
| **date** | YYYY-MM-DD |
| **lane** | A1 \| A2 \| A3 \| B \| local composite |
| **service** | fal.ai / OpenRouter / … |
| **model** | exact model id |
| **settings** | res · aspect · steps · safety · … |
| **FRAME** | ON \| OFF |
| **concept** | One-line intent |
| **changes** | vs prior / vs base |
| **size** | 1024² / 2K / 2625² |
| **seed** | or n/a |
| **request_id** | or n/a |
| **cost_note** | optional |
| **output** | exact filename (one file only) |
| **script_text** | Poem/title/dedication lines or n/a |
| **type_zone** | e.g. upper cream · lower-center SAFETY |
| **verdict** | pending \| keep \| maybe \| reject \| locked-provisional |
| **status** | working \| locked-provisional \| superseded |
| **promoted_to** | path or — |

## Character / style refs used
- boy / santa / jack / style / base: paths or n/a

## Prompt
(paste FULL prompt)

## Negative / constraints
…

## Gotchas
…

## Notes
…

## Related
…
```

Approved Tier B files keep a sidecar `*.recipe.md` with the same fields (Prompt required, or explicit pointer to the mock RECIPE that holds it). See `pages/p01-title.recipe.md`.

**Do not** ship a version with only a 6-row table and no Prompt.

## 7) MOCK-TYPE defaults (Photoshop preview → mirrors InDesign)

Same face/color always. **Size follows role** so PS design mirrors ID (see §1b).

| Setting | Poem pages | Dedication / short matter | Title page (P01) |
|---------|------------|---------------------------|------------------|
| Font | Cormorant Garamond Medium | same | **Cinzel Decorative** Regular (title) · Cormorant Medium (author) |
| Size / leading | **20 / 26** | **30 / ~40** (dialed p03) | Title **36 / 42** · author **18 / 24** |
| Tracking | **+5** | optional | optional |
| Color | **`#2C2C2C`** | **`#2C2C2C`** | **`#2C2C2C`** |
| Alignment | Center | Center | Center |
| **Default start** | Inside SAFETY (never canvas 0,0) | Quiet / dialed zone | **Lower-center SAFETY** (~y **1729 px** on 2625) |
| Layer name | `MOCK-TYPE - {slug} (preview)` | same | same |
| Stack | Above **CLOUD** · TYPE zone guide **hidden** | same | same |
| Position edits | **Move** tool only | same | same — never Free Transform |

**Photoshop 300 ppi type-API quirk (LOCKED):** high-level `createTextLayer` / `set_character_style` size is scaled by **72/300**. To get Character-panel **N pt**, pass **`N × (300/72)`** (e.g. 36 → **150**) **or** set size with batchPlay `pointsUnit: N`. Verify Character shows the intended pt before matching InDesign.

Print type is still **rebuilt live in InDesign** (never ship raster MOCK-TYPE). Cloud brush stays in PS → export RGBA → place full-bleed.

### PS-first vs early InDesign (LOCKED 2026-07-20)

**Default:** finish the **Photoshop MOCK close** (art + MOCK-TYPE + cloud wash) before deep InDesign work on that page. Then agent mirrors pt + position into live type.

| Phase | Do this | Skip / light touch |
|-------|---------|-------------------|
| Dial art + type in PS | Full creative loop | Don’t chase pixel-perfect ID yet |
| PS “close enough” | Place art + rebuild live type in ID to **same pt/spot** | — |
| Jon tweaks in PS | Re-read MOCK → nudge ID once | Don’t maintain two creative masters in parallel |
| Early ID smoke (optional) | One page to prove bridges/fonts | Not the design desk |

**Why:** one creative desk (PS) → one print desk (ID). Same starting defaults so they don’t diverge “by default.”

---

## 8) Photoshop tab hygiene (hard rules)

1. Place PNG → paste/place onto **ART** → **File → Close** the PNG document (don’t save PNG as PSD).
2. Do **not** leave `art-*.png` tabs open after the page PSD owns the pixels.
3. Prefer **one** open working PSD; reopen `*-template.psd` only when starting a new unit.
4. Hide guide layers (TRIM/SAFETY/TYPE zone) before export chops if they burn into pixels.

**Gotcha:** UXP `open` often needs a file token — open PNG via `Photoshop.exe` / OS, then copy into the PSD, then close PNG. See `ISSUES-RESOLVED.md` Photoshop playbooks.

---

## 9) InDesign handoff

1. Export art (and later textCloud / paintFrame) per chops playbook in `ISSUES-RESOLVED.md`.
2. Place on the **correct book page** from `BOOK-PAGE-WORKFLOW.md` (prototype page # ≠ final book #).
3. Rebuild readable type as **live Cormorant** — do not ship raster MOCK-TYPE.
4. Safety: glyphs inside magenta 0.5″ zone.

---

## 10) Approval ladder

| Stage | Location | Meaning |
|-------|----------|---------|
| Mock try | `Media/generated/mocks/{unit}/vNN/` | Exploring |
| Composition lock | `Media/approved/pages|spreads|covers/` | Jon said lock look |
| Print plate | `Media/approved/print/` | Correct px · watermark-free · recipe complete |

Update `Media/approved/INDEX.md` on every promote.

---

## 11) Evolving this system — what to say

| You say | Agent does | Best for |
|---------|------------|----------|
| **`log fixes`** / **`log fix`** | Append newest-first entry to **`ISSUES-RESOLVED.md`** (Symptom · Cause · Resolution · Verify); promote durable rules into playbooks here / runbook | A bug, gotcha, or “we hit this — don’t repeat” |
| **`update docs`** | Harvest session into **living system docs**: this file · `BOOK-PRODUCTION-SYSTEM.md` · `BOOK-PAGE-WORKFLOW.md` (if map changed) · `CONTINUE-HERE` / `ReCall` · optional `BOOK-PLAYBOOK` · `docs:sync` / fleet when shared | Workflow evolution, decisions, folder/naming changes |
| **`update docs and mem0`** | Same as update docs **+** Mem0/Draven memory | End of a dial-in session |
| Both | Ideal when you fixed something **and** changed the process | e.g. size-parity + Klein D2 rules |

**Does it matter?** Yes, slightly:

- **`log fixes` alone** → strong incident trail; may miss folding into `BOOK-PAGE-WORKFLOW` / playbook unless the agent also promotes.
- **`update docs` alone** → best for “keep evolving the master system”; still should touch `ISSUES-RESOLVED` if there was a concrete fix.
- **Practical habit while dialing:** say **`update docs`** after a workflow chat (like this one). Say **`log fixes`** when something broke and you want the symptom→fix card. Say both when unsure.

`BOOK-PAGE-WORKFLOW.md` = **page map** (what goes on which page).  
`PAGE-BUILD-WORKFLOW.md` = **how we build** each page.  
`update docs` should refresh **both** when either changed.

---

## 12) Recommendations / watch-outs (living)

| Item | Note |
|------|------|
| **1:1 mirror** | Same pixels + poem MOCK **20/26** + full-canvas cloud → PS should match ID without constant resize |
| **Klein = Dial D2** | Always; don’t freestyle a “closer to Gemini” prompt on 4B |
| **No fake gutter in art** | Hide orange fold; prompt negatives on every spread gen |
| **Version budget** | Cap ~5 serious tries per unit, then pick or change brief |
| **Scoreboard** | Keep `Media/generated/mocks/_INDEX/README.md` current |
| **Don’t bake type** | MOCK-TYPE never in print export |
| **Credits ≠ Gemini OAuth** | Image gen = fal/Klein keys — not Gmail OAuth |
| **Template bloat** | Archive unused `*-v2` blanks once one blank is locked |
| **Kanban optional** | TaskBoard card per `PNN`/`SNN` if queue gets long |
| **Smoke first** | New blank/tool path → one single-page smoke (like P03) before 12 spreads |
