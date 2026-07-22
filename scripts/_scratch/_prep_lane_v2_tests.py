#!/usr/bin/env python3
"""Build watercolor-paper LoRA zip (augmented from 2 styles2 refs) + upload assets."""
from __future__ import annotations

import io
import json
import os
import urllib.request
import zipfile
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
CAP = (
    "Soft cream watercolor paper with subtle feathered edges, no illustrations, "
    "no text, warm ivory, gentle paper grain"
)
OUT_DIR = ROOT / "Media/generated/mocks/_INDEX/lora-watercolor-paper"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_env() -> None:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def fal_key() -> str:
    key = (os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY") or "").strip()
    if not key:
        raise SystemExit("no FAL key")
    return key


def upload_bytes(key: str, name: str, data: bytes, content_type: str) -> str:
    req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps({"file_name": name, "content_type": content_type}).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        meta = json.loads(resp.read().decode())
    put = urllib.request.Request(
        meta["upload_url"], data=data, headers={"Content-Type": content_type}, method="PUT"
    )
    with urllib.request.urlopen(put, timeout=180) as resp:
        resp.read()
    return meta["file_url"]


def variants(im: Image.Image, stem: str) -> list[tuple[str, Image.Image]]:
    im = im.convert("RGB")
    # focus on paper/wash areas — center and corner crops
    w, h = im.size
    crops = [
        ("full", im),
        ("c1", im.crop((0, 0, int(w * 0.7), int(h * 0.7)))),
        ("c2", im.crop((int(w * 0.3), int(h * 0.3), w, h))),
        ("c3", im.crop((int(w * 0.15), int(h * 0.15), int(w * 0.85), int(h * 0.85)))),
        ("flip", ImageOps.mirror(im)),
    ]
    out = []
    for tag, pic in crops:
        pic = pic.copy()
        pic.thumbnail((1280, 1280), Image.Resampling.LANCZOS)
        out.append((f"{stem}_{tag}", pic))
        # slight brightness variant
        bright = ImageEnhance.Brightness(pic).enhance(1.05)
        out.append((f"{stem}_{tag}_b", bright))
    return out


def main() -> None:
    load_env()
    key = fal_key()

    sources = [
        ROOT / "Images/styles2/spread-Frame-Style1.png",
        ROOT / "Images/styles2/p21-beat12-13-note-LEFT.png",
    ]
    # Also pull soft cream from style-lock edges? skip — stick to paper refs

    zip_path = OUT_DIR / "watercolor-paper-train.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        n = 0
        for src in sources:
            im = Image.open(src)
            for name, pic in variants(im, src.stem[:20]):
                buf = io.BytesIO()
                pic.save(buf, format="JPEG", quality=92)
                zf.writestr(f"{name}.jpg", buf.getvalue())
                zf.writestr(f"{name}.txt", CAP)
                n += 1
        print(f"zip entries pairs: {n}")

    zip_url = upload_bytes(key, "watercolor-paper-train.zip", zip_path.read_bytes(), "application/zip")
    print("zip_url", zip_url)

    # upload style lock for GPT edit
    lock = ROOT / "Media/approved/style-refs/style-lock-v2.png"
    im = Image.open(lock).convert("RGB")
    im.thumbnail((1536, 1536), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    lock_url = upload_bytes(key, "style-lock-v2-ref.png", buf.getvalue(), "image/png")
    print("lock_url", lock_url)

    meta = {"zip_url": zip_url, "style_lock_url": lock_url, "caption": CAP, "train_images": n}
    (OUT_DIR / "upload-meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
