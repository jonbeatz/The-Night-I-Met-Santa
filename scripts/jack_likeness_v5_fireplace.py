"""v5: best faces (v3e/v4c/v4f) into fireplace chair scenes. Banana Pro /edit."""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

import fal_client

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Media" / "generated" / "jack-likeness"
JACK = ROOT / "Images" / "jack"


def load_key() -> None:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k in ("FAL_KEY", "FAL_API_KEY") and v:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "tnims-jack/5"})
    with urllib.request.urlopen(req, timeout=180) as r:
        dest.write_bytes(r.read())


def main() -> None:
    load_key()
    if not os.environ.get("FAL_KEY"):
        raise SystemExit("FAL_KEY missing")

    print("UPLOAD (Banana Pro /edit finals lane)...", flush=True)
    urls = {
        "v3e": fal_client.upload_file(str(OUT / "v3e-max-photo-weight.png")),
        "v4c": fal_client.upload_file(str(OUT / "v4c-from-v3c-clean.png")),
        "v4f": fal_client.upload_file(str(OUT / "v4f-v3c-blue-sweater.png")),
        "v3a": fal_client.upload_file(str(OUT / "v3a-face-lock-from-v2b.png")),
        "face5": fal_client.upload_file(str(JACK / "jackFace5.jpg")),
        "photo": fal_client.upload_file(str(JACK / "IMG_7537.jpg")),
    }
    print("ok", flush=True)

    face = (
        "CRITICAL face identity: preserve the winners face likeness from the attached portrait refs "
        "(same man as photos) — high forehead, wispy bright white swept-back hair, warm smile, "
        "kind eyes. Soft clean fair skin with gentle wrinkles ONLY. "
        "NO brown age spots, NO liver spots on face or hands."
    )
    style = (
        "Painted gouache soft watercolor heirloom Christmas picture-book illustration, "
        "soft brushwork, NOT photoreal, no text, no watermark"
    )
    no_desk = "NOT a writing desk scene, NO rolltop desk, NO office papers."

    jobs = [
        (
            "v5a-v3e-face-into-fireplace",
            [urls["v3e"], urls["v3a"], urls["photo"], urls["face5"]],
            f"Take THIS mans face from the Christmas-tree portrait and place him in a cozy "
            f"red leather wingback chair by a stone fireplace (like classic fireplace portraits), "
            f"snowy window optional, cream cable-knit sweater, open book on lap. {face} {no_desk} {style}",
        ),
        (
            "v5b-v4c-face-into-fireplace",
            [urls["v4c"], urls["v3a"], urls["photo"], urls["face5"]],
            f"Use THIS mans face (best likeness) in a warm fireplace armchair scene — burgundy "
            f"wingback, roaring fire with garland, cream sweater, gentle smile, evening Christmas glow. "
            f"{face} {no_desk} {style}",
        ),
        (
            "v5c-v4f-face-blue-sweater-fire",
            [urls["v4f"], urls["v3a"], urls["photo"]],
            f"Same man face from the blue-sweater portrait, seated by fireplace in dusty-blue "
            f"knit sweater (keep that clothing), red chair, stone hearth, Christmas stockings. "
            f"{face} {no_desk} {style}",
        ),
        (
            "v5d-alt-side-angle-fire",
            [urls["v3e"], urls["v4c"], urls["photo"], urls["face5"]],
            f"Three-quarter view of this exact man in a wingback by a roaring fireplace, "
            f"slightly different angle than straight-on — cozy, reading a book or mug nearby, "
            f"cream sweater. {face} {no_desk} {style}",
        ),
        (
            "v5e-alt-wide-room-fire",
            [urls["v4c"], urls["v3e"], urls["photo"]],
            f"Wider cozy living-room Christmas scene: this exact man smaller in frame, red chair "
            f"center-left, large stone fireplace right with stockings, Christmas tree edge visible, "
            f"snowy window. Face still clearly his likeness. Cream knit sweater. {face} {no_desk} {style}",
        ),
        (
            "v5f-alt-cardigan-fire",
            [urls["v3e"], urls["v4f"], urls["v3a"], urls["photo"]],
            f"Fireplace armchair portrait of this exact man in a soft burgundy cardigan, "
            f"warm firelight, classic storybook composition. {face} {no_desk} {style}",
        ),
    ]

    results = []
    for name, image_urls, prompt in jobs:
        print(f"GEN {name}", flush=True)
        try:
            result = fal_client.subscribe(
                "fal-ai/nano-banana-pro/edit",
                arguments={
                    "prompt": prompt,
                    "image_urls": image_urls,
                    "num_images": 1,
                    "aspect_ratio": "1:1",
                    "resolution": "2K",
                    "output_format": "png",
                    "limit_generations": True,
                },
            )
            url = result["images"][0]["url"]
            dest = OUT / f"{name}.png"
            download(url, dest)
            print(f"  OK {dest.name} ({dest.stat().st_size // 1024} KB)", flush=True)
            results.append(
                {
                    "file": dest.name,
                    "status": "ok",
                    "model": "fal-ai/nano-banana-pro/edit",
                }
            )
        except Exception as e:
            print(f"  FAIL {e}", flush=True)
            results.append({"file": name, "status": "fail", "error": str(e)})

    man_path = OUT / "manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else {"results": []}
    man.setdefault("results", []).extend(results)
    man["pass"] = "v5-fireplace-from-best-faces"
    man["model_note"] = "All jack-likeness gens use Banana Pro /edit (finals), not Klein 4B dial"
    man_path.write_text(json.dumps(man, indent=2), encoding="utf-8")

    index_path = OUT / "INDEX.md"
    extra = """
## Pass v5 — best faces into fireplace/chair (no desk)

**Model:** `fal-ai/nano-banana-pro/edit` @ 2K (finals lane — NOT Klein 4B).

Face donors: v3e, v4c, v4f → scenes like v3a fireplace.

| File | Notes |
|------|-------|
| `v5a-v3e-face-into-fireplace.png` | v3e face → classic fire chair |
| `v5b-v4c-face-into-fireplace.png` | v4c face → fire chair |
| `v5c-v4f-face-blue-sweater-fire.png` | v4f face + blue sweater + fire |
| `v5d-alt-side-angle-fire.png` | Side/three-quarter fire |
| `v5e-alt-wide-room-fire.png` | Wider room with tree edge |
| `v5f-alt-cardigan-fire.png` | Burgundy cardigan + fire |
"""
    prev = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    index_path.write_text(prev + extra, encoding="utf-8")
    print("Done", flush=True)


if __name__ == "__main__":
    main()
