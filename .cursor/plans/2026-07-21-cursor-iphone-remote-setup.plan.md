---
name: ""
overview: ""
todos: []
isProject: false
---

# Plan: Cursor iPhone ↔ PC (Remote Control)

**Goal:** Talk to the agent on iPhone 17; agent edits this project; when you open the desktop IDE later, see the same work + conversation.

**Interactive checklist:** open canvas `cursor-iphone-remote-setup` beside chat (checkboxes persist).

**Docs:** https://cursor.com/docs/cloud-agent/mobile

---

## Part A — PC prep (once)

1. Confirm **paid** Cursor plan (Pro / Pro+ / Ultra) with Cloud Agents.
2. Update Cursor desktop to **≥ 3.9.8** (Help → Check for Updates).
3. Sign in with the **same account** you will use on iPhone.
4. Use **Privacy Mode** (not Legacy) — required for mobile/cloud.
5. Connect **GitHub** in [cursor.com/dashboard](https://cursor.com/dashboard) — Cursor GitHub App read-write on `jonbeatz/The-Night-I-Met-Santa`.
6. Confirm Git remote: `git remote -v` → `origin` → that repo.

---

## Part B — PC: Remote Control (before you leave)

1. Open **Agents Window** (Ctrl+Shift+P → “Agents”). Remote Control is **not** in classic IDE-only chat.
2. **Settings → Agents → enable Remote Control**.
3. Optional: enable **Keep this computer awake** (leave PC plugged in).
4. In the agent input: type **`/remote-control`**, then send a message (e.g. “Standing by for phone”).
5. Leave Cursor running; do **not** let Windows sleep / go offline.

---

## Part C — iPhone 17

1. Confirm **iOS 26+** (Settings → General → About).
2. Install **Cursor** from App Store: https://apps.apple.com/app/cursor/id6767085653
3. Sign in with the **same** Cursor account as PC.
4. If prompted → switch to **Privacy Mode**.
5. Open **inbox** → tap the Remote Control session from your PC.
6. Send a small test task; watch it stream.
7. Allow **notifications** (optional).

---

## Part D — When you come home

1. Open this project in the classic **IDE** (or Agents Window).
2. Open **Agents / Cloud Agents** → reopen the **same** session (phone history lives there, not always the old Chat tab).
3. Confirm files on disk (`git status`, docs/Media you asked for).

---

## Part E — Optional: Cloud Agents (PC off)

Use when the tower is packed away:

1. Phone → New agent → pick **The-Night-I-Met-Santa** repo + branch → Cloud machine.
2. Task → review diff/PR on phone.
3. Home → **pull/merge** that branch into local IDE.

**Note for this book:** Cloud is fine for docs/prompts. Prefer Remote Control for Photoshop / local Media / fal.

---

## One-line handoff

Agents Window → Settings → Agents → Remote Control on → `/remote-control` → continue on iPhone inbox.
