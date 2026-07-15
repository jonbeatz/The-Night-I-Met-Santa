# Hostinger Pitfalls — The-Night-I-Met-Santa

| Mistake | Fix |
|---------|-----|
| Staging updated, live stale | Sync to `THE_NIGHT_I_MET_SANTA_APP_ROOT`, hPanel Restart |
| Partial `.next` upload | Upload complete build folder |
| Wrong repo for MSC deploy | MSC = MyStudioChannel; this profile = The-Night-I-Met-Santa |
| Committed `.env.local` | Never — gitignored |
| MCP red after env change | `npm run sync:mcp-env` + reload Cursor MCP |

---

*Bootstrap template — 2026-07-15*
