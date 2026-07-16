#!/usr/bin/env python3
"""Generate / edit images via OpenRouter Image API (/api/v1/images).

Examples:
  python scripts/generate-image-openrouter.py --prompt "blue heron"
  python scripts/generate-image-openrouter.py --prompt "..." --ref Media/approved/covers/cover-front.png
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "google/gemini-3-pro-image"


def load_key() -> str:
    env_path = ROOT / ".env.local"
    if not env_path.exists():
        raise SystemExit(f"Missing {env_path}")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("OPENROUTER_API_KEY=") and not line.strip().startswith("#"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("OPENROUTER_API_KEY not set in .env.local")


def file_to_data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def call_images(payload: dict, key: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/images",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/jonbeatz/the-night-i-met-santa",
            "X-Title": "The-Night-I-Met-Santa",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenRouter HTTP {e.code}: {err_body[:2000]}") from e


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--ref", action="append", default=[], help="Reference image path (repeatable)")
    ap.add_argument("--resolution", default="1K", help="512 | 1K | 2K | 4K")
    ap.add_argument("--aspect-ratio", default="1:1")
    ap.add_argument("--output", default="")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--guidance", type=float, default=None, help="BFL passthrough (Klein/Flux)")
    ap.add_argument("--steps", type=int, default=None, help="BFL passthrough (Klein/Flux)")
    args = ap.parse_args()

    key = load_key()
    out_dir = ROOT / "Media" / "generated" / "openrouter-cover-pj-test"
    out_dir.mkdir(parents=True, exist_ok=True)

    refs = []
    for p in args.ref:
        path = Path(p)
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            raise SystemExit(f"Ref not found: {path}")
        refs.append({"type": "image_url", "image_url": {"url": file_to_data_url(path)}})

    payload: dict = {
        "model": args.model,
        "prompt": args.prompt,
        "n": args.n,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "output_format": "png",
    }
    if refs:
        payload["input_references"] = refs
    # Klein/Flux.2 passthrough (ignored by Gemini)
    bfl_opts = {}
    if args.guidance is not None:
        bfl_opts["guidance"] = args.guidance
    if args.steps is not None:
        bfl_opts["steps"] = args.steps
    if bfl_opts:
        payload["provider"] = {"options": {"black-forest-labs": bfl_opts}}

    t0 = time.time()
    result = call_images(payload, key)
    elapsed = round(time.time() - t0, 2)

    data = result.get("data") or []
    if not data:
        print(json.dumps({"success": False, "error": "no data", "raw": result}, indent=2))
        sys.exit(1)

    saved = []
    stamp = time.strftime("%Y%m%d-%H%M%S")
    for i, item in enumerate(data):
        b64 = item.get("b64_json")
        if not b64:
            continue
        ext = "png"
        mt = item.get("media_type") or "image/png"
        if "jpeg" in mt or "jpg" in mt:
            ext = "jpg"
        elif "webp" in mt:
            ext = "webp"
        if args.output and len(data) == 1:
            out = Path(args.output)
            if not out.is_absolute():
                out = ROOT / out
        else:
            out = out_dir / f"or-pj-{stamp}-{i+1}.{ext}"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(b64))
        saved.append(str(out))

    usage = result.get("usage") or {}
    print(
        json.dumps(
            {
                "success": True,
                "model": args.model,
                "elapsed_s": elapsed,
                "files": saved,
                "file_path": saved[0] if saved else None,
                "usage": usage,
                "cost": usage.get("cost"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
