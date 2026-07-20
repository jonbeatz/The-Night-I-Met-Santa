#!/usr/bin/env python3
"""Generate test-batch-v3: full 32-page art pass synced to poem-clean.txt.

Uses fal nano-banana-pro/edit + painted gouache style refs.
Outputs Media/generated/test-batch-v3/
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

# Unbuffered progress on Windows / piped Tee
try:
    sys.stdout.reconfigure(line_buffering=True)  # type: ignore[attr-defined]
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Media" / "generated" / "test-batch-v3"
SPREADS = OUT / "spreads"
REFS = OUT / "_style-refs" / "fal-urls.json"

STYLE = (
    "Traditional children's Christmas picture-book illustration, heavily painted "
    "heirloom gouache and soft watercolor, visible soft brushstrokes and gentle "
    "blended edges, NOT colored pencil NOT crayon NOT scratchy sketch, warm "
    "fireplace glow mixed with cool moonlight, deep crimson and forest green, "
    "Charles Santore–inspired Golden Age storybook, NOT photoreal, NOT CGI, "
    "no text, no letters, no watermark"
)

# Required on every wide/spread gen (Jon 2026-07-20 — no fake gutter on print art)
SPREAD_ADDON = (
    "seamless continuous two-page storybook spread across the full width, one "
    "unbroken painted scene through the center, NO fake book gutter, NO vertical "
    "fold line, NO center spine shadow, NO page-split seam, NO mockup binding "
    "crease down the middle"
)

SPREAD_NEGATIVES = (
    "fake book gutter, vertical fold line, center spine shadow, page crease, "
    "binding seam, mockup book fold, split-page line, gutter shadow overlay, "
    "text, letters, watermark, photoreal, CGI, colored pencil"
)

CONTINUITY = (
    "Continuous character lock: same young boy with brown hair in soft light-blue "
    "or lightly patterned pajamas; same Santa — brilliant soft-painted white beard, "
    "kind eyes, red coat WITH clear red suspenders (or burgundy robe over striped "
    "pajamas with suspenders for at-home scenes), same cozy Christmas Eve living "
    "room with stone fireplace, stockings, glowing tree, wrapped gifts. "
)

QUIET = "Leave soft quiet negative space for later poem text overlay (not white box)."


def load_env():
    env = ROOT / ".env.local"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
    if os.environ.get("FAL_API_KEY") and not os.environ.get("FAL_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


def urls():
    data = json.loads(REFS.read_text(encoding="utf-8"))
    return [data["spread"], data["sneak"], data["santa"]]


def download(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "tnims-v3/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        dest.write_bytes(r.read())


def gen(prompt: str, image_urls: list[str], aspect: str = "1:1") -> str:
    import fal_client

    full = f"{CONTINUITY}{prompt} {QUIET} {STYLE}"
    if aspect in ("21:9", "16:9", "2:1") or "SPREAD" in prompt.upper() or "spread" in prompt.lower()[:20]:
        full = f"{full} {SPREAD_ADDON}"
    result = fal_client.subscribe(
        "fal-ai/nano-banana-pro/edit",
        arguments={
            "prompt": full,
            "image_urls": image_urls,
            "resolution": "2K",
            "aspect_ratio": aspect,
            "output_format": "png",
            "num_images": 1,
            "limit_generations": True,
        },
    )
    return result["images"][0]["url"]


def split_spread(wide_path: Path, left: Path, right: Path, master: Path):
    from PIL import Image

    im = Image.open(wide_path).convert("RGB")
    # Normalize to 5250x2625 then split
    target = (5250, 2625)
    # Cover-fit into target
    scale = max(target[0] / im.width, target[1] / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    left0 = (nw - target[0]) // 2
    top0 = (nh - target[1]) // 2
    im = im.crop((left0, top0, left0 + target[0], top0 + target[1]))
    im.save(master, "PNG")
    im.crop((0, 0, 2625, 2625)).save(left, "PNG")
    im.crop((2625, 0, 5250, 2625)).save(right, "PNG")


# 32-page book order — unique art jobs keyed by stem
# Spreads produce LEFT/RIGHT page files
JOBS = [
    # Front matter
    ("p01-title", "1:1",
     "Interior TITLE PAGE art for a children's Christmas picture book, flat square poster, "
     "magical Christmas Eve living room with glowing tree and soft fireplace, empty soft "
     "upper sky/wall area for title later, cozy heirloom wonder, no people or tiny distant "
     "figures only, NO letters"),
    ("p02-half-title", "1:1",
     "Quiet half-title vignette, soft painted Christmas ornament — holly, pinecone, and "
     "ribbon on warm cream-shadow background, lots of soft empty space for a short title "
     "line later, gentle storybook, NO letters"),
    ("p03-copyright", "1:1",
     "Very quiet Christmas night field of soft falling snow and distant warm window glow, "
     "minimal detail, large soft empty space for small copyright text later, peaceful, NO letters"),
    ("p04-dedication", "1:1",
     "Soft dedication vignette: empty wooden chair by a glowing Christmas tree with a tiny "
     "blank note card (no readable writing), warm hearth light, quiet center for dedication "
     "text later, tender mood, NO letters"),
    ("p05-about-story", "1:1",
     "About-this-story page art: cozy snowy Christmas Eve window seat and fireplace study, "
     "wrapped gifts soft in corner, large gentle quiet cream wall region for longer prose "
     "later, intimate bookish Christmas mood, NO letters"),
    ("p06-about-author", "1:1",
     "About-the-author page art: warm writing desk by a frosted window at night, fountain "
     "pen and blank paper (no readable writing), soft lamp glow, Christmas tree softly in "
     "background, quiet lower/side space for prose, NO letters"),
    # Story beats
    ("p07-beat01-the-sneak", "1:1",
     "Beat 1 matching poem: Christmas Eve night, curious young boy in pajamas crouching "
     "and peeking from a dim hallway toward a glowing living room doorway, toys and gift "
     "wrap faintly visible beyond, magical hush anticipation, quiet lower-left for text"),
    ("p08-beat02-the-door", "1:1",
     "Beat 2 matching poem: decorated Christmas Eve door with wreath and red bow, old bolt "
     "and lock, warm golden light spilling under the door into darker hallway, child's hand "
     "reaching toward the knob, quiet upper-right for text"),
    ("p09-beat03-sneak-up", "1:1",
     "Beat 3 matching poem: child just inside Christmas living room sneaking forward among "
     "gifts, surprised frozen posture, Santa Claus HALF-SEEN ahead among boxes and ribbons "
     "(not full face yet), tree lights fireplace glow, quiet lower band for text"),
    ("spread-eyes-met", "21:9",
     "SPREAD Beat 4 matching poem: wide cinematic two-page Christmas storybook spread, "
     "child and Santa meeting eyes for the first time, jaw-dropped wonder, Santa in all "
     "his splendor brilliant white hair and beard, red coat WITH suspenders clearly "
     "visible, gifts ribbons boxes on living room floor, fireplace left tree right, "
     "seamless continuous scene across full width NO fake gutter or center fold line, "
     "quiet outer corners for text"),
    ("spread-sit-here", "21:9",
     "SPREAD Beat 5 matching poem: wide cinematic living-room spread, Santa sitting on "
     "the floor among boxes gifts and ribbons galore, kindly gesturing to open spot "
     "inviting child to sit, child still in awe nearby, seamless continuous across "
     "center NO fake fold line, quiet side panels for dialogue text"),
    ("spread-chat-laugh", "21:9",
     "SPREAD Beat 6 matching poem: wide cozy two-page spread, Santa and child sitting "
     "together among Christmas gifts chatting and laughing warmly, animated friendly "
     "conversation, tree lights and fireplace glow, seamless continuous scene NO fake "
     "gutter, quiet bands for poem text"),
    ("p16-beat07-cocoa", "1:1",
     "Beat 7 matching poem: Santa holding steaming mug of hot cocoa beside Christmas tree, "
     "storytelling gesture about places people toys music diamond rings, child listening "
     "nearby, soft steam, passion for cocoa instead of milk, quiet top-left for text"),
    ("p17-beat08-need-proof", "1:1",
     "Beat 8 matching poem: child looking upward startled by noise on the roof, Christmas "
     "living room night, realizing he needs proof, idea of a photo forming, slight urgency, "
     "Santa still nearby, quiet bottom for text"),
    ("p18-beat09-santa-gone", "1:1",
     "Beat 9 matching poem: child rushing back into Christmas living room holding a vintage "
     "camera, Santa has vanished, empty spot among gifts, disappointment urgency, roof noise "
     "suggested, quiet upper area for text"),
    ("p19-beat10-the-search", "1:1",
     "Beat 10 matching poem: child searching Christmas living room for a clue Santa left — "
     "hat or shoe — looking under ribbons around tree and gifts, worried curious expression, "
     "quiet bottom for text"),
    ("p20-beat11-flue-chair", "1:1",
     "Beat 11 matching poem: Christmas living room, child looking up dark chimney flue then "
     "noticing something small on seat of old wooden chair, dying fire glow soft moonlight, "
     "mystery and hope, quiet corner for text"),
    ("spread-the-note", "21:9",
     "SPREAD Beats 12–13 matching poem: wide cinematic climax spread, child on or beside "
     "old wooden chair discovering and tearing open small blank note from Santa (no readable "
     "writing), wonder and focus on the note, tree soft in background, seamless continuous "
     "across center NO fake gutter or fold line, quiet outer edges for poem text"),
    ("p23-beat14-what-he-wants", "1:1",
     "Beat 14 matching poem: child reading Santa's note by Christmas tree light, soft glow "
     "on paper (no readable letters), peaceful revelation Santa wants a simple note more "
     "than cakes cocoa milk gifts, quiet top for text"),
    ("spread-closing-blessing", "21:9",
     "SPREAD Beat 15 matching poem: wide heartfelt closing blessing spread, warm magical "
     "living room after Santa's visit, child holding note near glowing tree and fireplace, "
     "soft snow light at window, mood of always love Christmas act like a kid pray to your "
     "Savior, seamless continuous across center NO fake gutter, quiet bands for final poem "
     "lines, no readable note text"),
    ("p26-god-bless", "1:1",
     "Closing 'God bless' vignette page: soft painted Christmas night window with gentle "
     "snowfall and distant star, warm interior glow, peaceful sacred cozy mood, large quiet "
     "center for short closing words later, NO letters"),
    ("p27-thank-you", "1:1",
     "Thank You page art: warm family Christmas hearth with stockings and soft gifts, "
     "empty cozy chairs suggesting loved ones, generous quiet cream wall/floor region for "
     "thank-you prose later, heartfelt, NO letters"),
    ("p28-family-hearth", "1:1",
     "Companion thank-you spread mood as single: soft painted Christmas living room empty "
     "but warm after the story, tree lights low, quiet snow outside window, large soft empty "
     "space for optional second thank-you panel text, NO letters"),
    ("p29-author-portrait", "1:1",
     "Author reprise page art: gentle vignette of an older kind gentleman by fireplace in "
     "soft painted storybook style (not photoreal portrait), Christmas tree glow, quiet "
     "space for 'Written by Jack Farrell' later, warm, NO letters on image"),
    ("p30-writing-desk", "1:1",
     "Quiet writing-desk Christmas Eve scene, blank paper and pen (no readable writing), "
     "soft lamp, frosted window snow, quiet space for short colophon, NO letters"),
    ("p31-quiet-ornament", "1:1",
     "Quiet end ornament page: painted holly sprig, red ribbon, and soft candle glow on "
     "warm cream background, lots of empty soft space, NO letters"),
    ("p32-merry-christmas", "1:1",
     "Final leaf art: magical quiet Christmas morning light through curtains onto empty "
     "living room with tree and leftover ribbons, hopeful peaceful ending, soft quiet band "
     "for 'Merry Christmas' later, NO letters"),
]

SPREAD_PAGE_MAP = {
    "spread-eyes-met": ("p10-beat04-eyes-met-LEFT", "p11-beat04-eyes-met-RIGHT"),
    "spread-sit-here": ("p12-beat05-sit-here-LEFT", "p13-beat05-sit-here-RIGHT"),
    "spread-chat-laugh": ("p14-beat06-chat-laugh-LEFT", "p15-beat06-chat-laugh-RIGHT"),
    "spread-the-note": ("p21-beat12-13-note-LEFT", "p22-beat12-13-note-RIGHT"),
    "spread-closing-blessing": ("p24-beat15-blessing-LEFT", "p25-beat15-blessing-RIGHT"),
}


def main():
    load_env()
    OUT.mkdir(parents=True, exist_ok=True)
    SPREADS.mkdir(parents=True, exist_ok=True)
    image_urls = urls()
    manifest = []

    for stem, aspect, prompt in JOBS:
        # skip if already complete
        if stem.startswith("spread-"):
            left_name, right_name = SPREAD_PAGE_MAP[stem]
            left_p = OUT / f"{left_name}.png"
            right_p = OUT / f"{right_name}.png"
            wide_p = SPREADS / f"{stem}-WIDE.png"
            if left_p.exists() and right_p.exists():
                print(f"SKIP {stem} (exists)")
                manifest.append({"stem": stem, "status": "exists"})
                continue
            print(f"GEN SPREAD {stem} ...")
            try:
                url = gen(prompt, image_urls, aspect=aspect)
                download(url, wide_p)
                master = SPREADS / f"{stem}-5250x2625.png"
                split_spread(wide_p, left_p, right_p, master)
                print(f"  OK {left_p.name} + {right_p.name}")
                manifest.append({"stem": stem, "url": url, "status": "ok"})
            except Exception as e:
                print(f"  FAIL {stem}: {e}")
                manifest.append({"stem": stem, "status": "fail", "error": str(e)})
            time.sleep(1)
        else:
            dest = OUT / f"{stem}.png"
            if dest.exists() and dest.stat().st_size > 50_000:
                print(f"SKIP {stem}")
                manifest.append({"stem": stem, "status": "exists"})
                continue
            print(f"GEN {stem} ...")
            try:
                url = gen(prompt, image_urls, aspect=aspect)
                download(url, dest)
                print(f"  OK {dest.name} ({dest.stat().st_size // 1024} KB)")
                manifest.append({"stem": stem, "url": url, "status": "ok"})
            except Exception as e:
                print(f"  FAIL {stem}: {e}")
                manifest.append({"stem": stem, "status": "fail", "error": str(e)})
            time.sleep(1)

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    ok = sum(1 for m in manifest if m["status"] in ("ok", "exists"))
    print(f"\nDone: {ok}/{len(manifest)} jobs")


if __name__ == "__main__":
    main()
