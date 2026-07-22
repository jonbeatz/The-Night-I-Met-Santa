from pathlib import Path
from urllib.request import urlretrieve
from PIL import Image

root = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
base = root / "Media/generated/mocks/_INDEX/text-page-lora"

samples = [
    {
        "dir": "v01",
        "url": "https://v3b.fal.media/files/b/0aa34e87/xZNbOfxym5mmfKCTeiVQS_wkgphsGE.png",
        "request_id": "019f8b2b-5018-7730-b1d0-5905ac3327c4",
        "seed": 573892410,
    },
    {
        "dir": "v02",
        "url": "https://v3b.fal.media/files/b/0aa34e8a/quKH-Q-YJk_UZ9D1rtCEU_DG3894kh.png",
        "request_id": "019f8b2b-bb1c-7f53-88c4-18b623054602",
        "seed": 42,
    },
]

lora_url = "https://v3b.fal.media/files/b/0aa34e8a/r8az-_smTtlyPagCKRA2q_pytorch_lora_weights.safetensors"
prompt = "Soft cream watercolor paper with subtle feathered edges, no illustrations, no text, warm ivory, gentle paper grain"

for s in samples:
    d = base / s["dir"]
    d.mkdir(parents=True, exist_ok=True)
    native = d / "art-2048.png"
    out = d / "art.png"
    urlretrieve(s["url"], native)
    im = Image.open(native).convert("RGB")
    print(f"{s['dir']} native={im.size}")
    # User asked 2625x2625 — native max is 2048; Lanczos upscale for layout test
    up = im.resize((2625, 2625), Image.Resampling.LANCZOS)
    up.save(out, "PNG")
    recipe = d / "RECIPE.md"
    recipe.write_text(
        f"""# Text-page LoRA paper — {s['dir']}

- **Endpoint:** `fal-ai/flux-2/lora`
- **LoRA:** `{lora_url}`
- **Scale:** 1.0
- **Prompt:** {prompt}
- **Seed:** {s['seed']}
- **Request ID:** `{s['request_id']}`
- **Native size:** 2048×2048 (endpoint max)
- **Saved for layout:** 2625×2625 Lanczos upscale → `art.png`
- **Native file:** `art-2048.png`
- **Style lock note:** style-lock-v2 used for hero tests; paper LoRA trained on styles2 paper refs (not style-lock image input — endpoint is loras-only)

""",
        encoding="utf-8",
    )
    print(f"saved {out} {out.stat().st_size}")

# Contact sheet of both + note meta
sheet_path = base / "lora-paper-v01-v02.png"
imgs = [Image.open(base / v / "art-2048.png").convert("RGB").resize((768, 768), Image.Resampling.LANCZOS) for v in ("v01", "v02")]
sheet = Image.new("RGB", (768 * 2 + 24, 768 + 48), (245, 240, 230))
sheet.paste(imgs[0], (12, 36))
sheet.paste(imgs[1], (780, 36))
sheet.save(sheet_path, "PNG")
print("sheet", sheet_path)

# Persist LoRA pointer
meta = base / "lora-weights.json"
meta.write_text(
    """{
  "trainer": "fal-ai/flux-2-trainer-v2",
  "train_request_id": "019f8b1b-d679-7370-a405-12d582a982db",
  "lora_weights": "https://v3b.fal.media/files/b/0aa34e8a/r8az-_smTtlyPagCKRA2q_pytorch_lora_weights.safetensors",
  "config": "https://v3b.fal.media/files/b/0aa34e7c/74BRnruSDbJmVdbByoYfY_config_63812592-4bf6-4f6c-8c5c-909c738c0ba2.json",
  "trigger_caption": "Soft cream watercolor paper with subtle feathered edges, no illustrations, no text, warm ivory, gentle paper grain",
  "train_refs": [
    "Images/styles2/spread-Frame-Style1.png",
    "Images/styles2/p21-beat12-13-note-LEFT.png"
  ],
  "inference": [
    {"id": "v01", "request_id": "019f8b2b-5018-7730-b1d0-5905ac3327c4", "seed": 573892410},
    {"id": "v02", "request_id": "019f8b2b-bb1c-7f53-88c4-18b623054602", "seed": 42}
  ]
}
""",
    encoding="utf-8",
)
print("meta ok")
