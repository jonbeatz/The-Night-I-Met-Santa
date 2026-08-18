# Image Workflow — Hermes fleet (shared workstation)

**Hub profile:** `D:\Hermes\projects\JonBeatz` (Command Center)  
**Canonical model inventory:** [COMFYUI-MODELS.md](./COMFYUI-MODELS.md) → [ENGINEERING.md](./ENGINEERING.md)  
**VRAM playbook:** [VRAM-IMAGE.md](./VRAM-IMAGE.md) → [ENGINEERING.md](./ENGINEERING.md)  
**Environment:** profile `.env.local` (from `.env.local.example` — run `npm run env:setup`)  
**Vault picker:** `H:\Vader_Vault\02_Knowledge\Patterns\Local-image-model-picker-16GB.md`

This is the **fleet agent source of truth** for Hugging Face cloud generation + fal + local ComfyUI editing, upscaling, and video on the shared RTX 16 GB box.

---

## Two pipelines (when to use which)

| Goal | Pipeline | VRAM | Speed | Cost |
|------|----------|------|-------|------|
| Quick photorealistic still (1024²) | **Hugging Face** `image:gen` / FLUX.1-schnell | **0** (cloud) | ~10–15 s | Free/cheap (HF token) |
| Paid bonus still / premium models | **fal.ai** `image:fal` | **0** (cloud) | ~5–30 s | Pay-per-use (~$0.003+ / image) |
| Local GPU txt2img, edit, inpaint, upscale, video | **ComfyUI** @ `:8188` | Uses GPU | 30 s – 5 min | $0 API |

**Rule:** Prefer **HF cloud** when LM Studio is loaded or VRAM is tight. Use **fal** for premium models (Nano Banana 2, GPT Image 2) or when HF is capped. Use **ComfyUI** when Jon asks for local GPU, img2img, inpaint, upscale, or video.

---

## Environment setup (first time)

```powershell
cd D:\Hermes\projects\JonBeatz
npm run env:setup          # creates .env.local; merges HF_TOKEN from MSC if present
npm run image:doctor       # HF_TOKEN, Comfy paths, Python deps + vault↔Comfy hardlink health
pip install huggingface_hub pillow python-dotenv
```

Required in **`.env.local`:**

| Variable | Purpose |
|----------|---------|
| `HF_TOKEN` | Hugging Face Inference API (FLUX.1-schnell) |
| `FAL_API_KEY` | fal.ai pay-per-use wallet ([fal.ai](https://fal.ai/pricing)) |
| `FAL_IMAGE_MODEL` | Default fal model id for `image:fal` (default `fal-ai/flux/schnell`) |
| `COMFYUI_ROOT` | Shared install `H:\AI_Models\ComfyUI` |
| `IMAGE_OUTPUT_DIR` | Hermes media vault `D:\Hermes\assets\media\JonBeatz` |
| `LMSTUDIO_*` / `MEM0_*` | Personal memory stack |

---

## Quick reference card

| What Jon wants | Command (JonBeatz) | Where it runs |
|----------------|-------------------|---------------|
| Cloud image from text | `npm run image:gen -- "prompt"` | Hugging Face API |
| Cloud image + open viewer | `npm run image:gen:open -- "prompt"` | HF + default photo app |
| **Paid bonus** cloud image | `npm run image:fal -- "prompt"` | fal.ai API (prepaid credits) |
| **Paid bonus** + open | `npm run image:fal:open -- "prompt"` | fal.ai + viewer |
| **Kling scroll clip** (start + end stills) | `npm run video:fal -- -StartImage a.png -EndImage b.png` | fal.ai queue |
| Start ComfyUI | `npm run comfy:start` | Local GPU :8188 |
| Stop ComfyUI (keep LM Studio) | `npm run comfy:stop` | Local |
| ComfyUI status JSON | `npm run comfy:status` | Local |
| Repair model hardlinks (post H: migration) | `npm run comfy:repair-symlinks` | Local |
| Check vault↔Comfy hardlinks only | `npm run comfy:hardlink-check` | Local |
| Full model comparison test | `npm run comfy:compare -- "prompt"` | Local GPU |
| LM Studio vault audit | `npm run lmstudio:audit` | Local |
| Health check (env + hardlinks) | `npm run image:doctor` | Local |
| ComfyUI web UI | Browser → http://127.0.0.1:8188 | Local |

### PowerShell profile commands (workstation-wide)

These live in Jon's **PowerShell profile** (shared with MSC). They call ComfyUI workflows under `H:\AI_Models\ComfyUI\workflows\`:

| Command | Purpose |
|---------|---------|
| `gen-image "prompt"` | HF FLUX cloud (same as MSC — uses repo `.env.local` when run from JonBeatz) |
| `gen-image-local "prompt"` | ComfyUI z-image-turbo GGUF |
| `edit-image -InputPath ... -Prompt ...` | img2img |
| `inpaint-image -InputPath ... -MaskPath ...` | inpaint |
| `upscale-image -InputPath ... -TargetSize 4K` | upscale |
| `fix-face -InputPath ...` | face restore |
| `generate-video -Prompt ...` | CogVideoX T2V — **disabled** (see parked note below); use `video:fal` |
| `animate-image -InputPath ...` | SVD image-to-video (legacy local) |

**Natural language:** Jon can say *"make me a chicken playing golf"* → agent runs cloud `gen-image` or asks cloud vs local.

Full cheat sheet (all parameters): MSC [IMAGE-VIDEO-CHEATSHEET.md](file:///D:/Cursor_Projectz/MyStudioChannel/.cursor/docs/IMAGE-VIDEO-CHEATSHEET.md) — same workstation commands.

---

## A. Hugging Face cloud (`npm run image:gen`)

Architecture:

```
npm run image:gen → scripts/gen-image.ps1 → scripts/generate-image.py
  → reads .env.local HF_TOKEN
  → Hugging Face InferenceClient (FLUX.1-schnell)
  → saves PNG to IMAGE_OUTPUT_DIR
```

Examples:

```powershell
npm run image:gen -- "a beautiful recording studio with gold accent lighting, photorealistic, 4k"
npm run image:gen -- "cyberpunk city" -- --width 1920 --height 1080
powershell -File scripts/gen-image.ps1 "portrait of astronaut" -Width 1920 -Height 1080 -Open
```

Output default: `D:\Hermes\assets\media\JonBeatz\generated-YYYYMMDD-HHMMSS.png`

---

## C. fal.ai cloud bonus (`npm run image:fal`)

Pay-per-use prepaid wallet — use when HF is capped or Jon wants premium models. Docs: [fal.ai pricing](https://fal.ai/pricing).

**GUI alt (WATCH):** [Open Generative AI](https://github.com/Anil-matcha/Open-Generative-AI) @ `D:\Hermes\apps\Open-Generative-AI` + [muapi](https://muapi.ai) — OSS studio for 200+ cloud models (image/video/lip sync/cinema) + optional local **sd.cpp** (incl. Z-Image). Dev `:3000` only. Not default over HF/fal; see `TOOLS-REFERENCE.md` § Open Generative AI.

Architecture:

```
npm run image:fal → scripts/gen-image-fal.ps1 → scripts/generate-image-fal.py
  → reads .env.local FAL_API_KEY
  → POST https://fal.run/{model}
  → saves PNG to IMAGE_OUTPUT_DIR (fal-*.png)
```

**Cursor MCP:** `npm run sync:mcp-env` writes **fal-ai** to `%USERPROFILE%\.cursor\mcp.json` → reload Cursor Settings → MCP.

| Model id (fal) | Use | ~Cost |
|----------------|-----|-------|
| `fal-ai/flux/schnell` | Default cheap still (same family as HF) | ~$0.003 |
| `fal-ai/flux-2/klein/4b` | **Picture-book dial** — cheap gouache iterates | ~$0.009/MP |
| `fal-ai/qwen-image-2/text-to-image` | **Picture-book fallback** when Klein misses | ~$0.035/img |
| `fal-ai/nano-banana` | Fast Google, text in image | ~$0.08 @ 1K |
| `fal-ai/nano-banana-pro` | Hero / 4K / character consistency | $0.15–0.30 |
| `fal-ai/nano-banana-pro/edit` | **Picture-book finals** + style refs (`image_urls`) | ~$0.15/img |
| `fal-ai/gpt-image-2` | Product shots, layouts | ~$0.005–0.21 by quality |

### Picture books (Hermes book workflow)

Locked recipe pioneered on **The-Night-I-Met-Santa** — full playbook lives in that project’s `BOOK-PRODUCTION-SYSTEM.md`. For any future picture book on fal:

| Priority | Lane | Endpoint | When |
|:--------:|------|----------|------|
| 1 | Dial / dev | `fal-ai/flux-2/klein/4b` | Layout, vibe, text-zone probes |
| 2 | Fallback | `fal-ai/qwen-image-2/text-to-image` | Klein missed; before finals spend |
| 3 | Finals | `fal-ai/nano-banana-pro/edit` + style refs | Approved pages/covers @ 2K |

**Skip:** Ideogram for child Christmas / pajamas beats if fal safety blocks.  
**Evidence template:** one real-beat compare folder (same prompt/seed) before locking lanes.  
**Call path:** prefer Cursor MCP `user-fal-ai` over default `image:fal` (Flux schnell) for dial/finals.

Examples:

```powershell
npm run image:fal -- "cinematic studio hero, dark gold, music producer"
npm run image:fal:open -- "product card with readable text"
powershell -File scripts/gen-image-fal.ps1 "portrait" -Model "fal-ai/nano-banana"
powershell -File scripts/gen-image-fal.ps1 "book sneak beat" -Model "fal-ai/flux-2/klein/4b"
```

**Policy:** Daily stills → `image:gen` (HF). fal = bonus when Jon asks **or** book lanes above. Picture-book finals = Banana `/edit` + refs, not Flux schnell.

### Scroll transition video (`npm run video:fal`)

Kling I2V for assembled → exploded product clips. See vault `ai-scroll-product-workflow/WORKFLOW.md`.

```powershell
npm run video:fal -- -StartImage assembled.png -EndImage exploded.png
```

Check balance: [fal.ai/dashboard](https://fal.ai/dashboard).

**fal credits exhausted?** Local fallback (manual install): **LongCat-Video** → **HunyuanVideo** → ComfyUI `generate-video` → **LTX Desktop** (GUI NLE — Jon download later). Same FFmpeg → WebP → `ScrollFrameHero`. Details: `TOOLS-REFERENCE.md` § LongCat / HunyuanVideo / LTX Desktop · `SCROLL-VIDEO-RESEARCH.md` tool matrix.

**Wan2.1 local weights (parked research lane):** `H:\AI_Models\Wan2.1` — keep **both** `checkpoints` (~16 GB native) and `hf` (~27 GB Diffusers). Not duplicates to delete; Windows verify = `npm run wan21:status`. Production clips still default to **fal**.

**CogVideo (parked — keep ~3.3 GB I2V):** `H:\AI_Models\ComfyUI\ComfyUI\models\CogVideo\CogVideoX_5b_I2V_GGUF_Q4_0.safetensors`. Workflow `txt2vid-cogvideo.json` stays in `workflows\_disabled\` (needs separate T2V weights to revive). Jon 2026-08-08: **do not delete** — fun/local I2V later; daily video = **fal**. Details in that folder’s README.

### Video polish chain (after gen)

Canonical runbook: **[VIDEO-POLISH-CHAIN.md](./VIDEO-POLISH-CHAIN.md)**

```powershell
npm run video:polish -- -InputPath "D:\Hermes\apps\kinocut-media\inbox\clip.mp4"
npm run freecut:open   # optional human pass
```

Flow: fal/OpenMontage → **Kinocut** cut/QC → **FreeCut** (optional) → `polish-out\`.

---

## D. ComfyUI local workflow

### Start / stop (JonBeatz npm wrappers → MSC scripts)

JonBeatz delegates to the **shared MSC ComfyUI scripts** (same engine, same VRAM guards):

```powershell
npm run comfy:start              # VRAM pre-flight, then launch
npm run comfy:start -- -LowVram -UnloadLMStudio   # 16 GB GPU + LM Studio loaded
npm run comfy:stop               # ComfyUI only — does NOT kill LM Studio
npm run comfy:restart
npm run comfy:status
```

**Agent rule:** Never auto-start ComfyUI unless Jon asks or `COMFYUI_AUTO_START=1` (legacy `JONBEATZ_COMFYUI_AUTO_START=1` also OK). See `.cursor/rules/image-workflow.mdc`.

### Web UI

http://127.0.0.1:8188 — drag workflow PNGs to load graphs; debug node execution visually.

### App Mode (preferred easy GUI — 2026-08-08)

**Day-to-day local gens:** use official **ComfyUI App Mode** (no node graph). Requires ComfyUI frontend ≥1.41.13 (this stack: **0.31.0** / frontend **1.48.7**).

```powershell
npm run comfy:start
# heavy Qwen: npm run comfy:start -- -UnloadLMStudio -LowVram
# → open http://127.0.0.1:8188 → Workflows → Hermes-Fable5 → *-AppMode.json
# → stay in App mode → edit controls → Run → npm run comfy:stop
```

| Dial | App Mode workflow (user library) | Controls |
|------|----------------------------------|----------|
| **Fast Q4** | `z-image-turbo-Q4-AppMode.json` | Prompt · Negative · W/H · Seed · Steps |
| **Keep BF16** | `z-image-turbo-BF16-AppMode.json` | same |
| **Best 2512** | `qwen-image-2512-AppMode.json` | same |
| **Flux Klein 4B** | `flux-klein-4B-AppMode.json` | same |
| **Flux Klein 9B** | `flux-klein-9B-AppMode.json` | same |
| **Edit 2511** | `edit-qwen-2511-AppMode.json` | **Image** · Prompt · Negative · Seed · Steps · Denoise |

**Path:** `H:\AI_Models\ComfyUI\ComfyUI\user\default\workflows\Hermes-Fable5\`  
**Vault:** `ComfyUI-App-Mode-Fable5` · picker `Local-image-model-picker-16GB`  
**Smoke:** App Mode z-image Q4 PASS → `D:\Hermes\assets\media\JonBeatz\comfyui-appmode-20260808\`

Use **Graph mode** only when building/debugging nodes. API workflows under `H:\AI_Models\ComfyUI\workflows\` remain the CLI / graph source of truth.

### Default local txt2img workflow (graph / API)

| Goal | Workflow | Notes |
|------|----------|-------|
| **Fast dial (default)** | `txt2img-gen-image-local.json` / `txt2img-z-image-turbo.json` | z-image-turbo Q4 + Qwen3-4B CLIP + `ae.safetensors` — ~50s @ 1024, 8 steps |
| **Fast lane, final quality** | `txt2img-z-image-turbo-bf16.json` | z-image-turbo **BF16** (11.5 GB safetensors) — ~155s cold @ 1024. Q4 = iterate, BF16 = final |
| **Best quality / realism** | `txt2img-qwen-image-2512.json` | Qwen-Image-2512 Q4_K_M + Qwen2.5-VL-7B TE + `qwen_image_vae` — ~4 min @ 1024 / 20 steps |
| **Local instruction edit** | `edit-image-qwen-2511.json` | **Qwen-Image-Edit-2511** Q4_K_M (local nano-banana-style edits) + Qwen2.5-VL TE — set `OVERRIDE_INPUT_IMAGE.png` + prompt; 20 steps / cfg 2.5 |
| **Flux quality (fast)** | `txt2img-flux-klein-9b.json` | FLUX.2 Klein **9B** Q4 + **Qwen3-8B** TE + `flux2-vae` — ~90–100s (**non-commercial**) |
| **Flux speed / Apache** | `txt2img-flux-klein.json` | Klein **4B** Q5 + Qwen3-4B TE |

> **VRAM rule (16 GB):** the big Qwen models (2512, Edit-2511) fully load but crawl (~199 s/step) if LM Studio's qwen3-4b stays resident. **`lms unload qwen3-4b-instruct-2507` before heavy Qwen renders**, then `npm run mem0:preflight` to restore. Klein + both z-image variants run fine with it resident.

- **Profile command (fast):** `gen-image-local "prompt"`
- **ComfyUI:** **v0.31.0** · torch **2.11.0+cu128** (RTX 50 / Blackwell — **never** `pip install torch` from default PyPI)
- **Repair links:** `npm run comfy:repair-symlinks` (symlink → hardlink fallback on same H: volume; drops deleted `flux1-dev-Q4_K_M`, includes Edit-2511 + BF16)
- **Hardlink health:** `npm run comfy:hardlink-check` or `npm run image:doctor` (fails on broken critical Fable 5 links — see vault gotcha `LLM-VAULT-vs-AI-Models-hardlinks`)
- **Smoke outputs:** `D:\Hermes\assets\media\JonBeatz\comfyui-smoke-20260807\` · App Mode `comfyui-appmode-20260808\`

#### Local vs fal picture-book lanes

| Book stage (fal) | Local equivalent |
|------------------|------------------|
| Dial `fal-ai/flux-2/klein/4b` | Same family → Klein 4B GGUF (slightly softer) |
| Fallback `fal-ai/qwen-image-2/...` | Related only → **Qwen-Image-2512** (not identical to fal Qwen-Image-2) |
| Finals `fal-ai/nano-banana-pro/edit` | **Local edit lane now exists** → `edit-image-qwen-2511.json` (Qwen-Image-Edit-2511). fal stays default for book finals; local is the free/offline option |

#### LM Studio custom load settings (red-dot configs)

Stored under `%USERPROFILE%\.lmstudio\.internal\user-concrete-model-default-config\` (refresh My Models / restart LM Studio to see **Customized**):

| Model | Parallel | Context | GPU |
|-------|----------|---------|-----|
| flux-2-klein-9b / qwen-image-2512 / **qwen-image-edit-2511** / klein-4b / z-image-turbo | 1 | 4096 | offload **max** + flash attn + keep-in-memory + KV GPU |
| Qwen3-8B (Klein TE) | 1 | 8192 | max GPU |
| Qwen2.5-VL-7B (Qwen-Image TE) | 1 | 4096 | max GPU |

> **⚠️ Reality check (2026-08-08):** LM Studio's llama-server **cannot load diffusion GGUFs at all** (tested every image arch on newest engine 2.27.1 — all fail "exited before becoming healthy"). Image GGUFs index in My Models but never load; the dials above are **inert insurance** in case LMS ships diffusion support. **ComfyUI is the ONLY local image runtime.** Model root: `H:\LLM_VAULT` (`downloadsFolder`) — the legacy `~\.lmstudio\models` junction was removed 2026-08-08 (restore: `mklink /J` → `H:\AI_Models`).

### Edit / inpaint / upscale / video

Requires ComfyUI running. Use profile `edit-image`, `inpaint-image`, `upscale-image`, `generate-video`, `animate-image` — see cheat sheet above.

### Cursor MCP — local ComfyUI (`comfyui-mcp`)

**JonBeatz project MCP** — agent-native control of your **local** ComfyUI instance (not Comfy Cloud). Package: [`comfyui-mcp`](https://www.npmjs.com/package/comfyui-mcp) (community, local-first).

| Item | Value |
|------|-------|
| **Config** | `.cursor/mcp.json` → server `comfyui` |
| **Package** | `npx -y comfyui-mcp` (stdio MCP) |
| **Target** | `COMFYUI_URL=http://127.0.0.1:8188` (from `COMFYUI_HOST`/`PORT` in `.env.local`) |
| **Data path** | `COMFYUI_PATH` = `COMFYUI_ROOT` (e.g. `H:\AI_Models\ComfyUI`) |
| **Safety** | `COMFYUI_ALWAYS_RESTART=false` — MCP does **not** auto-launch ComfyUI |

**Setup (once):**

```powershell
cd D:\Hermes\projects\JonBeatz
# Copy .cursor/mcp.json.example → .cursor/mcp.json if missing; comfyui block is included
npm run sync:mcp-env    # writes COMFYUI_URL + COMFYUI_PATH from .env.local
```

Then **Cursor Settings → MCP → enable `comfyui`** and refresh servers.

**Agent workflow with MCP:**

1. Jon asks for local GPU work → run **`npm run comfy:start`** first (VRAM pre-flight).
2. Use **comfyui MCP tools** for workflow authoring, execution, model/node ops in natural language.
3. When done → **`npm run comfy:stop`** to free VRAM for LM Studio / Mem0.

**VRAM rules still apply:** MCP does not replace `comfy:start`/`comfy:stop` guards. Never start ComfyUI via MCP auto-restart unless Jon explicitly opts in. Cloud Comfy MCP (`cloud.comfy.org`) is **not** used in this stack.

---

## E. Complete recipe examples

### 1. Cloud generate → local upscale

```powershell
npm run image:gen -- "mountain landscape at sunset"
npm run comfy:start
# Then in profile or agent: upscale-image -InputPath "D:\Hermes\assets\media\JonBeatz\generated-*.png" -TargetSize 4K
npm run comfy:stop
```

### 2. Local generate → edit → stop ComfyUI

```powershell
npm run comfy:start
gen-image-local "futuristic studio desk, photorealistic"
edit-image -InputPath "D:\Hermes\assets\media\JonBeatz\generated-local-*.png" -Prompt "add gold accent lighting" -Strength 0.45
npm run comfy:stop
```

### 3. Mem0 + image session

After a good prompt/style Jon wants to reuse:

```powershell
npm run mem0:add -- "Preferred image style: gold accent studio lighting, photorealistic 4k, FLUX cloud"
```

---

## F. Model & path reference

| Resource | Path |
|----------|------|
| ComfyUI engine | `H:\AI_Models\ComfyUI\` |
| Workflows | `H:\AI_Models\ComfyUI\workflows\` |
| Model cache (H:) | `H:\AI_Models\` |
| JonBeatz outputs | `D:\Hermes\assets\media\JonBeatz\` |
| MSC outputs (website) | `D:\Cursor_Projectz\MyStudioChannel\public\media\` |
| Restore symlinks | `H:\AI_Models\ComfyUI\scripts\repair-comfyui-symlinks.ps1` |
| Download SD1.5 fp16 | `hf download Comfy-Org/stable-diffusion-v1-5-archive v1-5-pruned-emaonly-fp16.safetensors` → checkpoints folder |

See **[COMFYUI-MODELS.md](./COMFYUI-MODELS.md)** for full model matrix.

---

## E. Troubleshooting

| Issue | Fix |
|-------|-----|
| `HF_TOKEN not configured` | `npm run env:setup` then set token in `.env.local` |
| ComfyUI not reachable | `npm run comfy:start` then open :8188 |
| CUDA OOM | `npm run comfy:stop`; use `-LowVram`; reduce resolution; unload LM Studio |
| Missing checkpoint | Run restore scripts; see COMFYUI-MODELS.md |
| Wrong output folder | Check `IMAGE_OUTPUT_DIR` in `.env.local` |

---

## F. Agent instructions

1. Read **this file** before any image/video task in JonBeatz.
2. Run **`npm run image:doctor`** if env or ComfyUI state is unclear.
3. **Cloud first** unless Jon says local/GPU/ComfyUI.
4. **Stop ComfyUI** when done (`npm run comfy:stop`) to free VRAM for LM Studio / Mem0.
5. Save outputs under **`public/media/`** for personal work. This keeps assets served root-relatively by Next.js.
6. Log reusable prompts/styles to **Mem0** + **ReCall.md**.

---

*Last updated: 2026-08-08 · +App Mode Fable 5 (`Hermes-Fable5/*-AppMode.json`) · +Qwen-Image-Edit-2511 + z-image BF16 · LMS junction removed · LMS can't load diffusion GGUFs — ComfyUI only · ComfyUI 0.31 · cu128*
