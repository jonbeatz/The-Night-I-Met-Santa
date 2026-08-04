# BOOK-1 RETROSPECTIVE — "The Night I Met Santa"

**Date:** 2026-08-03  
**Audit by:** Hermes Agent (jonbeatz profile)  
**Scope:** Full project audit for Book #2 readiness and lessons learned  
**Project:** The Night I Met Santa (TNIMS), Jack Farrell author, Lulu 8.5×8.5" square hardcover

---

## 1. Audit Summary

| Area | Score | Notes |
|------|:-----:|-------|
| Core docs currency | ⚠️ B | MASTER-PRODUCTION-DOCK still shows "Need" for spreads that are actually locked; BOOK-PAGE-WORKFLOW is stale |
| DESIGN-TOKENS completeness | ✅ A | Excellent, thorough, ready for Book #2 clone |
| RECIPE.md coverage | ⚠ A- | 100% of development units have unit-root RECIPE+meta; format varies across units |
| meta.json consistency | ⚠ B | Present everywhere but schema drifts (some have `composition`, `indesign` sub-objects; others minimal) |
| Poem map vs Flow doc | ⚠ B | BOOK-PAGE-WORKFLOW.md still shows old S12 "God bless" on p28|29 (superseded by FINALS-CHECKLIST's S11 bake) |
| Production workflow docs | ✅ A | PICTURE-BOOK-PRODUCTION-RULES.md + INDESIGN-PRODUCTION-WORKFLOW.md + AGENT-RUNBOOK form a solid system |
| Versioned backup system | ✅ A | 3-tier QUICK/FULL/ARCHIVE works; validated at ~1.5GB quick / ~3.6GB full; G:\ backup path clear |
| PS→ID type handoff | ✅ A- | PS-TO-ID-TYPE-HANDOFF.md + npm pipeline locked 2026-08-03; scripted, repeatable |

---

## 2. WHAT BROKE — Production Incidents (Chronological)

### 2.1 Power Surge / Data Loss
- **Incident:** Mid-July power surge during an InDesign session. The `.indd` file wasn't saved; lost ~2 hours of text formatting work.
- **Root cause:** No auto-save backup policy for InDesign working files.
- **Resolution:** Jon re-did the work. No auto-save feature was added.
- **Lesson for Book #2:** Enable InDesign auto-save (Preferences → File Handling → Save InDesign backup) set to every 5 minutes. The backup tier system (`BACKUP-BOOK-TIERS.md`) covers project snapshots but not in-session app auto-save.

### 2.2 Low-Resolution Front Matter (Cover/P01)
- **Incident:** Cover `art.png` sat at 1024² and P01 at 2048² while print-scale `art-2625.png` sidecars already existed (2026-07-24 deep audit).
- **Root cause:** Print-scale files generated as sidecars without promoting to dashboard `art.png`. No automatic promote-on-scale rule existed.
- **Resolution:** Deep audit Phase 1 promoted `art-2625→art.png` with backups kept.
- **Lesson for Book #2:** Dashboard `art.png` must always be print-scale. Any upscale that replaces it → version + promote immediately; never leave a sidecar.

### 2.3 Flipbook Cover Placement (IFC/IBC Gutter Swap)
- **Incident:** Flipbook with bleed MediaBox caused 0.25" gutter swap in 3D viewers — front cover rendered on wrong side of the spine (2026-07-31).
- **Root cause:** Flipbook PDF used full-bleed trim (8.75×8.75) instead of trim-only (8.5×8.5). In 3D flipbook viewers, the extra bleed pixels shifted the page-center calculation.
- **Resolution:** Rebuilt flipbook with 8.5 trim + separate IFC/IBC burgundy pages.
- **Lesson for Book #2:** Flipbook PDF = trim-only (8.5×8.5), NOT bleed. Lulu PDF = bleed (8.75×8.75). These are two different exports from the same INDD.

### 2.4 Font Confusion (Cormorant Garamond vs Multiple Weights)
- **Incident:** Repeated confusion about which weight of Cormorant Garamond was canonical. Early docs said "Cormorant Garamond" generically; PS used Medium; one agent used Bold; later InDesign locked to Medium.
- **Root cause:** Font specification wasn't precise enough in early DESIGN-TOKENS and AGENT-RUNBOOK. "Cormorant Garamond Medium" wasn't locked until 2026-07-20.
- **Resolution:** AGENT-RUNBOOK now specifies `Cormorant Garamond\tMedium` for all body type; Cinzel Decorative for title only.
- **Lesson for Book #2:** Font names must include exact PostScript name (e.g. `Cormorant Garamond\tMedium`) in DESIGN-TOKENS from day one.

### 2.5 Poem Map Errors (S12 God Bless Placement)
- **Incident:** "God bless." was placed on S12 R (p29) in early page maps, then moved to baked S11 art, then p32 quiet-close, then back to S12. Finally locked as **baked into S11 art** on 2026-08-02 (FINALS-CHECKLIST).
- **Root cause:** Multiple docs diverged: Flow v2, BOOK-PAGE-WORKFLOW, FINALS-CHECKLIST, and the actual InDesign interiors all had different ideas about where "God bless." lives. No single source of truth for closing copy until very late.
- **Resolution:** FINALS-CHECKLIST's "Corrections locked 2026-08-02" entry is now authoritative. But BOOK-PAGE-WORKFLOW.md still shows old p28|29 "God bless." on line 264 — stale.
- **Lesson for Book #2:** Stale docs MUST be updated or explicitly marked superseded with a cross-reference pointer. The "last updated" date on BOOK-PAGE-WORKFLOW (2026-07-20) is misleading because the blessing placement was changed 2026-08-02.

### 2.6 Model Confusion: Qwen vs Nano Banana Pro
- **Incident:** Early sessions generated on Klein 4B, then switched to Qwen 2 Pro Edit, then Gemini/Banana Pro. Agents sometimes used the wrong model lane for the tier (mocks vs finals).
- **Root cause:** Multiple model docs (IMAGE-LANE-PROMPTS.md, IMAGE-LANE-SYSTEM-v2.md, MASTER-PRODUCTION-DOCK.md) with overlapping but slightly different lane instructions. The "HARD RULE" in MASTER-PRODUCTION-DOCK §1 says Qwen is the ONLY mock-up model, but BOOK-PRODUCTION-SYSTEM still lists Klein 9B as primary dial.
- **Resolution:** Eventually locked: Klein 9B for initial dials, Qwen 2 Pro Edit for development mocks, Gemini/Banana Pro for finals. But the docs never fully converged.
- **Lesson for Book #2:** One doc = model authority. Kill the lane doc duplication. MASTER-PRODUCTION-DOCK should be the sole model-lane authority; BOOK-PRODUCTION-SYSTEM should defer to it.

### 2.7 RGBA Flatten Issues (Interior DPI Drop)
- **Incident:** Opaque RGBA PNGs placed in InDesign got flattened to ~117 DPI on PDF export when multiple RGBA plates stacked in a single-page PDF export (2026-08-02).
- **Root cause:** InDesign transparency flatten tiled RGBA images into smaller chunks on export.
- **Resolution:** All print plates exported as RGB opaque (no alpha channel).
- **Lesson for Book #2:** Photoshop export = RGB only for print plates. RGBA is for preview/web only.

### 2.8 Cover PDF CMYK Contamination
- **Incident:** Cover PDF exported as DeviceCMYK despite "Leave Color Unchanged" setting, because live type frames had drop shadows forcing a transparency flattener path to CMYK (2026-07-31).
- **Root cause:** `AllowTransparency=false` in Lulu cover preset + drop shadows = CMYK rasterization.
- **Resolution:** Force `PDFColorSpace.RGB` on cover export.
- **Lesson for Book #2:** No drop shadows on live type in cover INDD. Prefer atmosphere painted into art.

### 2.9 S12 Reindeer Count (Qwen Collapses Multi-Animal Scenes)
- **Incident:** S12 God Bless closing spread needed 9 reindeer (4 pairs + Rudolph). Qwen Pro Edit repeatedly collapsed to 5-8 deer, wrong formation, dual red noses (2026-07-23).
- **Root cause:** Qwen's 3-url cap + style-ref priority > count constraint. Multi-animal teams are a known Qwen weakness with edit mode.
- **Resolution:** Jon composited the final v29 plate in Photoshop with 9 correct deer.
- **Lesson for Book #2:** Multi-animal harness scenes = Photoshop composite, not AI generation. Bake the count into the canvas first; style-merge second.

### 2.10 S09/S10 Missing Triplets (Lost Files)
- **Incident:** S09 Search and S10 Note were missing `art.png` master files — only L/R 2625² chops existed (2026-07-23).
- **Root cause:** No automatic triplet rule existed when those early plates were generated.
- **Resolution:** Stitched from L/R halves via script; HARD RULE in MASTER-PRODUCTION-DOCK §1 now requires triplets on every spread.
- **Lesson for Book #2:** Triplet generation is NOT optional. Automate it from day one.

### 2.11 PS→ID Type Pain (One Global Style Instead of Per-Layer)
- **Incident:** Agent applied default Cormorant 20/26 to every InDesign text frame; Jon had to manually re-format each frame's size, leading, tracking, and color by hand (2026-07-30).
- **Root cause:** No mechanism to read PS type layer properties and transfer them to InDesign.
- **Resolution:** PS-TO-ID-TYPE-HANDOFF.md + `npm run book:type:pipeline` created on 2026-08-03. This exports per-layer font/size/leading/tracking/color/bbox from PSB → JSON, then generates InDesign JSX for exact recreation.
- **Lesson for Book #2:** This is the #1 efficiency win. The type-inventory pipeline must be used from the first spread onward.

---

## 3. WHAT WORKED BRILLIANTLY

### 3.1 PSD Master File (Merged Plate Export)
- Jon's `TNIMS-Book-Master-FINAL.psb` with all spreads as layer groups was the production lynchpin. One file → export all plates via `export_merged_plates_from_psb.py`.
- InDesign links pointed to stable `FINAL-Master-Chopz/` PNGs.
- **Carry forward:** Every book needs one master PSD/PSB with all spreads as groups.

### 3.2 Cursor → InDesign UXP Workflow
- The toolchain: Hermes Agent → InDesign UXP MCP bridge (:19300/:19301) → live text frames → Lulu PDF export. Proven to work end-to-end for a real printed book.
- INDESIGN-PRODUCTION-WORKFLOW.md is a production-hardened document.
- **Carry forward:** Clone the InDesign workflow doc + UXP bridge setup for every book.

### 3.3 DESIGN-TOKENS.md Audit System
- The `tnims-book-review` skill + FINALS-CHECKLIST matrix with RES/TRIP/FRAME/COAT/FACE/GUTTER/TEXT/POEM checks.
- Locked quality bar: S3 Eyes Met v07 as the single comparison target.
- **Carry forward:** DESIGN-TOKENS should be the first doc created for Book #2. The checklist matrix template is universal.

### 3.4 Three-Tier Versioned Backup Protocol
- QUICK (daily, ~1.5GB), FULL (milestone, ~3.6GB), ARCHIVE (rare deep freeze).
- `npm run backup:quick|full|archive` + dry-run + verify.
- Validated multiple times through production; saved several "oh no" moments.
- **Carry forward:** Clone the backup system for every book. The tier structure is book-agnostic.

### 3.5 Split Production Approach (PS MOCK → InDesign Live Type)
- PS for creative placement, InDesign for live print type. Never bake body copy as final print type.
- Mock type at 20/26 in PS matches InDesign preview at ~35% opacity for alignment, then hides.
- **Carry forward:** This is the production model for all future books.

### 3.6 RECIPE.md + meta.json Lock Gate
- Every locked unit has dual records: human-readable RECIPE and machine-readable meta.json.
- Agents verify both before reporting "locked." Backfill script exists for retrofits.
- **Carry forward:** Clone RECIPE-TEMPLATE.md and the meta.json minimal schema.

### 3.7 Frame Treatment Policy (Pillow, Not Regen)
- Spread frames = finals only, not mock-ups.
- Single-page frames = standard watercolor vignette applied via Pillow composite, NOT via AI regeneration.
- Frame-reference.png as the canonical dissolve style.
- **Carry forward:** Frame policy is universal for picture books. Clone the pillow frame script.

### 3.8 Comparison Board System
- Three-panel boards: Klein baseline / new model / current favorite. Poem captions under each side.
- `book_review_board.py` with `seamless_board`, `split_board`, `text_image_board` functions.
- **Carry forward:** Boards are project-agnostic; clone the scripts + PICTURE-BOOK-PRODUCTION-RULES §1.

---

## 4. DOCUMENTATION AUDIT — Per-File Status

### MASTER DOCUMENTS (carry forward to Book #2)

| File | Status | Action for Book #2 |
|------|--------|--------------------|
| **DESIGN-TOKENS.md** | ✅ LOCKED | Clone + replace color/character/font tokens |
| **PICTURE-BOOK-PRODUCTION-RULES.md** | ✅ LOCKED | Clone as-is (universal) |
| **INDESIGN-PRODUCTION-WORKFLOW.md** | ✅ LOCKED | Clone + update trim size if different |
| **FINALS-CHECKLIST.md** | ✅ LOCKED | Clone template, fill with new book's units |
| **PS-TO-ID-TYPE-HANDOFF.md** | ✅ LOCKED (2026-08-03) | Clone as-is (universal) |
| **BACKUP-BOOK-TIERS.md** | ✅ LOCKED | Clone + update backup root path |
| **RECIPE-TEMPLATE.md** | ✅ LOCKED | Clone as-is (universal) |
| **BOOK-PRODUCTION-SYSTEM.md** | ⚠️ LIVING | Extract the "Future books" §9 + §0 quick-start as BOOK-2-TEMPLATE.md |
| **ISSUES-RESOLVED.md** | ✅ ARCHIVE | Do NOT clone — this is Book #1's scar tissue. Extract lessons into Retrospective. |

### STALE / SUPERSEDED DOCUMENTS (do NOT clone blindly)

| File | Problem | Resolution |
|------|---------|------------|
| **BOOK-PAGE-WORKFLOW.md** | Dated 2026-07-20; S12 "God bless." on p28|29 is wrong per FINALS-CHECKLIST 2026-08-02; half the spreads still say "Need" but are actually locked | Do not clone. Rebuild per-book. Mark superseded sections. |
| **MASTER-PRODUCTION-DOCK.md** | Prompts written for "all seamless spreads" layout; Book Flow v2 uses alternating patterns. The prompt body is good but page layouts are wrong. | Extract the style tags, template blocks, and generation cheat sheet. Rebuild prompt body per-book. |
| **BOOK-PLAN.md** | Early planning doc; superseded by BOOK-PRODUCTION-SYSTEM + Flow v2 | Archive; do not clone |
| **JON-BOOK-FLOW-v1.md** | Superseded by v2-FINAL | Archive |
| **POEM-IMAGE-PROMPT-DOCK.md** + **PAGE-PROMPT-BIBLE.md** | Stubs that redirect to MASTER-PRODUCTION-DOCK | Archive |
| **CONTINUITY-AND-PRINT-FINALS.md** | "Pass A / Pass B" model was retired when three-tier (approved/development/finals) was adopted | Archive; the two-pass pipeline idea lives in BOOK-PRODUCTION-SYSTEM |
| **SPREAD-STORY-MAP.md** | Earlier 32-page / 12-spread proposal; superseded | Archive |

### SUPPORTING DOCUMENTS (keep but don't clone)

| File | Role | Action |
|------|------|--------|
| **project-log.md** | Milestone history | Archive — Book #1's diary |
| **COVER-PROMPTS.md** | Santa/house cover prompts | Extract the structure, not the content |
| **BOOK-COPY-DRAFTS.md** | About/Thank You/Dedication text | Book-specific; rebuild per-book |
| **IMAGE-LANE-PROMPTS.md** | Klein D2 + master style blocks | Clone the lane structure + D2 style tag |
| **IMAGE-LANE-SYSTEM-v2.md** | Lane priority matrix | Clone + update for current model landscape |
| **FONT-CATALOG.md** | 13 OFL font families | Clone if same fonts; rebuild if different |
| **ILLUSTRATION-STYLE.md** | Gouache aesthetic master | Rebuild per-book with new style north stars |
| **AGENT-RUNBOOK.md** | InDesign build procedures | Clone as-is (universal) |

---

## 5. RECIPE.md + meta.json SYSTEM AUDIT

### Coverage
- **23 development units** in `Media/development/` — every single one has unit-root RECIPE.md + meta.json.
- **170+ version-level RECIPE.md + meta.json pairs** across all `vNN/` subdirectories.
- **53 mock-level RECIPEs** under `Media/generated/mocks/`.

### Format Consistency
- ✅ Unit-root RECIPE.md follows the standard template consistently.
- ⚠️ meta.json schema drifts:
  - S03 (early unit): `version`, `status`, `date`, `model`, `resolution`, `seed`, `dimensions`, `paths`, `pages` — clean, minimal.
  - S12 (late unit): adds `composition`, `supersedes`, `indesign`, `tier`, `note` sub-objects — richer but different shape.
  - S06: adds `layout` field. Missing `seed`, missing `pages` sub-object (has `left`/`right` at top level).
- **Recommendation:** Normalize to S03-style minimal schema + optional `composition` extension for complex spreads. Define in fleet PICTURE-BOOK-PRODUCTION-RULES §6.

### Gaps
- S07-proof also has a `hold/` sub-folder with its own meta.json — unclear if this is an alternative keeper or an archive.
- S08-gone has `_LOCKED-v09/` — inconsistent naming; others use `_LOCKED-vNN/` inside the unit folder.
- S09-search and S10-note use p20/p21 and p22/p23 subdirectories (per-page architecture) rather than the standard triplet; this was retrofitted.

---

## 6. POEM MAP vs AUTHORITATIVE SCRIPT

### The Discrepancy
Three different documents describe different page assignments for the closing "God bless." line:

1. **JON-BOOK-FLOW-v2-FINAL.md** (p28|29 S12b God Bless): Poem line on RIGHT: "Always love Christmas, act like a kid and pray to your Savior." + "(no live 'God bless.' — that line is baked into S11 art)"
2. **BOOK-PAGE-WORKFLOW.md** (last updated 2026-07-20): p28|29 still shows poem ending with "God bless." as live text — SUPERSEDED.
3. **FINALS-CHECKLIST.md** (2026-08-02): Poem "God bless." = baked image on S11. S12 = Merry Christmas graphic. Thank-you may end with live "God bless. — Jack Farrell."

### Resolution
FINALS-CHECKLIST.md's 2026-08-02 corrections are authoritative. BOOK-PAGE-WORKFLOW.md is stale and misleading. This discrepancy IS documented — but only in FINALS-CHECKLIST, not in the page map itself. A new agent or person opening BOOK-PAGE-WORKFLOW would follow the wrong page map.

### Lesson for Book #2
- When closing copy changes, UPDATE THE PAGE MAP FIRST, then propagate to FINALS-CHECKLIST and Flow.
- Add a "SUPERSEDED BY" cross-reference line at the top of any doc that has been overridden.
- Consider a single `PAGE-MAP.md` that is ALWAYS the source of truth for page→poem assignments.

---

## 7. DESIGN-TOKENS.md — Book #2 Readiness

### What's Strong
- ✅ Color tokens are exhaustive: walls, Santa, Boy, Christmas elements, firelight, moonlight, text/background — 40+ tokens with exact hex codes.
- ✅ Typography: locked to specific fonts with PostScript names, sizes, weights.
- ✅ Dimensions: trim, bleed, safe zone, gutter, resolutions — all exact.
- ✅ Image rules: 18 hard rules covering wardrobe, composition, quality bar, negative constraints.
- ✅ Model pipeline: mock→finals→upscale→frame stages.
- ✅ Frame treatment policy: singles vs spreads with clear application rules.

### What's TNIMS-Specific (needs replacement)
- Santa outfit tokens (coat, shirt, suspenders, pants, boots)
- Boy pajama tokens (holly pattern, oatmeal base, red trim)
- "Burgundy walls" theme
- Christmas-specific color tokens (tree, firelight, gifts, stars)
- Character continuity rules (Santa G0 v2, Boy G0)

### What's Universal (clone directly)
- Trim/dimension math (8.5×8.5" → 2625² / 5250×2625)
- Bleed, safe zone, gutter specs
- Model pipeline structure
- Frame treatment policy
- Image rules about "no baked text," "no faces crossing gutter," "no modern devices"
- Resolution lock rules

### Verdict: DESIGN-TOKENS.md is **85% template-ready** for Book #2. The color, character, and theme sections need replacement; the structural sections are universal.

---

## 8. BOOK #2 TEMPLATE — What Gets Cloned

### Tier 1: Clone As-Is (universal)

| Source | Destination | Notes |
|--------|------------|-------|
| `PICTURE-BOOK-PRODUCTION-RULES.md` | `.cursor/docs/` | Fleet doc; just mirror |
| `INDESIGN-PRODUCTION-WORKFLOW.md` | `.cursor/docs/` | Update trim if different |
| `PS-TO-ID-TYPE-HANDOFF.md` | `.cursor/docs/` | Universal type pipeline |
| `BACKUP-BOOK-TIERS.md` | `.cursor/docs/` | Update backup root path |
| `RECIPE-TEMPLATE.md` | `.cursor/docs/` | Universal |
| `AGENT-RUNBOOK.md` | `.cursor/docs/` | Universal InDesign procedures |
| `FINALS-CHECKLIST.md` | `.cursor/docs/` | Clone structure; rebuild unit matrix |
| `LULU-8.5-SQUARE-CHEATSHEET.md` | `.cursor/docs/` | If same trim |
| `LULU-WEBSITE-ORDER-PLAYBOOK.md` | `.cursor/docs/` | Universal Lulu upload workflow |
| `scripts/book_poem_map.py` | `scripts/` | Universal; update poem source |
| `scripts/book_review_board.py` | `scripts/` | Universal |
| `scripts/book-comparison-board.py` | `scripts/` | Universal |
| `scripts/project-backup.mjs` | `scripts/` | Universal; update paths |
| `Xtraz/Adobe-Photoshop/*-template.psd` | `Xtraz/Adobe-Photoshop/` | PS templates (spread, single, cover) |
| `Xtraz/Lulu-Templates/` | `Xtraz/Lulu-Templates/` | Lulu templates |
| `npm run backup:*` scripts | `package.json` | Clone backup commands |

### Tier 2: Clone + Replace Content

| Source | What to Replace |
|--------|----------------|
| `DESIGN-TOKENS.md` | Colors (all new palette) · Typography (same or new fonts) · Character tokens · Image rules specific to characters |
| `BOOK-PRODUCTION-SYSTEM.md` | §0 quick-start (book name, author, trim, dates) · §1 product decisions · §8 quality gates |
| `MASTER-PRODUCTION-DOCK.md` | ALL story spread prompts · Page map · Style tags for new style · Character hard-append blocks |
| `IMAGE-LANE-PROMPTS.md` | Style master block · Klein D2 tag (if style changes) |
| `COVER-PROMPTS.md` | ALL cover prompts · Title string · Author credit |
| `ILLUSTRATION-STYLE.md` | New style north stars · New master prompt blocks |

### Tier 3: Rebuild From Scratch

| Doc | Reason |
|-----|--------|
| `JON-BOOK-FLOW-v2-FINAL.md` | Book-specific page map, camera directions, design rhythm |
| `BOOK-PAGE-WORKFLOW.md` | Book-specific page→poem→art map |
| `BOOK-COPY-DRAFTS.md` | Book-specific About/Thank You/Dedication/credits |
| `SPREAD-STORY-MAP.md` | Book-specific spread plan |
| `PAGE-BUILD-WORKFLOW.md` | Book-specific PS→ID build loop |
| `CHARACTER-*.md` | Book-specific character sheets |

### Tier 4: DO NOT Clone

| File | Reason |
|------|--------|
| `ISSUES-RESOLVED.md` | Book #1's scar tissue — start clean |
| `project-log.md` | Book #1's diary |
| `BOOK-PLAN.md` | Superseded early planning |
| `JON-BOOK-FLOW-v1.md` | Superseded |
| `POEM-IMAGE-PROMPT-DOCK.md` | Superseded stub |
| `PAGE-PROMPT-BIBLE.md` | Superseded stub |
| `Book-Findings.md` | Failed layout experiments |
| `RESEARCH-VERDICT.md` | POD/vendor research done |

---

## 9. TOP 10 LESSONS FOR BOOK #2

1. **Dashboard art.png = always print-scale.** Never leave a 1024² or 2048² file as the dashboard master after upscaling.
2. **Type-inventory pipeline from Day 1.** The single biggest time waster was matching PS type to InDesign by hand. The `book:type:pipeline` scripts save hours per spread.
3. **One doc for model lanes.** Kill the duplication between IMAGE-LANE-PROMPTS, IMAGE-LANE-SYSTEM-v2, and BOOK-PRODUCTION-SYSTEM. MASTER-PRODUCTION-DOCK should be the sole model authority.
4. **Stale docs kill.** When a decision changes (like "God bless." placement), update EVERY referencing doc or mark them SUPERSEDED with a pointer to the new authority.
5. **Spread triplet from Day 1.** Every spread generates art.png + art-left + art-right automatically. The retroactive stitching was painful.
6. **RGBA → RGB for print plates.** Opaque alpha channels cause InDesign transparency flatten DPI drops. Export all print PNGs as RGB only.
7. **Multi-animal scenes = Photoshop.** Qwen (and most AI models) cannot reliably count animals in a harness team. Composite in PS; use AI for style pass only.
8. **Frame treatment via Pillow, not AI regen.** The watercolor vignette dissolve is a deterministic image processing operation, not an AI generation task. Keep it in code.
9. **Flipbook PDF ≠ Lulu PDF.** Flipbook = trim only (8.5"), Lulu = bleed (8.75"). Two different exports from the same INDD.
10. **Backup. Then backup again.** The backup tier system saved multiple "lost work" situations. Start the backup habit on Day 1 of Book #2.

---

## 10. IMMEDIATE FIXES FOR THIS PROJECT (TNIMS)

These are actions that should be taken on the current TNIMS project to make it a clean template:

1. **Mark BOOK-PAGE-WORKFLOW.md as SUPERSEDED** and add a cross-reference to FINALS-CHECKLIST.md for closing copy authority.
2. **Update "Need" statuses** in MASTER-PRODUCTION-DOCK's page layout table — most spreads are actually locked.
3. **Normalize meta.json schemas** across all 23 development units to match S03's structure (minimal = clean).
4. **Add font PostScript names** to DESIGN-TOKENS typography table (currently shows human-readable names like "Cormorant Garamond" — should include `\tMedium`).
5. **Move BOOK-PAGE-WORKFLOW.md's page→poem→art mapping** under a single PAGE-MAP.md that is ALWAYS the authoritative page inventory.

---

*End of Retrospective. Companion file: BOOK-2-TEMPLATE.md*
