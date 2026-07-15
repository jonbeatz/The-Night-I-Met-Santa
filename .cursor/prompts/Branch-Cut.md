# Workflow: JonBeatz Branch Cut + Version Bump

When the user says **"branch cut"**, **"cut JonBeatz-Project-vN"**, **"cut new development branch"**, or **"Lets Cut New Branch"** (full ritual — not a bare `git checkout -b`):

**Profile root:** `D:\Hermes\projects\JonBeatz`  
**Related:** `.cursor/prompts/Release-Version.md` · `.cursor/docs/VERSION-RELEASE.md`

---

## Triggers

| Say this | Action |
|----------|--------|
| **"branch cut"**, **"cut development branch"** | Full ritual below; infer next N from current branch (e.g. v4 active → cut **v5**) |
| **"Cut JonBeatz-Project-v5"** (explicit N) | Full ritual for that branch name |
| **"Lets Cut New Branch"** | Same full ritual |

**Do not** stop after `git checkout -b` alone — that leaves GitHub Releases, README Current Status, TRUTH, and Restore-Points out of sync.

**`main` stays untouched** unless Jon explicitly asks to merge a milestone branch.

---

## Phase 0: Preflight

1. **Local (JonBeatz root):** `git status -sb` — working tree must be clean or user-approved commit first.
2. **Record freeze line:** Note current active branch + short SHA (e.g. `JonBeatz-Project-v4` @ `cb94dd3` → will freeze).
3. **Backup (recommended):** `npm run backup:quick` — report folder under `G:\Hermes_Project_BackUpz\JonBeatz\`.
4. **Parse target:** Branch `JonBeatz-Project-v{N}` → version **`N.0.0`** → tag **`vN.0.0`**.

---

## Phase 1: Create branch

**Local:**

```powershell
cd D:\Hermes\projects\JonBeatz
git fetch origin
git checkout JonBeatz-Project-v{prev}    # current active line, clean HEAD
git pull
git checkout -b JonBeatz-Project-v{N}
```

Confirm: `git branch --show-current` → `JonBeatz-Project-v{N}`.

---

## Phase 2: Governance (before or alongside bump)

Edit (do **not** skip):

| File | Update |
|------|--------|
| **`package.json`** | `"version": "N.0.0"` |
| **`.cursor/docs/CHANGELOG.md`** | New `N.0.0` section (kickoff / branch cut) |
| **`.cursor/docs/Checkpoint.md`** | New milestone row; update **Current line** |
| **`.cursor/docs/Restore-Points.md`** | New row **`RP-YYYY-MM-DD-vN-start`** with frozen + active restore commands |
| **`TRUTH.md`** | Version line → **N.0.0**; note active branch + frozen branch @ `<short-sha>` |
| **`ReCall.md`** + **`project-log.md`** | Branch-cut session note |
| **`HISTORY.md`** | Milestone entry when substantial (optional on pure kickoff) |

---

## Phase 3: Version sync + GitHub Release

**Local:**

```powershell
npm run version:sync
npm run encoding:check
npm run docs:sync

git add -A
git commit -m "chore: cut JonBeatz-Project-v{N} — bump to N.0.0"
git push -u origin JonBeatz-Project-v{N}
npm run release
```

`npm run release` must create tag **`vN.0.0`** and GitHub Release with **`--latest`**.

Use **`npm run release -- -SkipPush`** only when branch is already pushed and you need tag/release only.

---

## Phase 4: Post-bump verification

1. **Checkpoint audit:** `.cursor/docs/Checkpoint.md` — frozen branch rows must name the correct prior line (no global replace corruption).
2. **Docs gate:** `npm run docs:sync` must exit **0** — README Current Status table must match `package.json`.
3. **GitHub check (report to user):**
   - [Releases](https://github.com/jonbeatz/JonBeatz-Command-Center/releases) → **vN.0.0** shows **Latest**
   - [README](https://github.com/jonbeatz/JonBeatz-Command-Center) → Current Status **vN.0.0**
4. **Optional:** **"update docs and mem0"** — Mem0 memories for branch cut + restore SHAs.

---

## Phase 5: Closeout report

Print:

```
JonBeatz-Project-v{N} branch cut complete
  Active:  JonBeatz-Project-v{N} @ <sha>
  Frozen:  JonBeatz-Project-v{prev} @ <freeze-sha>
  Version: N.0.0  |  Tag: vN.0.0  |  GitHub Latest: vN.0.0
  Live:    jon-beatz.com / jonbeatz.dev unchanged until site:package deploy
  Restore frozen: git fetch origin && git checkout JonBeatz-Project-v{prev} && git reset --hard <freeze-sha>
```

---

## Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Tag shows v5 but Releases sidebar still v4 | Tag pushed without `gh release create --latest` | Run `npm run release` |
| README badge v5, table still v4 | Skipped `version:sync` | Run `npm run version:sync` then `docs:sync` |
| Checkpoint milestones all same branch | Careless global branch replace | Scoped edits only; audit after bump |
| Wrong robocopy restore path | Legacy `D:\Hermes\JonBeatz` | Use `D:\Hermes\projects\JonBeatz` |

---

## Related commands

| Command | Purpose |
|---------|---------|
| `npm run backup:quick` | Pre-cut backup |
| `npm run version:sync` | README badges, TRUTH, MASTER-COMMANDS |
| `npm run docs:sync` | Docs alignment audit |
| `npm run release` | Tag + GitHub release (`--latest`) |
