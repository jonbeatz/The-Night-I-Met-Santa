# Release Version — JonBeatz GitHub Tag + Release

**Triggers:** `release version`, `publish release`, `tag and release`, after version bump on milestone branch

---

## Prerequisites

- Version bumped in **`package.json`** (source of truth)
- **CHANGELOG.md** entry added (`.cursor/docs/CHANGELOG.md`)
- **HISTORY.md** + **ReCall.md** updated
- Branch pushed to `origin`

---

## Steps (agent runs all)

```powershell
cd D:\Hermes\projects\JonBeatz

# 1. Sync README badges, TRUTH, MASTER-COMMANDS from package.json
npm run version:sync

# 2. Docs alignment audit
npm run docs:sync

# 3. Commit if sync changed files (ask Jon unless already requested)

# 4. Push branch (if not already)
git push -u origin HEAD

# 5. Publish tag + GitHub release (--latest)
npm run release
```

---

## What gets updated automatically

| Target | Source |
|--------|--------|
| Git tag `vX.Y.Z` | `package.json` version |
| GitHub Release (Latest) | `gh release create` |
| README version badge | `sync-version.ps1` |
| README release badge | `JonBeatz-Command-Center` repo slug |
| TRUTH.md version line | `sync-version.ps1` |

---

## Pitfalls

- **Wrong repo in badges** — must be `jonbeatz/JonBeatz-Command-Center`, not `jonbeatz/jonbeatz`
- **Tag without release** — always run `npm run release`, not manual tag only
- **Uncommitted changes** — commit before release for clean tag SHA

---

## Mem0 (optional)

```powershell
npm run mem0:add -- "Released JonBeatz vX.Y.Z on branch {branch}: {one-line summary}"
```
