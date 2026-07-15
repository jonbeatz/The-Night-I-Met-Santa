# Hostinger Deploy — The-Night-I-Met-Santa

**Pre-flight:** Set `THE_NIGHT_I_MET_SANTA_DOMAIN`, `THE_NIGHT_I_MET_SANTA_WEB_ROOT`, `THE_NIGHT_I_MET_SANTA_APP_ROOT`, and `FTP_REMOTE_PATH` in `.env.local` before first go-live.

---

## Option A — GitHub Pages (preview)

If `.github/workflows/deploy-pages.yml` exists, push to `main` deploys to:

`https://jonbeatz.github.io/The-Night-I-Met-Santa/`

Local test: `$env:GITHUB_PAGES='true'; npm run build:pages`

---

## Option B — Hostinger Node.js (production domain)

| Step | Where | Action |
|------|-------|--------|
| 1 | Local | `npm run web:build` — verify exit 0 |
| 2 | Local | FTPS upload to `FTP_REMOTE_PATH` (staging) |
| 3 | Local (SSH) | Sync staging → `THE_NIGHT_I_MET_SANTA_APP_ROOT` |
| 4 | hPanel | Node.js **Restart** |
| 5 | Local | HTTP smoke on `https://THE_NIGHT_I_MET_SANTA_DOMAIN/` |

MSC full bible: `D:\Cursor_Projectz\MyStudioChannel\.cursor\docs\HOSTINGER-DEPLOY.md`

---

## Pitfalls

See `.cursor/docs/PITFALLS-HOSTINGER.md`

---

*Bootstrap template — 2026-07-15*
