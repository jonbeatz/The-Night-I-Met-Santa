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
| Keepers | `Media/generated/test-batch-v2/` · covers `Media/generated/test-covers-v3/` |

---

## 1) Locked product decisions (this book + defaults for next)

| Decision | Choice | Rationale / where |
|----------|--------|-------------------|
| Printer | **Lulu** primary | Square HC; single copy OK — `RESEARCH-VERDICT.md` |
| Not KDP for this trim | Skip square HC path | Same |
| Soft proof first | Paperback optional | Cheaper before gift HC |
| Page count | **32** | Even; industry sweet spot; Lulu HC min 24 |
| Spreads | **4–5** cinematic doubles | Big emotional beats meet at gutter |
| Layout engine | **Pillow pre-compose** → Typst binder | Reject Typst PNG alpha stacks |
| Rejected layouts | v3 white boxes · v4 checkerboard · v5 soft rect “boxes” | `Book-Findings.md` |
| Text on interiors | **After** art approve | Cloud/watercolor wash under type — not hard white boxes |
| Cover type in AI | Prefer festive gold flourish title | Or art-only + `build_cover_v2.py` if spelling breaks |
| About / Thank You | **Draft A locked** | `BOOK-COPY-DRAFTS.md` |
| Art medium | **Painted gouache / soft watercolor** | `ILLUSTRATION-STYLE.md` |
| Art size page | **2625 × 2625** @ 300 DPI | 8.75" with 0.125" bleed |
| Art size spread | **5250 × 2625** master → split L/R | Continuous scene across gutter |

---

## 2) Tool stack (what we actually use)

### Image generation — **locked lanes** (Jon 2026-07-15)

| Priority | Lane | Endpoint | ~Cost | When |
|:--------:|------|----------|------:|------|
| 1 | **Dial / dev** | `fal-ai/flux-2/klein/4b` | ~$0.009/MP (~$0.01 @ square_hd) | Layout, vibe, text-zone probes — default iterate |
| 2 | **Fallback** | `fal-ai/qwen-image-2/text-to-image` | ~$0.035/image | Klein misses the vibe; 2nd option before spending Banana |
| 3 | **Finals** | `fal-ai/nano-banana-pro/edit` + style refs | ~$0.15/image | Approved pages / covers after dial |

**Skipped:** Ideogram V3/V4 (safety friction on Christmas child storybook beats).  
**Evidence:** `Media/generated/model-compare-beat01/` (Beat 1 sneak; Jon picks `02` dial, `07` fallback, `05` finals).

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
[7] Promote keepers → Media/ (final names)
[8] Quiet-zone map per page
[9] Pillow composite poem text
[10] Typst / PDF → Lulu
```

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
| 2026-07-15 | Full `update docs` harvest: playbook §9 future-book recipe, Book-Findings §10, ReCall/CONTINUE, Hermes-Picture-Book-Production vault pattern | Docs ritual |

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
- [ ] 300 DPI · bleed · safety margins
- [ ] Interior PDF + cover wrap separate
- [ ] Soft proof → then gift hardcover

### Handoff

- [ ] Winners promoted out of `generated/` into `Media/`
- [ ] This playbook decision log updated
- [ ] Vault / Draven note for next session

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
