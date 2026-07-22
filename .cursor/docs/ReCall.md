# ReCall.md — The-Night-I-Met-Santa

## Current focus
**PHASE: S2 Threshold dial** (p6|7 full seamless spread) after **S1 Approach KEEP**.  
**S1 LOCKED/KEEP:** p4 `S01-approach/v13` + p5 `v14` — crack-is-the-story (narrow beam crawl + face-on wider spill).  
**S2 current:** `S02-threshold/v03` (2048×1024 Qwen spread) · `keep-leaning` · board `…/S02-threshold-comparison-spread-v03-2026-07-22.png`  
**SoT:** `Media/generated/mocks/_FLOW-CURRENT.json` · flipbook `Output/flipbook-2026-07-22.pdf`  
**Always-open 4:** Flow v2 · Master Dock · IMAGE-LANE-SYSTEM-v2 · AGENT-RUNBOOK  
**Logging:** RECIPE + `_FLOW-CURRENT` for tests; `project-log.md` only on lock / promote / phase complete.  
**Locks:** style-lock-v2 · santa-G0-v2 · boy G0 · S1 mockup-quality L/R targets.

## Birthday deadline
**2026-08-15** — Lulu hardcover gift for Jack Farrell. Order proof by **~July 25–28**.

## Last updated
2026-07-22 — Docs sync + Mem0/vault/Mnemosyne. S1 v13|v14 KEEP. S2 v03 dial pending Jon eye. IMAGE-LANE logging rule + AGENTS project-log gate.

## Where to continue
1. **Jon eye on S2 v03** — keep / lean / reject → update `_FLOW-CURRENT` → flipbook
2. Next Flow v2 beats (S3 locked art note; S4 Sit Here already has style/santa locks)
3. InDesign cold start when plates are keep/locked enough for PSD
4. P01 Title PSD path still queued after art dials settle

## Reference (new this session)
- **POEM-IMAGE-PROMPT-DOCK.md** — alternate poem↔page↔prompt dock (review)
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
| **POEM-IMAGE-PROMPT-DOCK** | Poem + pages + generation prompts (alt · review) |
| PAGE-PROMPT-BIBLE | Older beat prompts (prefer dock when generating) |
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
| Full dial books (2026-07-21) | `Media/generated/new-test-book-v1` · `v2` · `v3` (gitignored; maps inside) |
| Style-ref (Qwen peek) | `Media/approved/style-refs/pages/07-qwen-image-2.png` |
| InDesign Bridge plugin | `tools/layout-mcp/indesign-uxp-server/plugin/manifest.json` |
| **Photoshop working** | **`Xtraz/Adobe-Photoshop/`** (default agent save folder) |
| Photoshop UXP setup | `tools/layout-mcp/PHOTOSHOP-SETUP.md` |

## Decisions locked
- Format: **8.5×8.5"** · Printer: **Lulu** · Color: **sRGB** · **35–40 pages** (locked)
- Layout: **InDesign UXP** = production (`AGENT-RUNBOOK.md`); Pillow/Typst = **fallback only**; Affinity = optional polish
- Style: **Painted gouache** (not colored pencil)
- **Image lanes:** dial **Klein 9B** (default) → **Qwen** alt → Klein **4B** light only → **finals Gemini/Banana**
- **Image providers:** **fal.ai first** · **OpenRouter second** (Gemini / Klein 4B backup) — `IMAGE-LANE-PROMPTS.md`
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
- **Klein dial:** **9B** + **Dial D2** default; **4B** light only (`IMAGE-LANE-PROMPTS.md`)
- **Docs triggers:** `update docs` = workflow harvest · `log fixes` = ISSUES card (`PAGE-BUILD-WORKFLOW.md` §11)
- **Tony email (LOCKED):** **Tony** / **T** / **TNyse** / **bigtee** → **`bigtee@gmail.com`**
- **First PSD/INDD create (2026-07-20):** Jon **Save As** to final path → click dialogs → **ready** → agent edits (avoids modal hang + A4 Untitled mistake)
- **PS-first (2026-07-20):** dial MOCK in Photoshop then mirror live type in InDesign (same pt/spot)
- **Title defaults (P01):** Cinzel **36/42** + Cormorant author **18/24** · `#2C2C2C` · lower-center SAFETY · no Free Transform
- **PS text API @300ppi:** pass `pt×(300/72)` or batchPlay `pointsUnit` — verify Character panel
- **ID live type:** `page.textFrames.add` on Type layer — avoid orphan `create_text_frame`; check `overflows === false`
- **PS layer to JPG export (2026-07-20):** skill `Photoshop-Layer-Export` · `npm run ps:export-layers` · playbook in ISSUES-RESOLVED
- **Page build loop:** `.cursor/docs/PAGE-BUILD-WORKFLOW.md` · `Media/generated/mocks/{unit}/vNN/` + **RECIPE.md**
- **Print pixels:** page **2625²** · spread **5250×2625** = full **300 DPI** at Lulu bleed size (Pass B); dial may be lower
- **No fake gutter** on final spread art (MOCK-only fold OK)
- **DTP (2026-07-19 FINAL):** Affinity MCP `:6767` + InDesign UXP `:19300/:19301` **IN USE**. Cold flow: CC Desktop signed in (**Jon confirms**) → agent launches UDT+InDesign+bridge → **Jon clicks Load & Watch** (agent cannot) → MCP. Web adobe.com login not enough. Keep CC installed; Startup disable OK.
- **Photoshop MCP (2026-07-20 LIVE):** adobepy UXP broker `:47391` + dcc-mcp-photoshop `:8766/mcp` — **not** COM. Prefs: Enable Developer Mode only. Doc: `tools/layout-mcp/PHOTOSHOP-SETUP.md`. COM MCPs (loonghao/alisaitteke) rejected on this PC (`0x80080005`). **Default save folder:** `Xtraz/Adobe-Photoshop/`
- **Creative Cloud:** keep Desktop app installed (licensing); OK to disable Startup — do **not** uninstall while keeping InDesign/UDT

## Session note 2026-07-21 (late) — full-book dial tests v1–v3

- **v1** Klein 9B T2I → `new-test-book-v1` (32 interior + covers; TEXT-IMAGE-MAP)
- **v2** Qwen T2I → `new-test-book-v2` (spine-safe + camera/proof beats S07–S08)
- **v3** Qwen edit+T2I → `new-test-book-v3` (atmosphere `07-qwen-image-2` · boy/santa G0 refs · less photoreal)
- Scripts: `scripts/_scratch/_gen_new_test_book_v{1,2,3}.py` (resumable)
- **Not finals** — dial only. Jon reviewing tomorrow before Pass B / page builds.
- Known dial quirks: occasional baked letters on covers; S07 camera beat sometimes soft

## Session note 2026-07-21 — P01 title art lock (v22)

- **Locked (provisional):** `Media/approved/pages/p01-title.png` ← `mocks/P01-title/v22` (Jon corrected from v21)
- Layout: simpler fireplace+tree · scenery lower · open cream TOP · FRAME ON
- Alts not locked: v21 / v23 / v24
- Next: place into `p01-title.psd` · MOCK type in **upper** cream · then P02

## Session note 2026-07-20 — P01 title dial + fix log
- P01: `p01-title.psd` + `book-interior-v1.indd` — Jon confirmed live title visible after overset fix
- Logged cards: first-save · PS API 300ppi · MOCK↔ID parity · ID overset/orphan frame — see `ISSUES-RESOLVED.md`
- **PS-first** locked; title Cinzel 36 + Cormorant 18; skill `Photoshop-Layer-Export` + `npm run ps:export-layers`
- Pugicorn shelf refs affirm spread-first pacing (no map change)
- Tony Google OAuth guide emailed; aliases Tony/T/TNyse/bigtee → bigtee@gmail.com
- Next: continue sequential (P02) after Jon approves P01 composition / cloud
