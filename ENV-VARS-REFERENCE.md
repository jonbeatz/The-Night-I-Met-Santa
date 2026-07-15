# ENV-VARS-REFERENCE.md — Shared Environment Variable Registry

Central registry of all environment variables used across JonBeatz, MyStudioChannel, and mobile-dev projects. Each var includes its source project, whether it's required, and where it's set.

## AI / LLM Stack

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| DEEPSEEK_API_KEY | Yes | JonBeatz, MSC | — | `.env.local` | DeepSeek V4 API provider key for LiteLLM |
| DEEPSEEK_API_KEY_NAME | No | JonBeatz | — | `.env.local` | Human-readable label for the API key |
| MSC_LITELLM_MASTER_KEY | Yes | JonBeatz, MSC | sk-jonbeatz-deepseek-2026 | `.env.local` | LiteLLM proxy local master key |
| MSC_LITELLM_PORT | No | JonBeatz, MSC | 4000 | `.env.local` | LiteLLM proxy port |
| MSC_LITELLM_CONFIG | Conditional | JonBeatz, MSC | config/litellm_config.yaml | `.env.local` | LiteLLM yaml config file path |
| MSC_LITELLM_START_NGROK | No | JonBeatz, MSC | 0 | `.env.local` | Set to 1 to enable ngrok tunnel for Cursor Agent |
| MSC_LITELLM_DATABASE_URL | No | MSC | — | `.env.local` | LiteLLM Postgres URL (currently unused — DB-less mode) |
| DISABLE_SCHEMA_UPDATE | No | JonBeatz, MSC | true | `.env.local` | Prevents LiteLLM schema migration on start |

## Telegram

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| TELEGRAM_BOT_TOKEN | Yes | JonBeatz | — | `.env.local` + profile .env | Telegram bot token for gateway |
| TELEGRAM_CHAT_ID | Yes | JonBeatz | — | `.env.local` + profile .env | Authorized iPhone chat ID |
| TELEGRAM_ALLOWED_USERS | Yes | JonBeatz | — | `.env.local` + profile .env | Comma-separated allowed user IDs |
| TELEGRAM_HOME_CHANNEL | No | JonBeatz | — | `.env.local` + profile .env | Default channel for outbound notifications |
| TELEGRAM_TIMEZONE | No | JonBeatz | America/Los_Angeles | `.env.local` + profile .env | Timezone for Telegram timestamps |

## LM Studio / Local LLM

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| LMSTUDIO_HOST | No | JonBeatz | 127.0.0.1 | `.env.local` | LM Studio host |
| LMSTUDIO_PORT | No | JonBeatz | 1234 | `.env.local` | LM Studio port |
| LMSTUDIO_MODEL | No | JonBeatz | qwen3-4b-instruct-2507 | `.env.local` | Default LM Studio model |
| LMSTUDIO_CONTEXT_LENGTH | No | JonBeatz | 16384 | `.env.local` | LM Studio context window (VRAM-safe on 16 GB) |
| HERMES_LM_MODEL | No | JonBeatz | qwen3-4b-instruct-2507 | `.env.local` | Hermes local model override |
| HERMES_LM_CONTEXT | No | JonBeatz | 16384 | `.env.local` | Hermes local context length |
| HERMES_LM_PARALLEL | No | JonBeatz | 1 | `.env.local` | Parallel LM slots (1 = single-user, saves VRAM) |
| HERMES_LOCAL_CONTEXT_LENGTH | No | JonBeatz | 16384 | `.env.local` | Local mode context (unused if DeepSeek active) |
| HERMES_DEEPSEEK_CONTEXT_LENGTH | No | JonBeatz | 1000000 | `.env.local` | DeepSeek mode context (1M tokens) |

## Hermes Desktop / Agent

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| HERMES_AGENT_TIMEOUT | No | JonBeatz | 3600 | profile .env | Agent idle timeout (seconds) |
| HERMES_AGENT_TIMEOUT_WARNING | No | JonBeatz | 1800 | profile .env | Agent idle warning threshold (seconds) |

## Mem0 (Memory Store)

Per-project isolation: Each project uses its own Mem0 collection and Qdrant path, configured in `.env.local`. This prevents memory cross-contamination between profiles.

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| MEM0_USER_ID | Required | Any | the-night-i-met-santa | `.env.local` | Mem0 user/namespace identifier |
| MEM0_COLLECTION | Required | Any | the-night-i-met-santa_memories | `.env.local` | Mem0 collection name |
| MEM0_QDRANT_PATH | Required | Any | %USERPROFILE%\.mem0\qdrant_the-night-i-met-santa | `.env.local` | Local Qdrant vector store path |
| MEM0_API_KEY | Required | Any | — | `.env.local` | Mem0 API key for local service |
| MEM0_LM_MODEL | No | mobile-dev | (inherits HERMES_LM_MODEL) | `.env.local` | Optional Mem0 model override |

## Hugging Face / Image Generation

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| HF_TOKEN | Conditional | JonBeatz | — | `.env.local` | Hugging Face inference API token |
| HF_TOKEN_NAME | No | JonBeatz | — | `.env.local` | Human-readable key label |
| HF_IMAGE_MODEL | No | JonBeatz | black-forest-labs/FLUX.1-schnell | `.env.local` | Default HF image model |
| IMAGE_OUTPUT_DIR | No | JonBeatz | ./public/media | `.env.local` | Image output directory |
| IMAGE_DEFAULT_WIDTH | No | JonBeatz | 1024 | `.env.local` | Default image width |
| IMAGE_DEFAULT_HEIGHT | No | JonBeatz | 1024 | `.env.local` | Default image height |

## ComfyUI (Local GPU Pipeline)

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| COMFYUI_HOST | No | JonBeatz | 127.0.0.1 | `.env.local` | ComfyUI host |
| COMFYUI_PORT | No | JonBeatz | 8188 | `.env.local` | ComfyUI port |
| COMFYUI_ROOT | Required (if used) | JonBeatz | H:\AI_Models\ComfyUI | `.env.local` | ComfyUI installation root |
| COMFYUI_MAIN | Required (if used) | JonBeatz | %COMFYUI_ROOT%\ComfyUI | `.env.local` | ComfyUI main directory |
| COMFYUI_WORKFLOWS_DIR | No | JonBeatz | %COMFYUI_ROOT%\workflows | `.env.local` | ComfyUI workflows directory |
| COMFYUI_MODELS_DIR | No | JonBeatz | %COMFYUI_ROOT%\ComfyUI\models | `.env.local` | ComfyUI models directory |
| VRAM_WARN_PERCENT | No | JonBeatz | 65 | `.env.local` | VRAM warning threshold |
| VRAM_BLOCK_MB | No | JonBeatz | 10240 | `.env.local` | VRAM block size in MB |
| JONBEATZ_COMFYUI_AUTO_START | No | JonBeatz | 0 | `.env.local` | Auto-start ComfyUI on boot |

## FAL.ai (Bonus Image Gen)

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| FAL_API_KEY | Conditional | JonBeatz | — | `.env.local` | fal.ai API key |
| FAL_API_KEY_NAME | No | JonBeatz | — | `.env.local` | Human-readable key label |
| FAL_IMAGE_MODEL | No | JonBeatz | fal-ai/flux/schnell | `.env.local` | Default fal image model |

## Draven Voice (TTS)

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| DRAVEN_VOICE | No | JonBeatz | omnivoice | `.env.local` | Primary TTS engine |
| DRAVEN_VOICE_FALLBACK | No | JonBeatz | edge | `.env.local` | Fallback TTS engine |
| DRAVEN_VOICE_POLICY | No | JonBeatz | ritual | `.env.local` | When to speak (ritual, always, never) |
| DRAVEN_VOICE_ERRORS | No | JonBeatz | 1 | `.env.local` | Speak errors aloud |
| OMNIVOICE_PYTHON | Conditional | JonBeatz | — | `.env.local` | OmniVoice Python path |
| DRAVEN_OMNI_PORT | No | JonBeatz | 18776 | `.env.local` | OmniVoice daemon port |
| DRAVEN_OMNI_HOST | No | JonBeatz | 127.0.0.1 | `.env.local` | OmniVoice daemon host |
| DRAVEN_OMNI_MODEL | No | JonBeatz | k2-fsa/OmniVoice | `.env.local` | OmniVoice model |
| DRAVEN_OMNI_OUTPUT_DIR | No | JonBeatz | D:/Hermes/assets/audio/generated | `.env.local` | Audio output directory |
| DRAVEN_OMNI_STOP_ON_END | No | JonBeatz | 1 | `.env.local` | Stop daemon on End Project (0|1) |
| DRAVEN_OMNI_INSTRUCT | No | JonBeatz | male, low pitch, british accent | `.env.local` | Speaker instruction |
| DRAVEN_OMNI_STEPS | No | JonBeatz | 16 | `.env.local` | TTS inference steps (short) |
| DRAVEN_OMNI_STEPS_MEDIUM | No | JonBeatz | 24 | `.env.local` | TTS inference steps (medium) |
| DRAVEN_OMNI_STEPS_LONG | No | JonBeatz | 32 | `.env.local` | TTS inference steps (long) |
| DRAVEN_OMNI_GUIDANCE | No | JonBeatz | 1.5 | `.env.local` | Classifier-free guidance scale |
| DRAVEN_OMNI_MIN_STD | No | JonBeatz | 0.03 | `.env.local` | Minimum standard deviation (voice quality) |
| DRAVEN_OMNI_MIN_PEAK | No | JonBeatz | 0.02 | `.env.local` | Minimum peak threshold |

## Draven Memory (AI Assistant — Cross-Session)

These vars are used by `scripts/draven-mem0.ps1` — you typically don't need to set them manually unless you want a different collection name.

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| DRAVEN_MEM0_USER_ID | No | JonBeatz | draven | `draven-mem0.ps1` (hardcoded) | Draven's Mem0 user ID |
| DRAVEN_MEM0_COLLECTION | No | JonBeatz | draven_memories | `draven-mem0.ps1` (hardcoded) | Draven's Mem0 collection name |
| DRAVEN_MEM0_QDRANT_PATH | No | JonBeatz | %USERPROFILE%\.mem0\qdrant_draven | `draven-mem0.ps1` (hardcoded) | Draven's Qdrant storage path |

Draven's memory is **shared across all projects** — it's not per-project isolated like `MEM0_USER_ID`/`MEM0_COLLECTION`. Use `npm run draven:add/search/list` from any project.

## Stripe / Payment

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| STRIPE_API_KEY | Conditional | MCP config | — | `.env.local` | Stripe API key (sk for server, pk for client) |

## Ngrok Tunnel

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| NGROK_AUTHTOKEN | Required (tunnel) | JonBeatz, MSC | — | `.env.local` | Ngrok auth token |
| MSC_NGROK_BIN | No | MSC | — | `.env.local` | Path to ngrok binary (overrides auto-detect) |

## OpenRouter (fallback)

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| OPENROUTER_API_KEY | No | MSC | — | `.env.local` | OpenRouter API key (fallback provider) |

## MCP Servers (Cursor AI Tools)

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| 21ST_DEV_MAGIC_API_KEY | Conditional | JonBeatz, MSC | — | `.env.local` | 21st.dev UI component registry |
| BROWSERBASE_API_KEY | Conditional | JonBeatz, MSC | — | `.env.local` | Browserbase cloud browser automation |
| BROWSERBASE_PROJECT_ID | Conditional | JonBeatz, MSC | — | `.env.local` | Browserbase project ID |
| COMPOSIO_API_KEY | No | JonBeatz, MSC | — | `.env.local` | Composio social integration platform |
| GITHUB_PERSONAL_ACCESS_TOKEN | Conditional | JonBeatz, MSC | — | `.env.local` | GitHub PAT for MCP tools |
| TAVILY_API_KEY | Conditional | JonBeatz, MSC | — | `.env.local` | Tavily search API |
| STRIPE_API_KEY | Conditional | Any | — | `.env.local` | Stripe API key for MCP payment tools |
| FIRECRAWL_API_KEY | Conditional | Node-Launcher-v2 | — | `.env.local` | Firecrawl web scraping API for MCP tools |
| GROQ_API_KEY | Conditional | JonBeatz | — | `%USERPROFILE%\.config\watch\.env` | claude-video Whisper fallback (caption-less videos) |

## Hermes Agent (Desktop)

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| HERMES_AGENT_TIMEOUT | No | JonBeatz | 3600 | Profile `.env` | Agent idle timeout (seconds) |
| HERMES_AGENT_TIMEOUT_WARNING | No | JonBeatz | 1800 | Profile `.env` | Agent idle warning threshold (seconds) |

## Hostinger / Deploy

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| HOSTINGER_API_TOKEN | Required (MSC deploy) | JonBeatz, MSC | — | `.env.local` | Hostinger hPanel API token |
| FTP_HOST | Required (FTP deploy) | MSC | — | `.env.local` | FTP server host |
| FTP_USERNAME | Required (FTP deploy) | MSC | — | `.env.local` | FTP username |
| FTP_PASSWORD | Required (FTP deploy) | MSC | — | `.env.local` | FTP password |
| FTP_PORT | No | MSC | 21 | `.env.local` | FTP port |
| FTP_REMOTE_PATH | Required (FTP deploy) | MSC | /nodejs | `.env.local` | FTP remote base path |
| HOSTINGER_SSH_HOST | Required (SSH deploy) | MSC | — | `.env.local` | Hostinger SSH host |
| HOSTINGER_SSH_PORT | No | MSC | 65002 | `.env.local` | Hostinger SSH port |
| HOSTINGER_SSH_USER | Required (SSH deploy) | MSC | — | `.env.local` | Hostinger SSH user |
| HOSTINGER_SSH_PASSWORD | Required (SSH deploy) | MSC | — | `.env.local` | Hostinger SSH password |
| HOSTINGER_APP_ROOT | Required (MSC) | MSC | — | `.env.local` | Remote app root directory |
| MSC_BACKUP_ROOT | Required (MSC) | MSC | — | `.env.local` | MSC backup destination |

## Project / Profile

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| JONBEATZ_BACKUP_ROOT | Required (JonBeatz) | JonBeatz | — | `.env.local` | Profile backup destination root |
| MSC_REPO_ROOT | Required (MSC) | JonBeatz | D:\Cursor_Projectz\MyStudioChannel | `.env.local` | MSC repository root path |
| AI_MODELS_ROOT | No | JonBeatz | H:\AI_Models | `.env.local` | AI models base directory — **fleet default for weights ≥2GB** (Wan2.1, ComfyUI checkpoints, large LLMs) |
| RESEND_API_KEY | Conditional | MSC | — | `.env.local` | Resend transactional email API key |
| AGENTMAIL_API_KEY | Conditional | Next-Flick, Hermes agents | — | `.env.local` | [AgentMail](https://www.agentmail.to/) — AI agent email inboxes (2-way threads, OTP, attachments); free tier at agentmail.to |
| GEMINI_API_KEY | No | JonBeatz | — | `.env.local` | Google Gemini API key (unused) |
| PAYLOAD_SECRET | Required (MSC) | MSC | — | `.env.local` | Payload CMS secret key |
| DATABASE_URL | Required (MSC) | MSC | file:./payload.sqlite | `.env.local` | Payload database URL |

## n8n (local workflow automation)

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| N8N_HOST | Yes (local UI) | Profile | 127.0.0.1 | n8n `.env` / start bat | Host used in URLs / webhooks (does **not** bind the socket alone) |
| N8N_LISTEN_ADDRESS | Yes (security) | Profile | 127.0.0.1 | n8n `.env` / start bat | **Actual listen bind** — set to `127.0.0.1` (v2 default is `::`) |
| N8N_PORT | Yes | Profile | 5678 | n8n `.env` | HTTP port |
| N8N_ENCRYPTION_KEY | Yes | Profile | — | n8n `.env` | Credential encryption (never commit) |
| N8N_USER_FOLDER | Yes | Profile | — | n8n `.env` | Data directory (workflows / SQLite) |
| N8N_OWNER_PASSWORD | Conditional | Profile helpers | — | profile `.env.local` | Password for `scripts/n8n_*.py` API helpers (never commit) |
| WEBHOOK_URL | No | Profile | http://127.0.0.1:5678/ | n8n `.env` | Public webhook base (use localhost for local-only) |
| EXTENDED_HEALTH_HOST | No | Sidecar | 127.0.0.1 | process env | Extended Health sidecar bind host |
| EXTENDED_HEALTH_PORT | No | Sidecar | 5699 | process env | Extended Health sidecar port |
| EXTENDED_HEALTH_DISK | No | Sidecar | D | process env | Drive letter for free-space check |
| EXTENDED_HEALTH_DISK_MIN | No | Sidecar | 10 | process env | Fail if free % ≤ this |
| EXTENDED_HEALTH_PROFILE | No | Sidecar | — | process env | Hermes profile name required in `hermes gateway list` |
| NGROK_API_URL | No | Sidecar | http://127.0.0.1:4040/api/tunnels | process env | ngrok inspector API |
| HERMES_EXE | No | Sidecar | auto | process env | Absolute path to hermes.exe |

## JonBeatz Static Sites (Hostinger)

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| JONBEATZ_DOMAIN | Required | JonBeatz | — | `.env.local` | jon-beatz.com domain |
| JONBEATZ_WEB_ROOT | Required | JonBeatz | — | `.env.local` | Remote web root on Hostinger |
| JONBEATZ_DEPLOY_METHOD | No | JonBeatz | static-mcp | `.env.local` | Deploy method for jon-beatz.com |
| JONBEATZ_DEV_DOMAIN | Required | JonBeatz | — | `.env.local` | jonbeatz.dev domain |
| JONBEATZ_DEV_WEB_ROOT | Required | JonBeatz | — | `.env.local` | Remote web root on Hostinger |
| JONBEATZ_DEV_DEPLOY_METHOD | No | JonBeatz | static-mcp | `.env.local` | Deploy method for jonbeatz.dev |
| NEXT_PUBLIC_JB_VARIANT | Required | JonBeatz | — | `.env.local` | Site variant (gold | dev) |

## Workstation Paths

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| HERMES_DEEPSEEK_API | No | JonBeatz | _core-scripts/deepseek-api | `.env.local` | DeepSeek API scripts path |
| MSC_REPO_ROOT | No | MSC | D:\Cursor_Projectz\MyStudioChannel | `.env.local` | MSC repository root path |
| MSC_COMFY_SCRIPTS | No | MSC | — | `.env.local` | MSC ComfyUI custom scripts path |
| AI_MODELS_ROOT | No | JonBeatz | H:\AI_Models | `.env.local` | AI models base directory — **fleet default for weights ≥2GB** (Wan2.1, ComfyUI checkpoints, large LLMs) |
| AI_MODELS_CACHE | No | JonBeatz | H:\AI_Models | `.env.local` | AI models cache directory |

## Mobile Dev (Flutter)

| Variable | Required? | Source | Default | Set in | Purpose |
|----------|-----------|--------|---------|--------|---------|
| APP_NAME | Required | mobile-dev | — | `.env.local` | Flutter app display name |
| DART_PACKAGE | Required | mobile-dev | — | `.env.local` | Dart package name |
| BUNDLE_ID | Required (iOS) | mobile-dev | — | `.env.local` | iOS bundle ID |
| FLUTTER_HOME | Required | mobile-dev | — | `.env.local` | Flutter SDK installation path |
| ANDROID_HOME | Required (Android) | mobile-dev | — | `.env.local` | Android SDK installation path |
| EMULATOR_AVD | Recommended (Android) | mobile-dev | — | `.env.local` | Android emulator AVD name |
| JEDI_IOS_BACKUP_ROOT | Required | mobile-dev | — | `.env.local` | Per-project backup destination |

---

## Tools & MCP setup status

For **READY vs NEEDS_KEY** per tool (production stack + watchlist), see:

> [docs/TOOLS-SETUP-STATUS.md](./docs/TOOLS-SETUP-STATUS.md)

Grades and one-line summaries: [docs/TOOLS-WATCHLIST.md](./docs/TOOLS-WATCHLIST.md)

**Tool chest:** [docs/TOOL-CHEST-INDEX.md](./docs/TOOL-CHEST-INDEX.md) · **Regenerate secrets map:** `npm run ecosystem:audit`

---

## How to use this reference

1. **For a new project:** Copy `.env.local.example` from the shared template, then uncomment and set the vars relevant to your project.
2. **When adding a new service:** Add its vars here first, then implement in your project.
3. **Drift detection:** Run `check-shared-version.ps1` to verify your project's env matches the shared registry.
