#!/usr/bin/env python3
"""S6 Cocoa LEFT v02 — faint village whisper + soft vignette dissolve; R stays locked v01."""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
sys.path.insert(0, str(ROOT / "scripts"))

from book_review_board import text_image_board  # noqa: E402

DEV = ROOT / "Media/development/S06-cocoa"
MOCKS = ROOT / "Media/generated/mocks/S06-cocoa"
VILLAGE = ROOT / "Images/styles3/E-back-village-snow.png"
HEARTH = ROOT / "Images/styles3/p28-family-hearth.png"
RIGHT_LOCKED = DEV / "v01" / "art-right.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
DAY = "2026-07-22"
VERSION = "v02"
URLS_OUT = ROOT / "scripts/_scratch/_s06_v02_urls.json"

PROMPT_L = (
    "Image 1 = cream watercolor paper base. "
    "Image 2 = SNOWY VILLAGE atmosphere reference (distant cottages, warm windows, crescent moon, "
    "stars, snow-covered evergreens) — use ONLY as a VERY FAINT whisper. "
    "Image 3 = FRAME TREATMENT reference — soft watercolor vignette that dissolves into cream/ivory "
    "at the edges (richest color toward center, gentle bleed outward to paper). "
    "Create a SINGLE square children's-book TEXT PAGE (1:1) for S6 Cocoa LEFT (p14). "
    "Dreamy watercolor text page: the village scene sits VERY faintly in the background — "
    "like a watercolor wash at about 15-25% opacity — atmosphere only, NOT a full illustration. "
    "The village is a whisper: Christmas Eve mood without distracting from poem words. "
    "Apply the vignette frame treatment: the whole page is one cohesive watercolor painting that "
    "breathes — scene gently bleeds and fades to soft ivory/cream paper at the edges. "
    "NOT a hard-edged illustration dropped on paper. NOT a busy room scene. "
    "LARGE OPEN quiet CENTER for live poem text — fully readable against soft wash. "
    "Cream/ivory base, watercolor paper texture, heirloom storybook feel. "
    "NO Santa. NO boy. NO fireplace interior as the main subject. NO literal product props "
    "(no coat/tie/ring row). NO snowman vignette as a hard sticker. Art only — no letters, no poem text."
)

NEG_L = (
    "strong opaque illustration, high contrast village, busy full scene, hard edges, "
    "rectangular photo crop, Santa, child, boy, indoor fireplace as hero, Christmas tree filling page, "
    "coat tie ring product row, snowman sticker, dark muddy center, text, letters, watermark, "
    "100% opacity painting, competing focal points in the middle"
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


def write_recipe(vdir: Path, seed: int, req_id: str, url: str) -> None:
    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S06-cocoa / {VERSION} LEFT

| Field | Value |
|-------|--------|
| **name** | S6 Cocoa L — faint village whisper text page |
| **unit** | S06-cocoa |
| **book page** | Flow v2 p14 TEXT (p15 R stays v01 KEEP) |
| **version** | {VERSION} (LEFT only) |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **refs** | cream base · E-back-village-snow · p28-family-hearth (vignette frame) |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **fal_url** | `{url}` |
| **status** | working — village whisper 15-25% · soft dissolve edges |
| **paired_right** | v01 art-right KEEP (cocoa prop hero) |

## Intent

Dreamy text page: distant snowy village as faint atmosphere; Ref 2 soft vignette dissolve to cream edges; open center for poem.
""",
        encoding="utf-8",
    )


def upload_phase() -> dict:
    load_env()
    cream = Image.new("RGB", (1536, 1536), (250, 244, 232))
    cream_path = ROOT / "scripts/_scratch/_s06_v02_cream.png"
    cream.save(cream_path, "PNG")
    urls = {
        "cream": upload(cream_path, "s06-v02-cream.png", (1536, 1536)),
        "village": upload(VILLAGE, "e-back-village-snow.png"),
        "hearth_frame": upload(HEARTH, "p28-family-hearth-frame.png"),
        "prompt": PROMPT_L,
        "negative": NEG_L,
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps({k: urls[k] for k in ("cream", "village", "hearth_frame")}, indent=2))
    return urls


def save(url: str, seed: int, req_id: str) -> None:
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    for base in (DEV / VERSION, MOCKS / VERSION):
        base.mkdir(parents=True, exist_ok=True)
        (base / "art-left.png").write_bytes(data)
        # keep locked right alongside for the pair
        if RIGHT_LOCKED.exists():
            (base / "art-right.png").write_bytes(RIGHT_LOCKED.read_bytes())
        write_recipe(base, seed, req_id, url)
        (base / "meta.json").write_text(
            json.dumps(
                {
                    "version": VERSION,
                    "side": "left",
                    "layout": "text_plus_image",
                    "left": {"url": url, "seed": seed, "request_id": req_id},
                    "right": {"locked": "v01", "path": str(RIGHT_LOCKED.relative_to(ROOT))},
                    "model": "fal-ai/qwen-image-2/pro/edit",
                    "refs": ["E-back-village-snow.png", "p28-family-hearth.png"],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    (DEV / "art-left.png").write_bytes(data)
    left = Image.open(io.BytesIO(data)).convert("RGB")
    right = Image.open(RIGHT_LOCKED).convert("RGB")
    board = MOCKS / "_INDEX" / f"S06-cocoa-{VERSION}-L-plus-R-v01-{DAY}.png"
    text_image_board(
        left,
        right,
        board,
        unit="S06-cocoa",
        version=f"{VERSION} L + v01 R KEEP",
        day=DAY,
        tech="Qwen 2 Pro /edit · square · village whisper + vignette frame",
        subtitle="L = faint village dissolve · R = cocoa prop hero LOCKED",
    )
    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art-left.png")], check=False)
    print("saved", DEV / VERSION)
    print("board", board)


if __name__ == "__main__":
    if sys.argv[1] == "upload":
        upload_phase()
    elif sys.argv[1] == "save":
        save(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        raise SystemExit("upload | save url seed req_id")
