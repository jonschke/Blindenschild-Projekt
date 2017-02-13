import adsk.core, adsk.fusion
import math

app = adsk.core.Application.get();
ui = app.userInterface;
BuchstabenDictionary = {}


design = app.activeProduct
root = design.rootComponent
occs = root.occurrences

#### Definition of the Functions #####
def DegtoRad(Deg):
	return Deg*math.pi/180

def floatConversion (number):
    return float(number.replace(",", "."))
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

##### Definition of parameters #####

Schild = "12"
Schildformat = "42,4"
SchildformatAlsFloat = floatConversion(Schildformat)/10
SchildBreite = adsk.core.ValueInput.createByReal(2.0)
FilletRadius1 = adsk.core.ValueInput.createByReal(0.5)
FilletRadius2 = adsk.core.ValueInput.createByReal(0.1)
WinkelfuerDrehung = -50
WinkelfueSeite1= -70
WinkelfueSeite2= 35
ZahlZuBuchstabe = {"1":"A", "2":"B", "3":"C", "4":"D", "5":"E", "6":"F", "7":"G", "8":"H", "9":"I", "0": "J" }
BuchstabeZuZahl = {"A":"1", "B":"2", "C":"3", "D":"4", "E":"5", "F":"6", "G":"7", "H": "8", "I": "9", "J":"0" }
xVerschiebung = 0
RadfuerDrehung = DegtoRad(WinkelfuerDrehung)
RadfuerSeite1 = DegtoRad(WinkelfueSeite1)
RadfuerSeite2 = DegtoRad(WinkelfueSeite2)
#### Generating basic points and vectors ####
Ursprung = adsk.core.Point3D.create()
BasisPunkt = adsk.core.Point3D.create(0,float(SchildformatAlsFloat)/2,0)
ObererPunkt = adsk.core.Point3D.create(0,float(SchildformatAlsFloat)/2+0.2,0)
XVektor = adsk.core.Vector3D.create(1,0,0)
MoveMatrix = adsk.core.Matrix3D.create()
Vektor = adsk.core.Vector3D.create(0,0,0)


#### Get the char files #####

AktivesProjekt = app.data.activeProject
WurzelOrdner = AktivesProjekt.rootFolder.dataFolders
BuchstabenOrdner = WurzelOrdner.itemByName("Blindenschrift Projekt").dataFolders.itemByName("Buchstaben")
PyramidenschriftOrdner = BuchstabenOrdner.dataFolders.itemByName("16mm ({}) Einfarbig".format(Schildformat))
BrailleOrdner = BuchstabenOrdner.dataFolders.itemByName("Braille {}".format(Schildformat))
Pyramidenbuchstaben = PyramidenschriftOrdner.dataFiles
Braillebuchstaben = BrailleOrdner.dataFiles
#### Generate new Components for the braille and the pyramid string

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

####  Generate list of file names out of the input string ######
PyramidenDateinamenListe, BrailleDateinamenListe = stringtoDateinamenListe(Schild, Schildformat)
#### Generate dictionary to access the files from the filenames ######
PyramidenDictionary = makeitemNamenDictionary(Pyramidenbuchstaben)
BrailleDictionary = makeitemNamenDictionary(Braillebuchstaben)

##### Insert all the pyramid letters ####

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
#### Move the pyramid componenet so it is symetrical to the yz-plane ####
SchildBreite = adsk.core.ValueInput.createByReal(Vektor.x+0.5)
Vektor.x = -Vektor.x/2
MoveMatrix.translation = Vektor
PyramidenOcc.transform = MoveMatrix
design.snapshots.add()
#### Reset the Vektor and the MoveMatrix ####
Vektor.x = 0.33
MoveMatrix = adsk.core.Matrix3D.create()
MoveMatrix.translation = Vektor

#### Inserting the braille letters ####
for DateiName in BrailleDateinamenListe:
	Datei = BrailleDictionary[DateiName]
	Buchstabe = BrailleOccs.addByInsert(Datei, MoveMatrix, True)
	Vektor.x += 0.66
	MoveMatrix.translation = Vektor

Vektor.x = -(Vektor.x -0.33)/2
MoveMatrix.setToRotation(RadfuerDrehung, XVektor, Ursprung)
MoveMatrix.translation = Vektor
BrailleOcc.transform = MoveMatrix
design.snapshots.add()
##### Generate the Baseplate #####
### Generating the profile ####
BasisSkizze = root.sketches.add(root.yZConstructionPlane)
BasisKurven = BasisSkizze.sketchCurves
BasisLines = BasisKurven.sketchLines
Kurve1 = BasisKurven.sketchArcs.addByCenterStartSweep(Ursprung, BasisPunkt, RadfuerSeite1)
Kurve2 = BasisKurven.sketchArcs.addByCenterStartSweep(Ursprung, Kurve1.endSketchPoint, RadfuerSeite2)
Kurven = BasisSkizze.findConnectedCurves(Kurve1)
Offset = BasisSkizze.offset(Kurven, ObererPunkt, 0.2)
BasisLines.addByTwoPoints(Kurve1.startSketchPoint, Offset.item(0).startSketchPoint)
BasisLines.addByTwoPoints(Kurve2.endSketchPoint, Offset.item(1).endSketchPoint)
### Extrude the Profile ###

Profile = BasisSkizze.profiles.item(0)
RootExtrudes = root.features.extrudeFeatures
RootExtrudeInput = RootExtrudes.createInput(Profile, 3)
RootExtrudeInput.setSymmetricExtent(SchildBreite ,True)
Extrusion = RootExtrudes.add(RootExtrudeInput)

### Get the Bodies ###

Bodies = root.bRepBodies
Body = Bodies.item(0)

#### The Filet Process must be inserted after the combination process, but right now the item numbers are wrong #####
'''
edgeCollection1 = adsk.core.ObjectCollection.create();
edgeCollection2 = adsk.core.ObjectCollection.create();

edgeCollection1.add(Body.edges.item(0))
edgeCollection1.add(Body.edges.item(2))
edgeCollection1.add(Body.edges.item(7))
edgeCollection1.add(Body.edges.item(11))


RootFilets = root.features.filletFeatures
Filet1Input = RootFilets.createInput()
Filet2Input = RootFilets.createInput()
Filet1Input.addConstantRadiusEdgeSet(edgeCollection1, FilletRadius1, False)


Filet1 = RootFilets.add(Filet1Input)
UpperEdges = Body.faces.item(6).edges
for n in range(0,UpperEdges.count):
	edgeCollection2.add(UpperEdges.item(n))


Filet2Input.addConstantRadiusEdgeSet(edgeCollection2, FilletRadius2, False)
Filet2 = RootFilets.add(Filet2Input)'''
#### Combination and finish ###

RootCombines = root.features.combineFeatures

BuchstabenBodies = root.findBRepUsingPoint(Ursprung, 0, 40, True)
BuchstabenBodies.removeByItem(Body)
print(BuchstabenBodies.count)
CombineFeatures = root.features.combineFeatures
CombineInput = CombineFeatures.createInput(Body, BuchstabenBodies)
CombineInput.isKeepToolBodies = True
CombineInput.operation = 0
Combination = CombineFeatures.add(CombineInput)
for i in range(0, occs.count):
    occs.item(i).isLightBulbOn = False
