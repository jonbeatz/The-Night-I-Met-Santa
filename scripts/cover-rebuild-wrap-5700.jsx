#target photoshop
/**
 * Rebuild Wrap with FULL layered groups from Front + Back masters.
 * Panel clip via clipping-mask base layers (keeps all nested layers editable).
 */
app.displayDialogs = DialogModes.NO;
var log = [];
function L(s) { log.push(String(s)); }

var ROOT = "D:/Hermes/projects/The-Night-I-Met-Santa/";
var OUT = ROOT + "Xtraz/Adobe-Photoshop/FINAL-Master-PSDs/5700x3075-version/";
var LINKS = ROOT + "Xtraz/Adobe-inDesign/FINAL-Master-inDD/links/";
var FRONT_PATH = OUT + "TNIMS-Cover-FRONT-FINAL-5700x3075.psd";
var BACK_PATH = OUT + "TNIMS-Cover-BACK-FINAL-5700x3075.psd";
var WRAP_PATH = OUT + "TNIMS-Cover-Wrap-FINAL-5700x3075.psd";
var RESULT = ROOT + "scripts/_scratch/_cover_rebuild_wrap_result.txt";

var BW = 2813, SW = 75, WW = 5700, WH = 3075;
var FRONT_X = BW + SW; // 2888

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

/** Solid panel rectangle used as clipping base for a LayerSet above it */
function addClipBase(doc, name, left, top, right, bottom) {
  app.activeDocument = doc;
  var base = doc.artLayers.add();
  base.name = name;
  doc.selection.select([
    [UnitValue(left, "px"), UnitValue(top, "px")],
    [UnitValue(right, "px"), UnitValue(top, "px")],
    [UnitValue(right, "px"), UnitValue(bottom, "px")],
    [UnitValue(left, "px"), UnitValue(bottom, "px")]
  ]);
  var c = new SolidColor();
  c.rgb.red = 255; c.rgb.green = 255; c.rgb.blue = 255;
  doc.selection.fill(c);
  doc.selection.deselect();
  return base;
}

/**
 * Duplicate art group from panel master → wrap.
 * Map panel canvas origin to wrap panelOriginX; clip overhang with clipping mask.
 */
function placeArtGroup(srcDoc, artName, wrap, destName, panelOriginX, maskL, maskR) {
  app.activeDocument = srcDoc;
  var art = findTop(srcDoc, artName);
  if (!art) throw new Error("missing " + artName + " on " + srcDoc.name);
  var ox = art.bounds[0].as("px");
  var oy = art.bounds[1].as("px");
  L(destName + " src offset " + ox + "," + oy);

  // Ensure source art visibility is print-correct before duplicate
  // (open docs may still have type/QR hidden after an art-no-type export)
  function forcePrintVis(layer) {
    var n = layer.name || "";
    if (layer.typename === "ArtLayer" && layer.kind === LayerKind.TEXT) layer.visible = true;
    if (n === "Jon-Beatz-QR1-print") layer.visible = true;
    if (n === "Jon-Beatz-QR1" || n === "DigitalStudioz-QR1") layer.visible = false;
    if (n.indexOf("GUIDES") >= 0) layer.visible = false;
    if (layer.typename === "LayerSet") {
      for (var i = 0; i < layer.layers.length; i++) forcePrintVis(layer.layers[i]);
    }
  }
  forcePrintVis(art);

  art.duplicate(wrap, ElementPlacement.PLACEATBEGINNING);
  app.activeDocument = wrap;
  var lyr = wrap.layers[0];
  lyr.name = destName;

  var b = lyr.bounds;
  var curX = b[0].as("px");
  var curY = b[1].as("px");
  var targetX = panelOriginX + ox;
  var targetY = 0 + oy;
  lyr.translate(UnitValue(targetX - curX, "px"), UnitValue(targetY - curY, "px"));

  // Clipping base under the group
  var base = addClipBase(wrap, destName + "-clip", maskL, 0, maskR, WH);
  // Move base to just below the art group
  base.move(lyr, ElementPlacement.PLACEAFTER);
  // Clip art group to base
  wrap.activeLayer = lyr;
  lyr.grouped = true;

  b = lyr.bounds;
  L(destName + " placed+clipped " + b[0].as("px") + "," + b[1].as("px") + "->" + b[2].as("px") + "," + b[3].as("px"));
  return lyr;
}

try {
  var front = findDoc("FRONT-FINAL-5700");
  if (!front) front = ensureOpen(FRONT_PATH, "FRONT-FINAL-5700");
  app.activeDocument = front;
  front.save();
  L("FRONT saved");

  var back = ensureOpen(BACK_PATH, "BACK-FINAL-5700");

  for (var i = app.documents.length - 1; i >= 0; i--) {
    var n = app.documents[i].name;
    if (
      n.indexOf("Wrap-FINAL-5700") >= 0 ||
      n.indexOf("FROM-FRONT-BUILD") >= 0 ||
      n.indexOf("art-no-type") >= 0 ||
      n.indexOf("Wrap-REBUILD") >= 0 ||
      n.indexOf("Wrap-COVERFIT") >= 0
    ) {
      app.documents[i].close(SaveOptions.DONOTSAVECHANGES);
      L("closed " + n);
    }
  }

  var wrap = app.documents.add(
    UnitValue(WW, "px"),
    UnitValue(WH, "px"),
    300,
    "TNIMS-Wrap-REBUILD",
    NewDocumentMode.RGB,
    DocumentFill.TRANSPARENT
  );

  // Order bottom→top eventually: SPINE, BACK-clip, BACK, FRONT-clip, FRONT, GUIDES
  placeArtGroup(back, "Back-Cover-Art", wrap, "BACK", 0, 0, BW);
  placeArtGroup(front, "Front-Cover-Art", wrap, "FRONT", FRONT_X, FRONT_X, WW);

  app.activeDocument = wrap;
  var spine = wrap.artLayers.add();
  spine.name = "SPINE";
  wrap.selection.select([
    [UnitValue(BW, "px"), UnitValue(0, "px")],
    [UnitValue(BW + SW, "px"), UnitValue(0, "px")],
    [UnitValue(BW + SW, "px"), UnitValue(WH, "px")],
    [UnitValue(BW, "px"), UnitValue(WH, "px")]
  ]);
  var sc = new SolidColor();
  sc.rgb.red = 88; sc.rgb.green = 18; sc.rgb.blue = 28;
  wrap.selection.fill(sc);
  wrap.selection.deselect();
  spine.move(wrap.layers[wrap.layers.length - 1], ElementPlacement.PLACEAFTER);
  L("SPINE ok");

  var guidesFile = new File(LINKS + "02-LULU-GUIDES-WRAP-5700x3075.png");
  if (!guidesFile.exists) {
    guidesFile = new File(ROOT + "Xtraz/Lulu-Templates/from-lulu/ps-guide-overlays/02-LULU-GUIDES-WRAP-5700x3075.png");
  }
  if (guidesFile.exists) {
    app.open(guidesFile);
    var gDoc = app.activeDocument;
    gDoc.activeLayer.duplicate(wrap, ElementPlacement.PLACEATBEGINNING);
    gDoc.close(SaveOptions.DONOTSAVECHANGES);
    app.activeDocument = wrap;
    wrap.layers[0].name = "02-LULU-GUIDES";
    var GG = wrap.layers[0];
    var ggb = GG.bounds;
    var ggw = ggb[2].as("px") - ggb[0].as("px");
    var ggh = ggb[3].as("px") - ggb[1].as("px");
    GG.resize((WW / ggw) * 100, (WH / ggh) * 100, AnchorPosition.TOPLEFT);
    ggb = GG.bounds;
    GG.translate(UnitValue(0 - ggb[0].as("px"), "px"), UnitValue(0 - ggb[1].as("px"), "px"));
    GG.visible = false;
    L("GUIDES ok");
  }

  for (var x = wrap.layers.length - 1; x >= 0; x--) {
    if (wrap.layers[x].name === "Layer 1") wrap.layers[x].remove();
  }

  // Nest each panel into a tidy folder: BACK contains clip+art? 
  // Keep flat top-level: GUIDES, FRONT, FRONT-clip, BACK, BACK-clip, SPINE
  // Better UX: put clip base + art inside a parent folder without breaking clipping.
  // Clipping must stay: art immediately above clip base.
  // Parent group wrapping both can break clipping — leave as:
  //   FRONT (group, clipped) / FRONT-clip / BACK (group, clipped) / BACK-clip / SPINE

  function dump(layer, depth) {
    var pad = "";
    for (var d = 0; d < depth; d++) pad += "  ";
    var clip = "";
    try { if (layer.grouped) clip = " [clip]"; } catch (e) {}
    L(pad + layer.typename + " " + layer.name + (layer.visible ? "" : " [hid]") + clip);
    if (layer.typename === "LayerSet") {
      for (var ci = 0; ci < layer.layers.length; ci++) dump(layer.layers[ci], depth + 1);
    }
  }
  L("--- wrap tree ---");
  for (var ti = 0; ti < wrap.layers.length; ti++) dump(wrap.layers[ti], 0);

  var opts = new PhotoshopSaveOptions();
  opts.embedColorProfile = true;
  opts.maximizeCompatibility = true;
  var wout = new File(WRAP_PATH);
  if (wout.exists) {
    try { wout.remove(); } catch (eRm) { L("rm " + eRm); }
  }
  wrap.saveAs(wout, opts, true, Extension.LOWERCASE);
  L("WRAP saved");
  wrap.close(SaveOptions.DONOTSAVECHANGES);

  while (app.documents.length > 0) app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
  app.open(new File(FRONT_PATH));
  app.open(new File(BACK_PATH));
  app.open(new File(WRAP_PATH));
  L("OPEN three SoT");
  L("DONE");
} catch (e) {
  L("ERROR " + e);
}

var rf = new File(RESULT);
rf.open("w");
rf.write(log.join("\n"));
rf.close();
