# SKILL-INDEX.md — Shared Domain Skills

Searchable catalog of all portable skills available in `shared-profile-content/skills/`. Each skill includes domain tags so you can `rg "tag" SKILL-INDEX.md` to find the right one.

## Design & UI

| Skill | Tags | Purpose | Source |
|-------|------|---------|--------|
| frontend-design | design, anti-slop, aesthetic, typography, brief | **Anthropic's canonical anti-slop design brief** (vendored) — distinctive aesthetic direction, palette/type/signature planning, self-critique. Read first, then apply project tokens. | anthropics/skills |
| NovaMira-Design | design, dark-theme, bento, glass, saas, grid | Glassmorphism SaaS design system — dark layered neutrals, Studio Gold (#F5B841), 8px rhythm | JonBeatz |
| MSC-UI-Taste | ui, audit, quality, motion, anti-slop | Anti-slop UI taste layer — audit workflow, motion philosophy, quality gate for generated code | JonBeatz |
| Premium-UI | ui, components, shadcn, animation, micro-interactions | Pre-wired premium component techniques — shadcn registries, micro-interactions, physics animations | JonBeatz |
| Component-Registries | ui, shadcn, registry, aceternity, magicui, cultui, cli | 2026 shadcn ecosystem map — which registry for what, CLI namespaces, official shadcn skill install, Tailwind v4 | Core |
| DesignMD | design, extraction, cli | Design system extraction from live URLs via @designmdcc/cli | JonBeatz |
| Design-Engineer | design, audit, rubric, screenshot, oklch, anti-slop, polish | Playwright visual feedback loop + design canon — premium polish after scroll/3D builds | SolPowa/vault |
| Nova | css, tokens, grid, namespace, cinematic | CSS conventions — jb-/nm- namespaces, Studio Gold tokens, cinematic 16:9 grids | JonBeatz |

## Motion & Interaction

| Skill | Tags | Purpose | Source |
|-------|------|---------|--------|
| Scroll-Motion | scroll, gsap, lenis, scrolltrigger, splittext, parallax, pin | 2026 scroll stack — Lenis + GSAP + **parallax playbook** + `ParallaxStack.tsx` + CSS scroll()/view() | Core |
| Scroll-Video-Sequence | scroll, video, canvas, frame-scrub, apple, ffmpeg, cinematic, loader, hash | Canvas image-sequence hero — WebP FFmpeg, progressive loader gate, hash chapters, `ScrollFrameHero.tsx` template | Core |
| 3d-scroll-website | scroll, canvas, frame-sequence, devini, neumorphic, agency | Devini Labs full pipeline — Next.js frame-sequence hero, Lenis, section architecture; vault at `assets/3d-web-workflows` | Devini/vault |
| View-Transitions | transitions, view-transitions-api, morph, spa, nextjs, routing | Native page/state morph animations (0kb JS) — shared-element morphs, route transitions, Next.js + React 19, reduced-motion | Core |
| Motion-Accessibility | a11y, prefers-reduced-motion, performance, cwv, safety-gate | Reduced-motion across CSS/motion/GSAP/Lenis + Core Web Vitals budget for heavy scroll/3D. The safety gate for every motion-heavy build. | Core |

## 3D & WebGL

| Skill | Tags | Purpose | Source |
|-------|------|---------|--------|
| 3D-Website-Fusion | 3d, website, fusion, production, scroll, color-shift, particles | **Master fusion skill** — combines Three.js + scroll + particles + wireframe core + color-shift + glassmorphism CSS portal into one production 3D website | JonBeatz |
| Three.js-Ops | 3d, threejs, r3f, webgl, scene, lighting | Three.js/R3F scene setup, lighting, GLTF/GLB loading, animation | JonBeatz |
| WebGL-UI | 3d, webgl, shader, effects, post-processing | Shader effects, post-processing, interactive 3D UI components | JonBeatz |
| 3D-Modeling | 3d, gltf, glb, optimization, animation | GLTF/GLB loading, optimization, animation for web | JonBeatz |
| 3D-Scroll | 3d, scroll, parallax, gsap, transitions | Scroll-triggered 3D transitions, parallax effects, GSAP-style motion | JonBeatz |
| GLB-Asset-Sourcing | 3d, assets, sourcing, licensing, glb, hdr, environment | Finding, downloading, validating free GLB models + HDR environment maps — sources, licenses, file validation | VaderLabz |
| R3F-Gotchas | 3d, r3f, troubleshooting, bugs, workarounds, threejs | Known React Three Fiber issues — EffectComposer crash, Float deadlock, GLB rendering, Canvas positioning | VaderLabz |

## Git & DevOps

| Skill | Tags | Purpose | Source |
|-------|------|---------|--------|
| GitHub-Ops | git, github, repo, automation, api | GitHub API operations, repo management, content fetching, discovery | JonBeatz |
| Hostinger-Ops | hosting, hostinger, deploy, ftp, ssh, mcp | Hostinger deploy operations — hPanel restart, two-folder model, MCP quartet, profile boundary | JonBeatz |

## Workflow & Operations

| Skill | Tags | Purpose | Source |
|-------|------|---------|--------|
| Workflow-Portable/Workflow-Ops | workflow, triggers, commands, operating-model | Trigger-command operating model — natural language to agent actions | MSC |
| Workflow-Portable/Checkpoint-Restore | backup, restore, git, milestone | Restore-point format and branch-cut ritual for project checkpoints | MSC |
| Workflow-Portable/Deploy-FTP-Node | deploy, ftp, node, ssh, hosting | Golden split — local build then server restart. Deploy workflow for Node apps | MSC |
| Workflow-Portable/Docs-Governance | docs, sync, version, audit | Source-of-truth order, drift audits, doc sync governance | MSC |
| Workflow-Portable/Session-Closeout | session, closeout, deploy, wrap-up | End-of-session ritual with optional deploy step | MSC |
| Workflow-Portable/Deploy-Profile-Package | deploy, preflight, build, upload, verify | Repo-first deploy workflow — preflight, build, upload, restart verification | MSC-Projectz |
| Workflow-Portable/Session-Handoff-Restore | handoff, restore, closeout, checkpoint | Unified closeout + checkpoint workflow with handoff notes | MSC-Projectz |

## Code & Automation

| Skill | Tags | Purpose | Source |
|-------|------|---------|--------|
| UI-Generator | ui, components, shadcn, ai-sdk, nextjs | Expert UI component generator — Cult UI, AI SDK patterns, Next.js 16 + Tailwind v4 | Node-Launcher-v2 |
| Git-Commit | git, commit, conventional, format | Conventional commits format (`type(scope): subject`) skill | Node-Launcher-v2 |
| imported/CURATED-INDEX | reference, index, whitelist | Curated whitelist of 15 approved external skill categories for manual sourcing | MSC |
| Nextjs-Tailwind-Bootstrap | nextjs, tailwind, tailwind-v4, bootstrap, setup, postcss, css | Tailwind CSS **v4** setup checklist for skeleton-bootstrapped projects — install, config, verification, troubleshooting | VaderLabz |

## Automation & Integration

| Skill | Tags | Purpose | Source |
|-------|------|---------|--------|
| Google-Workspace | google, gmail, calendar, drive, automation | Google automation via Hermes — Gmail, Calendar, Drive operations | JonBeatz |
| Image-Workflow | image, hf, comfyui, genai, upscale, video | HF cloud generation + ComfyUI local edit/upscale/video pipeline | JonBeatz |
| Background-Removal | image, processing, rembg, u2net, python | AI background removal with rembg + U^2-Net — transparent PNG pipeline, CLI tool | VaderLabz |
| **Photoshop-Layer-Export** | photoshop, layers, export, jpg, psb, adobepy, book-refs | **Solo-eyeball export:** each layer → named JPG via adobepy (`npm run ps:export-layers`) | The-Night-I-Met-Santa |

## GitHub & Docs

| Skill | Tags | Purpose | Source |
|-------|------|---------|--------|
| GitHub-README-Template | github, readme, badges, template, docs | Standard GitHub README template with shields.io badges, status table, comparison table, screenshots. References D:\Hermes\projects\JonBeatz\README.md as canonical format. | VaderLabz |

---

## How to use a skill

Skills are read by the AI agent when relevant to the current task. To invoke a skill:

1. Find the right skill using this index
2. The agent reads `skills/<skill-path>/SKILL.md` for instructions
3. Follow the workflow steps inside the skill file

## Keeping skills in sync (single source of truth)

This folder (`_core-scripts/shared-profile-content/skills/`) is the **canonical library**. Projects get copies at bootstrap, then stay current with a one-command pull — no more hunting through old projects:

```powershell
npm run sync:skills          # pull latest shared skills into THIS project's .cursor/skills
npm run sync:skills -- -DryRun   # preview changes, write nothing
npm run sync:skills:global   # (JonBeatz hub) install into ~/.claude/skills — global to every project + Cursor/Claude
```

- **Non-destructive:** shared skills are refreshed from the library; **project-unique** skills (e.g. `digitalstudioz-layout`) are never touched.
- **Auto-refresh:** `sync:skills` runs automatically at **Start Project** (via `session-start.ps1`; pass `-SkipSkills` to opt out), so every session begins with the latest library.
- **Authoring flow:** edit/add a skill *here* in the library → run `sync:skills` in each project (and `sync:skills:global` once) → commit. Never edit a skill only inside a single project.

### Docs sync (same idea, for the universal docs)

The `docs/` folder here is the canonical set of universal docs. Refresh a project's `.cursor/docs` copies with:

```powershell
npm run sync:docs            # PREVIEW - list universal docs that differ from the library
npm run sync:docs -- -Write  # apply refreshes, then review `git diff`
npm run sync:docs -- -Write -AddMissing   # also add universal docs not present yet
```

- **Placeholder-aware:** re-substitutes each project's values (`The-Night-I-Met-Santa`, `THE_NIGHT_I_MET_SANTA`, `D:\\Hermes\\projects\\The-Night-I-Met-Santa`, `The-Night-I-Met-Santa` from git remote, etc.). Non-derivable values live in `.cursor/docs/.docsync.json` (e.g. `PROFILE_DESCRIPTION`).
- **Guarded + safe:** a doc with any unresolved placeholder is skipped, never written half-baked; preview-by-default; docs are git-tracked so `-Write` is always recoverable. Local doc edits show up in `git diff` — review before committing.

## Adding a new skill

See `CONTRIBUTING.md` for the workflow to contribute new skills back to the shared library.
