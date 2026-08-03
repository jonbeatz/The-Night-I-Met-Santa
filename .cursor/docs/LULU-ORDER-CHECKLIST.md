# Lulu order checklist — TNIMS

**Status 2026-08-03:** **ORDERS PLACED** — full website playbook → **`.cursor/docs/LULU-WEBSITE-ORDER-PLAYBOOK.md`**  
**Orders:** Jack **USD-C4242921** · Jon **USD-C4242970**

**Goal (original):** Hardcover casewrap gift for Jack · birthday **2026-08-15** (+ softcover copies + Jon keep set).  
**Why Lulu first on interior:** Spine width depends on **page count + paper**. Lulu generates the **exact cover template** after the interior PDF is uploaded.

## Cover workflow — best plan (TNIMS + future Hermes books)

**Development:** You do **not** need Lulu’s exact template on day one. Keep a **ballpark** end goal (trim size, hardcover vs paperback, rough page range) and design/generate at that print res. Exact spine width can wait.

**Before final cover PDF / order:** Download Lulu’s template (after interior upload) and align the wrap to **exact** px — that’s a late lock, not a start gate.

| Phase | Do this | Why |
|-------|---------|-----|
| Early | Ballpark trim + binding; build art at high print res (pages **2625²** · spreads **5250×2625**; cover panels ~square bleed size) | Creative progress without page-count stress |
| When page count is stable enough | Upload interior draft → grab template | Unlocks exact spine / wrap |
| Late | Fit wrap to template (**HC: 5700×3075 · 0.25″ spine** · **SC: 17.387×8.75″ · 0.137″ spine**) | Delivery geometry |
| Spine type | Skip on thin spines (≤~0.25″) | Usually illegible |
| Photoshop | Smart Objects for art/logo/QR; keep layer styles on SO replace | Non-destructive resize |
| Recipes | Highest useful print res for keepers | Downscale OK; tiny dials ≠ masters |

**Spine text policy (gift hardcover, short book):** Prefer **no spine text** — color/art strip only.

**Cover edge preflight:** Zoom all four edges with guides off; keep `02-LULU-GUIDES` on **top**. Full gotchas: `tools/layout-mcp/PHOTOSHOP-SETUP.md`.

---

## Files (SoT)

| Role | Path |
|------|------|
| Interior PDF | `Output/FINAL-Master-PDFs/TNIMS-Interior-FINAL.pdf` (**34 pp**) |
| Hardcover cover | `Output/FINAL-Master-PDFs/TNIMS-Cover-FINAL.pdf` |
| Softcover cover | `Output/FINAL-Master-PDFs/TNIMS-Cover-SOFTCOVER-FINAL.pdf` |
| Flipbook (not for Lulu) | `Output/FINAL-Master-PDFs/TNIMS-Flipbook-FINAL.pdf` |
| Lulu templates / specs | `Xtraz/Lulu-Templates/from-lulu/` |
| **Website order playbook** | **`.cursor/docs/LULU-WEBSITE-ORDER-PLAYBOOK.md`** |

---

## Lulu connect options

| Mode | When | How |
|------|------|-----|
| **A — Manual + agent** | Anytime | You upload/download; agent rebuilds covers / docs |
| **B — Browser assist (used for orders)** | Order path | Cursor Simple Browser · unlock for file picker + pay · cart = `https://www.lulu.com/cart` |
| **C — Lulu Print API** | Optional / future | developers.lulu.com — not used for these gifts |

**Browser assist rules:** Prefer Jon logged in · never pay without OK · Language **English** + Category **Children** on Start before Review unlocks.

---

## Phase A — Approve interiors (local)

- [x] Interior / Cover PDFs approved for upload
- [x] Page count locked **34**

---

## Phase B — Create Lulu project + upload interior

- [x] **HC** draft/publish **`v82ejwq`** · Case Wrap · Matte · Premium · 80# · ~$18.28
- [x] **SC** draft/publish **`454zdy8`** · Perfect Bound · Matte · Premium · 80# · ~$9.46
- [x] Interior uploaded both · templates captured · specs docs in `from-lulu/`

---

## Phase C — Cover to Lulu spine

- [x] HC wrap **19×10.25″** / spine **0.25″**
- [x] SC cover built **17.387×8.75″** / spine **0.137″** (`build-softcover-cover-from-hc.py`)

---

## Phase D — Upload cover + soft-proof

- [x] Both covers uploaded · soft-proof OK (Jon)
- [x] Confirm and Publish · Add to Cart both bindings

---

## Phase E — Orders (done 2026-08-03)

- [x] **Jack:** 1 HC + 2 SC · Expedited · RE5RQ6G15 · **USD-C4242921** · $59.85 · est. Aug 11–12
- [x] **Jon:** 1 HC + 1 SC · Mail · RAC26SAVE10 · **USD-C4242970** · $34.53 · est. Aug 18–19
- [ ] (Optional) Archive Print-Ready zip if downloaded · track tracking emails

---

## What you do *not* need

| Skip | Why |
|------|-----|
| Upload Flipbook to Lulu | Digital preview only |
| Custom endsheets | Lulu white endsheets automatic |
| Spine type | Under 80 pages |
| Wrong cart URLs (`/account/cart`, `/shop/cart`) | Use **`/cart` only** |
| Softcover as same project as HC | Separate Lulu project required |

---

## Best process (one sentence)

**Lock page count → upload Interior → download template → build cover → upload cover → English+Children on Start → soft-proof → Confirm and Publish → Add HC+SC to `/cart` → one address per checkout → coupon → ship method → pay.**
