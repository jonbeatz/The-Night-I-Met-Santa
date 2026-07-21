---
name: Photoshop-Layer-Export
description: Export each Photoshop layer as its own JPG (solo-visibility loop) via adobepy — book refs, comps, plate dumps
---

# Photoshop — export each layer as JPG

**Good-to-know skill** for this profile (dialed **2026-07-20** on `Pugicorn-Book-Refrence.psb`).

Use when Jon asks to: dump every layer to JPG/PNG, “eyeball each layer and save,” export a PSB/PSD stack as separate images named by layer.

## When to use

| Ask | Do this |
|-----|---------|
| Export each layer as JPG into a folder | This skill + script |
| One composite / chops for InDesign | `ISSUES-RESOLVED.md` chops playbook — not this |
| Gift print plates | InDesign path — not this |

## Prerequisites

1. Photoshop open with the **source `.psd` / `.psb` active** (or named in the command)
2. Broker + MCP up: `npm run layout:photoshop-mcp` · UDT plugin Watching
3. Output folder exists (script creates it)

## Canonical method (solo eyeball)

Photoshop does not export “each layer as file” cleanly for mixed smart-objects without compositing. Reliable approach:

1. List layers **top → bottom** (`doc.layers`)
2. Find the **currently visible** layer (or a start name Jon gives)
3. **Hide all** layers
4. For each layer in order (**start → up the panel** = toward top = decreasing index):
   - Show **only** that layer
   - `doc.export(path, format="jpg", as_copy=True)` (fallback `save_as` jpg copy)
   - Filename = **exact layer name** (sanitized) + `.jpg`
5. Leave last exported layer visible (or restore Jon’s pick)

## Run (from repo root)

```powershell
# Default: open Pugicorn PSB → cropped folder (example from first use)
npm run ps:export-layers

# Custom doc + out dir
npm run ps:export-layers -- --doc "My-File.psb" --out "Images\references\My-File\cropped"

# Start from a named layer, walk up the panel
npm run ps:export-layers -- --doc "My-File.psd" --out "D:\path\to\out" --start "Pugicorn-a"
```

Script: `scripts/ps-export-layers-jpg.py`  
Scratch origin: `scripts/_scratch/_ps_export_pugicorn_layers.py`

## Gotchas

| Issue | Fix |
|-------|-----|
| Console `UnicodeEncodeError` on Windows | Avoid fancy arrows in prints; set `$env:PYTHONIOENCODING='utf-8'` |
| Smart Object looks blank | Brief settle (`sleep 0.15`) after show; export still composites document pixels |
| Wrong order | Layers panel **up** = toward top = **lower index** in `doc.layers` |
| Orphan / wrong doc | Select document by name first (`batch_play` select) |
| JPG missing | Check `export()` then `save_as(..., format="jpg", as_copy=True)` |

## First verified run

- **Source:** `Images/references/Pugicorn-Book-Refrence/Pugicorn-Book-Refrence.psb` (1800×1466)
- **Out:** `Images/references/Pugicorn-Book-Refrence/cropped/`
- **Result:** 18/18 — `Pugicorn-a.jpg` … `Pugicorn-r.jpg`
- **Order:** started visible `Pugicorn-a`, walked up to `Pugicorn-r`

## Related docs

- `tools/layout-mcp/PHOTOSHOP-SETUP.md` — MCP stack
- `.cursor/docs/ISSUES-RESOLVED.md` — Playbook: export each layer as JPG
- `AGENT-RUNBOOK.md` — gift print still InDesign
