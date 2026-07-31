#targetengine "session"
/**
 * Re-export TNIMS Interior FINAL with S04 isolated pages, then merge via Python.
 */
(function () {
  app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;
  app.scriptPreferences.measurementUnit = MeasurementUnits.INCHES;

  var interior = null;
  for (var i = 0; i < app.documents.length; i++) {
    if (app.documents[i].name.indexOf("Interior-FINAL") >= 0) {
      interior = app.documents[i];
      break;
    }
  }
  if (!interior) {
    interior = app.open(
      File("D:/Hermes/projects/The-Night-I-Met-Santa/Xtraz/Adobe-Finals/TNIMS-Interior-FINAL.indd")
    );
  }
  app.activeDocument = interior;

  function linkName(rect) {
    try {
      if (rect.graphics.length && rect.graphics[0].itemLink) {
        return String(rect.graphics[0].itemLink.name);
      }
    } catch (e) {}
    return "";
  }

  var p10 = interior.pages.itemByName("10");
  var p11 = interior.pages.itemByName("11");
  var left = null;
  var right = null;
  var r;
  for (r = 0; r < p10.rectangles.length; r++) {
    if (linkName(p10.rectangles[r]).indexOf("S04-p10-left") >= 0) left = p10.rectangles[r];
  }
  for (r = 0; r < p11.rectangles.length; r++) {
    if (linkName(p11.rectangles[r]).indexOf("S04-p11-right") >= 0) right = p11.rectangles[r];
  }
  if (!left || !right) {
    throw new Error("S04 L/R missing");
  }
  left.visible = true;
  right.visible = true;

  var base = app.pdfExportPresets.itemByName("[High Quality Print]");
  try {
    app.pdfExportPreferences.properties = base.properties;
  } catch (e) {}
  var p = app.pdfExportPreferences;
  p.exportReaderSpreads = false;
  p.standardsCompliance = PDFXStandards.NONE;
  try {
    p.pdfColorSpace = PDFColorSpace.UNCHANGED_COLOR_SPACE;
  } catch (e1) {}
  try {
    p.includeICCProfiles = true;
  } catch (e2) {}
  p.cropMarks = false;
  p.bleedMarks = false;
  p.registrationMarks = false;
  p.colorBars = false;
  p.pageInformationMarks = false;
  p.useDocumentBleedWithPDF = true;
  p.bleedTop = 0;
  p.bleedBottom = 0;
  p.bleedInside = 0;
  p.bleedOutside = 0;
  try {
    p.acrobatCompatibility = AcrobatCompatibility.ACROBAT_5;
  } catch (e3) {}

  var folder = Folder("D:/Hermes/projects/The-Night-I-Met-Santa/Output/interiors/_s04_pages");
  if (!folder.exists) folder.create();

  p.pageRange = "1-9,12-30";
  var rest = File(folder.fsName + "/rest.pdf");
  if (rest.exists) rest.remove();
  interior.exportFile(ExportFormat.PDF_TYPE, rest, false);

  right.visible = false;
  left.visible = true;
  p.pageRange = "10";
  var p10pdf = File(folder.fsName + "/p10.pdf");
  if (p10pdf.exists) p10pdf.remove();
  interior.exportFile(ExportFormat.PDF_TYPE, p10pdf, false);

  left.visible = false;
  right.visible = true;
  p.pageRange = "11";
  var p11pdf = File(folder.fsName + "/p11.pdf");
  if (p11pdf.exists) p11pdf.remove();
  interior.exportFile(ExportFormat.PDF_TYPE, p11pdf, false);

  left.visible = true;
  right.visible = true;
  interior.save();

  __result = {
    ok: true,
    rest: rest.length,
    p10: p10pdf.length,
    p11: p11pdf.length
  };
})();
