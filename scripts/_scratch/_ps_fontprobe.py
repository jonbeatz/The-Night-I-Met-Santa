from adobe.photoshop import Photoshop
app = Photoshop()
# try create with common PS names
candidates = [
  "CormorantGaramond-Medium",
  "CormorantGaramondMedium",
  "CormorantGaramond-Regular",
  "CormorantGaramond-Light",
  "EBGaramond-Medium",
  "Georgia",
]
print("active", app.activeDocument.name if app.activeDocument else None)
