"""One-off: Gemini 3 Pro image from P01 v17 spot layout — longer timeout, fewer refs."""
from __future__ import annotations

import base64
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

MODEL = "google/gemini-3-pro-image"
OUT = ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v18"
OUT.mkdir(parents=True, exist_ok=True)

REFS = [
    ROOT / "Media" / "generated" / "mocks" / "P01-title" / "v17" / "art-P01-title-dial.png",
    ROOT / "Images" / "styles1" / "p21-beat12-13-note-LEFT.png",
    ROOT / "Media" / "approved" / "covers" / "cover-front.png",
]

PROMPT = """Based on the attached spot-illustration reference (centered Christmas tree with presents on an open cream field — clean title-page LAYOUT like a single floating graphic): create a print-quality children's Christmas TITLE PAGE illustration in our locked heirloom style.

LAYOUT: clean SPOT illustration centered on the page — NOT full-bleed room, NOT wall-to-wall scene. Large calm negative space around a single Christmas tree with wrapped presents under it. Soft cream/ivory open background with gentle watercolor paper feel. Plenty of margin for later typography above/below. Square 1:1.

STYLE (master): Traditional children's Christmas picture-book illustration, heirloom storybook quality, heavily painted in rich gouache and soft watercolor with visible soft brushstrokes and gentle blended edges, NOT colored pencil NOT crayon NOT scratchy sketch lines, warm soft golden tree-light glow, deep crimson and forest green palette with warm cream and muted earth tones, nostalgic Golden Age painted realism, intimate cozy magical atmosphere, Charles Santore–inspired storybook painting, classic Clement C. Moore Christmas book feel, highly detailed but soft and painterly, print-ready composition, no text, no letters, no watermark.

Match the soft painted watercolor quality of our locked cover and p21 fireplace refs. Keep the quiet centered tree+gifts composition of the v17 dial. No people, no faces, no fireplace, no furniture room, no logos, no text."""


def load_key() -> str:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        if line.startswith("OPENROUTER_API_KEY=") and not line.strip().startswith("#"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("OPENROUTER_API_KEY missing")


def file_to_data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def main() -> None:
    key = load_key()
    refs = []
    for p in REFS:
        if not p.exists():
            raise SystemExit(f"missing {p}")
        print(f"ref {p.name} ({p.stat().st_size} bytes)")
        refs.append({"type": "image_url", "image_url": {"url": file_to_data_url(p)}})

    payload = {
        "model": MODEL,
        "prompt": PROMPT,
        "n": 1,
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "output_format": "png",
        "input_references": refs,
    }
    body = json.dumps(payload).encode("utf-8")
    print(f"payload_bytes={len(body)} calling {MODEL}…")
    t0 = time.time()
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
        with urllib.request.urlopen(req, timeout=600) as r:
            result = json.load(r)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code}: {err[:2000]}") from e

    elapsed = round(time.time() - t0, 2)
    data = result.get("data") or []
    if not data or not data[0].get("b64_json"):
        raise SystemExit(json.dumps(result, indent=2)[:2000])

    out = OUT / "art-P01-title-gemini.png"
    out.write_bytes(base64.b64decode(data[0]["b64_json"]))
    # also save dial-named copy for consistency
    dial = OUT / "art-P01-title-dial.png"
    dial.write_bytes(out.read_bytes())

    usage = result.get("usage") or {}
    recipe = f"""# RECIPE — P01-title / v18

| Field | Value |
|-------|--------|
| **unit** | P01-title |
| **version** | v18 |
| **date** | 2026-07-20 |
| **lane** | B finals test |
| **service** | OpenRouter |
| **model** | `{MODEL}` |
| **resolution** | 2K · 1:1 |
| **layout base** | v17 spot tree+gifts |
| **style refs** | v17 dial · p21 · cover-front (beige-v2) |
| **elapsed_s** | {elapsed} |
| **cost** | {usage.get("cost")} |
| **verdict** | pending Jon review |

## Notes
Gemini 3 Pro Image test — same spot layout as v17, master ILLUSTRATION-STYLE prompt.
"""
    (OUT / "RECIPE.md").write_text(recipe, encoding="utf-8")
    print(json.dumps({"success": True, "file": str(out), "bytes": out.stat().st_size, "elapsed_s": elapsed, "cost": usage.get("cost")}, indent=2))


if __name__ == "__main__":
    main()
