#!/usr/bin/env python3
# JonBeatz — Hugging Face FLUX.1-schnell image generation (zero local VRAM)
# Usage: python scripts/generate-image.py --prompt "..." [--output path] [--width N] [--height N]

import os
import sys
import json
import argparse
from pathlib import Path


def expand_env(value: str) -> str:
    return os.path.expandvars(os.path.expanduser(value))


def load_env_local(project_root: Path) -> None:
    env_path = project_root / ".env.local"
    if not env_path.exists():
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = expand_env(val.strip().strip('"').strip("'"))
            if key and key not in os.environ:
                os.environ[key] = val


def get_hf_token(project_root: Path) -> str | None:
    if os.environ.get("HF_TOKEN", "").strip():
        return os.environ["HF_TOKEN"].strip()
    env_local_path = project_root / ".env.local"
    if env_local_path.exists():
        with open(env_local_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("HF_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip('"').strip("'")
                    return token or None
    return None


def default_output_dir(project_root: Path) -> Path:
    raw = os.environ.get("IMAGE_OUTPUT_DIR", "").strip()
    if raw:
        return Path(expand_env(raw))
    # Canonical Hermes media vault: D:\Hermes\assets\media\{projectName}
    project_name = project_root.name or "JonBeatz"
    return Path(r"D:\Hermes\assets\media") / project_name


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate images via Hugging Face Inference API")
    parser.add_argument("--prompt", required=True, type=str, help="Image prompt")
    parser.add_argument("--model", type=str, default="", help="HF model id")
    parser.add_argument("--output", type=str, default="", help="Output PNG path")
    parser.add_argument("--width", type=int, default=0, help="Width (default from env or 1024)")
    parser.add_argument("--height", type=int, default=0, help="Height (default from env or 1024)")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    load_env_local(project_root)

    hf_token = get_hf_token(project_root)
    if not hf_token or hf_token.startswith("hf_your"):
        print(json.dumps({
            "success": False,
            "error": "HF_TOKEN not configured. Run: npm run env:setup — then set HF_TOKEN in .env.local"
        }))
        return 1

    model = args.model or os.environ.get("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")
    width = args.width or int(os.environ.get("IMAGE_DEFAULT_WIDTH", "1024"))
    height = args.height or int(os.environ.get("IMAGE_DEFAULT_HEIGHT", "1024"))

    if args.output:
        output_path = Path(expand_env(args.output)).resolve()
    else:
        import datetime
        media_dir = default_output_dir(project_root)
        media_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = (media_dir / f"generated-{ts}.png").resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from huggingface_hub import InferenceClient

        client = InferenceClient(api_key=hf_token)
        image = client.text_to_image(
            prompt=args.prompt,
            model=model,
            width=width,
            height=height,
        )
        image.save(str(output_path), "PNG")

        print(json.dumps({
            "success": True,
            "file_path": str(output_path),
            "prompt": args.prompt,
            "model": model,
            "width": width,
            "height": height,
        }))
        return 0

    except ImportError:
        print(json.dumps({
            "success": False,
            "error": "Missing packages. Run: pip install huggingface_hub pillow python-dotenv"
        }))
        return 1
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
