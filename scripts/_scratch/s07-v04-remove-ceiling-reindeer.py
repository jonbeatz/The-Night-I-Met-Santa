"""S7 v04 — Klein 9B /edit: remove ceiling reindeer from v03, keep look-up + holly PJs."""
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

    base = ROOT / "Media/generated/mocks/S07-proof/v03/art.png"
    out = ROOT / "Media/generated/mocks/S07-proof/v04/art.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    base_url = fal_client.upload_file(str(base))

    d2 = (
        "KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast, "
        "rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous "
        "but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare. "
        "Soft blended edges. NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated."
    )
    prompt = (
        "Edit this Christmas storybook spread carefully. KEEP the exact same composition, camera, lighting, "
        "and the child's look-up pose (gazing upward in awe toward the ceiling / roof). "
        "KEEP the child in oatmeal/taupe holly pajamas ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume. "
        "KEEP the camera on the floor, tree, gifts, doorway, sofa, stockings. "
        "CRITICAL FIX: REMOVE all reindeer that are popping through the ceiling, bursting from walls, "
        "or mounted oddly near the ceiling. No reindeer bodies breaking through the roof or ceiling. "
        "No flying reindeer inside the room. Replace that ceiling area with normal cozy ceiling / soft "
        "shadow / quiet upper wall — the child is reacting to SOUND from the roof above, not seeing "
        "reindeer crash into the room. Implied roof noise only. FRAME OFF full bleed. No readable text. "
        + d2
    )

    print("Calling fal-ai/flux-2/klein/9b/edit (remove ceiling reindeer)...")
    result = fal_client.subscribe(
        "fal-ai/flux-2/klein/9b/edit",
        arguments={
            "prompt": prompt,
            "image_urls": [base_url],
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

    (out.parent / "RECIPE.md").write_text(
        f"""# RECIPE — S07-proof / v04

| Field | Value |
|-------|--------|
| **name** | Proof — remove ceiling reindeer (keep v03 look-up + holly PJs) |
| **unit** | S07-proof |
| **book page** | 18|19 · S7 · SPREAD |
| **page role** | `spread` |
| **spread side** | `wide-master` |
| **version** | v04 |
| **date** | 2026-07-21 |
| **lane** | A1 dial edit (Klein 9B /edit) |
| **service** | fal.ai |
| **model** | `fal-ai/flux-2/klein/9b/edit` |
| **settings** | 1536x768 · edit from v03 |
| **FRAME** | OFF |
| **concept** | Same look-up beat · roof noise implied · no reindeer through ceiling |
| **changes** | vs v03: remove reindeer popping through ceiling/walls; quiet upper ceiling/wall |
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

- base / edit source: `Media/generated/mocks/S07-proof/v03/art.png`

## Prompt

{prompt}

## Notes

- Jon 2026-07-21: v03 art good but reindeer popping through ceiling — targeted fix.
""",
        encoding="utf-8",
    )
    print("RECIPE written")


if __name__ == "__main__":
    main()
