# START HERE — The-Night-I-Met-Santa Daily Ops

If an agent is new to this profile, read this file first.

**Profile root:** `D:\Hermes\projects\The-Night-I-Met-Santa`  
**Hermes slug:** `the-night-i-met-santa`  
**Kind:** Gift children’s book (Jack Farrell) — print via Lulu, birthday Aug 15

> **Book handoff:** After this file, always read **`.cursor/docs/CONTINUE-HERE.md`** and **`.cursor/docs/ReCall.md`**.

## Operator Profile

- **Operator:** Jon
- **Handshake (required):**
  - Startup: **"Ok Jon — The-Night-I-Met-Santa profile loaded, ready."**
  - Closeout: **"Great work Jon — session saved."**

---

## Source-of-Truth Order

When docs differ, use this priority:

1. `TRUTH.md` — Project constitution (gift book, not a website)
2. **Always-open book stack (4):**
   - `.cursor/docs/JON-BOOK-FLOW-v2-FINAL.md`
   - `.cursor/docs/MASTER-PRODUCTION-DOCK.md`
   - `.cursor/docs/IMAGE-LANE-SYSTEM-v2.md`
   - `AGENT-RUNBOOK.md`
3. `Media/generated/mocks/_FLOW-CURRENT.json` — current plate paths + verdicts (`decided_by` + `date`)
4. `START-HERE.md` (this file)
5. **`CONTINUE-HERE.md`** — where we are + what to do next
6. Everything else = **reference** (PAGE-BUILD, ISSUES-RESOLVED, ILLUSTRATION-STYLE, BOOK-PLAYBOOK, fleet mirrors) — open only when needed

> **Book handoff:** After this file, read **CONTINUE-HERE** + **ReCall**, then the four always-open docs. Do not auto-load the full historical stack.

**Shared canonical (fleet tools):** `D:\Hermes\projects\_core-scripts\shared-profile-content\docs\TOOLS-*.md`

---

## Start Project (cold boot)

Say **Start Project** or **Cold Start**.

**Agent must:**
1. Run `npm run session:start -- -Full` from profile root (auto-launches LM Studio if offline, starts DeepSeek + ngrok)
2. Run `npm run mem0:preflight` → if offline, alert operator to start LM Studio manually
3. Run `npm run mem0:search -- "test"` as smoke test → if fails, ask operator to load `qwen3-4b-instruct-2507` in LM Studio GUI
4. Read `TRUTH.md`, this file, and `ReCall.md`
5. Search Mem0 for "current priorities"
6. Print session status card (ports, services, Mem0)

---

## Open Project (resume — keep fleet)

Say **Open Project** or **Resume Session** when switching into this workspace (LiteLLM/ngrok may already be up).

**Agent must:**
1. Run `npm run session:open` (light probes only — no `-Full`)
2. Read `TRUTH.md`, this file, and `ReCall.md`
3. `npm run mem0:search -- "current priorities"`
4. Print status card — **no** `draven:speak`

---

## Close Project (switch away — keep fleet)

Say **Close Project** or **Close Session** when leaving this folder for another Hermes project.

**Agent must:**
1. Summarize + update `ReCall.md` and `project-log.md` (note fleet left running)
2. Mem0 + `npm run session:handoff`
3. **AskQuestion** for git — never auto-commit
4. **Do not** run `session:stop` or `draven:speak`
5. **Do not** stop dev on `:3000` unless operator is quitting Cursor — another project uses `:3001` if `:3000` is busy

---

## End Project (day-end)

Say **End Project**, **End Session**, or **Done for today**.

**Agent must:**
1. Summarize what was done
2. Update `ReCall.md` and `project-log.md`
3. Mem0 + vault
4. **AskQuestion** for git, then **AskQuestion** to stop dev on **:3000** when listening (recommend stop before quitting Cursor), then **AskQuestion** for stop LiteLLM + ngrok (recommend stop)
5. `draven:speak` farewell, then `npm run session:stop` (with `-StopDeepSeek` if confirmed)

**LM Studio:** Keep **off** Windows Startup autostart. `session:start -- -Full` launches when needed. See `FLEET-BOOT-SESSION.md`.

---

## Local Services

| Service | URL |
|---------|-----|
| LiteLLM (paid) | http://localhost:4000 |
| LM Studio (free) | http://localhost:1234 |
| ngrok inspector | http://localhost:4040 |

---

## Mem0 Quick Reference

```powershell
npm run mem0:preflight   # Verify LM Studio
npm run mem0:search -- "query"
npm run mem0:add -- "text to remember"
npm run mem0:list
```

Default model: **qwen3-4b-instruct-2507** @ LM Studio `:1234`
Collection: `the-night-i-met-santa_memories`

---

## Environment Variables

See `ENV-VARS-REFERENCE.md` for the full registry of env vars this profile uses. Key vars are set in `.env.local`.

---

## Fitness Check

To check if this project is missing shared skeleton features:

```powershell
powershell -File D:\Hermes\projects\_core-scripts\shared-profile-content\scripts\check-shared-version.ps1
```

Or read `D:\Hermes\projects\_core-scripts\shared-profile-content\docs\FITNESS-CHECK.md` for the full checklist.

## Docs & UTF-8 Hygiene

Before doc commits:

```powershell
npm run encoding:check   # mojibake scan
npm run docs:sync        # alignment audit
```

Never bulk-rewrite markdown from PowerShell without `-Encoding UTF8`.

---

*Created: 2026-07-14*
