# Layout app automation research (Affinity + InDesign)

**Date:** 2026-07-16 · **Updated:** wired into `.cursor/mcp.json`
**Setup how-to:** `tools/layout-mcp/SETUP.md`
**Lulu sizes:** `.cursor/docs/LULU-8.5-SQUARE-CHEATSHEET.md`

---

## Bottom line

| App | Agent-controllable? | Status on this PC |
|-----|---------------------|-------------------|
| **Affinity Publisher** | Partial (official MCP beta) | **Wired + verified** — port 6767 · 109 SDK docs extracted |
| **Adobe InDesign** | Yes via UXP MCP | **Wired** — bridge **19300/19301** running; needs **one-time UXP plugin load** |
| **InDesign COM JSX** | Yes in theory | **Broken today** (`Server execution failed`) — kept as fallback |
| **Pillow + Typst** | Full | Still production path for gift book |

---

## What we installed

| Path | Role |
|------|------|
| `.cursor/mcp.json` | Cursor MCP: `affinity`, `indesign-uxp`, `indesign-exec` |
| `tools/layout-mcp/affinity-scripting/` | Community helpers + extracted SDK docs |
| `tools/layout-mcp/indesign-uxp-server/` | UXP plugin + bridge (ports remapped off 3000) |
| `tools/layout-mcp/indesign-scripting-mcp/` | COM exec (fallback) |
| `Xtraz/Lulu-Templates/` | Book Creation Guide PDF + help HTML |

**npm:** `layout:indesign-bridge` · `layout:affinity-inspector` · `layout:affinity-docs`

---

## Your next 2 minutes (InDesign)

1. Open **Adobe UXP Developer Tools** → Add Plugin →
   `tools\layout-mcp\indesign-uxp-server\plugin\manifest.json` → **Load**
2. In InDesign: open **InDesign Bridge** panel → must say **Connected to bridge ✓**
3. **Reload Cursor MCP** (or restart Cursor window) so `affinity` + `indesign-uxp` attach

Affinity MCP is already on — after Cursor reload you should see Affinity tools.

---

## Lulu note

Exact **cover wrap + spine** PDF only appears after interior upload on Lulu. We saved the Book Creation Guide + casewrap/bleed help locally; cheatsheet has 8.5×8.5 / 2625² numbers.
