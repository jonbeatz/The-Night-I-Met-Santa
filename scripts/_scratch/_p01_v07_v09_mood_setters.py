#!/usr/bin/env python3
"""P01 title v07–v09 — window / desk / quiet corner — rich atmospheric, not clip-art."""
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
SCENE = ROOT / "Images/styles3/p30-writing-desk.png"  # desk + moon window + tree + fire DNA
DESK_TEX = ROOT / "Images/styles3/hands-writing-overhead-v3.png"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048

ANTI_CLIP = (
    " Rich painterly watercolor/gouache — soft wet edges, atmospheric depth, visible brushstrokes, "
    "subtle paper grain. NOT clip-art, NOT sticker, NOT flat icon, NOT basic graphic, NOT vector cartoon."
)

NEGATIVE = (
    "text, letters, typography, title, copyright, watermark, logo, people, faces, hands, child, boy, "
    "clip art, sticker, flat icon, vector graphic, basic cartoon, hard cutout, "
    "deep burgundy walls, full-bleed burgundy, photorealistic, busy crowd"
)

JOBS = [
    {
        "ver": "v07",
        "name": "Winter Window",
        "label": ("v07 WINTER WINDOW", "Moon · snow · cream curtains · tree peek"),
        "refs": "style+scene",
        "prompt": (
            "Create a SINGLE square children's-book TITLE PAGE — intimate mood-setter, not a full story beat. "
            "Image 1 = paint style (watercolor/gouache, warm light). "
            "Image 2 = composition/atmosphere DNA: cozy room, window to snowy night with full moon, "
            "Christmas tree edge, wrapped gifts — remake with CREAM/IVORY walls (NOT burgundy). "
            "Focal: quiet window looking out at falling snow and a bright full moon through soft panes. "
            "Soft blue-gray winter light. Light cream curtains tied back. Edge of Christmas tree with warm lights "
            "and a few ornaments on one side. One or two wrapped presents below. Optional tiny holly on sill. "
            "Open cream space for title above / copyright below. Soft vignette fading to cream paper (FRAME ON). "
            "Feeling: warm inside, snow outside, story about to begin."
            + ANTI_CLIP
            + " Art only — no people, no hands, no baked text."
        ),
    },
    {
        "ver": "v08",
        "name": "Writing Desk",
        "label": ("v08 WRITING DESK", "Lamp · blank paper · pen · no person"),
        "refs": "style+scene+desk",
        "prompt": (
            "Create a SINGLE square children's-book TITLE PAGE — quiet writer's desk, mood only. "
            "Image 1 = paint style. "
            "Image 2 = room DNA (desk, lamp glow, tree edge, winter window) — REMOVE every person, face, and hand. "
            "Image 3 = wooden desk texture / overhead writing desk lighting reference only. "
            "Objects only: wooden writing desk, blank cream paper or open blank book, fountain pen resting beside it, "
            "warm brass desk lamp casting golden glow, small holly sprig, optional coffee/tea cup. "
            "Soft background: edge of Christmas tree with warm lights; cream/ivory walls (NOT burgundy). "
            "Feeling: the writer just stepped away; the story is waiting. Generous open cream for title type. "
            "FRAME ON soft vignette to cream paper."
            + ANTI_CLIP
            + " Art only — no people, no hands, no faces, no baked text."
        ),
    },
    {
        "ver": "v09",
        "name": "Quiet Room Corner",
        "label": ("v09 QUIET ROOM CORNER", "Tree edge · snow window · soft fire glow"),
        "refs": "style+scene",
        "prompt": (
            "Create a SINGLE square children's-book TITLE PAGE — softest atmospheric room corner. "
            "Image 1 = paint style. "
            "Image 2 = room DNA (tree, fireplace warmth, window to snow) — simplify into a dreamy corner vignette. "
            "Composition: edge of Christmas tree with soft golden lights; window with snow falling outside; "
            "barest hint of fireplace glow. Everything soft, slightly distant, hazy watercolor. "
            "Cream/ivory walls (NOT burgundy). Scene fades softly into cream at the edges for title placement. "
            "No characters, no sleigh, no busy detail. Feeling: threshold of a warm home on a snowy night. "
            "FRAME ON vignette to cream paper."
            + ANTI_CLIP
            + " Art only — no people, no baked text."
        ),
    },
]


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


def write_recipe(job: dict, seed, req_id: str) -> None:
    out = OUT_BASE / job["ver"]
    text = f"""# RECIPE — P01-title / {job['ver']}

| Field | Value |
|-------|--------|
| **name** | {job['name']} |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE |
| **page role** | single |
| **version** | {job['ver']} |
| **date** | {DAY} |
| **lane** | A2 Qwen 2 Pro Edit |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · cream/ivory dominant · anti-clip-art language |
| **FRAME** | ON |
| **concept** | Mood-setter title page — distinct direction vs quiet ornaments / simple windows |
| **size** | 2048² |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **type_zone** | Open cream for Cormorant title + copyright |
| **verdict** | pending |
| **status** | working |
| **tier** | development |

## Refs

- `Media/approved/style-refs/style-lock-v2.png`
- `Images/styles3/p30-writing-desk.png` (room DNA — desk/window/tree/fire)
- desk texture (v08): `Images/styles3/hands-writing-overhead-v3.png`

## Prompt

{job['prompt']}

## Negative

{NEGATIVE}

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v07-v09-board.png`
- Script: `scripts/_scratch/_p01_v07_v09_mood_setters.py`
"""
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(results: list[dict]) -> Path:
    panel, label_h = 720, 100
    gap, margin, header = 24, 32, 100
    w = margin * 2 + panel * 3 + gap * 2
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), (245, 240, 230))
    draw = ImageDraw.Draw(board)
    draw.text((margin, 28), "P01 Title — Mood Setters (v07–v09)", fill=(40, 30, 28), font=font(28))
    draw.text(
        (margin, 64),
        "Cream walls · painterly · Qwen 2 Pro Edit · p30 room DNA · FRAME ON · no baked text",
        fill=(90, 70, 60),
        font=font(14),
    )
    for i, r in enumerate(results):
        x = margin + i * (panel + gap)
        y = margin + header
        im = Image.open(r["path"]).convert("RGB").resize((panel, panel), Image.Resampling.LANCZOS)
        board.paste(im, (x, y))
        title, sub = r["label"]
        draw.rectangle([x, y + panel, x + panel, y + panel + label_h], fill=(235, 228, 215))
        draw.text((x + 12, y + panel + 16), title, fill=(30, 24, 22), font=font(18))
        draw.text((x + 12, y + panel + 46), sub, fill=(80, 60, 50), font=font(14))
        draw.text((x + 12, y + panel + 72), f"seed {r['seed']}", fill=(110, 90, 80), font=font(13))
    out = ROOT / "Media/generated/mocks/_INDEX/P01-title-v07-v09-board.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    scene_url = prepare_upload(SCENE, "p30-writing-desk.png", key)
    desk_url = prepare_upload(DESK_TEX, "hands-writing-overhead.png", key)
    print("refs uploaded")

    pending = []
    for job in JOBS:
        if job["refs"] == "style+scene+desk":
            urls = [style_url, scene_url, desk_url]
        else:
            urls = [style_url, scene_url]
        print("submit", job["ver"])
        submitted = fal_req(
            key,
            ENDPOINT,
            {
                "prompt": job["prompt"],
                "negative_prompt": NEGATIVE,
                "image_urls": urls,
                "image_size": {"width": SIZE, "height": SIZE},
                "num_images": 1,
                "output_format": "png",
                "enable_prompt_expansion": False,
                "enable_safety_checker": True,
            },
        )
        print("  request_id", submitted.get("request_id"))
        pending.append({**job, "submitted": submitted})

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
        write_recipe(item, seed, req_id)
        (out / "meta.json").write_text(
            json.dumps({"request_id": req_id, "seed": seed, "fal_image_url": img_url}, indent=2),
            encoding="utf-8",
        )
        results.append({"path": art, "seed": seed, "label": item["label"]})

    board = build_board(results)
    print("BOARD", board)


if __name__ == "__main__":
    main()
