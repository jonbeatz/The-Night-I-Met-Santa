# Lulu website order playbook — TNIMS (hardcover + softcover)

**Locked after live orders 2026-08-03.** Recreate from this doc.  
**Companion:** `.cursor/docs/LULU-ORDER-CHECKLIST.md` (phases A–E) · specs in `Xtraz/Lulu-Templates/from-lulu/`.

---

## Orders placed (SoT)

| | **Jack gift** | **Jon keep** |
|--|---------------|--------------|
| **Order #** | **USD-C4242921** | **USD-C4242970** |
| **Ship to** | Jack Farrell · 195 Lincoln St · Abington, MA 02351 · (781) 534-2277 | Jon Farrell · 337 N 4th St · Montebello, CA 90640 · (213) 219-8893 |
| **Bill to** | Jon Farrell · 576 N Bellflower Blvd #142 · Long Beach, CA 90814 · (213) 219-8893 | Same Long Beach billing |
| **Cart** | 1 hardcover + **2** softcover | 1 hardcover + **1** softcover |
| **Shipping** | **Expedited** $26.24 · est. **Aug 11–12** | **Mail** $6.94 · est. **Aug 18–19** |
| **Coupon** | **RE5RQ6G15** (−15%) | **RAC26SAVE10** (−10%) |
| **Paid** | **$59.85** | **$34.53** |
| **Email** | jonbeatz@gmail.com | jonbeatz@gmail.com |

**Why two checkouts:** One shipping address per cart. Do **not** mix Abington + Montebello in one order.

---

## Lulu projects (published)

| Role | Project ID | Binding | Unit print | Cover PDF size |
|------|------------|---------|------------|----------------|
| Hardcover | **`v82ejwq`** | Case Wrap · Matte · Premium Color · 80# coated · 34pp | ~$18.28 | **19 × 10.25″** · spine **0.25″** |
| Softcover | **`454zdy8`** | Perfect Bound · Matte · same paper/color/pages | ~$9.46 | **17.387 × 8.75″** · spine **0.137″** |

Titles on Lulu: *The Night I Met Santa* · *The Night I Met Santa Softcover* (separate projects — required).

### Final PDFs (local)

| File | Path |
|------|------|
| Interior (both) | `Output/FINAL-Master-PDFs/TNIMS-Interior-FINAL.pdf` |
| Hardcover cover | `Output/FINAL-Master-PDFs/TNIMS-Cover-FINAL.pdf` |
| Softcover cover | `Output/FINAL-Master-PDFs/TNIMS-Cover-SOFTCOVER-FINAL.pdf` |
| Softcover build | `scripts/build-softcover-cover-from-hc.py` |
| Softcover specs | `Xtraz/Lulu-Templates/from-lulu/SPECS-SOFTCOVER-LOCKED-2026-08-03.md` |
| Hardcover specs | `Xtraz/Lulu-Templates/from-lulu/SPECS-LOCKED-2026-08-01.md` |

---

## Product settings (do not change without reason)

| Spec | Value |
|------|--------|
| Product type | **Print Book** |
| Goal | **Print Your Book** (buy copies — **not** Publish / Global Distribution) |
| Language | **English** |
| Category | **Children** (Children’s / juvenile as shown in Lulu picker) |
| Size | Square **8.5 × 8.5 in** |
| Interior color | **Premium Color** (ignore Standard even if ink warning appears) |
| Paper | **80# White — Coated** |
| Cover finish | **Matte** |
| Pages | **34** |

---

## End-to-end website workflow

### 0 — Browser assist rules

1. Prefer **Cursor Simple Browser** with Jon already logged into Lulu.
2. Agent **locks** the tab while driving; **unlock** for OS file pickers and card payment.
3. **Never pay** until Jon confirms.
4. Cart URL that works: **`https://www.lulu.com/cart`** only.

### 1 — Create project (Start)

1. Create project → **Print Book**.
2. Goal → **Print Your Book**.
3. Title → HC: *The Night I Met Santa* · SC: *The Night I Met Santa Softcover*.
4. **Mandatory before Design/Review unlocks:**
   - **Book language** = **English** (select from dropdown / Enter to commit).
   - **Book category** = **Children** (type + select option).
5. Click **Design Your Project**.

**Gotcha:** If Language + Category are empty, Start can sit on “processing” and **Review Book stays disabled**. Fill both first.

### 2 — Design (files + specs)

1. Upload **interior** PDF (same file for HC and SC).
2. Confirm size **Square 8.5×8.5** · **34** pages.
3. Select **Premium Color** · **80# White Coated** · binding (**Case Wrap** or **Perfect Bound**) · **Matte**.
4. Download Lulu **cover template** (spine depends on binding + page count).
5. Build cover PDF to template size (HC wrap already locked; SC = remap from HC via script).
6. Upload **cover** PDF.
7. Soft-proof in Lulu preview (Jon eyes OK).
8. When Design is complete → **Review Book**.

**Operator intervention:** OS file picker for PDF uploads — agent unlocks browser; Jon picks files from `Output/FINAL-Master-PDFs/`.

**Softcover cover tip:** If Lulu preview goes blank after a huge raw-embed PDF, re-export with JPEG compression (~3–5 MB worked). Script path above.

**Ink warning:** Expected on illustrated books — stay on **Premium Color**.

### 3 — Review → publish → cart

1. **Review** → **Confirm and Publish** (button may disable while processing).
2. When Complete → **Add to Cart**.
3. Repeat for the second binding if needed (My Projects → **Add Version 1 to Cart** on each published project).
4. Open **`https://www.lulu.com/cart`**.
5. Set quantities (spinbuttons) → Tab/blur so cart badge updates.
6. **Checkout**.

**Cart pattern that worked**

| Order | From My Projects | Qty |
|-------|------------------|-----|
| Jack | Add HC + Add SC | HC **1** · SC **2** |
| Jon | Add HC + Add SC | HC **1** · SC **1** |

After first Add, use **Continue Shopping** (or return to Projects) before adding the second title.

### 4 — Checkout shipping

1. Fill ship-to (or autocomplete address → pick USA option).
2. Phone required.
3. **Choose Delivery Method** → pick Mail / Ground / Priority / Expedited / Express.
4. Continue to Payment.

### 5 — Billing + pay

1. If billing ≠ shipping: **uncheck** “Use my shipping address”.
2. Fill billing (Jon Long Beach for both gift orders).
3. **Choose Payment Method** → card / GPay / Apple Pay.
4. Jon pays · agent stops before Pay unless told otherwise.

---

## Coupons (tested 2026-08-03)

| Code | Result |
|------|--------|
| **RE5RQ6G15** | **Works −15%** (best on Jack order). Second checkout: *Discount code already redeemed*. |
| **RAC26SAVE10** | **Works −10%** (applied on Jon order). |
| LULU20 · READ15 · SALETIME40 · TREAT15 · PLOT10 · WELCOME15 | *Oops! That code isn’t working for this order.* |

**Recommendation:** Try codes at checkout before delivery step. Prefer highest % that applies. Assume many codes are **single-use per account**.

---

## Shipping options (observed this session)

Costs **scale with cart weight/destination** — use as ballpark, not a price list.

### Jack cart (MA · 1 HC + 2 SC) — observed

| Method | Cost | Est. business days |
|--------|------|--------------------|
| Mail | ~$7.69 | 12–13 |
| Ground Home | ~$15.74 | 10–11 |
| Priority Mail | ~$19.24 | 10–11 |
| **Expedited** | **~$26.24** | **7–8** ← used for birthday buffer |
| Express | ~$43.24 | 6–7 |

### Jon cart (CA · 1 HC + 1 SC) — observed

| Method | Cost | Est. business days |
|--------|------|--------------------|
| **Mail** | **~$6.94** | **12–13** ← used |
| Ground Home | ~$14.99 | 10–11 |
| Priority Mail | ~$17.24 | 10–11 |
| Expedited | ~$23.74 | 7–8 |
| Express | ~$39.74 | 6–7 |

**Decision guide**

- **Deadline / gift date tight** → Expedited (or Express).
- **No rush + save money** → Mail (~$8 cheaper than Ground here; only ~2 biz days slower on estimate).
- Priority ≈ Ground time, slightly more money — usually skip unless Mail unavailable.

---

## What Jon must do by hand (agent cannot / should unlock)

| Step | Why |
|------|-----|
| Pick PDFs in OS file dialog | Browser sandbox |
| Soft-proof eye OK | Taste / print judgment |
| Confirm pay / enter card | Money gate |
| Provide phones / confirm addresses | PII + accuracy |
| Optional: download Print-Ready zip | See below |

---

## `454zdy8_DRAFT_print_ready` zip (download popup)

**What it is:** Lulu’s **Print-Ready Files** package for project `454zdy8` (softcover), offered from Review/Complete (**Print-Ready Files** button). Snapshot of what Lulu accepted for print.

**Keep?** Optional archive — useful once as “what went to press.” **Not required** to reorder (projects stay published; re-Add to Cart from My Projects).

**Suggested save (if kept):** `Xtraz/Lulu-Templates/from-lulu/print-ready/454zdy8_DRAFT_print_ready.zip` (or Downloads archive). Do not treat as a new master over `Output/FINAL-Master-PDFs/`.

---

## 404 / wrong URL gotchas (avoid)

| Bad / confusing | Use instead |
|-----------------|-------------|
| `lulu.com/account/cart` | **`https://www.lulu.com/cart`** |
| `lulu.com/shop/cart` | **`https://www.lulu.com/cart`** |
| Jumping to Review before Language + Category | Fill Start fields first |
| Guessing wizard step URLs while Start still processing | Wait for Design to load · use nav links Start → Design → Review |
| Opening stale checkout session after order | New cart → new checkout UUID |

If a 404 appears: go **My Projects** or **`/cart`** — do not hammer the broken URL.

---

## Softcover recreate (short)

1. New Print Your Book project · title *… Softcover*.
2. English + Children · same interior PDF.
3. Perfect Bound · Premium · 80# coated · Matte.
4. Download SC template → run `scripts/build-softcover-cover-from-hc.py` (or rebuild) → upload SC cover.
5. Soft-proof → Confirm and Publish → Add to Cart.

Hardcover already published as `v82ejwq` — re-Add from My Projects for more copies.

---

## Recommendations (next time / other books)

1. **Two projects** when HC + SC both needed — never one project for both bindings.
2. **Same interior** PDF is fine; **cover files differ** (spine/width).
3. **Language + Category on Start** before anything else.
4. **Cart = one address.** Split gift vs personal into separate checkouts.
5. **Birthday / deadline** → Expedited early; personal copies → Mail OK.
6. **Coupons:** try before pay; don’t count on reuse.
7. **Proof vs gift:** this run ordered gift/keep copies directly after soft-proof — still valid for reprints via Add to Cart.
8. Prefer Cursor Simple Browser assist; unlock only for uploads + payment.

---

## Quick recreate checklist

- [ ] PDFs ready under `Output/FINAL-Master-PDFs/`
- [ ] Logged into Lulu (Simple Browser)
- [ ] HC project published (or create + upload + English/Children + publish)
- [ ] SC project published (or create + SC cover + publish)
- [ ] Add both to **`/cart`** · set qtys
- [ ] Checkout → ship address → delivery method
- [ ] Billing (if different) → try coupon → pay
- [ ] Save order #s to ReCall / vault
