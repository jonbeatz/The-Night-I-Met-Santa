"""Stamp flow-pass RECIPE verdicts + run S7/S8 Lane B wardrobe finals."""
from __future__ import annotations

import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
MOCKS = ROOT / "Media" / "generated" / "mocks"
APPROVED = ROOT / "Media" / "approved"

VERDICTS = {
    "S01-approach/v01": ("keep", "Flow pass keep 2026-07-21"),
    "S02-threshold/v01": ("reject", "Flow pass reject — wardrobe/composition miss; superseded by v02"),
    "S02-threshold/v02": ("keep", "Flow pass keep (backup) 2026-07-21 — holly PJs OK; Santa fuller than half-seen (finals may deepen shadow)"),
    "S04-sit-here/v01": ("keep", "Flow pass keep 2026-07-21"),
    "S05-chat/v01": ("reject", "Flow pass reject — twin Santa; superseded by v02"),
    "S05-chat/v02": ("keep", "Flow pass keep (backup) 2026-07-21 — one Santa + holly PJs"),
    "S06-cocoa/v01": ("keep", "Flow pass keep 2026-07-21"),
    "S07-proof/v01": ("keep-leaning", "Composition keep — wardrobe drift (red coat). Fix on Lane B finals with G0 holly PJs"),
    "S08-gone/v01": ("keep-leaning", "Composition keep — wardrobe drift (red coat). Fix on Lane B finals with G0 holly PJs"),
    "S09-search/v01": ("keep", "Flow pass keep 2026-07-21"),
    "S10-note/v01": ("keep", "Flow pass keep 2026-07-21"),
    "S11-wish/v01": ("reject", "Flow pass reject — baked letters on note; superseded by v02"),
    "S11-wish/v02": ("keep", "Flow pass keep (backup) 2026-07-21 — blank note + holly PJs"),
    "S12-blessing/v01": ("keep", "Flow pass keep 2026-07-21"),
    "P02-copyright/v01": ("keep", "Flow pass keep 2026-07-21 — FRAME ON matter"),
    "P03-dedication/v01": ("keep", "Flow pass keep 2026-07-21 — FRAME ON matter"),
    "P05-about-vignette/v01": ("keep", "Flow pass keep 2026-07-21 — FRAME ON matter"),
    "P32-quiet-close/v01": ("keep", "Flow pass keep 2026-07-21 — FRAME ON matter"),
    "P33-merry-christmas/v01": ("keep", "Flow pass keep 2026-07-21 — FRAME ON matter"),
}

MASTER = (
    "Traditional children's Christmas picture-book illustration, heirloom storybook quality, "
    "heavily painted in rich gouache and soft watercolor with visible soft brushstrokes and gentle blended edges, "
    "NOT colored pencil NOT crayon NOT scratchy sketch lines, warm fireplace glow mixed with cool moonlight, "
    "golden ember highlights, deep crimson and forest green palette with warm cream and muted earth tones, "
    "nostalgic Golden Age painted realism, intimate cozy magical atmosphere, Charles Santore–inspired storybook painting, "
    "classic Clement C. Moore Christmas book feel, highly detailed but soft and painterly, print-ready composition, "
    "no text, no letters, no watermark"
)

SPREAD = (
    "ONE continuous unbroken painted scene across the full width — same room, same moment, same lighting, "
    "like one wide painting with a fold in the middle, NOT two separate images. Seamless through the center: "
    "NO fake book gutter, NO vertical fold line, NO center spine shadow. Keep faces and critical props AWAY "
    "from the exact center fold — center band is background only. WATERCOLOR FRAME OFF: full-bleed to all edges."
)

PJ = (
    "Child wears oatmeal/taupe holly pajamas ONLY — NOT a red coat, NOT a Santa suit, NOT a Santa costume. "
    "Match the boy character reference: oatmeal/taupe pajamas with green holly leaves and red berries."
)

HARD_NEG = (
    "NO readable letters, NO text, NO handwriting, NO watermark, NO logos, NO phone UI, "
    "NO second Santa, NO child in red coat or Santa costume."
)


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
    # fal_client looks for FAL_KEY
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def stamp_verdicts() -> None:
    for rel, (verdict, note) in VERDICTS.items():
        path = MOCKS / rel / "RECIPE.md"
        if not path.exists():
            print(f"MISSING RECIPE: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        text2 = re.sub(
            r"(\|\s*\*\*verdict\*\*\s*\|\s*)([^|\n]+)(\s*\|)",
            rf"\1**{verdict}**\3",
            text,
            count=1,
        )
        # Append note if Notes section exists
        if "## Notes" in text2:
            if note not in text2:
                text2 = text2.rstrip() + f"\n\n- Verdict stamp: {note}\n"
        else:
            text2 = text2.rstrip() + f"\n\n## Notes\n\n- Verdict stamp: {note}\n"
        path.write_text(text2, encoding="utf-8")
        print(f"stamped {rel} -> {verdict}")


def write_s3_sidecar() -> None:
    path = APPROVED / "spreads" / "spread-eyes-met.recipe.md"
    path.write_text(
        """# spread-eyes-met.recipe.md

| Field | Value |
|-------|--------|
| **name** | Eyes met / splendor |
| **approved_file** | `Media/approved/spreads/spread-eyes-met.png` |
| **unit** | S03-eyes-met |
| **book page** | 10\\|11 · S3 · SPREAD |
| **page role** | `spread` |
| **spread side** | `wide-master` |
| **version** | locked (pre-flow) |
| **date** | 2026-07-15 (lock) · noted in flow pass 2026-07-21 |
| **lane** | B finals (earlier generation — not Klein dial) |
| **service** | fal.ai / prior pipeline |
| **model** | *(see style-refs / eyes-met history — do not regenerate)* |
| **FRAME** | OFF |
| **concept** | Child and Santa eyes lock — emotional centerpiece |
| **size** | 2752×1536 (dial/lock px — print remake → 5250×2625 later) |
| **verdict** | **locked** |
| **status** | **locked** |
| **promoted_to** | *(this file)* |

## Prompt

*(Locked plate — do not regenerate. Full beat prompt lives in MASTER-PRODUCTION-DOCK S3.)*

## Notes

- Flow pass 2026-07-21: only locked story art in the Klein dial set; style jump vs dials is expected and OK.
- Print remake on Lane B later if needed for exact Lulu px — composition lock stands.
""",
        encoding="utf-8",
    )
    print(f"wrote {path}")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "TNIMS-flow-finals/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())


def write_final_recipe(
    unit: str,
    ver: str,
    name: str,
    pages: str,
    script: str,
    zone: str,
    prompt: str,
    refs: list[str],
    base: str,
    notes: str,
) -> None:
    path = MOCKS / unit / ver / "RECIPE.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    ref_lines = "\n".join(f"- `{r}`" for r in refs)
    path.write_text(
        f"""# RECIPE — {unit} / {ver}

| Field | Value |
|-------|--------|
| **name** | {name} |
| **unit** | {unit} |
| **book page** | {pages} |
| **page role** | `spread` |
| **spread side** | `wide-master` |
| **version** | {ver} |
| **date** | 2026-07-21 |
| **lane** | B finals (Gemini edit) |
| **service** | fal.ai |
| **model** | `fal-ai/gemini-3-pro-image-preview/edit` |
| **settings** | resolution 2K · aspect 21:9 · FRAME OFF · wardrobe fix from dial keep-leaning |
| **FRAME** | OFF |
| **concept** | Keep dial composition · fix child to oatmeal holly PJs (G0) |
| **changes** | vs dial v01: remove red coat / Santa costume on child; lock holly PJs |
| **size** | 2K wide (print remake → 5250×2625 later if needed) |
| **seed** | n/a |
| **request_id** | n/a |
| **cost_note** | ~$0.14–0.15 Lane B |
| **output** | art.png |
| **script_text** | {script} |
| **type_zone** | {zone} |
| **verdict** | pending |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used

{ref_lines}
- base / edit source: `{base}`

## Prompt

{prompt}

## Negative / constraints

- {HARD_NEG}
- {PJ}
- FRAME OFF · continuous spread · faces off center fold

## Notes

{notes}
""",
        encoding="utf-8",
    )


def run_wardrobe_finals() -> None:
    import fal_client

    boy = APPROVED / "characters" / "boy-narrator-G0.png"
    santa = APPROVED / "characters" / "santa-G0.png"
    cover = APPROVED / "covers" / "cover-front.png"
    style = APPROVED / "spreads" / "spread-eyes-met.png"

    print("Uploading refs...")
    urls = {
        "boy": fal_client.upload_file(str(boy)),
        "santa": fal_client.upload_file(str(santa)),
        "cover": fal_client.upload_file(str(cover)),
        "style": fal_client.upload_file(str(style)),
    }

    jobs = [
        {
            "unit": "S07-proof",
            "ver": "v02",
            "name": "Proof — Lane B wardrobe fix (holly PJs)",
            "pages": "18|19 · S7 · SPREAD",
            "script": "L: roof noise / needed proof · R: photo best bet",
            "zone": "Bottom left · bottom right",
            "base": MOCKS / "S07-proof" / "v01" / "art.png",
            "scene": (
                "Reimagine this Christmas storybook SPREAD while KEEPING the same composition and camera: "
                "child looking sharply upward toward the ceiling hearing reindeer noise on the roof, "
                "playful urgency; a simple classic camera nearby as the idea for proof "
                "(era-neutral camera body, NOT a modern phone UI). Warm interior, Christmas tree glow. "
                "CRITICAL WARDROBE FIX: the child must wear oatmeal/taupe holly pajamas ONLY — "
                "remove any red coat, Santa suit, or Santa costume on the child. "
                "Santa may be partly visible or already shifting away. Quiet bottom bands for later text."
            ),
            "notes": "Lane B after flow-pass keep-leaning on v01. Composition preserved; wardrobe → G0 holly PJs.",
        },
        {
            "unit": "S08-gone",
            "ver": "v02",
            "name": "Gone — Lane B wardrobe fix (holly PJs)",
            "pages": "20|21 · S8 · SPREAD",
            "script": "L: empty Santa spot · R: child returns with camera",
            "zone": "Upper left · upper right",
            "base": MOCKS / "S08-gone" / "v01" / "art.png",
            "scene": (
                "Reimagine this Christmas storybook SPREAD while KEEPING the same composition and camera: "
                "empty spot among gifts where Santa sat, wrapping paper still, tree glowing; "
                "child rushing back holding a camera, disappointment and urgency, door ajar, "
                "suggestion of roof noise by upward glance. No Santa figure present. "
                "CRITICAL WARDROBE FIX: the child must wear oatmeal/taupe holly pajamas ONLY — "
                "remove any red coat, Santa suit, or Santa costume on the child. "
                "Quiet upper areas for later text."
            ),
            "notes": "Lane B after flow-pass keep-leaning on v01. Composition preserved; wardrobe → G0 holly PJs.",
        },
    ]

    for job in jobs:
        base = job["base"]
        print(f"\n=== {job['unit']} {job['ver']} ===")
        base_url = fal_client.upload_file(str(base))
        prompt = f"{job['scene']} {PJ} {MASTER} {SPREAD} {HARD_NEG}"
        result = fal_client.subscribe(
            "fal-ai/gemini-3-pro-image-preview/edit",
            arguments={
                "prompt": prompt,
                "image_urls": [base_url, urls["boy"], urls["cover"], urls["style"], urls["santa"]],
                "resolution": "2K",
                "aspect_ratio": "21:9",
                "output_format": "png",
                "num_images": 1,
                "limit_generations": True,
                "safety_tolerance": "4",
            },
        )
        out_url = result["images"][0]["url"]
        out = MOCKS / job["unit"] / job["ver"] / "art.png"
        download(out_url, out)
        print(f"Saved {out}")
        write_final_recipe(
            unit=job["unit"],
            ver=job["ver"],
            name=job["name"],
            pages=job["pages"],
            script=job["script"],
            zone=job["zone"],
            prompt=prompt,
            refs=[
                "Media/approved/characters/boy-narrator-G0.png",
                "Media/approved/characters/santa-G0.png",
                "Media/approved/covers/cover-front.png",
                "Media/approved/spreads/spread-eyes-met.png",
                str(base.relative_to(ROOT)).replace("\\", "/"),
            ],
            base=str(base.relative_to(ROOT)).replace("\\", "/"),
            notes=job["notes"],
        )


def main() -> None:
    load_env()
    print("=== Stamp verdicts ===")
    stamp_verdicts()
    print("\n=== S3 sidecar ===")
    write_s3_sidecar()
    print("\n=== S7/S8 Lane B wardrobe finals ===")
    run_wardrobe_finals()
    print("\nDONE")


if __name__ == "__main__":
    main()
