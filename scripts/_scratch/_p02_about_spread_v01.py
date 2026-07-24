#!/usr/bin/env python3
"""P02 about/dedication spread v01 — fireplace+tree, burgundy walls, Qwen Pro Edit."""
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
OUT = ROOT / "Media/generated/mocks/P02-about-spread/v01"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"

# image 1 style · image 2 composition · image 3 burgundy / same-house night
REFS = [
    (
        ROOT / "Media/approved/style-refs/style-lock-v2.png",
        "style-lock-v2.png",
    ),
    (
        ROOT / "Media/generated/Ai-Image-Tests/p01-title.png",
        "p01-title-composition.png",
    ),
    (
        ROOT / "Media/generated/mocks/S01-approach/v14/art.png",
        "s01-v14-burgundy.png",
    ),
]

PROMPT = (
    "Create a seamless FULL SPREAD children's book painting (wide landscape). "
    "Use image 1 for watercolor/gouache style, warm golden light, burgundy wall color. "
    "Use image 2 for composition only: stone fireplace LEFT, decorated Christmas tree RIGHT, "
    "presents at tree base, wooden floor — one continuous living room, pages meeting in the middle, "
    "NO gutter seam or fold line. "
    "Use image 3 for deep burgundy wall color and same-house night atmosphere (same home as the hallway). "
    "Deep burgundy walls matching image 1 and image 3. Dramatic warm golden firelight chiaroscuro — "
    "fire casts long soft shadows across the room. Stone fireplace with green garland and stockings on mantel. "
    "Full Christmas tree with warm white/golden lights and ornaments. Wrapped presents at tree base. "
    "Wooden floor planks. Keep sparse and open — large soft wall/wash areas UPPER LEFT for About text "
    "and UPPER RIGHT for Dedication text. Soft feathered watercolor vignette into cream (FRAME ON). "
    "Art only — no letters, no title, no watermark, no people, no animals."
)

NEGATIVE = (
    "text, letters, typography, watermark, logo, people, faces, animals, gutter line, "
    "page fold, split seam, photorealistic, pale cream walls, white walls, bright daylight"
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
        raise SystemExit("Missing FAL_KEY")
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


def prepare_upload(path: Path, name: str, key: str) -> str:
    im = Image.open(path).convert("RGB")
    # keep wide refs reasonably large on long edge
    im.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return upload_bytes(key, Path(name).with_suffix(".png").name, buf.getvalue(), "image/png")


def fal_req(key: str, url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"Authorization": f"Key {key}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:2000]}") from e


def wait_result(key: str, submitted: dict) -> dict:
    for i in range(100):
        time.sleep(3 if i else 1)
        st = fal_req(key, submitted["status_url"])
        status = st.get("status") or st.get("queue_status")
        print(f"[{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, submitted["response_url"])
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    raise SystemExit("timeout")


def main() -> None:
    load_env()
    key = fal_key()
    OUT.mkdir(parents=True, exist_ok=True)

    urls = []
    for path, name in REFS:
        print("upload", path.name)
        urls.append(prepare_upload(path, name, key))

    payload = {
        "prompt": PROMPT,
        "negative_prompt": NEGATIVE,
        "image_urls": urls,
        "image_size": {"width": 2048, "height": 1024},
        "num_images": 1,
        "output_format": "png",
        "enable_prompt_expansion": False,
        "enable_safety_checker": True,
    }
    print("prompt_len", len(PROMPT))
    submitted = fal_req(key, ENDPOINT, payload)
    req_id = submitted["request_id"]
    print("request_id", req_id)
    (OUT / "job.json").write_text(json.dumps(submitted, indent=2), encoding="utf-8")

    result = wait_result(key, submitted)
    (OUT / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    images = result.get("images") or []
    img_url = images[0]["url"] if isinstance(images[0], dict) else images[0]
    seed = result.get("seed")
    art = OUT / "art.png"
    urllib.request.urlretrieve(img_url, art)
    print("saved", art, Image.open(art).size, "seed", seed)

    recipe = f"""# RECIPE — P02-about-spread / v01

| Field | Value |
|-------|--------|
| **name** | About + Dedication living-room spread · fireplace L / tree R |
| **unit** | P02-about-spread |
| **book page** | 2\\|3 · About + Dedication · FULL SPREAD |
| **page role** | spread |
| **spread side** | wide-master |
| **version** | v01 |
| **date** | {DAY} |
| **lane** | A2 mock favorite (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · enable_prompt_expansion=false · 3 refs |
| **FRAME** | ON |
| **concept** | Same house/night as S1 — living room instead of hallway; burgundy walls + firelight chiaroscuro; open wash for About (L) + Dedication (R) |
| **changes** | First dial in this unit from Ai-Image-Tests fireplace/tree composition |
| **size** | 2048×1024 dial |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | L: About This Story · R: Dedication (*For my family, with love. — Jack Farrell*) — InDesign later |
| **type_zone** | Upper-left soft wall (About) · upper-right soft wall (Dedication) |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- boy: n/a
- santa: n/a
- jack: n/a
- style / frame:
  - image 1: `Media/approved/style-refs/style-lock-v2.png`
  - image 2: `Media/generated/Ai-Image-Tests/p01-title.png` (fireplace+tree composition)
  - image 3: `Media/generated/mocks/S01-approach/v14/art.png` (burgundy / same-house night)
- base / edit source: multi-ref edit

## Prompt

{PROMPT}

## Negative / constraints

{NEGATIVE}

## Gotchas

- Source file is named `p01-title.png` but content is About/Dedication fireplace+tree composition.
- Flow v2 historically listed R as window/chair — this dial follows Jon brief: **one** living-room spread (fireplace L · tree R).

## Notes

- Visual bridge to S1: burgundy walls + warm golden light, different room.
- Next: Jon eye · optional Banana Pro finals.

## Related

- Flow v2 p2\\|3 · Script: `scripts/_scratch/_p02_about_spread_v01.py`
"""
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "request_id": req_id,
                "seed": seed,
                "image_urls": urls,
                "fal_image_url": img_url,
                "output": str(art),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("RECIPE written")


if __name__ == "__main__":
    main()
