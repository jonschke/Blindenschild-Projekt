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

xVerschiebung = 0
AktivesProjekt = app.data.activeProject
WurzelOrdner = AktivesProjekt.rootFolder.dataFolders
BuchstabenOrdner = WurzelOrdner.itemByName("Blindenschrift Projekt").dataFolders.itemByName("Buchstaben")
PyramidenschriftOrdner = BuchstabenOrdner.dataFolders.itemByName("16mm ({}) Einfarbig".format(Schildformat))
BrailleOrdner = BuchstabenOrdner.dataFolders.itemByName("Braille {}".format(Schildformat))
Pyramidenbuchstaben = PyramidenschriftOrdner.dataFiles
Braillebuchstaben = BrailleOrdner.dataFiles
ZahlZuBuchstabe = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I", 0 : "J" }
BuchstabeZuZahl = {"A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H": 8, "I": 9, "J":0 }
ZahlenModus = 0
Ursprung = adsk.core.Point3D.create()
XVektor = adsk.core.Vektor3D.create(1,0,0)
WinkelfuerDrehung = -50
radfuerDrehung = math.pi*WinkelfuerDrehung/180
##### KomponentenErstellung ####

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
		dateiName = datei.item(n).name
		datei = datei.item(n)
		itemNamenDictionary.update({dateiName : datei})
	return itemNamenDictionary

PyramidenDateinamenListe, BrailleDateinamenListe = stringtoDateinamenListe(Schild, Schildformat)


PyramidenDictionary = makeitemNamenDictionary(Pyramidenbuchstaben)
BrailleDictionary = makeitemNamenDictionary(Braillebuchstaben)


Vektor = adsk.core.Vector3D.create(0,0,0)


for DateiName in PyramidenDateinamenListe:
    Datei = PyramidenDictionary[DateiName]
    Buchstabe = PyramidenOccs.addByInsert(Datei, MoveMatrix, True)
    halbeBuchstabenBreite = Buchstabe.component.parentDesign.allParameters.itemByName("breite").value
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
exit()

Vektor = adsk.core.Vector3D.create(0.66,0,0)
#???
MoveMatrix = adsk.core.Matrix3D.create(Vektor)

for DateiName in BrailleDateinamenListe:
	Datei = BrailleDictionary
	Buchstabe = BrailleOccs.addByInsert(Datei, MoveMatrix, True)
	Vektor.x += 0.33
	MoveMatrix.translation = Vektor

Vektor.x = -Vektor.x/2
MoveMatrix.translation = Vektor
MoveMatrix.setToRotation(radfuerDrehung, XVektor, Ursprung)
BrailleOcc.transform = MoveMatrix
design.snapshots.add()
