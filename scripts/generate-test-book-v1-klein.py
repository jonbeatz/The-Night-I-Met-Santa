#!/usr/bin/env python3
"""Klein 4B full-book layout mock → Media/generated/test-book-v1/

Lane A only (IMAGE-LANE-PROMPTS.md Dial D2).
Each unit: WIDE (2:1) + LEFT + RIGHT split.
Resume-safe: skips existing WIDE files.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Media" / "generated" / "test-book-v1"
MODEL = "black-forest-labs/flux.2-klein-4b"
GUIDANCE = 4.6
STEPS = 30
RESOLUTION = "1K"

KLEIN = (
    "KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast, "
    "rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous "
    "but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare. "
    "Clean Santa coat — NO letters, NO glyphs on clothing. Soft blended edges. "
    "NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated. "
    "No text, no letters, no watermark, no title typography in the image."
)

CAST = (
    "Continuity: young boy ~5-7 years old in oatmeal/beige pajamas with tiny green holly and red berries, "
    "barefoot when indoors. Santa Claus: brilliant white hair and beard, red coat WITH brown suspenders, "
    "kind grandfatherly face when visible. Same cozy Christmas Eve living room family set."
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


def gen(prompt: str, out_path: Path, aspect: str, refs: list[Path], key: str) -> Path:
    if out_path.exists() and out_path.stat().st_size > 1000:
        print(f"  SKIP exists: {out_path.name}")
        return out_path
    payload: dict = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "aspect_ratio": aspect,
        "resolution": RESOLUTION,
        "output_format": "png",
        "provider": {"options": {"black-forest-labs": {"guidance": GUIDANCE, "steps": STEPS}}},
    }
    if refs:
        payload["input_references"] = [
            {"type": "image_url", "image_url": {"url": file_to_data_url(p)}} for p in refs if p.exists()
        ]
    t0 = time.time()
    try:
        result = call_images(payload, key)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code}: {err[:1500]}") from e
    data = result.get("data") or []
    if not data or not data[0].get("b64_json"):
        raise SystemExit(f"No image data: {json.dumps(result)[:800]}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(data[0]["b64_json"]))
    cost = (result.get("usage") or {}).get("cost")
    print(f"  OK {out_path.name}  {round(time.time()-t0,1)}s  cost={cost}")
    return out_path


def split_lr(wide_path: Path, left_path: Path, right_path: Path) -> None:
    im = Image.open(wide_path).convert("RGB")
    w, h = im.size
    mid = w // 2
    im.crop((0, 0, mid, h)).save(left_path)
    im.crop((mid, 0, w, h)).save(right_path)
    print(f"  SPLIT -> {left_path.name} | {right_path.name}  ({w}x{h})")


def job_wide(
    stem: str,
    folder: Path,
    scene: str,
    key: str,
    refs: list[Path],
    aspect: str = "16:9",
) -> None:
    wide = folder / f"{stem}-WIDE.png"
    left = folder / f"{stem}-LEFT.png"
    right = folder / f"{stem}-RIGHT.png"
    prompt = f"{scene}\n\n{CAST}\n\n{KLEIN}\n\nWide cinematic two-page open-book layout, continuous scene across full width, leave soft quiet outer corners for later text overlay, gutter-safe (important faces/props not centered on middle fold)."
    print(f"\n== {stem} ==")
    (OUT / "prompts" / f"{stem}.txt").write_text(prompt, encoding="utf-8")
    gen(prompt, wide, aspect, refs, key)
    split_lr(wide, left, right)


def job_single(stem: str, folder: Path, scene: str, key: str, refs: list[Path]) -> None:
    path = folder / f"{stem}.png"
    prompt = f"{scene}\n\n{CAST}\n\n{KLEIN}\n\nSquare children's picture-book page, leave soft quiet zone for later text overlay."
    print(f"\n== {stem} ==")
    (OUT / "prompts" / f"{stem}.txt").write_text(prompt, encoding="utf-8")
    gen(prompt, path, "1:1", refs, key)


def main() -> None:
    key = load_key()
    covers = OUT / "covers"
    matter = OUT / "matter"
    spreads = OUT / "spreads"
    for d in (covers, matter, spreads, OUT / "prompts"):
        d.mkdir(parents=True, exist_ok=True)

    ref_cover = ROOT / "Media/approved/covers/cover-front.png"
    ref_boy = ROOT / "Media/approved/characters/boy-narrator-G0.png"
    ref_santa = ROOT / "Media/approved/characters/santa-G0.png"
    ref_jack = ROOT / "Media/approved/characters/jack-farrell-portrait.png"
    cast_refs = [ref_cover, ref_boy, ref_santa]
    boy_refs = [ref_cover, ref_boy]
    santa_refs = [ref_cover, ref_santa]
    jack_refs = [ref_jack, ref_cover]

    # --- COVERS ---
    job_single(
        "00-cover-front-klein",
        covers,
        "Children's Christmas book FRONT COVER scene matching the approved cover composition: "
        "young boy in oatmeal holly pajamas peeking from left doorway into warm living room; "
        "Santa kneeling by Christmas tree with BACK and SIDE to viewer — Santa face HIDDEN looking into sack; "
        "glowing tree, gifts, fireplace edge; magical hush. Composition like classic peek-at-Santa cover.",
        key,
        cast_refs,
    )
    job_single(
        "00-cover-back-klein",
        covers,
        "Children's Christmas book BACK COVER art: quiet snowy night village path OR warm empty living room "
        "after Santa left, glowing tree soft embers fireplace, cozy heirloom mood, soft open space in center "
        "and lower third for blurb text later, no people or tiny distant figures only.",
        key,
        [ref_cover],
    )
    job_wide(
        "00-cover-wrap",
        covers,
        "Full dust-jacket WRAP mock: LEFT half = back cover quiet snowy Christmas night path with warm window glow; "
        "RIGHT half = front cover boy peeking at Santa from doorway (Santa face hidden). Continuous Christmas night mood.",
        key,
        cast_refs,
        aspect="21:9",
    )

    # --- MATTER OPENS (facing pages as WIDE + L/R) ---
    job_wide(
        "01-title-copyright",
        matter,
        "Open book front matter spread. LEFT page: elegant quiet title-page atmosphere — soft Christmas tree glow, "
        "ornament vignette, empty soft center for title text later, magical cream and gold. "
        "RIGHT page: copyright-page calm — soft muted living-room corner or parchment-warm empty space, "
        "very quiet, plenty of open area for small legal text later. Continuous soft Christmas palette.",
        key,
        [ref_cover],
    )
    job_wide(
        "02-dedication-about",
        matter,
        "Open book matter spread. LEFT: soft dedication page — gentle candlelight or single ornament, "
        "lots of quiet cream space for short dedication text. "
        "RIGHT: About This Story page mood — peek of living room glow and toys, wonder atmosphere, "
        "open soft zone for paragraph text. Warm heirloom Christmas.",
        key,
        boy_refs,
    )
    job_wide(
        "03-thankyou-author",
        matter,
        "Open book back-matter spread. LEFT: Thank You page — warm soft vignette living room after Christmas Eve, "
        "quiet open space for thank-you text. "
        "RIGHT: About the Author page — elderly kind man in cream cable-knit sweater in armchair by Christmas tree "
        "(match Jack Farrell portrait mood), soft open zone beside him for author bio text.",
        key,
        jack_refs,
    )
    job_wide(
        "04-quiet-merrychristmas",
        matter,
        "Open book closing matter spread. LEFT: quiet ornament page — soft glowing Christmas ornament or candle, "
        "peaceful vignette, open space for God bless / Merry Christmas lines. "
        "RIGHT: final Merry Christmas page — soft magical Christmas night window snow or tree star glow, "
        "warm blessing mood, open center for closing lines.",
        key,
        [ref_cover],
    )

    # --- STORY SPREADS S1–S12 (G2.1 map) ---
    story = [
        (
            "S01-approach",
            "STORY SPREAD Approach: Christmas Eve night, curious boy in oatmeal holly pajamas crouching and peeking "
            "from a deep shadowed hallway toward a warmly glowing living room doorway; toys faintly visible beyond; "
            "anticipation and hush; continuous scene hallway LEFT → doorway glow RIGHT.",
            boy_refs,
        ),
        (
            "S02-threshold",
            "STORY SPREAD Threshold: decorated Christmas door with wreath and bolt on LEFT; boy entering living room "
            "on RIGHT; Santa Claus HALF-SEEN among gifts and ribbons (not full face yet); shock and wonder; "
            "warm tree light ahead.",
            cast_refs,
        ),
        (
            "S03-eyes-met",
            "STORY SPREAD Eyes Met HERO: boy and Santa Claus meeting eyes for the first time face-to-face; "
            "Santa in all his splendor brilliant white hair, red coat WITH suspenders clearly visible; "
            "gifts ribbons boxes on floor; boy's jaw-drop wonder; intimate magical moment across full width.",
            cast_refs,
        ),
        (
            "S04-sit-here",
            "STORY SPREAD Sit Here: Santa sitting on living-room floor among boxes gifts and ribbons galore, "
            "kindly beckoning boy to sit beside him; boy still standing in awe; tree and fireplace glow; "
            "cozy invitation moment.",
            cast_refs,
        ),
        (
            "S05-chat",
            "STORY SPREAD Chat & Laugh: Santa and boy sitting together on floor among Christmas gifts, "
            "laughing warmly chatting; animated friendly conversation; tree lights fireplace; "
            "who-cares joyful hour mood.",
            cast_refs,
        ),
        (
            "S06-cocoa",
            "STORY SPREAD Cocoa: Santa holding steaming mug of hot cocoa, storytelling gesture; boy listening nearby; "
            "toys gifts tree glow; passion for cocoa instead of milk beat; soft steam; cozy magic.",
            cast_refs,
        ),
        (
            "S07-proof",
            "STORY SPREAD Need Proof: boy looking upward startled by noise on the roof; idea to get a camera for proof; "
            "Christmas living room urgency; Santa still in scene or mid-departure cue; playful scramble mood.",
            cast_refs,
        ),
        (
            "S08-gone",
            "STORY SPREAD Gone: boy rushes back with a simple old camera; living room now empty of Santa; "
            "gifts remain under glowing tree; disappointment without proof; empty warm room feeling.",
            boy_refs,
        ),
        (
            "S09-search",
            "STORY SPREAD Search: boy searching living room for clue — hat shoe tip; looking up empty fireplace flue; "
            "then noticing something on an old wooden chair; continuous search → chair discovery across width.",
            boy_refs,
        ),
        (
            "S10-the-note",
            "STORY SPREAD The Note: LEFT boy finds folded note on chair; RIGHT boy tearing open the note with wonder; "
            "no readable writing on paper — blank soft paper only; tree glow fireplace; emotional climax.",
            boy_refs,
        ),
        (
            "S11-wish",
            "STORY SPREAD Wish: soft intimate moment — boy holding open note near glowing Christmas tree; "
            "magical quiet realization that what Santa wants is simply a note; no readable text on paper; "
            "warm blessing light.",
            boy_refs,
        ),
        (
            "S12-blessing",
            "STORY SPREAD Closing Blessing: Santa and boy together in warm farewell mood among gifts and tree; "
            "gentle blessing atmosphere — love Christmas, act like a kid, faith; soft magical golden glow; "
            "heirloom closing image. Santa kind face visible.",
            cast_refs,
        ),
    ]

    for stem, scene, refs in story:
        job_wide(stem, spreads, scene, key, refs, aspect="16:9")

    manifest = {
        "model": MODEL,
        "guidance": GUIDANCE,
        "steps": STEPS,
        "lane": "A-Klein-D2",
        "out": str(OUT),
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("\nDONE test-book-v1 generation")


if __name__ == "__main__":
    main()
