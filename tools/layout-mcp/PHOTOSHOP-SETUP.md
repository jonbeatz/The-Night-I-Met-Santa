# Photoshop MCP setup (UXP — not COM)

**Status:** **LIVE / smoke-tested 2026-07-20**  
**Authoritative for Photoshop agent control on this PC.**  
InDesign still owns gift print layout — see [`SETUP.md`](./SETUP.md). Watchlist context: [`.cursor/docs/ADOBE-CC-MCP-GUIDE.md`](../../.cursor/docs/ADOBE-CC-MCP-GUIDE.md).

**Default working folder (agent saves here):**  
`D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop`  
(= repo-relative `Xtraz/Adobe-Photoshop/`). Use for any `.psd` / intermediates the agent creates with Jon. Chops for InDesign still go to `Images/chopz/`; approved keepers → `Media/approved/`.

### Blank starters (PSD)

| File | Size @ 300 | Role |
|------|------------|------|
| `spread-page-template.psd` | 5250×2625 | Facing spreads — cyan TRIM / magenta SAFETY / orange FOLD |
| `single-page-template.psd` | 2625×2625 | One interior page — cyan TRIM / magenta SAFETY |
| `book-covers-template.psd` | 2625×2625 | Front **or** back cover art — same guides + hinge hints |
| *(no spine PSD)* | — | Spine width from Lulu after interior upload; one-piece casewrap |

**Path:** `Xtraz/Adobe-Photoshop/`  
**Shared use:** Duplicate → Save As · paint **ART** · hide orange MOCK lines for finals · type stays **live in InDesign** (Cormorant interiors / Cinzel cover title).

**Spread layers (bottom → top):** `white-bg` → `paper-base` → ART → trim/safety → fold → cloud → type L/R  
**Single layers:** `white-bg` → `paper-base` → ART → TRIM → SAFETY → cloud → type  
**Cover layers:** `white-bg` → `paper-base` → ART → TRIM → SAFETY → hinge hints → TITLE / CREDITS zones  

Full key: `Xtraz/Adobe-Photoshop/README.md` · `ISSUES-RESOLVED.md` · `AGENT-RUNBOOK.md`.

**Why UXP:** Windows COM to Photoshop 2026 fails on this PC (`0x80080005` / Server execution failed) — same class of failure as InDesign COM. Community COM MCPs (loonghao / alisaitteke) will **not** work until Adobe COM is repaired. **UXP WebSocket** matches our working InDesign path.

---

## Stack

| Piece | Role | Port / path |
|-------|------|-------------|
| **adobepy** broker | Rust JSON-RPC hub | `127.0.0.1:47391` |
| **UXP plugin** | Inside Photoshop | `tools/layout-mcp/photoshop-adobepy/bridges/photoshop/` |
| **dcc-mcp-photoshop** | MCP Streamable HTTP | `http://127.0.0.1:8766/mcp` |
| Cursor | `.cursor/mcp.json` → `photoshop` | `"url": "http://127.0.0.1:8766/mcp"` |

Package roots: `tools/layout-mcp/photoshop-adobepy/`  
- **Tracked:** `bridges/photoshop/`, `start-photoshop-mcp.ps1`, this doc  
- **Gitignored:** `.venv/`, `*.zip`, `adobepy-*-windows-x64/` (re-extract from [adobepy releases](https://github.com/dcc-mcp/adobepy/releases) if missing)

Versions locked at install: **adobepy 0.5.2** · **dcc-mcp-photoshop 0.1.37** · Photoshop **2026** (app version **27.8.0**, registry **200.0**)

---

## One-time install (DONE 2026-07-20)

1. Downloaded `adobepy-0.5.2-windows-x64.zip` → extracted under `photoshop-adobepy/`
2. `uv venv` + wheel install `adobepy` + `pip/uv` install `dcc-mcp-photoshop`
3. `adobepy install-bridge photoshop --dest …/bridges/photoshop`
4. Cursor `mcp.json` entry + `npm run layout:photoshop-mcp`
5. Jon: Preferences → Plugins → **Enable Developer Mode** only (Generator / Remote Connections **off** — not needed)
6. Jon: UDT **Add Plugin** → `bridges/photoshop/manifest.json` → **Load & Watch**
7. Jon: Photoshop → **Plugins → Adobe Python Bridge**
8. Smoke PASS (see below)

If the zip/venv is wiped: re-extract release, recreate venv, `adobepy install-bridge` again; plugin path stays the same for UDT.

---

## Cold-start (each session)

| Step | Who | Action |
|------|-----|--------|
| **1** | Jon | Photoshop **2026** open |
| **2** | Jon | Creative Cloud Desktop signed in (needed for UDT Load) |
| **3** | Agent / Jon | Launch **UXP Developer Tools** (often already running with InDesign) |
| **4** | Agent | `npm run layout:photoshop-mcp` (broker `:47391` + MCP `:8766`) — start **before** relying on an existing Watching plugin |
| **5** | **Jon** | UDT → **Load & Watch** (or **Reload** if already Watching) on **Adobe Python Bridge for Photoshop** (`com.adobepy.bridge.photoshop`) — agent cannot click Electron |
| **6** | Jon | Photoshop panel **Adobe Python Bridge** open / connected |
| **7** | Jon | Reload Cursor MCP if `photoshop` not green |
| **8** | Agent | Smoke: broker `"sessions":≥1` + `/v1/readyz` `"dcc":true` + document info |

**If Cursor is green but smoke fails (`sessions:0` / `dcc:false`):** broker was restarted after the plugin connected. **UDT Reload** on the PS bridge (not a full Photoshop quit). Then re-smoke.

**If Cursor Settings shows photoshop red / Error / Logout:** almost always MCP HTTP is down — start `npm run layout:photoshop-mcp` first. Then re-auth / toggle the MCP if Cursor still shows only `mcp_auth`. Then UDT Reload → smoke `sessions≥1` + `dcc:true`. CC + UDT Loaded does **not** start `:8766`.

### Preferences (Plugins page)

| Setting | Need? |
|---------|-------|
| **Enable Developer Mode** | **Yes** — required for UDT Load |
| Enable Generator | No |
| Enable Remote Connections | No (old Generator protocol — not our path) |
| Legacy Extensions | Leave as-is |

Developer Mode changes apply after **Photoshop restart**.

---

## Smoke checks (verified PASS 2026-07-20)

```powershell
curl.exe -s http://127.0.0.1:47391/health
# expect: "sessions":1 (or more), "status":"ok"

curl.exe -s http://127.0.0.1:8766/v1/readyz
# expect: "dcc":true, host_execution_bridge true (not 503)

# Optional tool call via HTTP:
curl.exe -s -X POST http://127.0.0.1:8766/v1/call -H "Content-Type: application/json" --data-raw "{\"tool_slug\":\"photoshop_document__get_document_info\",\"arguments\":{}}"
```

**Smoke doc used:** `spread-01-eyes-met-5250x2625-v3.psd`  
- **5250 × 2625** px · RGB · resolution *tag* 72 (metadata only — pixels = print 300 DPI)  
- **9 layers** incl. Spread-Pages-Frames, Guides, Text, Brushes, Spread-Pages*, Red, white-bg  

**Python SDK alternate** (same broker):

```powershell
$env:ADOBEPY_TOKEN='dev-token'
.\tools\layout-mcp\photoshop-adobepy\.venv\Scripts\python.exe -c "from adobe.photoshop import Photoshop; d=Photoshop(token='dev-token').active_document; print(d.name, d.width, d.height)"
```

### Agent / Cursor notes

- MCP skills are **lazy-loaded**: call `search_tools` / `load_skill` (`photoshop-document`, `photoshop-layers`, …) before document tools appear.
- Cursor’s tool picker can lag after `load_skill` — if `CallMcpTool` 404s, use HTTP `/v1/call` or reload MCP; bridge is still live.
- Plugin id: `com.adobepy.bridge.photoshop`

---

## npm

```powershell
npm run layout:photoshop-mcp      # broker (if needed) + MCP :8766  (keep running)
npm run layout:photoshop-broker   # broker only :47391
```

---

## Do not

- Do **not** use loonghao `photoshop-mcp-server` / alisaitteke COM on this PC until COM works  
- Do **not** dual-drive the same doc with Flue + this bridge  
- Do **not** enable Generator Remote Connections “just because” — unrelated to UXP  
- Do **not** treat Photoshop MCP as the gift **print** path — InDesign still owns type + Lulu PDF  
- Do **not** dump agent-made `.psd` into `Media/` or `Output/` by default — use **`Xtraz/Adobe-Photoshop/`** first; promote keepers to `Media/approved/` / chops to `Images/chopz/` when ready  

---

## Rejected on this PC (2026-07-20)

| Attempt | Result |
|---------|--------|
| loonghao COM + `PS_VERSION=2026` | Fail — `photoshop-python-api` map tops at **2025→190**; no 2026→200; COM `0x80080005` |
| Direct `Photoshop.Application` / `.200` | Fail — Server execution failed / Operation unavailable |
| Registry | Photoshop **200.0** present — ProgID registered; **COM runtime still broken** |
| alisaitteke primary | Skip — Windows path is COM; UXP addon is Neural Filters only |

**Lesson:** On this machine, Adobe desktop automation that works = **UXP bridge** (InDesign + Photoshop). Prefer UXP for any new Adobe app before COM.

---

## Good-to-know — export each layer as JPG (2026-07-20)

**Skill:** `.cursor/skills/Photoshop-Layer-Export/SKILL.md`  
**Script:** `scripts/ps-export-layers-jpg.py` · **npm:** `npm run ps:export-layers`

Solo-visibility loop (hide all → show one → export JPG named after layer → walk **up** the Layers panel). Verified on `Pugicorn-Book-Refrence.psb` → `Images/references/Pugicorn-Book-Refrence/cropped/` (18/18).

```powershell
npm run layout:photoshop-mcp   # if broker down
# Photoshop: open the .psd/.psb
npm run ps:export-layers -- --doc "My-File.psb" --out "Images\references\My-File\cropped"
```

Playbook card: `.cursor/docs/ISSUES-RESOLVED.md` → **Playbook — Export each Photoshop layer as JPG**.

