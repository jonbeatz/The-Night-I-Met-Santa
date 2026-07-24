#!/usr/bin/env python3
"""P01 title v25 — Victorian house vignette via Qwen 2 Pro Edit."""
from __future__ import annotations

import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/generated/mocks/P01-title/v25"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"

# image 1 = style · image 2 = house focal · image 3 = circular vignette
# Ref1 lamppost / wreath / magical feeling carried in prompt (3-URL cap)
REFS = [
    (
        ROOT / "Media/approved/style-refs/style-lock-v2.png",
        "style-lock-v2.png",
        "image/png",
    ),
    (
        ROOT / "Media/generated/Ai-Image-Tests/openbookFront-Ref2.jpg",
        "openbookFront-Ref2.jpg",
        "image/jpeg",
    ),
    (
        ROOT / "Media/generated/Ai-Image-Tests/openbookFront-Ref3.jpg",
        "openbookFront-Ref3.jpg",
        "image/jpeg",
    ),
]

PROMPT = (
    "Using image 1 for watercolor/gouache paint style and warm golden lighting only. "
    "Using image 2 for the Victorian house subject: snowy roof, warm golden light glowing from every window, "
    "Christmas wreath on the front door, white picket fence across the bottom with a red bow accent. "
    "Using image 3 for the contained soft circular vignette composition — scene as a framed painting that "
    "feathers into cream/white paper at the edges. "
    "Add a decorative foreground lamppost with a festive red bow and holly (from the open-book lamppost refs). "
    "Snow-covered evergreens frame left and right. Soft falling snow. Dreamy winter sky: deep purple-blue "
    "at top with burgundy undertones in shadows (match image 1 wall atmosphere), warming to golden-peach "
    "near the horizon. Leave open cream space in the UPPER CENTER for title text later. "
    "Art only — no letters, no title, no copyright, no watermark, no people, no animals. "
    "FRAME ON: soft irregular watercolor vignette edge into cream."
)

NEGATIVE = (
    "text, letters, typography, title, watermark, logo, signature, people, faces, animals, "
    "photorealistic, hard crop edge, full-bleed edge-to-edge with no cream margin, double house"
)


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
        raise SystemExit("Missing FAL_KEY / FAL_API_KEY")
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


def prepare_upload(path: Path, name: str, content_type: str, key: str) -> str:
    im = Image.open(path).convert("RGB")
    im.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    if content_type == "image/png":
        im.save(buf, format="PNG", optimize=True)
    else:
        im.save(buf, format="JPEG", quality=92)
        name = Path(name).with_suffix(".jpg").name
        content_type = "image/jpeg"
    return upload_bytes(key, name, buf.getvalue(), content_type)


def fal_post(key: str, url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"Authorization": f"Key {key}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise SystemExit(f"HTTP {e.code}: {body[:2000]}") from e


def main() -> None:
    load_env()
    key = fal_key()
    OUT.mkdir(parents=True, exist_ok=True)

    urls = []
    for path, name, ctype in REFS:
        print("upload", path.name)
        urls.append(prepare_upload(path, name, ctype, key))
    print("urls", urls)

    payload = {
        "prompt": PROMPT,
        "negative_prompt": NEGATIVE,
        "image_urls": urls,
        "image_size": {"width": 2048, "height": 2048},
        "num_images": 1,
        "output_format": "png",
        "enable_prompt_expansion": False,
        "enable_safety_checker": True,
    }
    print("prompt_len", len(PROMPT))
    submitted = fal_post(key, ENDPOINT, payload)
    req_id = submitted.get("request_id")
    status_url = submitted.get("status_url")
    response_url = submitted.get("response_url")
    print("request_id", req_id)
    (OUT / "job.json").write_text(json.dumps(submitted, indent=2), encoding="utf-8")

    result = None
    for i in range(90):
        time.sleep(3 if i else 1)
        st = fal_post(key, status_url)
        status = st.get("status") or st.get("queue_status")
        print(f"[{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            result = fal_post(key, response_url) if response_url else st
            break
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    if result is None:
        raise SystemExit("timeout waiting for fal job")

    (OUT / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    images = result.get("images") or result.get("data", {}).get("images") or []
    if not images:
        raise SystemExit(f"no images in result: {list(result.keys())}")
    img_url = images[0]["url"] if isinstance(images[0], dict) else images[0]
    seed = result.get("seed")
    art_path = OUT / "art.png"
    urllib.request.urlretrieve(img_url, art_path)
    print("saved", art_path, Image.open(art_path).size, "seed", seed)

    recipe = f"""# RECIPE — P01-title / v25

| Field | Value |
|-------|--------|
| **name** | Victorian house title vignette · lamppost + fence bows |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE (right-hand) |
| **page role** | single |
| **spread side** | n/a (right-hand open after burgundy pastedown) |
| **version** | v25 |
| **date** | 2026-07-22 |
| **lane** | A2 alt / mock favorite look (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · enable_prompt_expansion=false · 3 image_urls (cap) |
| **FRAME** | ON |
| **concept** | First visual when opening cover — framed Victorian house night scene; cream upper-center for live Cormorant title |
| **changes** | New concept dial from openbookFront Refs 1–3 + style-lock-v2 (not from v22–v24 fireplace/tree path) |
| **size** | 2048² dial |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | Title / author / copyright placed later in InDesign — art only |
| **type_zone** | Upper-center cream wash (title) · lower cream for author/copyright |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- boy: n/a
- santa: n/a
- jack: n/a
- style / frame:
  - image 1: `Media/approved/style-refs/style-lock-v2.png`
  - image 2: `Media/generated/Ai-Image-Tests/openbookFront-Ref2.jpg` (Victorian house focal)
  - image 3: `Media/generated/Ai-Image-Tests/openbookFront-Ref3.jpg` (circular vignette)
  - prompt-only (3-URL cap): `openbookFront-Ref1.jpg` lamppost + wreath/magical feeling
- base / edit source: multi-ref edit (no prior P01 art)

## Prompt

{PROMPT}

## Negative / constraints

{NEGATIVE}

## Gotchas

- Qwen Pro Edit allows **max 3** `image_urls` — Ref1 composition cues (lamppost, red bow, special-place feeling) are prompt-only; Ref2 + Ref3 + style-lock take the three slots.
- No baked text — title/copyright are InDesign live type.

## Notes

- Pull burgundy into house shadows + sky undertones to connect with S1 / style-lock-v2 walls.
- Next: Jon eye · if keep-leaning, Banana Pro finals pass optional.

## Related

- Prev: v22–v24 fireplace/tree title path
- Flow v2 P01 · casewrap pastedowns = solid burgundy (not this page)
- Script: `scripts/_scratch/_p01_v25_victorian_house.py`
"""
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    meta = {
        "request_id": req_id,
        "seed": seed,
        "image_urls": urls,
        "output": str(art_path),
        "fal_image_url": img_url,
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("RECIPE written")


if __name__ == "__main__":
    main()
