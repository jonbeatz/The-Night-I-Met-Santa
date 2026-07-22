"""S7 v03 — Klein 9B /edit from v01 composition, holly PJs only."""
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

    base = ROOT / "Media/generated/mocks/S07-proof/v01/art.png"
    boy = ROOT / "Media/approved/characters/boy-narrator-G0.png"
    out = ROOT / "Media/generated/mocks/S07-proof/v03/art.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    base_url = fal_client.upload_file(str(base))
    boy_url = fal_client.upload_file(str(boy))

    d2 = (
        "KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast, "
        "rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous "
        "but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare. "
        "Clean Santa coat — NO letters, NO glyphs on clothing. Soft blended edges. "
        "NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated."
    )
    prompt = (
        "Edit this Christmas storybook spread carefully. KEEP the exact same composition, camera, "
        "and look-up pose: child on the right looking sharply upward toward the ceiling with awe "
        "(roof noise beat), camera on the floor in the foreground, Christmas tree and gifts on the left, "
        "dark doorway, warm room. ONLY change the child wardrobe: child wears oatmeal/taupe holly pajamas "
        "ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume, NOT a Santa hat. Match the boy "
        "reference pajamas (oatmeal/taupe with green holly leaves and red berries). Keep FRAME OFF full bleed. "
        "No readable text. No letters. " + d2
    )

    print("Calling fal-ai/flux-2/klein/9b/edit...")
    result = fal_client.subscribe(
        "fal-ai/flux-2/klein/9b/edit",
        arguments={
            "prompt": prompt,
            "image_urls": [base_url, boy_url],
            "image_size": {"width": 1536, "height": 768},
            "output_format": "png",
            "num_images": 1,
        },
    )
    url = result["images"][0]["url"]
    req = urllib.request.Request(url, headers={"User-Agent": "TNIMS/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        out.write_bytes(resp.read())
    print(f"Saved {out} ({out.stat().st_size} bytes)")

    recipe = out.parent / "RECIPE.md"
    recipe.write_text(
        f"""# RECIPE — S07-proof / v03

| Field | Value |
|-------|--------|
| **name** | Proof — Klein edit wardrobe fix (keep v01 look-up) |
| **unit** | S07-proof |
| **book page** | 18|19 · S7 · SPREAD |
| **page role** | `spread` |
| **spread side** | `wide-master` |
| **version** | v03 |
| **date** | 2026-07-21 |
| **lane** | A1 dial edit (Klein 9B /edit) |
| **service** | fal.ai |
| **model** | `fal-ai/flux-2/klein/9b/edit` |
| **settings** | 1536x768 · edit from v01 composition · boy G0 PJ ref |
| **FRAME** | OFF |
| **concept** | Keep v01 look-up composition · fix clothes to oatmeal holly PJs |
| **changes** | vs v01: red coat/Santa hat → holly PJs only. vs v02: restore v01 pose (v02 composition drift) |
| **size** | 1536x768 |
| **seed** | n/a |
| **request_id** | n/a |
| **cost_note** | ~$0.01 dial edit |
| **output** | art.png |
| **script_text** | L: roof noise / needed proof · R: photo best bet |
| **type_zone** | Bottom left · bottom right |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

- boy: `Media/approved/characters/boy-narrator-G0.png`
- base / edit source: `Media/generated/mocks/S07-proof/v01/art.png`

## Prompt

{prompt}

## Notes

- Last Klein dial for flow pass. Stop Klein dials after this; prepare InDesign.
""",
        encoding="utf-8",
    )
    print("RECIPE written")


if __name__ == "__main__":
    main()
