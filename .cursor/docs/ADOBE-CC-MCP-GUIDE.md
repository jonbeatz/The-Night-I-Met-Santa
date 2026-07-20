# Adobe Creative Cloud ↔ Cursor MCP — Guide

**Date:** 2026-07-19 · **Project:** The Night I Met Santa  
**Role:** Watchlist + corrected install notes — **not** an install-now checklist  
**InDesign authority:** [`tools/layout-mcp/SETUP.md`](../../tools/layout-mcp/SETUP.md) (do not re-own that path here)

**Status (this PC):** InDesign UXP **LIVE** · Affinity **READY when open** · Photoshop / Illustrator / AE / Premiere — **not wired** (optional later)

---

## Verified 2026-07-19 (research pass)

Live GitHub / npm / PyPI checks. Use this section when the catalog below drifts.

| Claim / package | Verdict |
|-----------------|--------|
| InDesign UXP `:19300/:19301` | **OK** — production path for this book |
| Affinity `:6767` “always LIVE” | **Wrong** — only when Affinity is open + MCP toggles ON |
| `pip` / `uvx` `photoshop-mcp-server` (loonghao) | **OK** — PyPI **0.1.11**, Windows-only COM, ★~282 |
| `@alisaitteke/photoshop-mcp` | **OK** — npm **1.3.13**, Win+Mac, ★~200 |
| `illustrator-mcp-server` (ie3jp) | **OK package** — but upstream: **Windows COM not tested on real hardware** |
| `npm i -g after-effects-mcp` | **Dangerous** — npm name points to **a-y-ibrahim** (★3), **not** Dakkshin (★500) |
| Dakkshin After Effects | **OK via git clone** + `npm run install-bridge` — no clean global npm for that repo |
| `premiere-pro-mcp` (leancoderkavy) | **OK** — npm **1.1.5** + CEP panel |
| `npm i -g premiere-pro-mcp-full` | **404** — does not exist; ayushozha is **clone + `just install`** |
| Flue `pip install flue` | **OK** — PyPI **1.0.31** · **not an MCP server** (shell/skill bridge) |
| npm package name `flue` | **Wrong product** — unrelated Firebase utility |
| Huge tool counts (269 / 1k+) | **Marketing** — prefer fewer, smoke-tested tools |

**Fleet gate:** These are unofficial community bridges. ADOPT only after a Windows smoke test. Do **not** auto-fleet-sync into other Hermes profiles.

---

## Overview

**Unofficial** community MCP (and Flue shell) bridges can drive some Adobe apps from Cursor. They can break on Creative Cloud updates. There is **no** official Adobe “full CC MCP suite.”

You already have **InDesign** working via UXP Bridge (`:19300/:19301`). Other apps need **separate** servers or Flue adapters — install only when a real workflow needs them.

### How Adobe apps connect (typical)

| App | Extension system | Bridge type |
|-----|------------------|-------------|
| **InDesign** | UXP (modern) | WebSocket `:19300/:19301` — **our production path** |
| **Photoshop** | UXP + COM / ExtendScript | Python MCP (Windows) or Node MCP |
| **Illustrator** | ExtendScript / COM | Node MCP (macOS primary; Windows risky) |
| **Premiere Pro** | CEP + ExtendScript | Node MCP + CEP panel |
| **After Effects** | CEP / ExtendScript panel | Node MCP + bridge panel |
| **Media Encoder** | No public agent API | No useful MCP — export from Premiere |

---

## What you already have (TNIMS)

| Component | Notes | Status |
|-----------|-------|--------|
| UXP Developer Tools | 2.2.1.2 | Installed |
| Creative Cloud Desktop | Keep for licensing | Installed |
| InDesign + UXP Bridge | `:19300/:19301` · see SETUP.md | **LIVE when Connected** |
| Affinity MCP | `:6767` · Affinity open + MCP all ON | **READY when open** (not always up) |
| `indesign-exec` (COM/JSX) | Fallback only | Ignore — prefer UXP |
| Cursor MCP | Project `.cursor/mcp.json` | Working |

---

## MCP / bridge catalog

### Photoshop — two options

#### Option A: loonghao (Windows-friendly default)

| | |
|---|---|
| **GitHub** | [loonghao/photoshop-python-api-mcp-server](https://github.com/loonghao/photoshop-python-api-mcp-server) ★~282 |
| **License** | MIT |
| **Platform** | **Windows only** (COM) |
| **Package** | PyPI `photoshop-mcp-server` |
| **Best config** | `uvx` + `PS_VERSION` (see install below) |

#### Option B: alisaitteke (cross-platform / more agent recipes)

| | |
|---|---|
| **GitHub** | [alisaitteke/photoshop-mcp](https://github.com/alisaitteke/photoshop-mcp) ★~200 |
| **License** | MIT (repo badge) |
| **Platform** | Windows + macOS |
| **Package** | npm `@alisaitteke/photoshop-mcp` **1.3.13** |
| **Bonus** | Standalone web UI; recipe workflows |

**TNIMS pick:** A/B one afternoon before wiring either into `.cursor/mcp.json`. Do **not** enable both at once.

---

### Illustrator

| | |
|---|---|
| **GitHub** | [ie3jp/illustrator-mcp-server](https://github.com/ie3jp/illustrator-mcp-server) ★~60 |
| **License** | MIT |
| **Package** | npm `illustrator-mcp-server` **1.5.1** |
| **Requires** | Illustrator CC 2024+ |
| **Windows risk** | Upstream: *“Windows uses PowerShell COM automation (not yet tested on real hardware)”* |

**Stale alt (reference only):** [spencerhhubert/illustrator-mcp-server](https://github.com/spencerhhubert/illustrator-mcp-server) — last push ~2024-12; no license; skip for installs.

**TNIMS pick:** **Defer** until after a Windows smoke test — not needed for gift print path.

---

### After Effects

#### Preferred: Dakkshin (popular; clone install)

| | |
|---|---|
| **GitHub** | [Dakkshin/after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp) ★~500 |
| **License** | MIT |
| **Method** | **git clone** → `npm install` → `npm run install-bridge` → AE panel open |
| **Do not** | `npm install -g after-effects-mcp` (wrong publisher — see Verified table) |

#### Alt: ishu86

| | |
|---|---|
| **GitHub** | [ishu86/after-effects-mcp](https://github.com/ishu86/after-effects-mcp) ★~19 |
| **Package name** | `ae-mcp` (not the global `after-effects-mcp` name) |

**Name collision:** npm `after-effects-mcp` currently resolves to [a-y-ibrahim/after-effects-mcp](https://github.com/a-y-ibrahim/after-effects-mcp) (★~3), not Dakkshin.

---

### Premiere Pro

#### Preferred: leancoderkavy

| | |
|---|---|
| **GitHub** | [leancoderkavy/premiere-pro-mcp](https://github.com/leancoderkavy/premiere-pro-mcp) ★~124 |
| **License** | MIT |
| **Package** | npm `premiere-pro-mcp` **1.1.5** |
| **Method** | npm + **CEP panel** (`premiere-pro-mcp --install-cep` or manual `%APPDATA%\Adobe\CEP\extensions\`) |
| **Tool count** | Marketed ~269 — treat as approximate |

#### Alt: ayushozha (largest surface; heavier build)

| | |
|---|---|
| **GitHub** | [ayushozha/AdobePremiereProMCP](https://github.com/ayushozha/AdobePremiereProMCP) ★~59 |
| **License** | MIT |
| **Install** | **Clone + `just install` / `just install-panel`** — **not** `premiere-pro-mcp-full` on npm |
| **Stack** | Go orchestrator + CEP/TS bridge (heavier than leancoderkavy) |

---

## Flue — unified shell alternative (not MCP)

| | |
|---|---|
| **GitHub** | [SFKislev/Flue](https://github.com/SFKislev/Flue) ★~56 |
| **License** | MIT |
| **Install** | `pip install flue` then `flue setup` (PyPI **1.0.31**) |
| **What it is** | Shell/skill bridge into app scripting APIs — **not** a Cursor MCP server |
| **Covers** | Photoshop, Illustrator, Premiere, After Effects, InDesign, plus non-Adobe apps |
| **Pros** | One pip install; multi-app |
| **Cons** | Less mature than dedicated MCPs; **InDesign adapter can conflict with our UXP bridge** if both drive the same doc |

**TNIMS:** Skip for now. If experimenting later, do **not** dual-control InDesign (Flue **or** UXP, not both).

---

## Corrected install blocks (when Jon approves)

### General pattern

1. Install the bridge (pip / npm / clone as documented above)
2. Launch the Adobe app (+ CEP/UXP panel if required)
3. Add entry to **this repo’s** `.cursor/mcp.json` (Jon confirms first)
4. Reload Cursor MCP → green
5. Smoke-test one tiny command
6. Do **not** fleet-sync until smoke passes

### Photoshop — loonghao (recommended Windows pattern)

```json
{
  "mcpServers": {
    "photoshop": {
      "command": "uvx",
      "args": ["--python", "3.10", "photoshop-mcp-server"],
      "env": {
        "PS_VERSION": "2025"
      }
    }
  }
}
```

Set `PS_VERSION` to the year folder Photoshop reports (e.g. `"2024"`, `"2025"`, `"2026"`).  
Alt: `pip install photoshop-mcp-server` then point `command` at the installed console script — `uvx` is preferred upstream.

### Photoshop — alisaitteke

```json
{
  "mcpServers": {
    "photoshop": {
      "command": "npx",
      "args": ["-y", "@alisaitteke/photoshop-mcp"]
    }
  }
}
```

### Illustrator (defer on Windows)

```json
{
  "mcpServers": {
    "illustrator": {
      "command": "npx",
      "args": ["-y", "illustrator-mcp-server"]
    }
  }
}
```

Smoke on this PC before trusting for book assets.

### Premiere Pro — leancoderkavy

```powershell
npm install -g premiere-pro-mcp
premiere-pro-mcp --install-cep
```

```json
{
  "mcpServers": {
    "premiere-pro": {
      "command": "npx",
      "args": ["-y", "premiere-pro-mcp"],
      "env": {
        "PREMIERE_TEMP_DIR": "C:\\Users\\JONBEATZ\\AppData\\Local\\Temp\\premiere-mcp-bridge"
      }
    }
  }
}
```

In Premiere: **Window → Extensions → MCP Bridge** and match temp directory to `PREMIERE_TEMP_DIR`.

### After Effects — Dakkshin (clone; not global npm name)

```powershell
git clone https://github.com/Dakkshin/after-effects-mcp.git D:\Hermes\tools\after-effects-mcp
cd D:\Hermes\tools\after-effects-mcp
npm install
npm run install-bridge
```

Point Cursor MCP `command`/`args` at that repo’s built `build/index.js` (per their README). Open the MCP Bridge panel in AE before calling tools.

---

## UXP vs CEP

| App | System | Cursor path |
|-----|--------|-------------|
| InDesign | UXP WebSocket | Our bridge — see SETUP.md |
| Photoshop | COM / ExtendScript | Python or Node MCP |
| Illustrator | ExtendScript / COM | Node MCP |
| Premiere / AE | CEP panel + scripts | Node MCP + panel |

Premiere and AE need a **CEP (or AE script) panel** as the in-app bridge. InDesign’s UXP bridge is more direct for our workflow.

---

## Example prompts (optional apps)

### Photoshop
- Create an 8.5×8.5" 300 DPI document with 0.125" bleed guides  
- Batch-convert files under `Media/` to sRGB  
- Soft watercolor texture overlay at ~50% opacity  

### Illustrator
- Typography lockups for the book title  
- Outline text / SVG export for web  

### After Effects / Premiere
- Book trailer / social motion (post-gift)  
- Color grade to warm holiday palette  

---

## Recommendations for this book project

### Do now
1. **Nothing new** — keep **InDesign UXP** as gift print production  
2. Art finals stay **Gemini / Banana + G0 refs** (see `BOOK-PRODUCTION-SYSTEM.md`)

### Maybe later (after proof / if a real PS pain appears)
3. **One** Photoshop MCP (loonghao *or* alisaitteke) — A/B first  
4. Illustrator — only after Windows smoke passes  

### Later (trailer / CTFU / other projects)
5. After Effects — Dakkshin via **clone**  
6. Premiere — leancoderkavy + CEP  

### Skip / watch
- Media Encoder MCP (none)  
- Flue as InDesign replacement or dual driver  
- `npm i -g after-effects-mcp` / `premiere-pro-mcp-full`  
- spencerhhubert Illustrator · ayushozha Premiere until install is simpler  

---

## Quick-start (Photoshop only — when approved)

```powershell
# Prefer uvx (no global pollute)
# Then merge the loonghao JSON block above into .cursor/mcp.json
# Launch Photoshop → reload Cursor MCP → smoke:
#   "Create a new 8.5x8.5 inch 300 DPI RGB document"
```

Until Jon says otherwise, **do not** add Photoshop/Illustrator/AE/Premiere entries to this project’s MCP config.

---

## Resource links

| Resource | Link |
|----------|------|
| InDesign / Affinity setup (canonical) | [`tools/layout-mcp/SETUP.md`](../../tools/layout-mcp/SETUP.md) |
| Photoshop MCP (Python / Windows) | https://github.com/loonghao/photoshop-python-api-mcp-server |
| Photoshop MCP (Node) | https://github.com/alisaitteke/photoshop-mcp |
| Illustrator MCP | https://github.com/ie3jp/illustrator-mcp-server |
| Illustrator MCP (stale) | https://github.com/spencerhhubert/illustrator-mcp-server |
| After Effects (Dakkshin — clone) | https://github.com/Dakkshin/after-effects-mcp |
| After Effects npm name collision | https://github.com/a-y-ibrahim/after-effects-mcp |
| After Effects (ishu) | https://github.com/ishu86/after-effects-mcp |
| Premiere Pro MCP | https://github.com/leancoderkavy/premiere-pro-mcp |
| Premiere Pro MCP (heavy) | https://github.com/ayushozha/AdobePremiereProMCP |
| Flue (shell bridge, not MCP) | https://github.com/SFKislev/Flue |
| MCP protocol | https://modelcontextprotocol.io |

---

*Verified research pass: 2026-07-19. Update the Verified table when re-checking stars / package names.*
