#!/usr/bin/env python3
"""Upload S4 style-lock refs to fal CDN (resized)."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def load_env() -> None:
    env_path = ROOT / ".env.local"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def fal_key() -> str:
    key = (os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY") or "").strip()
    if not key:
        raise SystemExit("Missing FAL_KEY / FAL_API_KEY")
    return key


def upload_png(key: str, name: str, data: bytes) -> str:
    req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps({"file_name": name, "content_type": "image/png"}).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        meta = json.loads(resp.read().decode())
    put = urllib.request.Request(
        meta["upload_url"],
        data=data,
        headers={"Content-Type": "image/png"},
        method="PUT",
    )
    with urllib.request.urlopen(put, timeout=120) as resp:
        resp.read()
    return meta["file_url"]


def main() -> None:
    load_env()
    key = fal_key()
    files = [
        ROOT / "Images/styles2/07-qwen-image-2.png",
        ROOT / "Images/styles2/p08-beat02-the-door.png",
        ROOT / "Images/styles2/klein-dial-D2-sweetspot.png",
    ]
    urls = []
    for path in files:
        im = Image.open(path).convert("RGB")
        im.thumbnail((1536, 1536), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="PNG", optimize=True)
        data = buf.getvalue()
        url = upload_png(key, f"{path.stem}-ref.png", data)
        urls.append({"name": path.name, "url": url, "bytes": len(data)})
        print(path.name, url, len(data))

    out = ROOT / "Media/generated/mocks/S04-sit-here/_INDEX/style-refs-urls-2026-07-22.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
