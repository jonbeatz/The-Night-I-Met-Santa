from adobe.photoshop import Photoshop
app = Photoshop()
app.batch_play([{
  "_obj": "select",
  "_target": [{"_ref": "document", "_name": "p03-dedication.psd"}],
}], modal=True, command_name="Select p03")
# Ensure TYPE guide stays hidden; MOCK-TYPE visible on top
app.batch_play([
  {"_obj": "select", "_target": [{"_ref": "layer", "_name": "TYPE zone - live Cormorant in InDesign"}]},
  {"_obj": "hide", "null": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}]},
], modal=True, command_name="Keep TYPE guide hidden")
app.batch_play([
  {"_obj": "select", "_target": [{"_ref": "layer", "_name": "MOCK-TYPE - dedication (preview)"}]},
  {"_obj": "show", "null": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}]},
], modal=True, command_name="Show MOCK-TYPE")
print("ready for Jon review")
