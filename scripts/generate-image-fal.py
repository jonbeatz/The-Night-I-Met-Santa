#!/usr/bin/env python3
# JonBeatz — fal.ai pay-per-use image generation (bonus pipeline)
# Usage: python scripts/generate-image-fal.py --prompt "..." [--model fal-ai/flux/schnell]

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
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


def get_fal_key(project_root: Path) -> str | None:
    for name in ("FAL_API_KEY", "FAL_KEY"):
        val = os.environ.get(name, "").strip()
        if val:
            return val
    env_path = project_root / ".env.local"
    if not env_path.exists():
        return None
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            for prefix in ("FAL_API_KEY=", "FAL_KEY="):
                if line.startswith(prefix):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val and not val.lower().startswith("your_"):
                        return val
    return None


def default_output_dir(project_root: Path) -> Path:
    project_name = project_root.name or "JonBeatz"
    custom = os.environ.get("IMAGE_OUTPUT_DIR", "").strip()
    if custom:
        return Path(expand_env(custom)).resolve()
    return Path(r"D:\Hermes\assets\media") / project_name


def download_file(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "JonBeatz-fal-gen/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate images via fal.ai API")
    parser.add_argument("--prompt", required=True, type=str)
    parser.add_argument("--model", type=str, default="")
    parser.add_argument("--output", type=str, default="")
    parser.add_argument("--width", type=int, default=0)
    parser.add_argument("--height", type=int, default=0)
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    load_env_local(project_root)

    fal_key = get_fal_key(project_root)
    if not fal_key:
        print(json.dumps({
            "success": False,
            "error": "FAL_API_KEY not configured. Add key from fal.ai dashboard to .env.local"
        }))
        return 1

    model = args.model or os.environ.get("FAL_IMAGE_MODEL", "fal-ai/flux/schnell")
    width = args.width or int(os.environ.get("IMAGE_DEFAULT_WIDTH", "1024"))
    height = args.height or int(os.environ.get("IMAGE_DEFAULT_HEIGHT", "1024"))

    if args.output:
        output_path = Path(expand_env(args.output)).resolve()
    else:
        import datetime
        media_dir = default_output_dir(project_root)
        media_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = (media_dir / f"fal-{ts}.png").resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    endpoint = model if model.startswith("http") else f"https://fal.run/{model.lstrip('/')}"
    payload: dict = {"prompt": args.prompt}
    if width > 0 and height > 0:
        payload["image_size"] = {"width": width, "height": height}

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Key {fal_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"success": False, "error": f"fal HTTP {e.code}: {detail}"}))
        return 1
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        return 1

    images = result.get("images") or []
    if not images:
        print(json.dumps({"success": False, "error": f"No images in fal response: {result}"}))
        return 1

    image_url = images[0].get("url")
    if not image_url:
        print(json.dumps({"success": False, "error": f"Missing image url: {images[0]}"}))
        return 1

    try:
        download_file(image_url, output_path)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Download failed: {e}"}))
        return 1

    print(json.dumps({
        "success": True,
        "file_path": str(output_path),
        "prompt": args.prompt,
        "model": model,
        "width": width,
        "height": height,
        "provider": "fal.ai",
        "source_url": image_url,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
