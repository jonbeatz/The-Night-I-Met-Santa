# FINALS CHECKLIST — The Night I Met Santa

**Date:** 2026-07-23 · **SoT art:** `Media/generated/mocks/_FLOW-CURRENT.json`  
**Quality bar:** S3 Eyes Met **v07** · **Frame ref (singles):** `Media/approved/style-refs/frame-reference.png`  
**Never call anything “final.”** This is the pre-Banana / pre-InDesign gate list.

---

## How to grade

| Priority | Meaning |
|----------|---------|
| **HIGH** | Blocks Lulu finals or Banana spend — fix before regenerating other pages |
| **MED** | Fix on finals pass or Jon eye — does not block book assembly mocks |
| **LOW** | Polish / optional |

### Check columns (every unit)

| Code | Check |
|------|--------|
| **RES** | Singles **2625²** · spreads **5250×2625** + L/R **2625²** |
| **TRIP** | Triplet present when seamless: `art.png` + `art-left.png` + `art-right.png` |
| **FRAME** | ON when beat requires cream dissolve · OFF on story-spread keepers until finals |
| **COAT** | Santa coat **OPEN** + striped shirt + suspenders over shirt (vs `santa-G0-v2`) |
| **FACE** | Boy / Santa G0 drift (eyes, beard, age, holly PJs) |
| **GUTTER** | No baked fold line · faces/eyes not bisected · continuous scene |
| **TEXT** | No baked letters · type zones open for InDesign |
| **TYPE-INV** | `type-inventory.json` for units with live type (`npm run book:type:export`) |
| **POEM** | Copy matches inventory below / `scripts/book_poem_map.py` |
| **RECIPE+meta** | Unit-root `Media/development/{unit}/RECIPE.md` **and** `meta.json` both present |

---

## Poem / text inventory — closing (Interior FINAL · 2026-08-02)

| Page | Role | InDesign text | Art plate |
|------|------|----------------|-----------|
| **p26\|27** | **S11** | Live poem (note / favor stanzas). **Poem “God bless.” is baked into S11 art** — not a live text frame | `S11-spread.png` |
| **p28\|29** | **S12** | **No live type** — **Merry Christmas graphic** baked into art (replaces old “God bless.” on this spread) | `S12-spread.png` |
| **p30** | Thank You | Thank You Draft — body ends live *God bless. — Jack Farrell* (author sign-off, separate from poem close) | thank-you spread |
| **p31** | Author | Optional credits — portrait-led | author plate |
| **p32** | Quiet Close L / back blurb | As placed in Interior FINAL | `Back-Page` / quiet as linked |
| **p33** | Quiet Close R | As placed | — |

**Corrections locked 2026-08-02**

- Poem **"God bless."** moved off S12 → **baked image on S11**. S12 now carries a **Merry Christmas graphic** in the art (Jon preferred). Do **not** add live “God bless.” on S12.
- Thank-you page live *God bless. — Jack Farrell* is the **author sign-off**, not the poem North Star line.
- Older note “God bless on S12 R only” is **superseded**.

**Corrections locked 2026-07-23** (historical)

- S12 page-index remap of that week is superseded by Interior FINAL page map above.
- p32 ≠ “God bless. / Merry Christmas.” — that older Flow line remains superseded.

---

## Phase 1 back-matter audit (2026-07-23)

| Page | Grade | Action taken | Path |
|------|-------|--------------|------|
| **p30** | **PASS** | FINE AS-IS — 2625² cream paper, FRAME ON, no bake | `Media/development/P-thank-you/art.png` |
| **p31** | **KEEP / FAVORITE** | Closer-zoom page-fill (Jon 2026-07-23) · approved source untouched · prev framed → `art-PREV-framed-before-closer-zoom.png` | `Media/development/P-author/art.png` |
| **p32** | Was FAIL res → **PASS tech** | SeedVR + cream dissolve → 2625² · content keep-leaning · Jon eye still open | `…/P-quiet-close/art-left.png` |
| **p33** | Was FAIL res → **PASS tech** | Same · Jon eye still open | `…/P-quiet-close/art-right.png` |

---

## Priority scoreboard (this pass)

| Priority | Count | Units |
|----------|------:|-------|
| **HIGH** | **4** | Cover res · P01 res · **S12** (working / coat / deer) · S12 text-zone confirm after PS |
| **MED** | **5** | p32\|33 Jon eye · S5 arm-in-gutter · spread **FRAME** deferred to finals · Cover/P01 SeedVR · Banana regenerates queue |
| **LOW** | **3** | Gift-clutter density preference · S10 L edge cream softer than p30 · Optional padding p34–36 |

---

## HIGH — fix first

### Cover · **v14-MyPhotoshop-v2** · `Media/development/Cover/art.png`
| Check | Result |
|-------|--------|
| RES | **PASS 2625²** @ 300 DPI (Jon PS · promoted 2026-07-29) |
| FRAME | N/A cover wrap path |
| COAT | N/A (face mostly hidden lock) |
| TEXT | Title + flourish **baked** · **Written by Jack Farrell** = live InDesign |
| Notes | Supersedes beige-v2 (`art-beige-v2-superseded-2026-07-29.png`) · source `v14-MyPhotosho-v1/Cover-art-v2.png` · also: back `art-back.png` · pastedown · spine placeholder |

### P01 Title · **v25** · `Media/development/P01-title/art.png`
| Check | Result |
|-------|--------|
| RES | **2625²** dashboard (from v25 2048) · SeedVR optional on finals |
| FRAME | **OFF** — full-bleed burgundy `#4A0E17` |
| TEXT | Live InDesign on burgundy · **page 1 = RIGHT** of opening (left cream endpaper) |
| Notes | KEEP 2026-07-28 · supersedes v16 (`art-v16-keep-backup.png`) · centered window · tree right |

### S12 God Bless · v22 · **p26\|27** · `Media/development/S12-god-bless/`
| Check | Result |
|-------|--------|
| Status | **working** — Jon Photoshop master in progress |
| RES / TRIP | PASS — 5250×2625 + L/R 2625² |
| FRAME | Soft cream vignette present (early — OK for closing epic) |
| COAT | **FAIL vs G0 v2** — coat reads **closed** on current v22 |
| FACE | Chuckle/moon/star strong; face OK-ish · still dial |
| GUTTER | OK continuous sky · house clear of fold |
| TEXT | Open sky under North Star for **"God bless."** — protect in PS |
| Deer | ~7–8 ahead (target 9 = 4 pairs + Rudolph; Rudolph-only red nose) |
| Notes | **Do not burn more Qwen gens** until Jon delivers PS plate |

---

## MED

| Unit | Issue | Action |
|------|--------|--------|
| **p32\|33** Quiet Close | Tech PASS @ 2625 + FRAME ON · mood keep-leaning | Jon eye approve → flip FLOW `keep` |
| **S5 Chat v01** | Santa left arm crosses fold | Accept or nudge on Banana finals |
| **Story spreads** | Cream **spread** frame = finals-only per Master Dock | Apply `standard spread frame treatment` after lock approve |
| **Banana regenerates** | Phase 3 | Style-lock + santa-G0-v2 pass later |

---

## Locked / keep units — checklist matrix

Legend: ✅ pass · ⚠ watch · ❌ fail · — n/a · 🔒 locked keep

| Unit | Pages | Ver | Status | RES | TRIP | FRAME | COAT | FACE | GUTTER | TEXT | Pri |
|------|-------|-----|--------|-----|------|-------|------|------|--------|------|-----|
| Cover | Cover | v14-PS-v2 | 🔒 keep | ✅ 2625 | — | — | — | OK hide | — | ⚠ title baked · author live | **M** |
| Back cover | Back | v02 | working | ✅ 2625 | — | — | — | — | — | ✅ scrub | **M** |
| Pastedown | Casewrap | v01 | 🔒 keep | ✅ solid | — | — | — | — | — | — | L |
| P01 Title | 1 (RIGHT) | v25 | 🔒 keep | ✅ 2625 | — | OFF (burgundy bleed) | — | — | — | ✅ | **M** |
| P02 About | 2\|3 | v04 | 🔒 keep | ✅ | ✅ | soft L/R | — | — | ✅ corner | ✅ | L |
| S1 Approach | 4\|5 | v13\|v14 | 🔒 keep | ✅ | ✅ split | OFF OK | — | boy OK | n/a split | ✅ | L |
| S2 Threshold | 6\|7 | v06 | 🔒 keep | ✅ | ✅ | OFF OK | ✅ open | ✅ | ✅ | ✅ | L |
| **S3 Eyes Met** | 8\|9 | **v07** | 🔒 **quality bar** | ✅ | ✅ | OFF OK | ✅ open | ✅ G0 | ✅ | ✅ | — |
| S4 Sit Here | 10\|11 | v13 | 🔒 keep | ✅ | ✅ | L ON / R OFF | ✅ open R | ✅ | n/a split | ✅ | L |
| S5 Chat | 12\|13 | v01 | 🔒 keep | ✅ | ✅ | OFF OK | ✅ open | ✅ | ⚠ arm | ✅ | **M** |
| S6 Cocoa | 14\|15 | v04\|v03 | 🔒 keep | ✅ | ✅ | L+R cream | ✅ open R | ✅ | n/a | ✅ | L |
| S7 Proof | 16\|17 | v03 | 🔒 keep | ✅ | ✅ | OFF (unframed lock) | — | boy OK | ✅ | ✅ | L |
| S8 Gone | 18\|19 | v09 | 🔒 keep | ✅ | ✅ | OFF OK | — | boy OK | ✅ | ✅ | L |
| S9 Search | 20\|21 | v06\|v05 | 🔒 keep | ✅ | ✅ *stitched 7-23* | soft | — | boy OK | n/a | ✅ | L |
| S10 Note | 22\|23 | v02 | 🔒 keep | ✅ | ✅ *stitched 7-23* | L ON | — | ✅ | n/a | ✅ | L |
| S11 Wish | 24\|25 | v01 | 🔒 keep | ✅ | ✅ | OFF OK | — | boy OK | ✅ | ✅ L all / R none | L |
| **S12 God Bless** | **26\|27** | v22 | **working** | ✅ | ✅ | soft ON | ❌ closed | ⚠ | ✅ | ⚠ zone | **H** |
| p28\|29 | — | merged | merged | — | — | — | — | — | — | — | — |
| P Thank You | 30 | lora-v03 | 🔒 keep | ✅ | — | ✅ ON | — | — | — | ✅ | L |
| P Author | 31 | closer-zoom | 🔒 FAVORITE | ✅ | — | page-fill | — | Jack lock | — | live later | L |
| Quiet Close | 32\|33 | v02 | working | ✅ | — | ✅ ON | — | — | — | ✅ map | **M** |
| p34 Padding | 34 | v01 | working opt | ✅ | — | ✅ ON | — | — | — | ✅ | L |
| p35 Colophon | 35 | v01 | working opt | ✅ | — | ✅ ON | — | — | — | ✅ open | L |
| p36 Blank | 36 | v01 | working opt | ✅ cream | — | — | — | — | — | — | L |

\*S09 / S10 `art.png` missing earlier this session — **stitched from L\|R** 2026-07-23 (hygiene only, no regen).

---

## FRAME on/off by beat (target)

| FRAME ON (singles / text) | FRAME OFF until finals (story image) |
|---------------------------|--------------------------------------|
| P01 · S4 L · S6 L · S10 L · p30 · p31 · p32 · p33 | S1 · S2 · S3 · S4 R · S5 · S7 · S8 · S9 · S11 |
| S12 closing epic — soft vignette OK early | S6 R currently has cream (Jon KEEP — leave) |

---

## Wardrobe / face quick notes (Santa visible)

| Spread | Coat | Notes |
|--------|------|-------|
| S2 v06 | ✅ open | Wardrobe pass done |
| S3 v07 | ✅ open | Quality bar |
| S4 R v13 | ✅ open | Beckons R |
| S5 v01 | ✅ open | Arm near gutter |
| S6 R v03 | ✅ open | Solo cocoa |
| S12 v22 | ❌ closed | Fix in Jon PS / Banana |

---

## Hygiene done this pass

1. p31 **closer-zoom FAVORITE** → `Media/development/P-author/art.png` (approved `jack-farrell-portrait.png` untouched)
2. p32\|33 SeedVR + cream → 2625² (`v02-upscale-framed`)
3. S09 + S10 `art.png` triplets restored
4. `book_poem_map.py` + `BOOK-COPY-DRAFTS.md` + Flow quiet-close text corrected for p32/p33
5. FLOW notes updated for p30–33

---

## Next (not this pass)

1. Jon finishes **S12 PS master** → swap FLOW primary · re-check coat + nine deer + “God bless.” sky
2. Jon eye **p32\|33** → status `keep`
3. Phase 3: Cover / P01 print size · Banana regenerates · spine/wrap docs only until then
