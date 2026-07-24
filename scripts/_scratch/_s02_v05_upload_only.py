#!/usr/bin/env python3
"""Upload S02 v05 refs only; print CDN URLs for MCP submit."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
V04 = ROOT / "Media/development/S02-threshold/v04/art.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
COVER = ROOT / "Media/generated/test-book-v1/covers/00-cover-front-APPROVED-beige-v2.png"
OUT = ROOT / "scripts/_scratch/_s02_v05_urls.json"


def load_env() -> None:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def fal_key() -> str:
    key = (os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY") or "").strip()
    if not key:
        raise SystemExit("Missing FAL_KEY")
    return key


def upload(path: Path, name: str, size: tuple[int, int] | None = None) -> str:
    key = fal_key()
    im = Image.open(path).convert("RGB")
    if size:
        im = im.resize(size, Image.Resampling.LANCZOS)
    else:
        im.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps({"file_name": name, "content_type": "image/png"}).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        meta = json.loads(resp.read().decode())
    put = urllib.request.Request(
        meta["upload_url"], data=buf.getvalue(), headers={"Content-Type": "image/png"}, method="PUT"
    )
    with urllib.request.urlopen(put, timeout=180) as resp:
        resp.read()
    return meta["file_url"]


def main() -> None:
    load_env()
    for p in (V04, STYLE, COVER):
        if not p.is_file():
            raise SystemExit(f"missing {p}")
    urls = {
        "v04": upload(V04, "s02-v04-base.png", (2048, 1024)),
        "style": upload(STYLE, "style-lock-v2.png"),
        "cover": upload(COVER, "cover-beige-v2.png"),
    }
    OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps(urls, indent=2))


if __name__ == "__main__":
    main()
