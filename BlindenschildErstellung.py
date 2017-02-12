import adsk.core, adsk.fusion
import math

app = adsk.core.Application.get();
ui = app.userInterface;
BuchstabenDictionary = {}
Schild = "12"
Schildformat = "42,4"

design = app.activeProduct
root = design.rootComponent
occs = root.occurrences
def DegtoRad(Deg):
	return Deg*math.pi/180

def floatConversion (number):
    return float(number.replace(",", "."))

SchildformatAlsFloat = floatConversion(Schildformat)/10
xVerschiebung = 0
AktivesProjekt = app.data.activeProject
WurzelOrdner = AktivesProjekt.rootFolder.dataFolders
BuchstabenOrdner = WurzelOrdner.itemByName("Blindenschrift Projekt").dataFolders.itemByName("Buchstaben")
PyramidenschriftOrdner = BuchstabenOrdner.dataFolders.itemByName("16mm ({}) Einfarbig".format(Schildformat))
BrailleOrdner = BuchstabenOrdner.dataFolders.itemByName("Braille {}".format(Schildformat))
Pyramidenbuchstaben = PyramidenschriftOrdner.dataFiles
Braillebuchstaben = BrailleOrdner.dataFiles
ZahlZuBuchstabe = {"1":"A", "2":"B", "3":"C", "4":"D", "5":"E", "6":"F", "7":"G", "8":"H", "9":"I", "0": "J" }
BuchstabeZuZahl = {"A":"1", "B":"2", "C":"3", "D":"4", "E":"5", "F":"6", "G":"7", "H": "8", "I": "9", "J":"0" }
SchildBreite = adsk.core.ValueInput.createByReal(20)


Ursprung = adsk.core.Point3D.create()
obererPunkt = adsk.core.Point3D.create(0,float(SchildformatAlsFloat)/2,0)
untererPunkt = adsk.core.Point3D.create(0,float(SchildformatAlsFloat)/2-0.2,0)
XVektor = adsk.core.Vector3D.create(1,0,0)
WinkelfuerDrehung = -50
WinkelfueSeite1= 70
WinkelfueSeite2=-35
radfuerDrehung = DegtoRad(WinkelfuerDrehung)
radfuerSeite1 = DegtoRad(WinkelfueSeite1)
radfuerSeite2 = DegtoRad(WinkelfueSeite2)
##### KomponentenErstellung ####
BasisSkizze = root.sketches.add(root.yZConstructionPlane)
BasisKurven = BasisSkizze.sketchCurves
BasisLines = BasisKurven.sketchLines
Kurve1 = BasisKurven.sketchArcs.addByCenterStartSweep(Ursprung, obererPunkt, radfuerSeite1)
Kurve2 = BasisKurven.sketchArcs.addByCenterStartSweep(Ursprung,Kurve1.startSketchPoint, radfuerSeite2)
Kurven = BasisSkizze.findConnectedCurves(Kurve1)
Offset = BasisSkizze.offset(Kurven, untererPunkt, 0.2)
BasisLines.addByTwoPoints(Kurve1.endSketchPoint, Offset.item(1).endSketchPoint)
BasisLines.addByTwoPoints(Kurve2.startSketchPoint, Offset.item(0).startSketchPoint)
Profile = BasisSkizze.profiles.item(0)
RootExtrudes = root.features.extrudeFeatures
RootExtrudeInput = rootExtrudes.createInput(Profile, 3)
RootExtrudeInput.setSymmetricExtent(SchildBreite ,True)
Extrusion = RootExtrudes.add(RootExtrudeInput)

exit()

MoveMatrix = adsk.core.Matrix3D.create()
PyramidenOcc = occs.addNewComponent(MoveMatrix)
BrailleOcc = occs.addNewComponent(MoveMatrix)

PyramidenOcc.component.name = "Pyramiden Buchstaben"
BrailleOcc.component.name = "Braille Buchstaben"

PyramidenComponent = PyramidenOcc.component
BrailleComponent = BrailleOcc.component

PyramidenComponent.name = "Pyramiden Buchstaben"
BrailleComponent.name = "Braille Buchstaben"

PyramidenOccs = PyramidenComponent.occurrences
BrailleOccs = BrailleComponent.occurrences


def stringtoDateinamenListe(beschriftung, schildformat):
	ZahlenModus = 0
	brailleDateinamenListe = []
	pyramidenDateinamenListe = []
	for char in beschriftung:
		if char == " ":
			brailleDateinamenListe.append("Leerzeichen Braille {}".format(Schildformat))
			pyramidenDateinamenListe.append("Leerzeichen Einfarbig Pyramiden {}".format(Schildformat))
			ZahlenModus = 0
			continue
		if char.isdigit():
			pyramidenDateinamenListe.append("{} Einfarbig Pyramiden {}".format(char, Schildformat))
			if not ZahlenModus:
				brailleDateinamenListe.append("Raute Braille {}".format( Schildformat))
				ZahlenModus = 1
			brailleDateinamenListe.append("{} ({}) Braille {}".format(ZahlZuBuchstabe[char], char, Schildformat))
			continue
		if char.isalpha():
			pyramidenDateinamenListe.append("{} Einfarbig Pyramiden {}".format(char, Schildformat))
			if char in BuchstabeZuZahl:
				if ZahlenModus:
					brailleDateinamenListe.append("Apostroph Braille {}".format(Schildformat))
				brailleDateinamenListe.append("{} ({}) Braille {}".format(char, BuchstabeZuZahl[char], Schildformat))
			else:
				brailleDateinamenListe.append("{} Braille {}".format(char, Schildformat))
			ZahlenModus = 0
			continue
		if char == ".":
			pyramidenDateinamenListe.append("Punkt Einfarbig Pyramiden {}".format(Schildformat))
			brailleDateinamenListe.append("Punkt Braille {}".format(Schildformat))
			ZahlenModus = 0
	return pyramidenDateinamenListe, brailleDateinamenListe

def makeitemNamenDictionary (dateien):
	itemNamenDictionary = {}
	for n in range(0, len(dateien)):
		dateiName = dateien.item(n).name
		datei = dateien.item(n)
		itemNamenDictionary.update({dateiName : datei})
	return itemNamenDictionary







PyramidenDateinamenListe, BrailleDateinamenListe = stringtoDateinamenListe(Schild, Schildformat)


PyramidenDictionary = makeitemNamenDictionary(Pyramidenbuchstaben)
BrailleDictionary = makeitemNamenDictionary(Braillebuchstaben)


Vektor = adsk.core.Vector3D.create(0,0,0)


for DateiName in PyramidenDateinamenListe:
    Datei = PyramidenDictionary[DateiName]
    Buchstabe = PyramidenOccs.addByInsert(Datei, MoveMatrix, True)
    halbeBuchstabenBreite = Buchstabe.component.parentDesign.allParameters.itemByName("breite").value/2
    xVerschiebung += halbeBuchstabenBreite
    Vektor.x = xVerschiebung
    MoveMatrix.translation = Vektor
    Buchstabe.transform = MoveMatrix
    xVerschiebung += halbeBuchstabenBreite
    Vektor.x = xVerschiebung
    MoveMatrix.translation = Vektor
    design.snapshots.add()

Vektor.x = -Vektor.x/2
MoveMatrix.translation = Vektor
PyramidenOcc.transform = MoveMatrix
design.snapshots.add()

Vektor.x = 0.33
#???
MoveMatrix = adsk.core.Matrix3D.create()
MoveMatrix.translation = Vektor

for DateiName in BrailleDateinamenListe:
	Datei = BrailleDictionary[DateiName]
	Buchstabe = BrailleOccs.addByInsert(Datei, MoveMatrix, True)
	Vektor.x += 0.66
	MoveMatrix.translation = Vektor

Vektor.x = -(Vektor.x -0.33)/2
MoveMatrix.setToRotation(radfuerDrehung, XVektor, Ursprung)
MoveMatrix.translation = Vektor
BrailleOcc.transform = MoveMatrix
design.snapshots.add()
# Blindenschild-Projekt
