#!/usr/bin/env python3
"""P02 fireplace + P03 tree — SPLIT singles (About | Dedication), like S1 Approach."""
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
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
# Best continuous scene for identity chops (v01 — before text-layout experiments)
SOURCE = ROOT / "Media/generated/mocks/P02-about-spread/v01/art.png"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-22"
SIZE = 2048

JOBS = [
    {
        "unit": "P02-fireplace",
        "ver": "v01",
        "name": "About — hearth single (SPLIT L)",
        "book_page": "2 · About This Story · SINGLE LEFT",
        "type_zone": "Open burgundy wall (right of fireplace / upper soft wall) for About text cloud",
        "crop": (0.0, 0.0, 0.48, 1.0),  # left of v01 spread
        "prompt": (
            "Create a SINGLE square children's-book page painting (not a half-spread). "
            "Image 1 = watercolor/gouache style, burgundy walls, warm golden light. "
            "Image 2 = fireplace identity — remake as a full standalone page. "
            "Stone fireplace with crackling fire, green garland on mantel, three stockings, "
            "wreath on the chimney. Deep burgundy wall behind with generous open soft wall space "
            "for About text (keep some quiet wall — do not fill the frame with stone). "
            "Warm golden firelight casting soft shadows. Wooden floor visible. "
            "Soft feathered watercolor vignette into cream (FRAME ON). "
            "Art only — no letters, no title, no watermark, no people, no Christmas tree, no door."
        ),
    },
    {
        "unit": "P03-tree",
        "ver": "v01",
        "name": "Dedication — tree + door single (SPLIT R)",
        "book_page": "3 · Dedication · SINGLE RIGHT",
        "type_zone": "Open burgundy wall (left of tree / soft wall) for Dedication text cloud",
        "crop": (0.45, 0.0, 1.0, 1.0),  # right of v01 spread
        "prompt": (
            "Create a SINGLE square children's-book page painting (not a half-spread). "
            "Image 1 = watercolor/gouache style, burgundy walls, warm golden light. "
            "Image 2 = Christmas tree + door identity — remake as a full standalone page. "
            "Full decorated Christmas tree with warm golden lights and ornaments, wrapped presents "
            "at the base, wooden door with wreath and red bow on the right. "
            "Deep burgundy wall behind with generous open soft wall space for Dedication text "
            "(quiet wall to the left of the tree — do not pack the whole frame). "
            "Same warm golden glow as a cozy living room at night. Wooden floor visible. "
            "Soft feathered watercolor vignette into cream (FRAME ON). "
            "Art only — no letters, no title, no watermark, no people, no fireplace."
        ),
    },
]

NEGATIVE = (
    "text, letters, typography, watermark, logo, people, faces, "
    "panorama, double page, gutter line, half-spread crop, "
    "photorealistic, pale cream walls, white walls"
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


def make_crop(job: dict) -> Path:
    src = Image.open(SOURCE).convert("RGB")
    w, h = src.size
    x0, y0, x1, y1 = job["crop"]
    crop = src.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
    # Pad to square on cream so Qwen gets a page-like frame, not a skinny strip
    side = max(crop.size)
    cream = (248, 242, 230)
    sq = Image.new("RGB", (side, side), cream)
    sq.paste(crop, ((side - crop.width) // 2, (side - crop.height) // 2))
    sq = sq.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    out_dir = ROOT / f"Media/generated/mocks/{job['unit']}/{job['ver']}"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "_ref-crop.png"
    sq.save(path, "PNG")
    return path


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(job: dict, seed, req_id: str) -> None:
    out = ROOT / f"Media/generated/mocks/{job['unit']}/{job['ver']}"
    text = f"""# RECIPE — {job['unit']} / {job['ver']}

| Field | Value |
|-------|--------|
| **name** | {job['name']} |
| **unit** | {job['unit']} |
| **book page** | {job['book_page']} |
| **page role** | single |
| **spread side** | {'left' if 'fireplace' in job['unit'] else 'right'} |
| **version** | {job['ver']} |
| **date** | {DAY} |
| **lane** | A2 mock favorite (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · refs: style-lock-v2 + crop from P02-about-spread/v01 |
| **FRAME** | ON |
| **concept** | SPLIT layout pivot — same room as partner page, separate composition (like S1 Approach) |
| **changes** | Replaces failed continuous About/Dedication panorama (P02-about-spread v01–v03) |
| **size** | 2048² dial |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | {'About This Story' if 'fireplace' in job['unit'] else 'Dedication — For my family, with love. — Jack Farrell'} — InDesign later |
| **type_zone** | {job['type_zone']} |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- style: `Media/approved/style-refs/style-lock-v2.png`
- identity crop: `_ref-crop.png` from `Media/generated/mocks/P02-about-spread/v01/art.png`
- partner: {'P03-tree/v01' if 'fireplace' in job['unit'] else 'P02-fireplace/v01'}

## Prompt

{job['prompt']}

## Negative / constraints

{NEGATIVE}

## Notes

- Jon pivot 2026-07-22: continuous fireplace+tree spread failed (dense / squished / stretched). SPLIT like S1.
- Continuity: same burgundy walls, golden light, wooden floor language across both singles.

## Related

- Board: `Media/generated/mocks/_INDEX/P02-P03-split-hearth-tree-board.png`
- Script: `scripts/_scratch/_p02_p03_split_hearth_tree.py`
"""
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(paths_labels: list[tuple[Path, str, str, object]]) -> Path:
    panel, label_h = 720, 100
    gap, margin, header = 28, 36, 100
    w = margin * 2 + panel * 2 + gap
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), (245, 240, 230))
    draw = ImageDraw.Draw(board)
    draw.text((margin, 24), "P02 | P03 — SPLIT hearth + tree (About / Dedication)", fill=(40, 30, 28), font=font(26))
    draw.text(
        (margin, 58),
        "Same room · separate singles · like S1 Approach · Qwen 2 Pro Edit · FRAME ON",
        fill=(90, 70, 60),
        font=font(15),
    )
    for i, (path, title, sub, seed) in enumerate(paths_labels):
        x = margin + i * (panel + gap)
        y = margin + header
        im = Image.open(path).convert("RGB").resize((panel, panel), Image.Resampling.LANCZOS)
        board.paste(im, (x, y))
        draw.rectangle([x, y + panel, x + panel, y + panel + label_h], fill=(235, 228, 215))
        draw.text((x + 12, y + panel + 16), title, fill=(30, 24, 22), font=font(18))
        draw.text((x + 12, y + panel + 46), sub, fill=(80, 60, 50), font=font(14))
        draw.text((x + 12, y + panel + 72), f"seed {seed}", fill=(110, 90, 80), font=font(13))
    out = ROOT / "Media/generated/mocks/_INDEX/P02-P03-split-hearth-tree-board.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()

    print("upload style-lock")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)

    pending = []
    for job in JOBS:
        crop_path = make_crop(job)
        print("crop", job["unit"], crop_path)
        crop_url = prepare_upload(crop_path, f"{job['unit']}-crop.png", key)
        payload = {
            "prompt": job["prompt"],
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, crop_url],
            "image_size": {"width": SIZE, "height": SIZE},
            "num_images": 1,
            "output_format": "png",
            "enable_prompt_expansion": False,
            "enable_safety_checker": True,
        }
        print("submit", job["unit"])
        submitted = fal_req(key, ENDPOINT, payload)
        print("  request_id", submitted.get("request_id"))
        pending.append({**job, "submitted": submitted, "crop_path": crop_path})

    results = []
    for item in pending:
        unit, ver = item["unit"], item["ver"]
        out = ROOT / f"Media/generated/mocks/{unit}/{ver}"
        out.mkdir(parents=True, exist_ok=True)
        print("wait", unit)
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
            json.dumps(
                {"request_id": req_id, "seed": seed, "fal_image_url": img_url, "source_spread": str(SOURCE)},
                indent=2,
            ),
            encoding="utf-8",
        )
        if "fireplace" in unit:
            results.append((art, "P02 LEFT — FIREPLACE", "About · open burgundy for text", seed))
        else:
            results.append((art, "P03 RIGHT — TREE + DOOR", "Dedication · open burgundy for text", seed))

    board = build_board(results)
    print("BOARD", board)


if __name__ == "__main__":
    main()
