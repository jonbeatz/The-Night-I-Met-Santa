#!/usr/bin/env python3
"""S02 Threshold v04 — Qwen 2 Pro Edit: keep v03 composition, fix coat/bag/tree/PJs."""
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
DEV = ROOT / "Media/development/S02-threshold"
MOCKS = ROOT / "Media/generated/mocks/S02-threshold"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
VERSION = "v04"
SIZE = 2048

HARD_WARDROBE = (
    "HARD WARDROBE LOCK: Child wears oatmeal/taupe holly pajamas ONLY — warm beige/taupe fabric "
    "with green holly leaves and red berries — NOT bright white, NOT cream-white, NOT a red coat, "
    "NOT a Santa suit, NOT a Santa costume. Match image 2 (boy G0) exactly for pajamas color and pattern. "
    "Santa wears a FULL red coat with black suspenders clearly visible ON TOP OF the red coat fabric — "
    "NOT shirtsleeves, NOT red shirt alone. Open relaxed collar. Match image 3 (santa-G0-v2)."
)

PROMPT = (
    "Image 1 = watercolor/gouache paint STYLE and burgundy room atmosphere (style-lock). "
    "Image 2 = boy character + oatmeal/taupe holly pajamas lock. "
    "Image 3 = Santa character + red coat with black suspenders over coat lock. "
    "Create a wide seamless TWO-PAGE Christmas storybook SPREAD (2:1) for S2 Threshold. "
    "COMPOSITION (locked layout): LEFT — over-shoulder view of the boy entering slowly through an open "
    "doorway, back and shoulder toward viewer, stepping into the room, discovery and surprise — he has "
    "just seen Santa but they have NOT made eye contact yet. RIGHT — Santa kneeling on the wooden floor "
    "at work among gifts, focused on his job, has NOT noticed the boy. Continuous burgundy living room "
    "across the gutter; wood floor and wall wash cross the middle; faces and critical props OFF the center fold. "
    "Gift landscape opens ahead from the doorway. "
    "ACTION FIX: Santa is taking wrapped presents OUT of his large burlap sack and placing them UNDER "
    "the Christmas tree — gifts being set out on the floor, accumulating beneath the tree. NOT packing "
    "the sack. NOT putting gifts into the bag. "
    "TREE FIX: exactly ONE Christmas tree on the right half — warm lights, ornaments, presents under it. "
    "NO second tree. NO duplicate tree on the left or center. "
    "STORY BEAT: moment of realization / sneak-up — Santa is still just a man doing his job. Not the "
    "eyes-met hero punch yet. Traditional children's Christmas picture-book illustration, heirloom "
    "storybook quality, heavily painted rich gouache and soft watercolor, visible soft brushstrokes, "
    "gentle blended edges, NOT colored pencil NOT crayon. Warm tree glow + doorway light spill. Art only — "
    "no text, no letters, no watermark. "
    + HARD_WARDROBE
)

NEGATIVE = (
    "two Christmas trees, second tree, duplicate tree, shirtsleeves Santa, Santa in red shirt only, "
    "no coat, packing sack, putting gifts into bag, filling the bag, bright white pajamas, cream-white PJs, "
    "red coat on child, Santa suit on child, eyes meeting, face-to-face stare, text, letters, watermark, "
    "colored pencil, crayon, phone, modern UI"
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
    # Spread refs: allow wide style lock; characters square-ish
    im.thumbnail((SIZE, SIZE), Image.Resampling.LANCZOS)
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
    for i in range(120):
        time.sleep(3 if i else 1)
        st = fal_req(key, submitted["status_url"])
        status = st.get("status") or st.get("queue_status")
        print(f"  [{i}] {status}", flush=True)
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


def write_recipe(vdir: Path, seed: int, req_id: str, url: str) -> None:
    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S02-threshold / {VERSION}

| Field | Value |
|-------|--------|
| **name** | S2 Threshold — enter / Santa placing gifts (coat + one tree fix) |
| **unit** | S02-threshold |
| **book page** | Flow v2 p6\\|7 · FULL SPREAD |
| **page role** | spread |
| **version** | {VERSION} |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · refs: style-lock-v2 + boy-narrator-G0 + santa-G0-v2 |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **fal_url** | `{url}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — v03 composition + wardrobe/action/tree fixes |
| **tier** | dial_mock |
| **previous** | v03 |

## Fixes vs v03

1. Full red coat + black suspenders **over** coat (not shirtsleeves)
2. Presents OUT of sack → UNDER the tree (not packing)
3. Exactly ONE Christmas tree (right)
4. Boy oatmeal/taupe holly PJs (Boy G0) — not bright white

## Brief (Flow v2)

LEFT: boy entering slowly from doorway (over-shoulder), surprise/discovery.  
RIGHT: Santa at work placing gifts under tree — has not noticed boy yet.  
Seamless continuous room. Hard wardrobe append applied.

## Poem ref

L: I didn't know it when I entered the room / to surprise the amazement or even the shock.  
R: Now I'm usually calm… / But what do you say when you sneak up on Santa?
""",
        encoding="utf-8",
    )


def build_board(im: Image.Image, out: Path) -> None:
    w, h = im.size
    mid = w // 2
    left = im.crop((0, 0, mid, h)).convert("RGB")
    right = im.crop((mid, 0, w, h)).convert("RGB")
    panel_h = 520
    sc = panel_h / h
    full_w = int(w * sc)
    full = im.convert("RGB").resize((full_w, panel_h), Image.Resampling.LANCZOS)
    half_w = int(mid * sc)
    left_r = left.resize((half_w, panel_h), Image.Resampling.LANCZOS)
    right_r = right.resize((half_w, panel_h), Image.Resampling.LANCZOS)
    margin, gap, header, label = 28, 16, 72, 56
    sheet_w = margin * 2 + max(full_w, half_w * 2 + gap)
    sheet_h = margin * 2 + header + panel_h + label + gap + panel_h + label
    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S2 Threshold SPREAD — {VERSION} ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 44),
        "Fixes: red coat+suspenders · placing under tree · ONE tree · oatmeal holly PJs",
        fill=(110, 100, 90),
        font=font(13),
    )
    y = margin + header
    sheet.paste(full, (margin, y))
    d.text((margin, y + panel_h + 8), "FULL SPREAD (p6|7 continuous)", fill=(32, 28, 24), font=font(16))
    y2 = y + panel_h + label + gap
    sheet.paste(left_r, (margin, y2))
    sheet.paste(right_r, (margin + half_w + gap, y2))
    d.text((margin, y2 + panel_h + 8), "LEFT half (p6)", fill=(32, 28, 24), font=font(15))
    d.text((margin + half_w + gap, y2 + panel_h + 8), "RIGHT half (p7)", fill=(32, 28, 24), font=font(15))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)


def main() -> None:
    load_env()
    key = fal_key()
    for p in (STYLE, BOY, SANTA):
        if not p.is_file():
            raise SystemExit(f"missing {p}")

    print("upload refs…", flush=True)
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)
    boy_url = prepare_upload(BOY, "boy-narrator-G0.png", key)
    santa_url = prepare_upload(SANTA, "santa-G0-v2.png", key)
    print("style", style_url)
    print("boy", boy_url)
    print("santa", santa_url)

    payload = {
        "prompt": PROMPT,
        "negative_prompt": NEGATIVE,
        "image_urls": [style_url, boy_url, santa_url],
        "image_size": {"width": 2048, "height": 1024},
        "num_images": 1,
        "output_format": "png",
        "enable_safety_checker": True,
        "enable_prompt_expansion": False,
    }
    print("submit Qwen 2 Pro /edit…", flush=True)
    submitted = fal_req(key, ENDPOINT, payload)
    req_id = submitted.get("request_id") or submitted.get("id") or ""
    print("request_id", req_id, flush=True)
    result = wait_result(key, submitted)
    images = result.get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:4000])
    url = images[0]["url"] if isinstance(images[0], dict) else images[0]
    seed = result.get("seed", 0)
    print("url", url, "seed", seed, flush=True)

    vdir_dev = DEV / VERSION
    vdir_mock = MOCKS / VERSION
    vdir_dev.mkdir(parents=True, exist_ok=True)
    vdir_mock.mkdir(parents=True, exist_ok=True)

    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    (vdir_dev / "art.png").write_bytes(data)
    (vdir_mock / "art.png").write_bytes(data)
    im = Image.open(io.BytesIO(data)).convert("RGB")
    print("saved", vdir_dev / "art.png", im.size)

    write_recipe(vdir_dev, seed, req_id, url)
    write_recipe(vdir_mock, seed, req_id, url)

    board = MOCKS / "_INDEX" / f"S02-threshold-comparison-spread-{VERSION}-{DAY}.png"
    build_board(im, board)

    meta = {
        "version": VERSION,
        "seed": seed,
        "request_id": req_id,
        "url": url,
        "size": list(im.size),
        "model": "fal-ai/qwen-image-2/pro/edit",
        "refs": ["style-lock-v2", "boy-narrator-G0", "santa-G0-v2"],
    }
    (vdir_dev / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (vdir_mock / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("DONE", json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
