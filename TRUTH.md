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
- **Image gen (locked lanes):** dial **`fal-ai/flux-2/klein/4b`** → fallback **`fal-ai/qwen-image-2/text-to-image`** → finals **`fal-ai/nano-banana-pro/edit`** + style refs — see `BOOK-PRODUCTION-SYSTEM.md` (§2).
- **Layout:** Pillow pre-composite + Typst front matter (avoid Typst PNG alpha layering)
- **Print:** Lulu 8.5×8.5" (proof paperback → hardcover gift)
- **Playbook:** `.cursor/docs/BOOK-PRODUCTION-SYSTEM.md` — dialed workflow for this book + future titles

## Source-of-truth order

1. `TRUTH.md` (this file)
2. `.cursor/docs/START-HERE.md`
3. `.cursor/docs/CONTINUE-HERE.md` — **session continue / next actions**
4. **`.cursor/docs/BOOK-PRODUCTION-SYSTEM.md`** — **reusable playbook** (tools, decisions, recreate-for-next-book)
5. `.cursor/docs/BOOK-PLAN.md`
6. `Book-Findings.md` — layout experiments + POD research
7. `.cursor/docs/ILLUSTRATION-STYLE.md` / `PAGE-PROMPT-BIBLE.md` / `COVER-PROMPTS.md`
8. `.cursor/docs/IMAGE-WORKFLOW.md`
9. `.cursor/docs/MASTER-COMMANDS.md`
10. `.cursor/docs/ReCall.md`
11. Shared TOOLS-* via `.cursor/docs/` mirrors

## Asset locations (root — not under `.cursor/assets`)

- `Media/` · `Images/` · `Audio/` · `Transcription/` · `Pages/` · `Output/`

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
