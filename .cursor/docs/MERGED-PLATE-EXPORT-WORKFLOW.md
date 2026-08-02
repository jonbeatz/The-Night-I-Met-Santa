# Merged Plate Export Workflow — TNIMS

**Locked 2026-08-01** · Source of truth for exporting art from the Book Master PSB into InDesign finals.

## Folder map (finals)

| Role | Path |
|------|------|
| Master PSB | `Xtraz/Adobe-Photoshop/FINAL-Master-PSDs/TNIMS-Book-Master-FINAL.psb` |
| Cover PSDs | `…/FINAL-Master-PSDs/TNIMS-Cover-*.psd` |
| Chopz (art links) | `Xtraz/Adobe-Finals/FINAL-Master-Chopz/` |
| InDesign masters | `Xtraz/Adobe-inDesign/FINAL-Master-inDD/` |
| PDF deliverables | `Output/FINAL-Master-PDFs/` |

Chopz subfolders:

- `TNIMS-Interior-FINAL-Chopz/` — Lulu interior links  
- `TNIMS-Flipbook-FINAL-Chopz/` — same PNGs (copy) for flipbook INDD  
- `TNIMS-Cover-FINAL-Chopz/` — cover wrap chops (from cover PSDs, not the book PSB)  
- `*/originalz/` — prior chops kept for rollback  

## PSB structure (best practice)

Keep **two stacks** in `TNIMS-Book-Master-FINAL.psb` (5250×2625 @ 300 DPI):

| Stack | Purpose |
|-------|---------|
| **`TNIMS-Layer-Comps`** | Editable: smart objects, drkn, logos, live type groups |
| **`TNIMS-Merged-Comps`** | One stamped `*Merged*` plate per unit + optional Text group |

Unit groups: `PO` · `P01` · `P02` · `S01`–`S12` · `P-author-thank-you` · `Back-Page` (p32\|33)

### Glow / shadow type shells (intentional)

Many pages use **fill opacity 0** on type with **Outer Glow / Drop Shadow** so only the effect stamps into Merged.  
**Live Cormorant (or Cinzel) in InDesign sits on top** and matches position — this is the preferred readability path. Do **not** strip those shells from Merged before export.

When updating a Merged stamp:

1. Solo the unit in Layer-Comps (or Merged stack)  
2. Include glow shells if desired  
3. Stamp / update that unit’s `*Merged*` pixel (or Merged group)  
4. Leave unit groups **hidden** in Merged-Comps — export does not need them visible  

Optional: color-label export units **green** for eye-scan (nice-to-have, not required).

### Future option — color-only export (not built yet)

Jon may want: “export all **yellow** (or red/…) layers” without relying on `*Merged*` names.  
**Plan when asked:** add `--color yellow` (and/or color+name) to `scripts/export_merged_plates_from_psb.py` via PSD layer color labels (`lclr`). Default stays name-based `*Merged*`.

## Export command

```powershell
# From repo root — all units -> Interior + Flipbook chopz
python scripts/export_merged_plates_from_psb.py --all

# Subset
python scripts/export_merged_plates_from_psb.py --only S03,S12,Back-Page
```

**Method:** `psd_tools` reads `*Merged*` via **`topil()`** (raw stamped pixels).  
Do **not** use `composite()` alone — hidden parent groups return blank white/black.

Manifest: `FINAL-Master-Chopz/TNIMS-Interior-FINAL-Chopz/_export-manifest.json`

### Photoshop UXP (optional live control)

For agent visibility / layer ops (not required for Merged PNG dump):

1. `npm run layout:photoshop-mcp` (broker `:47391` + MCP `:8766`)  
2. UDT → Adobe Python Bridge for Photoshop → **Reload** then **Watch**  
3. Smoke: `curl.exe -s http://127.0.0.1:47391/health` → `"sessions":1`  
4. If Cursor photoshop MCP is red: re-auth / toggle MCP, then Reload UDT after any broker restart  

InDesign: prefer **indesign-uxp** (Bridge Connected). Same cold-start: UDT Reload if bridge was up before server restart.

## InDesign placement

| Rule | Detail |
|------|--------|
| **Reuse masters** | Relink into existing `FINAL-Master-inDD` INDDs — do not rebuild from scratch |
| **Spreads** | Place one `*-spread.png` (5250×2625) centered on spine (`AGENT-RUNBOOK` seamless rule) |
| **S04** | Text\|image split — L/R halves **meet at spine** (no facing bleed). Isolate merge = legacy fallback only |
| **P0\|P01** | One `P0-P01-spread.png` on p2\|3 (copyright left · title/dedication right) |
| **P02** | Use Jon’s baked plate if logo is in art — do **not** re-place `logo-our-story-begins.png` |
| **Live type** | Overlay poem / dedication / thank-you on glow shells; hide MOCK when done |
| **Same art, two PDFs** | Interior = 8.75² bleed Lulu · Flipbook = 8.5² trim — middle art identical; Flipbook ends = FRONT/BACK covers |
| **Covers** | Keep in `TNIMS-Cover-*.psd` — **not** inside Book Master PSB |

### End matter (2026-08-01)

| Pages | Content |
|------:|---------|
| 30\|31 | Thank You + Dad / author (`P-author-thank-you-spread`) |
| 32\|33 | Quiet close + Happy Holidays \| solid burgundy (`Back-Page-spread`) |

p32 = back of Dad’s portrait leaf. p33 burgundy is an **interior** closer — **not** Lulu’s physical back cover (endsheets stay white/auto).

## Lulu + flipbook PDF

After relink + type match:

1. Export Interior (normal Lulu bleed; S04 spine-meet) → `Output/FINAL-Master-PDFs/`  
2. Rebuild Flipbook from Interior + FRONT/BACK → export trim PDF  
3. Cover: wait for Lulu spine template after interior upload → then export sRGB Cover PDF  
4. Spec verify scripts under `scripts/_scratch/_verify_finals_pdfs.py`  

## What worked well (keep)

1. Dual stack Layer-Comps + Merged-Comps  
2. Fill-0 + glow shells → ID live type overlay  
3. One Merged export feeding Interior **and** Flipbook chopz  
4. Finals folder quartet: PSDs · Chopz · inDD · PDFs  
5. `psd_tools` + `topil()` for fast batch without depending on UXP for every dump  
6. Broker restart → always **UDT Reload** PS bridge (Loaded ≠ sessions≥1)  

## What to avoid

- Forcing short logos into ultra-wide 4:1 canvas (letter squash)  
- Treating Lulu endsheets as designable interior pages  
- `composite()` export while Merged unit groups are hidden  
- New blank INDDs when masters already have live type + page map  
- Calling Merged “final print” without InDesign live type + PDF verify  

## Related

- `AGENT-RUNBOOK.md` — print authority · seamless spread · S04 spine-meet  
- `tools/layout-mcp/PHOTOSHOP-SETUP.md` — UXP cold-start  
- `scripts/export_merged_plates_from_psb.py` — this pipeline  
