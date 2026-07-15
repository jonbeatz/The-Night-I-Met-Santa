# Agent notes — The-Night-I-Met-Santa

Read in order:

1. **`TRUTH.md`**
2. **`.cursor/docs/START-HERE.md`**
3. **`.cursor/docs/CONTINUE-HERE.md`** ← where to resume book work
4. **`.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`** ← dialed tools/decisions (reuse for future books)
5. **`.cursor/docs/TEXT-OVERLAY-POLICY.md`** ← how text sits on art (open zones, not gray blobs)
6. **`.cursor/docs/BOOK-PLAN.md`**
7. **`.cursor/docs/ReCall.md`**

## Project facts

- **Root:** `D:\Hermes\projects\The-Night-I-Met-Santa`
- Hermes fleet sibling (shared docs/skills/rules). Isolated Mem0: `the-night-i-met-santa`
- Gift book for Jack Farrell · birthday **2026-08-15** · Lulu **8.5×8.5"**
- **Art default:** painted gouache / soft watercolor — **not** colored pencil (see `ILLUSTRATION-STYLE.md`; keepers `Media/generated/test-batch-v2/`)
- **Image lanes:** dial Klein 4B → fallback Qwen Image 2 → finals Banana `/edit`+refs (`BOOK-PRODUCTION-SYSTEM.md` §2)
- Layout v3–v5 rejected — build organic cloud overlay / bleed spread next
## Paths

| Asset | Path |
|-------|------|
| Poem | `Transcription/poem-clean.txt` |
| Art | `Media/` (project root) |
| Layout refs | `Images/references/layout/` |
| Findings | `Book-Findings.md` |
| Compositor | `composite_pages.py` |
| Typst | `book-final.typ` |
| Rejected sources | `_archive/layout-attempts/` |

## Rules

- Assets live at **project root**, not `.cursor/assets/`
- Pillow pre-composite poem pages; no Typst PNG alpha stacks
- Do not auto-revive archived Typst v3/v4
