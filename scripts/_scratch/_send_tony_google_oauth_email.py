"""Send Tony the Google OAuth Hermes setup email (same pattern as Adobe workflow email)."""
from __future__ import annotations

import base64
import json
import mimetypes
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN = Path.home() / "AppData" / "Local" / "hermes" / "google_token.json"
ATTACH = Path(r"D:\Hermes\projects\JonBeatz\.cursor\docs\EMAIL-Tony-Google-OAuth-Hermes-Setup.md")
TO = "bigtee@gmail.com"
SUBJECT = "Google OAuth + Hermes setup (Gmail / Drive — same stack as Jon)"

BODY = """Hey Tony —

Jon asked me (Draven) to send you the follow-up to the Adobe + Cursor guide — this one unlocks the fully authenticated Google Workspace loop he’s been bragging about.

WHAT THIS IS
Attached: EMAIL-Tony-Google-OAuth-Hermes-Setup.md

It’s a click-through setup guide so you can wire Hermes + Cursor to YOUR Google account (your own GCP Desktop OAuth client — no shared secrets). When you’re done, your agent can:
  • Read / search / send Gmail
  • List & work with Google Drive / Docs / Sheets
  • Use Calendar (and optional YouTube scopes)
  • Keep tokens in the Hermes home folder so Hermes Desktop + Cursor both see them

Companion to: ADOBE-TNYSE-WORKFLOW.md (Adobe InDesign/Photoshop from Cursor).
This doc = Google auth. Adobe doc = Creative Cloud bridges.

Save the attachment in the project you’ll open in Cursor (or drop it in chat).

BEST PROMPT — paste into Cursor Agent after the file is loaded:

---
Read @EMAIL-Tony-Google-OAuth-Hermes-Setup.md end-to-end.

I have Hermes on this machine and want the same personal Google OAuth setup (Gmail + Drive + Calendar + Docs/Sheets). I am on a Mac unless I say otherwise — translate PowerShell paths to macOS/bash when needed (%LOCALAPPDATA%\\hermes → ~/.hermes or $env:LOCALAPPDATA equivalent).

Walk me through Part A (GCP console) then Part B (Hermes setup.py) step by step. Do not skip: create MY OWN Desktop OAuth client, download client_secret JSON, --client-secret, --auth-url, paste the full localhost:1 redirect URL, --auth-code, --check, then smoke-test gmail search and drive list.

Remind me that ERR_UNSAFE_PORT on localhost:1 is normal. Prefer publishing the OAuth app In production so refresh tokens don’t die every 7 days.

After --check passes, tell Hermes/Cursor that tokens live under the Hermes home google_token.json / google_client_secret.json and never commit those files.
---

QUICK DOCTOR (optional — also in the doc):

python $HERMES_HOME/skills/productivity/google-workspace/scripts/setup.py --check
python …/google_api.py gmail search "is:unread" --max 3
python …/google_api.py drive list --max 3

Thank you — enjoy the setup.
— Draven
(on behalf of Jon)
"""


def main() -> None:
    payload = json.loads(TOKEN.read_text(encoding="utf-8"))
    creds = Credentials.from_authorized_user_info(payload)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN.write_text(creds.to_json(), encoding="utf-8")

    service = build("gmail", "v1", credentials=creds)

    msg = MIMEMultipart()
    msg["To"] = TO
    msg["From"] = "Jon Beatz <jonbeatz@gmail.com>"
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(BODY, "plain", "utf-8"))

    data = ATTACH.read_bytes()
    part = MIMEApplication(data, Name=ATTACH.name)
    part.add_header("Content-Disposition", "attachment", filename=ATTACH.name)
    # ensure markdown content-type
    ctype = mimetypes.guess_type(ATTACH.name)[0] or "text/markdown"
    part.set_type(ctype)
    msg.attach(part)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print(json.dumps({"status": "sent", "id": result["id"], "threadId": result.get("threadId", ""), "to": TO, "attachment": ATTACH.name}, indent=2))


if __name__ == "__main__":
    main()
