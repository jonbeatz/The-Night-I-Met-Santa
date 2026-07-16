"""v6 final: faces ONLY from Jon favorites v4a/v4c/v4f. New scenes. Banana /edit."""
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
    req = urllib.request.Request(url, headers={"User-Agent": "tnims-jack/6"})
    with urllib.request.urlopen(req, timeout=180) as r:
        dest.write_bytes(r.read())


def main() -> None:
    load_key()
    if not os.environ.get("FAL_KEY"):
        raise SystemExit("FAL_KEY missing")

    print("UPLOAD face donors (Jon favorites) first...", flush=True)
    # Order matters: face winners FIRST so model locks identity from them
    urls = {
        "v4a": fal_client.upload_file(str(OUT / "v4a-from-v3e-clean.png")),
        "v4c": fal_client.upload_file(str(OUT / "v4c-from-v3c-clean.png")),
        "v4f": fal_client.upload_file(str(OUT / "v4f-v3c-blue-sweater.png")),
        "photo": fal_client.upload_file(str(JACK / "IMG_7537.jpg")),
        "face5": fal_client.upload_file(str(JACK / "jackFace5.jpg")),
        "face4": fal_client.upload_file(str(JACK / "jackFace4.jpg")),
    }
    print("ok", flush=True)

    # Lead with painted favorites + real photos — NO old generic fireplace plate
    face_stack = [
        urls["v4f"],
        urls["v4c"],
        urls["v4a"],
        urls["photo"],
        urls["face5"],
        urls["face4"],
    ]

    face = (
        "FACE LOCK: the man MUST look like the same person as the FIRST three attached "
        "illustrations (Jon favorites) and the real photos — that specific face identity. "
        "High forehead, wispy bright white swept-back hair, warm open smile, kind eyes, "
        "soft clean fair skin. NO brown age spots on face or hands. "
        "Do NOT use a generic silver-haired grandpa face. Do NOT revert to a different man's face."
    )
    style = (
        "Painted gouache soft watercolor heirloom Christmas children's picture-book, "
        "soft brushwork, NOT photoreal, no text, no watermark"
    )

    jobs = [
        (
            "v6a-closeup-likeness",
            face_stack,
            f"Tight CLOSE-UP portrait (shoulders up) of this exact man on Christmas Eve — "
            f"warm indoor firelight on his face, soft bokeh tree lights behind, cream or soft "
            f"blue knit sweater collar visible. Face fills most of the frame so likeness is clear. "
            f"{face} {style}",
        ),
        (
            "v6b-fireplace-chair-new",
            face_stack,
            f"NEW composition: this exact man in a deep red wingback chair angled three-quarter, "
            f"stone fireplace blazing to one side, Christmas stockings, snowy window. "
            f"Cream cable sweater. Different pose/camera than prior plates. {face} {style}",
        ),
        (
            "v6c-santa-hat",
            face_stack,
            f"This exact man wearing a classic soft red Santa hat with white fur trim and pom-pom, "
            f"warm Christmas living room with fireplace glow behind him, friendly smile looking "
            f"at viewer, cream or burgundy knit sweater. Playful heirloom storybook portrait. "
            f"{face} {style}",
        ),
        (
            "v6d-armchair-tree-lights",
            face_stack,
            f"NEW scene: this exact man seated in a cozy armchair beside a glowing Christmas tree "
            f"(warm fairy lights, soft ornaments), mug of cocoa on a small table, evening light. "
            f"Soft blue or cream sweater. Intimate storybook mood. {face} {style}",
        ),
        (
            "v6e-window-snow-portrait",
            face_stack,
            f"NEW scene: this exact man standing or half-seated by a large frost-kissed window "
            f"showing falling snow and village lights, warm lamp glow on his face, festive "
            f"scarlet cardigan. Quiet Christmas Eve wonder. {face} {style}",
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
                    "face_donors": ["v4f", "v4c", "v4a", "IMG_7537", "jackFace5", "jackFace4"],
                }
            )
        except Exception as e:
            print(f"  FAIL {e}", flush=True)
            results.append({"file": name, "status": "fail", "error": str(e)})

    man_path = OUT / "manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else {"results": []}
    man.setdefault("results", []).extend(results)
    man["pass"] = "v6-final-favorite-faces"
    man_path.write_text(json.dumps(man, indent=2), encoding="utf-8")

    index_path = OUT / "INDEX.md"
    extra = """
## Pass v6 — FINAL (favorite faces only → new scenes)

**Face donors (in prompt order):** `v4f`, `v4c`, `v4a` + real photos.  
**Model:** Banana Pro `/edit` @ 2K. No old generic fireplace base plate.

| File | Notes |
|------|-------|
| `v6a-closeup-likeness.png` | Close-up / shoulders-up |
| `v6b-fireplace-chair-new.png` | New fireplace chair angle |
| `v6c-santa-hat.png` | Santa hat version |
| `v6d-armchair-tree-lights.png` | Tree + cocoa armchair |
| `v6e-window-snow-portrait.png` | Window snow / cardigan |
"""
    prev = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    index_path.write_text(prev + extra, encoding="utf-8")
    print("Done ->", OUT, flush=True)


if __name__ == "__main__":
    main()
