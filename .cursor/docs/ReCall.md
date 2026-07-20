# ReCall.md — The-Night-I-Met-Santa

## Current focus
**InDesign = production** (runbook authority). Pillow/Typst = fallback only.  
**Page count locked: 35–40.**  
**Spread build loop locked:** PS MOCK + chops (`Images/chopz/`) → InDesign match → live Cormorant.  
Working `.indd`: `Xtraz/Adobe-inDesign/eyes-met-prototype-v1.indd`  
Pages **4–5** = eyes-met MOCK-matched stack; pages **2–3** = earlier comparison prototype.

**DTP:** Affinity MCP + InDesign UXP Bridge + **Photoshop adobepy UXP LIVE** (`:47391` / `:8766`). Cold flow: CC Desktop signed in (Jon confirms) → agent UDT+apps+bridges → **Jon Load & Watch** → MCP.

**PSD blanks locked:** `Xtraz/Adobe-Photoshop/` → `spread-page-template.psd` · `single-page-template.psd` · `book-covers-template.psd` (no spine-only PSD).

## Birthday deadline
**2026-08-15** — Lulu hardcover gift for Jack Farrell. Order proof by **~July 25–28**.

## Last updated
2026-07-20 **night** — PSD blanks (spread/single/cover) + Photoshop MCP LIVE; docs/Mem0/vault/Mnemosyne sync. **Tomorrow:** one-page design → InDesign · poem storyboard imagery · PS solo-layer / chop export tests.

## Where to continue (tomorrow)
1. **One-page design** from `single-page-template.psd` → place into InDesign (live Cormorant)
2. Start **storyboard imagery** that matches poem beats (real scenes, not dial-only mocks)
3. **Photoshop MCP tests:** solo layers + export chops to `Images/chopz/` for agent/Jon loop
4. Hide/delete MOCK-REF when pages 4–5 approved
5. Optional: Lulu `.joboptions` + smoke PDF → `Output/interiors/`
6. **S01 Approach LEFT** Lane A when ready for next story beat

## Reference (new this session)
- **Photoshop UXP MCP:** `tools/layout-mcp/PHOTOSHOP-SETUP.md` — LIVE; COM MCPs skip
- **Adobe CC MCP watchlist:** `.cursor/docs/ADOBE-CC-MCP-GUIDE.md`
- **ArcRift:** fleet `TOOLS-WATCHLIST` — C (74) WATCH record; do not install (Mem0/Mnemosyne primary)

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
- **Print pixels:** page **2625²** · spread **5250×2625** = full **300 DPI** at Lulu bleed size (Pass B); dial may be lower
- **No fake gutter** on final spread art (MOCK-only fold OK)
- **DTP (2026-07-19 FINAL):** Affinity MCP `:6767` + InDesign UXP `:19300/:19301` **IN USE**. Cold flow: CC Desktop signed in (**Jon confirms**) → agent launches UDT+InDesign+bridge → **Jon clicks Load & Watch** (agent cannot) → MCP. Web adobe.com login not enough. Keep CC installed; Startup disable OK.
- **Photoshop MCP (2026-07-20 LIVE):** adobepy UXP broker `:47391` + dcc-mcp-photoshop `:8766/mcp` — **not** COM. Prefs: Enable Developer Mode only. Doc: `tools/layout-mcp/PHOTOSHOP-SETUP.md`. COM MCPs (loonghao/alisaitteke) rejected on this PC (`0x80080005`). **Default save folder:** `Xtraz/Adobe-Photoshop/`
- **Creative Cloud:** keep Desktop app installed (licensing); OK to disable Startup — do **not** uninstall while keeping InDesign/UDT
