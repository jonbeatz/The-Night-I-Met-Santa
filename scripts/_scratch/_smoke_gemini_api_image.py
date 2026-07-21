"""Additive Gemini API image smoke — does NOT change fal/OpenRouter lanes."""
from __future__ import annotations

import base64
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "Media" / "generated" / "gemini-api-smoke"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_env_local() -> None:
    env_path = ROOT / ".env.local"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v

load_env_local()
key = os.environ.get("GEMINI_API_KEY", "").strip()
if not key:
    print("ERROR: GEMINI_API_KEY missing in env / .env.local")
    sys.exit(1)

from google import genai

# Prefer Flash image (Nano Banana family) — cheap smoke, not Pro
MODEL = os.environ.get("GEMINI_IMAGE_SMOKE_MODEL", "gemini-2.5-flash-image")
PROMPT = (
    "Traditional children's Christmas picture-book illustration, painted gouache feel: "
    "a single glowing red Christmas ornament hanging from a green pine branch, "
    "soft warm light, simple soft background, no text, no letters, no watermark."
)

client = genai.Client(api_key=key)
print(f"model={MODEL}")
print("calling generate_content...")
response = client.models.generate_content(
    model=MODEL,
    contents=PROMPT,
)

saved = None
text_bits = []
candidates = getattr(response, "candidates", None) or []
if not candidates:
    print("ERROR: no candidates")
    print(response)
    sys.exit(2)

parts = candidates[0].content.parts
for part in parts:
    t = getattr(part, "text", None)
    if t:
        text_bits.append(t)
    inline = getattr(part, "inline_data", None)
    if inline is not None:
        data = inline.data
        mime = getattr(inline, "mime_type", None) or "image/png"
        if isinstance(data, str):
            raw = base64.b64decode(data)
        else:
            raw = bytes(data)
        ext = ".png" if "png" in mime else ".jpg" if "jpeg" in mime or "jpg" in mime else ".bin"
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        saved = OUT_DIR / f"smoke-ornament-{stamp}{ext}"
        saved.write_bytes(raw)
        print(f"saved={saved} bytes={len(raw)} mime={mime}")

if text_bits:
    print("text:", " ".join(text_bits)[:400])

if not saved:
    print("ERROR: no inline image in response")
    print(repr(response))
    sys.exit(3)

readme = OUT_DIR / "README.md"
if not readme.exists():
    readme.write_text(
        "# Gemini API smoke (optional)\n\n"
        "Additive test only — **not** production Lane A/B.\n\n"
        "- Auth: `GEMINI_API_KEY` (AI Studio), not Gmail OAuth\n"
        "- Default model: `gemini-2.5-flash-image` (Nano Banana family)\n"
        "- Book finals stay on fal `nano-banana-pro/edit` + refs\n",
        encoding="utf-8",
    )
print("OK")
