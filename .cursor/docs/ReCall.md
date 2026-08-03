# ReCall.md — The-Night-I-Met-Santa

## Session resume (read in order)

1. `TRUTH.md`
2. `.cursor/docs/START-HERE.md`
3. **This file** — `.cursor/docs/ReCall.md`
4. `.cursor/docs/CONTINUE-HERE.md`
5. **`.cursor/docs/LULU-ORDER-CHECKLIST.md`** + **`Xtraz/Lulu-Templates/from-lulu/`**
6. **`.cursor/docs/MERGED-PLATE-EXPORT-WORKFLOW.md`** — finals export playbook
7. **`.cursor/docs/COVER-REBUILD-WORKFLOW.md`** — Front/Back → Wrap → INDD → flipbook
8. Always-open: Flow v2 · Master Dock · IMAGE-LANE-v2 · `AGENT-RUNBOOK.md`
9. SoT plates: `Media/generated/mocks/_FLOW-CURRENT.json`

## Current focus
**Print-ready path almost closed.** Interior + Cover + Flipbook PDFs refreshed · back-cover mantel/curtains (`Merged-Back-Cover-BG`) propagated through Wrap/INDD/flipbook · thank-you spread locked · **not ordered.** Soft-proof Cover vs Lulu guides; optional QR/credits nudge still open from Phase C leave-off.

## Birthday deadline
**2026-08-15** — Lulu hardcover gift for Jack Farrell.

## Last updated
2026-08-03 — Session harvest: print PDF audit + back BG update + sled vector recipe.

### Print / PDF (2026-08-02 night)
- PDFs: `Output/FINAL-Master-PDFs/` — Interior (Lulu Interior) · Cover (Lulu Cover) · Flipbook (HQ Print, preview only)
- Notes: `Output/FINAL-Master-PDFs/PRINT-READINESS-NOTES-2026-08-02.md`
- **RGBA trap:** opaque RGBA spreads (`P02`, thank-you) exported as ~117 DPI tiles — flatten to **RGB** before Lulu PDF. Fixed + verified ~301 DPI.
- **Cover “12 DPI” Hermes flag:** false alarm — QR is ~300 DPI at placed size (~0.78″); don’t divide by full 19″ wrap width.
- Softcover: **not needed** for gift (HC casewrap). Same interior PDF; paperback needs separate Lulu cover template.

### Cover / back BG
- Back PSD SoT includes `covers` (mantel/curtain) + **`Merged-Back-Cover-BG`**
- Propagate: `npm run book:cover:rebuild-wrap` → `book:cover:art-notype` → Cover INDD relink → rebake flipbook FRONT/BACK from Cover export
- Flipbook square crop can clip tree/QR on the right — **expected**; print SoT is Cover wrap, not flipbook trim

### Thank-you / poem close (locked)
- Poem **“God bless.”** baked on **S11** art · S12 = Merry Christmas graphic in art
- Thank-you: gold logos in art · live white body + *God bless.* sign-off · portrait right

### Sled silhouette vector (reusable)
- Source: `Images/references/sled1.psd`
- **Winner:** Illustrator Image Trace (B&W) after upscale+blur+threshold → `sled1-vector.ai` / `.svg` / `.eps`
- Photoshop Work Path OK for simple logos; complex silhouettes → Illustrator. Judge smoothness in AI at 400%, not browser PNG previews.

## Start here next
1. Soft-proof Cover PDF vs Lulu guides (QR left/up · credits inward if still needed)  
2. Re-upload Interior to Lulu when Jon OK (same 34 pp → same spine)  
3. Cover PDF upload → proof only when Jon says order  
4. **Do not order** until explicit OK  

## System of record
| Doc | Use |
|-----|-----|
| **COVER-REBUILD-WORKFLOW.md** | Front/Back edit → Wrap → art-notype → INDD → flipbook |
| **LULU-ORDER-CHECKLIST.md** | Phases A–E |
| **PRINT-READINESS-NOTES-*** | Latest PDF audit |
| **AGENT-RUNBOOK.md** | Print authority |
| CONTINUE-HERE | Next actions |
