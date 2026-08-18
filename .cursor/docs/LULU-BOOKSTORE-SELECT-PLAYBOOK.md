# Lulu Bookstore Select — Wizard Playbook (no holdups)

**Status:** LOCKED from TNIMS live run · **2026-08-18**  
**Use for:** TNIMS family links · **Harlow’s Big Adventure** (later) · any Hermes picture book that needs shareable order links without going public.  
**Companion (TNIMS links + prices):** [LULU-FAMILY-ORDERING.md](./LULU-FAMILY-ORDERING.md)  
**Payee pattern (no SSN):** vault `02_Knowledge/Patterns/Lulu-Payee-Jon-Farrell.md`  
**Vault SoT:** `H:\Vader_Vault\02_Knowledge\Patterns\Lulu-Bookstore-Select-Playbook.md`

---

## What we want (and what we do **not** want)

| Goal | Setting |
|------|---------|
| Family/friends order themselves | **Lulu Bookstore** + **`Select Access`** |
| Link works; **not** in Bookstore search | **Select** (UI icon often `access-direct`) |
| No ISBN / no barcode | Bookstore only — **do not** check **Global Distribution** |
| Author credit for family editions | **Jon Farrell** (not Jon Beatz) |
| Public searchable later | Only then flip to **General Access** — **not** for family-only |

| Access | Effect |
|--------|--------|
| **Private** | No share link — author account only |
| **Select** | Unlisted · **direct URL only** ← family default |
| **General** | Public Bookstore search ← avoid until intentional |

**Do not confuse “publish to Bookstore” with “make it public.”** Publishing under **Select** still puts the product on Lulu’s shop at a secret URL — it does **not** mean General/searchable.

---

## TNIMS live share links (easy find)

| Binding | Project ID | List | Select URL |
|---------|------------|------|------------|
| Softcover | `454zdy8` | **$12.00** | https://www.lulu.com/shop/jon-farrell/the-night-i-met-santa-softcover/paperback/product-454zdy8.html |
| Hardcover | `v82ejwq` | **$22.00** | https://www.lulu.com/shop/jon-farrell/the-night-i-met-santa-hardcover/hardcover/product-v82ejwq.html |

Print cost (approx): SC ~$9.46 · HC ~$18.28. Shipping/tax = buyer at checkout.

---

## CRITICAL: Pricing step (the holdup we hit)

### Symptom
- You type **Fixed List Price** (e.g. `$12` / `$22`) in the USD box.
- UI **looks** filled.
- **Final Review stays grey / disabled.**
- Backend / GraphQL often still has `pricing: null` — the fixed price **never saved**.

### Correct method (always do this)

1. On **Pricing & Payees** → **Set Price by** → choose **`Revenue Goal`** (not Fixed List Price).
2. Enter the **creator revenue target in USD** (Tab / blur so Lulu recalculates).
3. Lulu fills **all currency list prices** (USD/EUR/AUD/GBP/CAD) for you.
4. Confirm USD list matches your intended family price.
5. Then add payee → **Final Review** enables.

### Revenue Goal → intended list (TNIMS)

| Binding | Intended list | **Revenue Goal (USD)** | Why |
|---------|---------------|------------------------|-----|
| Softcover | ~$12 | **≈ $2.03** | ~80% of ($12 − $9.46) |
| Hardcover | ~$22 | **≈ $2.98** | ~80% of ($22 − $18.28) |

**Formula (Lulu Bookstore):** creator keeps ~**80% of (List − print cost)**; Lulu keeps ~20% of that markup.  
So: `Revenue Goal ≈ 0.8 × (desired list − print cost)`.

### Agent / operator checklist (pricing)

- [ ] Set Price by = **Revenue Goal**
- [ ] Typed goal → **Tab out** → USD list populated to target
- [ ] Other currencies non-empty
- [ ] Payee attached (share **100%** if sole payee)
- [ ] **Final Review** button/link **enabled** (not grey)

**Never** rely on Fixed List Price alone in this wizard until Lulu fixes save behavior. If Fixed somehow works later, still prefer Revenue Goal for multi-currency save reliability.

---

## Wizard order (do every step — one project at a time)

Repeat for **each** binding (SC and HC are separate Lulu projects).

### 1 — Start
- Goal: **Publish Your Book**
- Check **Lulu Bookstore**
- **Uncheck** Global Distribution
- Title: include Softcover / Hardcover in the project title so family links stay distinct

### 2 — Copyright
- Author / copyright: **Jon Farrell**
- Year: current
- **Proceed without ISBN** (Bookstore-only)

### 3 — Design
- Interior + cover already uploaded from print finals (skip if already done)

### 4 — Details (metadata)
| Field | TNIMS values (reuse pattern) |
|-------|------------------------------|
| Description | ≥50 chars; bookstore blurb |
| Lulu category | **Children's** |
| BISAC main | **JUVENILE FICTION / Holidays & Celebrations / Christmas & Advent** (`JUV017010`) — or book-appropriate BISAC |
| Keywords | At least one (e.g. `Christmas`) — commit as a **chip** (Enter / create option); “0 / 50” means not saved |
| Audience | **Children/Juvenile** |
| Explicit | Off |

### 5 — Pricing & Payees
1. **Revenue Goal** path (see CRITICAL above)
2. Payees:
   - **First book:** Create New Payee → Jon Farrell + PayPal + address (tax ID **only in Lulu**, never vault/repo)
   - **Later books (Harlow etc.):** **Select from Existing Payees** → check **Jon Farrell** → **Add Payees** → Share **100%**

### 6 — Review → Confirm and Publish
- Click **Confirm and Publish**
- Wait for **Complete** / Success

### 7 — Retail Options (access) — do **not** skip
After publish, on the same Review/Complete page:

1. Under **Retail Options → Lulu Bookstore**, select **`Select Access`** (radio `directAccess` / label “Unlisted…direct URL”)
2. Click **`Publish to the Lulu Bookstore`** (button appears when Select is chosen)
3. Confirm My Projects shows **COMPLETE · SELECT ACCESS** + correct list price

**Wrong:** leaving **Private** (no family link).  
**Wrong:** choosing **General** for family-only.  
**Right:** **Select** + Publish to Bookstore.

### 8 — Grab the share URL
1. **My Projects**
2. Row should show **SELECT ACCESS** (icon `access-direct`)
3. Open the Select/status control → product page, **or** copy the shop href on the Select link  
   Pattern: `https://www.lulu.com/shop/jon-farrell/<slug>/<paperback|hardcover>/product-<id>.html`
4. Save link in vault + project `LULU-FAMILY-ORDERING.md` (or Harlow equivalent)

### 9 — Verify (optional but recommended)
- Incognito / logged out → open link → add to cart → other ship-to address → see list price
- Bookstore search should **not** find the title under Select
- **Cart gotcha:** logged in as **author** → cart often shows **print cost**; family / logged out → **list price**

---

## After family orders — Sales & Payments

| What | Reality |
|------|---------|
| Live “new order” email with buyer name | **No** (privacy) |
| When sale shows in account | **End of that business day** on [Sales & Payments](https://www.lulu.com/account/sales-payments) — not live |
| What you see | Title · qty · region · channel (Lulu) · your revenue · CSV |
| PayPal money | ≥ **$5**/month earned → paid by **end of following month** |

Same-day $0 after family buys is normal — check next morning. Vault gotcha: `Gotchas/Lulu-Bookstore-sales-reporting.md`

---

## Agent automation notes (Cursor browser)

- Prefer **Revenue Goal** + Tab/blur; do not fight Fixed List Price.
- Keywords/BISAC are react-select: type search → pick option → ensure chip/count updates (`Keywords 1 / 50`).
- Existing payee: click **Jon Farrell** checkbox until `checked`, then **Add Payees** (button enables when selected).
- Select Access: click label/`#directAccess`, then **Publish to the Lulu Bookstore**.
- Product URLs may appear as `<a>` under SELECT ACCESS on My Projects (`aria-label=access-direct`).

---

## Harlow’s Big Adventure (reuse later)

When HBA is ready for family/friends ordering:

1. Follow **this playbook** end-to-end (Bookstore + Select + Revenue Goal).
2. Reuse payee **Jon Farrell** (existing) — do not recreate unless needed.
3. Set list prices intentionally; compute Revenue Goal = `0.8 × (list − print)`.
4. Document share links in Harlow `LULU-FAMILY-ORDERING.md` + vault hub [[Harlows-Big-Adventure]].
5. Stay on **Select** until Jon explicitly wants **General** / Global Dist / ISBN.

---

## Never-dos

- Do not store SSN / Tax ID in vault, Mem0, Mnemosyne, or git.
- Do not use Fixed List Price as the only pricing method (save bug → Final Review stuck).
- Do not enable Global Distribution for family Select links.
- Do not call Select “public” — General is public.
- Do not retire/replace payee casually; reuse Existing Payees.
- Do not panic if Sales & Payments is $0 the same day family ordered — wait until end of business day / next morning.

---

## Sources

- [Creator Revenue Guide](https://help.lulu.com/en/support/solutions/articles/64000262744-creator-revenue-guide) — Bookstore sales by end of business day
- [Selling on Lulu](https://help.lulu.com/en/support/solutions/articles/64000259798-selling-on-lulu)
- [Project Overview — get the link](https://help.lulu.com/en/support/solutions/articles/64000256834-project-overview-page)
- [Select Access](https://help.lulu.com/en/support/solutions/articles/64000255486-how-to-create-a-print-book)
- [Retail price / commission](https://help.lulu.com/en/support/solutions/articles/64000255458-how-do-i-set-the-retail-price-for-my-print-book-)
- [ISBN — Bookstore doesn’t require](https://help.lulu.com/en/support/solutions/articles/64000255457-isbn-the-basics)
