# TEXT OVERLAY POLICY — Locked direction (Jon feedback 2026-07-15)

**Status:** Direction locked from Jon’s mockup tweaks · still dial before full compositor ship  
**North-star refs (Jon):**  
- `Images/references/layout/ref-text-jon-eyes-left-soft-fade.png`  
- `Images/references/layout/ref-text-jon-sneak-side-bleed.png`  
Plus original: `ref-overlay-cloud-text.png` · `ref-spread-bleed-text.png`

---

## Absolute rules

1. **Never cover faces** (child or Santa) — or other hero features (hands on note, eyes-meet). If a wash would hit a face → move zone.
2. **Legibility first** — text sits on a soft **white/ivory paint fade** strong enough to read, then **blends into the art**.
3. **Edges must fade** — smooth gradient / faint **paint-brush swipes**, not a standout blob with a hard outline.
4. **Glow must cover every line** — if using a corner/side fade, also seat type on a **soft white glow sized to the full text block** so no line sits on bare dark tree/wall.
5. **Use open design areas** — walls, side panels, bottom corners, side-bleeds — never drop type in the middle of a window, over gifts as default, or over Santa’s head.
6. **Large storybook serif** (Georgia bold family) — cover-title *feel*, flat ink.

---

## Reject forever

| Reject | Example |
|--------|---------|
| Gray mud clouds | Early mocks |
| Soft cream **rectangles** | `wash-A` |
| Harsh solid white “sticker” blobs | `07-note` v2 white-paint |
| Wash sitting **on Santa’s / child’s face** | `02-eyes-right` v2 |
| Text middle of a bright window | note page mid-window |

---

## Preferred placements (from Jon)

| Situation | Zone | Wash |
|-----------|------|------|
| Open cream wall (eyes-met left) | Upper/mid **left wall** | Soft corner/side fade OR none if wall already light |
| Busy figure on left (Santa right page) | **Bottom-right** quiet area | White gradient **from BR corner toward** figure — stop before the face |
| Peek / doorway scenes | **Left side bleed** | Long soft vertical paint bleed (Jon sneak mockup) |
| Note / chair pages | **Lower** quiet band / corner | Soft mist — not mid-window |
| Dark hall walls | Left dark wall | **Light ink**, little/no white wash |

---

## Paint-fade recipe (engineering)

- Color: warm white/ivory `(255, 250, 242)`  
- **Always** add a **text-block soft glow** sized to the full stanza (+ pad) so every line sits on paper — not only a short corner gradient  
- Edge: large blur + faint paint-swipe lobes  
- Side bleed / corner wash can add atmosphere; glow under type is what guarantees legibility  

---

## Mock folder

| Folder | Status |
|--------|--------|
| `text-mocks-v2/` | Closer; superseded by v3 for harsh blob / face hits |
| **`text-mocks-v3/`** | Rebuild matching Jon refs |

Script: `scripts/mock_text_overlay_v3.py`
