#!/usr/bin/env python3
"""Age-up boy on S01-L, S03, S04-R to match S07/S08 (~5–7). Qwen dials — do not overwrite KEEP.
Image1=plate · Image2=S07 age ref · Image3=boy G0.
"""
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
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
AGE_REF = DEV / "S07-proof" / "art.png"  # age target plate
ENDPOINT = "https://queue.fal.run/fal-ai/qwen-image-2/pro/edit"
DAY = "2026-07-30"
GEN = 2048

JOBS = [
    {
        "unit": "S01-approach",
        "ver": "v15-age-s07",
        "src": DEV / "S01-approach" / "art-left.png",
        "kind": "single",
        "out_name": "art-left.png",
        "note": "Crawl doorway L — age boy to S07 (~5-7), keep crawl pose",
    },
    {
        "unit": "S03-eyes-met",
        "ver": "v08-age-s07",
        "src": DEV / "S03-eyes-met" / "art.png",
        "kind": "spread",
        "out_name": "art.png",
        "note": "Eyes-met spread — age boy only; keep Santa/scene; quality-bar sensitive",
    },
    {
        "unit": "S04-sit-here",
        "ver": "v14-age-s07",
        "src": DEV / "S04-sit-here" / "art-right.png",
        "kind": "single",
        "out_name": "art-right.png",
        "note": "Sit-here R — age boy; then stitch art.png with existing art-left",
        "stitch_left": DEV / "S04-sit-here" / "art-left.png",
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


def prepare_upload(path: Path, name: str, key: str, size: tuple[int, int] | None = None) -> str:
    im = Image.open(path).convert("RGB")
    if size:
        im = im.resize(size, Image.Resampling.LANCZOS)
    else:
        im.thumbnail((GEN * 2, GEN), Image.Resampling.LANCZOS)
        # cap longest side to GEN*2 for spreads, GEN for singles handled below
        w, h = im.size
        scale = min(1.0, GEN / max(w, h) * (2 if w > h * 1.2 else 1))
        if scale < 1:
            im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
        # Prefer max dimension GEN for singles, 2048x1024-ish for spreads
        if im.size[0] >= im.size[1] * 1.5:
            im.thumbnail((GEN * 2, GEN), Image.Resampling.LANCZOS)
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


def age_prompt(note: str, is_spread: bool) -> str:
    shape = "wide children's book SPREAD" if is_spread else "square children's book page"
    return (
        f"Edit Image 1 ({shape}). CRITICAL: only change the BOY's AGE — make him the SAME age as "
        f"the boy in Image 2 (about 5–7 years old: longer limbs, less baby-round face, more school-age "
        f"proportions — NOT a toddler). Keep Image 1's pose, camera, lighting, room, gifts, and Santa "
        f"exactly. Do not redesign the scene. Image 3 = Boy G0 identity lock (messy light-brown hair "
        f"with golden highlights, brown eyes, rosy cheeks, oatmeal holly PJs with red trim/cuffs). "
        f"Apply Image 3 face/hair/PJs identity at the older age matching Image 2. "
        f"Scene note: {note}. ART ONLY — no typography."
    )


NEGATIVE = (
    "toddler, baby face, chubby toddler, 2 year old, 3 year old, oversized baby head, "
    "different boy, wrong pajamas, red coat on boy, change Santa pose, new room, "
    "title text, typography, extra child"
)


def save_docs(out: Path, job: dict, seed: int, urls: list[str], result_url: str) -> None:
    (out / "RECIPE.md").write_text(
        f"""# RECIPE — {job['unit']} / {job['ver']}

| Field | Value |
|-------|--------|
| **unit** | {job['unit']} |
| **version** | {job['ver']} |
| **date** | {DAY} |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **seed** | {seed} |
| **status** | dial — age-up alt (awaiting Jon KEEP) |
| **age target** | S07-proof / S08-gone boy (~5–7) |
| **identity** | boy-narrator-G0 |
| **does not replace KEEP** | until Jon says keep |

## Change

Age the boy only to match S07/S08. Pose/scene/Santa unchanged.

## Note

{job['note']}
""",
        encoding="utf-8",
    )
    (out / "meta.json").write_text(
        json.dumps(
            {
                "unit": job["unit"],
                "version": job["ver"],
                "date": DAY,
                "status": "dial",
                "seed": seed,
                "age_target": "S07-proof / S08-gone",
                "image_urls": urls,
                "result_url": result_url,
                "note": job["note"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def board_pair(keep: Image.Image, alt: Image.Image, title: str, dest: Path) -> None:
    k = keep.convert("RGB")
    a = alt.convert("RGB")
    # normalize to same height
    th = 900
    def fit(im: Image.Image) -> Image.Image:
        r = th / im.size[1]
        return im.resize((max(1, int(im.size[0] * r)), th), Image.Resampling.LANCZOS)

    k, a = fit(k), fit(a)
    pad, lh = 16, 44
    w = k.size[0] + a.size[0] + pad * 3
    h = th + pad * 2 + lh
    board = Image.new("RGB", (w, h), (250, 248, 244))
    draw = ImageDraw.Draw(board)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    draw.text((pad, 10), title, fill=(40, 40, 40), font=font)
    board.paste(k, (pad, lh))
    board.paste(a, (pad * 2 + k.size[0], lh))
    dest.parent.mkdir(parents=True, exist_ok=True)
    board.save(dest, optimize=True)


def run_job(key: str, job: dict) -> None:
    src: Path = job["src"]
    out = DEV / job["unit"] / job["ver"]
    out.mkdir(parents=True, exist_ok=True)
    is_spread = job["kind"] == "spread"
    print(f"\n=== {job['unit']} {job['ver']} ===")
    print("upload", src.name)

    if is_spread:
        # upload at ~2048x1024
        src_im = Image.open(src).convert("RGB")
        upload_size = (2048, 1024)
        src_im_u = src_im.resize(upload_size, Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        src_im_u.save(buf, format="PNG", optimize=True)
        url_src = upload_bytes(key, f"{job['unit']}-src.png", buf.getvalue(), "image/png")
        out_w, out_h = 5250, 2625
        image_size = {"width": 2048, "height": 1024}
    else:
        url_src = prepare_upload(src, f"{job['unit']}-src.png", key, size=(GEN, GEN))
        out_w = out_h = 2625
        image_size = {"width": GEN, "height": GEN}

    # Age ref: upload S07 (thumbnail) — boy on right of that spread is the age target
    url_age = prepare_upload(AGE_REF, "age-s07.png", key)
    url_boy = prepare_upload(BOY, "boy-G0.png", key, size=(GEN, GEN))
    urls = [url_src, url_age, url_boy]

    print("submit Qwen")
    submitted = fal_req(
        key,
        ENDPOINT,
        {
            "prompt": age_prompt(job["note"], is_spread),
            "negative_prompt": NEGATIVE[:500],
            "image_urls": urls,
            "num_images": 1,
            "output_format": "png",
            "enable_prompt_expansion": False,
            "image_size": image_size,
        },
    )
    print("request_id", submitted.get("request_id"))
    result = wait_result(key, submitted)
    images = result.get("images") or []
    if not images:
        raise SystemExit(json.dumps(result, indent=2)[:3000])
    result_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    seed = int(result.get("seed") or 0)

    raw = out / "art-raw.png"
    download(result_url, raw)
    im = Image.open(raw).convert("RGB")
    im = im.resize((out_w, out_h), Image.Resampling.LANCZOS)
    im.save(out / job["out_name"], optimize=True, dpi=(300, 300))

    if is_spread:
        # triplet
        half = out_w // 2
        im.crop((0, 0, half, out_h)).save(out / "art-left.png", optimize=True, dpi=(300, 300))
        im.crop((half, 0, out_w, out_h)).save(out / "art-right.png", optimize=True, dpi=(300, 300))
        im.save(out / "art.png", optimize=True, dpi=(300, 300))

    if job.get("stitch_left"):
        left = Image.open(job["stitch_left"]).convert("RGB").resize((2625, 2625), Image.Resampling.LANCZOS)
        right = im if im.size == (2625, 2625) else im.resize((2625, 2625), Image.Resampling.LANCZOS)
        if job["out_name"] == "art-right.png":
            right = Image.open(out / "art-right.png").convert("RGB")
        spread = Image.new("RGB", (5250, 2625))
        spread.paste(left, (0, 0))
        spread.paste(right, (2625, 0))
        spread.save(out / "art.png", optimize=True, dpi=(300, 300))
        # copy left into version folder for triplet completeness
        left.save(out / "art-left.png", optimize=True, dpi=(300, 300))

    save_docs(out, job, seed, urls, result_url)

    # comparison board vs current KEEP
    keep_im = Image.open(src).convert("RGB")
    alt_im = Image.open(out / ("art.png" if is_spread or job.get("stitch_left") else job["out_name"]))
    board_pair(
        keep_im,
        alt_im,
        f"{job['unit']} KEEP  vs  {job['ver']} (boy age → S07/S08)",
        INDEX / f"{job['unit']}-{job['ver']}-board.png",
    )
    print("saved", out, "seed", seed)


def main() -> None:
    load_env()
    key = fal_key()
    for p in (BOY, AGE_REF):
        if not p.is_file():
            raise SystemExit(f"missing {p}")
    for job in JOBS:
        if not job["src"].is_file():
            raise SystemExit(f"missing {job['src']}")
        run_job(key, job)
    print("\nDONE all age-up dials — awaiting Jon KEEP before dashboard promote")


if __name__ == "__main__":
    main()
