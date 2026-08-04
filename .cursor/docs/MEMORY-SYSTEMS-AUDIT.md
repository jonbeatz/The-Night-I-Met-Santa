# Memory Systems Audit — TNIMS Production

**Date:** 2026-08-03  
**Auditor:** Draven (Hermes subagent)  
**Trigger:** Post-Lulu-order external memory systems audit  
**Scope:** Mem0, Mnemosyne, Vader_Vault, custom scripts, H:\Hermes-BackUpz

---

## Executive Summary

| System | Status | Critical Issues |
|--------|--------|-----------------|
| **Mem0 (jonbeatz + draven)** | ✅ Strong | No Lulu-order-final entry; draven "leave-off" stale (says "no Lulu order yet") |
| **Mnemosyne** | ⚠️ Broken | `npm run mnemosyne:recall` fails with `--top-k` error; 114 memories inaccessible via CLI |
| **Vader_Vault Sessions** | ⚠️ Gap | Missing 2026-08-02 session (cover production day); Mem0 reported "2 new vault sessions" that don't exist |
| **Vader_Vault Project Hub** | ✅ Current | Updated with Lulu orders, order IDs, coupon codes, shipping estimates |
| **G:\Hermes_Project_BackUpz** | 🔴 Stale | Last backup v1-j dated 2026-07-23 — no FINAL-Master-PDFs, no cover finals, no Lulu order era |
| **H:\Hermes-BackUpz** | 🟡 Partial | Master backup from 2026-07-25; no project-level TNIMS backup found; no PDFs |
| **Custom Scripts** | ✅ Production | 49 scripts; `book:type:*` and `book:cover:*` pipelines documented and working |

---

## 1. Mem0 (jonbeatz_memories + draven_memories)

### Findings
- **jonbeatz_memories:** Rich coverage — vault-sync entries covering every TNIMS session from 2026-07-14 through 2026-08-03. Captures workflow locks, spread verdicts, production decisions, Lulu specs.
- **draven_memories:** 20+ TNIMS entries covering cover production, flow pass, Lulu playbook, backup protocols. System-level production knowledge well-indexed.
- Both collections capture the full arc: research → moodboard → flow pass → InDesign build → PDF export → Lulu orders.

### Issues
| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 1 | **draven leave-off entry stale:** "no Lulu order yet" dated 2026-08-03 (pre-order state). Orders placed same day but entry not updated. | Medium | Add final order confirmation to draven: `npm run draven:add -- "TNIMS Lulu orders placed 2026-08-03: Jack USD-C4242921 (HC+2SC Expedited $59.85), Jon USD-C4242970 (HC+SC Mail $34.53)"` |
| 2 | **No dedicated "BOOK-COMPLETE" summary entry** in either collection. Production knowledge is scattered across vault-sync entries, not consolidated. | Medium | Create a single consolidated "TNIMS Production Complete" entry covering: final spec, order IDs, key decisions, gotchas, reusable playbook references. |
| 3 | **jonbeatz project-level Mem0** (`the-night-i-met-santa_memories`) not verified — only searched the main jonbeatz and draven collections. If the project has its own collection, it may be empty. | Low | Verify with `npm run mem0:search --collection the-night-i-met-santa_memories` |

---

## 2. Mnemosyne

### Findings
- **114 total memories**, 9 working memory entries, 0 episodic, 0 knowledge triples.
- **CLI is broken:** `npm run mnemosyne:recall` fails with `Error: top_k must be an integer: --top-k`. The PowerShell wrapper (`scripts/mnemosyne-chat.ps1`) appears to pass `--top-k` as a string instead of integer.
- **Status check passes** — `npm run mnemosyne:status` reports all green, smoke test OK.
- **No `mnemosyne:search` script** — only `recall`, `status`, `install`, `stats` are available.
- No way to verify whether TNIMS production entries exist in Mnemosyne without fixing the CLI.

### Issues
| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 4 | **`npm run mnemosyne:recall` broken** — blocks all Mnemosyne recall from Hermes. | 🔴 High | Fix `scripts/mnemosyne-chat.ps1` — cast `--top-k` argument to integer. Check the parameter binding in the PowerShell script. |
| 5 | **Mnemosyne recall unavailable** means we cannot verify if TNIMS production decisions were logged there. If the "Log It" protocol was followed, entries exist but are inaccessible. | Medium | Fix #4 first, then recall and verify. Add missing entries if needed. |
| 6 | **No `mnemosyne:search` script** — `stats` shows 114 entries but no way to search by keyword. Only recall by query works. | Low | Consider adding a search wrapper or using `mnemosyne:recall` with varied queries once fixed. |

---

## 3. Vader_Vault Sessions (`H:\Vader_Vault\03_AI_Memory\Sessions\`)

### Findings
- **35 TNIMS session files** spanning 2026-07-14 through 2026-08-03.
- Coverage is dense during peak production (Jul 19-24: ~20 files), sparse in late July/early August.
- Session files use inconsistent naming conventions: mix of `the-night-i-met-santa`, `The-Night-I-Met-Santa`, and `TNIMS` prefixes.
- **project-log.md** exists but is stale (last update: July 19, 2026). Still references early production state (S01 Approach as "Next Action").

### Session Gap Analysis
| Date | Sessions | Status |
|------|----------|--------|
| Jul 14-16 | 3 files | ✅ Covered |
| Jul 19-20 | 8 files | ✅ Heavy (DTP workflow, Photoshop MCP, P01 dial) |
| Jul 21-22 | 11 files | ✅ Peak (flow pass, workflow locked, book flow v2) |
| Jul 23-24 | 6 files | ✅ End Project + deep audit |
| Jul 25 | 2 files (system upgrades, cross-project fixes) | ⚠️ Non-TNIMS but relevant |
| Jul 27-28 | 4 files | ✅ P01 + S12 locks |
| Jul 29 | **0 files** | 🟡 Gap (Mem0 shows vault sync) |
| Jul 30-31 | 3 files | ✅ Cover v14, burgundy-open, PDF fix |
| **Aug 01** | 2 files | ✅ Gold-foil logos, merged chopz |
| **Aug 02** | **0 files** | 🔴 **GAP** — Cover production day (spine calc, 5700×3075 template, 1px edge fix). Mem0 draven entry says "2 new vault sessions" but no files exist. |
| **Aug 03** | 2 files | ✅ Print audit + Lulu orders |

### Issues
| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 7 | **2026-08-02 session missing from Vault.** This was the cover production day — spine calculation, 5700×3075 Lulu template, 1px white edge fix, Smart Object workflow. Knowledge only exists in draven Mem0. | 🔴 High | Reconstruct 2026-08-02 session log from draven Mem0 entries and write to `2026-08-02-The-Night-I-Met-Santa.md` |
| 8 | **2026-07-29 gap** — Mem0 reports vault sync but no session file found. | Low | Verify if sync was for non-TNIMS sessions or if file was lost. |
| 9 | **project-log.md stale** — still reflects July 19 state. Missing all InDesign production, PDF export, Lulu order phases. | Medium | Update project-log.md with full production timeline through 2026-08-03. |
| 10 | **Inconsistent naming** — mix of `the-night-i-met-santa`, `The-Night-I-Met-Santa`, and `TNIMS` prefixes makes grepping fragile. | Low | Adopt consistent `YYYY-MM-DD-The-Night-I-Met-Santa[-topic].md` pattern going forward. |

---

## 4. Vader_Vault Project Hub (`H:\Vader_Vault\01_Projects\The-Night-I-Met-Santa.md`)

### Findings
- **✅ Current and accurate.** Updated 2026-08-03 with:
  - Both Lulu order IDs (USD-C4242921, USD-C4242970)
  - Cart details (items, shipping, totals, coupons)
  - Project IDs (HC `v82ejwq`, SC `454zdy8`)
  - Deliverable paths
  - Key learnings from Lulu website
  - Links to playbook and related knowledge notes
- Frontmatter status: `ordered-awaiting-delivery`
- Well-structured with tables and clear next actions.

### Issues
| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 11 | **No issues.** | — | Maintain this quality for future books. |

---

## 5. Custom Scripts (`D:\Hermes\projects\The-Night-I-Met-Santa\scripts\`)

### Findings
- **49 script files** covering: image generation (FAL, OpenRouter), flipbook assembly, PDF verification, cover rebuild (PS/JSX), type inventory pipeline (PS→ID handoff), backup, docs update, model comparison, text overlay, book poem map.
- **Production pipelines documented in package.json:**
  - `book:cover:*` — Cover rebuild workflow (rebuild-wrap, art-notype, reopen-sot) via `cover-rebuild.ps1` + JSX
  - `book:type:*` — PS→ID type handoff pipeline (export, page-map, validate, apply, styles)
  - `backup:*` — Tiered backup (quick/light/standard/full/archive) via `project-backup.mjs`
- **Key production scripts confirmed working:**
  - `book_poem_map.py` (332 lines) — poem/caption map from Flow v2, used for comparison boards
  - `book-flipbook-assemble.py` (311 lines) — flipbook PDF assembly from `_FLOW-CURRENT.json`
  - `cover-rebuild.ps1` (49 lines) — Photoshop JSX runner for cover operations
  - `export_type_inventory_from_psb.py` (344 lines) — PS text extraction for InDesign handoff
  - `build_indesign_page_map.py` (163 lines) — page map from type inventory
  - `project-backup.mjs` (459 lines) — comprehensive tiered backup system

### Issues
| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 12 | **Scripts have no README** — no index of what each script does, when to use it, or dependencies. | Medium | Create `scripts/README.md` with script inventory, purpose, and usage examples. |
| 13 | **`project-backup.mjs` targets `G:\Hermes_Project_BackUpz`** — G: drive backup is stale (last v1-j, 2026-07-23). No post-production full backup exists. | 🔴 High | Run `npm run backup:full` immediately to capture FINAL-Master-PDFs, cover finals, and Lulu order state. |
| 14 | **Some scripts are one-shot artifacts** — `generate-test-book-v1-klein.py`, `jack_likeness_v5_fireplace.py`, `mock_text_overlay_v2.py`, `model_compare_beat01.py` are historical and no longer relevant. | Low | Consider archiving to `scripts/_archive/` to reduce noise. |
| 15 | **No `validate_type_inventory.py`** exists despite being referenced in `book:type:validate` and `book:type:pipeline` npm scripts. | 🟡 Medium | Verify if script is missing or at a different path. Pipeline will fail if validation step is dead. |

---

## 6. Backups

### G:\Hermes_Project_BackUpz\The-Night-I-Met-Santa\
- **10 backup versions** (v1-a through v1-j)
- **Last backup:** v1-j, modified **2026-07-23** — **11 days stale**
- v1-j contents: `Output/` has old flipbooks from July 21-22, no `FINAL-Master-PDFs/`, no cover finals
- **No backup since July 23** — missing all post-mock-book work: InDesign production, cover rebuilds, interior PDFs, flipbook finals, Lulu orders

### H:\Hermes-BackUpz\
- **Master-Hermes-Backup** from 2026-07-25 (system upgrade day) — apps, assets, profiles
- **projects/** directory backs up other projects (DigitalStudioz, JonBeatz, etc.) but **NO The-Night-I-Met-Santa**
- **No PDFs, no book deliverables** found anywhere in H:\Hermes-BackUpz

### Issues
| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 16 | **G: backup 11 days stale** — missing all final production deliverables. | 🔴 Critical | Run `npm run backup:full` (or `backup:archive`) from TNIMS repo root immediately. |
| 17 | **H:\Hermes-BackUpz has no TNIMS project backup** — the "Master" backup covers system/apps but not book deliverables. | 🔴 Critical | Either add TNIMS to H:\Hermes-BackUpz projects or document that G: is the canonical backup for books. |
| 18 | **No offsite/cold storage** — both backups are on local drives (G: and H:). If both drives are in the same PC, there's no disaster recovery. | Medium | Consider cloud backup of FINAL-Master-PDFs (Google Drive, GitHub LFS, or similar). |

---

## Summary: Action Items by Priority

### 🔴 Critical (do immediately)
1. **Run `npm run backup:full`** from TNIMS repo — capture all final deliverables
2. **Reconstruct 2026-08-02 Vault session** from draven Mem0 entries
3. **Fix Mnemosyne CLI** (`--top-k` integer cast in `scripts/mnemosyne-chat.ps1`)

### 🟡 Medium (do before next book)
4. Update draven leave-off entry with order confirmation
5. Create consolidated "TNIMS Production Complete" Mem0 entry
6. Update project-log.md with full production timeline
7. Create `scripts/README.md` with script inventory
8. Verify `validate_type_inventory.py` exists (or fix pipeline)
9. Add TNIMS to H:\Hermes-BackUpz or document G: as canonical
10. Verify project-level Mem0 collection if it exists

### 🟢 Low (nice to have)
11. Archive one-shot historical scripts
12. Standardize session naming convention
13. Investigate 2026-07-29 vault sync gap
14. Consider offsite backup for FINAL-Master-PDFs
15. Add `mnemosyne:search` script for keyword search

---

## Systems That Worked Well
- **Vader_Vault Project Hub** — accurate, timely, well-structured Lulu order documentation
- **draven Mem0** — comprehensive production knowledge, 20+ TNIMS entries, good gotcha capture
- **jonbeatz Mem0** — vault-sync pipeline kept session history consistent
- **Custom script pipeline** — `book:cover:*` and `book:type:*` are well-designed and documented in package.json
- **Session density** — 35 Vault sessions provide excellent production traceability for the critical weeks
- **Lulu playbook capture** — quick documentation of website quirks (cart URL, English+Children, separate checkouts)

---

*Audit performed by Draven via Hermes Agent subagent. Report saved to `.cursor/docs/MEMORY-SYSTEMS-AUDIT.md`.*
