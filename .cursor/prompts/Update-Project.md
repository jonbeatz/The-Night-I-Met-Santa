# Update Project — JonBeatz Personal

**Triggers:** `Update Project`, `Sync Project`

Sync tracking docs from recent git activity. Does **not** replace **update docs** (version/CHANGELOG alignment).

---

## Step 1: Detect recent changes

From `D:\Hermes\projects\JonBeatz`:

```powershell
git log --oneline -10
git diff --name-only HEAD~5
git branch --show-current
git rev-parse --short HEAD
```

---

## Step 2: Update `project-log.md`

Append checkpoint:

```markdown
### YYYY-MM-DD — Update Project checkpoint
- **Branch:** [current branch] @ [short sha]
- **Status:** [progress from recent commits]
- **Files changed:** [from git diff]
- **Next:** [inferred next steps]
```

---

## Step 3: Update `Checkpoint.md`

Refresh **Current line** and add milestone row if a release shipped. Do **not** rewrite full history.

| Version | Date | Milestone | Notes |
|---------|------|-----------|-------|

---

## Step 4: Restore-Points (optional)

If a backup or release milestone occurred this session, append to `.cursor/docs/Restore-Points.md`.

---

## Step 5: Summary report

```
-------------------------------------------------------------------------------
PROJECT UPDATE — [date]
-------------------------------------------------------------------------------
project-log.md … checkpoint added
Checkpoint.md … [updated | unchanged]
Branch … [name] @ [sha]
Version … [from package.json]
Build … [npm run build pass/fail if runtime changed]
-------------------------------------------------------------------------------
Project tracking updated. Ready to commit when Jon says so.
-------------------------------------------------------------------------------
```

---

## Rules

- **Do not** auto-commit
- **Do not** modify CHANGELOG.md (releases only — use **update docs**)
- Preserve existing formatting — append only
- Run `npm run build` only if recent commits touched `app/`, `components/`, or `package.json` runtime deps
