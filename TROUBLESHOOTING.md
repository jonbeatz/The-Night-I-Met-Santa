# TROUBLESHOOTING.md — Shared Profile Content Troubleshooting

Top 10 known issues you're likely to hit when bootstrapping or maintaining a project.

## 1. "No messaging platforms enabled" from Telegram gateway

**Symptom:** Telegram gateway starts but can't send/receive messages.

**Cause:** Profile `.env` is missing `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, or `TELEGRAM_ALLOWED_USERS`.

**Fix:**
```powershell
npm run sync:telegram-env   # Push TELEGRAM_ vars from project .env.local → profile .env
npm run telegram:ensure     # Ensure gateway restarts with new env
```

## 2. Mem0 can't connect / "Connection refused"

**Symptom:** `mem0:add` or `mem0:search` fails immediately.

**Causes:**
- Mem0 server not running (starts via Hermes Desktop, not standalone)
- MEM0_API_KEY mismatch between `.env.local` and running Mem0 container
- Qdrant path doesn't exist

**Fix:**
```powershell
npm run mem0:preflight
# Check MEM0_API_KEY, MEM0_USER_ID, MEM0_COLLECTION in .env.local
```

## 3. DeepSeek / LiteLLM won't start

**Symptom:** `deepseek:on` fails silently or starts then stops immediately.

**Causes:**
- DeepSeek API key expired or incorrect in `.env2.local`
- LiteLLM config yaml has stale route
- Port 4000 already in use
- DISABLE_SCHEMA_UPDATE=true not set (tries Postgres that doesn't exist)

**Fix:**
```powershell
npm run deepseek:status    # Check if process is running
npm run deepseek:test      # Verify API key works
# Check .env.local for MSC_LITELLM_MASTER_KEY and DISABLE_SCHEMA_UPDATE
```

## 4. npm scripts that call `_core-scripts` paths fail

**Symptom:** `npm run` commands like `sync:mcp-env` or `telegram:ensure` throw "cannot find path".

**Cause:** Project was bootstrapped but `_core-scripts` is not at `D:\Hermes\projects\_core-scripts\`.

**Fix:** Either:
- Set up `_core-scripts` at the expected location (only if on the same workstation)
- Or override the paths in `package.json` scripts section to point to your local copy

## 5. "git commit" fails with pre-commit hook

**Symptom:** Pre-commit hook runs checks that fail (encoding, linting, etc.).

**Common fixes:**
```powershell
npm run encoding:check     # Fix mojibake before committing
# Or bypass hook (if safe): git commit --no-verify -m "message"
```

## 6. Cursor Agent can't use MCP tools

**Symptom:** MCP tools aren't available in Cursor chat or show "not found".

**Causes:**
- `.cursor/mcp.json` missing or malformed
- Env vars not set (GITHUB_PERSONAL_ACCESS_TOKEN, TAVILY_API_KEY, HOSTINGER_API_TOKEN, etc.)
- Cursor needs to reload (close/reopen project)

**Fix:**
```powershell
npm run sync:mcp-env       # Push MCP vars to .env.local
# Then reload Cursor window
```

## 7. Draven voice doesn't speak

**Symptom:** `npm run draven:speak -- "hello"` returns silently.

**Fix:**
```powershell
# Check OmniVoice daemon:
npm run draven:omni-daemon -Stop   # Stop stale daemon
npm run draven:speak -- "test"     # Starts fresh
# Check .env.local: DRAVEN_VOICE, OMNIVOICE_PYTHON
```

## 8. "Start Project" ritual fails or says nothing

**Symptom:** Agent doesn't respond to "Start Project" with expected status card.

**Cause:** `Start-Project.md` prompt not found at `.cursor/prompts/` or agent didn't read it.

**Fix:** Verify:
```powershell
Test-Path .cursor/prompts/Start-Project.md
# If missing, re-copy from shared-profile-content/prompts/
```

## 9. Repo-Brain.md mentions templates but they don't exist

**Symptom:** Following REPO-BRAIN.md, template files are missing.

**Cause:** Project was set up manually, not via bootstrap script.

**Fix:** Either:
```powershell
# Run the bootstrap script (safe, won't overwrite existing files)
powershell -File D:\Hermes\projects\_core-scripts\shared-profile-content\scripts\bootstrap-new-project.ps1 `
  -ProjectName "MyProject" -ProjectRoot "." -ProjectSlug "myproject" -ProjectDesc "..."
```
Or manually copy from `shared-profile-content/templates/`.

## 10. Docs / encoding corruption in markdown files

**Symptom:** Markdown files show extra characters, garbled text, or BOM issues in git diff.

**Cause:** PowerShell `>` / `Set-Content` defaults to UTF-16 or BOM UTF-8.

**Fix:**
```powershell
npm run encoding:check     # Detect issues
# Always use -Encoding UTF8 with PowerShell file ops
# Or use Python/Node.js for markdown file operations
```

## 11. Gateway keeps retrying a removed messaging platform after clearing .env

**Symptom:** A secondary gateway platform (e.g. Photon iMessage) keeps failing/retrying (`Invalid credentials` 401, reconnect loops) even after you removed all of its `*_*` vars from every `.env`.

**Cause:** Hermes caches platform credentials in **two** places. Beyond the `.env` files, the device token + project secret are stored in `auth.json` under `credential_pool` (`%LOCALAPPDATA%\hermes\auth.json` and `...\profiles\<slug>\auth.json`). Clearing `.env` alone does **not** disable the platform.

**Fix:**
```powershell
# Remove the platform's keys from credential_pool in BOTH auth.json files,
# then restart the gateway. Edit JSON with Python (NOT PowerShell - BOM risk):
python -c "import json,os; p=os.path.expandvars(r'%LOCALAPPDATA%\hermes\auth.json'); d=json.load(open(p,encoding='utf-8')); [d.get('credential_pool',{}).pop(k,None) for k in ('photon','photon_project','photon_user')]; json.dump(d,open(p,'w',encoding='utf-8'),indent=2)"
hermes gateway stop
npm run telegram:gateway
```
Verify the log shows `Gateway running with 1 platform(s)`. Note: a direct console `gateway run` can hang on TTY input — prefer the headless `npm run telegram:gateway` spawn, and kill any orphan sidecar still holding its port (e.g. `:8789`) first.

## 12. n8n still listens on all interfaces after setting N8N_HOST=127.0.0.1

**Symptom:** `Get-NetTCPConnection -LocalPort 5678` shows `LocalAddress ::` or `0.0.0.0` even though `.env` has `N8N_HOST=127.0.0.1`.

**Cause:** On n8n v2, **`N8N_HOST` is for URLs / webhooks** — the socket bind uses **`N8N_LISTEN_ADDRESS`** (default `::`).

**Fix:**
```env
N8N_HOST=127.0.0.1
N8N_LISTEN_ADDRESS=127.0.0.1
```
Restart n8n, then confirm `LocalAddress` is `127.0.0.1`. See `docs/N8N-SETUP.md`.

## 13. n8n Community Edition rejects Execute Command (need process/disk checks)

**Symptom:** Activating a workflow fails with `Unrecognized node type: n8n-nodes-base.executeCommand`.

**Cause:** CE disables shell execution nodes.

**Fix:** Run the Extended Health sidecar and probe it over HTTP:
```powershell
# From shared library (or copy next to your n8n app folder)
$env:EXTENDED_HEALTH_PROFILE = "your-profile-slug"   # optional
& D:\Hermes\projects\_core-scripts\shared-profile-content\scripts\start-extended-health.bat
Invoke-RestMethod http://127.0.0.1:5699/health/extended
```
Wire n8n HTTP Request → `http://127.0.0.1:5699/health/extended`. Full pattern in `docs/N8N-SETUP.md`.

---

## Still stuck?

File an issue or contribute your fix: see `CONTRIBUTING.md`.
