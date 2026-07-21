# Agent notes — The-Night-I-Met-Santa

Read in order:

1. **`TRUTH.md`**
2. **`AGENT-RUNBOOK.md`** ← **authoritative build procedure** (DTP, print, design, never-dos)
3. **`.cursor/docs/CONTINUE-HERE.md`** ← where to resume book work
4. **`.cursor/docs/PAGE-BUILD-WORKFLOW.md`** ← image → PSD → MOCK-TYPE → InDesign · mocks/RECIPE · tab hygiene
5. **`.cursor/docs/BOOK-PAGE-WORKFLOW.md`** ← full page/poem/image map (draft)
6. **`.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`** ← dialed tools/decisions (this title)
7. **`.cursor/docs/ISSUES-RESOLVED.md`** ← **`log fixes`** + Playbook (MOCK/chops/InDesign)
8. **`.cursor/docs/INDESIGN-PRODUCTION-WORKFLOW.md`** ← InDesign/Lulu specs
9. **`.cursor/docs/IMAGE-LANE-PROMPTS.md`** ← Klein Dial D2 vs Gemini/Banana finals
10. **`.cursor/docs/ILLUSTRATION-STYLE.md`** · **`FONT-CATALOG.md`** · **`CONTINUITY-AND-PRINT-FINALS.md`** · **`TEXT-OVERLAY-POLICY.md`**
11. **`BOOK-PLAYBOOK.md`** ← future-book master (repo root) — when spinning a new title
12. **`.cursor/docs/ReCall.md`** · **`.cursor/docs/START-HERE.md`**

**Do not** auto-load: fleet mirrors (`IMAGE-WORKFLOW.md`, `3D-*`, Hostinger, Showcase), superseded stubs (`BOOK-PLAN`, `SPREAD-STORY-MAP` → `_archive/docs/`), or Tony handoff (`ADOBE-TNYSE-WORKFLOW`) unless asked.

## Project facts

- **Root:** `D:\Hermes\projects\The-Night-I-Met-Santa`
- Hermes fleet sibling (shared docs/skills/rules). Isolated Mem0: `the-night-i-met-santa`
- Gift book for Jack Farrell · birthday **2026-08-15** · Lulu **8.5×8.5"** · **35–40 pages**
- **Art default:** painted gouache / soft watercolor — **not** colored pencil (see `ILLUSTRATION-STYLE.md`)
- **Image lanes:** Klein **9B** dial (D2) → Qwen alt → Klein **4B** light → Gemini/Banana finals (**master**) — `IMAGE-LANE-PROMPTS.md`
- **Image providers:** **fal.ai first** · OpenRouter second
- **Production:** **page-by-page** Lane A→B. Never call anything “final.”
- **Layout:** **InDesign UXP** (`AGENT-RUNBOOK.md`). Pillow/Typst = **fallback only**. Affinity = optional polish.
- **Locks:** cover beige-v2 · boy G0 · santa-G0 · Jack portrait style-match-B · eyes-met FINAL-TEST-A · **P01 title = v22** (`Media/approved/pages/p01-title.png`, provisional 2026-07-21)
- **Jack Farrell portrait:** `Media/approved/characters/jack-farrell-portrait.png` · `CHARACTER-JACK-FARRELL.md`
- **DTP:** Affinity MCP + InDesign UXP Bridge **READY** · Photoshop adobepy UXP **LIVE** — `tools/layout-mcp/SETUP.md` · PS `PHOTOSHOP-SETUP.md`

## Paths

| Asset | Path |
|-------|------|
| Poem | `Transcription/poem-clean.txt` |
| Art pipeline | `Media/approved/` · `Media/generated/` (incl. `mocks/`) · `Media/assets/` |
| Photo / layout refs | `Images/references/` |
| InDesign chops | `Images/chopz/` |
| Fonts (local) | `Xtraz/Fonts/` (gitignored) · `FONT-CATALOG.md` |
| InDesign / Photoshop / Affinity | `Xtraz/Adobe-inDesign/` · `Xtraz/Adobe-Photoshop/` · `Xtraz/Affinity/` |
| Lulu templates / PDF exports | `Xtraz/Lulu-Templates/` · `Output/interiors/` · `Output/covers/` |
| `Pages/` | **Deprecated** — empty fallback only (`Pages/README.md`) |
| Scratch / archive | `scripts/_scratch/` · `_archive/docs/` · `_archive/images-scratch/` |
| Build runbook | `AGENT-RUNBOOK.md` |
| Problem → fix log | `.cursor/docs/ISSUES-RESOLVED.md` (**log fixes**) |

## Rules

- Assets live at **project root**, not `.cursor/assets/`
- **InDesign** for poem text-on-art (cloud PNG + Cormorant). Do **not** use Pillow as the gift path.
- Do not auto-revive archived Typst v3/v4 or `_archive/docs/` maps
- Page-by-page only; Jon approves each; never regenerate G0 locks
- Keep `Images/` (refs + chops) separate from `Media/` (generated/approved art)
