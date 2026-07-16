#!/usr/bin/env python3
"""Fix test-book-v1: generate true LEFT+RIGHT 1:1 pages, stitch WIDE 2:1.

Klein often ignores non-square aspect — so we do L/R as separate gens.
Resume-safe: skips existing LEFT/RIGHT over 1000 bytes.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Media" / "generated" / "test-book-v1"
MODEL = "black-forest-labs/flux.2-klein-4b"
GUIDANCE = 4.6
STEPS = 30

KLEIN = (
    "KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast, "
    "rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous "
    "but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare. "
    "Clean Santa coat — NO letters, NO glyphs on clothing. Soft blended edges. "
    "NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated. "
    "No text, no letters, no watermark, no title typography in the image."
)

CAST = (
    "Continuity: young boy ~5-7 in oatmeal/beige pajamas with tiny green holly and red berries. "
    "Santa: brilliant white hair/beard, red coat WITH brown suspenders when visible. "
    "Same cozy Christmas Eve living room set."
)


def load_key() -> str:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        if line.startswith("OPENROUTER_API_KEY=") and not line.strip().startswith("#"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("OPENROUTER_API_KEY missing")


def file_to_data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def call_images(payload: dict, key: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/images",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/jonbeatz/the-night-i-met-santa",
            "X-Title": "The-Night-I-Met-Santa-test-book-v1",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def gen(prompt: str, out_path: Path, refs: list[Path], key: str, force: bool = False) -> Path:
    if (not force) and out_path.exists() and out_path.stat().st_size > 1000:
        # Re-gen if previous was a bad half-split from square wide (tall half)
        try:
            w, h = Image.open(out_path).size
            if w < h * 0.7:  # half-width portrait from bad split
                force = True
            elif out_path.name.endswith("-WIDE.png") and w <= h + 20:
                force = True  # square fake wide
        except Exception:
            pass
        if not force:
            print(f"  SKIP {out_path.name}")
            return out_path

    payload: dict = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "aspect_ratio": "1:1",
        "resolution": "1K",
        "output_format": "png",
        "provider": {"options": {"black-forest-labs": {"guidance": GUIDANCE, "steps": STEPS}}},
    }
    if refs:
        payload["input_references"] = [
            {"type": "image_url", "image_url": {"url": file_to_data_url(p)}} for p in refs if p.exists()
        ]
    import time

    t0 = time.time()
    try:
        result = call_images(payload, key)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:1500]}") from e
    data = result.get("data") or []
    if not data or not data[0].get("b64_json"):
        raise SystemExit(f"No image: {json.dumps(result)[:600]}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(data[0]["b64_json"]))
    cost = (result.get("usage") or {}).get("cost")
    print(f"  OK {out_path.name}  {round(time.time()-t0,1)}s  cost={cost}")
    return out_path


def stitch_wide(left: Path, right: Path, wide: Path) -> None:
    L = Image.open(left).convert("RGB")
    R = Image.open(right).convert("RGB")
    # match heights
    h = min(L.height, R.height)
    L = L.resize((int(L.width * h / L.height), h), Image.Resampling.LANCZOS)
    R = R.resize((int(R.width * h / R.height), h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (L.width + R.width, h))
    canvas.paste(L, (0, 0))
    canvas.paste(R, (L.width, 0))
    canvas.save(wide)
    print(f"  STITCH {wide.name}  {canvas.size[0]}x{canvas.size[1]}")


def page_pair(
    stem: str,
    folder: Path,
    left_scene: str,
    right_scene: str,
    refs: list[Path],
    key: str,
) -> None:
    print(f"\n== {stem} ==")
    left = folder / f"{stem}-LEFT.png"
    right = folder / f"{stem}-RIGHT.png"
    wide = folder / f"{stem}-WIDE.png"
    lp = (
        f"LEFT page of an open children's Christmas picture book. {left_scene}\n\n{CAST}\n\n{KLEIN}\n"
        "Square page. Soft quiet zone for later text. Continuous story with facing right page (same room/night)."
    )
    rp = (
        f"RIGHT page of an open children's Christmas picture book. {right_scene}\n\n{CAST}\n\n{KLEIN}\n"
        "Square page. Soft quiet zone for later text. Continuous story with facing left page (same room/night)."
    )
    (OUT / "prompts" / f"{stem}-LEFT.txt").write_text(lp, encoding="utf-8")
    (OUT / "prompts" / f"{stem}-RIGHT.txt").write_text(rp, encoding="utf-8")
    gen(lp, left, refs, key)
    gen(rp, right, refs, key)
    stitch_wide(left, right, wide)


def main() -> None:
    key = load_key()
    covers = OUT / "covers"
    matter = OUT / "matter"
    spreads = OUT / "spreads"
    (OUT / "prompts").mkdir(parents=True, exist_ok=True)

    ref_cover = ROOT / "Media/approved/covers/cover-front.png"
    ref_boy = ROOT / "Media/approved/characters/boy-narrator-G0.png"
    ref_santa = ROOT / "Media/approved/characters/santa-G0.png"
    ref_jack = ROOT / "Media/approved/characters/jack-farrell-portrait.png"
    cast_refs = [ref_cover, ref_boy, ref_santa]
    boy_refs = [ref_cover, ref_boy]
    jack_refs = [ref_jack, ref_cover]

    # Cover wrap as true L/R
    page_pair(
        "00-cover-wrap",
        covers,
        "BACK COVER art: quiet snowy Christmas night village path, warm window glow, soft open center for blurb later.",
        "FRONT COVER: boy in oatmeal holly pajamas peeking from doorway; Santa by tree BACK/SIDE only — face HIDDEN; gifts tree glow.",
        cast_refs,
        key,
    )

    page_pair(
        "01-title-copyright",
        matter,
        "Title page atmosphere: soft Christmas tree glow, ornament vignette, empty soft cream center for title text later.",
        "Copyright page calm: soft muted warm empty space / quiet living-room corner, lots of open area for small legal text.",
        [ref_cover],
        key,
    )
    page_pair(
        "02-dedication-about",
        matter,
        "Dedication page: gentle candlelight or single ornament, lots of quiet cream space for short dedication.",
        "About This Story page: peek of living room glow and toys, wonder mood, open soft zone for paragraph text.",
        boy_refs,
        key,
    )
    page_pair(
        "03-thankyou-author",
        matter,
        "Thank You page: warm soft vignette after Christmas Eve, quiet open space for thank-you text.",
        "About the Author: elderly kind man cream cable-knit sweater in armchair by Christmas tree (Jack Farrell mood), open zone for bio.",
        jack_refs,
        key,
    )
    page_pair(
        "04-quiet-merrychristmas",
        matter,
        "Quiet ornament page: soft glowing Christmas ornament or candle, peaceful vignette, open space for blessing lines.",
        "Final Merry Christmas page: magical night window snow or tree star glow, warm blessing mood, open center for closing lines.",
        [ref_cover],
        key,
    )

    story = [
        (
            "S01-approach",
            "Dim hallway Christmas Eve: boy in oatmeal holly pajamas crouching peeking toward glowing living-room doorway; anticipation.",
            "Warm living-room doorway glow from hallway view; toys faintly visible beyond door; magical hush continuing the sneak.",
            boy_refs,
        ),
        (
            "S02-threshold",
            "Decorated Christmas door with wreath and bolt; boy's hand near knob; warm light under door; nerves.",
            "Boy just inside living room; Santa HALF-SEEN among gifts (not full face); shock and wonder; tree lights.",
            cast_refs,
        ),
        (
            "S03-eyes-met",
            "Boy's face of wonder jaw-drop as he meets Santa's eyes; Christmas living room gifts around; intimate magic.",
            "Santa in full splendor brilliant white hair, red coat WITH suspenders, kind eyes meeting child; gifts ribbons floor.",
            cast_refs,
        ),
        (
            "S04-sit-here",
            "Wide gift field on floor boxes ribbons; boy standing still in awe nearby Santa.",
            "Santa sitting on floor among gifts kindly beckoning 'sit here'; tree fireplace glow; cozy invitation.",
            cast_refs,
        ),
        (
            "S05-chat",
            "Boy sitting on floor among gifts laughing with Santa; warm chat thrill.",
            "Santa laughing warmly mid-story with child; tree lights fireplace; joyful hour mood.",
            cast_refs,
        ),
        (
            "S06-cocoa",
            "Boy listening near Christmas tree as Santa tells stories of places people things; cozy.",
            "Santa holding steaming hot cocoa mug proudly; cocoa not milk beat; soft steam tree glow.",
            cast_refs,
        ),
        (
            "S07-proof",
            "Boy looking up startled by noise on the roof; Christmas living room urgency.",
            "Boy forming plan for a camera / photo proof; playful scramble; Santa mid-scene or departing cue.",
            cast_refs,
        ),
        (
            "S08-gone",
            "Boy rushing back through doorway with a simple old camera; urgency.",
            "Empty living room — Santa gone; gifts under glowing tree; boy disappointed without proof.",
            boy_refs,
        ),
        (
            "S09-search",
            "Boy searching room for clue hat shoe tip; looking around gifts fireplace.",
            "Boy looks up empty flue then notices something on old wooden chair; discovery moment.",
            boy_refs,
        ),
        (
            "S10-the-note",
            "Boy finds folded note on chair; wonder; paper blank no readable writing.",
            "Boy tearing open the note with emotion; blank soft paper only; tree glow fireplace.",
            boy_refs,
        ),
        (
            "S11-wish",
            "Boy holding open note near glowing Christmas tree; soft quiet realization.",
            "Magical soft light — what Santa wants is simply a note feeling; no readable text on paper.",
            boy_refs,
        ),
        (
            "S12-blessing",
            "Santa and boy warm farewell among gifts; gentle blessing mood love Christmas act like a kid.",
            "Closing heirloom blessing glow; Santa kind face; tree star; God-bless atmosphere.",
            cast_refs,
        ),
    ]

    for stem, left_s, right_s, refs in story:
        page_pair(stem, spreads, left_s, right_s, refs, key)

    print("\nDONE true L/R + stitched WIDE")


if __name__ == "__main__":
    main()
