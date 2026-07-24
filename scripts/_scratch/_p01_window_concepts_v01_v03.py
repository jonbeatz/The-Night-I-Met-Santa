#!/usr/bin/env python3
"""P01 title — three quiet window concepts into Media/development/P01-title/v01–v03."""
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
OUT_BASE = ROOT / "Media/development/P01-title"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048

BASE = (
    "Create a SINGLE square children's-book TITLE PAGE painting — quiet tone-setter, NOT a story scene. "
    "Image 1 = watercolor/gouache style, deep burgundy walls, warm golden light (style-lock). "
    "Centered or slightly upper-center: a simple window (dark wood or soft white painted trim) looking out "
    "on a snowy winter night. Outside: deep blue-purple night sky, bright full moon, a few stars, "
    "distant snow-covered evergreens, soft falling snow. Inside: deep burgundy wall around the window "
    "(match image 1 burgundy). Warm golden light from off-frame gently kisses the window frame and wall. "
    "Leave open soft space ABOVE the window for the title and BELOW for copyright — intimate, contained. "
    "Atmospheric, soft brushstrokes, not hyper-detailed. Soft feathered watercolor vignette into cream (FRAME ON). "
    "Art only — no letters, no title, no copyright, no watermark, no people, no faces."
)

JOBS = [
    {
        "ver": "v01",
        "name": "Quiet window — pure moon night",
        "extra": " No sleigh, no ribbon, no story props — only the window, moon, snow, evergreens, burgundy wall.",
    },
    {
        "ver": "v02",
        "name": "Quiet window — faint sleigh on the moon",
        "extra": (
            " Subtle story hint only: the faintest tiny silhouette of Santa's sleigh and reindeer "
            "crossing the bright moon — distant, easy to miss, not dominating."
        ),
    },
    {
        "ver": "v03",
        "name": "Quiet window — snowy branch + red ribbon",
        "extra": (
            " Subtle story hint only: a single snow-covered evergreen branch frames the top of the window "
            "from outside, with a small red ribbon tied to it — quiet accent, not busy."
        ),
    },
]

NEGATIVE = (
    "text, letters, typography, title, copyright, watermark, logo, people, faces, boy, santa close-up, "
    "busy interior furniture, fireplace, Christmas tree indoors, photorealistic, hard crop, full-bleed no vignette"
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
        print(f"  [{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, submitted["response_url"])
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    raise SystemExit("timeout")


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(job: dict, seed, req_id: str, prompt: str) -> None:
    out = OUT_BASE / job["ver"]
    text = f"""# RECIPE — P01-title / {job['ver']} (window concepts)

| Field | Value |
|-------|--------|
| **name** | {job['name']} |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE (right-hand) |
| **page role** | single |
| **spread side** | n/a |
| **version** | {job['ver']} |
| **date** | {DAY} |
| **lane** | A2 mock favorite (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · style-lock-v2 only · enable_prompt_expansion=false |
| **FRAME** | ON |
| **concept** | Quiet winter window tone-setter — title above / copyright below in InDesign |
| **changes** | New window concept dial series under `Media/development/P01-title/` (does not auto-replace art.png) |
| **size** | 2048² |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | Title · Written by Jack Farrell · copyright — InDesign Cormorant later |
| **type_zone** | Open wash above window (title) · open wash below (copyright) |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |
| **tier** | development |

## Refs

- image 1: `Media/approved/style-refs/style-lock-v2.png`

## Prompt

{prompt}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-window-concepts-board.png`
- Script: `scripts/_scratch/_p01_window_concepts_v01_v03.py`
"""
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(results: list[dict]) -> Path:
    panel, label_h = 720, 100
    gap, margin, header = 24, 32, 100
    w = margin * 2 + panel * 3 + gap * 2
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), (245, 240, 230))
    draw = ImageDraw.Draw(board)
    draw.text((margin, 28), "P01 Title — Window Concepts", fill=(40, 30, 28), font=font(30))
    draw.text(
        (margin, 64),
        "Quiet tone-setter · Qwen 2 Pro Edit · style-lock-v2 · FRAME ON · no baked text",
        fill=(90, 70, 60),
        font=font(15),
    )
    labels = [
        ("v01 PURE WINDOW", "Moon · snow · burgundy wall"),
        ("v02 FAINT SLEIGH", "Tiny silhouette across the moon"),
        ("v03 BRANCH + RIBBON", "Snowy evergreen · small red bow"),
    ]
    for i, r in enumerate(results):
        x = margin + i * (panel + gap)
        y = margin + header
        im = Image.open(r["path"]).convert("RGB").resize((panel, panel), Image.Resampling.LANCZOS)
        board.paste(im, (x, y))
        draw.rectangle([x, y + panel, x + panel, y + panel + label_h], fill=(235, 228, 215))
        draw.text((x + 12, y + panel + 16), labels[i][0], fill=(30, 24, 22), font=font(18))
        draw.text((x + 12, y + panel + 46), labels[i][1], fill=(80, 60, 50), font=font(14))
        draw.text((x + 12, y + panel + 72), f"seed {r['seed']}", fill=(110, 90, 80), font=font(13))
    out = ROOT / "Media/generated/mocks/_INDEX/P01-title-window-concepts-board.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    print("style uploaded")

    pending = []
    for job in JOBS:
        prompt = BASE + job["extra"]
        print("submit", job["ver"], "len", len(prompt))
        submitted = fal_req(
            key,
            ENDPOINT,
            {
                "prompt": prompt,
                "negative_prompt": NEGATIVE,
                "image_urls": [style_url],
                "image_size": {"width": SIZE, "height": SIZE},
                "num_images": 1,
                "output_format": "png",
                "enable_prompt_expansion": False,
                "enable_safety_checker": True,
            },
        )
        print("  request_id", submitted.get("request_id"))
        pending.append({**job, "submitted": submitted, "prompt": prompt})

    results = []
    for item in pending:
        ver = item["ver"]
        out = OUT_BASE / ver
        out.mkdir(parents=True, exist_ok=True)
        print("wait", ver)
        result = wait_result(key, item["submitted"])
        (out / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        images = result["images"]
        img_url = images[0]["url"] if isinstance(images[0], dict) else images[0]
        seed = result.get("seed")
        req_id = item["submitted"]["request_id"]
        art = out / "art.png"
        urllib.request.urlretrieve(img_url, art)
        print("saved", art, Image.open(art).size, "seed", seed)
        write_recipe(item, seed, req_id, item["prompt"])
        (out / "meta.json").write_text(
            json.dumps({"request_id": req_id, "seed": seed, "fal_image_url": img_url}, indent=2),
            encoding="utf-8",
        )
        results.append({"path": art, "seed": seed})

    board = build_board(results)
    print("BOARD", board)


if __name__ == "__main__":
    main()
