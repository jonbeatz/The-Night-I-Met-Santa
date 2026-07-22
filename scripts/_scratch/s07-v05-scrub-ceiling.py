"""S7 v05 — Gemini edit: scrub ceiling reindeer; keep v03/v04 look-up + holly PJs."""
from __future__ import annotations

import os
import urllib.request
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")


def load_env() -> None:
    env = ROOT / ".env.local"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def main() -> None:
    load_env()
    import fal_client

    # Prefer v03 (cleaner than v04 half-fix) as base; scrub ceiling hard
    base = ROOT / "Media/generated/mocks/S07-proof/v03/art.png"
    out = ROOT / "Media/generated/mocks/S07-proof/v05/art.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    base_url = fal_client.upload_file(str(base))

    master = (
        "Traditional children's Christmas picture-book illustration, heirloom storybook quality, "
        "heavily painted in rich gouache and soft watercolor, NOT colored pencil, warm fireplace and tree glow, "
        "Charles Santore–inspired, no text, no letters, no watermark"
    )
    prompt = (
        "Surgical edit of this Christmas storybook spread. "
        "KEEP almost everything identical: same wide composition, same child on the right looking sharply UP "
        "toward the ceiling in awe, same oatmeal/taupe holly pajamas, same camera and small card on the floor, "
        "same Christmas tree, gifts, green sofa, doorway, stockings, bookshelf, lighting. "
        "ONLY FIX THE CEILING / UPPER CENTER: completely REMOVE every reindeer, deer, antler, hoof, leg, "
        "or animal silhouette that is popping through, bursting from, or floating under the ceiling. "
        "Replace with a normal cozy ceiling and soft warm light wash — empty quiet upper wall/ceiling only. "
        "The child hears reindeer ON THE ROOF outside (implied sound), they must NOT appear inside the room "
        "or through the ceiling. No mounted deer heads. No magical animals breaking architecture. "
        "WATERCOLOR FRAME OFF full bleed. " + master
    )

    print("Calling gemini-3-pro-image-preview/edit (scrub ceiling)...")
    result = fal_client.subscribe(
        "fal-ai/gemini-3-pro-image-preview/edit",
        arguments={
            "prompt": prompt,
            "image_urls": [base_url],
            "resolution": "2K",
            "aspect_ratio": "21:9",
            "output_format": "png",
            "num_images": 1,
            "limit_generations": True,
            "safety_tolerance": "4",
        },
    )
    url = result["images"][0]["url"]
    req = urllib.request.Request(url, headers={"User-Agent": "TNIMS/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        out.write_bytes(resp.read())
    print(f"Saved {out} ({out.stat().st_size} bytes)")

    (out.parent / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v05

| Field | Value |
|-------|--------|
| **name** | Proof — scrub ceiling reindeer (surgical) |
| **unit** | S07-proof |
| **book page** | 18|19 · S7 · SPREAD |
| **page role** | `spread` |
| **spread side** | `wide-master` |
| **version** | v05 |
| **date** | 2026-07-21 |
| **lane** | B finals edit (Gemini) |
| **service** | fal.ai |
| **model** | `fal-ai/gemini-3-pro-image-preview/edit` |
| **settings** | 2K · 21:9 · surgical ceiling scrub from v03 |
| **FRAME** | OFF |
| **concept** | Keep look-up + holly PJs · roof noise implied · clean ceiling |
| **changes** | vs v03/v04: remove all reindeer popping through ceiling |
| **size** | 2K wide |
| **seed** | n/a |
| **request_id** | n/a |
| **cost_note** | ~$0.14–0.15 Lane B |
| **output** | art.png |
| **script_text** | L: roof noise / needed proof · R: photo best bet |
| **type_zone** | Bottom left · bottom right |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- base / edit source: `Media/generated/mocks/S07-proof/v03/art.png`

## Prompt

{prompt}

## Notes

- Jon: v03 good but reindeer through ceiling. Klein v04 still left ghosts — Gemini surgical scrub.
""",
        encoding="utf-8",
    )
    print("RECIPE written")


if __name__ == "__main__":
    main()
