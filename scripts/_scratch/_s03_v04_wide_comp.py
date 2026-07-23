#!/usr/bin/env python3
"""S3 Eyes Met v04 — WIDE composition guide + book style + G0 locks."""
from __future__ import annotations

import io
import json
import os
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
DEV = ROOT / "Media/development/S03-eyes-met"
MOCKS = ROOT / "Media/generated/mocks/S03-eyes-met"
COMP = ROOT / "Images/styles3/spread-01-eyes-met-WIDE.png"
STYLE = ROOT / "Media/approved/style-refs/style-lock-v2.png"
BOY = ROOT / "Media/approved/characters/boy-narrator-G0.png"
SANTA = ROOT / "Media/approved/characters/santa-G0-v2.png"
QUALITY = ROOT / "Media/development/S02-threshold/v05/art.png"
DAY = "2026-07-22"
VERSION = "v04"
URLS_OUT = ROOT / "scripts/_scratch/_s03_v04_urls.json"
CHAR_STRIP = ROOT / "scripts/_scratch/_s03_v04_char_strip.png"

PROMPT = (
    "Image 1 = COMPOSITION GUIDE ONLY — copy this layout EXACTLY for a wide two-page Christmas "
    "storybook SPREAD (2:1): fireplace with warm fire on the FAR LEFT wall, stockings on the mantel, "
    "garland with small lights; boy stands in front of the fireplace on the LEFT looking across the room; "
    "Santa kneeling CENTER-RIGHT on one knee among gifts, holding a present mid-task; Christmas tree on "
    "the FAR RIGHT full and decorated; floor between them covered with wrapped presents and ribbons — "
    "a true gift sea; wide full living-room composition, not a close crop. "
    "Image 2 = paint STYLE (style-lock-v2) — watercolor/gouache storybook. "
    "Image 3 = character locks: LEFT half = boy G0 (oatmeal/taupe holly pajamas), RIGHT half = Santa G0 v2 "
    "(red coat with black suspenders OVER the coat). "
    "STYLE FOR THIS BOOK (override cream walls from image 1): deep rich BURGUNDY / wine walls — NOT cream, "
    "NOT beige. Warm golden firelight from the fireplace + luminous golden glow from the tree lights. "
    "Rich oil-painting saturation and deep atmospheric corner shadows matching the locked S2 Threshold "
    "quality bar — deep burgundies, warm golds, luminous highlights. "
    "CHARACTERS: Boy — oatmeal/taupe holly PJs (match image 3 left), barefoot, mouth open in awe, eyes wide, "
    "looking across at Santa. Santa — FULL red coat with black suspenders clearly visible ON TOP of the red "
    "coat fabric (match image 3 right / santa-G0-v2), on one knee, holding a present, looking back at the boy "
    "with a warm kind expression. "
    "CRITICAL: EYES MUST MEET. The boy's gaze locks directly onto Santa's face. Santa looks back at the boy. "
    "Their eyes connect across the gift sea. If eyes do not connect, the image fails. "
    "Art only — no text, no letters, no watermark."
)

NEGATIVE = (
    "cream walls, beige walls, white walls, pale walls, flat lighting, eyes not meeting, looking away, "
    "looking past, averted gaze, suspenders under coat, suspenders on shirt only, shirtsleeves Santa, "
    "no coat, bright white pajamas, Santa suit on child, close crop, tight crop, missing fireplace, "
    "missing stockings, missing tree, empty floor, text, letters, watermark, colored pencil"
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


def make_char_strip() -> Path:
    """Pack boy + santa into one ref so Qwen's 3-slot limit still gets both G0s."""
    boy = Image.open(BOY).convert("RGB")
    santa = Image.open(SANTA).convert("RGB")
    h = 1024
    def fit(im: Image.Image) -> Image.Image:
        r = h / im.height
        return im.resize((max(1, int(im.width * r)), h), Image.Resampling.LANCZOS)

    b, s = fit(boy), fit(santa)
    strip = Image.new("RGB", (b.width + s.width, h), (245, 240, 230))
    strip.paste(b, (0, 0))
    strip.paste(s, (b.width, 0))
    # mild labels in corner for model cue (tiny — will be ignored as style)
    strip.save(CHAR_STRIP, "PNG", optimize=True)
    return CHAR_STRIP


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


def font(sz: int) -> ImageFont.ImageFont:
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def write_recipe(vdir: Path, seed: int, req_id: str, url: str) -> None:
    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — S03-eyes-met / {VERSION}

| Field | Value |
|-------|--------|
| **name** | S3 Eyes Met — WIDE composition guide + burgundy book style |
| **unit** | S03-eyes-met |
| **book page** | Flow v2 p8\\|9 · FULL SPREAD |
| **page role** | spread · emotional centerpiece |
| **version** | {VERSION} |
| **date** | {DAY} |
| **lane** | Dial / mock-up (Qwen 2 Pro Edit) |
| **model** | `fal-ai/qwen-image-2/pro/edit` |
| **settings** | 2048×1024 · composition WIDE + style-lock-v2 + boy\\|santa G0 strip |
| **composition_ref** | `Images/styles3/spread-01-eyes-met-WIDE.png` |
| **seed** | {seed} |
| **request_id** | `{req_id}` |
| **fal_url** | `{url}` |
| **cost_note** | ~$0.08 |
| **output** | art.png |
| **status** | working — fireplace L · boy · Santa center-R · tree R · eyes meet |
| **tier** | dial_mock |
| **previous** | v02 |
| **gpt_pillar** | true (finals later) |

## Layout (from WIDE ref)

- Fireplace + stockings + garland FAR LEFT
- Boy in front of fireplace, awe / open mouth
- Santa kneeling center-right among gifts, holding present
- Tree FAR RIGHT
- Gift sea on floor between them
- Wide full room (not close crop)

## Style overrides

- Burgundy walls (not cream from ref)
- Oil-painting richness = S2 Threshold v05 quality bar
- Watercolor/gouache = style-lock-v2
- Suspenders OVER red coat (santa-G0-v2)
- Eyes must meet
""",
        encoding="utf-8",
    )


def build_board(im: Image.Image, out: Path) -> None:
    w, h = im.size
    mid = w // 2
    left = im.crop((0, 0, mid, h))
    right = im.crop((mid, 0, w, h))
    panel_h = 480
    sc = panel_h / h
    full_w = int(w * sc)
    full = im.resize((full_w, panel_h), Image.Resampling.LANCZOS)
    half_w = int(mid * sc)
    left_r = left.resize((half_w, panel_h), Image.Resampling.LANCZOS)
    right_r = right.resize((half_w, panel_h), Image.Resampling.LANCZOS)
    # also small comp thumb
    comp = Image.open(COMP).convert("RGB")
    comp_h = 220
    comp_w = int(comp.width * (comp_h / comp.height))
    comp_r = comp.resize((comp_w, comp_h), Image.Resampling.LANCZOS)

    margin, gap, header, label = 28, 16, 72, 48
    sheet_w = margin * 2 + max(full_w, half_w * 2 + gap, comp_w)
    sheet_h = margin * 2 + header + comp_h + 36 + panel_h + label + gap + panel_h + label
    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 248, 240))
    d = ImageDraw.Draw(sheet)
    d.text((margin, 14), f"S3 Eyes Met — {VERSION} ({DAY})", fill=(28, 24, 20), font=font(24))
    d.text(
        (margin, 44),
        "Comp = styles3/spread-01-eyes-met-WIDE · burgundy book style · eyes must meet",
        fill=(110, 100, 90),
        font=font(13),
    )
    y = margin + header
    sheet.paste(comp_r, (margin, y))
    d.text((margin, y + comp_h + 8), "COMPOSITION REF (WIDE)", fill=(32, 28, 24), font=font(14))
    y = y + comp_h + 36
    sheet.paste(full, (margin, y))
    d.text((margin, y + panel_h + 8), "FULL SPREAD v04 (p8|9)", fill=(32, 28, 24), font=font(16))
    y2 = y + panel_h + label + gap
    sheet.paste(left_r, (margin, y2))
    sheet.paste(right_r, (margin + half_w + gap, y2))
    d.text((margin, y2 + panel_h + 8), "LEFT (p8)", fill=(32, 28, 24), font=font(15))
    d.text((margin + half_w + gap, y2 + panel_h + 8), "RIGHT (p9)", fill=(32, 28, 24), font=font(15))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG")
    print("board", out)


def upload_refs() -> dict:
    load_env()
    for p in (COMP, STYLE, BOY, SANTA):
        if not p.is_file():
            raise SystemExit(f"missing {p}")
    strip = make_char_strip()
    # Keep composition wide aspect for layout fidelity
    urls = {
        "composition": upload(COMP, "eyes-met-WIDE-comp.png"),
        "style": upload(STYLE, "style-lock-v2.png"),
        "chars": upload(strip, "boy-santa-G0-strip.png"),
    }
    URLS_OUT.write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print(json.dumps(urls, indent=2))
    return urls


def save_result(url: str, seed: int, req_id: str) -> None:
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    for vdir in (DEV / VERSION, MOCKS / VERSION):
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / "art.png").write_bytes(data)
        write_recipe(vdir, seed, req_id, url)
        (vdir / "meta.json").write_text(
            json.dumps(
                {
                    "version": VERSION,
                    "seed": seed,
                    "request_id": req_id,
                    "url": url,
                    "model": "fal-ai/qwen-image-2/pro/edit",
                    "composition_ref": "Images/styles3/spread-01-eyes-met-WIDE.png",
                    "refs": ["WIDE-comp", "style-lock-v2", "boy|santa-G0-strip"],
                    "quality_bar": "S02-threshold/v05",
                    "previous": "v02",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    im = Image.open(io.BytesIO(data)).convert("RGB")
    board = MOCKS / "_INDEX" / f"S03-eyes-met-comparison-spread-{VERSION}-{DAY}.png"
    build_board(im, board)
    subprocess.run(["cmd", "/c", "start", "", str(DEV / VERSION / "art.png")], check=False)
    subprocess.run(["cmd", "/c", "start", "", str(board)], check=False)
    print("saved", DEV / VERSION / "art.png", im.size)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "upload":
        upload_refs()
    elif sys.argv[1] == "save":
        save_result(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        raise SystemExit("upload | save <url> <seed> <req_id>")
