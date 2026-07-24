# Agent notes — The-Night-I-Met-Santa

## Always open (book work) — these four only

1. **`.cursor/docs/JON-BOOK-FLOW-v2-FINAL.md`** — page map / rhythm / GPT pillars  
2. **`.cursor/docs/MASTER-PRODUCTION-DOCK.md`** — prompts  
3. **`.cursor/docs/IMAGE-LANE-SYSTEM-v2.md`** — lanes · boards · flipbook · hero spend  
4. **`AGENT-RUNBOOK.md`** — InDesign / print / never-dos  

**Current plates SoT:** `Media/generated/mocks/_FLOW-CURRENT.json` (flipbook reads this only).

**Session resume:** `TRUTH.md` → `CONTINUE-HERE.md` → `ReCall.md` → then the four above.

Everything else is **reference on demand** (do not auto-load): `PAGE-BUILD-WORKFLOW`, `BOOK-PAGE-WORKFLOW`, `BOOK-PRODUCTION-SYSTEM`, `ISSUES-RESOLVED`, `INDESIGN-PRODUCTION-WORKFLOW`, `IMAGE-LANE-PROMPTS`, `ILLUSTRATION-STYLE`, `FONT-CATALOG`, `BOOK-PLAYBOOK`, fleet mirrors, archives, Tony handoff.

## Project facts

- **Root:** `D:\Hermes\projects\The-Night-I-Met-Santa`
- Gift book for Jack Farrell · birthday **2026-08-15** · Lulu **8.5×8.5"**
- **Art:** painted gouache / soft watercolor · **fal.ai first**
- **Style lock:** `Media/approved/style-refs/style-lock-v2.png` (Krea regen + santa-G0-v2) — **only** style file in approved
- **Santa lock:** `santa-G0-v2.png` (+ standing `santa-G0.png`) — **open** red coat · cream striped shirt · brown suspenders **over shirt** · red pants · black boots
- **Boy G0:** `boy-narrator-G0.png` + `boy-narrator-G0-face.png` — oatmeal/taupe holly · red trim/buttons · brown eyes
- **Hero spend:** GPT High 4K **only** if `gpt_pillar: true` (S3 · S12b). **Primary finals** = Banana Pro `/edit` + style-lock-v2 + santa-G0-v2 (+ boy G0). Alt = pure Krea atmospheric.
- **Dial:** Klein 9B primary · Qwen 2 Pro `/edit` favorite mock look · always attach style-lock-v2 (+ Boy/Santa G0 when characters present)
- **Comparison boards:** one board per decision (Klein | new | favorite). Retroactive S04 multi-boards = archive.
- **Quality bar (2026-07-22):** `Media/development/S03-eyes-met/v07/art.png` — prefer fewer gifts later; doorway spill from S2 v05
- **Forever locks (approved/):** boy G0 · **santa-G0-v2** · Jack portrait · style-lock-v2 · frame refs
- **Story keeps (development/):** P01 v16 · P02 v04 · S1 v13|v14 · **S2 v06** · **S3 v07** · **S4 v13** · S5–S11 KEEP · **S12 v22 working** (Jon PS)
- **Back matter:** p30 KEEP · p31 framed (`P-author`) · p32|33 working · **"God bless." on S12 R only**
- **Pre-finals gate:** `.cursor/docs/FINALS-CHECKLIST.md`
- **Current-best page art:** `Media/development/` (not Lulu-final)
- **Layout:** InDesign UXP · Photoshop adobepy LIVE

## Media three-tier (LOCKED 2026-07-22)

| Tier | Path | What belongs |
|------|------|----------------|
| **1 — Forever** | `Media/approved/` | **Only** `characters/` + `style-refs/style-lock-v2.png` (+ recipe). Never put page art here. |
| **2 — Current best** | `Media/development/` | Visual dashboard — one folder per Flow unit. On **keep** / **lock it (for now)** → **COPY** image here **+ write `RECIPE.md` + `meta.json`**. Pre-InDesign, no live text. |
| **3 — Lulu-ready** | `Media/finals/` | Empty until InDesign live text + bleed + export. Then graduate from development. |
| Dials | `Media/generated/mocks/` | Versioned dials + RECIPE. SoT machine list: `_FLOW-CURRENT.json` |
| Old approved clutter | `Media/generated/mocks/archive/` | Former covers/pages/spreads/style-refs |

**Rules**
1. Jon says **keep** / **lock it** → copy to `Media/development/{unit}/` (update FLOW `path` + `tier: "development"`) **and** write unit-root **`RECIPE.md` + `meta.json`**. Do not report locked until both exist.
2. Page built in InDesign with text → output to `Media/finals/` (`tier: "finals"`).
3. `approved/` = character refs + style lock **ONLY**.
4. `_FLOW-CURRENT.json` = machine-readable SoT (`tier`: `approved` \| `development` \| `finals` \| `mocks`).
5. `development/` = human visual dashboard. **Nothing is Lulu-final until `finals/`.**
6. Quality-bar compare: `Media/development/_quality-targets/S03-eyes-met-v07-quality-bar.jpg` (PNG under `S03-eyes-met/` remains SoT).

## Paths

| Asset | Path |
|-------|------|
| Poem | `Transcription/poem-clean.txt` |
| Current plates | `Media/generated/mocks/_FLOW-CURRENT.json` |
| Forever locks | `Media/approved/characters/` · `Media/approved/style-refs/style-lock-v2.png` |
| Current-best art | `Media/development/` |
| Lulu-ready | `Media/finals/` |
| Dials | `Media/generated/mocks/` |
| Flipbook | `Output/flipbook-{date}.pdf` |
| InDesign / PS | `Xtraz/Adobe-inDesign/` · `Xtraz/Adobe-Photoshop/` |

## Rules

- Never call anything “final” until it lives in `Media/finals/` (InDesign + live text). Never regen G0 / style-lock without Jon.
- Update `_FLOW-CURRENT.json` when a plate or verdict changes (`decided_by` + `date` + `tier` required).
- Then rebuild flipbook: `npm run book:flipbook`
- **`project-log.md` = milestones/decisions only** — not individual model tests or comparison-board runs. Document tests/boards in each version’s `RECIPE.md` and in `_FLOW-CURRENT.json`. Log to `.cursor/docs/project-log.md` only when: a spread is locked, a character reference is promoted, or a production phase completes.
- **Backups (book tiers):** `npm run backup:quick` (daily) · `backup:full` (milestone) · `backup:archive` (deep). See `.cursor/docs/BACKUP-BOOK-TIERS.md`.
- **Milestone git tags:** When Jon says **commit and push** or **lock it** on a major decision, after that commit succeeds create an **annotated** tag (so the one-line message is stored), then push the tag.
  - **Name:** `{category}-{what}-locked` (or `…-final` when that reads clearer) — e.g. `s1-approach-locked`, `santa-character-locked`, `style-lock-v2-final`, `s2-threshold-locked`, `production-workflow-locked`
  - **When:** **After** the commit that contains the change — never tag before commit
  - **Message (one line):** what was locked + version — e.g. `S1 Approach locked — v13 LEFT + v14 RIGHT`
  - **Commands:** `git tag -a <name> -m "<message>"` then `git push origin <name>` (or `git push origin --tags` when pushing several)
  - **Do not** tag routine dials, docs-only tidy, or backup-script commits — only locked spreads, promoted character/style refs, or production-phase locks
  - Skip if Jon says commit/push without a lock (ordinary WIP)
