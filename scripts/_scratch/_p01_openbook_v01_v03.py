#!/usr/bin/env python3
"""P01 title openbook concepts v01–v03 — one ref each + style-lock-v2, comparison board."""
from __future__ import annotations

import io
import json
import os
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
BASE = ROOT / "Media/generated/mocks/P01-title"
ARCHIVE = BASE / "_archive-pre-openbook-concepts"
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
DAY = "2026-07-22"

NEGATIVE = (
    "text, letters, typography, title, watermark, logo, signature, people, faces, "
    "photorealistic, hard crop, full-bleed with no cream margin, baked words"
)

# Concept maps to USER Image N, not filename order:
# v01 wreath ← Ref2 lamppost title page
# v02 snowman ← Ref3
# v03 landscape ← Ref1
JOBS = [
    {
        "ver": "v01",
        "name": "Wreath-framed title page reimagine",
        "concept_ref": ROOT / "Media/generated/Ai-Image-Tests/openbookFront-Ref2.jpg",
        "ref_label": "openbookFront-Ref2.jpg (user Image 1 — wreath/title)",
        "prompt": (
            "Reimagine ONLY image 2 as a children's book title-page painting. "
            "Use image 1 solely for watercolor/gouache paint style, warm golden light, and burgundy shadow undertones. "
            "KEY idea: a large decorative Christmas wreath (evergreen, holly, red berries, soft red ribbon) "
            "frames the CENTER of the page — open cream space INSIDE the wreath for title text later. "
            "Behind/through the wreath: soft snowy village or winter landscape with warm window lights. "
            "Keep a decorative lamppost with a festive red bow in the foreground. "
            "Optional tiny Santa sleigh silhouette in the distant glow — no detail. "
            "Soft feathered watercolor vignette into cream paper (FRAME ON). "
            "Art only — no letters, no title, no copyright, no watermark, no people."
        ),
    },
    {
        "ver": "v02",
        "name": "Snowman lantern circular vignette",
        "concept_ref": ROOT / "Media/generated/Ai-Image-Tests/openbookFront-Ref3.jpg",
        "ref_label": "openbookFront-Ref3.jpg (user Image 2 — snowman)",
        "prompt": (
            "Reimagine ONLY image 2 as a children's book title-page painting. "
            "Use image 1 solely for watercolor/gouache paint style, warm golden light, and burgundy in deep shadows. "
            "KEY idea: contained soft CIRCULAR vignette — intimate winter night scene. "
            "Center: cheerful snowman with black top hat (holly), striped scarf, stick arms, glowing lantern "
            "as the warm golden focal light. Snow-covered evergreens flank left and right. "
            "Full moon and soft starry night sky. Snowman + lantern light are the clear focus. "
            "Feathered circular wash fading to cream paper (FRAME ON). "
            "Art only — no letters, no title, no copyright, no watermark, no people."
        ),
    },
    {
        "ver": "v03",
        "name": "Quiet watercolor winter landscape",
        "concept_ref": ROOT / "Media/generated/Ai-Image-Tests/openbookFront-Ref1.jpg",
        "ref_label": "openbookFront-Ref1.jpg (user Image 3 — landscape)",
        "prompt": (
            "Reimagine ONLY image 2 as a children's book title-page painting. "
            "Use image 1 solely for watercolor/gouache paint style and burgundy undertones in distant shadows. "
            "KEY idea: peaceful quiet winter landscape — mood over decoration. "
            "Snow-covered evergreens, white picket fence with ONE red bow accent (only bright color pop), "
            "soft winter sky peach-to-lavender. Large open cream space across TOP and CENTER for title. "
            "Visible brushstrokes, soft feathered vignette edges into cream (FRAME ON). "
            "No lamppost clutter, no wreath, no snowman, no sleigh, no village. "
            "Art only — no letters, no title, no copyright, no watermark, no people."
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
    if path.suffix.lower() == ".png":
        im.save(buf, format="PNG", optimize=True)
        ctype = "image/png"
        if not name.lower().endswith(".png"):
            name = Path(name).with_suffix(".png").name
    else:
        im.save(buf, format="JPEG", quality=92)
        ctype = "image/jpeg"
        name = Path(name).with_suffix(".jpg").name
    return upload_bytes(key, name, buf.getvalue(), ctype)


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
        body = e.read().decode(errors="replace")
        raise SystemExit(f"HTTP {e.code}: {body[:2000]}") from e


def wait_result(key: str, submitted: dict) -> dict:
    status_url = submitted["status_url"]
    response_url = submitted.get("response_url")
    for i in range(100):
        time.sleep(3 if i else 1)
        st = fal_req(key, status_url)
        status = st.get("status") or st.get("queue_status")
        print(f"  [{i}] {status}")
        if status in ("COMPLETED", "OK", "completed"):
            return fal_req(key, response_url) if response_url else st
        if status in ("FAILED", "ERROR", "failed"):
            raise SystemExit(json.dumps(st, indent=2)[:3000])
    raise SystemExit("timeout")


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def archive_old() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for ver in ("v01", "v02", "v03"):
        src = BASE / ver
        if not src.is_dir():
            continue
        # skip if already only our new art from a partial run
        dest = ARCHIVE / f"{ver}-{int(time.time())}"
        if any(src.iterdir()):
            print("archive", src, "->", dest)
            shutil.move(str(src), str(dest))


def write_recipe(job: dict, seed, req_id: str, style_url: str, concept_url: str) -> None:
    out = BASE / job["ver"]
    prompt = job["prompt"]
    text = f"""# RECIPE — P01-title / {job["ver"]}

| Field | Value |
|-------|--------|
| **name** | {job["name"]} |
| **unit** | P01-title |
| **book page** | 1 · Title + Copyright · SINGLE (right-hand) |
| **page role** | single |
| **spread side** | n/a |
| **version** | {job["ver"]} |
| **date** | {DAY} |
| **lane** | A2 mock favorite (Qwen 2 Pro Edit) |
| **service** | fal.ai |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048² · enable_prompt_expansion=false · 2 refs only (no blend of concept refs) |
| **FRAME** | ON |
| **concept** | One-ref reimagine — do not blend other openbook refs |
| **changes** | Openbook concept dial set (archived prior {job["ver"]} → `_archive-pre-openbook-concepts/`) |
| **size** | 2048² |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **script_text** | InDesign later — art only |
| **type_zone** | Cream open area for title (wreath interior / upper sky / top-center) |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- boy: n/a
- santa: n/a (optional distant sleigh silhouette on v01 only)
- jack: n/a
- style / frame:
  - image 1: `Media/approved/style-refs/style-lock-v2.png` ({style_url})
  - image 2: `{job["ref_label"]}` ({concept_url})
- base / edit source: single-concept reimagine (not blended with sibling refs)

## Prompt

{prompt}

## Negative / constraints

{NEGATIVE}

## Gotchas

- Do **not** attach sibling openbook refs — one concept image only + style-lock.
- Filename vs user Image #: Ref2→v01 wreath · Ref3→v02 snowman · Ref1→v03 landscape.

## Notes

- Comparison board: `Media/generated/mocks/_INDEX/P01-title-openbook-v01-v03-board.png`

## Related

- Script: `scripts/_scratch/_p01_openbook_v01_v03.py`
- Sibling dials: P01-title v01 / v02 / v03 (this set)
"""
    (out / "RECIPE.md").write_text(text, encoding="utf-8")


def build_board(results: list[dict]) -> Path:
    panel, label_h = 720, 96
    gap, margin, header = 24, 32, 88
    w = margin * 2 + panel * 3 + gap * 2
    h = margin * 2 + header + panel + label_h
    board = Image.new("RGB", (w, h), (245, 240, 230))
    draw = ImageDraw.Draw(board)
    draw.text((margin, 28), "P01 Title — openbook concepts (one ref each + style-lock-v2)", fill=(40, 30, 28), font=font(28))
    draw.text((margin, 58), "Qwen 2 Pro Edit · FRAME ON · no baked text · do not blend", fill=(90, 70, 60), font=font(16))
    for i, r in enumerate(results):
        x = margin + i * (panel + gap)
        y = margin + header
        im = Image.open(r["path"]).convert("RGB")
        im = im.resize((panel, panel), Image.Resampling.LANCZOS)
        board.paste(im, (x, y))
        draw.rectangle([x, y + panel, x + panel, y + panel + label_h], fill=(235, 228, 215))
        draw.text((x + 12, y + panel + 14), r["title"], fill=(30, 24, 22), font=font(18))
        draw.text((x + 12, y + panel + 44), r["sub"], fill=(80, 60, 50), font=font(14))
        draw.text((x + 12, y + panel + 68), f"seed {r['seed']}", fill=(110, 90, 80), font=font(13))
    out = ROOT / "Media/generated/mocks/_INDEX/P01-title-openbook-v01-v03-board.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    board.save(out, "PNG")
    return out


def main() -> None:
    load_env()
    key = fal_key()
    archive_old()

    print("upload style-lock-v2")
    style_url = prepare_upload(STYLE, "style-lock-v2.png", key)

    # submit all three, then poll
    pending = []
    for job in JOBS:
        print("upload", job["concept_ref"].name, "for", job["ver"])
        concept_url = prepare_upload(job["concept_ref"], job["concept_ref"].name, key)
        payload = {
            "prompt": job["prompt"],
            "negative_prompt": NEGATIVE,
            "image_urls": [style_url, concept_url],
            "image_size": {"width": 2048, "height": 2048},
            "num_images": 1,
            "output_format": "png",
            "enable_prompt_expansion": False,
            "enable_safety_checker": True,
        }
        print("submit", job["ver"], "prompt_len", len(job["prompt"]))
        submitted = fal_req(key, ENDPOINT, payload)
        pending.append({**job, "submitted": submitted, "style_url": style_url, "concept_url": concept_url})
        print("  request_id", submitted.get("request_id"))

    results = []
    for item in pending:
        ver = item["ver"]
        out = BASE / ver
        out.mkdir(parents=True, exist_ok=True)
        print("wait", ver)
        result = wait_result(key, item["submitted"])
        (out / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        images = result.get("images") or []
        img_url = images[0]["url"] if isinstance(images[0], dict) else images[0]
        seed = result.get("seed")
        req_id = item["submitted"].get("request_id")
        art = out / "art.png"
        urllib.request.urlretrieve(img_url, art)
        print("saved", art, Image.open(art).size, "seed", seed)
        write_recipe(item, seed, req_id, item["style_url"], item["concept_url"])
        (out / "meta.json").write_text(
            json.dumps(
                {
                    "request_id": req_id,
                    "seed": seed,
                    "style_url": item["style_url"],
                    "concept_url": item["concept_url"],
                    "fal_image_url": img_url,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        short = {
            "v01": ("v01 WREATH FRAME", "Ref2 reimagine · title space inside wreath"),
            "v02": ("v02 SNOWMAN LANTERN", "Ref3 reimagine · circular vignette"),
            "v03": ("v03 QUIET LANDSCAPE", "Ref1 reimagine · fence bow · open cream"),
        }[ver]
        results.append({"path": art, "title": short[0], "sub": short[1], "seed": seed})

    board = build_board(results)
    print("BOARD", board)


if __name__ == "__main__":
    main()
