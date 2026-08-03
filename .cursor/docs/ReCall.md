# ReCall.md — The-Night-I-Met-Santa

## Session resume (read in order)

1. `TRUTH.md`
2. `.cursor/docs/START-HERE.md`
3. **This file** — `.cursor/docs/ReCall.md`
4. `.cursor/docs/CONTINUE-HERE.md`
5. **`.cursor/docs/LULU-WEBSITE-ORDER-PLAYBOOK.md`** ← full Lulu website recreate (HC+SC+cart+coupons+shipping)
6. **`.cursor/docs/LULU-ORDER-CHECKLIST.md`**
7. **`.cursor/docs/MERGED-PLATE-EXPORT-WORKFLOW.md`**
8. **`.cursor/docs/COVER-REBUILD-WORKFLOW.md`**
9. **`.cursor/docs/PS-TO-ID-TYPE-HANDOFF.md`** ← PS→ID type inventory + book-2 upgrades (fleet §7)
10. Always-open: Flow v2 · Master Dock · IMAGE-LANE-v2 · `AGENT-RUNBOOK.md`
11. SoT plates: `Media/generated/mocks/_FLOW-CURRENT.json`

## Current focus
**Day-end 2026-08-03.** Lulu orders live · type-inventory pipeline shipped · continue tomorrow with delivery watch + optional full `book:type:pipeline`.

## Last updated
2026-08-03 late — End Project. Session: Lulu website orders + playbook · PS→ID type handoff + `book:type:*` tooling (S01 smoke OK).

### Lulu orders (2026-08-03)
| Who | Order # | Cart | Ship | Coupon | Total | Est. delivery |
|-----|---------|------|------|--------|-------|---------------|
| **Jack** | **USD-C4242921** | 1 HC + 2 SC → Abington MA | Expedited | RE5RQ6G15 (−15%) | $59.85 | Aug 11–12 |
| **Jon** | **USD-C4242970** | 1 HC + 1 SC · Montebello CA | Mail | RAC26SAVE10 (−10%) | $34.53 | Aug 18–19 |

**Projects:** HC `v82ejwq` · SC `454zdy8` · both published.  
**Billing (both):** Jon · 576 N Bellflower #142 · Long Beach CA 90814 · (213) 219-8893.  
**Playbook:** `.cursor/docs/LULU-WEBSITE-ORDER-PLAYBOOK.md`

### Final PDFs
| File | Use |
|------|------|
| `TNIMS-Interior-FINAL.pdf` | Both bindings |
| `TNIMS-Cover-FINAL.pdf` | Hardcover |
| `TNIMS-Cover-SOFTCOVER-FINAL.pdf` | Softcover |
| `TNIMS-Flipbook-FINAL.pdf` | Preview only |

### Lulu website lessons (short)
- Start: **English** + **Children** before Review unlocks
- Goal: **Print Your Book** · Premium Color · 80# coated · Matte
- Cart only at **`https://www.lulu.com/cart`** (not `/account/cart`)
- Two projects for HC+SC · Add Version to Cart · set qtys · one address per checkout
- Coupons: RE5RQ6G15 15% (single-use) · RAC26SAVE10 10%
- Mail ≈ Ground ETA −2 days, ~$8 cheaper (this cart)
- Optional zip `454zdy8_DRAFT_print_ready` = Lulu Print-Ready snapshot (archive OK, not new master)

### Type handoff (shipped this session)
- Doc: `.cursor/docs/PS-TO-ID-TYPE-HANDOFF.md` · fleet §7
- npm: `book:type:export` · `export:split` · `validate` · `page-map` · `apply` · `styles` · `pipeline`
- S01 smoke: 2 frames after dedupe → `Media/development/S01-approach/type-inventory.json`

## Start here next
1. Watch order emails / tracking for Jack (Expedited) then Jon (Mail)
2. Optional: `npm run book:type:pipeline` for full book inventory (or unit-by-unit)
3. Reprints: My Projects → Add to Cart → playbook
4. Physical QC when Jack’s Expedited box arrives (aim before **2026-08-15**)

## System of record
| Doc | Use |
|-----|-----|
| **LULU-WEBSITE-ORDER-PLAYBOOK.md** | Recreate website order end-to-end |
| **LULU-ORDER-CHECKLIST.md** | Phases A–E status |
| **COVER-REBUILD-WORKFLOW.md** | Cover PS/INDD |
| **AGENT-RUNBOOK.md** | Print authority |
| **PS-TO-ID-TYPE-HANDOFF.md** | Type inventory · live ID · MOCK |
| CONTINUE-HERE | Next actions |
