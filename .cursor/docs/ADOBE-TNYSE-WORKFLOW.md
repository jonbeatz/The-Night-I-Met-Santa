# ADOBE-TNYSE-WORKFLOW.md

**For:** Tony (Mac) — set up the same **Cursor / Claude Code → Adobe InDesign + Photoshop** agent pipeline we use on Windows  
**From:** Jon / The Night I Met Santa book project (Hermes, 2026-07)  
**Purpose:** Hand this file to your coding agent (Cursor or Claude Code). It has everything needed to configure Creative Cloud, UXP Developer Tools, bridges, and MCP so the agent can drive **InDesign** and **Photoshop**.  
**Status:** Proven LIVE on Windows (2026-07-19 InDesign · 2026-07-20 Photoshop). Mac notes included — **smoke-test on your Mac** before trusting production work.

> **Apple / Mac callouts** are marked **`[MAC]`**. Follow those instead of Windows paths/commands when you are on macOS.

---

## 0) What this system is (30-second version)

```
You (human)
  └─ Cursor / Claude Code (agent)
        ├─ MCP: indesign-uxp  → Node bridge :19300/:19301 → UXP plugin inside InDesign
        └─ MCP: photoshop     → HTTP :8766 → adobepy broker :47391 → UXP plugin inside Photoshop

Glue app: Adobe UXP Developer Tools (UDT) — Load & Watch the two plugins
License hub: Adobe Creative Cloud Desktop — must be signed in for UDT Load
```

**Roles we use on the book:**

| App | Agent role |
|-----|------------|
| **Photoshop** | MOCK layouts, layer/chop exports, art cleanup (watermarks, guides) |
| **InDesign** | Production print layout — place art, live type, export Lulu PDF |
| **Creative Cloud Desktop** | Licensing + UDT sign-in (not optional) |
| **UXP Developer Tools** | Load / Watch / Reload the bridge plugins |

**Do not** rely on Windows COM automation (loonghao / alisaitteke Photoshop COM MCPs, InDesign COM). On our Windows PC COM is broken; on **Mac COM does not exist anyway**. **UXP bridges are the portable path.**

---

## 1) Prerequisites

### Software (both OS)

| Piece | Notes |
|-------|--------|
| Adobe Creative Cloud Desktop | Keep installed; signed in for sessions |
| Adobe InDesign (2024+) | We use **2026** |
| Adobe Photoshop (2024+ / UXP min ~25.0) | We use **2026** |
| **Adobe UXP Developer Tools** | Install from Creative Cloud (not the old `devtools-cli` for InDesign) |
| Node.js 18+ (20+ fine) | For InDesign bridge MCP |
| Python 3.11+ + [uv](https://github.com/astral-sh/uv) | For Photoshop MCP stack |
| Cursor **or** Claude Code | MCP client |

### `[MAC]` install hints

```bash
# Homebrew examples (adjust if you already have them)
brew install node
brew install uv
# Creative Cloud + apps: install from Adobe, not Homebrew
```

Typical Mac app paths:

| App | Path |
|-----|------|
| Creative Cloud | `/Applications/Adobe Creative Cloud/Adobe Creative Cloud.app` (or Creative Cloud Desktop) |
| UXP Developer Tools | `/Applications/Adobe UXP Developer Tools/Adobe UXP Developer Tools.app` |
| InDesign 2026 | `/Applications/Adobe InDesign 2026/Adobe InDesign 2026.app` |
| Photoshop 2026 | `/Applications/Adobe Photoshop 2026/Adobe Photoshop 2026.app` |

Launch examples:

```bash
open -a "Adobe Creative Cloud"
open -a "Adobe UXP Developer Tools"
open -a "Adobe InDesign 2026"
open -a "Adobe Photoshop 2026"
```

### Windows reference (Jon’s machine — for comparison only)

| App | Path |
|-----|------|
| CC | `C:\Program Files\Adobe\Adobe Creative Cloud\ACC\Creative Cloud.exe` |
| UDT | `C:\Program Files\Adobe\Adobe UXP Developer Tools\Adobe UXP Developer Tools.exe` |
| InDesign | `C:\Program Files\Adobe\Adobe InDesign 2026\InDesign.exe` |
| Photoshop | `C:\Program Files\Adobe\Adobe Photoshop 2026\Photoshop.exe` |

---

## 2) Architecture & ports (keep these)

| Service | Port | Protocol | Who starts it |
|---------|-----:|----------|---------------|
| InDesign UXP HTTP | **19300** | HTTP | Node bridge process |
| InDesign UXP WebSocket | **19301** | WS | Same Node bridge |
| Photoshop adobepy broker | **47391** | HTTP/WS hub | `adobepy broker` |
| Photoshop MCP | **8766** | MCP Streamable HTTP `/mcp` | `dcc-mcp-photoshop` |
| Affinity MCP (optional) | **6767** | SSE | Affinity app itself |
| UDT Service Port (Jon’s PC) | **14001** | UDT prefs | UDT app |

**Why not 3000?** Classic samples use 3000/3001 — that collides with Next.js / local web apps. **Always remap InDesign bridge to 19300/19301.**

```
Cursor ──MCP──► indesign-uxp (Node src/index.js)
                    │
                    ▼
              bridge :19300/:19301
                    │
                    ▼
         InDesign UXP plugin  com.ads.indesign-bridge
              (Load & Watch in UDT)


Cursor ──HTTP MCP──► http://127.0.0.1:8766/mcp  (dcc-mcp-photoshop)
                           │
                           ▼
                    adobepy broker :47391
                           │
                           ▼
         Photoshop UXP plugin  com.adobepy.bridge.photoshop
              (Load & Watch in UDT + Plugins → Adobe Python Bridge)
```

---

## 3) What to copy / clone

You do **not** need Jon’s whole Hermes fleet. You need:

### A) InDesign UXP bridge (Node)

Source of truth in Jon’s repo:

```
tools/layout-mcp/indesign-uxp-server/
  bridge/server.js          ← HTTP/WS bridge (:19300/:19301)
  src/index.js              ← Cursor MCP server wrapper
  plugin/manifest.json      ← UDT “Add Plugin” target
  plugin/…                  ← UXP plugin assets
```

**Tony options:**

1. Copy that folder into your project as `tools/layout-mcp/indesign-uxp-server/`, **or**
2. Ask your agent to vendor the same pattern from Adobe’s UXP samples + MCP wrapper (ports must stay 19300/19301).

Then:

```bash
cd tools/layout-mcp/indesign-uxp-server
npm install
```

### B) Photoshop adobepy + dcc-mcp (UXP, not COM)

Upstream:

| Piece | Link |
|-------|------|
| adobepy | https://github.com/dcc-mcp/adobepy |
| dcc-mcp-photoshop | https://github.com/dcc-mcp/dcc-mcp-photoshop (PyPI `dcc-mcp-photoshop`) |

Versions we locked: **adobepy 0.5.2** · **dcc-mcp-photoshop 0.1.37**

Plugin id: **`com.adobepy.bridge.photoshop`**  
Panel name: **Adobe Python Bridge**

### C) Optional Affinity

Only if you use Affinity Studio — official local MCP on `:6767`. Independent of Creative Cloud. Skip if you only care about Adobe.

---

## 4) One-time setup — InDesign

### 4.1 Creative Cloud + UDT

1. Install **Creative Cloud Desktop**, **InDesign**, **UXP Developer Tools**.
2. Sign into **Creative Cloud Desktop** (the app — **not** only adobe.com in a browser).
3. Open UDT once so it can authenticate.

**Proven gotcha:** If CC Desktop is closed or not fully signed in, UDT shows **Sign-In Required** and plugins stay **Not loaded**. Web login alone is **not** enough.

### 4.2 Add the InDesign Bridge plugin

1. UDT → **Add Plugin** → select:
   - `…/indesign-uxp-server/plugin/manifest.json`
2. Click **Load & Watch** (state should become **Watching**).
3. Open InDesign → open the **Bridge** panel → wait for **Connected to bridge ✓**.

Plugin id: **`com.ads.indesign-bridge`**.

**Human-only step:** Agents **cannot** reliably click UDT Load & Watch (Electron UI). You must click it.

### 4.3 Start the Node bridge

**Windows (Jon):**

```powershell
$env:INDESIGN_BRIDGE_HTTP_PORT='19300'
$env:INDESIGN_BRIDGE_WS_PORT='19301'
node tools/layout-mcp/indesign-uxp-server/bridge/server.js
# or: npm run layout:indesign-bridge
```

**`[MAC]`:**

```bash
export INDESIGN_BRIDGE_HTTP_PORT=19300
export INDESIGN_BRIDGE_WS_PORT=19301
node tools/layout-mcp/indesign-uxp-server/bridge/server.js
```

Keep this terminal running for the session.

### 4.4 Wire Cursor / Claude Code MCP

Project `.cursor/mcp.json` (or Claude Code MCP config) — **use your Mac absolute paths**:

```json
{
  "mcpServers": {
    "indesign-uxp": {
      "command": "node",
      "args": [
        "/Users/TONY/YOUR-PROJECT/tools/layout-mcp/indesign-uxp-server/src/index.js"
      ],
      "cwd": "/Users/TONY/YOUR-PROJECT/tools/layout-mcp/indesign-uxp-server",
      "env": {
        "INDESIGN_BRIDGE_HTTP_PORT": "19300",
        "INDESIGN_BRIDGE_WS_PORT": "19301"
      }
    }
  }
}
```

**`[MAC]`:** Prefer forward-slash absolute paths. Do **not** paste Jon’s `D:\\Hermes\\…` Windows paths.

Reload MCP in Cursor. Expect on the order of **~100+ tools** when Connected.

### 4.5 InDesign smoke

With InDesign open + Bridge **Connected**:

- Create an 8.5×8.5" document (or 215.9 mm square)
- Confirm tools respond (`get_document_info` / `create_document` / etc.)

**Gotcha:** New text frames can land on the **pasteboard** and look “missing” — zoom out / check page placement. Bridge can still be healthy.

---

## 5) One-time setup — Photoshop (adobepy UXP)

### 5.1 Why this stack

| Approach | Verdict |
|----------|---------|
| Windows COM MCPs (loonghao, alisaitteke) | Fail on Jon’s PC (`0x80080005`); **N/A on Mac** |
| **adobepy UXP + dcc-mcp-photoshop** | **LIVE** — WebSocket into Photoshop; portable |

### 5.2 Install broker + Python MCP

**`[MAC]` recommended:**

```bash
mkdir -p tools/layout-mcp/photoshop-adobepy
cd tools/layout-mcp/photoshop-adobepy

# 1) Get adobepy Mac binary from GitHub Releases (NOT the windows-x64 zip)
#    https://github.com/dcc-mcp/adobepy/releases
#    Extract so you have something like:
#    ./adobepy-*-macos-*/bin/adobepy   (or similar)
chmod +x ./adobepy-*/bin/adobepy

# 2) Python venv + packages
uv venv .venv
source .venv/bin/activate
uv pip install adobepy dcc-mcp-photoshop
# pin if you want our proven pair:
# uv pip install 'adobepy==0.5.2' 'dcc-mcp-photoshop==0.1.37'

# 3) Stage UXP bridge files
./adobepy-*/bin/adobepy install-bridge photoshop --dest ./bridges/photoshop
# or, if adobepy is on PATH via the wheel:
# adobepy install-bridge photoshop --dest ./bridges/photoshop
```

**Windows reference (Jon):** extract `adobepy-0.5.2-windows-x64.zip`, venv under `photoshop-adobepy/.venv`, `npm run layout:photoshop-mcp`.

### 5.3 Photoshop prefs

Photoshop → **Preferences → Plugins**:

| Setting | Need? |
|---------|-------|
| **Enable Developer Mode** | **YES** |
| Enable Generator | No |
| Enable Remote Connections | No (old Generator protocol — not this path) |

Restart Photoshop after enabling Developer Mode.

### 5.4 Load plugin in UDT

1. UDT → **Add Plugin** →  
   `tools/layout-mcp/photoshop-adobepy/bridges/photoshop/manifest.json`
2. **Load & Watch** → state **Watching**
3. Photoshop → **Plugins → Adobe Python Bridge for Photoshop → Adobe Python Bridge** (panel open / checked)

### 5.5 Start broker + MCP each session

**`[MAC]` start script** — save as `tools/layout-mcp/photoshop-adobepy/start-photoshop-mcp.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
# Adjust binary path to match your extracted release name:
ADOBEPY="$ROOT"/adobepy-0.5.2-macos-*/bin/adobepy
ADOBEPY=$(echo $ADOBEPY)  # expand glob
PY="$ROOT/.venv/bin/python"
TOKEN="${ADOBEPY_TOKEN:-dev-token}"
PORT="${DCC_MCP_PHOTOSHOP_PORT:-8766}"

export ADOBEPY_TOKEN="$TOKEN"
export ADOBEPY_BROKER_URL="http://127.0.0.1:47391"

if ! curl -sf "http://127.0.0.1:47391/health" >/dev/null 2>&1; then
  echo "[photoshop-mcp] Starting adobepy broker on :47391 ..."
  "$ADOBEPY" broker --token "$TOKEN" &
  sleep 2
fi

echo "[photoshop-mcp] Starting MCP on :$PORT ..."
echo "[photoshop-mcp] Cursor URL: http://127.0.0.1:$PORT/mcp"
exec "$PY" -m dcc_mcp_photoshop --mcp-port "$PORT" --broker-url "$ADOBEPY_BROKER_URL"
```

```bash
chmod +x tools/layout-mcp/photoshop-adobepy/start-photoshop-mcp.sh
./tools/layout-mcp/photoshop-adobepy/start-photoshop-mcp.sh
```

**Critical order:** start broker/MCP **before** (or then **Reload**) the UXP plugin. If the plugin was Watching and you restart the broker, UDT still shows Watching but broker reports `"sessions":0`. Fix = **UDT → Reload** on the Photoshop plugin (usually no need to quit Photoshop).

### 5.6 Wire Photoshop MCP in Cursor

```json
{
  "mcpServers": {
    "photoshop": {
      "url": "http://127.0.0.1:8766/mcp"
    }
  }
}
```

Cursor green ≠ ready. Truth checks:

```bash
curl -s http://127.0.0.1:47391/health
# expect: "status":"ok" and "sessions": 1 (or more)

curl -s http://127.0.0.1:8766/v1/readyz
# expect: "dcc": true   (not 503)
```

Document smoke (after `load_skill` / or HTTP):

```bash
curl -s -X POST http://127.0.0.1:8766/v1/call \
  -H "Content-Type: application/json" \
  --data-raw '{"tool_slug":"photoshop_document__get_document_info","arguments":{}}'
```

Python SDK alternate:

```bash
export ADOBEPY_TOKEN=dev-token
./tools/layout-mcp/photoshop-adobepy/.venv/bin/python -c \
  "from adobe.photoshop import Photoshop; d=Photoshop(token='dev-token').active_document; print(d.name, d.width, d.height)"
```

### 5.7 Agent note — lazy skills

`dcc-mcp-photoshop` exposes tools via **skills**. Typical flow:

1. `search_tools` / `load_skill` with `photoshop-document` (and layers, etc. as needed)
2. Then call `photoshop_document__get_document_info`, `list_layers`, …
3. If Cursor’s tool list lags after `load_skill`, use HTTP `/v1/call` — bridge can still be live

---

## 6) Combined cold-start ritual (each work session)

Do this **in order**. Do not skip CC sign-in.

| Step | Who | Action |
|-----:|-----|--------|
| 1 | Human | Open **Creative Cloud Desktop** → fully signed in |
| 2 | Human / agent | Open **InDesign** + **Photoshop** (as needed) |
| 3 | Human / agent | Open **UXP Developer Tools** |
| 4 | Agent | Start InDesign Node bridge (`:19300/:19301`) |
| 5 | Agent | Start Photoshop broker + MCP (`:47391` + `:8766`) |
| 6 | **Human** | UDT → **Load & Watch** (or **Reload**) InDesign Bridge |
| 7 | **Human** | UDT → **Load & Watch** (or **Reload**) Adobe Python Bridge for Photoshop |
| 8 | Human | InDesign Bridge panel **Connected ✓** · Photoshop **Adobe Python Bridge** panel open |
| 9 | Human | Reload Cursor / Claude MCP if servers look red |
| 10 | Agent | Smoke: InDesign doc info · PS `sessions≥1` + `dcc:true` |

**`[MAC]` launch helpers:**

```bash
open -a "Adobe Creative Cloud"
# wait until human confirms signed in
open -a "Adobe UXP Developer Tools"
open -a "Adobe InDesign 2026"
open -a "Adobe Photoshop 2026"
```

---

## 7) How we use this for a picture-book (process knowledge)

You can reuse this pattern for any illustrated book / print project:

### Production split

1. **Photoshop** — design MOCK spreads/singles, export **chops** (LEFT/RIGHT art, cloud overlays, frames).
2. **InDesign** — place chops, recreate poem/type as **live text** (never ship raster poem for print), export press PDF.
3. Human approves **page-by-page** — do not batch-regenerate a whole book blindly.

### Print sizes we use (8.5×8.5" Lulu hardcover)

| Asset | Pixels @ 300 DPI |
|-------|------------------|
| Single page + bleed | **2625 × 2625** |
| Full spread + bleed | **5250 × 2625** |

Photoshop’s “72 dpi” tag is often metadata only — **pixel count** matters for print.

### Type

- Poem / body: live InDesign text (we use Cormorant Garamond)
- No poem text baked into AI art
- Soft irregular **cloud / wash** under type (not hard white boxes)

### Quality gates

- No fake gutter/fold line in **final** spread art (MOCK fold OK for screen alignment)
- Check **watermarks** on finals — remove in Photoshop before print
- Keep faces/text inside safety (~0.5" from trim)

### Optional Affinity

Affinity MCP `:6767` for polish only — not required for the Adobe UXP path.

---

## 8) Full example `.cursor/mcp.json` (Mac)

Replace `YOUR_USER` / `YOUR-PROJECT`:

```json
{
  "mcpServers": {
    "indesign-uxp": {
      "command": "node",
      "args": [
        "/Users/YOUR_USER/YOUR-PROJECT/tools/layout-mcp/indesign-uxp-server/src/index.js"
      ],
      "cwd": "/Users/YOUR_USER/YOUR-PROJECT/tools/layout-mcp/indesign-uxp-server",
      "env": {
        "INDESIGN_BRIDGE_HTTP_PORT": "19300",
        "INDESIGN_BRIDGE_WS_PORT": "19301"
      }
    },
    "photoshop": {
      "url": "http://127.0.0.1:8766/mcp"
    }
  }
}
```

Optional Affinity (only if Affinity open + MCP enabled in app settings):

```json
"affinity": {
  "command": "uvx",
  "args": [
    "--from", "mcp-proxy", "mcp-proxy",
    "--transport", "sse",
    "http://127.0.0.1:6767/sse"
  ]
}
```

**Skip** Windows-only COM servers (`indesign-exec` COM, loonghao Photoshop COM) on Mac.

---

## 9) Troubleshooting (hard-won)

| Symptom | Fix |
|---------|-----|
| UDT **Sign-In Required** | Open Creative Cloud **Desktop**, finish login, relaunch UDT |
| InDesign Bridge not Connected | Bridge process running? Ports 19300/19301 free? Plugin Watching? |
| Cursor `photoshop` green but tools 503 | Check `sessions` + `dcc` — usually need **UDT Reload** after broker restart |
| Broker `"sessions":0` | Reload Photoshop UXP plugin; confirm Adobe Python Bridge panel open |
| PS Developer Mode ignored | Restart Photoshop after enabling |
| Agent can’t click Load & Watch | Expected — human must click |
| Text “invisible” in InDesign | Often on pasteboard — not a dead bridge |
| Port 3000 conflict | Keep InDesign on **19300/19301** |
| PowerShell script breaks on `—` | Windows-only; Mac bash scripts should stay ASCII |
| COM MCP install guides | Ignore on Mac; use UXP |

---

## 10) Checklist for Tony’s agent (copy/paste)

```
[ ] Creative Cloud Desktop installed + signed in
[ ] InDesign + Photoshop + UXP Developer Tools installed
[ ] Node + uv + Python 3.11+ on PATH
[ ] Vendor indesign-uxp-server (plugin + bridge + MCP) with ports 19300/19301
[ ] npm install inside indesign-uxp-server
[ ] Download Mac adobepy binary + uv venv + dcc-mcp-photoshop
[ ] adobepy install-bridge photoshop → bridges/photoshop
[ ] Photoshop: Enable Developer Mode → restart PS
[ ] UDT Add Plugin → InDesign Bridge + Adobe Python Bridge → Load & Watch
[ ] Write start-photoshop-mcp.sh (Mac) ; keep bridge node process running
[ ] .cursor/mcp.json with Mac absolute paths + photoshop URL :8766/mcp
[ ] Smoke: InDesign Connected + create 8.5×8.5 doc
[ ] Smoke: curl :47391/health sessions≥1 ; :8766/v1/readyz dcc:true
[ ] Smoke: get_document_info on an open PSD
```

---

## 11) Upstream + Jon’s deeper docs (if you have the repo)

| Doc | What |
|-----|------|
| `tools/layout-mcp/SETUP.md` | InDesign + Affinity (Windows-proven) |
| `tools/layout-mcp/PHOTOSHOP-SETUP.md` | Photoshop adobepy (Windows-proven) |
| `.cursor/docs/ADOBE-CC-MCP-GUIDE.md` | Broader Adobe MCP watchlist |
| `AGENT-RUNBOOK.md` | Book production cold-start + print rules |
| `.cursor/docs/BOOK-PAGE-WORKFLOW.md` | Example full-book page/poem/image map |
| `.cursor/docs/ISSUES-RESOLVED.md` | Gotchas (sessions:0, encoding, etc.) |

---

## 12) License / expectations

- These bridges are **community / unofficial**. Adobe updates can break them — re-smoke after CC updates.
- There is **no** official “full Creative Cloud MCP suite.”
- Keep Creative Cloud Desktop installed for licensing even if you disable it at login for RAM.
- Agent automates documents; **you** own Load & Watch and creative approval.

---

## 13) One-liner for Claude Code / Cursor

> Set up local MCP control of Adobe InDesign and Photoshop on macOS using UXP Developer Tools: (1) Node InDesign bridge on ports 19300/19301 with plugin `com.ads.indesign-bridge`, (2) adobepy broker on 47391 + dcc-mcp-photoshop on 8766/mcp with plugin `com.adobepy.bridge.photoshop`. Creative Cloud Desktop must be signed in before UDT Load & Watch. Prefer UXP over COM. Follow ADOBE-TNYSE-WORKFLOW.md end-to-end, use Mac paths and bash start scripts, then smoke-test Connected + sessions≥1 + dcc:true.

---

*Compiled 2026-07-20 from The-Night-I-Met-Santa production setup (Jon). Mac install steps adapted for Tony — verify on hardware before production.*
