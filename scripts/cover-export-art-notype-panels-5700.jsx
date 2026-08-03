#target photoshop
/**
 * Export Front + Back panels for Cover INDD art-no-type compose.
 * Hides: Type layers, QR layers/groups, Lulu guides
 * Keeps: cover-title-logo, Frame, art (live author/credits stay in InDesign)
 *
 * Outputs:
 *   scripts/_scratch/_panel-front-art-notype.png
 *   scripts/_scratch/_panel-back-art-notype.png
 *
 * Then: python scripts/cover-compose-art-notype-5700.py
 */
app.displayDialogs = DialogModes.NO;
var log = [];
function L(s) { log.push(String(s)); }

var ROOT = "D:/Hermes/projects/The-Night-I-Met-Santa/";
var OUT = ROOT + "Xtraz/Adobe-Photoshop/FINAL-Master-PSDs/5700x3075-version/";
var FRONT_PATH = OUT + "TNIMS-Cover-FRONT-FINAL-5700x3075.psd";
var BACK_PATH = OUT + "TNIMS-Cover-BACK-FINAL-5700x3075.psd";
var TMP_FRONT = ROOT + "scripts/_scratch/_panel-front-art-notype.png";
var TMP_BACK = ROOT + "scripts/_scratch/_panel-back-art-notype.png";
var RESULT = ROOT + "scripts/_scratch/_cover_export_art_notype_result.txt";

function findDoc(sub) {
  for (var i = 0; i < app.documents.length; i++) {
    if (app.documents[i].name.indexOf(sub) >= 0) return app.documents[i];
  }
  return null;
}
function findTop(doc, name) {
  for (var i = 0; i < doc.layers.length; i++) {
    if (doc.layers[i].name === name) return doc.layers[i];
  }
  return null;
}
function ensureOpen(path, sub) {
  var d = findDoc(sub);
  if (d) return d;
  app.open(new File(path));
  return findDoc(sub);
}
function hideForArtNoType(layer, state) {
  var n = layer.name || "";
  var isType = (layer.typename === "ArtLayer" && layer.kind === LayerKind.TEXT);
  var hide =
    isType ||
    n.indexOf("GUIDES") >= 0 ||
    n.indexOf("QR") >= 0 ||
    n.indexOf("Jon-Beatz-QR") >= 0 ||
    n.indexOf("DigitalStudioz-QR") >= 0 ||
    n === "Text" ||
    n === "QR-Codes";
  state.push({ layer: layer, vis: layer.visible });
  if (hide) layer.visible = false;
  if (layer.typename === "LayerSet") {
    for (var i = 0; i < layer.layers.length; i++) hideForArtNoType(layer.layers[i], state);
  }
}
function restoreVis(state) {
  for (var i = 0; i < state.length; i++) {
    try { state[i].layer.visible = state[i].vis; } catch (e) {}
  }
}
function exportPanelPng(doc, outPath) {
  var g = findTop(doc, "02-LULU-GUIDES");
  var gVis = false;
  if (g) { gVis = g.visible; g.visible = false; }
  var f = new File(outPath);
  if (f.exists) { try { f.remove(); } catch (e) {} }
  var opts = new PNGSaveOptions();
  opts.compression = 6;
  opts.interlaced = false;
  doc.saveAs(f, opts, true, Extension.LOWERCASE);
  if (g) g.visible = gVis;
  L("exported " + outPath);
}

try {
  var front = ensureOpen(FRONT_PATH, "FRONT-FINAL-5700");
  var back = ensureOpen(BACK_PATH, "BACK-FINAL-5700");

  app.activeDocument = front;
  var stF = [];
  for (var fi = 0; fi < front.layers.length; fi++) hideForArtNoType(front.layers[fi], stF);
  exportPanelPng(front, TMP_FRONT);
  restoreVis(stF);

  app.activeDocument = back;
  var stB = [];
  for (var bi = 0; bi < back.layers.length; bi++) hideForArtNoType(back.layers[bi], stB);
  exportPanelPng(back, TMP_BACK);
  restoreVis(stB);

  L("DONE — next: python scripts/cover-compose-art-notype-5700.py");
} catch (e) {
  L("ERROR " + e);
}

var rf = new File(RESULT);
rf.open("w");
rf.write(log.join("\n"));
rf.close();
