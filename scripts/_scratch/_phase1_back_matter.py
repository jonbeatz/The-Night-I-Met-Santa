#!/usr/bin/env python3
"""Phase 1: frame p31 Jack portrait; SeedVR upscale p32/p33 to 2625; keep p30."""
from __future__ import annotations

import io
import json
import os
import shutil
import urllib.request
from pathlib import Path

import fal_client
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
JACK = ROOT / "Media/approved/characters/jack-farrell-portrait.png"
P30 = ROOT / "Media/development/P-thank-you/art.png"
P32 = ROOT / "Media/development/P-quiet-close/art-left.png"
P33 = ROOT / "Media/development/P-quiet-close/art-right.png"
AUTHOR = ROOT / "Media/development/P-author"
QUIET = ROOT / "Media/development/P-quiet-close"
FRAME_REF = ROOT / "Media/approved/style-refs/spread-frame-reference.png"
FLOW = ROOT / "Media/generated/mocks/_FLOW-CURRENT.json"
SEEDVR = "fal-ai/seedvr/upscale/image"
PAGE = 2625
CREAM = (252, 246, 238)
DAY = "2026-07-23"


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


def cream_frame_square(art: Image.Image, size: int = PAGE) -> Image.Image:
    """Soft dissolve to cream on all sides (match p30 language)."""
    art = art.convert("RGB").resize((size, size), Image.Resampling.LANCZOS)
    cream = Image.new("RGB", (size, size), CREAM)

    # Soft rounded content mask — vignette stays near edges
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    pad = int(size * 0.06)
    d.rounded_rectangle([pad, pad, size - pad, size - pad], radius=int(size * 0.08), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=int(size * 0.045)))

    # Optional: blend with frame-ref cream detection if present
    if FRAME_REF.is_file():
        fr = Image.open(FRAME_REF).convert("RGB").resize((size, size), Image.Resampling.LANCZOS)
        arr = np.asarray(fr, dtype=np.float32)
        cream_a = np.array(CREAM, dtype=np.float32)
        dist = np.linalg.norm(arr - cream_a, axis=2)
        content = np.clip((dist - 12.0) / 40.0, 0, 1)
        content = content * content * (3 - 2 * content)
        m = np.asarray(mask, dtype=np.float32) / 255.0
        m = np.clip(np.maximum(m, content * 0.35), 0, 1)
        # Keep center fully opaque
        yy, xx = np.mgrid[0:size, 0:size]
        cy, cx = size / 2.0, size / 2.0
        ell = 1.0 - np.clip(((xx - cx) / (size * 0.42)) ** 2 + ((yy - cy) / (size * 0.42)) ** 2, 0, 1)
        ell = ell * ell * (3 - 2 * ell)
        m = np.clip(np.maximum(m, ell), 0, 1)
        mask = Image.fromarray((m * 255).astype(np.uint8), mode="L")
        mask = mask.filter(ImageFilter.GaussianBlur(radius=8))

    return Image.composite(art, cream, mask)


def seedvr_to_square(src: Path, dest: Path) -> None:
    load_env()
    im = Image.open(src).convert("RGB")
    tmp = dest.parent / f"_tmp-{dest.stem}.png"
    # SeedVR wants reasonable input; keep native then upscale
    im.save(tmp)
    print("SeedVR", src.name, "->", dest.name)
    up = fal_client.subscribe(
        SEEDVR,
        arguments={
            "image_url": fal_client.upload_file(str(tmp)),
            "upscale_mode": "factor",
            "upscale_factor": 2.5,
            "noise_scale": 0.08,
            "output_format": "png",
        },
        with_logs=True,
    )
    u = up["image"]["url"] if isinstance(up.get("image"), dict) else up["image"]
    out = download(u).resize((PAGE, PAGE), Image.Resampling.LANCZOS)
    # Reinforce cream edge dissolve for quiet-close singles
    out = cream_frame_square(out, PAGE)
    out.save(dest, optimize=True)
    tmp.unlink(missing_ok=True)
    print("saved", dest, out.size)


def frame_jack() -> Path:
    AUTHOR.mkdir(parents=True, exist_ok=True)
    raw = Image.open(JACK).convert("RGB")
    framed = cream_frame_square(raw, PAGE)
    out = AUTHOR / "art.png"
    framed.save(out, optimize=True)
    # version archive
    vdir = AUTHOR / "v01-framed"
    vdir.mkdir(exist_ok=True)
    shutil.copy2(out, vdir / "art.png")
    (vdir / "RECIPE.md").write_text(
        f"""# RECIPE — P-author / v01-framed (p31)

| Field | Value |
|-------|--------|
| **source** | Media/approved/characters/jack-farrell-portrait.png (LOCKED — not regenerated) |
| **treatment** | Pillow cream soft-dissolve vignette @ 2625×2625 |
| **date** | {DAY} |
| **note** | Approved file untouched; development framed plate for InDesign mock |
""",
        encoding="utf-8",
    )
    (AUTHOR / "meta.json").write_text(
        json.dumps(
            {
                "unit": "P-author",
                "page": 31,
                "version": "v01-framed",
                "source": "Media/approved/characters/jack-farrell-portrait.png",
                "status": "ready",
                "size": [PAGE, PAGE],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("p31 framed", out)
    return out


def main() -> None:
    load_env()
    # Audit notes
    audit = {
        "p30": {
            "grade": "PASS",
            "action": "FINE AS-IS",
            "notes": "2625² cream paper + vignette present; no baked text; faint warm edge OK as Jack whisper",
            "size": list(Image.open(P30).size),
        },
        "p31": {
            "grade": "PASS after frame",
            "action": "FRAME ONLY (no regen)",
            "notes": "Approved portrait locked; Pillow cream vignette @ 2625 for mock/InDesign",
        },
        "p32": {
            "grade": "FAIL resolution",
            "action": "UPSCALE + frame reinforce (content keep-leaning)",
            "notes": "Was 1024²; quiet room mood OK; oval vignette → soft cream dissolve @ 2625",
            "size_before": list(Image.open(P32).size),
        },
        "p33": {
            "grade": "FAIL resolution",
            "action": "UPSCALE + frame reinforce (content keep-leaning)",
            "notes": "Was 1024²; ornament/mantel matches plan; no baked text",
            "size_before": list(Image.open(P33).size),
        },
    }

    # 1) p31
    jack_out = frame_jack()

    # 2) Archive old quiet-close then upscale
    arch = QUIET / "_archive-1024-v01"
    arch.mkdir(exist_ok=True)
    for name in ("art-left.png", "art-right.png"):
        src = QUIET / name
        if src.is_file() and Image.open(src).size[0] < 2000:
            shutil.copy2(src, arch / name)

    seedvr_to_square(arch / "art-left.png" if (arch / "art-left.png").is_file() else P32, QUIET / "art-left.png")
    seedvr_to_square(arch / "art-right.png" if (arch / "art-right.png").is_file() else P33, QUIET / "art-right.png")

    # Also write art.png as a side-by-side contact? Not needed — singles only.
    (QUIET / "meta.json").write_text(
        json.dumps(
            {
                "unit": "P-quiet-close",
                "pages": "32|33",
                "version": "v02-upscale-framed",
                "status": "working",
                "note": "SeedVR 2625 + cream dissolve; content from v01 keep-leaning",
                "date": DAY,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (QUIET / "v02-upscale-framed").mkdir(exist_ok=True)
    shutil.copy2(QUIET / "art-left.png", QUIET / "v02-upscale-framed" / "art-left.png")
    shutil.copy2(QUIET / "art-right.png", QUIET / "v02-upscale-framed" / "art-right.png")

    audit["p32"]["size_after"] = list(Image.open(QUIET / "art-left.png").size)
    audit["p33"]["size_after"] = list(Image.open(QUIET / "art-right.png").size)
    audit["p31"]["path"] = str(jack_out.relative_to(ROOT)).replace("\\", "/")

    (QUIET / "AUDIT-phase1.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    (AUTHOR / "AUDIT-phase1.json").write_text(json.dumps({"p31": audit["p31"]}, indent=2), encoding="utf-8")

    # FLOW updates
    root = json.loads(FLOW.read_text(encoding="utf-8"))
    for p in root["plates"]:
        if p["id"] == "p30":
            p["notes"] = "PASS audit · cream vignette KEEP · text in InDesign (Thank You + Draft)"
            p["status"] = "keep"
        if p["id"] == "p31":
            p["path"] = "Media/development/P-author/art.png"
            p["development_path"] = "Media/development/P-author/art.png"
            p["version"] = "style-match-B + v01-framed"
            p["notes"] = "LOCKED portrait + Pillow cream vignette 2625 · approved source untouched"
            p["status"] = "locked"
            p["caption"] = "p31 · Jack Farrell portrait · LOCKED + framed"
        if p["id"] == "p32":
            p["version"] = "v02-upscale-framed"
            p["model"] = "SeedVR + Pillow cream dissolve"
            p["status"] = "working"
            p["date"] = DAY
            p["notes"] = "Upscaled 1024→2625 · cream frame · InDesign: Merry Christmas. only (God bless on S12 R)"
            p["path"] = "Media/development/P-quiet-close/art-left.png"
            p["development_path"] = "Media/development/P-quiet-close/art-left.png"
            p["caption"] = "p32 · Quiet Close L · v02"
        if p["id"] == "p33":
            p["version"] = "v02-upscale-framed"
            p["model"] = "SeedVR + Pillow cream dissolve"
            p["status"] = "working"
            p["date"] = DAY
            p["notes"] = "Upscaled 1024→2625 · cream frame · InDesign: May the magic… line"
            p["path"] = "Media/development/P-quiet-close/art-right.png"
            p["development_path"] = "Media/development/P-quiet-close/art-right.png"
            p["caption"] = "p33 · Quiet Close R · v02"
    for d in root.get("verdicts", []):
        if d.get("page") in ("30", "31", "32", "33", "30|31", "32|33"):
            pass
    root["updated"] = DAY
    FLOW.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("AUDIT", json.dumps(audit, indent=2))
    print("DONE phase1 back matter")


if __name__ == "__main__":
    main()
