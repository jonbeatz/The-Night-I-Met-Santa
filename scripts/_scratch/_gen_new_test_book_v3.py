"""
new-test-book-v3 — Qwen Image 2 full dial, more stylized / less photoreal.
Atmosphere north star: Media/approved/style-refs/pages/07-qwen-image-2.png
Character locks: boy-narrator-G0 + santa-G0 (edit refs).
Spine-safe + camera beats. Resumable. One PNG per unit.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image

ROOT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa")
load_dotenv(ROOT / ".env.local")
KEY = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
if not KEY:
    raise SystemExit("FAL_API_KEY missing")

OUT = ROOT / "Media" / "generated" / "new-test-book-v3"
TMP = OUT / "_refs_rgb"
DATE = "2026-07-21"
BATCH = "new-test-book-v3"
T2I = "fal-ai/qwen-image-2/text-to-image"
EDIT = "fal-ai/qwen-image-2/edit"

STYLE_SRC = ROOT / "Media" / "approved" / "style-refs" / "pages" / "07-qwen-image-2.png"
BOY_SRC = ROOT / "Media" / "approved" / "characters" / "boy-narrator-G0.png"
SANTA_SRC = ROOT / "Media" / "approved" / "characters" / "santa-G0.png"
JACK_SRC = ROOT / "Media" / "approved" / "characters" / "jack-farrell-portrait.png"

# Compressed style (T2I) — more artistic than v2, match 07-qwen atmosphere
ATMO = (
    "Match approved style-ref atmosphere: deep cool teal/blue hallway shadows vs brilliant warm "
    "golden fireplace spill, wet-on-wet watercolor walls, soft haze in the lit room, irregular "
    "watercolor paper vignette FRAME ON bleeding into cream paper. Rich opaque gouache + soft watercolor. "
    "VISIBLE brushwork. Storybook illustration — stylized and painterly, NOT photoreal, NOT photo skin, "
    "NOT CGI, NOT hyper-detailed pores. Soft simplified storybook faces with rosy cheeks and gentle features."
)

FRAME = (
    "WATERCOLOR FRAME ON: soft irregular cream vignette, feathered painted edges into open paper, "
    "hand-painted storybook plate. Open cream washes for later typography. No Polaroid, no hard crop."
)

SPINE = (
    "SPINE-SAFE: faces/heads/eyes OFF the center 20–25% width. Characters LEFT and/or RIGHT thirds only. "
    "Center = soft room / gifts / cream wash only. Continuous scene, NO fake gutter line."
)

STYLE_TAIL = (
    "Heirloom children's Christmas picture-book, Charles Santore–adjacent painted gouache, "
    "NO letters, NO glyphs, NO watermark, NOT colored pencil, NOT photoreal photograph."
)

NEG = (
    "photoreal, photograph, photo skin, hyperreal pores, CGI, 3D render, plastic skin, "
    "letters, text, glyphs, watermark, logo, comic hard gutters, fake spine, face on center fold, "
    "colored pencil, crayon"
)

BOY_DESC = (
    "stylized storybook boy matching locked G0: ~7 years, soft messy brown hair, bright blue eyes, "
    "rosy cheeks, gentle painted face (NOT photoreal), oatmeal holly-print pajamas with red trim cuffs"
)
SANTA_DESC = (
    "stylized storybook Santa matching locked G0: kind jolly painted face, rosy cheeks, full white beard, "
    "brilliant white hair, red coat/robe with white fur, brown leather suspenders, home-visit energy "
    "(NOT photoreal Santa)"
)
CAMERA = "vintage handheld film camera silver/black, no brand text, no screen glyphs"


def fal_headers(json_body: bool = False) -> dict:
    h = {"Authorization": f"Key {KEY}"}
    if json_body:
        h["Content-Type"] = "application/json"
    return h


def to_rgb_png(src: Path, dest: Path) -> Path:
    """Qwen edit rejects alpha — flatten onto cream."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (245, 240, 230, 255))
        bg.alpha_composite(rgba)
        bg.convert("RGB").save(dest, "PNG")
    else:
        im.convert("RGB").save(dest, "PNG")
    return dest


def upload(path: Path) -> str:
    req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        data=json.dumps({"file_name": path.name, "content_type": "image/png"}).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        meta = json.loads(r.read().decode())
    put = urllib.request.Request(
        meta["upload_url"],
        data=path.read_bytes(),
        method="PUT",
        headers={"Content-Type": "image/png"},
    )
    with urllib.request.urlopen(put, timeout=180) as r:
        if r.status not in (200, 201):
            raise RuntimeError(f"PUT {r.status}")
    return meta["file_url"]


def fal_run(endpoint: str, body: dict) -> dict:
    req = urllib.request.Request(
        f"https://fal.run/{endpoint}",
        data=json.dumps(body).encode(),
        headers=fal_headers(True),
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            err = e.read().decode(errors="replace")[:900]
            print(f"  HTTP {e.code} attempt {attempt+1}: {err}")
            if attempt == 2:
                raise
            time.sleep(6)
        except Exception as e:
            print(f"  err attempt {attempt+1}: {e}")
            if attempt == 2:
                raise
            time.sleep(6)
    raise RuntimeError("unreachable")


def trunc800(s: str) -> str:
    s = " ".join(s.split())
    return s if len(s) <= 800 else s[:797] + "…"


# mode: t2i | edit-boy | edit-both | edit-jack | edit-style
PLATES: list[dict] = [
    {
        "id": "cover-front",
        "pages": "cover-front",
        "form": "COVER",
        "filename": "art-cover-front.png",
        "size": "square_hd",
        "mode": "edit-boy",
        "type_zone": "upper/mid cream for title type",
        "script_text": "The Night I Met Santa · Jack Farrell (cover type later)",
        "seed": 920101,
        "scene_short": (
            f"Square cover: {BOY_DESC} peeking from dark cool hallway into warm gold Christmas room "
            f"(tree + fire glow). Santa face HIDDEN. Soft open cream for title. Magical hush."
        ),
        "scene_t2i": "",  # unused when edit
    },
    {
        "id": "cover-back",
        "pages": "cover-back",
        "form": "COVER",
        "filename": "art-cover-back.png",
        "size": "square_hd",
        "mode": "edit-style",
        "type_zone": "center/lower for blurb",
        "script_text": "Back blurb + Illustrated edition designed by Jon Farrell · 2026",
        "seed": 920102,
        "scene_short": (
            "Square back cover: quiet snowy night path or soft ember vignette, large calm cream wash "
            "for blurb. Tiny holly at edges. No faces. Painterly watercolor FRAME ON."
        ),
    },
    {
        "id": "P01-title",
        "pages": "1",
        "form": "SINGLE",
        "filename": "art-P01-title.png",
        "size": "square_hd",
        "mode": "edit-style",
        "type_zone": "UPPER cream open wash",
        "script_text": "The Night I Met Santa · Jack Farrell",
        "seed": 920201,
        "scene_short": (
            "Title plate: fireplace LEFT, Christmas tree RIGHT, scenery LOWER, generous empty cream "
            "TOP for title. No people. Soft wet watercolor, warm glow. FRAME ON."
        ),
    },
    {
        "id": "P02-copyright",
        "pages": "2",
        "form": "SINGLE",
        "filename": "art-P02-copyright-textplate.png",
        "size": "square_hd",
        "mode": "t2i",
        "type_zone": "center (quiet type plate)",
        "script_text": "First illustrated edition, 2026. / Written by Jack Farrell. / Book design by Jon Farrell.",
        "seed": 920202,
        "scene_short": "",
        "scene_t2i": (
            "TEXT-ONLY storybook plate: cream watercolor paper, delicate painted vignette frame, "
            "tiny holly corners only, large empty center for copyright type. Quiet heirloom paper. No people."
        ),
    },
    {
        "id": "P03-dedication",
        "pages": "3",
        "form": "SINGLE",
        "filename": "art-P03-dedication.png",
        "size": "square_hd",
        "mode": "edit-style",
        "type_zone": "center / lower-center soft wash",
        "script_text": "For my family, with love. — Jack Farrell",
        "seed": 920203,
        "scene_short": (
            "Dedication: sparse soft hearth embers vignette, large calm cream center for dedication type. "
            "No people. Dreamy quiet paint."
        ),
    },
    {
        "id": "P04-about-text",
        "pages": "4",
        "form": "SINGLE",
        "filename": "art-P04-about-textplate.png",
        "size": "square_hd",
        "mode": "t2i",
        "type_zone": "full soft center for About body",
        "script_text": "About This Story + Draft A body (BOOK-COPY-DRAFTS.md)",
        "seed": 920204,
        "scene_t2i": (
            "LEFT matter TEXT PLATE: soft cream watercolor framed paper, faint warm wash, tiny pine at edges, "
            "large empty center for About paragraphs. No middle scene. Quiet heirloom paper."
        ),
    },
    {
        "id": "P05-about-art",
        "pages": "5",
        "form": "SINGLE",
        "filename": "art-P05-about-vignette.png",
        "size": "square_hd",
        "mode": "edit-style",
        "type_zone": "minimal — supporting image page",
        "script_text": "(little or no type — companion to About)",
        "seed": 920205,
        "scene_short": (
            "Quiet Christmas Eve vignette: snowy window, soft tree glow, empty gift room hush. "
            "No people. Painterly wet watercolor FRAME ON."
        ),
    },
    {
        "id": "S01-approach",
        "pages": "6|7",
        "form": "SPREAD",
        "filename": "art-S01-approach-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-boy",
        "type_zone": "soft open cloud zones L and/or lower for poem stanza",
        "script_text": (
            "I searched and I peeked when I first heard the noise. "
            "Something or someone was in with the toys. "
            "I slithered and crawled for a peek of a glimpse. "
            "It must be some fairies or holiday imps."
        ),
        "seed": 920301,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: {BOY_DESC} crawling/peeking in cool teal hallway. "
            f"RIGHT: warm gold living-room doorway with toys/tree light. CENTER: empty floor/cream. "
            f"Strong cool/warm contrast like style-ref."
        ),
    },
    {
        "id": "S02-threshold",
        "pages": "8|9",
        "form": "SPREAD",
        "filename": "art-S02-threshold-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-boy",
        "type_zone": "open wash near door / lower for stanza",
        "script_text": (
            "I got up the nerve to go to the door, a door that was decorated, bolted and locked. "
            "I didn't know it when I entered the room to surprise the amazement or even the shock. "
            "Now I'm usually calm, not very loud, or even known to be a ranter. "
            "But what do you say when you sneak up on Santa?"
        ),
        "seed": 920302,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: decorated door + {BOY_DESC} at threshold. "
            f"RIGHT: warm room, hint of red coat only (Santa face HIDDEN). CENTER: doorframe/floor. Nerves+wonder."
        ),
    },
    {
        "id": "S03-eyes-met",
        "pages": "10|11",
        "form": "SPREAD",
        "filename": "art-S03-eyes-met-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-both",
        "type_zone": "lower or side soft wash for stanza",
        "script_text": (
            "My jaw dropped when our eyes finally met. I knew right then, it was a moment I would never forget. "
            "For there he was in all his splendor, brilliant white hair, red coat with suspenders."
        ),
        "seed": 920303,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT third: {BOY_DESC} jaw-dropped wonder. "
            f"RIGHT third: {SANTA_DESC} in splendor by tree. CENTER: fireplace/gifts/cream — NO faces. "
            f"Stylized painted faces only."
        ),
    },
    {
        "id": "S04-sit-here",
        "pages": "12|13",
        "form": "SPREAD",
        "filename": "art-S04-sit-here-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-both",
        "type_zone": "open among gifts / lower for dialogue stanza",
        "script_text": (
            "He was down on the floor between boxes, gifts and ribbons galore. "
            "I couldn't move, I stayed very still. Finally he whispered, \"Sit over here. Have a moment to kill.\""
        ),
        "seed": 920304,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: hesitant {BOY_DESC}. RIGHT: {SANTA_DESC} sitting among gifts inviting him. "
            f"CENTER: ribbons/boxes/cream. Intimate painted storybook."
        ),
    },
    {
        "id": "S05-chat",
        "pages": "14|15",
        "form": "SPREAD",
        "filename": "art-S05-chat-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-both",
        "type_zone": "side/lower open wash",
        "script_text": (
            "Oh, what a feeling, such a thrill. We chatted and laughed what seemed like an hour. "
            "But with laughs, stories and chatter, who cares, it didn't much matter."
        ),
        "seed": 920305,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: laughing {BOY_DESC}. RIGHT: warm chatting {SANTA_DESC}. "
            f"CENTER: gift pile/rug/cream. Soft joyful paint, not photo."
        ),
    },
    {
        "id": "S06-cocoa",
        "pages": "16|17",
        "form": "SPREAD",
        "filename": "art-S06-cocoa-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-both",
        "type_zone": "open near cups / lower",
        "script_text": (
            "He spoke of many places, people and things. From toys to music to bright diamond rings. "
            "Coats made of wool, ties made of silk. He even revealed his passion for hot cocoa instead of cold milk."
        ),
        "seed": 920306,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: {BOY_DESC} with steaming cocoa. RIGHT: {SANTA_DESC} with cocoa storytelling. "
            f"CENTER: tray/steam/cream. Warm rich gouache."
        ),
    },
    {
        "id": "S07-proof-camera",
        "pages": "18|19",
        "form": "SPREAD",
        "filename": "art-S07-proof-camera-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-boy",
        "type_zone": "soft bands between three moments for stanza",
        "script_text": (
            "When I heard all the noise up in the roof, it hit me right then. I needed some proof. "
            "Where can I go? What can I get? I know, a photo. That's my best bet."
        ),
        "seed": 920307,
        "scene_short": (
            f"Wide spread as THREE soft vignette blooms (not hard comics). {SPINE} "
            f"LEFT: {BOY_DESC} looking UP at roof noise. CENTER: cream/empty room air only. "
            f"RIGHT: same boy grabbing {CAMERA}. No faces in center. No baked letters."
        ),
    },
    {
        "id": "S08-gone-camera",
        "pages": "20|21",
        "form": "SPREAD",
        "filename": "art-S08-gone-camera-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-boy",
        "type_zone": "open empty floor zone for stanza",
        "script_text": (
            "I flew out the door and was back in a flash. But oh no, the hour had already passed. "
            "And from the noise on top of the roof I realized that I was still without proof."
        ),
        "seed": 920308,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: {BOY_DESC} rushing back holding {CAMERA}. "
            f"RIGHT: empty spot where Santa sat, gifts remain, soft tree glow. CENTER: empty floor/cream. "
            f"Camera but no proof. Lonely wonder."
        ),
    },
    {
        "id": "S09-search",
        "pages": "22|23",
        "form": "SPREAD",
        "filename": "art-S09-search-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-boy",
        "type_zone": "open near chair / flue for stanza",
        "script_text": (
            "I turned around slowly. I needed to know, did he leave me a hint, a tip or a clue? "
            "Did he forget his hat or maybe a shoe? Now what am I supposed to do? "
            "I know, I'll look up the flue. I dashed to the flue but nothing was there. "
            "I looked over here and I looked over there. When I saw something on top of the chair, "
            "my proof I thought was just laying right there."
        ),
        "seed": 920309,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: {BOY_DESC} peeking up fireplace flue (camera aside on table). "
            f"RIGHT: noticing something on a chair. CENTER: flue/floor/cream. Soft detective wonder."
        ),
    },
    {
        "id": "S10-note",
        "pages": "24|25",
        "form": "SPREAD",
        "filename": "art-S10-note-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-boy",
        "type_zone": "open around note / lower for stanza",
        "script_text": (
            "It wasn't a shoe, hat or a coat. I couldn't believe it, the old guy. He left me a note. "
            "I fell on the chair and started to stare. What it said, I didn't care. "
            "I tore open the note that Santa had wrote. The words jumped out as to get my attention. "
            "And there was one thing he told me to mention."
        ),
        "seed": 920310,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: {BOY_DESC} on chair with blank folded note (NO readable letters painted). "
            f"RIGHT: warm lamp/tree. CENTER: cream/chair fabric. Emotional discovery, stylized paint."
        ),
    },
    {
        "id": "S11-wish",
        "pages": "26|27",
        "form": "SPREAD",
        "filename": "art-S11-wish-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-boy",
        "type_zone": "generous open wash for list stanza",
        "script_text": (
            "More than cakes, cocoa or milk. Shirts made of cotton or ties made of silk. "
            "Hats, stockings or a new coat. What he wants is simply a note."
        ),
        "seed": 920311,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: soft still-life cocoa/stockings/coat (no faces). "
            f"RIGHT: {BOY_DESC} holding blank note with quiet understanding. CENTER: generous cream wash."
        ),
    },
    {
        "id": "S12-blessing",
        "pages": "28|29",
        "form": "SPREAD",
        "filename": "art-S12-blessing-SPREAD.png",
        "size": {"width": 1536, "height": 768},
        "mode": "edit-boy",
        "type_zone": "open sky/snow wash for closing stanza",
        "script_text": (
            "He said I've had enough eggnogs, cider and soups. My belt's getting harder to fit in the loops. "
            "And one last thing, please do me a favor. Always love Christmas, act like a kid and pray to your Savior. "
            "God bless."
        ),
        "seed": 920312,
        "scene_short": (
            f"Wide spread. {SPINE} LEFT: peaceful {BOY_DESC} by warm Christmas window. "
            f"RIGHT: soft snowy night, distant sleigh/roof hint. CENTER: snow/cream sky. Gentle blessing mood."
        ),
    },
    {
        "id": "P30-thanks-text",
        "pages": "30",
        "form": "SINGLE",
        "filename": "art-P30-thanks-textplate.png",
        "size": "square_hd",
        "mode": "t2i",
        "type_zone": "center for Thank You body",
        "script_text": "Thank You (BOOK-COPY-DRAFTS.md)",
        "seed": 920401,
        "scene_t2i": (
            "LEFT back-matter TEXT PLATE: soft cream watercolor framed paper, faint holly wash, "
            "large empty center for Thank You type. Quiet heirloom paper. No busy scene."
        ),
    },
    {
        "id": "P31-portrait",
        "pages": "31",
        "form": "SINGLE",
        "filename": "art-P31-jack-portrait.png",
        "size": "square_hd",
        "mode": "edit-jack",
        "type_zone": "minimal caption space lower if needed",
        "script_text": "(Jack / Dad portrait page — companion to Thank You)",
        "seed": 920402,
        "scene_short": (
            "Warm storybook author portrait matching image 2 likeness, painted gouache like image 1 atmosphere, "
            "cozy armchair near soft Christmas tree, gentle smile, stylized NOT photoreal. Soft watercolor FRAME ON."
        ),
    },
    {
        "id": "P32-close",
        "pages": "32",
        "form": "SINGLE",
        "filename": "art-P32-quiet-close.png",
        "size": "square_hd",
        "mode": "edit-style",
        "type_zone": "center for Merry Christmas / quiet close",
        "script_text": "Quiet close / Merry Christmas (soft type later)",
        "seed": 920403,
        "scene_short": (
            "Final quiet close: soft ornament/candle/tiny tree vignette on cream, lots of open wash "
            "for Merry Christmas line. Peaceful. No people. No letters."
        ),
    },
]


def build_edit_prompt(plate: dict, mode: str) -> str:
    base = (
        "Paint a NEW Christmas children's-book illustration matching image 1 atmosphere "
        "(cool teal shadows vs warm gold fire spill, wet watercolor, FRAME ON vignette). "
    )
    if mode == "edit-boy":
        base += (
            "Character MUST match image 2 boy design — stylized painted storybook face, blue eyes, "
            "rosy cheeks, holly pajamas; NOT photoreal. "
        )
    elif mode == "edit-both":
        base += (
            "Boy MUST match image 2 (stylized painted face, blue eyes, holly PJs). "
            "Santa MUST match image 3 (stylized kind face, suspenders, red coat); NOT photoreal. "
        )
    elif mode == "edit-jack":
        base += "Portrait likeness from image 2, paint style of image 1; stylized gouache NOT photo. "
    elif mode == "edit-style":
        base += "Same paint language as image 1. "

    base += plate["scene_short"] + " Soft open cream for typography. NO letters/glyphs in art."
    return trunc800(base)


def build_t2i_prompt(plate: dict) -> str:
    return "\n\n".join(
        [
            plate.get("scene_t2i") or plate.get("scene_short") or "",
            ATMO,
            FRAME,
            STYLE_TAIL,
        ]
    )


def generate(plate: dict, urls: dict[str, str]) -> dict:
    unit_dir = OUT / plate["id"]
    unit_dir.mkdir(parents=True, exist_ok=True)
    out_file = unit_dir / plate["filename"]
    recipe_file = unit_dir / "RECIPE.md"

    if out_file.is_file() and out_file.stat().st_size > 10_000:
        print(f"SKIP existing {plate['id']}")
        return {"id": plate["id"], "path": str(out_file), "skipped": True}

    mode = plate["mode"]
    print(f"GEN {plate['id']} ({mode}) …")

    if mode == "t2i":
        prompt = build_t2i_prompt(plate)
        endpoint = T2I
        body = {
            "prompt": prompt,
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checker": True,
            "enable_prompt_expansion": False,
            "negative_prompt": NEG[:500],
            "seed": plate["seed"],
            "image_size": plate["size"],
        }
        ref_note = "none (T2I)"
    else:
        prompt = build_edit_prompt(plate, mode)
        endpoint = EDIT
        if mode == "edit-boy":
            image_urls = [urls["style"], urls["boy"]]
        elif mode == "edit-both":
            image_urls = [urls["style"], urls["boy"], urls["santa"]]
        elif mode == "edit-jack":
            image_urls = [urls["style"], urls["jack"]]
        else:  # edit-style
            image_urls = [urls["style"]]
        body = {
            "prompt": prompt,
            "image_urls": image_urls,
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checker": True,
            "enable_prompt_expansion": False,
            "negative_prompt": NEG[:500],
            "seed": plate["seed"],
            "image_size": plate["size"],
        }
        ref_note = ", ".join(image_urls)

    result = fal_run(endpoint, body)
    imgs = result.get("images") or []
    if not imgs:
        raise RuntimeError(f"no images for {plate['id']}: {json.dumps(result)[:1200]}")
    url = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
    with urllib.request.urlopen(url, timeout=180) as r:
        out_file.write_bytes(r.read())

    used_seed = result.get("seed", plate["seed"])
    size_s = plate["size"] if isinstance(plate["size"], str) else f"{plate['size']['width']}x{plate['size']['height']}"
    role = "spread" if plate["form"] == "SPREAD" else "single" if plate["form"] != "COVER" else "cover"
    recipe = f"""# RECIPE — {BATCH} / {plate['id']}

| Field | Value |
|-------|--------|
| **name** | {plate['id']} |
| **unit** | {BATCH}/{plate['id']} |
| **book page** | {plate['pages']} · {plate['form']} |
| **page role** | `{role}` |
| **spread side** | `{'wide-master' if plate['form']=='SPREAD' else 'n/a'}` |
| **version** | v1 |
| **date** | {DATE} |
| **lane** | A2 dial stylized (Qwen Image 2) |
| **service** | fal.ai |
| **model** | `{endpoint}` |
| **settings** | seed {used_seed} · size {size_s} · png · prompt_expansion off · mode {mode} |
| **FRAME** | ON |
| **concept** | Stylized full-book dial — G0 chars + 07-qwen atmosphere |
| **changes** | Less photoreal vs v2; character/style edit refs; new seeds |
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
- style-ref: `Media/approved/style-refs/pages/07-qwen-image-2.png`
- boy: `Media/approved/characters/boy-narrator-G0.png`
- santa: `Media/approved/characters/santa-G0.png`
- uploaded: {ref_note}

## Prompt

{prompt}

## Negative / constraints
- {NEG}

## Gotchas
- Dial only — Pass B Gemini for print finals
- Edit prompts capped ~800 chars (Qwen edit)

## Notes
- Spine-safe · camera beats · anti-photoreal

## Related
- Master map: `../TEXT-IMAGE-MAP.md`
- Compare: `../new-test-book-v1/` (Klein) · `../new-test-book-v2/` (Qwen raw)
"""
    recipe_file.write_text(recipe, encoding="utf-8")
    print(f"  wrote {out_file.name} ({out_file.stat().st_size} bytes)")
    return {"id": plate["id"], "path": str(out_file), "skipped": False, "seed": used_seed}


def write_maps(results: list[dict]) -> None:
    status = {r["id"]: ("skipped" if r.get("skipped") else "generated") for r in results}
    lines = [
        f"# TEXT ↔ IMAGE MAP — {BATCH}",
        "",
        f"**Date:** {DATE}  ",
        "**Lane:** A2 Qwen Image 2 **stylized** (edit + T2I) + FRAME ON  ",
        "**Atmosphere:** `Media/approved/style-refs/pages/07-qwen-image-2.png`  ",
        "**Characters:** boy-narrator-G0 · santa-G0 (edit refs)  ",
        "**Goal:** Less photoreal than v2 · more painted storybook · spine-safe · camera beats  ",
        "**Interior:** **32 pages** (+ covers)",
        "",
        "## How to read",
        "",
        "- One PNG per unit · live type in InDesign/PS (not baked).",
        "- Spreads keep faces off the center fold.",
        "",
        "## Cover",
        "",
        "| Piece | File | Copy / type |",
        "|-------|------|-------------|",
        "| cover-front | `cover-front/art-cover-front.png` | The Night I Met Santa · Jack Farrell |",
        "| cover-back | `cover-back/art-cover-back.png` | Back blurb + Jon Farrell · 2026 |",
        "",
        "## Interior (pages 1–32)",
        "",
        "| Pages | Form | Unit | Art file | Script / copy | Type zone |",
        "|------:|------|------|----------|---------------|-----------|",
    ]
    for p in PLATES:
        if p["form"] == "COVER":
            continue
        lines.append(
            f"| {p['pages']} | {p['form']} | `{p['id']}` | `{p['id']}/{p['filename']}` | "
            f"{p['script_text']} | {p['type_zone']} |"
        )
    lines += [
        "",
        "## Story spine",
        "",
        "S01 → S02 → S03 eyes-met → S04 → S05 → S06 → **S07 camera** → **S08 gone+camera** → "
        "S09 → S10 note → S11 → S12 blessing.",
        "",
        "## Generation results",
        "",
        "| Unit | Mode | Status |",
        "|------|------|--------|",
    ]
    for p in PLATES:
        lines.append(f"| `{p['id']}` | {p['mode']} | {status.get(p['id'], 'pending')} |")
    lines += [
        "",
        "## Next",
        "",
        "- Compare v1 Klein · v2 Qwen · **v3 stylized**.",
        "- Promote keepers → Lane B Gemini @ print px.",
        "",
    ]
    (OUT / "TEXT-IMAGE-MAP.md").write_text("\n".join(lines), encoding="utf-8")

    idx = [f"# INDEX — {BATCH}", "", "| # | Unit | File | Mode |", "|--:|------|------|------|"]
    for i, p in enumerate(PLATES, 1):
        idx.append(f"| {i} | `{p['id']}` | `{p['id']}/{p['filename']}` | {p['mode']} |")
    (OUT / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")

    (OUT / "README.md").write_text(
        f"""# {BATCH}

**Qwen Image 2** stylized full-book dial — atmosphere from `07-qwen-image-2.png`, characters from
`boy-narrator-G0` / `santa-G0` via edit refs. Less photoreal than v2.

| Doc | Role |
|-----|------|
| `TEXT-IMAGE-MAP.md` | Poem/copy ↔ image |
| `INDEX.md` | File list |
| `*/RECIPE.md` | Per-plate prompt/seed |

Resume: delete a unit’s `art-*.png`, then `python scripts\\_scratch\\_gen_new_test_book_v3.py`
""",
        encoding="utf-8",
    )
    print(f"maps → {OUT / 'TEXT-IMAGE-MAP.md'}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for src in (STYLE_SRC, BOY_SRC, SANTA_SRC, JACK_SRC):
        if not src.is_file():
            raise SystemExit(f"missing ref: {src}")

    print("flatten + upload refs…")
    style_p = to_rgb_png(STYLE_SRC, TMP / "style-07-qwen.png")
    boy_p = to_rgb_png(BOY_SRC, TMP / "boy-G0.png")
    santa_p = to_rgb_png(SANTA_SRC, TMP / "santa-G0.png")
    jack_p = to_rgb_png(JACK_SRC, TMP / "jack-portrait.png")
    urls = {
        "style": upload(style_p),
        "boy": upload(boy_p),
        "santa": upload(santa_p),
        "jack": upload(jack_p),
    }
    for k, u in urls.items():
        print(f"  {k}: {u[:80]}…")

    results = [generate(p, urls) for p in PLATES]
    write_maps(results)
    print(f"DONE — {len(results)} plates · {OUT}")


if __name__ == "__main__":
    main()
