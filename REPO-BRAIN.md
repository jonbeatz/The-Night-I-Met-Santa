# How to Start a New Project — Full Workflow

This guide walks you through creating a new project with the full shared brain
from `_core-scripts/shared-profile-content/` in 5 minutes.

---

## 1. The Shared Brain

All reusable artifacts live at:
**`D:\Hermes\projects\_core-scripts\shared-profile-content\`**

This is the **central source of truth** for every project. Update shared improvements
here first, then backport to existing projects.

| Folder | Contents |
|--------|----------|
| `templates/` | TRUTH, START-HERE, AGENTS, REPO-BRAIN, package.json, .cursorrules, backup script |
| `skills/` | Domain skills (design, 3D, git, deploy, automation) |
| `prompts/` | Session rituals (Start, End, Update, Release, Branch-Cut) |
| `rules/` | Shared .mdc rules (voice, mem0, workflow, image, checkpoint, etc.) |
| `docs/` | Universal references (MEM0, IMAGE, VOICE, TELEGRAM, ENGINEERING, INFRASTRUCTURE, PROJECT-STRUCTURE) |
| `scripts/` | Shared PowerShell/Node utilities |
| `mcp.json` | Canonical MCP server config |

## 2. Bootstrap a New Project (Automated)

Run this single command from anywhere:

```powershell
powershell -File D:\Hermes\projects\_core-scripts\shared-profile-content\scripts\bootstrap-new-project.ps1 `
  -ProjectName "MyNewApp" `
  -ProjectRoot "D:\Hermes\projects\MyNewApp" `
  -ProjectSlug "mynewapp" `
  -ProjectDesc "A new project"
```

**What it does:**
- Creates the project directory
- Copies and templatizes all 5+ skeleton files (TRUTH, START-HERE, AGENTS, REPO-BRAIN, package.json, .cursorrules, backup script)
- Creates `.cursor/` structure (rules, prompts, docs, skills)
- Copies all shared rules, prompts, skills, MCP config
- Creates session docs (ReCall.md, project-log.md)
- Initializes git with first commit
- Creates the backup root at `G:\Hermes_Project_BackUpz\MyNewApp\`
- Injects `scripts/project-backup.mjs` — ready for `npm run backup:quick`

## 3. The Standard Project Layout

Every project in the ecosystem follows this structure:

```
MyNewApp/
├── TRUTH.md              # Constitution
├── START-HERE.md         # Daily ops
├── AGENTS.md             # Agent orientation
├── REPO-BRAIN.md         # This file — onboarding guide
├── package.json          # npm scripts
├── .cursorrules          # Workspace rules
├── .env.local            # Secrets (gitignored)
├── scripts/
│   ├── project-backup.mjs  # Backup caller (from template)
│   └── ...                  # Project-specific scripts
└── .cursor/
    ├── rules/            # Shared rules
    ├── prompts/          # Session rituals
    ├── docs/             # Project docs + ReCall.md
    └── skills/           # Domain skills
```

## 4. Backup Convention

Every project has its own backup directory:
`G:\Hermes_Project_BackUpz\<ProjectName>\`

Folders are sequential: `<project-slug>-v1-a`, `v1-b`, ... `v1-z`, `v2-a`.

```powershell
npm run backup:quick    # Standard backup, no prompts
npm run backup:full     # Full mirror (includes node_modules)
npm run backup:clean    # Keep 10 newest backups
```

See `PROJECT-STRUCTURE.md` for the full ecosystem reference.

## 5. After Bootstrap — First Session

1. Open the project in Cursor
2. Say **"Start Project"** — the agent will read TRUTH, START-HERE, and ReCall
3. The project is immediately ready with all shared skills, rules, prompts, and docs
4. Add project-specific `.cursorrules` overrides, custom npm scripts, and env vars as needed

## 6. Staying in Sync

When `shared-profile-content` gets improvements (new skills, updated rules, better docs):

```powershell
# Option A: Re-copy shared artifacts (overwrites, re-applies your overrides manually)
Copy-Item -Path D:\Hermes\projects\_core-scripts\shared-profile-content\rules\*.mdc -Destination .cursor\rules\

# Option B: Selective cherry-pick (recommended)
Copy-Item -Path D:\Hermes\projects\_core-scripts\shared-profile-content\skills\NewSkill -Destination .cursor\skills\ -Recurse
```

See `CONTRIBUTING.md` in shared-profile-content for backport workflow.
