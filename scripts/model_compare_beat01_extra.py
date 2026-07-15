"""Append Ideogram V4 + Qwen Image 2 to Beat 1 model compare; lock dial/finals lanes."""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

import fal_client

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Media" / "generated" / "model-compare-beat01"
OUT.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "Christmas Eve night, a curious young boy with brown hair in soft patterned pajamas "
    "crouching and peeking from a dim hallway toward a glowing living room doorway, "
    "soft silhouette, Christmas tree and wrapped gifts faintly visible beyond the door, "
    "warm golden light from the room contrasting cool dark hallway, magical hush and anticipation, "
    "intimate heirloom storybook moment, leave soft quiet space in the lower left for later text overlay. "
    "Traditional children Christmas picture-book illustration, heavily painted heirloom gouache and soft watercolor, "
    "visible soft brushstrokes and gentle blended edges, NOT colored pencil NOT crayon, "
    "warm fireplace glow and cool moonlight, deep crimson and forest green, "
    "Charles Santore inspired Golden Age storybook, NOT photoreal, NOT CGI, no text, no letters, no watermark"
)
SEED = 42

JOBS = [
    (
        "06-ideogram-v4",
        "ideogram/v4",
        {
            "prompt": PROMPT,
            "image_size": "square_hd",
            "num_images": 1,
            "output_format": "png",
            "seed": SEED,
            "rendering_speed": "BALANCED",
            "expansion_model": "None",
        },
    ),
    (
        "07-qwen-image-2",
        "fal-ai/qwen-image-2/text-to-image",
        {
            "prompt": PROMPT,
            "image_size": "square_hd",
            "num_images": 1,
            "output_format": "png",
            "seed": SEED,
            "enable_prompt_expansion": False,
            "negative_prompt": (
                "photoreal, photo, CGI, 3D render, colored pencil, crayon, "
                "sketch, text, watermark, logo"
            ),
        },
    ),
]


def load_fal_key() -> None:
    env_path = ROOT / ".env.local"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k in ("FAL_KEY", "FAL_API_KEY") and v:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "tnims-compare/1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        dest.write_bytes(r.read())


def main() -> None:
    load_fal_key()
    if not os.environ.get("FAL_KEY"):
        raise SystemExit("FAL_KEY missing")

    manifest_path = OUT / "manifest.json"
    manifest = (
        json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest_path.exists()
        else {"results": []}
    )

    for name, endpoint, args in JOBS:
        print(f"GEN {name} -> {endpoint}", flush=True)
        try:
            result = fal_client.subscribe(endpoint, arguments=args)
            url = result["images"][0]["url"]
            dest = OUT / f"{name}.png"
            download(url, dest)
            entry = {
                "file": dest.name,
                "endpoint": endpoint,
                "url": url,
                "kb": dest.stat().st_size // 1024,
                "status": "ok",
            }
            print(f"  OK {dest.name} ({entry['kb']} KB)", flush=True)
        except Exception as e:
            entry = {
                "file": name,
                "endpoint": endpoint,
                "status": "fail",
                "error": str(e),
            }
            print(f"  FAIL {e}", flush=True)
        drop = {name, f"{name}.png"}
        manifest["results"] = [
            r for r in manifest.get("results", []) if r.get("file") not in drop
        ]
        manifest["results"].append(entry)

    manifest["lane_lock"] = {
        "dev_dial": "fal-ai/flux-2/klein/4b",
        "finals": "fal-ai/nano-banana-pro/edit + style refs",
        "locked_by": "Jon 2026-07-15",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    index = """# Model compare — Beat 1 (The Sneak)

Same prompt, same seed (42) where supported. Square book page scene.

## Lane lock (Jon 2026-07-15)

| Lane | Model | Use |
|------|-------|-----|
| **Dev / dial** | FLUX.2 [klein] 4B (`fal-ai/flux-2/klein/4b`) | Cheap iterates, layout/text zoning, vibe checks |
| **Finals** | Nano Banana Pro /edit + style refs | Approved pages after dial |

## Results

| # | File | Model | ~Cost |
|--:|------|-------|------|
| 1 | `01-flux-schnell.png` | FLUX.1 [schnell] | ~$0.003 |
| 2 | `02-flux2-klein-4b.png` | FLUX.2 [klein] 4B — **dev pick** | ~$0.009 |
| 3 | `03-flux2-klein-9b.png` | FLUX.2 [klein] 9B | ~$0.011 |
| 4 | `04-nano-banana-pro-1K.png` | Nano Banana Pro @ 1K (txt2img) | ~$0.15 |
| 5 | `05-nano-banana-EDIT-refs-production.png` | Banana /edit + refs — **finals path** | already paid |
| 6 | `06-ideogram-v4.png` | Ideogram V4 BALANCED | ~$0.01 |
| 7 | `07-qwen-image-2.png` | Qwen Image 2.0 | ~$0.035 |

Judge: painted gouache feel, child peek story match, quiet space for text, not photoreal/colored-pencil.
"""
    (OUT / "INDEX.md").write_text(index, encoding="utf-8")
    print(f"Done -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
