# Create TNIMS Lulu-matched spread PSD template via adobepy UXP.
# Specs: 5250x2625 @ 300 DPI, sRGB, bleed/trim/safety/fold guides.

from __future__ import annotations

import json
from pathlib import Path

from adobe.photoshop import Photoshop

OUT = Path(r"D:\Hermes\projects\The-Night-I-Met-Santa\Xtraz\Adobe-Photoshop\spread-page-template.psd")
OUT.parent.mkdir(parents=True, exist_ok=True)

# Pixel geometry @ 300 DPI (matches InDesign / Lulu cheatsheet)
W, H, DPI = 5250, 2625, 300
BLEED = 37.5       # 0.125"
TRIM_INSET = 37.5  # from page canvas edge to trim
SAFETY_FROM_TRIM = 150.0  # 0.5"
PAGE = 2625.0      # one page with bleed

# Absolute positions on full spread canvas
L_TRIM_L = TRIM_INSET
L_TRIM_R = PAGE - TRIM_INSET
L_SAFE_L = TRIM_INSET + SAFETY_FROM_TRIM
L_SAFE_R = PAGE - TRIM_INSET - SAFETY_FROM_TRIM
R_TRIM_L = PAGE + TRIM_INSET
R_TRIM_R = W - TRIM_INSET
R_SAFE_L = PAGE + TRIM_INSET + SAFETY_FROM_TRIM
R_SAFE_R = W - TRIM_INSET - SAFETY_FROM_TRIM
TRIM_T = TRIM_INSET
TRIM_B = H - TRIM_INSET
SAFE_T = TRIM_INSET + SAFETY_FROM_TRIM
SAFE_B = H - TRIM_INSET - SAFETY_FROM_TRIM
FOLD = PAGE  # center fold between L/R page canvases

JS = r"""
function run() {
  var W = __W__, H = __H__, DPI = __DPI__;
  app.displayDialogs = DialogModes.NO;
  app.preferences.rulerUnits = Units.PIXELS;
  app.preferences.typeUnits = TypeUnits.PIXELS;

  // Close existing template if open
  for (var i = app.documents.length - 1; i >= 0; i--) {
    var d0 = app.documents[i];
    if (d0.name.indexOf("spread-page-template") === 0) {
      d0.close(SaveOptions.DONOTSAVECHANGES);
    }
  }

  var doc = app.documents.add(
    UnitValue(W, "px"),
    UnitValue(H, "px"),
    DPI,
    "spread-page-template",
    NewDocumentMode.RGB,
    DocumentFill.WHITE,
    1.0,
    BitsPerChannelType.EIGHT,
    "sRGB IEC61966-2.1"
  );

  // Clear default guides
  doc.guides.removeAll();

  function v(x) { doc.guides.add(Direction.VERTICAL, UnitValue(x, "px")); }
  function h(y) { doc.guides.add(Direction.HORIZONTAL, UnitValue(y, "px")); }

  // --- Vertical: left page bleed edge is canvas 0; right outer is W ---
  // Left page trim + safety
  v(__L_TRIM_L__);
  v(__L_SAFE_L__);
  v(__L_SAFE_R__);
  v(__L_TRIM_R__);
  // Fold (MOCK reference only — do not bake into final art)
  v(__FOLD__);
  // Right page trim + safety
  v(__R_TRIM_L__);
  v(__R_SAFE_L__);
  v(__R_SAFE_R__);
  v(__R_TRIM_R__);

  // Horizontal: shared top/bottom for both pages
  h(__TRIM_T__);
  h(__SAFE_T__);
  h(__SAFE_B__);
  h(__TRIM_B__);

  // --- Layer stack (bottom → top) ---
  // Background already white from DocumentFill.WHITE — rename
  doc.activeLayer.isBackgroundLayer = false;
  doc.activeLayer.name = "white-bg";

  function solidLayer(name, r, g, b, opacity) {
    var layer = doc.artLayers.add();
    layer.name = name;
    layer.opacity = opacity;
    doc.selection.selectAll();
    var c = new SolidColor();
    c.rgb.red = r; c.rgb.green = g; c.rgb.blue = b;
    doc.selection.fill(c);
    doc.selection.deselect();
    return layer;
  }

  function strokeRect(name, left, top, right, bottom, r, g, b, opacity) {
    // Draw hollow box via selection border stroke
    var layer = doc.artLayers.add();
    layer.name = name;
    layer.opacity = opacity;
    doc.selection.select([
      [left, top],
      [right, top],
      [right, bottom],
      [left, bottom]
    ]);
    var c = new SolidColor();
    c.rgb.red = r; c.rgb.green = g; c.rgb.blue = b;
    // Stroke inside selection ~2px
    doc.selection.stroke(c, 2, StrokeLocation.INSIDE, ColorBlendMode.NORMAL, 100, false);
    doc.selection.deselect();
    return layer;
  }

  // Soft paper fill (optional base under art)
  var paper = solidLayer("paper-base", 252, 250, 245, 100);
  paper.visible = true;

  // Art placeholder group label as empty layer
  var art = doc.artLayers.add();
  art.name = "ART — paste / paint full-bleed scene here";
  art.opacity = 100;

  // Trim boxes (cyan) — left + right page
  strokeRect("TRIM-L (8.5in)", __L_TRIM_L__, __TRIM_T__, __L_TRIM_R__, __TRIM_B__, 0, 180, 220, 85);
  strokeRect("TRIM-R (8.5in)", __R_TRIM_L__, __TRIM_T__, __R_TRIM_R__, __TRIM_B__, 0, 180, 220, 85);

  // Safety boxes (magenta) — matches InDesign pink margins
  strokeRect("SAFETY-L (0.5in inset)", __L_SAFE_L__, __SAFE_T__, __L_SAFE_R__, __SAFE_B__, 220, 40, 160, 90);
  strokeRect("SAFETY-R (0.5in inset)", __R_SAFE_L__, __SAFE_T__, __R_SAFE_R__, __SAFE_B__, 220, 40, 160, 90);

  // Fold marker (orange dashed feel via thin fill column) — hide for finals
  var fold = doc.artLayers.add();
  fold.name = "FOLD (MOCK only — hide for finals)";
  fold.opacity = 60;
  doc.selection.select([
    [__FOLD__ - 1, 0],
    [__FOLD__ + 1, 0],
    [__FOLD__ + 1, H],
    [__FOLD__ - 1, H]
  ]);
  var fc = new SolidColor();
  fc.rgb.red = 255; fc.rgb.green = 140; fc.rgb.blue = 0;
  doc.selection.fill(fc);
  doc.selection.deselect();

  // Cloud / Type placeholders (empty)
  var cloud = doc.artLayers.add();
  cloud.name = "CLOUD — watercolor text wash (optional)";
  var typeL = doc.artLayers.add();
  typeL.name = "TYPE zone LEFT — live type in InDesign preferred";
  var typeR = doc.artLayers.add();
  typeR.name = "TYPE zone RIGHT — live type in InDesign preferred";

  // Info text layer
  var info = doc.artLayers.add();
  info.kind = LayerKind.TEXT;
  info.name = "TEMPLATE-INFO (delete before export)";
  var tf = info.textItem;
  tf.contents = "TNIMS spread template | 5250x2625 px @ 300 DPI | 17.5 x 8.75 in | sRGB | Lulu 8.5sq + 0.125 bleed | Cyan=TRIM | Magenta=SAFETY 0.5in | Orange=FOLD (hide on finals) | Save chops to Images/chopz | Working PSD: Xtraz/Adobe-Photoshop";
  tf.size = 10;
  tf.font = "ArialMT";
  tf.color.rgb.red = 40; tf.color.rgb.green = 40; tf.color.rgb.blue = 40;
  tf.position = [UnitValue(200, "px"), UnitValue(80, "px")];

  // Group overlay guides visually at top of stack but leave ART near bottom
  // Reorder: move overlays above ART
  // (Photoshop layer order: last created = top)

  // Save PSD
  var f = new File(__OUT__);
  var opts = new PhotoshopSaveOptions();
  opts.embedColorProfile = true;
  opts.alphaChannels = true;
  opts.layers = true;
  doc.saveAs(f, opts, true, Extension.LOWERCASE);

  return {
    ok: true,
    path: String(f.fsName),
    width: doc.width.as("px"),
    height: doc.height.as("px"),
    resolution: doc.resolution,
    mode: String(doc.mode),
    guides: doc.guides.length,
    layers: doc.layers.length
  };
}
run();
"""

repl = {
    "__W__": str(W),
    "__H__": str(H),
    "__DPI__": str(DPI),
    "__L_TRIM_L__": str(L_TRIM_L),
    "__L_TRIM_R__": str(L_TRIM_R),
    "__L_SAFE_L__": str(L_SAFE_L),
    "__L_SAFE_R__": str(L_SAFE_R),
    "__R_TRIM_L__": str(R_TRIM_L),
    "__R_TRIM_R__": str(R_TRIM_R),
    "__R_SAFE_L__": str(R_SAFE_L),
    "__R_SAFE_R__": str(R_SAFE_R),
    "__TRIM_T__": str(TRIM_T),
    "__TRIM_B__": str(TRIM_B),
    "__SAFE_T__": str(SAFE_T),
    "__SAFE_B__": str(SAFE_B),
    "__FOLD__": str(FOLD),
    "__OUT__": json.dumps(str(OUT).replace("\\", "/")),
}

for k, v in repl.items():
    JS = JS.replace(k, v)

app = Photoshop(token="dev-token")
# Prefer ExtendScript host eval if available
result = None
for method in ("eval_js", "evalJs"):
    fn = getattr(app, method, None)
    if callable(fn):
        try:
            result = fn(JS)
            break
        except Exception as e:
            print(f"{method} failed: {e}")

if result is None:
    # batchPlay / raw fallback
    raw = getattr(app, "raw", None)
    if raw is not None and hasattr(raw, "eval_extendscript"):
        result = raw.eval_extendscript(JS)
    else:
        raise SystemExit("No JS eval path on Photoshop facade")

print("RESULT:", result)
print("OUT exists:", OUT.exists(), "size:", OUT.stat().st_size if OUT.exists() else 0)
