#!/usr/bin/env python3
"""S12-god-bless v07 — ONE FIX: reindeer IN FRONT pulling sleigh (sleigh at back)."""
from __future__ import annotations

import io
import json
import os
import urllib.request
from pathlib import Path

import fal_client
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
OUT = ROOT / "Media/development/S12-god-bless"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
INDEX = ROOT / "Media/generated/mocks/_INDEX"
DAY = "2026-07-23"

BASE = OUT / "v06" / "art.png"
REF = ROOT / "Images/styles1/15862F89-0D70-4832-B724-7EFA3278B63E.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"

QWEN = "fal-ai/qwen-image-2/pro/edit"
SEEDVR = "fal-ai/seedvr/upscale/image"
SPREAD = (5250, 2625)
PAGE = 2625

PROMPT = """\
Surgical edit of this Christmas FINAL STORY IMAGE spread. KEEP almost everything LOCKED.

IMAGE 1 = current v06 closing spread (house, moon, North Star, 9 deer, oil quality) — preserve it.
IMAGE 2 = COMPOSITION guide for harness order: reindeer are IN FRONT of the sleigh PULLING it;
the sleigh sits at the BACK of the formation; reins connect from the team back to Santa.
IMAGE 3 = Santa G0 v2 — open red coat, warm smile (keep identity).

ONE FIX ONLY — HARNESS / ORDER:
The reindeer must be IN FRONT of the sleigh, PULLING it forward. Santa's sleigh is at the BACK
of the formation (behind the team). Reindeer lead the way toward the house; Santa follows.
Visible reins/harness lines from the team back to the sleigh behind them.
Do NOT put reindeer behind the sleigh. Do NOT reverse the pull direction.

KEEP LOCKED (do not redesign):
- Nine (9) reindeer in pairs (four pairs + Rudolph leading solo at the FRONT of the curve)
- Rudolph soft warm red nose glow (subtle, not laser) — he is furthest/smallest, leading toward house
- Curve still arcs upper-left toward house lower-right
- Victorian house lower-right warm golden windows + snowman + evergreens
- Full moon left behind/above Santa
- North Star right upper + OPEN dark blue sky below (NO text)
- Deep blue sky, rich oil painting, soft cream vignette dissolve
- NO baked text, NO duplicate Santa/sleigh, NO boy

Santa remains clearly visible in ornate sleigh at the REAR, open coat, warm smile, presents in sleigh.
"""

NEG = (
    "reindeer behind the sleigh, deer trailing after Santa, sleigh leading the team, "
    "pushing the sleigh from behind, text, God bless, letters, watermark, "
    "duplicate Santa, second sleigh, laser nose, neon nose, missing house, missing moon, boy"
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


def download(url: str, tries: int = 4) -> Image.Image:
    last: Exception | None = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=180) as resp:
                return Image.open(io.BytesIO(resp.read())).convert("RGB")
        except Exception as e:  # noqa: BLE001
            last = e
            print("retry", i, e)
    assert last is not None
    raise last


def main() -> None:
    load_env()
    if not BASE.is_file():
        BASE2 = OUT / "art.png"
        if not BASE2.is_file():
            raise SystemExit("missing v06 base")
        base_path = BASE2
    else:
        base_path = BASE

    for p in (base_path, REF, SANTA):
        if not p.is_file():
            raise SystemExit(f"missing: {p}")

    base_in = Image.open(base_path).convert("RGB").resize((2048, 1024), Image.Resampling.LANCZOS)
    tmp_base = OUT / "_tmp-v07-base.png"
    base_in.save(tmp_base)
    urls = [
        fal_client.upload_file(str(tmp_base)),
        fal_client.upload_file(str(REF)),
        fal_client.upload_file(str(SANTA)),
    ]

    print("=== Qwen S12-god-bless v07 · reindeer pull in front ===")
    result = fal_client.subscribe(
        QWEN,
        arguments={
            "prompt": PROMPT,
            "negative_prompt": NEG,
            "image_urls": urls,
            "image_size": {"width": 2048, "height": 1024},
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checker": True,
            "enable_prompt_expansion": False,
        },
        with_logs=True,
    )
    print(result)
    qurl = result["images"][0]["url"]
    seed = result.get("seed")
    raw = download(qurl)
    print("qwen", raw.size)
    tmp_q = OUT / "_tmp-v07-qwen.png"
    raw.save(tmp_q)

    try:
        up = fal_client.subscribe(
            SEEDVR,
            arguments={
                "image_url": fal_client.upload_file(str(tmp_q)),
                "upscale_mode": "factor",
                "upscale_factor": 2,
                "noise_scale": 0.1,
                "output_format": "png",
            },
            with_logs=True,
        )
        u = up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"]
        final = download(u).resize(SPREAD, Image.Resampling.LANCZOS)
        print("seedvr ok")
    except Exception as e:  # noqa: BLE001
        print("SeedVR fallback", e)
        final = raw.resize(SPREAD, Image.Resampling.LANCZOS)

    tmp_base.unlink(missing_ok=True)
    tmp_q.unlink(missing_ok=True)

    vdir = OUT / "v07"
    vdir.mkdir(parents=True, exist_ok=True)
    left = final.crop((0, 0, PAGE, PAGE))
    right = final.crop((PAGE, 0, SPREAD[0], SPREAD[1]))
    for dest in (vdir, OUT):
        final.save(dest / "art.png", optimize=True)
        left.save(dest / "art-left.png", optimize=True)
        right.save(dest / "art-right.png", optimize=True)
        print("saved", dest)

    recipe = f"""# RECIPE — S12-god-bless / v07

| Field | Value |
|-------|--------|
| **fix** | Reindeer IN FRONT pulling · sleigh at BACK |
| **version** | **v07** |
| **date** | {DAY} |
| **status** | working |
| **base** | v06 |
| **ref** | styles1/15862F89… (pull order toward house) |
| **seed** | {seed} |
| **fal_url** | `{qurl}` |
| **size** | 5250×2625 |
"""
    (vdir / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    (vdir / "meta.json").write_text(
        json.dumps(
            {
                "version": "v07",
                "status": "working",
                "fix": "reindeer_in_front_pulling_sleigh_at_back",
                "seed": seed,
                "fal_url": qurl,
                "size": list(SPREAD),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "unit": "S12-god-bless",
                "status": "working",
                "version": "v07",
                "pages": "26|27",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from book_review_board import seamless_board

    seamless_board(
        final,
        INDEX / f"S12-god-bless-v07-pull-order-{DAY}.png",
        unit="S12-god-bless",
        version="v07",
        day=DAY,
        tech="Qwen 2 Pro /edit v06 · 5250×2625 · ONE FIX: deer pull in front · sleigh at back",
        subtitle="Reindeer lead toward house · Santa follows · rest locked from v06",
    )

    root = json.loads(FLOW.read_text(encoding="utf-8"))
    note = (
        "S12-god-bless v07 · ONE FIX: reindeer IN FRONT pulling, sleigh at BACK · "
        "ref 15862F89 pull-order · rest locked from v06 · "
        "board S12-god-bless-v07-pull-order-2026-07-23.png"
    )
    for p in root["plates"]:
        if p["id"] in ("p26", "p27"):
            side = "left" if p["id"] == "p26" else "right"
            p.update(
                {
                    "version": "v07",
                    "status": "working",
                    "date": DAY,
                    "notes": note,
                    "path": f"Media/development/S12-god-bless/art-{side}.png",
                    "development_path": "Media/development/S12-god-bless/art.png",
                    "caption": f"p{p['page']} · S12 God Bless {'L' if side=='left' else 'R'} · v07",
                    "model": "Qwen 2 Pro /edit v06 · 5250×2625",
                }
            )
        if p["id"] in ("p28", "p29"):
            p.update(
                {
                    "version": "merged-v07",
                    "status": "merged",
                    "date": DAY,
                    "notes": "Absorbed into S12-god-bless v07 — " + note,
                }
            )
    for d in root["verdicts"]:
        if d.get("page") == "26|27":
            d.update({"version": "v07", "status": "working", "date": DAY, "notes": note})
        if d.get("page") == "28|29":
            d.update({"version": "merged-v07", "status": "merged", "date": DAY, "notes": "MERGED — " + note})
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("DONE", OUT / "art.png", "seed", seed)


if __name__ == "__main__":
    main()
