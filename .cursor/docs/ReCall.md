# ReCall.md — The-Night-I-Met-Santa

## Current focus
**Page-by-page Gemini finals** — one page/open at a time with locked G0s; Jon approves each.  
Klein full-book batches (`test-book-v1` / `v2`) **rejected** — do not repeat.  
Cover + cast locks held; story interiors still need careful remakes.

## Birthday deadline
**2026-08-15** — Lulu hardcover gift for Jack Farrell. Order proof by **~July 25–28**.

## Last updated
2026-07-15 late — cast style-match + page-by-page pivot after failed Klein book dumps.

## Where to continue
1. **Start page-by-page** — recommend S01 Approach LEFT (or eyes-met open as style anchor)
2. Lane B: **Gemini 3 Pro Image** (OpenRouter) or Banana `/edit` + boy/Santa G0 + style refs — **not** cover-as-ref on every interior
3. Pick **back cover** → `covers/cover-back.png`
4. Golden text page (**Cormorant**) → `composite_pages.py` → Typst → Lulu proof

## System of record
| Doc | Use |
|-----|-----|
| **BOOK-PLAYBOOK.md** (repo root) | Future-book master |
| **BOOK-PRODUCTION-SYSTEM.md** | Living ops for *this* title |
| **SPREAD-STORY-MAP.md** | 12-spread / 32-page map (proposed) |
| **IMAGE-LANE-PROMPTS.md** | Klein D2 vs Gemini master (do not mix) |
| CONTINUE-HERE | Next actions |
| FONT-CATALOG | Type roles |
| TEXT-OVERLAY-POLICY | Type on art |
| ILLUSTRATION-STYLE | Painted gouache default |
| PAGE-PROMPT-BIBLE | Beat prompts |
| CHARACTER-JACK-FARRELL | Author portrait |
| CONTINUITY-AND-PRINT-FINALS | Print remake plan |

## Paths
| What | Where |
|------|--------|
| Poem | `Transcription/poem-clean.txt` |
| **Approved** | **`Media/approved/`** |
| Cover LOCKED | `Media/approved/covers/cover-front.png` (beige-v2) |
| Boy G0 | `Media/approved/characters/boy-narrator-G0.png` |
| Santa G0 (paint north star) | `Media/approved/characters/santa-G0.png` |
| Jack portrait | `Media/approved/characters/jack-farrell-portrait.png` |
| Eyes-met | `Media/approved/spreads/spread-eyes-met.png` |
| Failed Klein mocks | `Media/generated/test-book-v1/` · `test-book-v2/` (gitignored) |

## Decisions locked
- Format: **8.5×8.5"** · Printer: **Lulu** · Color: **sRGB** · ~**32 pages** spread-first
- Layout: **Pillow cloud composite** → Typst binder
- Style: **Painted gouache** (not colored pencil)
- **Image lanes:** dial Klein 4B (cheap probes only) → Qwen fallback → **finals Gemini/Banana**
- **Dual prompts:** Klein = D2 append · Finals = ILLUSTRATION-STYLE master (`IMAGE-LANE-PROMPTS.md`)
- **Cover:** beige-v2 · oatmeal holly PJs · **Santa face HIDDEN** on cover
- **Boy G0:** style-match-A (santa-G0 polish)
- **Santa G0:** paint north star for cast
- **Jack portrait:** style-match-B
- **Eyes-met:** FINAL-TEST-A
- **Credits:** copyright — First illustrated edition 2026 / Written by Jack / Book design by Jon · back — Illustrated edition designed by Jon Farrell · 2026
- **Copy:** About + Thank You Draft A · quiet close locked
- **Production mode:** **page-by-page** approvals (no whole-book Klein dumps)
