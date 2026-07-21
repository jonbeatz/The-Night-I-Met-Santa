"""
new-test-book-v1 — full cover-to-cover Klein 9B dial test (32 interior pages).
Resumable: skips units that already have art-*.png.
One image file per unit (no twins). Writes RECIPE.md + updates TEXT-IMAGE-MAP.md.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
load_dotenv(ROOT / ".env.local")
KEY = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
if not KEY:
    raise SystemExit("FAL_API_KEY missing")

OUT = ROOT / "Media" / "generated" / "new-test-book-v1"
ENDPOINT = "fal-ai/flux-2/klein/9b"
DATE = "2026-07-21"

D2 = (
    "KLEIN STYLE (mockups only): deep shadowed hallway vs warm room, strong punchy contrast, "
    "rich saturated Christmas colors, opaque gouache feel. Christmas tree lights warm and luminous "
    "but CONTROLLED — soft bloom, ornaments and needles still readable, NOT blown-out white glare. "
    "Clean Santa coat — NO letters, NO glyphs on clothing. Soft blended edges. "
    "NOT washed out, NOT pale, NOT pencil grain, NOT cross-hatching, NOT desaturated."
)

FRAME = (
    "WATERCOLOR FRAME ON: soft irregular white/cream watercolor paper vignette around the scene — "
    "feathered painted edges bleeding into open paper, hand-painted storybook plate (not a hard "
    "rectangle crop, not full-bleed edge-to-edge). Leave calm open cream wash zones for later "
    "typography / soft text-cloud overlays. No hard photo border, no Polaroid frame."
)

STYLE_TAIL = (
    "Traditional children's Christmas picture-book illustration, heirloom storybook quality, "
    "heavily painted rich gouache and soft watercolor like Charles Santore holiday editions, "
    "visible soft brushstrokes, gentle blended edges. NO people-text, NO letters, NO glyphs, "
    "NO watermark, NO logo, NOT colored pencil, NOT crayon, NOT flat cartoon, NOT photoreal CGI."
)

BOY = (
    "young boy about 7–9 years old, oatmeal/taupe pajamas with tiny holly print, soft brown hair, "
    "warm storybook face, wonder in eyes"
)
SANTA = (
    "kind Santa with brilliant white hair and beard, classic red coat with suspenders, "
    "warm gentle expression, traditional Christmas storybook Santa"
)

# 32-page interior + cover plates (test run — ignore prior approvals)
# page_role: cover | single | spread | matter-text | matter-art
PLATES: list[dict] = [
    {
        "id": "cover-front",
        "pages": "cover-front",
        "form": "COVER",
        "filename": "art-cover-front.png",
        "size": "square_hd",
        "type_zone": "upper/mid cream for title type",
        "script_text": "The Night I Met Santa · Jack Farrell (cover type later)",
        "seed": 900101,
        "scene": (
            f"Square hardcover FRONT COVER mood: quiet Christmas Eve house doorway at night, "
            f"warm glow spilling from inside, decorated wreath, soft snow, cozy heirloom gift-book cover. "
            f"A child in {BOY} peeking from doorway — Santa face must stay HIDDEN (back turned or only "
            f"gloved hand / boot tip suggested). Soft open cream area for title typography. "
            f"Calm, magical, not scary."
        ),
    },
    {
        "id": "cover-back",
        "pages": "cover-back",
        "form": "COVER",
        "filename": "art-cover-back.png",
        "size": "square_hd",
        "type_zone": "center/lower for blurb",
        "script_text": "Back blurb + Illustrated edition designed by Jon Farrell · 2026",
        "seed": 900102,
        "scene": (
            "Square hardcover BACK COVER: quiet snowy night path or soft living-room ember glow vignette, "
            "gentle watercolor Christmas atmosphere, large calm open cream wash for back-cover blurb type. "
            "No people faces required. Soft ornamental holly suggestion at edges only."
        ),
    },
    {
        "id": "P01-title",
        "pages": "1",
        "form": "SINGLE",
        "filename": "art-P01-title.png",
        "size": "square_hd",
        "type_zone": "UPPER cream open wash",
        "script_text": "The Night I Met Santa · Jack Farrell",
        "seed": 900201,
        "scene": (
            "TITLE PAGE plate: cozy stone fireplace LEFT with stockings and soft fire, decorated Christmas "
            "tree RIGHT with warm controlled lights and a few gifts, scenery LOWER on the page, generous "
            "empty cream watercolor wash at TOP for title typography. Soft rug, quiet Christmas Eve room. "
            "No people. No hard ceiling lines."
        ),
    },
    {
        "id": "P02-copyright",
        "pages": "2",
        "form": "SINGLE",
        "filename": "art-P02-copyright-textplate.png",
        "size": "square_hd",
        "type_zone": "center (quiet type plate)",
        "script_text": "First illustrated edition, 2026. / Written by Jack Farrell. / Book design by Jon Farrell.",
        "seed": 900202,
        "scene": (
            "TEXT-ONLY storybook plate: soft cream watercolor paper with delicate painted vignette frame, "
            "tiny holly and soft wash ornaments in corners only, large calm empty center for copyright type. "
            "Almost blank heirloom paper, very quiet, no scene, no people, no furniture."
        ),
    },
    {
        "id": "P03-dedication",
        "pages": "3",
        "form": "SINGLE",
        "filename": "art-P03-dedication.png",
        "size": "square_hd",
        "type_zone": "center / lower-center soft wash",
        "script_text": "For my family, with love. — Jack Farrell",
        "seed": 900203,
        "scene": (
            "Dedication plate: soft hearth embers / quiet fireplace vignette, very gentle and sparse, "
            "warm glow, large calm open cream center for dedication typography. No people. Dreamy quiet."
        ),
    },
    {
        "id": "P04-about-text",
        "pages": "4",
        "form": "SINGLE",
        "filename": "art-P04-about-textplate.png",
        "size": "square_hd",
        "type_zone": "full soft center for About body",
        "script_text": "About This Story + Draft A body (BOOK-COPY-DRAFTS.md)",
        "seed": 900204,
        "scene": (
            "LEFT matter page TEXT PLATE: soft cream watercolor framed paper, faint warm wash, "
            "tiny pine sprigs at edges, large empty readable center for multi-paragraph About text. "
            "No scene illustration in the middle. Quiet heirloom paper look."
        ),
    },
    {
        "id": "P05-about-art",
        "pages": "5",
        "form": "SINGLE",
        "filename": "art-P05-about-vignette.png",
        "size": "square_hd",
        "type_zone": "minimal — supporting image page",
        "script_text": "(little or no type — companion to About)",
        "seed": 900205,
        "scene": (
            "RIGHT matter companion: quiet Christmas Eve vignette — snowy window, soft tree glow, "
            "empty gift room hush, peaceful wonder. Soft open edges. No people. Room to breathe."
        ),
    },
    {
        "id": "S01-approach",
        "pages": "6|7",
        "form": "SPREAD",
        "filename": "art-S01-approach-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "soft open cloud zones L and/or lower for poem stanza",
        "script_text": (
            "I searched and I peeked when I first heard the noise. "
            "Something or someone was in with the toys. "
            "I slithered and crawled for a peek of a glimpse. "
            "It must be some fairies or holiday imps."
        ),
        "seed": 900301,
        "scene": (
            f"WIDE seamless SPREAD (continuous left-to-right, NO center gutter line, NO spine fold): "
            f"Christmas Eve night hallway → living room doorway. {BOY} peeking/crawling toward a glowing room "
            f"full of toys and tree light beyond the door. Deep shadowed hallway vs warm room. Soft open "
            f"cream wash areas for poem text cloud (not baked letters). Magical hush."
        ),
    },
    {
        "id": "S02-threshold",
        "pages": "8|9",
        "form": "SPREAD",
        "filename": "art-S02-threshold-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "open wash near door / lower for stanza",
        "script_text": (
            "I got up the nerve to go to the door, a door that was decorated, bolted and locked. "
            "I didn't know it when I entered the room to surprise the amazement or even the shock. "
            "Now I'm usually calm, not very loud, or even known to be a ranter. "
            "But what do you say when you sneak up on Santa?"
        ),
        "seed": 900302,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: decorated Christmas door opening into a warm living room. "
            f"{BOY} at the threshold, stepping in. Beyond: hint of red coat / gifts — Santa not fully revealed yet. "
            f"Strong contrast hallway/room. Soft open zones for text cloud. Wonder and nerves."
        ),
    },
    {
        "id": "S03-eyes-met",
        "pages": "10|11",
        "form": "SPREAD",
        "filename": "art-S03-eyes-met-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "lower or side soft wash for stanza",
        "script_text": (
            "My jaw dropped when our eyes finally met. I knew right then, it was a moment I would never forget. "
            "For there he was in all his splendor, brilliant white hair, red coat with suspenders."
        ),
        "seed": 900303,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: magical first meeting. {BOY} and {SANTA} meeting eyes "
            f"across a gift-strewn living room floor by the Christmas tree and fireplace. Warm glow, "
            f"splendor, frozen wonder. Soft open cream areas for poem text. Faces clear, kind, storybook."
        ),
    },
    {
        "id": "S04-sit-here",
        "pages": "12|13",
        "form": "SPREAD",
        "filename": "art-S04-sit-here-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "open among gifts / lower for dialogue stanza",
        "script_text": (
            "He was down on the floor between boxes, gifts and ribbons galore. "
            "I couldn't move, I stayed very still. Finally he whispered, \"Sit over here. Have a moment to kill.\""
        ),
        "seed": 900304,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: {SANTA} sitting on the floor among wrapped gifts, boxes, "
            f"ribbons galore, inviting {BOY} to sit nearby. Warm tree lights, soft carpet. Generous soft open "
            f"zones between gifts for text cloud. Intimate, quiet thrill."
        ),
    },
    {
        "id": "S05-chat",
        "pages": "14|15",
        "form": "SPREAD",
        "filename": "art-S05-chat-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "side/lower open wash",
        "script_text": (
            "Oh, what a feeling, such a thrill. We chatted and laughed what seemed like an hour. "
            "But with laughs, stories and chatter, who cares, it didn't much matter."
        ),
        "seed": 900305,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: {BOY} and {SANTA} sitting together among gifts, chatting "
            f"and laughing softly, warm friendship glow, Christmas tree soft lights. Soft open cream areas "
            f"for poem. Joyful, intimate, not chaotic."
        ),
    },
    {
        "id": "S06-cocoa",
        "pages": "16|17",
        "form": "SPREAD",
        "filename": "art-S06-cocoa-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "open near cups / lower",
        "script_text": (
            "He spoke of many places, people and things. From toys to music to bright diamond rings. "
            "Coats made of wool, ties made of silk. He even revealed his passion for hot cocoa instead of cold milk."
        ),
        "seed": 900306,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: cozy chat continues — steaming hot cocoa mugs, soft firelight, "
            f"{SANTA} and {BOY} among toys and gifts, storytelling mood. Soft open wash for poem text. Warm, rich color."
        ),
    },
    {
        "id": "S07-proof-tripanel",
        "pages": "18|19",
        "form": "SPREAD",
        "filename": "art-S07-proof-tripanel-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "soft bands between three moments for stanza",
        "script_text": (
            "When I heard all the noise up in the roof, it hit me right then. I needed some proof. "
            "Where can I go? What can I get? I know, a photo. That's my best bet."
        ),
        "seed": 900307,
        "scene": (
            f"WIDE seamless SPREAD designed as THREE soft watercolor story beats flowing left-to-right "
            f"(NOT comic panels with hard gutters — soft vignette blooms that merge): "
            f"(1) roof noise / listening upward, (2) {BOY} realizing he needs proof, (3) idea of a camera/photo "
            f"with excited motion. Continuous Christmas living-room world. Soft open cream between beats for text. "
            f"NO hard comic borders, NO fake book spine line."
        ),
    },
    {
        "id": "S08-gone",
        "pages": "20|21",
        "form": "SPREAD",
        "filename": "art-S08-gone-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "open empty floor zone for stanza",
        "script_text": (
            "I flew out the door and was back in a flash. But oh no, the hour had already passed. "
            "And from the noise on top of the roof I realized that I was still without proof."
        ),
        "seed": 900308,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: {BOY} rushing back into the living room — gifts still there, "
            f"but Santa is gone; empty space where he sat, soft moonlight/tree glow, roof noise implied. "
            f"Emotional empty floor. Soft open wash for poem. Lonely wonder, not horror."
        ),
    },
    {
        "id": "S09-search",
        "pages": "22|23",
        "form": "SPREAD",
        "filename": "art-S09-search-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "open near chair / flue for stanza",
        "script_text": (
            "I turned around slowly. I needed to know, did he leave me a hint, a tip or a clue? "
            "Did he forget his hat or maybe a shoe? Now what am I supposed to do? "
            "I know, I'll look up the flue. I dashed to the flue but nothing was there. "
            "I looked over here and I looked over there. When I saw something on top of the chair, "
            "my proof I thought was just laying right there."
        ),
        "seed": 900309,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: {BOY} searching the Christmas room — peeking up the fireplace flue, "
            f"looking around gifts, noticing something resting on a chair. Soft detective wonder. "
            f"Open cream zones for longer poem text."
        ),
    },
    {
        "id": "S10-note",
        "pages": "24|25",
        "form": "SPREAD",
        "filename": "art-S10-note-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "open around note / lower for stanza",
        "script_text": (
            "It wasn't a shoe, hat or a coat. I couldn't believe it, the old guy. He left me a note. "
            "I fell on the chair and started to stare. What it said, I didn't care. "
            "I tore open the note that Santa had wrote. The words jumped out as to get my attention. "
            "And there was one thing he told me to mention."
        ),
        "seed": 900310,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: {BOY} on/near a chair finding and opening a handwritten note "
            f"from Santa (note paper blank — NO readable letters/glyphs in the painting). Warm lamp/tree glow, "
            f"emotional discovery. Soft open cream for poem text."
        ),
    },
    {
        "id": "S11-wish",
        "pages": "26|27",
        "form": "SPREAD",
        "filename": "art-S11-wish-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "generous open wash for list stanza",
        "script_text": (
            "More than cakes, cocoa or milk. Shirts made of cotton or ties made of silk. "
            "Hats, stockings or a new coat. What he wants is simply a note."
        ),
        "seed": 900311,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: gentle dreamy montage feel inside one continuous watercolor "
            f"room — soft suggestions of cocoa, stockings, coat, and a blank note as the true gift. "
            f"{BOY} holding the idea of a note with quiet understanding. Soft open cream for poem. Tender."
        ),
    },
    {
        "id": "S12-blessing",
        "pages": "28|29",
        "form": "SPREAD",
        "filename": "art-S12-blessing-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "type_zone": "open sky/snow wash for closing stanza",
        "script_text": (
            "He said I've had enough eggnogs, cider and soups. My belt's getting harder to fit in the loops. "
            "And one last thing, please do me a favor. Always love Christmas, act like a kid and pray to your Savior. "
            "God bless."
        ),
        "seed": 900312,
        "scene": (
            f"WIDE seamless SPREAD, NO fake gutter: closing blessing mood — soft snowy night outside the window, "
            f"warm Christmas room, {BOY} feeling peace; distant hint of sleigh/roof magic without hard details. "
            f"Hopeful, sacred-but-gentle Christmas love. Soft open cream for poem. God-bless quiet."
        ),
    },
    {
        "id": "P30-thanks-text",
        "pages": "30",
        "form": "SINGLE",
        "filename": "art-P30-thanks-textplate.png",
        "size": "square_hd",
        "type_zone": "center for Thank You body",
        "script_text": "Thank You (BOOK-COPY-DRAFTS.md)",
        "seed": 900401,
        "scene": (
            "LEFT back-matter TEXT PLATE: soft cream watercolor framed paper, faint holly wash, "
            "large empty center for Thank You typography. Quiet heirloom paper. No busy scene."
        ),
    },
    {
        "id": "P31-portrait",
        "pages": "31",
        "form": "SINGLE",
        "filename": "art-P31-jack-portrait.png",
        "size": "square_hd",
        "type_zone": "minimal caption space lower if needed",
        "script_text": "(Jack / Dad portrait page — companion to Thank You)",
        "seed": 900402,
        "scene": (
            "RIGHT back-matter: warm storybook portrait of a kind middle-aged father/author in a cozy armchair "
            "near a softly lit Christmas tree, gentle smile, heirloom painted gouache portrait mood. "
            "Soft watercolor frame. Calm, loving, gift-book feel."
        ),
    },
    {
        "id": "P32-close",
        "pages": "32",
        "form": "SINGLE",
        "filename": "art-P32-quiet-close.png",
        "size": "square_hd",
        "type_zone": "center for Merry Christmas / quiet close",
        "script_text": "Quiet close / Merry Christmas (soft type later)",
        "seed": 900403,
        "scene": (
            "Final quiet close plate: soft Christmas ornament / candle / tiny tree vignette on cream paper, "
            "lots of calm open wash for a short Merry Christmas line. Peaceful ending. No people."
        ),
    },
]


def fal_headers(json_body: bool = False) -> dict:
    h = {"Authorization": f"Key {KEY}"}
    if json_body:
        h["Content-Type"] = "application/json"
    return h


def build_prompt(scene: str) -> str:
    return f"{scene}\n\n{FRAME}\n\n{D2}\n\n{STYLE_TAIL}"


def generate(plate: dict) -> dict:
    unit_dir = OUT / plate["id"]
    unit_dir.mkdir(parents=True, exist_ok=True)
    out_file = unit_dir / plate["filename"]
    recipe_file = unit_dir / "RECIPE.md"
    prompt = build_prompt(plate["scene"])

    if out_file.is_file() and out_file.stat().st_size > 10_000:
        print(f"SKIP existing {plate['id']}")
        return {"id": plate["id"], "path": str(out_file), "skipped": True}

    body = {
        "prompt": prompt,
        "num_images": 1,
        "output_format": "png",
        "num_inference_steps": 8,
        "enable_safety_checker": True,
        "seed": plate["seed"],
        "image_size": plate["size"],
    }
    print(f"GEN {plate['id']} …")
    req = urllib.request.Request(
        f"https://fal.run/{ENDPOINT}",
        data=json.dumps(body).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                result = json.loads(r.read().decode())
            break
        except urllib.error.HTTPError as e:
            err = e.read().decode(errors="replace")[:800]
            print(f"  HTTP {e.code} attempt {attempt+1}: {err}")
            if attempt == 2:
                raise
            time.sleep(5)
        except Exception as e:
            print(f"  err attempt {attempt+1}: {e}")
            if attempt == 2:
                raise
            time.sleep(5)

    imgs = result.get("images") or []
    if not imgs:
        raise RuntimeError(f"no images for {plate['id']}: {json.dumps(result)[:1200]}")
    url = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
    with urllib.request.urlopen(url) as r:
        out_file.write_bytes(r.read())

    used_seed = result.get("seed", plate["seed"])
    size_s = plate["size"] if isinstance(plate["size"], str) else f"{plate['size']['width']}x{plate['size']['height']}"
    recipe = f"""# RECIPE — new-test-book-v1 / {plate['id']}

| Field | Value |
|-------|--------|
| **name** | {plate['id']} |
| **unit** | new-test-book-v1/{plate['id']} |
| **book page** | {plate['pages']} · {plate['form']} |
| **page role** | `{'spread' if plate['form']=='SPREAD' else 'single' if plate['form']!='COVER' else 'cover'}` |
| **spread side** | `{'wide-master' if plate['form']=='SPREAD' else 'n/a'}` |
| **version** | v1 |
| **date** | {DATE} |
| **lane** | A1 dial (Klein 9B) |
| **service** | fal.ai |
| **model** | `{ENDPOINT}` |
| **settings** | steps 8 · seed {used_seed} · size {size_s} · png |
| **FRAME** | ON |
| **concept** | Full-book dial test — {plate['form']} |
| **changes** | Fresh gen (ignore prior approved locks for this test folder) |
| **size** | {size_s} |
| **seed** | **{used_seed}** |
| **request_id** | n/a |
| **output** | `{plate['filename']}` *(one file only)* |
| **script_text** | {plate['script_text']} |
| **type_zone** | {plate['type_zone']} |
| **verdict** | test-run |
| **status** | working |
| **promoted_to** | — |

## Character / style refs used
- boy / santa: prompt continuity only (no approved locks this test)
- style: Dial D2 + FRAME ON + Santore-adjacent master language

## Prompt

{prompt}

## Negative / constraints
- No letters/glyphs in art · no watermark · no fake gutter on spreads · no Polaroid frame

## Gotchas
- Test dial only — not print finals (Pass B Gemini later)

## Notes
- Soft open washes reserved for Photoshop text-cloud overlays

## Related
- Master map: `../TEXT-IMAGE-MAP.md`
"""
    recipe_file.write_text(recipe, encoding="utf-8")
    print(f"  wrote {out_file.name} ({out_file.stat().st_size} bytes)")
    return {"id": plate["id"], "path": str(out_file), "skipped": False, "seed": used_seed}


def write_maps(results: list[dict]) -> None:
    lines = [
        "# TEXT ↔ IMAGE MAP — new-test-book-v1",
        "",
        f"**Date:** {DATE}  ",
        "**Lane:** A1 Klein 9B + Dial D2 + FRAME ON (fal.ai)  ",
        "**Interior count:** **32 pages** (+ cover front/back)  ",
        "**Purpose:** Full cover-to-cover dial imagination of book flow (not finals).  ",
        "**Roadmap:** `.cursor/docs/BOOK-PAGE-WORKFLOW.md` (trimmed to 32 for this test).",
        "",
        "## How to read",
        "",
        "- **Art file** = one PNG per unit (no duplicates).",
        "- **Script / copy** = what live InDesign type should carry (NOT painted into the PNG).",
        "- **Type zone** = where soft text-cloud / typography should sit in Photoshop / InDesign.",
        "",
        "## Cover",
        "",
        "| Piece | File | Copy / type |",
        "|-------|------|-------------|",
    ]
    for p in PLATES:
        if p["form"] != "COVER":
            continue
        rel = f"{p['id']}/{p['filename']}"
        lines.append(f"| {p['pages']} | `{rel}` | {p['script_text']} |")

    lines += [
        "",
        "## Interior (pages 1–32)",
        "",
        "| Pages | Form | Unit | Art file | Script / copy (for live type) | Type zone |",
        "|------:|------|------|----------|-------------------------------|-----------|",
    ]
    for p in PLATES:
        if p["form"] == "COVER":
            continue
        rel = f"{p['id']}/{p['filename']}"
        script = p["script_text"].replace("|", "/")
        lines.append(
            f"| {p['pages']} | {p['form']} | `{p['id']}` | `{rel}` | {script} | {p['type_zone']} |"
        )

    lines += [
        "",
        "## Spread-first story spine",
        "",
        "S01 approach → S02 threshold → S03 eyes-met → S04 sit-here → S05 chat → S06 cocoa → "
        "**S07 proof tri-panel** → S08 gone → S09 search → S10 note → S11 wish → S12 blessing.",
        "",
        "## Matter pattern",
        "",
        "- Text-heavy lefts use **watercolor text plates** (P02, P04, P30).",
        "- Supporting rights carry vignette / portrait (P05, P31).",
        "- Poem spreads leave **open cream** for Jon’s custom Photoshop text-cloud.",
        "",
        "## Generation results",
        "",
        "| Unit | Status |",
        "|------|--------|",
    ]
    for r in results:
        st = "skipped (already present)" if r.get("skipped") else "generated"
        lines.append(f"| `{r['id']}` | {st} |")

    lines += [
        "",
        "## Cost / next",
        "",
        "- Dial only (~1–2¢ per plate). Promote winners → Lane **B** Gemini finals @ print px.",
        "- Adjust map in BOOK-PAGE-WORKFLOW after Jon reviews flow.",
        "",
    ]
    (OUT / "TEXT-IMAGE-MAP.md").write_text("\n".join(lines), encoding="utf-8")

    index = [
        "# INDEX — new-test-book-v1",
        "",
        "Full Klein 9B dial test book. See **TEXT-IMAGE-MAP.md** for poem/copy pairing.",
        "",
        "| # | Unit | File |",
        "|--:|------|------|",
    ]
    for i, p in enumerate(PLATES, 1):
        index.append(f"| {i} | `{p['id']}` | `{p['id']}/{p['filename']}` |")
    (OUT / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")

    readme = f"""# new-test-book-v1

Cover-to-cover **Klein 9B** dial test (fal.ai) · FRAME ON · Dial D2 · 32 interior pages + covers.

This folder **ignores prior approved locks** on purpose — fresh imagination of full book flow.

| Doc | Role |
|-----|------|
| `TEXT-IMAGE-MAP.md` | Which poem/copy goes with which image + type zones |
| `INDEX.md` | File list |
| `*/RECIPE.md` | Per-plate prompt/seed |

**Not finals.** Next: Jon review → Pass B Gemini remakes for keepers.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for plate in PLATES:
        results.append(generate(plate))
        time.sleep(0.4)
    write_maps(results)
    print(f"DONE — {len(results)} plates · map → {OUT / 'TEXT-IMAGE-MAP.md'}")


if __name__ == "__main__":
    main()
