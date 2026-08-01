# CONTINUE HERE — The Night I Met Santa

**Read this first after TRUTH + START-HERE.**  
Project root: `D:\Hermes\projects\The-Night-I-Met-Santa`  
Operator: Jon · Gift for **Jack Farrell** · Birthday **2026-08-15**

---

## One-line status (2026-08-01 early AM)

**Gold foil end-page logos ready** (`Images/styles3/`). Masters still in `Adobe-Finals/final/`.  
**TOMORROW (priority):** Remake final PDF deliverables with latest remade artwork + place new logos as needed.

| Deliverable | Path | Spec |
|-------------|------|------|
| **INDD masters** | `Xtraz/Adobe-Finals/final/` | Interior 32 · Cover 1 · Flipbook 34 |
| **Interior PDF** | `Output/finals/TNIMS-Interior-FINAL-v2-burgundy-open-Lulu.pdf` | 32 · 8.75² / Trim 8.5² · S04 isolate — **re-export after art** |
| **Cover PDF** | `Output/finals/TNIMS-Cover-FINAL-Lulu.pdf` | 18.25×8.75 · sRGB — **re-export after art** |
| **Flipbook PDF** | `Output/finals/TNIMS-FLIPBOOK-trim.pdf` | **34** · 8.5² trim — **re-export after art** |

### New logos (2026-08-01) — transparent PNG
| Logo | Path |
|------|------|
| God Bless | `Images/styles3/logo-god-bless.png` (+ `-on-black`) |
| Jack Farrell | `Images/styles3/logo-jack-farrell.png` (+ `-on-black`) |
| Merry Christmas | `Images/styles3/logo-merry-christmas.png` (+ `-on-black`) |
| Source style | `Images/styles3/logo2.png` |

### Leave-off → start next
1. **Remake final last PDF deliverables** with latest remade artwork (Jon’s latest plates + logos).
2. Spec verify (`scripts/_scratch/_verify_finals_pdfs.py`) → refresh `Adobe-Finals/final/` snapshots if needed.
3. Then Lulu upload → spine → proof.

**Gift deadline:** **2026-08-15**.

---

## Copyright / p2|p3 (in ID — 2026-07-31)

**Source PSD:** `Xtraz/Adobe-Photoshop/TNIMS-P2-P3-v2.psb`  
**Art (no type):** `Images/chopz/from-psb-v7/P02-P03-spread-art.png` — seamless spread  
**Live type:** p2 · style `Copyright-Legal` · Cormorant Medium · 14/16 · tracking +12 · cream · **center** · `3-Live-Type`

```
Copyright © 2026 Jack Farrell
All rights reserved.

No part of this book may be reproduced or transmitted in any form
or by any means, electronic or mechanical, including photocopying,
recording, or by any information storage and retrieval system,
without permission in writing from the publisher or author.

This is a work of fiction. Names, characters, places, and incidents either
are the product of the author’s imagination or are used fictitiously,
and any resemblance to actual persons, living or dead, is entirely coincidental.

First illustrated edition, 2026. Book design by Jon Farrell.
www.jon-beatz.com
```

**Placement:** p1 blank burgundy · p2|p3 legal|title · not end blanks.

---

## What we are building

An **8.5×8.5"** full-color children’s picture book from Jack’s Christmas poem *The Night I Met Santa*, illustrated in **painted gouache / soft watercolor** (Golden Age / Santore–adjacent — **not** colored pencil), printed as **1 hardcover gift** (Lulu), possibly more later.  
**Candidate length:** **32 pages** (v2 burgundy-open). Rollback **30**. Target printer: **[Lulu](https://www.lulu.com/)**.  
**Build authority:** repo-root **`AGENT-RUNBOOK.md`**.

---

## Folder map (canonical)

| Path | Role |
|------|------|
| `Transcription/poem-clean.txt` | Poem text of record |
| **`Media/approved/`** | Keepers — `style-refs/` moodboard · Tier B locks — `INDEX.md` |
| `Media/generated/` | Experiments · **`mocks/{unit}/vNN/`** + RECIPE |
| `Media/assets/` | Watercolor cloud PNGs + reusable layout assets |
| `Images/references/` | Jack/photos + Christmas book + **layout** north stars |
| `Images/chopz/` | Exports for InDesign (incl. `from-psb-v7/` spread plates) |
| `Xtraz/Fonts/` | Local OFL pack (gitignored) — `FONT-CATALOG.md` |
| **`Xtraz/Adobe-Finals/`** | Print + flipbook INDDs / READMEs (gitignored binaries) |
| **`Xtraz/Adobe-inDesign/`** | Working `.indd` — **v10 current** |
| **`Xtraz/Adobe-Photoshop/`** | Working PSDs / **TNIMS-Master-Final-v7.psb** |
| **`Xtraz/Affinity/`** | Optional Affinity working docs |
| `Output/interiors/` · `Output/covers/` | Lulu PDF exports (gitignored) |
| `AGENT-RUNBOOK.md` | **Authoritative build runbook** (spread spine rule · per-layer type) |

---

## Layout north star

1. **Seamless spreads:** place **one** `5250×2625` spread PNG centered on the **spine** — never L/R halves with full bleed on both pages (`AGENT-RUNBOOK.md` § Seamless spread placement · `ISSUES-RESOLVED.md` 2026-07-30).
2. **Text+image** (S04 etc.): place **separate** L/R `2625²` chops · Lulu PDF export with facing art hidden then merge (`AGENT-RUNBOOK.md` § Text+image · `ISSUES-RESOLVED.md` 2026-07-31).
3. **Burgundy-open (v2):** two design pages at start (`#4A0E17`) so title stays RIGHT; not a substitute for Lulu’s white endsheets.
4. **Flipbook preview:** trim-only 8.5 PDF + Front→burgundy IFC→interior→burgundy IBC→Back.
5. **Cover export:** force `PDFColorSpace.RGB` if type has drop shadows (Leave Unchanged → CMYK flatten).
6. **Casewrap:** Lulu white endsheets automatic; fill cover wrap area on cover PDF only.

---

## Start next (priority order)

1. PS mockup copyright on p2 burgundy (copy above).
2. Set type in `TNIMS-Interior-FINAL-v2-burgundy-open.indd` → re-export PDF.
3. Lulu upload → spine template → proof.
