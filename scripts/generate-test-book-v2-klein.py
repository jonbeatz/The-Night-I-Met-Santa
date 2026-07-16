#!/usr/bin/env python3
"""test-book-v2 — FULL STORY layout mock (Klein 4B Dial D2).

CRITICAL FIX vs v1: do NOT pass cover as style ref on interior pages
(that made every page look like the cover). Distinct scene per page.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Media" / "generated" / "test-book-v2"
MODEL = "black-forest-labs/flux.2-klein-4b"
GUIDANCE = 4.6
STEPS = 30

KLEIN = (
    "KLEIN STYLE (mockups only): deep shadowed hallway vs warm room when relevant, strong punchy contrast, "
    "rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous "
    "but CONTROLLED — soft bloom, ornaments readable, NOT blown-out glare. "
    "Clean clothing — NO letters, NO glyphs. Soft blended edges. "
    "NOT washed out, NOT pale, NOT pencil grain, NOT desaturated. "
    "No text, no letters, no watermark, no book title typography."
)

CAST = (
    "Characters when present: boy age ~5-7, short brown hair, oatmeal/beige pajamas with tiny green holly "
    "and red berries, often barefoot. Santa: plump, brilliant white hair and beard, red coat, brown suspenders, "
    "kind face when shown. Same house living room / hallway family — but EACH PAGE is a DIFFERENT camera angle "
    "and DIFFERENT action. "
)

ANTI_COVER = (
    "IMPORTANT: This is an INTERIOR story page, NOT a book cover. "
    "Do NOT repeat the famous cover composition (boy peeking from doorway while Santa kneels at tree with back turned). "
    "Invent a fresh unique angle for THIS beat only."
)


def load_key() -> str:
    for line in (ROOT / ".env.local").read_text(encoding="utf-8").splitlines():
        if line.startswith("OPENROUTER_API_KEY=") and not line.strip().startswith("#"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("OPENROUTER_API_KEY missing")


def data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def call(payload: dict, key: str) -> dict:
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/images",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/jonbeatz/the-night-i-met-santa",
            "X-Title": "test-book-v2",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def gen(prompt: str, out: Path, refs: list[Path], key: str) -> None:
    if out.exists() and out.stat().st_size > 2000:
        print(f"  SKIP {out.name}")
        return
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "aspect_ratio": "1:1",
        "resolution": "1K",
        "output_format": "png",
        "provider": {"options": {"black-forest-labs": {"guidance": GUIDANCE, "steps": STEPS}}},
    }
    existing = [p for p in refs if p.exists()]
    if existing:
        payload["input_references"] = [
            {"type": "image_url", "image_url": {"url": data_url(p)}} for p in existing
        ]
    t0 = time.time()
    try:
        result = call(payload, key)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:1500]}") from e
    data = result.get("data") or []
    if not data or not data[0].get("b64_json"):
        raise SystemExit(f"No image for {out.name}: {json.dumps(result)[:500]}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(data[0]["b64_json"]))
    print(f"  OK {out.name}  {round(time.time()-t0,1)}s  cost={(result.get('usage') or {}).get('cost')}")


def stitch(left: Path, right: Path, wide: Path) -> None:
    L = Image.open(left).convert("RGB")
    R = Image.open(right).convert("RGB")
    h = min(L.height, R.height)
    L = L.resize((int(L.width * h / L.height), h), Image.Resampling.LANCZOS)
    R = R.resize((int(R.width * h / R.height), h), Image.Resampling.LANCZOS)
    c = Image.new("RGB", (L.width + R.width, h))
    c.paste(L, (0, 0))
    c.paste(R, (L.width, 0))
    c.save(wide)
    print(f"  STITCH {wide.name} {c.size[0]}x{c.size[1]}")


def page(stem: str, folder: Path, scene: str, refs: list[Path], key: str, anti_cover: bool = True) -> Path:
    out = folder / f"{stem}.png"
    bits = [scene, CAST, KLEIN]
    if anti_cover:
        bits.append(ANTI_COVER)
    bits.append("Square children's picture-book INTERIOR page. Soft quiet corner for later text overlay.")
    prompt = "\n\n".join(bits)
    (OUT / "prompts" / f"{stem}.txt").write_text(prompt, encoding="utf-8")
    print(f"\n== {stem} ==")
    gen(prompt, out, refs, key)
    return out


def pair(stem: str, folder: Path, left_scene: str, right_scene: str, refs: list[Path], key: str) -> None:
    L = page(f"{stem}-LEFT", folder, left_scene, refs, key)
    R = page(f"{stem}-RIGHT", folder, right_scene, refs, key)
    stitch(L, R, folder / f"{stem}-WIDE.png")


def main() -> None:
    key = load_key()
    for d in ("covers", "matter", "spreads", "prompts"):
        (OUT / d).mkdir(parents=True, exist_ok=True)

    boy = ROOT / "Media/approved/characters/boy-narrator-G0.png"
    santa = ROOT / "Media/approved/characters/santa-G0.png"
    jack = ROOT / "Media/approved/characters/jack-farrell-portrait.png"
    cover = ROOT / "Media/approved/covers/cover-front.png"

    # Seed approved cover (not regenerated as "the whole book")
    import shutil

    shutil.copy2(cover, OUT / "covers" / "00-cover-front-APPROVED.png")

    # ---- COVERS (cover ref OK here only) ----
    page(
        "00-cover-front-klein",
        OUT / "covers",
        "BOOK COVER ONLY: boy peeking from left doorway in oatmeal holly pajamas; Santa kneeling at Christmas tree "
        "with BACK to viewer face HIDDEN in sack; gifts; glowing tree. Classic peek composition.",
        [cover, boy, santa],
        key,
        anti_cover=False,
    )
    page(
        "00-cover-back",
        OUT / "covers",
        "BOOK BACK COVER: quiet snowy Christmas village street at night, one warm glowing window, soft falling snow, "
        "empty path, cozy lonely magic, open soft center for blurb text. NO boy peeking, NO Santa.",
        [],
        key,
        anti_cover=False,
    )

    # ---- MATTER (no cover ref) ----
    pair(
        "p01-02-title-copyright",
        OUT / "matter",
        "TITLE PAGE art only: soft close-up of a glowing Christmas tree topper star and ornaments, cream vignette, "
        "empty soft center for the title words later. NO people.",
        "COPYRIGHT PAGE art: quiet parchment-warm empty desk corner with a single pine sprig and candle, "
        "lots of blank soft space for small legal text. NO people, NO cover scene.",
        [],
        key,
    )
    pair(
        "p03-04-dedication-about",
        OUT / "matter",
        "DEDICATION PAGE: single red Christmas stocking hanging on a white mantel, soft fire glow, "
        "lots of quiet cream space for short dedication text. NO full cover scene.",
        "ABOUT THIS STORY mood: small toys and wrapped gifts on a rug, soft tree lights bokeh, "
        "wonder atmosphere, open zone for paragraphs. Boy optional tiny distant silhouette only.",
        [boy],
        key,
    )

    # ---- STORY S01–S12 — UNIQUE SCENES (boy/santa refs only, NEVER cover) ----
    pair(
        "S01-approach",
        OUT / "spreads",
        "SCENE: dark upstairs hallway at night. Boy on hands and knees crawling toward a crack of warm light "
        "under a door. Toys behind him. Camera LOW behind boy. Mystery noise mood.",
        "SCENE: boy's eye-level view through a slightly open door into a bright living room — "
        "blurred shapes of a Christmas tree and gift boxes beyond. Wonder. NO Santa face yet.",
        [boy],
        key,
    )
    pair(
        "S02-threshold",
        OUT / "spreads",
        "SCENE: CLOSE-UP of a decorated Christmas door — evergreen wreath, red bow, old iron bolt and lock. "
        "Warm gold light spilling under the door into dark hall. Boy's small hand reaching for the knob.",
        "SCENE: boy just stepped inside the living room, frozen mid-step among gift boxes. "
        "In the distance Santa's red coat and white beard partially visible among ribbons — half-hidden, not facing camera fully. "
        "Shock and comedy of almost catching Santa.",
        [boy, santa],
        key,
    )
    pair(
        "S03-eyes-met",
        OUT / "spreads",
        "SCENE: CLOSE intimate PORTRAIT of the boy's face — jaw dropped, eyes wide with wonder, "
        "warm tree-light on his cheeks. First meeting moment. Face fills much of frame.",
        "SCENE: Santa facing the boy/camera in FULL SPLENDOR — brilliant white hair, kind eyes, "
        "red coat WITH brown suspenders clearly visible, sitting among gifts. Magical hero reveal. "
        "NOT Santa's back. NOT doorway peek cover pose.",
        [boy, santa],
        key,
    )
    pair(
        "S04-sit-here",
        OUT / "spreads",
        "SCENE: HIGH angle looking down — living room floor covered with boxes, ribbons, wrapping paper galore. "
        "Boy standing stiff as a statue among the gifts.",
        "SCENE: Santa sitting cross-legged on the floor among presents, smiling, patting the empty spot beside him "
        "inviting the boy to sit. Warm fireplace behind. Friendly invitation beat.",
        [boy, santa],
        key,
    )
    pair(
        "S05-chat",
        OUT / "spreads",
        "SCENE: boy and Santa sitting side-by-side on the rug among gifts, mid-laugh, "
        "boy leaning in excitedly. Two-shot conversation. Warm tree bokeh.",
        "SCENE: tighter two-shot — Santa telling a funny story with animated hands, "
        "boy giggling, cocoa-colored warm light. Joyful chatter hour.",
        [boy, santa],
        key,
    )
    pair(
        "S06-cocoa",
        OUT / "spreads",
        "SCENE: Santa gesturing grandly while talking about faraway places, toys, diamond rings — "
        "storytelling pose. Boy listening cross-legged. Living room Christmas set.",
        "SCENE: HERO DETAIL — Santa cradling a steaming mug of hot cocoa, proud smile, soft steam rising. "
        "Boy watching the mug. Cocoa-instead-of-milk joke beat. Mug is the focus.",
        [boy, santa],
        key,
    )
    pair(
        "S07-proof",
        OUT / "spreads",
        "SCENE: boy jolts upright looking UP at the ceiling — noise on the roof. "
        "Santa glances up too. Urgent comic beat. Living room night.",
        "SCENE: boy scrambling toward a hallway clutching an old boxy camera idea — "
        "determined 'I need a photo for proof' energy. Motion blur sense. Camera prop visible.",
        [boy, santa],
        key,
    )
    pair(
        "S08-gone",
        OUT / "spreads",
        "SCENE: boy racing back through the living-room doorway holding a vintage camera, "
        "hair messy, breathless. Dynamic entry.",
        "SCENE: EMPTY living room where Santa was — dent in the gift pile, empty space, "
        "boy standing alone with camera lowered, disappointed. Tree still glowing. Santa gone.",
        [boy],
        key,
    )
    pair(
        "S09-search",
        OUT / "spreads",
        "SCENE: boy searching frantically around the tree — lifting ribbons, looking under boxes "
        "for a hat or shoe clue. Worried curious expression.",
        "SCENE: boy at the fireplace looking UP into the dark chimney flue (nothing there), "
        "THEN turning to notice a small folded paper on an old wooden chair seat. Discovery.",
        [boy],
        key,
    )
    pair(
        "S10-the-note",
        OUT / "spreads",
        "SCENE: boy kneeling by the wooden chair, picking up a small folded note. "
        "Astonished smile. Paper is BLANK of letters (no readable writing). Soft tree glow.",
        "SCENE: boy sitting hard on the chair tearing open the note, eyes huge. "
        "Close emotional climax. Blank paper surface only — no text glyphs.",
        [boy],
        key,
    )
    pair(
        "S11-wish",
        OUT / "spreads",
        "SCENE: boy standing near the Christmas tree holding the open note to the warm lights, "
        "peaceful soft expression. Revelation mood. No readable writing on paper.",
        "SCENE: quiet magical still-life — open note and a candy cane or ornament on a side table "
        "by tree glow, suggesting 'what he wants is simply a note.' Soft vignette. No people required.",
        [boy],
        key,
    )
    pair(
        "S12-blessing",
        OUT / "spreads",
        "SCENE: warm farewell — Santa's hand gently on the boy's shoulder among gifts, "
        "both soft smiles, blessing mood (love Christmas, act like a kid). Intimate.",
        "SCENE: final heirloom image — boy alone by the glowing tree holding the note to his heart, "
        "window snow soft blue outside, golden interior. God-bless closing atmosphere.",
        [boy, santa],
        key,
    )

    # ---- BACK MATTER ----
    pair(
        "p29-30-thankyou-author",
        OUT / "matter",
        "THANK YOU PAGE: empty armchair by dying fireplace embers and tree lights, soft quiet space for thank-you text. Peaceful.",
        "ABOUT THE AUTHOR: elderly kind man in cream cable-knit sweater seated in floral armchair by Christmas tree — "
        "match Jack Farrell portrait mood. Soft open zone beside him for bio text.",
        [jack],
        key,
    )
    pair(
        "p31-32-quiet-close",
        OUT / "matter",
        "QUIET PAGE: single glowing gold Christmas ornament hanging, soft bokeh, cream vignette, space for 'God bless / Merry Christmas'.",
        "FINAL PAGE: snowy night window with warm indoor curtain edge, soft star, blessing close mood, open center for final lines. NO cover peek scene.",
        [],
        key,
    )

    (OUT / "manifest.json").write_text(
        json.dumps({"model": MODEL, "lane": "Klein-D2", "note": "no cover-ref on interiors"}, indent=2),
        encoding="utf-8",
    )
    print("\nDONE test-book-v2")


if __name__ == "__main__":
    main()
