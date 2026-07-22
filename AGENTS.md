# Agent notes — The-Night-I-Met-Santa

## Always open (book work) — these four only

1. **`.cursor/docs/JON-BOOK-FLOW-v2-FINAL.md`** — page map / rhythm / GPT pillars  
2. **`.cursor/docs/MASTER-PRODUCTION-DOCK.md`** — prompts  
3. **`.cursor/docs/IMAGE-LANE-SYSTEM-v2.md`** — lanes · boards · flipbook · hero spend  
4. **`AGENT-RUNBOOK.md`** — InDesign / print / never-dos  

**Current plates SoT:** `Media/generated/mocks/_FLOW-CURRENT.json` (flipbook reads this only).

**Session resume:** `TRUTH.md` → `CONTINUE-HERE.md` → `ReCall.md` → then the four above.

Everything else is **reference on demand** (do not auto-load): `PAGE-BUILD-WORKFLOW`, `BOOK-PAGE-WORKFLOW`, `BOOK-PRODUCTION-SYSTEM`, `ISSUES-RESOLVED`, `INDESIGN-PRODUCTION-WORKFLOW`, `IMAGE-LANE-PROMPTS`, `ILLUSTRATION-STYLE`, `FONT-CATALOG`, `BOOK-PLAYBOOK`, fleet mirrors, archives, Tony handoff.

## Project facts

- **Root:** `D:\Hermes\projects\The-Night-I-Met-Santa`
- Gift book for Jack Farrell · birthday **2026-08-15** · Lulu **8.5×8.5"**
- **Art:** painted gouache / soft watercolor · **fal.ai first**
- **Style lock:** `Media/approved/style-refs/style-lock-v2.png` (Krea regen + santa-G0-v2)
- **Santa lock:** `Media/approved/characters/santa-G0-v2.png` (S4 v08 Banana Pro) — suspenders over coat · open collar
- **Hero spend:** GPT High 4K **only** if `gpt_pillar: true` (S3 · S12b). **Primary finals** = Banana Pro `/edit` + style-lock-v2 + santa-G0-v2. Alt = pure Krea atmospheric.
- **Dial:** Klein 9B primary · Qwen 2 Pro `/edit` favorite mock look · always attach style-lock-v2
- **Comparison boards:** one board per decision (Klein | new | favorite). Retroactive S04 multi-boards = archive.
- **Locks:** cover beige-v2 · boy G0 · **santa-G0-v2** · Jack portrait · eyes-met · P01 v22
- **Layout:** InDesign UXP · Photoshop adobepy LIVE

## Paths

| Asset | Path |
|-------|------|
| Poem | `Transcription/poem-clean.txt` |
| Current plates | `Media/generated/mocks/_FLOW-CURRENT.json` |
| Art | `Media/approved/` · `Media/generated/mocks/` |
| Flipbook | `Output/flipbook-{date}.pdf` |
| InDesign / PS | `Xtraz/Adobe-inDesign/` · `Xtraz/Adobe-Photoshop/` |

## Rules

- Never call anything “final.” Never regen G0 / locked plates without Jon.
- Update `_FLOW-CURRENT.json` when a plate or verdict changes (`decided_by` + `date` required).
- Then rebuild flipbook: `npm run book:flipbook`
- **`project-log.md` = milestones/decisions only** — not individual model tests or comparison-board runs. Document tests/boards in each version’s `RECIPE.md` and in `_FLOW-CURRENT.json`. Log to `.cursor/docs/project-log.md` only when: a spread is locked, a character reference is promoted, or a production phase completes.
