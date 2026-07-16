# TRUTH.md — The-Night-I-Met-Santa

**Version:** 1.0.0  
**Project root:** `D:\Hermes\projects\The-Night-I-Met-Santa`

## Identity & Governance

- **Name:** The-Night-I-Met-Santa
- **Slug:** `the-night-i-met-santa`
- **Type:** Hermes sibling project (gift book — **not** a website profile)
- **OS/Shell:** Windows 10/11 + PowerShell
- **Purpose:** Turn Jack Farrell’s Christmas poem into an 8.5×8.5" illustrated children’s book; print via Lulu; gift for birthday **2026-08-15**

## What this is / isn’t

| Is | Isn’t |
|----|-------|
| Standalone Hermes project with shared skeleton (docs/skills/rules) | JonBeatz personal profile |
| Picture-book + POD print workflow | Next.js / MSC / Hostinger deploy target |
| Isolated Mem0 slug `the-night-i-met-santa` | `jonbeatz_personal` memory |

## Core Connections

- **Shared library:** `D:\Hermes\projects\_core-scripts\shared-profile-content`
- **Image gen (locked lanes):** dial **Klein 4B** (fal or OpenRouter) → fallback **Qwen Image 2** → finals **Gemini 3 Pro Image (OpenRouter)** or **`nano-banana-pro/edit`** + G0 refs — see `BOOK-PRODUCTION-SYSTEM.md` + `IMAGE-LANE-PROMPTS.md`. **Page-by-page** for story finals (no whole-book Klein dumps).
- **Layout:** Pillow pre-composite + Typst front matter (avoid Typst PNG alpha layering)
- **Print:** Lulu 8.5×8.5" (proof paperback → hardcover gift)
- **Playbook:** `.cursor/docs/BOOK-PRODUCTION-SYSTEM.md` (this title) · future books: repo-root **`BOOK-PLAYBOOK.md`**
- **Approved art:** `Media/approved/` two-tier (`style-refs/` moodboard · Tier B print locks) — `INDEX.md`
- **Fonts:** `.cursor/docs/FONT-CATALOG.md` (Cormorant body · Cinzel cover; pack `Xtraz/Fonts/` gitignored)

## Source-of-truth order

1. `TRUTH.md` (this file)
2. `.cursor/docs/START-HERE.md`
3. `.cursor/docs/CONTINUE-HERE.md` — **session continue / next actions**
4. **`.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`** — living ops playbook
5. **`BOOK-PLAYBOOK.md`** — future-book master
6. `.cursor/docs/BOOK-PLAN.md`
7. `Book-Findings.md` — layout experiments + POD research
8. `.cursor/docs/ILLUSTRATION-STYLE.md` / `PAGE-PROMPT-BIBLE.md` / `COVER-PROMPTS.md` / `FONT-CATALOG.md`
9. `.cursor/docs/IMAGE-WORKFLOW.md`
10. `.cursor/docs/MASTER-COMMANDS.md`
11. `.cursor/docs/ReCall.md`
12. Shared TOOLS-* via `.cursor/docs/` mirrors

## Asset locations (root — not under `.cursor/assets`)

- `Media/` · **`Media/approved/`** · `Images/` · `Audio/` · `Transcription/` · `Pages/` · `Output/` · `Xtraz/Fonts/` (local)

## Isolation Rules

- Keep all book assets in this repo (`Media/`, `Pages/`, `Output/`, `Transcription/`).
- Do not mix MSC deploy / Hostinger hPanel work here.
- Mem0 collection: `the-night-i-met-santa_memories` only.

## Layout north star

Reference photos: `Images/references/layout/`  
Reject hard white text boxes (v3) and Typst alpha checkerboards (v4). Prefer organic cloud/watercolor washes or bleed-from-right spreads.

## Illustration style (locked — default look & feel)

**Painted gouache / soft watercolor storybook** — **not** colored pencil, **not** photoreal.  
Canonical prompt kit: **`.cursor/docs/ILLUSTRATION-STYLE.md`**.  
Approved look: `Media/generated/test-batch-v2/` (anchors: style-spread-06 + style-sneak-02).  
Use master style + negatives on every `image:fal:*` call.

---

*Skeleton from shared-profile-content · moved from F: 2026-07-14*
