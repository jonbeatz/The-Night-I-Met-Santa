# Layout MCP setup — Affinity + InDesign (TNIMS)

**Project:** `D:\Hermes\projects\The-Night-I-Met-Santa`
**Cursor config:** `.cursor/mcp.json` (this repo)
**Cloned tools:** `tools/layout-mcp/`

---

## Status (2026-07-16)

| Server | Wired in mcp.json | Ready when… |
|--------|-------------------|-------------|
| **affinity** | Yes | Affinity open + MCP toggles on (you did this) · port **6767** listening ✓ |
| **indesign-uxp** | Yes (primary) | Bridge on **19300/19301** + UXP plugin **Connected** (one-time load) |
| **indesign-exec** | Yes (fallback) | COM currently **fails** (`Server execution failed`) even with InDesign 2026 running — do not rely on it yet |

Ports **19300/19301** are intentional — classic UXP samples use 3000/3001 which collide with Next.js.

---

## Affinity (already mostly done)

1. Affinity open → Edit → Settings → Model Context Protocol → all ON ✓
2. Cursor → reload MCP / restart Cursor window so `affinity` server starts via `uvx mcp-proxy`.
3. Optional helpers:
   ```powershell
   cd tools\layout-mcp\affinity-scripting
   npx @modelcontextprotocol/inspector --sse http://127.0.0.1:6767/sse
   node extract_docs.js   # pulls SDK docs into docs/
   ```

**Best use:** open an existing `.afpub`, ask agent to place images / adjust layout / save script. Weak for inventing a full book from scratch.

---

## InDesign UXP (do once)

### Can we use [adobe-uxp/devtools-cli](https://github.com/adobe-uxp/devtools-cli)?

**Not for InDesign on this machine.** Honest findings (2026-07-16):

| Fact | Detail |
|------|--------|
| Official host matrix | Photoshop + XD only; **InDesign not listed**; Illustrator “not available yet” |
| Last release | **1.5.1** (Feb 2022) — targets Node ~12 |
| Install here | `yarn install` **failed** on Node 24 (`robotjs` native build error) |
| Adobe’s InDesign docs | Point to **UXP Developer Tool (UDT) GUI** from Creative Cloud, not this CLI — [InDesign UXP Dev Tools](https://developer.adobe.com/indesign/uxp/introduction/essentials/dev-tools/) |

Repo is cloned under `tools/layout-mcp/devtools-cli/` for reference only. **Do not** rely on `uxp plugin load` for our Bridge.

### A. Install Adobe UXP Developer Tools (UDT) — required

1. Open **Creative Cloud** desktop app
2. **All apps** → find **UXP Developer Tools** → **Install**
3. Launch UDT → enable **Developer Mode** when prompted (needs admin)

### B. Start the bridge (keep this terminal open)

```powershell
cd D:\Hermes\projects\The-Night-I-Met-Santa\tools\layout-mcp\indesign-uxp-server\bridge
$env:INDESIGN_BRIDGE_HTTP_PORT=19300
$env:INDESIGN_BRIDGE_WS_PORT=19301
node server.js
```

Or: `npm run layout:indesign-bridge` from project root.

### C. Load the UXP plugin (UDT GUI)

1. Open **UXP Developer Tools**
2. **Add Plugin** → select:
   `tools\layout-mcp\indesign-uxp-server\plugin\manifest.json`
3. Click **Load**
4. In InDesign: **Plugins → InDesign Bridge** → panel should say **Connected to bridge ✓**

### D. Cursor

Reload MCP. Server `indesign-uxp` auto-starts the bridge if not running (check ports 19300/19301).

---

## Lulu print assets

Downloaded under `Xtraz\Lulu-Templates\` (gitignored with rest of Xtraz):

| File | What |
|------|------|
| `lulu-book-creation-guide.pdf` | Official book creation guide (~2.5 MB) |
| `*-bleed*.html`, `hardcover-casewrap.html`, etc. | Help articles saved locally |
| See also `.cursor/docs/LULU-8.5-SQUARE-CHEATSHEET.md` | Project-specific 8.5×8.5 numbers |

**Note:** Lulu’s **exact cover wrap PDF** (with spine width) is generated **after** you upload an interior PDF on lulu.com — cannot pre-download a perfect spine for unknown page count. Use cheatsheet + Lulu calculator once page count locks (~32).

---

## Recommended workflow for this book

1. Keep generating art **page-by-page** (Gemini + G0s).
2. Place finals in Affinity **or** InDesign for typography/spreads when you want DTP polish.
3. Pillow cloud composite remains the proven text-on-art path until DTP A/B wins.
4. Export press PDF → Lulu.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Affinity MCP tools missing in Cursor | Affinity running? 6767 open? Reload Cursor MCP |
| InDesign Bridge not Connected | Bridge terminal running? Plugin loaded? Port 19301? |
| COM / indesign-exec fails | Known on this machine today — use UXP path |
| Port 3000 conflict | We remapped UXP to 19300/19301 — do not revert |
