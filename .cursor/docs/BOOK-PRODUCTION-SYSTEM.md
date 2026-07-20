# BOOK PRODUCTION SYSTEM — Hermes Picture-Book Playbook

**Status:** Living system doc · last updated **2026-07-15**  
**Purpose:** Dialed-in workflow to finish *The Night I Met Santa* **and** recreate the same system for **future picture books**.  
**Owner:** Jon · Agent continue file: `CONTINUE-HERE.md`

> When this file conflicts with session chat, **this + `TRUTH.md` win**. Update this doc when a decision sticks.  
> **Jon rule:** On **`update docs`**, agents must review the session and fold anything worth keeping into this playbook (decision log, tool path, folder locations, quality gates) — not only the usual TRUTH/ReCall sync.
---

## 0) Quick start (new book vs this book)

### Reuse for a **new** book (checklist)

1. Clone / copy this project skeleton (Hermes sibling) **or** open a fresh folder and pull shared `_core-scripts` fleet docs/skills.
2. Replace: poem/transcript · author · trim if needed · deadline.
3. Copy/adapt folders: `Media/`, `Images/references/`, `Transcription/`, `Pages/`, `Output/`.
4. Lock a **new** style north star → write `ILLUSTRATION-STYLE.md` (or retarget this one’s template).
5. Write `PAGE-PROMPT-BIBLE.md` from the new poem beats.
6. Run image pipeline (§3) → approve batch → promote to `Media/`.
7. Composite poem pages → Typst (or img2pdf) → Lulu cover wrap → proof.

### This book (*The Night I Met Santa*)

| Field | Value |
|-------|--------|
| Gift for | Jack Farrell |
| Birthday | **2026-08-15** (proof ~July 25–28) |
| Poem | `Transcription/poem-clean.txt` |
| Trim | **8.5 × 8.5"** Lulu casewrap HC |
| Pages | **32** even (no blanks) |
| Style locked | Painted **gouache** — not colored pencil |
| Keepers | `Media/generated/test-batch-v2/` · covers `Media/generated/test-covers-v3/` · **approved → `Media/approved/`** (two-tier) |
| Future-book master | Repo-root **`BOOK-PLAYBOOK.md`** (pair with this living ops doc) |
| Fonts | `.cursor/docs/FONT-CATALOG.md` · pack in `Xtraz/Fonts/` (gitignored; installed on PC) |

### Media/approved two-tier (Jon 2026-07-15)

| Tier | Path | Use |
|------|------|-----|
| **A moodboard** | `Media/approved/style-refs/{covers,back,jack,pages,santa,spread,story}/` | Favorites / shot ideas — **keep this org** |
| **B print locks** | `characters/` · `covers/` · `pages/` · `spreads/` | Clean kebab names for compositor/Typst |

Only Tier B is “locked for print.” See `Media/approved/INDEX.md`.

**Important (2026-07-15):** Tier B today = **composition approval**, often dial/~1K size — **not** Lulu pixel-final.  
Print remakes + boy/Santa continuity plan → **`.cursor/docs/CONTINUITY-AND-PRINT-FINALS.md`**.  
Final plates land in **`Media/approved/print/`** after Pass B. Each Tier B file should get a **`.recipe.md`** sidecar (see `covers/cover-front.recipe.md`).

---

## 1) Locked product decisions (this book + defaults for next)

| Decision | Choice | Rationale / where |
|----------|--------|-------------------|
| Printer | **Lulu** primary | Square HC; single copy OK — `RESEARCH-VERDICT.md` |
| Not KDP for this trim | Skip square HC path | Same |
| Soft proof first | Paperback optional | Cheaper before gift HC |
| Page count | **35–40** (locked 2026-07-19) | Front matter breathing room + 15-stanza pacing; earlier ~32 retired |
| Spreads | Emotional doubles as needed | Big beats meet at fold; no extra gutter under 60 pp |
| Layout engine | **InDesign UXP** (production) | Specs: `AGENT-RUNBOOK.md` + `INDESIGN-PRODUCTION-WORKFLOW.md` |
| Layout fallback | Pillow pre-compose → Typst | Emergency / offline only — **not** gift default |
| Rejected layouts | v3 white boxes · v4 checkerboard · v5 soft rect “boxes” | `Book-Findings.md` |
| Text on interiors | **After** art approve | Cloud/watercolor wash under type — not hard white boxes |
| Cover type in AI | Prefer festive gold flourish title | Or art-only + `build_cover_v2.py` if spelling breaks |
| About / Thank You | **Draft A locked** | `BOOK-COPY-DRAFTS.md` |
| Art medium | **Painted gouache / soft watercolor** | `ILLUSTRATION-STYLE.md` |
| Art size page | **2625 × 2625** @ 300 DPI | 8.75" with 0.125" bleed |
| Art size spread | **5250 × 2625** master → split L/R | Continuous scene across gutter |
| PS blanks | `Xtraz/Adobe-Photoshop/{spread,single-page,book-covers}-template.psd` | Cyan=TRIM · magenta=SAFETY · orange=MOCK · **no** spine PSD (Lulu wrap) |
| Poem typeface (preferred) | **Cormorant Garamond Medium** · **20/26** · tracking **+5** · centered · #2C2C2C | Locked Jon 2026-07-20 — `FONT-CATALOG.md` · `AGENT-RUNBOOK.md` §5 |
| Cover display type | **Cinzel Decorative** (alt Mountains of Christmas) | Same |
| Lulu color | **sRGB** export for full-color interior | Lulu printers use sRGB (2026 help) |
| Lulu paper | **Premium Color** / heavier stock | Heirloom gift feel |
| Safety | ≥ **0.5"** from trim (faces/text) | Lulu full-bleed recommendation |

---

## 2) Tool stack (what we actually use)

### Image generation — **locked lanes** (Jon 2026-07-15; dual prompts 2026-07-15 night)

| Priority | Lane | Endpoint | ~Cost | Style prompt | When |
|:--------:|------|----------|------:|--------------|------|
| 1 | **Dial / mockups** | Klein 4B — fal `flux-2/klein/4b` **or** OpenRouter `flux.2-klein-4b` | ~$0.01–0.015 | **Klein D2 append** (`IMAGE-LANE-PROMPTS.md`) | Layout, vibe, cheap probes |
| 2 | **Fallback** | `fal-ai/qwen-image-2/text-to-image` | ~$0.035 | Short master OK | Klein misses vibe |
| 3 | **Finals** | fal `nano-banana-pro/edit` **or** OpenRouter `google/gemini-3-pro-image` | ~$0.14–0.15 | **ILLUSTRATION-STYLE master** (Gemini/Banana) | Approved pages / covers / print |

**Dual-lane rule:** Klein = mockup prompt only. Gemini/Banana = original master only. Do not cross-contaminate.  
**Klein visual proof:** `Media/approved/style-refs/covers/klein-mockup-style-LOCKED-D2.png`  
**Detail:** `.cursor/docs/IMAGE-LANE-PROMPTS.md`

| Piece | Exact choice |
|-------|----------------|
| Provider | **fal.ai** (`FAL_API_KEY` / `FAL_KEY` in `.env.local`) |
| Finals model | **`fal-ai/nano-banana-pro/edit`** |
| Why edit | Style/character lock via `image_urls` refs |
| Resolution (finals) | **`2K`** (upscale later if needed) |
| Aspect | Pages/covers **`1:1`**; spreads wide then split |
| How we call it | Cursor MCP **`user-fal-ai`** → `run_model` / `check_job` / `get_job_result` |
| Upload refs | `fal_client.upload_file(path)` (Python) or MCP `upload_file` |
| Download | PowerShell `Invoke-WebRequest` → `Media/generated/<batch>/` |
| Auth | Never commit keys; sync MCP via JonBeatz `npm run sync:mcp-env` when needed |

**Style ref recipe (finals — repeatable):**

1. Approve 2–3 hero frames → save as `_style-refs/style-*.png`
2. Upload once per batch → keep URLs in `_style-refs/fal-urls.json`
3. Every finals image: pass those URLs in `image_urls` + scene prompt + master style block
4. Covers: also pass **title treatment ref** (e.g. `Images/references/cover/candidate-santa-D-best-title.png`)

### Image generation (legacy / last-resort — not the locked lanes)

| Tool | Role |
|------|------|
| `npm run image:fal*` → default **`fal-ai/flux/schnell`** | Ultra-cheap scratch only (prefer Klein 4B for dial) |
| `npm run image:gen` (HF) | Zero VRAM drafts |
| ComfyUI | Only if operator asks — faces / upscale / inpaint |

### Layout & PDF

| Tool | Role |
|------|------|
| `composite_pages.py` | Illustration + organic cloud wash + poem text → `Pages/*.jpg` |
| `book-final.typ` | Front matter + place composited pages |
| `build_cover_v2.py` | Casewrap cover PDF when AI type fails |
| `img2pdf` + `pikepdf` | Optional page→PDF / prepress (IN USE) |
| `npm run book:composite` / `book:typst` / `book:pdf:*` | Repo scripts |

### Session / Hermes fleet (supporting)

| Tool | Role |
|------|------|
| Open / Start / End Project rituals | Session health — don’t cold-boot unpaid stack on Open |
| Mem0 (`the-night-i-met-santa`) | Project memory |
| Draven Mem0 | Cross-project assistant memory |
| Vader Vault | Durable human-readable hub note |

---

## 3) Image workflow — step by step (recreate forever)

```
[1] Poem beats → PAGE-PROMPT-BIBLE
[2] Lock ILLUSTRATION-STYLE (+ negatives: NOT colored pencil)
[3] Seed style refs (2–3 approved painted frames)
[4] Batch folders under Media/generated/
      test-batch-vN/     story + spreads
      test-covers-vN/    front+back cover sets
[5] fal nano-banana-pro/edit @ 2K + image_urls
[6] Jon reviews → INDEX.md notes
[6b] **Copy winners → Media/approved/** (characters|style-refs|covers|pages|spreads) + update Media/approved/INDEX.md
[7] Promote keepers → Media/ (final names) *or* treat approved/ as print source
[8] Quiet-zone map per page
[9] Pillow composite poem text
[10] Typst / PDF → Lulu
```

**Approved folder (2026-07-15):** `Media/approved/` is the **human-facing “what Jon picked” shelf**. Batches stay in `Media/generated/`. Git tracks `approved/` (not `generated/`).

### Prompt anatomy

```
[SCENE: who/what/where/light/composition]
[QUIET ZONE: leave soft area for later text — interiors]
[STYLE: master block from ILLUSTRATION-STYLE.md]
[REFS: image_urls = style (+ title ref for covers)]
[NEGATIVES: colored pencil, photoreal, mockup book, gibberish type…]
```

### Cover-specific (front)

- Flat **poster** only — never 3D book mockup
- Title exactly: book title  
- Credit exactly: `Written By <Author>` (this book: Jack Farrell)
- Prefer ornate **gold display serif** + flourishes + star sparkles (title-ref image)

### Cover-specific (back)

- Matching mood/palette companion scene
- **No** baked blurb text preferred — leave large soft empty region (snow, cream wall, sky) for ISBN/blurb later

### Spreads

- One continuous scene → save WIDE + optional `5250x2625` + LEFT + RIGHT halves
- Critical beats only (this book: eyes met, sit here, note, closing, chat/laugh)

---

## 4) Folder contract (keep for every book)

| Path | Role |
|------|------|
| `Transcription/` | Clean poem / source text |
| `Media/` | **Final** promoted illustrations |
| `Media/generated/` | Experimental batches (git-large — manage carefully) |
| `Images/references/style/` or `_style-refs/` | Style north stars |
| `Images/references/cover/` | Cover / title treatment refs |
| `Images/references/layout/` | How text should sit on art |
| `Pages/` | Pre-composited print pages |
| `Output/` | Interior + cover PDFs |
| `.cursor/docs/` | Plans, prompts, this playbook |
| `_archive/` | Rejected experiments — do not auto-revive |

**Rule:** Working art lives at **project root** (`Media/`), never `.cursor/assets/`.

---

## 5) Doc map (system of record)

| Doc | Job |
|-----|-----|
| **`BOOK-PRODUCTION-SYSTEM.md`** (this file) | Reusable playbook + tool/decision lock |
| `TRUTH.md` | Project constitution |
| `CONTINUE-HERE.md` | Next actions this session |
| `ILLUSTRATION-STYLE.md` | Aesthetic default + master prompts |
| **`TEXT-OVERLAY-POLICY.md`** | **How poem/matter type sits on art** (open zones · white paint · large serif) |
| `PAGE-PROMPT-BIBLE.md` | Beat → fal prompt |
| `COVER-PROMPTS.md` | Cover dial-in |
| `BOOK-COPY-DRAFTS.md` | Locked About / Thank You / dedication |
| `BOOK-PLAN.md` | Specs + stanza map |
| `RESEARCH-VERDICT.md` | POD / GitHub / toolchain research |
| `Book-Findings.md` | Failed layout iterations (lessons) |
| `IMAGE-WORKFLOW.md` | Fleet image cmds (HF / fal / Comfy) |
| Batch `INDEX.md` files | What each generated folder contains |

---

## 6) Decision log (append-only)

| Date | Decision | Notes |
|------|----------|-------|
| 2026-07-14 | Lulu 8.5×8.5 HC; 32 pages; 4–5 spreads | G2 |
| 2026-07-14 | Pillow cloud text; reject v3–v5 | Layout north star photos |
| 2026-07-14 | About + Thank You **Draft A** locked | Copy |
| 2026-07-14 | Aesthetic = **painted gouache**, not colored pencil | Style |
| 2026-07-14 | Image winners via **fal Nano Banana Pro /edit** + style refs | Pipeline |
| 2026-07-14 | Style north stars = eyes-met **06** + sneak **02** | `test-batch-v2` |
| 2026-07-14 | Cover title treatment from candidate-santa-D | Gold flourish |
| 2026-07-14 | Full story batch `test-batch-v2` approved vibe | Story art |
| 2026-07-14 | Cover sets A–E in `test-covers-v3` (spectacular) | Covers pending pick |
| 2026-07-14 | Prepress libs **img2pdf** + **pikepdf** IN USE | PDF |
| 2026-07-14 | Full 32-page map + gen script `generate_test_batch_v3.py` | `Media/generated/test-batch-v3/` |
| 2026-07-14 | Text wash A/B/C/D/E mock script `mock_text_washes_v3.py` | Prefer **ellipse-cloud (B)** over soft rect |
| 2026-07-15 | fal wallet exhausted mid v3 — top up before finishing p31–p32 | Billing gate |
| 2026-07-14 | **Text overlay direction:** open zones + white paint / bleed / mist; reject gray blobs + soft rect. Mocks `text-mocks-v2/` = **closer, not perfect** — refine before shipping compositor | `TEXT-OVERLAY-POLICY.md` |
| 2026-07-15 | Jon mockups locked as refs: soft paint fades, **never cover faces**, Santa pages use **bottom-right** gradient; note pages **lower** not mid-window. Mocks → `text-mocks-v3/` | layout `ref-text-jon-*` |
| 2026-07-15 | Text wash dial: overpowered solid glow rejected — use **subtle mid-opacity** paper + long fade (Pillow; not a fal model issue). Cheap art dial = Flux schnell / Klein; finals stay Nano Banana Pro | compositing |
| 2026-07-15 | **Lane lock:** dial = **FLUX.2 [klein] 4B** (~$0.009/MP); **fallback** = **Qwen Image 2** (~$0.035/img); finals = **Nano Banana Pro /edit + refs** (~$0.15/img). Ideogram skipped (safety). Docs sync + vault pattern updated | Model lanes |
| 2026-07-15 | Harvested `book/Childrens_Book_Design_Summary*` → Lulu checklist §8b; **corrected color advice** to **sRGB** (not CMYK-first) per Lulu help | Prepress |
| 2026-07-15 | Flipbook webpage notes → `DIGITAL-FLIPBOOK-WATCH.md` (post-gift only; do not block print) | Optional digital |
| 2026-07-15 | **Jack Farrell portrait LOCKED** = `v6d-armchair-tree-lights` → `Media/approved/characters/jack-farrell-portrait.png`; remake kit `CHARACTER-JACK-FARRELL.md`; book use About Author / Thank You | Character |
| 2026-07-15 | Created **`Media/approved/`** shelf for Jon-selected finals (git-tracked); batches stay in `generated/` | Asset org |
| 2026-07-15 | **Cover LOCKED** beige-v2 (oatmeal holly PJs; Santa face hidden). Mid-blue runner-up only. | Cover |
| 2026-07-15 | Dual image lanes + prompts: Klein **D2** mockups vs Gemini/Banana **ILLUSTRATION-STYLE** master — `IMAGE-LANE-PROMPTS.md` | Prompts |
| 2026-07-15 | Cast unify: Boy G0 ← style-match-A; Santa G0 = paint north star; Jack portrait ← style-match-B; eyes-met = FINAL-TEST-A | Characters |
| 2026-07-15 | Klein **full-book** mocks (`test-book-v1`/`v2`) **rejected** (cover-bleed / not usable). **Page-by-page** Gemini finals only going forward | Process |
| 2026-07-15 | Spread-first story map proposed: 12 spreads + 8 matter = 32 — `SPREAD-STORY-MAP.md` | Pagination |
| 2026-07-15 | Edition credits locked (Jack author · Jon design) — `BOOK-COPY-DRAFTS.md` | Copy |
| 2026-07-19 | **DTP MCP LIVE + cold-start FINAL:** Affinity `:6767` + InDesign UXP `:19300/:19301`. Workflow: CC Desktop signed in (**Jon confirms**) → agent UDT+InDesign+bridge → **Jon Load & Watch** (agent cannot click Electron) → MCP smoke PASS. Web login not enough. Keep CC installed; Startup disable OK. Setup: `tools/layout-mcp/SETUP.md` | Layout automation |
| 2026-07-19 | **Production path flip:** InDesign UXP = gift print path; Pillow/Typst = fallback only. Page count locked **35–40**. `AGENT-RUNBOOK.md` authoritative for build. TRUTH/CONTINUE/AGENTS aligned. | Layout / governance |
| 2026-07-20 | **Spread build loop locked:** Jon PS MOCK (5250×2625) + chops in `Images/chopz/` → agent matches in InDesign → **live Cormorant** (no raster poem). MOCK @ ~35% for align then hide. Prefer **PNG** links. Details: `ISSUES-RESOLVED.md` + `AGENT-RUNBOOK.md` | Layout / process |
| 2026-07-20 | **No fake gutter on finals:** seamless spread art only. Optional center fold line OK on screen MOCKS; never bake into LEFT/RIGHT/SPREAD print plates. | Art / print |
| 2026-07-20 | **Print DPI confirmed:** finals must be exact **2625×2625** (page) / **5250×2625** (spread) = full **300 DPI** at Lulu bleed size. Pass A dial may be ~1K; Pass B remake before Lulu plates. | Print / resolution |
| 2026-07-20 | **Photoshop MCP LIVE (UXP):** COM rejected (`0x80080005`). Stack = adobepy broker `:47391` + dcc-mcp-photoshop `:8766` + UDT plugin `com.adobepy.bridge.photoshop`. Developer Mode only. Smoke PASS. `PHOTOSHOP-SETUP.md`. InDesign remains print authority. | DTP / automation |
| 2026-07-20 | **`spread-page-template.psd` locked:** 5250×2625 @ 300 RGB. Guides: cyan TRIM / magenta SAFETY / orange FOLD (MOCK only). Layers: white-bg → paper-base → ART → trim/safety → fold → cloud → type zones. Use: Duplicate→Save As; paint ART; hide fold for finals; Cormorant stays live in InDesign. Docs: `ISSUES-RESOLVED.md` · `PHOTOSHOP-SETUP.md` · `AGENT-RUNBOOK.md`. | Layout / PS |
| 2026-07-20 | **Also locked:** `single-page-template.psd` (2625²) + `book-covers-template.psd` (2625² front/back). **No** `book-spine-template.psd` — spine width from Lulu casewrap after interior upload. | Layout / PS |

*(Add a row whenever something sticks.)*

---

## 7) npm / agent command cheat sheet

```powershell
# From this project root
npm run image:doctor
npm run image:fal:page -- "<scene>. <MASTER STYLE>"   # override model for Nano Banana when scripting
npm run image:fal:spread -- "..."
npm run image:fal:cover -- "..."
npm run book:composite
npm run book:typst
npm run book:pdf:doctor
npm run book:pdf:from-pages
npm run book:pdf:verify
```

**Agent reality (2026-07-15):** Dial on **Klein 4B**, escalate to **Qwen Image 2** if needed, lock pages with **MCP `user-fal-ai` + `nano-banana-pro/edit` + refs**. Do not default to Flux schnell for dial.

### MCP generate template

```
endpoint_id: fal-ai/nano-banana-pro/edit
input:
  prompt: <scene + style + title if cover>
  image_urls: [<style...>, <title-ref optional>]
  resolution: "2K"
  aspect_ratio: "1:1"   # or auto / wide for spreads
  output_format: "png"
  num_images: 1
  limit_generations: true
```

---

## 8) Quality gates (ship checklist)

### Art

- [ ] Matches painted gouache north stars (not pencil/photoreal)
- [ ] Character wardrobe consistent enough across book
- [ ] Quiet zones exist where poem/About/Thank You go
- [ ] Spreads continuous across gutter
- [ ] Covers flat; title spelling verified (or rebuild type in Python)

### Print

- [ ] Even page count
- [ ] 300 DPI · 0.125" bleed · safety ≥ 0.5" from trim for faces/text
- [ ] Gutter: no critical faces on absolute center fold (32-page book needs no *extra* gutter margin)
- [ ] Interior PDF = single multi-page file; **odd pages = right**; no cover pages inside
- [ ] Cover = separate wrap PDF from **Lulu template** after real page count + paper known
- [ ] Color: **sRGB** for Lulu full color (review Lulu’s print-ready preview after upload)
- [ ] Flatten / no live transparency stacks in final pages (we already flatten via Pillow JPEG)
- [ ] Soft proof → then gift hardcover (**Premium Color**)

### Handoff

- [ ] Winners promoted out of `generated/` into `Media/`
- [ ] This playbook decision log updated
- [ ] Vault / Draven note for next session

---

## 8b) Lulu upload checklist (from design-summary notes + help center)

Absorbed from `.cursor/docs/book/Childrens_Book_Design_Summary*.md` and verified against [Lulu Interior Formatting](https://help.lulu.com/en/support/solutions/articles/64000255590-interior-formatting-the-basics) (modified 2026-06-08):

1. Download Lulu **cover template** only after interior page count + paper/ink are fixed (spine width depends on both).
2. Upload **interior** PDF first → review **print-ready** file Lulu generates (best color/proof check before pay).
3. Upload **cover** separately (front | spine | back).
4. Confirm trim is recognized as **8.5×8.5** (file size with bleed = **8.75×8.75** per page).
5. Order **one physical proof** before any multi-copy run.
6. Prefer **Premium Color**; blank trailing pages from POD machines are normal / not charged.

**Design spreads in software as doubles**, export to Lulu as **single pages in order** (not as one wide spread PDF unless the platform asks for it).

---

## 9) Future books — change only these

| Swap | Keep |
|------|------|
| Poem / beats | Folder layout + 2625 math (if same trim) |
| Style refs + ILLUSTRATION-STYLE | **Image lanes:** dial Klein 4B → fallback Qwen Image 2 → finals Banana `/edit` + refs |
| Cover title string + author | Cover flat-poster rules |
| About / Thank You copy | Pillow → Typst → Lulu path |
| Character sheets | Rejection list (no white boxes / no mockups; Ideogram skipped for child Christmas if safety blocks) |

### Future-book model recipe (copy this)

1. **Lock style** first (2–3 north-star frames).
2. **Dial** scenes on **`fal-ai/flux-2/klein/4b`** (~$0.01/sq) — layout + vibe only.
3. If Klein misses: **one** shot on **`fal-ai/qwen-image-2/text-to-image`** (~$0.035) before burning finals budget.
4. **Promote keepers** with **`fal-ai/nano-banana-pro/edit`** @ 2K + `image_urls` style refs (~$0.15).
5. Skip Ideogram for pajamas / child Christmas beats unless a non-child scene needs typography-in-image.
6. Prove a lane with a **real beat prompt** (same seed/prompt folder) before locking — see `Media/generated/model-compare-beat01/` as the template.

---

## 10) Instance status snapshot (refresh on Continue)

**Project:** The Night I Met Santa  
**Done:** Style lock · story batch v2 · covers v3 (5 sets) · copy A locked · print size docs · **image lanes locked** (Klein → Qwen → Banana) · Beat 1 model compare · text-overlay policy + mocks v3  
**Next:** Pick cover set → promote art → golden text page → rewrite cloud wash in `composite_pages.py` → sample page → full Pages → PDF → Lulu proof  

Detail: **`CONTINUE-HERE.md`**
