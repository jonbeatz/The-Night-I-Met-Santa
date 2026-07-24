#!/usr/bin/env python3
"""Resume: fetch completed fal jobs for P01 v21/v22 by request_id, save + board."""
from __future__ import annotations

import io
import json
import os
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/P01-title"
V19 = DEV / "v19" / "art.png"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
CREAM = (245, 240, 230)
SIZE = 2048
DAY = "2026-07-22"

# From last successful submits (script crashed after Krea COMPLETED before mkdir)
KREA_RID = "019f8ce0-1596-7931-9d37-e1743f9a5892"
BANANA_RID = "019f8ce0-1662-7400-9251-aa52d534908e"
KREA_EP = "krea/v2/medium/text-to-image"
BANANA_EP = "fal-ai/nano-banana-pro/edit"

PROMPT = open(
    ROOT / "scripts/_scratch/_p01_v21_v22_model_compare.py", encoding="utf-8"
).read()  # fallback unused


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


def key() -> str:
    return (os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY") or "").strip()


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Key {key()}"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode())


def wait(endpoint: str, rid: str) -> dict:
    status_url = f"https://queue.fal.run/{endpoint}/requests/{rid}/status"
    for i in range(80):
        st = get_json(status_url)
        print(endpoint.split("/")[0], i, st.get("status"))
        if st.get("status") in ("COMPLETED", "OK", "completed"):
            return get_json(st.get("response_url") or f"https://queue.fal.run/{endpoint}/requests/{rid}")
        if st.get("status") in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
        time.sleep(3)
    raise SystemExit("timeout " + rid)


def download(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=180) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def board_font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(ver: str, name: str, model: str, cost: str, seed, rid: str, note: str) -> None:
    # read shared prompt from compare script constants via hardcode short
    prompt = (
        "Children's book TITLE PAGE painting, square 1:1, ART ONLY — no text. "
        "Warm gold page-edge whisper · cream center · window LEFT + FULL tree RIGHT tip-to-base. "
        "Deep greens, warm golds, soft reds. Watercolor/gouache. (see compare script for full)"
    )
    text = f"""# RECIPE — P01-title / {ver}

| Field | Value |
|-------|--------|
| **name** | {name} |
| **unit** | P01-title |
| **version** | {ver} |
| **date** | {DAY} |
| **lane** | Model compare (same prompt as v21/v22 pair) |
| **model** | `{model}` |
| **seed** | {seed} |
| **request_id** | `{rid}` |
| **cost_note** | {cost} |
| **output** | art.png |
| **type** | NONE |
| **verdict** | pending |
| **status** | working · model test |
| **tier** | development |
| **note** | {note} |

## Related

- Board: `Media/generated/mocks/_INDEX/P01-title-v19-v21-v22-model-board.png`
- Full prompt: `scripts/_scratch/_p01_v21_v22_model_compare.py`
"""
    out = DEV / ver
    out.mkdir(parents=True, exist_ok=True)
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def main() -> None:
    load_env()
    print("fetch krea", KREA_RID)
    krea = wait(KREA_EP, KREA_RID)
    print("fetch banana", BANANA_RID)
    banana = wait(BANANA_EP, BANANA_RID)

    krea_url = krea["images"][0]["url"] if isinstance(krea["images"][0], dict) else krea["images"][0]
    banana_url = banana["images"][0]["url"] if isinstance(banana["images"][0], dict) else banana["images"][0]
    krea_art = download(krea_url)
    banana_art = download(banana_url)
    if max(krea_art.size) != SIZE:
        krea_art = krea_art.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    if max(banana_art.size) != SIZE:
        banana_art = banana_art.resize((SIZE, SIZE), Image.Resampling.LANCZOS)

    for ver, art, res, model, cost, rid, name, note in [
        (
            "v21",
            krea_art,
            krea,
            KREA_EP,
            "~$0.03",
            KREA_RID,
            "Model test — Krea 2 Medium",
            "Model compare only",
        ),
        (
            "v22",
            banana_art,
            banana,
            BANANA_EP,
            "~$0.15",
            BANANA_RID,
            "Model test — Nano Banana Pro /edit",
            "Model compare only — NEW Banana test (not old Gemini fireplace lock)",
        ),
    ]:
        out = DEV / ver
        out.mkdir(parents=True, exist_ok=True)
        art.save(out / "art.png", "PNG")
        art.save(out / "page.png", "PNG")
        (out / "meta.json").write_text(
            json.dumps(
                {"seed": res.get("seed"), "request_id": rid, "model": model, "cost_note": cost},
                indent=2,
            ),
            encoding="utf-8",
        )
        (out / "result.json").write_text(json.dumps(res, indent=2)[:25000], encoding="utf-8")
        write_recipe(ver, name, model, cost, res.get("seed"), rid, note)
        print("saved", ver, art.size, "seed", res.get("seed"))

    v19 = Image.open(V19).convert("RGB")
    panel, label_h, gap, margin, header = 720, 110, 28, 32, 110
    w = margin * 2 + panel * 3 + gap * 2
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(board)
    draw.text(
        (margin, 24),
        "P01 Title — model compare: v19 Qwen · v21 Krea · v22 Banana Pro",
        fill=(40, 30, 28),
        font=board_font(22),
    )
    draw.text(
        (margin, 62),
        "Same prompt · style-lock-v2 · full tree tip-to-base · gold page frame · cream center · NO text",
        fill=(90, 70, 60),
        font=board_font(13),
    )
    for i, (im, title, sub) in enumerate(
        [
            (v19, "v19 — Qwen 2 Pro Edit", "~$0.08 · rich-tree baseline"),
            (krea_art, "v21 — Krea 2 Medium", "~$0.03 · T2I + style refs"),
            (banana_art, "v22 — Nano Banana Pro /edit", "~$0.15 · finals lane"),
        ]
    ):
        x = margin + i * (panel + gap)
        y = margin + header
        board.paste(im.resize((panel, panel), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + panel + 10), title, fill=(40, 30, 28), font=board_font(16))
        draw.text((x, y + panel + 42), sub, fill=(90, 70, 60), font=board_font(12))
    out = INDEX / "P01-title-v19-v21-v22-model-board.png"
    INDEX.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    print("BOARD", out)


if __name__ == "__main__":
    main()
