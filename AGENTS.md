# Agent notes — The-Night-I-Met-Santa

Read in order:

1. **`TRUTH.md`**
2. **`AGENT-RUNBOOK.md`** ← **authoritative build procedure** (DTP, print, design, never-dos)
3. **`.cursor/docs/START-HERE.md`**
4. **`.cursor/docs/CONTINUE-HERE.md`** ← where to resume book work
5. **`.cursor/docs/INDESIGN-PRODUCTION-WORKFLOW.md`** ← InDesign/Lulu specs
6. **`.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`** ← dialed tools/decisions (this title)
7. **`.cursor/docs/IMAGE-LANE-PROMPTS.md`** ← Klein mockup vs Gemini/Banana finals prompts
8. **`BOOK-PLAYBOOK.md`** ← future-book master (repo root)
9. **`.cursor/docs/FONT-CATALOG.md`** ← type roles (Cormorant / Cinzel / scripts)
10. **`.cursor/docs/CONTINUITY-AND-PRINT-FINALS.md`** ← print-res remake + boy/Santa continuity
11. **`.cursor/docs/TEXT-OVERLAY-POLICY.md`** ← how text sits on art (open zones, not gray blobs)
12. **`.cursor/docs/BOOK-PLAN.md`**
13. **`.cursor/docs/ReCall.md`**

## Project facts

- **Root:** `D:\Hermes\projects\The-Night-I-Met-Santa`
- Hermes fleet sibling (shared docs/skills/rules). Isolated Mem0: `the-night-i-met-santa`
- Gift book for Jack Farrell · birthday **2026-08-15** · Lulu **8.5×8.5"** · **35–40 pages**
- **Art default:** painted gouache / soft watercolor — **not** colored pencil (see `ILLUSTRATION-STYLE.md`; keepers `Media/generated/test-batch-v2/`)
- **Image lanes:** Klein dial (**D2 style**) → Qwen fallback → Gemini/Banana finals (**master style**) — `IMAGE-LANE-PROMPTS.md`
- **Production:** **page-by-page** Lane A→B (Klein full-book dumps rejected). Never call anything “final.”
- **Layout production:** **InDesign UXP** (`AGENT-RUNBOOK.md`). Pillow/Typst = **fallback only**. Affinity = optional polish.
- **Locks:** cover beige-v2 · boy G0 · santa-G0 · Jack portrait style-match-B · eyes-met FINAL-TEST-A
- **Jack Farrell portrait:** `Media/approved/characters/jack-farrell-portrait.png` · `CHARACTER-JACK-FARRELL.md`
- **DTP:** Affinity MCP + InDesign UXP Bridge **READY** — cold-start in `AGENT-RUNBOOK.md` §1 / `tools/layout-mcp/SETUP.md`

## Paths

| Asset | Path |
|-------|------|
| Poem | `Transcription/poem-clean.txt` |
| Art | `Media/` (project root) |
| **Approved keepers** | **`Media/approved/`** (Tier A `style-refs/` moodboard · Tier B locks — `INDEX.md`) |
| Cloud assets | `Media/assets/` |
| Fonts (local) | `Xtraz/Fonts/` (gitignored) · catalog `FONT-CATALOG.md` |
| InDesign working docs | `Xtraz/Adobe-inDesign/` (gitignored via `Xtraz/`) |
| Affinity working docs | `Xtraz/Affinity/` (optional) |
| Lulu templates | `Xtraz/Lulu-Templates/` |
| Lulu PDF exports | `Output/interiors/` · `Output/covers/` |
| Build runbook | `AGENT-RUNBOOK.md` |
| Future playbook | `BOOK-PLAYBOOK.md` |
| Layout refs | `Images/references/layout/` |
| Findings | `Book-Findings.md` |
| Fallback compositor | `composite_pages.py` (emergency only) |
| Fallback Typst | `book-final.typ` (emergency only) |
| Rejected sources | `_archive/layout-attempts/` |

## Rules

- Assets live at **project root**, not `.cursor/assets/`
- **InDesign** for poem text-on-art (cloud PNG + Cormorant). Do **not** use Pillow as the gift path.
- Do not auto-revive archived Typst v3/v4
- Page-by-page only; Jon approves each; never regenerate G0 locks
