# Hostinger MSC Deploy — workspace switch ritual

**Triggers:** `push it live`, `deploy website`, `deploy msc`, `hostinger deploy`, `go live mystudiochannel`

**Read first:** `.cursor/docs/HOSTINGER-REFERENCE.md` · `.cursor/skills/Hostinger-Ops/SKILL.md`

---

## Phase 0: Confirm workspace

1. Check current repo root.
2. If **not** `D:\Cursor_Projectz\MyStudioChannel`:
   - Tell Jon: deploy scripts live in MSC — open that workspace (or confirm switch).
   - From JonBeatz you may still: `npm run sync:mcp-env` (Hostinger MCP token) and read reference docs.
3. If MSC repo is open → continue.

---

## Phase 1: Deploy mode (AskQuestion)

Use **AskQuestion** — one step at a time (per `interactive-workflows.mdc`):

| Option | MSC command |
|--------|-------------|
| **Quick DB** (recommended when APIs 500) | `npm run msc:push:db:live` |
| **Fast FTPS** (daily code/UI) | `npm run pushit:live:fast` |
| **Fast + DB** | `npm run pushit:live:fast -- -WithDb` |
| **Full FTPS** | `npm run pushit:live` |
| **Diagnose only** | `npm run msc:hostinger:deploy-diagnose` |

**Avoid:** MCP zip deploy (`hosting_deployJsApplication` zip) unless Jon explicitly overrides — see `PITFALLS-HOSTINGER.md`.

Full ritual detail: `{{MSC_WORKSPACE}}\.cursor\prompts\Push-Website-Live.md`

---

## Phase 2: Execute (MSC repo root)

Run selected command from `D:\Cursor_Projectz\MyStudioChannel`. Report progress; do not skip sync steps.

---

## Phase 3: hPanel restart (required)

**Live (Hostinger hPanel):** [https://hpanel.hostinger.com/](https://hpanel.hostinger.com/)

Jon restarts Node.js app (or agent reminds with explicit link).

---

## Phase 4: Verify

```powershell
cd D:\Cursor_Projectz\MyStudioChannel
npm run msc:verify:live
```

Optional: `npm run msc:verify:live:version`

---

## Rules

- Do **not** run MSC deploy from JonBeatz `package.json` (scripts not wired here)
- Do **not** auto-commit
- Log incidents to MSC `ISSUES-RESOLVED.md` or JonBeatz `log:fix` if lesson applies globally
