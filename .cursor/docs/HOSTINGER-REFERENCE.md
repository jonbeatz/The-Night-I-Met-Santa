# Hostinger Reference — The-Night-I-Met-Santa

**Profile root:** D:\\Hermes\\projects\\The-Night-I-Met-Santa  
**hPanel:** [https://hpanel.hostinger.com/](https://hpanel.hostinger.com/)

---

## Environment keys (`.env.local`)

| Key | Purpose |
|-----|---------|
| `HOSTINGER_API_TOKEN` | Hostinger MCP — run `npm run sync:mcp-env` |
| `FTP_*`, `HOSTINGER_SSH_*` | FTPS + SSH deploy (shared account) |
| `THE_NIGHT_I_MET_SANTA_DOMAIN` | Live domain for this project |
| `THE_NIGHT_I_MET_SANTA_WEB_ROOT` | Remote public web root |
| `THE_NIGHT_I_MET_SANTA_APP_ROOT` | Node.js app root (if applicable) |

Credentials merge from JonBeatz master `.env.local` on bootstrap — **never commit**.

---

## MCP (global Cursor)

After `npm run sync:mcp-env`: `hostinger-hosting`, `hostinger-vps`, `hostinger-domains`, `hostinger-dns`

---

## Golden split

| Where | What |
|-------|------|
| **Local (this repo)** | build + FTPS + SSH sync |
| **hPanel browser** | Node.js **Restart** only |
| **MSC deploy** | Use `D:\Cursor_Projectz\MyStudioChannel` — not this repo |

See `.cursor/docs/HOSTINGER-DEPLOY.md` and `.cursor/skills/Hostinger-Ops/SKILL.md`.

---

*Bootstrap template — 2026-07-22*
