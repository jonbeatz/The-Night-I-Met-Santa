#!/usr/bin/env python3
"""List OpenRouter image models that accept image input (for edit tests)."""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_key() -> str:
    env = (ROOT / ".env.local").read_text(encoding="utf-8")
    for line in env.splitlines():
        if line.startswith("OPENROUTER_API_KEY=") and not line.strip().startswith("#"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("OPENROUTER_API_KEY missing in .env.local")


def main() -> None:
    key = load_key()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/images/models",
        headers={"Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    models = data.get("data", [])
    print(f"total_image_models={len(models)}")
    for m in models:
        arch = m.get("architecture") or {}
        ins = arch.get("input_modalities") or []
        if "image" not in ins:
            continue
        params = list((m.get("supported_parameters") or {}).keys())
        mid = m.get("id")
        print(f"{mid}\tparams={','.join(params)}")


if __name__ == "__main__":
    main()
