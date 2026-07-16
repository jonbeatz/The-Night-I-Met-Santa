# Agent notes — The-Night-I-Met-Santa

Read in order:

1. **`TRUTH.md`**
2. **`.cursor/docs/START-HERE.md`**
3. **`.cursor/docs/CONTINUE-HERE.md`** ← where to resume book work
4. **`.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`** ← dialed tools/decisions (this title)
5. **`.cursor/docs/IMAGE-LANE-PROMPTS.md`** ← Klein mockup vs Gemini/Banana finals prompts
6. **`BOOK-PLAYBOOK.md`** ← future-book master (repo root)
7. **`.cursor/docs/FONT-CATALOG.md`** ← type roles (Cormorant / Cinzel / scripts)
8. **`.cursor/docs/CONTINUITY-AND-PRINT-FINALS.md`** ← print-res remake + boy/Santa continuity
9. **`.cursor/docs/TEXT-OVERLAY-POLICY.md`** ← how text sits on art (open zones, not gray blobs)
10. **`.cursor/docs/BOOK-PLAN.md`**
11. **`.cursor/docs/ReCall.md`**

## Project facts

- **Root:** `D:\Hermes\projects\The-Night-I-Met-Santa`
- Hermes fleet sibling (shared docs/skills/rules). Isolated Mem0: `the-night-i-met-santa`
- Gift book for Jack Farrell · birthday **2026-08-15** · Lulu **8.5×8.5"**
- **Art default:** painted gouache / soft watercolor — **not** colored pencil (see `ILLUSTRATION-STYLE.md`; keepers `Media/generated/test-batch-v2/`)
- **Image lanes:** Klein dial (**D2 style**) → Qwen fallback → Gemini/Banana finals (**master style**) — `IMAGE-LANE-PROMPTS.md`
- **Production:** **page-by-page** Gemini finals (Klein full-book dumps rejected)
- **Locks:** cover beige-v2 · boy G0 · santa-G0 · Jack portrait style-match-B · eyes-met FINAL-TEST-A
- **Jack Farrell portrait:** `Media/approved/characters/jack-farrell-portrait.png` · `CHARACTER-JACK-FARRELL.md`
- Layout v3–v5 rejected — build organic cloud overlay / bleed spread next
## Paths

| Asset | Path |
|-------|------|
| Poem | `Transcription/poem-clean.txt` |
| Art | `Media/` (project root) |
| **Approved keepers** | **`Media/approved/`** (Tier A `style-refs/` moodboard · Tier B locks — `INDEX.md`) |
| Fonts (local) | `Xtraz/Fonts/` (gitignored) · catalog `FONT-CATALOG.md` |
| Future playbook | `BOOK-PLAYBOOK.md` |

| Layout refs | `Images/references/layout/` |
| Findings | `Book-Findings.md` |
| Compositor | `composite_pages.py` |
| Typst | `book-final.typ` |
| Rejected sources | `_archive/layout-attempts/` |

## Rules

- Assets live at **project root**, not `.cursor/assets/`
- Pillow pre-composite poem pages; no Typst PNG alpha stacks
- Do not auto-revive archived Typst v3/v4
