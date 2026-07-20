# Adobe Creative Cloud ↔ Cursor MCP — Guide

**Date:** 2026-07-19 · **Project:** The Night I Met Santa  
**Role:** Watchlist + corrected install notes — **not** an install-now checklist  
**InDesign authority:** [`tools/layout-mcp/SETUP.md`](../../tools/layout-mcp/SETUP.md) (do not re-own that path here)

**Shareable setup for Tony (Mac):** [`ADOBE-TNYSE-WORKFLOW.md`](./ADOBE-TNYSE-WORKFLOW.md) — full Cursor/Claude → InDesign + Photoshop UXP pipeline with Mac notes.

**Status (this PC):** InDesign UXP **LIVE** · Affinity **READY when open** · Photoshop adobepy UXP **LIVE** (smoke 2026-07-20) · Illustrator / AE / Premiere — not wired

---

## Verified 2026-07-19 (research pass)

Live GitHub / npm / PyPI checks. Use this section when the catalog below drifts.

| Claim / package | Verdict |
|-----------------|--------|
| InDesign UXP `:19300/:19301` | **OK** — production path for this book |
| Affinity `:6767` “always LIVE” | **Wrong** — only when Affinity is open + MCP toggles ON |
| `pip` / `uvx` `photoshop-mcp-server` (loonghao) | **Package OK** — PyPI **0.1.11**, Windows COM — **FAILS on this PC** (`0x80080005`; no `PS_VERSION` map for 2026→200) |
| `@alisaitteke/photoshop-mcp` | **Package OK** — npm ≥1.3 / **1.4.0**, also **Windows COM** — same COM failure class |
| **dcc-mcp-photoshop + adobepy UXP** | **ADOPT path** — PyPI **0.1.37** + adobepy **0.5.2**; WebSocket UXP (bypasses COM) — see `tools/layout-mcp/PHOTOSHOP-SETUP.md` |
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
| **Photoshop + adobepy UXP** | Broker `:47391` · MCP `:8766/mcp` · plugin `com.adobepy.bridge.photoshop` | **LIVE** — smoke PASS 2026-07-20 (`PHOTOSHOP-SETUP.md`) |
| `indesign-exec` (COM/JSX) | Fallback only | Ignore — prefer UXP |
| Photoshop COM MCPs (loonghao / alisaitteke) | — | **Rejected on this PC** — `0x80080005` |
| Cursor MCP | Project `.cursor/mcp.json` | Working (+ `photoshop` URL entry) |

---

## MCP / bridge catalog

### Photoshop — pick for **this PC**

#### Option A (LOCKED for TNIMS): dcc-mcp-photoshop + adobepy UXP

| | |
|---|---|
| **GitHub** | [dcc-mcp/dcc-mcp-photoshop](https://github.com/dcc-mcp/dcc-mcp-photoshop) · [dcc-mcp/adobepy](https://github.com/dcc-mcp/adobepy) |
| **Why** | UXP WebSocket — **works when COM is broken** (proven need on this PC 2026-07-20) |
| **Local setup** | [`tools/layout-mcp/PHOTOSHOP-SETUP.md`](../../tools/layout-mcp/PHOTOSHOP-SETUP.md) |
| **Cursor** | `"url": "http://127.0.0.1:8766/mcp"` after `npm run layout:photoshop-mcp` |
| **Plugin** | UDT Load & Watch → `bridges/photoshop/manifest.json` (`com.adobepy.bridge.photoshop`) |

#### Option B: loonghao COM (skip here)

| | |
|---|---|
| **GitHub** | [loonghao/photoshop-python-api-mcp-server](https://github.com/loonghao/photoshop-python-api-mcp-server) ★~282 |
| **Platform** | Windows COM only |
| **TNIMS** | **SKIP** until Adobe COM fixed — smoke failed against PS 2026 |

#### Option C: alisaitteke (skip here for primary)

| | |
|---|---|
| **GitHub** | [alisaitteke/photoshop-mcp](https://github.com/alisaitteke/photoshop-mcp) ★~200 |
| **Platform** | Win+Mac — **Windows path is still COM** (UXP plugin only for Neural Filters) |
| **TNIMS** | **SKIP** as primary; same COM wall |

**TNIMS pick:** Option A only. Do **not** enable COM MCPs alongside it.

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
1. Keep **InDesign UXP** as gift print production  
2. Finish **Photoshop UXP** Load & Watch → smoke (`PHOTOSHOP-SETUP.md`)
3. Art finals stay **Gemini / Banana + G0 refs**

### Maybe later
4. Illustrator — only after Windows smoke (likely COM/CEP pain)  

### Later (trailer / other projects)
5. After Effects — Dakkshin via **clone**  
6. Premiere — leancoderkavy + CEP  

### Skip / watch
- Media Encoder MCP (none)  
- Flue as InDesign/Photoshop dual driver  
- loonghao / alisaitteke **COM** Photoshop on this PC until `0x80080005` fixed  
- `npm i -g after-effects-mcp` / `premiere-pro-mcp-full`  
- spencerhhubert Illustrator · ayushozha Premiere until install is simpler  

---

## Quick-start (Photoshop — UXP path)

```powershell
# Broker + MCP (keep running)
npm run layout:photoshop-mcp

# Then in UDT: Add Plugin → bridges/photoshop/manifest.json → Load & Watch
# Photoshop → Plugins → Adobe Python Bridge
# Reload Cursor MCP → smoke document info
```

Full steps: **`tools/layout-mcp/PHOTOSHOP-SETUP.md`**.  
Do **not** add loonghao/alisaitteke COM entries while UXP is the path.

---

## Resource links

| Resource | Link |
|----------|------|
| InDesign / Affinity setup (canonical) | [`tools/layout-mcp/SETUP.md`](../../tools/layout-mcp/SETUP.md) |
| **Photoshop UXP setup (TNIMS)** | [`tools/layout-mcp/PHOTOSHOP-SETUP.md`](../../tools/layout-mcp/PHOTOSHOP-SETUP.md) |
| Photoshop MCP (UXP / dcc-mcp) | https://github.com/dcc-mcp/dcc-mcp-photoshop |
| Adobe Python broker (adobepy) | https://github.com/dcc-mcp/adobepy |
| Photoshop MCP (Python COM — skip here) | https://github.com/loonghao/photoshop-python-api-mcp-server |
| Photoshop MCP (Node COM — skip here) | https://github.com/alisaitteke/photoshop-mcp |
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

*Verified research pass: 2026-07-19. Photoshop UXP path staged 2026-07-20 (COM rejected on this PC).*
