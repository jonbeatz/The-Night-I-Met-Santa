# ReCall.md — The-Night-I-Met-Santa

## Current focus
**InDesign = production** (runbook authority). Pillow/Typst = fallback only.  
**Page count locked: 35–40.** Working map: **`.cursor/docs/BOOK-PAGE-WORKFLOW.md`**.  
**Creative loop (dialing):** **`.cursor/docs/PAGE-BUILD-WORKFLOW.md`** — mocks/`vNN`+RECIPE → new PSD → **close PNG** → MOCK-TYPE (30pt `#2C2C2C`) → cloud → InDesign.  
Smoke unit: `p03-dedication.psd` · mocks `Media/generated/mocks/P03-dedication/v01/`.  
**Spread build loop:** PS MOCK + chops (`Images/chopz/`) → InDesign → live Cormorant (poem 20/26).  
**Continuity:** Boy G0 + Santa G0 in `Media/approved/characters/`.  
Working `.indd`: `eyes-met-prototype-v1.indd` · also `p03-dedication-smoke.indd`.  
Prototype pages **4–5** = eyes-met (= final book **S3 / pages 10\|11**).

**DTP:** Affinity MCP + InDesign UXP Bridge + **Photoshop adobepy UXP LIVE** (`:47391` / `:8766`). Cold flow: CC Desktop signed in (Jon confirms) → agent UDT+apps+bridges → **Jon Load & Watch** → MCP.

**PSD blanks locked:** `Xtraz/Adobe-Photoshop/` → `spread-page-template.psd` · `single-page-template.psd` · `book-covers-template.psd` (no spine-only PSD). Open **one working PSD** at a time; close source PNGs after place.

## Birthday deadline
**2026-08-15** — Lulu hardcover gift for Jack Farrell. Order proof by **~July 25–28**.

## Last updated
2026-07-20 — **PAGE-BUILD-WORKFLOW** dialed (mocks+RECIPE, close PNG, MOCK-TYPE 30pt #2C2C2C, G0 continuity). Fleet Google dual OAuth still noted. **Next:** confirm BOOK-PAGE-WORKFLOW → next page unit with full recipe loop.

## Where to continue
1. **Confirm** `.cursor/docs/BOOK-PAGE-WORKFLOW.md` (page count, L/R poem splits, About + Jack pages)
2. Run next unit via **`PAGE-BUILD-WORKFLOW.md`** (recipe + PSD tab hygiene)
3. Generate story art with G0 refs when boy/Santa appear
4. Hide/delete MOCK-REF when pages approved in full book doc
5. Optional: Lulu `.joboptions` + smoke PDF → `Output/interiors/`

## Reference (new this session)
- **PAGE-BUILD-WORKFLOW.md** — image → PSD → InDesign creative loop (living)
- **BOOK-PAGE-WORKFLOW.md** — authoritative page/poem/image map (draft)
- **Photoshop UXP MCP:** `tools/layout-mcp/PHOTOSHOP-SETUP.md` — LIVE; COM MCPs skip
- **Adobe CC MCP watchlist:** `.cursor/docs/ADOBE-CC-MCP-GUIDE.md`
- **ArcRift:** fleet `TOOLS-WATCHLIST` — C (74) WATCH record; do not install (Mem0/Mnemosyne primary)

## System of record
| Doc | Use |
|-----|-----|
| **PAGE-BUILD-WORKFLOW.md** | Per-page creative loop · mocks · RECIPE · MOCK-TYPE · tab hygiene |
| **BOOK-PAGE-WORKFLOW.md** | Full interior map — poem · art · filenames · matter |
| **BOOK-PLAYBOOK.md** (repo root) | Future-book master |
| **BOOK-PRODUCTION-SYSTEM.md** | Living ops for *this* title |
| **SPREAD-STORY-MAP.md** | Earlier 12-spread proposal (numbering → see WORKFLOW) |
| **IMAGE-LANE-PROMPTS.md** | Klein D2 vs Gemini master (do not mix) |
| CONTINUE-HERE | Next actions |
| FONT-CATALOG | Type roles |
| TEXT-OVERLAY-POLICY | Type on art |
| ILLUSTRATION-STYLE | Painted gouache default |
| PAGE-PROMPT-BIBLE | Beat prompts |
| CHARACTER-JACK-FARRELL | Author portrait |
| CONTINUITY-AND-PRINT-FINALS | Print remake plan |
| **LAYOUT-APP-AUTOMATION-RESEARCH** | Affinity/InDesign MCP — **READY 2026-07-19** |
| **tools/layout-mcp/SETUP.md** | How to start bridge + load UXP plugin |
| **ADOBE-CC-MCP-GUIDE.md** | Adobe MCP watchlist (verified 2026-07-19; PS LIVE 2026-07-20) — optional AE/Premiere later |
| **tools/layout-mcp/PHOTOSHOP-SETUP.md** | Photoshop adobepy UXP MCP — **LIVE** |
| LULU-8.5-SQUARE-CHEATSHEET | Trim, bleed, safety, cover-template notes |

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
| InDesign Bridge plugin | `tools/layout-mcp/indesign-uxp-server/plugin/manifest.json` |
| **Photoshop working** | **`Xtraz/Adobe-Photoshop/`** (default agent save folder) |
| Photoshop UXP setup | `tools/layout-mcp/PHOTOSHOP-SETUP.md` |

## Decisions locked
- Format: **8.5×8.5"** · Printer: **Lulu** · Color: **sRGB** · **35–40 pages** (locked)
- Layout: **InDesign UXP** = production (`AGENT-RUNBOOK.md`); Pillow/Typst = **fallback only**; Affinity = optional polish
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
- **Spread loop (2026-07-20):** PS MOCK 5250×2625 + chops → InDesign → live type; prefer PNG; layers Frame→Type→Cloud→Art
- **PSD blanks:** `spread-page-template.psd` (5250×2625) · `single-page-template.psd` (2625²) · `book-covers-template.psd` (2625² front/back) — cyan=TRIM · magenta=SAFETY · orange=MOCK; **no** spine-only PSD (Lulu casewrap after interior)
- **Poem type (2026-07-20):** Cormorant Garamond **Medium 20/26 tracking +5 centered #2C2C2C**
- **MOCK-TYPE PSD preview (2026-07-20):** poem **20/26** · matter **30/~40** · `#2C2C2C` — mirrors ID by role; close source PNG after place
- **PS ↔ ID (2026-07-20):** same pixel counts (2625² / 5250×2625) full-bleed place = 300 DPI; ignore 72 dpi tag; full-canvas textCloud
- **No fake gutter** in spread art (orange fold = MOCK guide only)
- **Klein dial:** 4B + **Dial D2** append only (`IMAGE-LANE-PROMPTS.md`)
- **Docs triggers:** `update docs` = workflow harvest · `log fixes` = ISSUES card (`PAGE-BUILD-WORKFLOW.md` §11)
- **Page build loop:** `.cursor/docs/PAGE-BUILD-WORKFLOW.md` · `Media/generated/mocks/{unit}/vNN/` + **RECIPE.md**
- **Print pixels:** page **2625²** · spread **5250×2625** = full **300 DPI** at Lulu bleed size (Pass B); dial may be lower
- **No fake gutter** on final spread art (MOCK-only fold OK)
- **DTP (2026-07-19 FINAL):** Affinity MCP `:6767` + InDesign UXP `:19300/:19301` **IN USE**. Cold flow: CC Desktop signed in (**Jon confirms**) → agent launches UDT+InDesign+bridge → **Jon clicks Load & Watch** (agent cannot) → MCP. Web adobe.com login not enough. Keep CC installed; Startup disable OK.
- **Photoshop MCP (2026-07-20 LIVE):** adobepy UXP broker `:47391` + dcc-mcp-photoshop `:8766/mcp` — **not** COM. Prefs: Enable Developer Mode only. Doc: `tools/layout-mcp/PHOTOSHOP-SETUP.md`. COM MCPs (loonghao/alisaitteke) rejected on this PC (`0x80080005`). **Default save folder:** `Xtraz/Adobe-Photoshop/`
- **Creative Cloud:** keep Desktop app installed (licensing); OK to disable Startup — do **not** uninstall while keeping InDesign/UDT

## Session note 2026-07-20 — PAGE-BUILD-WORKFLOW dial-in
- Canonical loop: `.cursor/docs/PAGE-BUILD-WORKFLOW.md` · mocks `Media/generated/mocks/` + RECIPE.md · close PNG after place
- MOCK-TYPE defaults: Cormorant Medium 30pt / #2C2C2C (from p03-dedication)
- Continuity: Boy G0 + Santa G0 always for character scenes
- Smoke: p03-dedication.psd still working unit
