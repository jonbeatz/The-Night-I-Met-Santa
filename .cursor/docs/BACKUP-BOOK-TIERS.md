# Book backup tiers — The-Night-I-Met-Santa

**Scope:** This project only. Does not change other Hermes profiles or existing `v1-a`…`v1-g` folders.

| Say / npm | Tier | When |
|-----------|------|------|
| **backup quick** / **backup light** · `npm run backup:quick` · `backup:light` | **QUICK** | Daily / after dial sessions |
| **backup full** · `npm run backup:full` | **FULL** | Milestone · End Project · pre-proof |
| **backup archive** · `npm run backup:archive` | **ARCHIVE** | Rare deep freeze (old dial batches) |
| **backup project** · `npm run backup:project` | Interactive tier pick | When you want a prompt |

`backup:standard` and `backup:quick:full` alias to quick / full for old muscle memory.

## What each tier skips

| Skip | QUICK | FULL | ARCHIVE |
|------|:-----:|:----:|:-------:|
| `node_modules` / `.venv` / `.next` | ✓ | ✓ | ✓ |
| Old `Media/generated/test-*` dial batches (~1.5GB+) | ✓ | ✓ | — included |
| `_archive/` · `Xtraz/Lulu-Templates` | ✓ | — | — |
| `Output/` flipbooks | **kept** | **kept** | **kept** |

**Always kept (all tiers):** `.env.local`, docs, `Media/approved/`, `Media/generated/mocks/`, working `Xtraz/Adobe-*`, `Images/`, `Transcription/`, scripts, `_FLOW-CURRENT.json`.

## Verify

Book checks warn if missing: santa-G0-v2 · style-lock-v2 · `_FLOW-CURRENT.json` · Photoshop folder · `Output/` PDFs.

## Dry-run

```powershell
npm run backup:dry
# or
node scripts/project-backup.mjs --full --yes --dry-run
```

## Root

`G:\Hermes_Project_BackUpz\The-Night-I-Met-Santa\the-night-i-met-santa-project-v{N}-{letter}`

## Validation (2026-07-22)

- **QUICK** `v1-h` ≈ **1.47 GB** (old website-style full `v1-g` was ≈ **3.64 GB**)
- Confirmed skipped: old `test-batch*` / `jack-likeness` / `_archive` / `Lulu-Templates` / `.venv`
- Confirmed kept: `Media/generated/mocks`, approved locks, `Output/*.pdf`
- Existing `v1-a`…`v1-g` untouched
