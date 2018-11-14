from PySide2 import QtGui

import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_ import Slot





class Init(Slot):
	def __init__(self, *args, **kwargs):
		super(Init, self).__init__(*args, **kwargs)

		#init widgets
		self.initWidgets(self)


		# self.ui.t000.clearFocus()
		self.ui.t000.viewport().setAutoFillBackground(False)
		self.ui.t000.setTextBackgroundColor(QtGui.QColor(50, 50, 50))


		# live surface #state and obj might need to be saved in external file
		# 'main' shorcut mode: ie. polygons, uv's, etc
		# pm.helpLine(width=20, height=8)
		# progress bar


	def info(self): #get current attributes. those with relavant values will be displayed.
		info={}
		# selection = pm.ls(selection=1)
		# objects = pm.ls(selection=1, objectsOnly=1)
		# value = len(objects); info.update({"selected objects: ":value}) #number of selected objects
		# currentSelection = [str(s) for s in pm.ls (selection=1)]; info.update({"Current Selection: ":currentSelection}) #currently selected objects
		
		# if selection: numQuads = pm.polyEvaluate (selection[0], face=1); info.update({"Num Quads: ":numQuads}) #number of faces

		# symmetry = pm.symmetricModelling(query=1, symmetry=1);
		# if symmetry==1: symmetry=True; info.update({"symmetry: ":symmetry}) #symmetry state
		# if symmetry: axis = pm.symmetricModelling(query=1, axis=1); info.update({"symmetry axis: ":axis}) #symmetry axis

		# xformConstraint = pm.xformConstraint(query=True, type=True)
		# if xformConstraint=='none': xformConstraint=None; info.update({"xform constrait: ":xformConstraint}) #transform constraits

		# value = pm.polyEvaluate(vertexComponent=1); info.update({"selected vertices: ":value}) #selected verts
		# value = pm.polyEvaluate(edgeComponent=1); info.update({"selected edges: ":value}) #selected edges
		# value = pm.polyEvaluate(faceComponent=1); info.update({"selected faces: ":value}) #selected faces
		# value = pm.polyEvaluate(uvComponent=1); info.update({"selected uv's: ":value}) #selected uv's

		#populate the textedit with any values
		for key, value in info.iteritems():
			if value:
				# self.ui.t000.setText(key+str(value)+'<br>') #<br> html break newline
				self.ui.t000.setHtml(key+str(value)+'<br>') #<br> html break newline





	# ------------------------------------------------
	' Geometry'
	# ------------------------------------------------








	#--makeSelection-------------------------------------------------------------------------

	# class Selection:

	#builds a selection array, according to arguments.
	#arg = selection type. "Current", "Geometry", "All"
	#index = index of array element to return. 0 = all
	#functionCall; if specified will call the specified fuction with selection as argument
	def makeSelection (selectionType, arrayIndex, functionCall=None):

		if (selectionType == "Current"):
			maxEval("sel = $") #store FPValue
			sel = rt.sel	#get FPValue

		if (selectionType == "Geometry"):
			maxEval("sel = Geometry")
			sel = rt.sel

		if (selectionType == "All"):
			sel = maxEval("sel = $*")
			sel = rt.sel

		selectionArray = []
		
		if (sel < 1): # check if sel is empty
			print "-< Nothing selected >-"
			return "noSelection" #or rt.undefined

		if (len(sel) == 0): #check if selection is not an array
			selectionArray.append(sel)
			
		else: #else if array, build python array
			for obj in sel:
				selectionArray.append(obj)

		if (arrayIndex == 0):
			#~ print selectionArray
			if (functionCall != None):
				return functionCall(selectionArray);
			else:
				return selectionArray

		if (arrayIndex >= 1): #subtract one index position to match maxscript convention
			#~ print selectionArray[arrayIndex]
			if (functionCall != None):
				return functionCall(selectionArray[arrayIndex-1]); 
			else:
				return selectionArray[arrayIndex-1];











	#--setSnapState--------------------------------------------------------------------------

	#set grid and snap settings on or off
	#state = string: "true", "false"
	def setSnapState (state):

		maxEval('''
		state = false
		if (state == "true") then
		(
			state = true
		)

		/*grid and snap settings*/

		/*body shapes*/
		snapmode.setOSnapItemActive 1 1 (state);
		snapmode.setOSnapItemActive 1 2 (state);
		snapmode.setOSnapItemActive 1 3 (state);
		snapmode.setOSnapItemActive 1 4 (state);
		snapmode.setOSnapItemActive 1 5 (state);
		/*nurbs*/	
		snapmode.setOSnapItemActive 2 1 (state);
		snapmode.setOSnapItemActive 2 2 (state);
		snapmode.setOSnapItemActive 2 3 (state);
		snapmode.setOSnapItemActive 2 4 (state);
		snapmode.setOSnapItemActive 2 5 (state);
		snapmode.setOSnapItemActive 2 6 (state);
		snapmode.setOSnapItemActive 2 7 (state);
		snapmode.setOSnapItemActive 2 8 (state);
		snapmode.setOSnapItemActive 2 9 (state);
		snapmode.setOSnapItemActive 2 10 (state);
		/*Point Cloud Shapes*/
		snapmode.setOSnapItemActive 3 1 (state);
		/*standard*/
		snapmode.setOSnapItemActive 4 1 (state);
		snapmode.setOSnapItemActive 4 2 (state);
		/*standard*/
		snapmode.setOSnapItemActive 5 1 (state);
		snapmode.setOSnapItemActive 5 2 (state);
		/*standard*/
		snapmode.setOSnapItemActive 6 1 (state);
		snapmode.setOSnapItemActive 6 2 (state);
		/*standard*/
		snapmode.setOSnapItemActive 7 1 (state);
		snapmode.setOSnapItemActive 7 2 (state);
		snapmode.setOSnapItemActive 7 3 (state);
		snapmode.setOSnapItemActive 7 4 (state);
		snapmode.setOSnapItemActive 7 5 (state);
		snapmode.setOSnapItemActive 7 6 (state);
		''')


	#Detaches editable_mesh elements into new objects	
	def detachElement (obj):

		elementArray = []

		print obj[0] #object
		print obj[6] #baseObject class TYPE |string|
		print obj[7] #isValidNode

		if (obj[4] == rt.Editable_Poly and obj[7]): #or obj[6] == "Shape" or obj[6] == "Geometry" 

			rename = obj[0].name	
			rename += "_ele"
			#~ maxEval("undo \"DetachToElement\" on")
			while ((rt.polyOp.getNumFaces(obj[0])) > 0):
				elementToDetach = rt.polyOp.getElementsUsingFace(obj[0],[1]) #(1)
				rt.polyOp.detachFaces(obj[0], elementToDetach, delete=True, asNode=True, name=rename)
			rt.delete(obj[0])
			elementArray = rt.execute("$"+rename+"*")

			rt.select(elementArray)

		else:
			print "-< Object must be an Editable_Poly >-"
		
		return elementArray



	#--alignVertices-------------------------------------------------------------------------

	#align vertices
	# 'vertex.pos.x = vertPosX' ect doesnt work. had to use maxscript
	# selection: as array
	# mode:
	# 0 - YZ
	# 1 - XZ
	# 2 - XY
	# 3 -  X
	# 4 -  Y
	# 5 -  Z
	#notes: (align all vertices at once) by putting each vert index and coordinates in a dict (or two arrays) then if when iterating through a vert falls within the tolerance specified in a textfield align that vert in coordinate. then repeat the process for the other coordinates x,y,z specified by checkboxes. using edges may be a better approach. or both with a subObjectLevel check
	#create edge alignment tool and then use subObjectLevel check to call either that function or this one from the same buttons.
	#to save ui space; have a single align button, x, y, z, and align 'all' checkboxes and a tolerance textfield.
	def alignVertices (selection, mode):

		# maxEval('undo "alignVertices" on')

		componentArray = selection.selectedVerts
		
		if len(componentArray) == 0:
			print "No vertices selected"
		
		if len(componentArray) < 2:
			print "Selection must contain at least two vertices"
			return
		
		lastSelected = componentArray[-1]#3ds max re-orders array by vert index, so this doesnt work for aligning to last selected
		#~ print lastSelected.pos
		aX = lastSelected.pos[0]
		aY = lastSelected.pos[1]
		aZ = lastSelected.pos[2]
		
		for vertex in componentArray:
			#~ print vertex.pos
			vX = vertex.pos[0]
			vY = vertex.pos[1]
			vZ = vertex.pos[2]

			maxEval('global alignXYZ')
			
			if mode == 0: #align YZ
				maxEval('''
				fn alignXYZ mode vertex vX vY vZ aX aY aZ=
				(
					vertex.pos.x = vX
					vertex.pos.y = aY
					vertex.pos.z = aZ
				)
				''')
				
			if mode == 1: #align XZ
				maxEval('''
				fn alignXYZ mode vertex vX vY vZ aX aY aZ=
				(
					vertex.pos.x = aX
					vertex.pos.y = vY
					vertex.pos.z = aZ
				)
				''')
			
			if mode == 2: #align XY
				maxEval('''
				fn alignXYZ mode vertex vX vY vZ aX aY aZ=
				(
					vertex.pos.x = aX
					vertex.pos.y = aY
					vertex.pos.z = vZ
				)
				''')
			
			if mode == 3: #X
				maxEval('''
				fn alignXYZ mode vertex vX vY vZ aX aY aZ=
				(
					vertex.pos.x = aX
					vertex.pos.y = vY
					vertex.pos.z = vZ
				)
				''')
			
			if mode == 4: #Y
				maxEval('''
				fn alignXYZ mode vertex vX vY vZ aX aY aZ=
				(
					vertex.pos.x = vX
					vertex.pos.y = aY
					vertex.pos.z = vZ
				)
				''')
			
			if mode == 5: #Z
				maxEval('''
				fn alignXYZ mode vertex vX vY vZ aX aY aZ=
				(
					vertex.pos.x = vX
					vertex.pos.y = vY
					vertex.pos.z = aZ
				)
				''')
			
			print 100*"-"
			print "vertex.index:", vertex.index
			print "position:", vX, vY, vZ
			print "align:   ", aX, aY, aZ
			
			rt.alignXYZ(mode, vertex, vX, vY, vZ, aX, aY, aZ)
			
			print "result:  ", vertex.pos[0], vertex.pos[1], vertex.pos[2]



	#--scaleObject--------------------------------------------------------------------------

	#'s' argument is a textfield scale amount
	#'x,y,z' arguments are checkbox boolean values. 
	#basically working except for final 'obj.scale([s, s, s])' command in python. variable definitions included for debugging. to get working an option is to use the maxEval method in the alignVertices function.
	def scaleObject (size, x, y ,z):
		# global tk_textField__000
		tk_textField_000 = 1.50
		tk_isChecked_002 = True
		tk_isChecked_003 = True
		tk_isChecked_004 = True

		s = tk_textField_000
		x = tk_isChecked_002
		y = tk_isChecked_003
		z = tk_isChecked_004
		#-------------------------
		s = size
		sel = makeSelection ("Current", 0)

		for obj in sel:
			if (tk_isChecked_002 and tk_isChecked_003 and tk_isChecked_004):
				obj.scale([s, s, s])
			if (not tk_isChecked_002 and tk_isChecked_003 and tk_isChecked_004):
				obj.scale([1, s, s])
			if (tk_isChecked_002 (not tk_isChecked_003) and tk_isChecked_004):
				obj.scale([s, 1, s])
			if (tk_isChecked_002 and tk_isChecked_003 (not tk_isChecked_004)):
				obj.scale([s, s, 1])
			if (not tk_isChecked_002 (not tk_isChecked_003) and tk_isChecked_004):
				obj.scale([1, 1, s])
			if (tk_isChecked_002 (not tk_isChecked_003) (not tk_isChecked_004)):
				obj.scale([s, 1, 1])
			if (tk_isChecked_002 and tk_isChecked_003 and tk_isChecked_004):
				obj.scale([1, s, 1])
			if (not tk_isChecked_002 (not tk_isChecked_003) (not tk_isChecked_004)):
				obj.scale([1, 1, 1])




	#--ExtrudeObject------------------------------------------------------------------------

	#extrudes one object at a time but can be called repeatedly for an array of selected objects
	#takes classString as an argument which is an array containing the object and class information
	#~ --	[0] --object
	#~ --	[1] --baseObject
	#~ -- [4] --baseObject class
	#~ -- [6] --baseObject class type string. eg. Editable,Shape,Geometry
	#notes: in another function; if selection (subobjectlevel) is == face or edge, store that face if necessary in an array and then extrude by a certain amount (if needed surface normal direction). then switch to move tool (calling a center pivot on component if needed) so that the extrude can be manipulated with widget instead of spinner.
	def extrudeObject (objects):
		if (objects == rt.undefined or objects == "noSelection"):
			print "Nothing selected. Returned string: noSelection"
			return "noSelection"

		for obj in objects:
			
			classString = classInfo(obj)
			
			if (classString[6] == "Editable_Poly" or classString[4] == rt.Editable_mesh): #had to add Editable_mesh explicitly, here and in the error catch, because the keyword was unknown to pymxs.runtime. added it to the called function anyhow in case they fix it at some point
				maxEval('macros.run "Modifiers" "Face_Extrude"')
				print classString[4]
				
			if (classString[6] == "Shape"):
				#if 'convert to mesh object' checkbox true convert currently selected:
				if (tk_isChecked_000 == True):
					maxEval('''
					convertTo $ PolyMeshObject; --convert to poly
					macros.run "Modifiers" "Face_Extrude"; --extrude modifier
					''')
				else:
					maxEval('macros.run "Modifiers" "Extrude"')
				print classString[4]

			if (classString[6] == "Geometry"):
				#if 'convert to mesh object' checkbox true convert currently selected:
				if (tk_isChecked_000 == True):
					maxEval('''
					convertTo $ TriMeshGeometry; --convert to mesh object
					maxEval('macros.run "Modifiers" "Face_Extrude"; --extrude
					''')

			#else, if undefined..
			else:
				print "::unknown object type::"
				print classString[4]

			if (objects.count > 1):
				rt.deselect(classString[0])
			
		if (objects.count > 1): #reselect all initially selected nodes
			rt.clearSelection()
			for obj in objects:
				rt.selectMore(obj)


	#--centerPivotOnSelection----------------------------------------------------------------

	def centerPivotOnSelection ():

		#Get the face vertices, add their positions together, divide by the number of the vertices 
		#- that's your centerpoint.

		# the above method will get you the average position of the vertices that constitute the 
		#faces in question. For the center of the bounds of these vertices (if that's of interest 
		#to you), you'll need to get the min position and the max position of the vertex set and 
		#then calculate the median position:
		#p3_minPosition + P3_maxPosition / 2 -- The min and the max position values contain the 
		#minimum x, y and z values and the maximum x, y and z values of the vertex set 
		#respectively. That is to say, for example, that the min x value may come from a 
		#different vert than the min y value.

		#component bounding box method:
		#two bits of code written by anubis will need cleaning up, but might be helpful
	# 	(	
	# 	if selection.count == 1 and classOf (curO = selection[1]) == Editable_Poly do
	# 	(
	# 		if (selFacesBA = polyop.getFaceSelection curO).numberset != 0 do
	# 		(
	# 			faceVertsBA = polyop.getVertsUsingFace curO selFacesBA
	# 			with redraw off 
	# 			(
	# 				tMesh = mesh mesh:curO.mesh
	# 				tMesh.pos = curO.pos
	# 				tMesh.objectOffsetPos = curO.objectOffsetPos
	# 				if faceVertsBA.count > 0 do 
	# 				(
	# 					delete tMesh.verts[((tMesh.verts as BitArray) - (faceVertsBA))]
	# 				)
	# 				c = snapshot tMesh
	# 				c.transform = matrix3 1
	# 				d = dummy boxsize:(c.max - c.min)
	# 				delete c
	# 				d.transform = tMesh.transform
	# 				d.pos = tMesh.center
	# 				d.name = tMesh.name + "_box"
	# 				delete tMesh
	# 			)
	# 		)
	# 	)
	# )


		pass



	#third party script to return node information
	def getElements(node):
		obj = node.GetObject()
		objTriMesh = obj.AsTriObject()
		objMesh = objTriMesh.GetMesh()

		numVerts = objMesh.GetNumVertices()
		numFaces = objMesh.GetNumFaces()

		allElements = []

		faces = MaxPlus.BitArray(numFaces)
		faces.SetAll()
		verts = [[] for i in range(numVerts)]

		for i in range(0, numFaces):
			face = objMesh.GetFace(i)
		for k in range(0,3):
			verts[face.GetVert(k)].append(i)

		for i in range(0, numFaces): 
			if faces[i]:

				element = []
				element.append(i)
				faceBits = MaxPlus.BitArray(numFaces)
				vertBits = MaxPlus.BitArray(numVerts)

				#for j in range(0, len(element)):
				j = 0
				while j < len(element):
					fi = element[j]
					j += 1

				if not faceBits[fi]:
					face = objMesh.GetFace(fi)

				for k in range(0,3):
					v = face.GetVert(k)

				if vertBits[v]:
					continue

		for singleFace in range(0, len(verts[v])):
			element.append(verts[v][singleFace])
			vertBits.Set(v, True)

			faceBits.Set(fi, True)
			faces.Clear(fi)

			allElements.append(MaxPlus.BitArray(faceBits))

		return allElements







	# ------------------------------------------------
	' DAG objects'
	# ------------------------------------------------




	#--filterSelectionByBaseClass-------------------------------------------------------------

	# returns the base class type as a string
	def filterSelectionByBaseClass (baseObjClass):
		
		obj = baseObjClass

		#Editable Mesh
		if (obj == rt.Editable_Poly):
			return "Editable_Poly"
		
		if (obj == rt.Editable_Patch): #no pymxs.runtime attribute Editable_Patch
			return "Editable_Patch"
		
		if (obj == rt.Editable_mesh): #no pymxs.runtime attribute Editable_mesh
			return "Editable_Mesh"
			
		if (obj == rt.NURBSSurf): #no pymxs.runtime attribute NURBSSurf
			return "NURBSSurf"

		#Shapes
		if (obj == rt.Line or \
			obj == rt.Circle or \
			obj == rt.Arc or \
			obj == rt.NGon or \
			obj == rt.Text or \
			obj == rt.Egg or \
			obj == rt.Rectangle or \
			obj == rt.Ellipse or \
			obj == rt.Donut or \
			obj == rt.Star or \
			obj == rt.Helix or \
			obj == rt.Section):
			return "Shape"

		#Geometry
		if (obj == rt.Box or \
			obj == rt.Sphere or \
			obj == rt.Cylinder or \
			obj == rt.Torus or \
			obj == rt.Teapot or \
			obj == rt.TextPlus or \
			obj == rt.Cone or \
			obj == rt.GeoSphere or \
			obj == rt.Tube or \
			obj == rt.Pyramid or \
			obj == rt.Plane):
			return "Geometry"

	#--classInfo-----------------------------------------------------------------------------

	#returns various object class information as elements in an array
	#calls filterSelectionByBaseClass()
	def classInfo (obj, query=False):
		#functions used:
		#~ filterSelectionByBaseClass()

		if (obj == "noSelection"):
			return obj #rt.undefined

		baseObj = obj.baseObject
		baseObjClass = rt.classOf(baseObj) #get the base object class.  ie. Editable_Poly
		classTypeString = filterSelectionByBaseClass(baseObjClass) #func takes the base object class and returns the type as a string
		superClass = rt.superClassOf(obj)
		isValid = rt.isValidNode(obj)
		subObjectLevel = rt.getSelectionLevel(obj)
		
		# selectedVerts = rt.selectedVerts(obj)
		# selectedEdges = rt.selectedEdges(obj)
		# selectedFaces = rt.selectedFaces(obj)
		
		# numOfVerts = objMesh.GetNumVertices()
		# numOfFaces = objMesh.GetNumFaces()
		
		# faceBitArray = MaxPlus.BitArray(numFaces)
		# vertBitArray = MaxPlus.BitArray(numVerts)
		
		superClassString = "superClass: Unknown"
		if (superClass == rt.GeometryClass):
			superClassString = "GeometryClass"
		if (superClass == rt.shape):
			superClassString = "shape"
		if (superClass == rt.light):
			superClassString = "light"
		if (superClass == rt.camera):
			superClassString = "camera"
		if (superClass == rt.SpacewarpObject):
			superClassString = "SpacewarpObject"
		if (superClass == rt.helper):
			superClassString = "helper"
		if (superClass == rt.system):
			superClassString = "system"
		#rt.default: "default" #aka unknown type


		baseObjClassString = "objectClass: Unknown"
		if (baseObjClass == rt.Editable_Poly):
			baseObjClassString = "Editable_Poly"
		if (baseObjClass == rt.Editable_mesh):
			baseObjClassString = "Editable_Mesh"
		if (baseObjClass == rt.Editable_Patch):
			baseObjClassString = "Editble_Patch"
		if (baseObjClass == rt.NURBSSurf):
			baseObjClassString = "NURBSSurf"
		if (baseObjClass == rt.Box):
			baseObjClassString = "Box"
		if (baseObjClass == rt.Sphere):
			baseObjClassString = "Sphere"
		if (baseObjClass == rt.Cylinder):
			baseObjClassString = "Cylinder"
		if (baseObjClass == rt.Torus):
			baseObjClassString = "Torus"
		if (baseObjClass == rt.Teapot):
			baseObjClassString = "Teapot"
		if (baseObjClass == rt.TextPlus):
			baseObjClassString = "TextPlus"
		if (baseObjClass == rt.Cone):
			baseObjClassString = "Cone"
		if (baseObjClass == rt.GeoSphere):
			baseObjClassString = "GeoSphere"
		if (baseObjClass == rt.Tube):
			baseObjClassString = "Tube"
		if (baseObjClass == rt.Pyramid):
			baseObjClassString = "Pyramid"
		if (baseObjClass == rt.Plane):
			baseObjClassString = "Plane"
		if (baseObjClass == rt.Line):
			baseObjClassString = "Line"
		if (baseObjClass == rt.Circle):
			baseObjClassString = "Circle"
		if (baseObjClass == rt.Arc):
			baseObjClassString = "Arc"
		if (baseObjClass == rt.NGon):
			baseObjClassString = "NGon"
		if (baseObjClass == rt.Text):
			baseObjClassString = "Text"
		if (baseObjClass == rt.Egg):
			baseObjClassString = "Egg"
		if (baseObjClass == rt.Rectangle):
			baseObjClassString = "Rectangle"
		if (baseObjClass == rt.Ellipse):
			baseObjClassString = "Line"
		if (baseObjClass == rt.Donut):
			baseObjClassString = "Donut"
		if (baseObjClass == rt.Star):
			baseObjClassString = "Star"
		if (baseObjClass == rt.Helix):
			baseObjClassString = "Helix"
		if (baseObjClass == rt.Section):
			baseObjClassString = "Section"

		
		returnedClassInfoArray = []
		returnedClassInfoArray.append(obj)
		returnedClassInfoArray.append(baseObj)
		returnedClassInfoArray.append(superClass)
		returnedClassInfoArray.append(superClassString)
		returnedClassInfoArray.append(baseObjClass)
		returnedClassInfoArray.append(baseObjClassString)
		returnedClassInfoArray.append(classTypeString)
		returnedClassInfoArray.append(isValid)
		returnedClassInfoArray.append(subObjectLevel)
		# returnedClassInfoArray.append(selectedVerts)
		# returnedClassInfoArray.append(selectedEdges)
		# returnedClassInfoArray.append(selectedFaces)
		# returnedClassInfoArray.append(numberOfVerts)
		# returnedClassInfoArray.append(numberOfFaces)
		# returnedClassInfoArray.append(vertBitArray)
		# returnedClassInfoArray.append(faceBitArray)
		
		
		if (query == True):
			#python index / maxscript array index starting at 1
			print "0-1---object:----------------------", returnedClassInfoArray[0]
			print "1-2---baseObject:------------------", returnedClassInfoArray[1]
			print "2-3---superClass:------------------", returnedClassInfoArray[2]
			print "3-4---superClass:|string|----------", returnedClassInfoArray[3]
			print "4-5---baseObjectClass:-------------", returnedClassInfoArray[4]
			print "5-6---baseObjectClass:|string|-----", returnedClassInfoArray[5]
			print "6-7---baseObjectClass TYPE:|string|", returnedClassInfoArray[6] #eg. Editable,Shape,Geometry
			print "7-8---isValidNode:|bool|-----------", returnedClassInfoArray[7] #True, False, 1, 0
			print "8-9---subObjectLevel:|int|---------", returnedClassInfoArray[8] #[mesh] 0=object level,1=vertex level,2=edge level,3=face,4=polygon,5=element,[poly] 0=object level,1=vertex level,2=edge level,3=border,4=polygon,5=element
			# print "9-10--selectedVerts:|array|--------", returnedClassInfoArray[9] #selectedVerts
			# print "10-11-selectedEdges:|array|--------", returnedClassInfoArray[10] #selectedEdges
			# print "11-12-selectedFaces:|array|--------", returnedClassInfoArray[11] #selectedFaces
			# print "12-13-numberOfVerts:|int|----------", returnedClassInfoArray[12] #number of selected vertices
			# print "13-14-numberOfFaces:|int|----------". returnedClassInfoArray[13] #number of selected faces
			# print "14-15-vertBitArray:----------------", returnedClassInfoArray[14]
			# print "15-16-faceBitArray:----------------", returnedClassInfoArray[15]
			print "="*40

		return returnedClassInfoArray









	# ------------------------------------------------
	' Ui'
	# ------------------------------------------------







	def viewPortMessage (message='', statusMessage='', assistMessage='', position='topCenter'):
		#args: statusMessage='string' - message to display (accepts html formatting).
		#			position='string' - position on screen. possible values are: topCenter","topRight","midLeft","midCenter","midCenterTop","midCenterBot","midRight","botLeft","botCenter","botRight"
		#ex. func.viewPortMessage("shutting down:<hl>"+str(timer)+"</hl>")
		message=statusMessage; statusMessage=''
		pm.inViewMessage(message=message, statusMessage=statusMessage, assistMessage=assistMessage, position=position, fontSize=10, fade=1, fadeInTime=0, fadeStayTime=1000, fadeOutTime=500, alpha=75) #1000ms = 1 sec









#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------