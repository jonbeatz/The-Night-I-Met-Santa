#!/usr/bin/env python3
"""S04 age-up retry — keep Santa + invite pose; only age the boy."""
from __future__ import annotations

import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
SRC = DEV / "S04-sit-here" / "art-right.png"
LEFT = DEV / "S04-sit-here" / "art-left.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
AGE = DEV / "S07-proof" / "art.png"
OUT = DEV / "S04-sit-here" / "v14b-age-s07"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-30"
GEN = 2048

PROMPT = (
    "Edit Image 1 carefully. Image 1 shows Santa sitting cross-legged inviting a young boy "
    "who stands facing him by a Christmas tree and gifts. "
    "KEEP Santa EXACTLY — same seated pose, open red coat, striped shirt, brown suspenders, "
    "gesture hand, smile, position. KEEP tree, gifts, floor, lighting. "
    "ONLY change the standing BOY: age him up to match Image 2's boy (~5–7 years old — "
    "school-age proportions, less toddler baby-face, longer limbs) while he remains STANDING "
    "in the same spot looking up at Santa. Do NOT remove Santa. Do NOT sit the boy down. "
    "Do NOT change to boy-alone. Image 3 = Boy G0 identity (messy light-brown hair, brown eyes, "
    "oatmeal holly PJs red trim). ART ONLY."
)
NEGATIVE = (
    "remove Santa, missing Santa, boy alone, boy sitting cross-legged alone, no Santa, "
    "toddler, baby face, extra child, title text"
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


def prepare_upload(path: Path, name: str, key: str, size=None) -> str:
    im = Image.open(path).convert("RGB")
    if size:
        im = im.resize(size, Image.Resampling.LANCZOS)
    else:
        im.thumbnail((GEN, GEN), Image.Resampling.LANCZOS)
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
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:2000]}") from e


def wait_result(key: str, submitted: dict) -> dict:
    for i in range(120):
        time.sleep(3 if i else 1)
        st = fal_req(key, submitted["status_url"])
        status = st.get("status") or st.get("queue_status")
        print(f"  [{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, submitted["response_url"])
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    raise SystemExit("timeout")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=180) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    load_env()
    key = fal_key()
    OUT.mkdir(parents=True, exist_ok=True)
    print("upload S04-R + S07 age + boy G0")
    urls = [
        prepare_upload(SRC, "s04-src.png", key, (GEN, GEN)),
        prepare_upload(AGE, "age-s07.png", key),
        prepare_upload(BOY, "boy-G0.png", key, (GEN, GEN)),
    ]
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_urls": urls,
            "num_images": 1,
            "output_format": "png",
            "enable_prompt_expansion": False,
            "image_size": {"width": GEN, "height": GEN},
        },
    )
    print("request_id", submitted.get("request_id"))
    result = wait_result(key, submitted)
    images = result.get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:3000])
    result_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    seed = int(result.get("seed") or 0)
    raw = OUT / "art-raw.png"
    download(result_url, raw)
    right = Image.open(raw).convert("RGB").resize((2625, 2625), Image.Resampling.LANCZOS)
    right.save(OUT / "art-right.png", optimize=True, dpi=(300, 300))
    left = Image.open(LEFT).convert("RGB").resize((2625, 2625), Image.Resampling.LANCZOS)
    left.save(OUT / "art-left.png", optimize=True, dpi=(300, 300))
    spread = Image.new("RGB", (5250, 2625))
    spread.paste(left, (0, 0))
    spread.paste(right, (2625, 0))
    spread.save(OUT / "art.png", optimize=True, dpi=(300, 300))

    (OUT / "RECIPE.md").write_text(
        f"""# RECIPE — S04-sit-here / v14b-age-s07

| Field | Value |
|-------|--------|
| **version** | v14b-age-s07 |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **seed** | {seed} |
| **status** | dial — age-up retry (Santa locked) |
| **note** | v14 dropped Santa — v14b forces keep Santa + standing boy |

Age boy only to S07/S08 (~5–7). Keep Santa invite pose.
""",
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "unit": "S04-sit-here",
                "version": "v14b-age-s07",
                "date": DAY,
                "status": "dial",
                "seed": seed,
                "result_url": result_url,
                "replaces_attempt": "v14-age-s07",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    keep = Image.open(SRC).convert("RGB").resize((900, 900))
    alt = right.resize((900, 900))
    board = Image.new("RGB", (900 * 2 + 48, 900 + 60), (250, 248, 244))
    draw = ImageDraw.Draw(board)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    draw.text((16, 12), "S04-R KEEP  vs  v14b age-up (Santa kept)", fill=(40, 40, 40), font=font)
    board.paste(keep, (16, 44))
    board.paste(alt, (32 + 900, 44))
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(INDEX / "S04-sit-here-v14b-age-s07-board.png", optimize=True)
    print("DONE v14b seed", seed)


if __name__ == "__main__":
    main()
