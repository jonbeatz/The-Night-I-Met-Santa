"""
Convert watercolor washes to transparent overlays.
- White/light areas → fully transparent
- Colored wash areas → partially transparent (subtle)
- Edge-feathered blend into full transparency
"""
from PIL import Image
import os

from pathlib import Path
MEDIA = str(Path(__file__).resolve().parent / "Media")
files = ["wc-v2-bl.png", "wc-v2-br.png", "wc-v2-tl.png", "wc-v2-tr.png", "wc-v2-bc.png"]

for fname in files:
    path = os.path.join(MEDIA, fname)
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    print(f"Processing {fname}: {w}x{h}")

    pixels = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # Calculate brightness — how "white" is this pixel
            brightness = (r + g + b) / 3

            if brightness > 240:
                # Near-white: fully transparent
                pixels[x, y] = (r, g, b, 0)
            elif brightness > 200:
                # Light area: mostly transparent, keep slight tint
                alpha = int((240 - brightness) / 40 * 60)  # 0-60 range
                pixels[x, y] = (r, g, b, alpha)
            elif brightness > 150:
                # Medium wash: semi-transparent
                alpha = int((200 - brightness) / 50 * 100) + 60  # 60-160 range
                pixels[x, y] = (r, g, b, alpha)
            elif brightness > 100:
                # Darker wash: more visible
                alpha = int((150 - brightness) / 50 * 60) + 160  # 160-220 range
                pixels[x, y] = (r, g, b, alpha)
            else:
                # Darkest wash area: nearly opaque but still subtle
                pixels[x, y] = (r, g, b, 200)

    # Save as proper transparent PNG
    out_name = fname.replace("wc-v2-", "wc-trans-")
    out_path = os.path.join(MEDIA, out_name)
    img.save(out_path, "PNG")
    size_kb = os.path.getsize(out_path) / 1024
    print(f"  → {out_name} ({size_kb:.0f} KB)")

print("\nDone! All transparent washes created.")
