---
name: Image-Workflow
description: Hermes fleet Hugging Face + fal + ComfyUI image pipeline — cloud stills, local GPU edit/upscale, Fable 5 model dials
---

# Image Workflow (Hermes fleet)

Use this skill for image, inpaint, upscale, or video requests in any Hermes profile that shares the workstation ComfyUI stack.

## Read first

1. `.cursor/docs/IMAGE-WORKFLOW.md` — master guide (includes **App Mode**)
2. `.cursor/docs/ENGINEERING.md` — Comfy model inventory + VRAM (canonical; stubs `COMFYUI-MODELS.md` / `VRAM-IMAGE.md` redirect here)
3. Book projects: `IMAGE-LANE-SYSTEM-v2.md` + `LOCAL-COMFY-PICKER.md` when present
4. Vault: `[[Local-image-model-picker-16GB]]` · `[[ComfyUI-App-Mode-Fable5]]`

## Quick commands

```powershell
npm run env:setup           # first-time .env.local
npm run image:doctor        # env + vault<->Comfy hardlink health
npm run comfy:hardlink-check
npm run image:gen -- "prompt"   # HF cloud (if profile has it)
npm run image:fal -- "prompt"   # fal paid (if profile has it)
npm run comfy:start         # only when local GPU needed
npm run comfy:start -- -UnloadLMStudio -LowVram   # before heavy Qwen
npm run comfy:status
npm run comfy:stop
npm run mem0:preflight      # restore qwen3-4b after unload
```

## Decision tree

- **Fast still, VRAM tight, LM Studio up** → HF `image:gen` or fal
- **Book dials / print finals** → project IMAGE-LANE (usually fal Klein → Qwen → Banana Pro)
- **Local GPU / free offline (prompt → Run)** → ComfyUI **App Mode** (preferred) — Workflows → **Hermes-Fable5** → `*-AppMode.json`
- **Local GPU graph / CLI / debug** → same dials via `H:\AI_Models\ComfyUI\workflows\` API JSON
- **Best local quality** → Qwen-Image-2512 · **local edit** → Edit-2511 · **fast** → z-image Q4/BF16 · **Flux** → Klein 9B/4B
- **Done with ComfyUI** → `comfy:stop`

## App Mode (default easy path)

1. `npm run comfy:start` → http://127.0.0.1:8188
2. Open `Hermes-Fable5/<dial>-AppMode.json` (user library)
3. Stay in **App** mode → edit Prompt / size / seed → **Run**
4. Edit dial: `edit-qwen-2511-AppMode.json` (Image + Denoise)
5. `npm run comfy:stop` when finished

## Stack facts (2026-08-08)

- ComfyUI **0.31.0** · torch **2.11.0+cu128** · shared `H:\AI_Models\ComfyUI`
- Models: `H:\LLM_VAULT` GGUFs + hardlinks; BF16 under ComfyUI `diffusion_models/`
- App Mode files: `ComfyUI\user\default\workflows\Hermes-Fable5\*-AppMode.json`
- Never `pip install torch` from default PyPI on this box
## Outputs

`IMAGE_OUTPUT_DIR` → `D:\Hermes\assets\media\{ProjectName}`

## Related MSC docs (same workstation)

- `D:\Cursor_Projectz\MyStudioChannel\.cursor\docs\IMAGE-VIDEO-CHEATSHEET.md`
- `D:\Cursor_Projectz\MyStudioChannel\.cursor\docs\comfyui-setup.md`
