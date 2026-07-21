# Backport Candidates — Shared Skeleton Improvement Queue

When you discover something during a session that could benefit future projects, log it here. At the end of the session (or when you have a few minutes), review and backport.

## Triage criteria

| Include | Skip |
|---------|------|
| New scripts, rules, prompts, skills that are project-agnostic | Project-specific business logic |
| Bugs found in bootstrap/scripts/templates | One-time configuration tweaks |
| Environment variables worth documenting | Personal preferences that won't generalize |
| Missing docs or reference pages | Deprecated/legacy workarounds |
| Workflow improvements to prompts or rituals | Changes requiring bootstrap rewrite |

## Queue

| # | What | Type | Project | Date | Status |
|---|------|------|---------|------|--------|
| 9 | Picture-book **full RECIPE template** + provider/lane priority (fal first · Klein 9B dial → Qwen → 4B light → Gemini finals · Dial D2 vs master · FRAME toggle · don’t mid-paint-crop vignettes) — promote from TNIMS `_RECIPE-TEMPLATE.md` + `IMAGE-LANE-PROMPTS.md` + `BOOK-PLAYBOOK.md` into shared IMAGE-WORKFLOW / book skeleton | docs/templates | The-Night-I-Met-Santa | 2026-07-21 | **pending — after 2–3 more pages** |
| 8 | Picture-book **PAGE-BUILD** master (folder skeleton Media/Images/Xtraz/Output, mocks+RECIPE, PS↔ID parity, Klein Dial D2, MOCK-TYPE roles) — promote from TNIMS `PAGE-BUILD-WORKFLOW.md` + `BOOK-PLAYBOOK.md` into shared docs/templates **after** 2–3 pages dialed | docs/templates | The-Night-I-Met-Santa | 2026-07-20 | **pending — wait until dialed** (refresh lanes 2026-07-21) |
| 3 | Experience Engine layout doc: monolith pages may need inline-style lock when Tailwind v4 layout refactors fail repeatedly; pair with project-local layout skill | docs/skill | DigitalStudioz | 2026-07-03 | pending |

## Completed

| # | What | Version | Date |
|---|------|---------|------|
| 7 | Picture-book fal model-lane recipe (Klein dial → Qwen fallback → Banana finals) in shared IMAGE-WORKFLOW | 1.31.5 | 2026-07-15 |
| 6 | Extended Health sidecar: system Python launcher (not Hermes venv) for `hermes update` safety | 1.29.2 | 2026-07-11 |
| 5 | End Project clickable AskQuestion UX (`end-project-ritual.mdc`, Hard UI rule, never Reply 1/2) | 1.29.1 | 2026-07-11 |
| 4 | n8n `N8N_LISTEN_ADDRESS` gotcha + Extended Health sidecar pattern (CE no Execute Command) | 1.29.0 | 2026-07-11 |
| 2 | DigitalStudioz gaps: env merge, Hostinger/GitHub docs, sync-mcp-env wrapper, repair script, universal doc copy in bootstrap | 1.12.0 | 2026-07-03 |
| 1 | Premium scroll toolkit: Lenis provider, GSAP scroll hook, CustomCursor, StudioRails | 1.8.0 | 2026-06-29 |
| 2 | TROUBLESHOOTING #11: removed gateway platform retries due to auth.json credential_pool cache (Photon gotcha) | 1.9.0 | 2026-06-29 |
|   |      |         |      |
