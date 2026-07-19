# Layout MCP setup — Affinity + InDesign (TNIMS)

**Project:** `D:\Hermes\projects\The-Night-I-Met-Santa`  
**Cursor config:** `.cursor/mcp.json` (this repo)  
**Cloned tools:** `tools/layout-mcp/`  
**Status date:** **2026-07-19 — LIVE / smoke-tested**

---

## Status

| Server | Wired in mcp.json | Status |
|--------|-------------------|--------|
| **affinity** | Yes | **READY** — Affinity open + MCP all ON · `:6767` · Cursor shows ~11 tools |
| **indesign-uxp** | Yes (primary) | **READY** — bridge `:19300/:19301` + UXP plugin **Connected ✓** · ~135 tools |
| **indesign-exec** | Yes (fallback) | COM historically fails — prefer **indesign-uxp** |

Ports **19300/19301** are intentional — classic UXP samples use 3000/3001 which collide with Next.js / Hermes web apps.

UDT **Service Port** on this PC: **14001** (Preferences in Adobe UXP Developer Tools).

### Creative Cloud Desktop — keep installed (2026-07-19)

**Do not uninstall** Adobe Creative Cloud Desktop while keeping InDesign / UXP Developer Tools.

| Action | OK? | Why |
|--------|-----|-----|
| Uninstall Creative Cloud Desktop | **No** | Adobe requires CC hub for licensing/updates of remaining CC apps; uninstaller expects other apps gone first |
| Keep InDesign + UDT + Bridge | **Yes** | What we need for MCP |
| Disable **Creative Cloud.exe** in Task Manager → Startup apps | **Yes** | Stops ~450MB+ background helpers from auto-starting |
| Quit Creative Cloud when **fully idle** (no UDT load needed) | **Yes** | Free RAM |
| Load / Watch InDesign Bridge in UDT | **Needs CC signed in** | Cold test 2026-07-19: UDT shows **Sign-In Required** if CC Desktop is closed — “sign-in to CreativeCloud Desktop … then relaunch UXP Developer Tools.” Plugin stays **Not loaded** until then |

**Practical session:** **Creative Cloud Desktop must be running and signed in** before UDT can Load/Watch (web adobe.com login is **not** enough — proven 2026-07-19).  

**Agent gate:** Do **not** launch UDT on process heuristics alone (CC window + Desktop Service can appear **before** Jon finishes sign-in → UDT **Sign-In Required**). Wait until Jon confirms **fully logged into Creative Cloud Desktop**, *then* UDT → Load & Watch → InDesign → Bridge Connected. Startup disable for CC is still OK; bring CC up only for DTP sessions.

Affinity is **not** Creative Cloud (Canva/Affinity WindowsApps) — independent of CC.

---

## One-time setup (DONE 2026-07-19)

1. Installed **Adobe UXP Developer Tools** (Creative Cloud) — v2.2.1.2  
2. **Add Plugin** →  
   `D:\Hermes\projects\The-Night-I-Met-Santa\tools\layout-mcp\indesign-uxp-server\plugin\manifest.json`  
3. State **Watching** · Load Successful · id `com.ads.indesign-bridge`  
4. InDesign → Bridge Panel → **Connected to bridge ✓**  
5. Cursor MCP reloaded — `affinity` + `indesign-uxp` + `indesign-exec` green

### Can we use adobe-uxp/devtools-cli?

**No for InDesign.** Host matrix = Photoshop + XD; Node 24 install fails. Use **UDT GUI** only. Clone under `tools/layout-mcp/devtools-cli/` is reference-only.

---

## Proven cold-start workflow (2026-07-19 FINAL)

Do this in order. Skipping or rushing CC sign-in breaks UDT.

| Step | Who | Action |
|------|-----|--------|
| **1** | Agent | Launch `Creative Cloud.exe` (`C:\Program Files\Adobe\Adobe Creative Cloud\ACC\Creative Cloud.exe`) |
| **2** | **Jon** | Sign in fully until normal CC Desktop home shows. Reply **logged in** (or confirm in chat). |
| **3** | Agent | **WAIT** — do **not** start UDT on process heuristics (CC window + Desktop Service can appear *before* sign-in finishes → **Sign-In Required**). |
| **4** | Agent | Launch UDT + InDesign + `npm run layout:indesign-bridge` (`:19300/:19301`) |
| **5** | **Jon** | In UDT → **Load & Watch** on InDesign Bridge (`com.ads.indesign-bridge`). Agent **cannot** click this (Electron UI — UIA/coords fail). |
| **6** | Jon / auto | InDesign **Bridge Panel** → **Connected to bridge ✓** |
| **7** | Agent | MCP smoke (`create_document` 8.5×8.5" etc.) |

### What does NOT work

| Attempt | Result |
|---------|--------|
| adobe.com / Brave web login only | **Fail** — UDT still Sign-In Required |
| Uninstall Creative Cloud Desktop | **No** — keep installed for licensing |
| Agent auto-click Load & Watch | **Fail** — Electron; Jon must click |
| Launch UDT before Jon confirms CC signed in | **Fail** — Sign-In Required |

### What DOES work (trim RAM)

- Disable `Creative Cloud.exe` in Task Manager → Startup apps  
- Bring CC Desktop up only for DTP sessions  
- After Bridge Connected, quitting big CC UI may be OK until next cold Load  

### Agent launch paths

```powershell
# After Jon confirms CC Desktop signed in:
npm run layout:indesign-bridge
# UDT:  C:\Program Files\Adobe\Adobe UXP Developer Tools\Adobe UXP Developer Tools.exe
# ID:   C:\Program Files\Adobe\Adobe InDesign 2026\InDesign.exe
# CC:   C:\Program Files\Adobe\Adobe Creative Cloud\ACC\Creative Cloud.exe
```

Affinity: Edit → Settings → Model Context Protocol → all ON (already set). Independent of Creative Cloud.

---

## Affinity usage notes

1. Affinity must be running for `:6767` / MCP tools  
2. `execute_script` requires reading SDK **preamble** first (`read_sdk_documentation_topic`)  
3. Use `console.log` — scripts don’t return values otherwise  
4. `render_spread` needs `document_session_uuid`  
5. Best for polish on an existing doc — weak for inventing a full book from scratch  

Optional:

```powershell
cd tools\layout-mcp\affinity-scripting
npx @modelcontextprotocol/inspector --sse http://127.0.0.1:6767/sse
node extract_docs.js
```

---

## InDesign UXP usage notes

1. Bridge must listen on **19300/19301** (`npm run layout:indesign-bridge`)  
2. Plugin Connected in InDesign  
3. Prefer **indesign-uxp** tools (`create_document`, `place_image`, `create_text_frame`, …)  
4. **Gotcha (2026-07-19):** smoke text frames can land on dark **pasteboard** and look “hidden” — confirm page placement; not a broken bridge  
5. Document sizes for this book: **8.5×8.5"** = **215.9 mm** square; bleed ~**3.175 mm** (0.125")

---

## Lulu print assets

Under `Xtraz\Lulu-Templates\` (gitignored with rest of Xtraz):

| File | What |
|------|------|
| `lulu-book-creation-guide.pdf` | Official book creation guide |
| `*-bleed*.html`, `hardcover-casewrap.html`, etc. | Help articles saved locally |
| `.cursor/docs/LULU-8.5-SQUARE-CHEATSHEET.md` | Project 8.5×8.5 numbers |

Exact cover wrap PDF (spine) comes **after** interior upload on lulu.com.

---

## Recommended workflow for this book

1. Generate art **page-by-page** (Gemini + G0s)  
2. Optional: place finals in Affinity **or** InDesign for typography/spreads  
3. Pillow cloud composite remains proven text-on-art until DTP A/B wins  
4. Export press PDF → Lulu  

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Affinity MCP tools missing | Affinity running? `:6767`? Reload Cursor MCP |
| InDesign Bridge not Connected | Bridge running? UDT Watching? Port 19301? |
| Text “invisible” in InDesign | Likely on pasteboard — zoom out / move to page |
| COM / indesign-exec fails | Use UXP path |
| Port 3000 conflict | Keep remapped **19300/19301** — do not revert |
