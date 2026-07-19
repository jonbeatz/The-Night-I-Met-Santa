# Layout app automation research (Affinity + InDesign)

**Date:** 2026-07-16 · **Updated:** 2026-07-19 (proven cold-start workflow FINAL)  
**Setup how-to:** `tools/layout-mcp/SETUP.md`  
**Lulu sizes:** `.cursor/docs/LULU-8.5-SQUARE-CHEATSHEET.md`

---

## Bottom line

| App | Agent-controllable? | Status on this PC (2026-07-19) |
|-----|---------------------|--------------------------------|
| **Affinity** (Studio / Designer) | Partial (official MCP beta) | **IN USE / READY** — `:6767` · MCP toggles ON · Cursor `affinity` (11 tools) · script smoke PASS |
| **Adobe InDesign 2026** | Yes via UXP MCP | **IN USE / READY** — UDT + Bridge + MCP; smoke `create_document` 8.5×8.5" PASS |
| **InDesign COM JSX** (`indesign-exec`) | Yes in theory | **Fallback only** — historically `Server execution failed`; prefer UXP |
| **Pillow + Typst** | Full | **Still production path** for gift book until DTP A/B wins |

---

## Proven cold-start (FINAL)

1. Agent launches **Creative Cloud Desktop**  
2. **Jon** signs in fully → says **logged in** (do not trust process heuristics alone)  
3. Agent launches **UDT** + **InDesign** + `npm run layout:indesign-bridge`  
4. **Jon** clicks **Load & Watch** in UDT (agent cannot — Electron)  
5. Bridge Panel **Connected ✓** → agent MCP smoke  

**Not enough:** adobe.com web login alone. **Required:** CC Desktop app running + signed in for UDT Load.  
**Keep CC installed**; Startup disable OK between sessions.  
Full table: `tools/layout-mcp/SETUP.md` → Proven cold-start workflow.

---

## What we have in the tool chest

| Path / piece | Role |
|--------------|------|
| `.cursor/mcp.json` | Cursor MCP: `affinity`, `indesign-uxp`, `indesign-exec` |
| `tools/layout-mcp/affinity-scripting/` | Community helpers + extracted SDK docs |
| `tools/layout-mcp/indesign-uxp-server/` | UXP plugin **InDesign Bridge** + HTTP/WS bridge |
| `tools/layout-mcp/indesign-scripting-mcp/` | COM exec (fallback) |
| Adobe **UXP Developer Tools** 2.2.1.2 | Loads/watches plugin (`Service Port` **14001**) |
| Creative Cloud Desktop | **Required** for UDT Load (not optional when loading plugin) |
| `Xtraz/Lulu-Templates/` | Book Creation Guide PDF + help HTML |

**npm:** `layout:indesign-bridge` · `layout:affinity-inspector` · `layout:affinity-docs` · `layout:install`

**Install paths (this PC):**
- CC: `C:\Program Files\Adobe\Adobe Creative Cloud\ACC\Creative Cloud.exe`
- UDT: `C:\Program Files\Adobe\Adobe UXP Developer Tools\Adobe UXP Developer Tools.exe`
- InDesign: `C:\Program Files\Adobe\Adobe InDesign 2026\InDesign.exe`
- Affinity: WindowsApps / `Affinity.exe` (Start menu)
- Plugin: `tools\layout-mcp\indesign-uxp-server\plugin\manifest.json`

---

## Verified 2026-07-19

1. UDT installed → plugin `com.ads.indesign-bridge` Add Plugin once  
2. Full cold flow after CC sign-in confirm → Jon Load & Watch → MCP `create_document` 8.5×8.5" PASS  
3. Affinity MCP script smoke PASS (separate from CC)  
4. Gotchas locked: pasteboard text placement; no agent Load click; no UDT before CC confirmed  

---

## Workflow stance

1. Art: **page-by-page Gemini + G0s** (unchanged)  
2. Text-on-art: **Pillow cloud** → Typst remains default print path  
3. Affinity / InDesign: optional polish, spreads, typography, PDF export A/B  
4. Exact Lulu cover wrap PDF still after interior upload (spine depends on page count)  

---

## Lulu note

Exact **cover wrap + spine** PDF only appears after interior upload on Lulu. Cheatsheet: 8.5×8.5 / 2625² numbers in `LULU-8.5-SQUARE-CHEATSHEET.md`.
