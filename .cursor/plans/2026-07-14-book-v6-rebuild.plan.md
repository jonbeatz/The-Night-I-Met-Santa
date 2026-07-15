# Book v6 Rebuild Plan — The Night I Met Santa

**Date:** 2026-07-14  
**Status:** G2 locked — 32 pages · 3–4 cinematic spreads · copy drafts ready  
**Goal:** Polished holiday picture book, Lulu 8.5×8.5" casewrap HC, gift Aug 15  
**Copy file:** `.cursor/docs/BOOK-COPY-DRAFTS.md`

---

## Research verdict (agents + prior RESEARCH-VERDICT)

| Decision | Choice |
|----------|--------|
| Trim | **8.5 × 8.5"** |
| Target interior | **32 pages** (even; industry sweet spot; Lulu HC min 24) |
| Printer | **Lulu** casewrap hardcover |
| Layout | Pillow **organic cloud / snow-area text** → flat JPEG → Typst binder |
| Style | Painterly Christmas storybook (Santore-adjacent) — **polish / redo**, not revive v3–v5 |
| Avoid | White square text boxes · Typst PNG alpha stacks · blank white pages · KDP square HC |

---

## Poem → image count

Poem (`Transcription/poem-clean.txt`): **15 narrative stanzas** (+ closing “God bless.”).

| Asset class | Count | Notes |
|-------------|------:|-------|
| Story illustrations (action-matched) | **15** | One per stanza; redo for polish + character lock |
| True double-page spreads (optional) | **3–4** | Same scenes as wide canvases; split to 2 PDF pages |
| Front-matter illustrations | **4** | Title · copyright quiet art · dedication · about story/author |
| Closing / thanks illustrations | **2** | Thank-you to family · final “God bless” vignette |
| Cover wrap | **2** | New **front** + new **back** (spine from page count) |
| **Total unique art pieces to approve** | **~23–25** | 15 story + ~6 matter + 2 covers (± spreads as wider versions) |

Existing `Media/` has ~15 mapped scenes + cover alts — **keep compositions as guides; regenerate polished finals**.

---

## Recommended 32-page map (no blanks)

Every leaf has art (vignette OK). Text integrated into design.

| Page | Content | Art |
|-----:|---------|-----|
| 1 | Title | Full-bleed title art |
| 2 | Copyright / First Edition 2026 | Quiet snow / ornament field |
| 3 | Dedication (family) | Soft vignette |
| 4 | About this story + author note (Jack) | Jack/fireplace or writing desk |
| 5–26 | Poem body (see beat map) | 15 scenes + 3–4 as **spreads** (use 2 pages each) |
| 27–28 | Climactic note / Santa’s wish (if not already a spread) | Spread or full-bleed |
| 29 | Closing stanza + “God bless.” | Warm vignette |
| 30 | Thank you — family & loved ones | Heartfelt illustrated page |
| 31 | Author / “Written by Jack Farrell” reprise | Portrait vignette |
| 32 | Quiet end ornament (“Merry Christmas”) | Matching holiday art — **not blank** |

Adjust spread count so total stays **32**. Default body math:

**G2 LOCKED (2026-07-14):** 32 pages · **4 cinematic spreads** · remaining beats as singles.

**Body math:** 11 singles + 4 spreads (8 pages) = **19** story pages · rest = front/back matter inside 32.

### Story beat → illustration (action-matched)

| # | Poem beat | Scene action to show |
|--:|-----------|----------------------|
| 1 | Heard noise / peeked | Child sneaking toward toys / room glow |
| 2 | Decided to go to door | Decorated bolted door; child at threshold |
| 3 | Entered / “sneak up on Santa” | Child entering; Santa half-seen among gifts |
| 4 | Eyes met / splendor | Face-to-face: white hair, red coat, suspenders |
| 5 | Floor among gifts / “Sit over here” | Santa on floor beckoning; ribbons/boxes |
| 6 | Chatted & laughed | Warm two-shot by tree / gifts |
| 7 | Stories, cocoa (not milk) | Santa with cocoa; cozy storytelling |
| 8 | Roof noise → needs proof → photo idea | Child + camera idea; rooftop sounds cue |
| 9 | Dash for camera; Santa gone | Empty room / open door; child with camera |
| 10 | Search for clue (hat/shoe) | Searching under tree / room |
| 11 | Flue + chair | Looking up chimney; object on chair |
| 12 | Found the note | Note on chair; wonder |
| 13 | Tearing open the note | Hands opening letter; surprise |
| 14 | What he wants: a note | Letter words / warm message visual |
| 15 | Eggnog / belt / “act like a kid… Savior” | Santa’s closing wish; holy/warm Christmas close |

**Spread LOCKED (full 5250×2625):** #4 eyes met · #5 sit-with-Santa · #12–13 note reveal · #15 final blessing.

---

## Print image sizes (Lulu @ 300 DPI)

| Use | Inches (with bleed) | Pixels @ 300 DPI |
|-----|---------------------|------------------|
| **One full page** (single side) | **8.75 × 8.75** | **2625 × 2625** |
| Trim live area | 8.5 × 8.5 | 2550 × 2550 |
| Text/face safety | ≥0.5" inside trim | keep content in ~7.5×7.5" |
| **Two-page spread master** | **17.5 × 8.75** | **5250 × 2625** |
| Then export | Left + right halves | each **2625 × 2625** |

**Cover wrap:** After interior upload, download **Lulu’s template**. For ~32 pp casewrap, spine ≈ **0.25"**; wrap ≈ **~19.5 × 10.25"** → ~**5850 × 3075 px** (verify template). Order: Back → Spine → Front.

---

## Text-in-image design (from project refs)

| Mode | Use | Ref |
|------|-----|-----|
| **A — Cloud / snow negative space** | Default for night + busy scenes | `Images/references/layout/ref-overlay-cloud-text.png` |
| **B — Bleed-from-right** | Quieter / contemplative beats | `ref-spread-bleed-text.png` |
| Rejected | Hard white boxes (v3), Typst alpha (v4), soft cream rectangles (v5) | `_archive/layout-attempts/` |

Engineering: generate art without poem text baked in → Pillow paints irregular cloud/feathered paper → set Georgia (or similar) → **flat JPEG**. Typst only places pages + thin front matter labels if needed.

---

## Toolchain (re-audited)

| Step | Tool | Status |
|------|------|--------|
| Character lock + polish | fal **nano-banana-pro** (+ Jack refs) | READY |
| Drafts | HF / flux via JonBeatz `image:*` | READY |
| Local inpaint/upscale | ComfyUI | As needed |
| Page composite | Rewrite `composite_pages.py` → cloud @ **2625** | MUST REWRITE |
| Binder | `book-final.typ` | READY after Pages exist |
| Cover | `build_cover_v2.py` + new art; fix page-count spine | READY shell |
| Skip this cycle | Affinity, LaTeX, DesignMD, WeasyPrint, KDP HC | — |

---

## Approval gates (do not skip)

| Gate | What Jon approves | Before… |
|------|-------------------|---------|
| **G0** | Style lock: Santa sheet + Jack/Dad sheet (3–5 refs) | Any batch regen |
| **G1** | Layout mode: cloud default ± bleed-spread mix; **1 sample page** | Batch composites |
| **G2** | **This 32-page map** + which beats are spreads | Regenerating all art |
| **G3** | Each story illo + cover/back (one-by-one or thrice a week) | Final composites |
| **G4** | All `Pages/page-NN` with text placement | Interior PDF |
| **G5** | Interior PDF digital flip (8.75" pages) | Lulu upload |
| **G6** | Cover wrap from Lulu template | Order |
| **G7** | Cheap physical proof (~Jul 25–28) | Gift hardcover |
| **G8** | Gift HC order | Ship for Aug 15 |

---

## Week-one build sequence

1. Approve **G2 page map** + layout mode (this doc)  
2. **G0** style lock (fal + refs)  
3. Rewrite compositor + **G1** sample page  
4. Polish/regenerate story art → **G3**  
5. New cover + back → approve  
6. Write about-story + thanks copy with Jon  
7. Batch Pages → Typst → G5–G8  

---

## Copy status

| Piece | Status |
|-------|--------|
| Dedication | Locked |
| About This Story | **Locked Draft A** (2026-07-14) |
| Thank You | **Locked Draft A** (2026-07-14) |
| Spreads | **Locked** — 4 cinematic moments |
| Canonical file | `.cursor/docs/BOOK-COPY-DRAFTS.md` |

Next gate: **G0 style lock** (Santa + Jack).
