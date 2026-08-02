# Lulu order checklist — TNIMS

**Goal:** One hardcover casewrap gift for Jack · birthday **2026-08-15**  
**Why Lulu first on interior:** Spine width depends on **page count + paper**. Lulu generates the **exact cover template** after the interior PDF is uploaded. Our wrap PSD used a **0.75″ spine placeholder**; for **hardcover 24–84 pp** Lulu’s table is **0.25″ spine** — confirm with their downloaded template.

## Current intent (2026-08-01) — SPECS ONLY · NOT FINAL SUBMIT

We are **not** locking the master / ordering the gift yet.

| Doing now | Not doing yet |
|-----------|----------------|
| Upload Interior PDF to get **page size, page count, binding options, cover template, spine** | Calling this the irrevocable “final” interior |
| Download cover template → rebuild wrap in PS/ID | Ordering proof or gift without Jon saying so |
| Keep project as a **draft** on Lulu | Hitting Review → purchase / publish as done |

Type/art polish can still land later. **Same page count (34)** → same spine → re-upload interior when truly ready. **No order/pay** until Jon explicitly says so.

**Files (current SoT)**

| Role | Path |
|------|------|
| Interior PDF | `Output/FINAL-Master-PDFs/TNIMS-Interior-FINAL.pdf` (**34 pp** · 8.75×8.75″) |
| Flipbook PDF (optional / not for Lulu) | `Output/FINAL-Master-PDFs/TNIMS-Flipbook-FINAL.pdf` |
| Cover wrap PSD (working) | `Xtraz/Adobe-Photoshop/FINAL-Master-PSDs/TNIMS-Cover-Wrap-FINAL.psd` |
| Cover INDD | `Xtraz/Adobe-inDesign/FINAL-Master-inDD/TNIMS-Cover-FINAL.indd` |
| Cover PDF (after rebuild) | `Output/FINAL-Master-PDFs/TNIMS-Cover-FINAL.pdf` (or `Output/covers/`) |
| Lulu template drop | `Xtraz/Lulu-Templates/from-lulu/` |
| Export presets | `Xtraz/Lulu-Templates/.../Lulu-Interior-Print-PDF.joboptions` · `Lulu-Cover-Print-PDF.joboptions` |

Check boxes as you go. Agent can help on any step — say the step number.

---

## Early upload OK? (page count locked)

**Yes.** If you will **not add/remove pages**, you can upload the current Interior PDF **now** to get Lulu’s cover template / specs — even if you still nudge type later.

| Change later | Re-upload interior? | New cover template? |
|--------------|---------------------|---------------------|
| Type position / wording / live text only | Yes (replace PDF) | **No** — same page count → same spine |
| Art swap same page count | Yes | **No** |
| Add or remove pages | Yes | **Yes** — spine/template changes |

Treat this book as **page-count final lock** once you upload for the template. Type polish can land in a later interior replace before ordering the gift.

---

## Lulu connect options (how we work together)

| Mode | When | How |
|------|------|-----|
| **A — Manual + agent (default)** | Anytime | You upload/download on lulu.com; drop template in `Xtraz/Lulu-Templates/from-lulu/`; agent rebuilds cover / fixes PDFs |
| **B — Browser assist (ready)** | Phase B–D | Agent drives Cursor browser / Playwright on Lulu; can use `LULU_*` from `.env.local` to sign in when you ask — **you confirm before order/pay** |
| **C — Lulu Print API** | Optional / future | Separate **API client id/secret** from [developers.lulu.com](https://developers.lulu.com/home) — **not** the website password. Needs public PDF URLs. Not set up yet |
| **No Lulu MCP** | — | Nothing in Cursor is a native Lulu MCP today |

### Credentials (local only — never commit)

Stored in **`.env.local`** (gitignored):

| Var | Use |
|-----|-----|
| `LULU_URL` | Site / create URL |
| `LULU_USERNAME` | Website login |
| `LULU_PASSWORD` | Website login |

Do **not** put these in Mem0, vault, git, or chat. Website password ≠ Print API keys.

**Browser assist rules**
1. Prefer you already logged in; agent may fill login from `.env.local` only when you explicitly ask.
2. Agent navigates create-project → upload Interior → download cover template → save into `from-lulu/`.
3. You confirm before any **order / pay** click.
4. Assist path: **Cursor browser** and/or **Playwright**; Pilot if connected. Stop with **stop browser**.
5. Interior file: `D:\Hermes\projects\The-Night-I-Met-Santa\Output\FINAL-Master-PDFs\TNIMS-Interior-FINAL.pdf`

**Say to start:** `start Phase B` · `lulu browser assist` · `upload interior now` · `sign me into Lulu`

---

## Phase A — Approve interiors (local)

- [ ] **A1.** Open `TNIMS-Interior-FINAL.pdf` page-by-page
- [ ] **A2.** Spot-check: **p2\|3** · **p4\|5** · **p12\|13** (S04) · **p30\|31** · **p32\|33** · pastedown ends
- [ ] **A3.** No gutter slivers · type readable · no white boxes
- [ ] **A4.** (Optional) Flipbook PDF — not for Lulu
- [ ] **A5.** Either **full approve** *or* **page-count lock** (type tweaks still OK) → proceed to Phase B

**Gate for B:** Page count locked (34) · PDF exists. Full art/type approve can finish before **gift** order, not before template download.

---

## Phase B — Create Lulu project + upload interior

- [x] **B1.** Create Lulu project: **Print Book** · goal **Print Your Book** · title **The Night I Met Santa** (draft `v82ejwq`)
- [x] **B2.** Page count = **34** · size **Square 8.5×8.5"**
- [x] **B3.** Uploaded `TNIMS-Interior-FINAL.pdf` (specs pass only — not final master)
- [x] **B4.** Ink coverage → selected **Premium Color** (ignore Standard)
- [x] **B5.** Cover template saved: `Xtraz/Lulu-Templates/v82ejwq-cover-template.pdf` (+ copy in `from-lulu/`)
- [x] **B6.** Spine from Lulu UI: **0.25 in / 6.35 mm** · cover **19 × 10.25 in** — see `from-lulu/SPECS-LOCKED-2026-08-01.md`
- [x] **B7.** Specs: **Premium Color** · **80# White Coated** · **Hardcover Case Wrap** · **Matte** · ~**$18.28** print

**Gate:** Template on disk → Phase C when Jon is ready. **No order.**

---

## Phase C — Rebuild cover to Lulu spine (TEST started)

- [x] **C0.** Specs + template locked (B complete)
- [x] **C1.** Spine **0.25″** · canvas **19 × 10.25″** @ 300 = **5700 × 3075**
- [x] **C2.** **TEST** remap wrap art → `Xtraz/Lulu-Templates/from-lulu/phase-c-test/`
- [ ] **C3.** Jon eye-check TEST (wrap flaps · title · faces · spine strip)
- [ ] **C4.** Rebuild master Cover PSD / Place art at Lulu size (not old 5475×2625)
- [ ] **C5.** Relink Cover INDD · live type · **no spine text**
- [ ] **C6.** Export Cover PDF sRGB — only when Jon says upload-ready

**Test outputs:** `cover-wrap-LULU-19x10.25-TEST.png` (+ `-guides` · `-lulu-guides`)

---

## Phase D — Upload cover + order proof

- [ ] **D1.** Upload Cover PDF to same Lulu project
- [ ] **D2.** Check Lulu cover preview
- [ ] **D3.** **Order ONE proof** (not gift yet) — confirm with Jon before pay
- [ ] **D4.** Note ETA vs **2026-08-15**

**Gate:** Physical proof arrives.

---

## Phase E — Proof → gift order

- [ ] **E1.** Physical check (color · bleed · S04 · cover · type)
- [ ] **E2.** Fixes → re-export → re-upload (same page count = no new template)
- [ ] **E3.** Order gift with shipping buffer before **2026-08-15**
- [ ] **E4.** (Optional) Graduate PDFs → `Media/finals/` + ReCall note

---

## What you do *not* need

| Skip | Why |
|------|-----|
| Upload Flipbook to Lulu | Digital preview only |
| Custom endsheets | Lulu white endsheets automatic |
| Spine type | Under 80 pages |
| Waiting for “perfect type” before first upload | Page count locked → template OK now |
| Lulu API keys for this gift | Optional; website + browser assist enough |
| S04 isolate merge | Spine-meet already in Interior |

---

## Best process (one sentence)

**Lock page count → upload Interior (even if type still polishing) → download Lulu cover template → rebuild cover → replace interior if type fixes land → upload cover → proof → gift.**
