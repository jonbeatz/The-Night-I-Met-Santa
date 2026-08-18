# Local ComfyUI picker — The Night I Met Santa

**Updated:** 2026-08-08 (Fable 5 stack locked on shared workstation)
**Runtime:** ComfyUI only (`H:\AI_Models\ComfyUI` · `:8188`). LM Studio cannot load diffusion GGUFs.
**Fleet docs:** `.cursor/docs/IMAGE-WORKFLOW.md` · ENGINEERING · vault `[[Local-image-model-picker-16GB]]`

> **Book production default stays fal / IMAGE-LANE.** Local Comfy is for free/offline dials and instruction edits.

## Start / stop

```powershell
npm run comfy:start
npm run comfy:start -- -LowVram -UnloadLMStudio   # before Qwen-2512 / Edit-2511
http://127.0.0.1:8188
npm run comfy:stop
npm run mem0:preflight
```

**Outputs:** `D:\Hermes\assets\media\The-Night-I-Met-Santa` (promote keepers into project Media with RECIPE).

## Best local models

| Job | Workflow |
|-----|----------|
| Fast iterate | `txt2img-z-image-turbo.json` (Q4) |
| Fast keep | `txt2img-z-image-turbo-bf16.json` |
| Best quality | `txt2img-qwen-image-2512.json` |
| Local edit | `edit-image-qwen-2511.json` |
| Flux quality (NC) | `txt2img-flux-klein-9b.json` |
| Flux speed / Apache | `txt2img-flux-klein.json` |

Book finals still prefer fal **nano-banana-pro** when spending for print.
