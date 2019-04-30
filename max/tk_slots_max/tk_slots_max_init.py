import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_ import Slot





class Init(Slot):
	def __init__(self, *args, **kwargs):
		super(Init, self).__init__(*args, **kwargs)

		
		# live surface #state and obj might need to be saved in external file
		# 'main' shorcut mode: ie. polygons, uv's, etc
		# pm.helpLine(width=20, height=8)
		# progress bar


	def info(self): #get current attributes. those with relavant values will be displayed.

		infoDict={}
		sel = rt.selection

		level = rt.subObjectLevel

		selCount = len(sel) #number of selected objects
		currentSelection = [str(s.name) for s in sel]; infoDict.update({str(selCount)+" Selected Objects: ":currentSelection}) #currently selected objects


		for obj in rt.selection:
			type_ = rt.classOf(obj)
			
			# if sel: numQuads = pm.polyEvaluate (selection[0], face=1); infoDict.update({"#Quads: ":numQuads}) #number of faces

			# symmetry = pm.symmetricModelling(query=1, symmetry=1);
			# if symmetry==1: symmetry=True; infoDict.update({"Symmetry State: ":symmetry}) #symmetry state
			# if symmetry: axis = pm.symmetricModelling(query=1, axis=1); infoDict.update({"Symmetry Axis: ":axis}) #symmetry axis

			# xformConstraint = pm.xformConstraint(query=True, type=True)
			# if xformConstraint=='none': xformConstraint=None; infoDict.update({"Xform Constrait: ":xformConstraint}) #transform constraits
			
			if type_=='Editable_Poly' or type_=='Edit_Poly':
				if level==1: #get vertex info
					selectedVerts = Init.bitArrayToArray(rt.polyop.getVertSelection(obj))
					print selectedVerts
					collapsedList = Init.collapseList(selectedVerts)
					print collapsedList
					numVerts = rt.polyop.getNumVerts(obj)
					infoDict.update({'Selected '+str(len(selectedVerts))+'/'+str(numVerts)+" Vertices: ":collapsedList}) #selected verts

				if level==2: #get edge info
					selectedEdges = Init.bitArrayToArray(rt.polyop.getEdgeSelection(obj))
					collapsedList = Init.collapseList(selectedEdges)
					numEdges = rt.polyop.getNumEdges(obj)
					infoDict.update({'Selected '+str(len(selectedEdges))+'/'+str(numEdges)+" Edges: ":collapsedList}) #selected edges
					
				if level==4: #get face info
					selectedFaces = Init.bitArrayToArray(rt.polyop.getFaceSelection(obj))
					collapsedList = Init.collapseList(selectedFaces)
					numFaces = rt.polyop.getNumFaces(obj)
					infoDict.update({'Selected '+str(len(selectedFaces))+'/'+str(numFaces)+" Faces: ":collapsedList}) #selected faces


			# selectedUVs = ; infoDict.update({"Selected UV's: ":selectedUVs}) #selected uv's

		prevCommand = self.sb.prevCommand(docString=True); infoDict.update({"Previous Command: ":prevCommand})  #get button text from last used command

		#populate the textedit with any values
		t = self.ui.t000
		t.clear()
		for key, value in infoDict.iteritems():
			if value:
				t.append(key+str(value))



	# ------------------------------------------------
	' Geometry'
	# ------------------------------------------------


	#--setSnapState--------------------------------------------------------------------------

	#set grid and snap settings on or off
	#state = string: "true", "false"
	@staticmethod
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



	@staticmethod
	def selectFaceLoop(tolerance, includeOpenEdges=False):

		maxEval('''
		selEdges = #{}
		theObj = $

		eCount = polyOp.getNumEdges theObj
		for e = 1 to eCount do
		(
			theFaces = (polyOp.getEdgeFaces theObj e) as array
			if theFaces.count == 2 then
			(
			 theAngle = acos(dot (polyOp.getFaceNormal theObj theFaces[1]) (polyOp.getFaceNormal theObj theFaces[2])) 
				if theAngle >= tolerance do selEdges[e] = true
			)	
			else 
				if includeOpenEdges do selEdges[e] = true
		)
		case classof (modPanel.getCurrentObject()) of
		(
			Editable_Poly: polyOp.setEdgeSelection theObj selEdges 
			Edit_Poly: (modPanel.getCurrentObject()).SetSelection #Edge &selEdges 
		)	
		redrawViews()
		''')


	#Get edges between min and max angle
	@staticmethod
	def getEdgesByAngle(minAngle, maxAngle):
		edgelist=[]
		for obj in rt.selection:

			for edge in list(range(1, obj.edges.count)):
				faces = rt.polyOp.getEdgeFaces(obj, edge)
				if faces.count==2:

					v1 = rt.polyop.getFaceNormal(obj, faces[0])
					v2 = rt.polyop.getFaceNormal(obj, faces[1])

					angle = rt.acos(rt.dot(rt.normalize(v1), rt.normalize(v2)))
					if angle >= minAngle and angle <= maxAngle:
						edgelist.append(edge)

			return edgelist


	#Detaches editable_mesh elements into new objects	
	@staticmethod
	def detachElement(obj):

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
	@staticmethod
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
	@staticmethod
	def scaleObject (size, x, y ,z):

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
		sel = self.getObjects ("Current", 0)

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
	@staticmethod
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
	@staticmethod
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
	@staticmethod
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



	#--getObjects-------------------------------------------------------------------------

	#builds a selection array, according to arguments.
	@staticmethod
	def getObjects(selectionType='current'):
		'''
		#args:
			selectionType='string' 
			'Current'	currently selected object/s
			'Geometry'	all geometry objects in scene
			'All'		all scene objects
		#returns:
			selection object as list
		'''

		selectionType = selectionType.title()

		if (selectionType == "Current"):
			sel = rt.selection

		if (selectionType == "Geometry"):
			sel = rt.geometry

		if (selectionType == "All"):
			sel = maxEval("sel = $*")
			sel = rt.sel

		
		if not sel:
			print "# Warning: Nothing selected. #"
			return None

		else:
			return [obj for obj in sel]



	#--filterSelectionByBaseClass-------------------------------------------------------------

	# returns the base class type as a string
	@staticmethod
	def filterSelectionByBaseClass(baseObjClass):
		'''
		#args:
			baseObjClass = <base class object>
		#returns:
			the type of base class object as a 'string'
		'''
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

		#Shapes.  If obj matches a shape object; return 'shape'
		shapes = [rt.Line, rt.Circle, rt.Arc, rt.NGon, rt.Text, rt.Egg, rt.Rectangle, rt.Ellipse, rt.Donut, rt.Star, rt.Helix, rt.Section]
		for key, value in shapes.iteritems():
			if obj == key:
				return "Shape"

		#Geometry.  If obj matches a geometry object; return 'geometry'
		geometry = [rt.Box, rt.Sphere, rt.Cylinder, rt.Torus, rt.Teapot, rt.TextPlus, rt.Cone, rt.GeoSphere, rt.Tube, rt.Pyramid, rt.Plane]
		for key, value in geometry.iteritems():
			if obj == key:
				return "Geometry"



	@staticmethod
	def getSuperClassType(superClass):
		'''
		#args:
			superClass = <super class object>
		#returns:
			the type of super class as a 'string'
		'''
		# If superclass obj matches a type; return type
		superClassDict = {rt.GeometryClass:"GeometryClass", rt.shape:"shape", rt.light:"light", rt.camera:"camera", rt.SpacewarpObject:"SpacewarpObject", rt.helper:"helper", rt.system:"system"}
		#rt.default: "default" #aka unknown type
		
		for key, value in superClassDict.iteritems():
				if (superClass == key):
					return value



	@staticmethod
	def getBaseObjectType(baseObjClass):
		#takes the base object class (ie. Editable_Poly) and ruturns the type as a string
		baseObjDict = {rt.Editable_Poly:"Editable_Poly", rt.Editable_mesh:"Editable_Mesh", rt.Editable_Patch:"Editble_Patch", rt.NURBSSurf:"NURBSSurf", rt.Box:"Box", rt.Sphere:"Sphere", rt.Cylinder:"Cylinder", rt.Torus:"Torus", rt.Teapot:"Teapot", rt.TextPlus:"TextPlus", rt.Cone:"Cone", rt.GeoSphere:"GeoSphere", rt.Tube:"Tube", rt.Pyramid:"Pyramid", rt.Plane:"Plane", rt.Line:"Line", rt.Circle:"Circle", rt.Arc:"Arc", rt.NGon:"NGon", rt.Text:"Text", rt.Egg:"Egg", rt.Rectangle:"Rectangle", rt.Ellipse:"Line", rt.Donut:"Donut", rt.Star:"Star", rt.Helix:"Helix", rt.Section:"Section"}

		for key, value in baseObjDict.iteritems():
			if (baseObjClass == key):
				return value



	#returns various object class information as elements in an array
	#calls filterSelectionByBaseClass()
	@staticmethod
	def classInfo (obj, query=False):
		'''
		#args:
			obj=<object>
			query=print results to console
		
		#returns:
			dictionary:
				object:----------------------	
				baseObject:------------------	
				superClass:------------------	
				superClass:|string|----------	
				baseObjectClass:-------------	
				baseObjectClass:|string|-----	
				baseObjectClass TYPE:|string|	
				isValidNode:|bool|-----------	
		'''
		if (obj == "noSelection"):
			return obj #rt.undefined

		baseObj = obj.baseObject
		baseObjClass = rt.classOf(baseObj) #get the base object class.  ie. Editable_Poly
		classTypeString = filterSelectionByBaseClass(baseObjClass) #func takes the base object class and returns the type as a string
		superClass = rt.superClassOf(obj)
		isValid = rt.isValidNode(obj)

		
		superClassString = getSuperClassType(superClass)
		baseObjectString = getBaseObjectType(baseObjClass)
		
		
		classInfoDict = {'object':obj, 'baseObject':baseObj, 'superClass':superClass, 'superClassString':superClassString, 'baseObjectClass':baseObjClass, 'baseObjectClassString':baseObjClassString, 'baseObjectClassType':classTypeString, 'isValidNode':isValid}

		
		if query:
			for key, value in classInfoDict.iteritems():
				print key+': ', value

		return classInfoDict


	@staticmethod
	def bitArrayToArray(bitArray):
		'''
		#args:
				bitArray=bit array
						*or list of bit arrays

		#returns:
				list containing indices of on (True) bits
		'''
		if type(bitArray[0])!=bool: #if list of bitArrays: flatten
			list_=[]
			for array in bitArray:
				list_.append([i+1 for i, bit in enumerate(array) if bit==1])
			return [bit for array in list_ for bit in array]

		return [i+1 for i, bit in enumerate(bitArray) if bit==1]


	@staticmethod
	def collapseList(list_):
		'''
		#args:
				list_=list - of integers
		#returns:
				list with sequencial integers collapsed in string format. ie. ['20', '22..28']
		'''
		ranges = []
		for x in list_:
			if not ranges:
				ranges.append([x])
			elif int(x)-prev_x == 1:
				ranges[-1].append(x)
			else:
				ranges.append([x])
			prev_x = int(x)

		collapsedList = ["..".join([r[0], r[-1]] if len(r) > 1 else r) for r in ranges]
		return collapsedList


	@staticmethod
	def convertToEditPoly(prompt=False):
		'''
		args:
			prompt=bool - prompt user before execution
		'''
		for obj in rt.selection:
			if prompt:
				if not rt.queryBox('Convert Object to Editable Poly?'):
					return
			
			rt.modPanel.setCurrentObject (obj.baseObject)
			
			mod = rt.Edit_Poly()
			rt.modpanel.addModToSelection(mod)

			index = rt.modPanel.getModifierIndex(obj, mod)
			rt.maxOps.CollapseNodeTo(obj, index, False)


	@staticmethod
	def toggleXraySelected():
		toggle = Slot.cycle([0,1], 'toggleXraySelected') #toggle 0/1

		for obj in rt.selection:
			obj.xray = toggle


	@staticmethod
	def toggleBackfaceCull():
		toggle = Slot.cycle([0,1], 'toggleBackfaceCull') #toggle 0/1

		for obj in rt.Geometry:
			obj.backfacecull = toggle


	@staticmethod
	def displayWireframeOnMesh(state=None, query=False):
		'''
		args:
			state=bool - display wireframe on mesh in viewport True/False
			query=bool - return current state
		returns:
			bool (current state) if query
		'''
		currentState = MaxPlus.ViewportManager.GetActiveViewportShowEdgeFaces()
		if query:
			return currentState
		if state:
			MaxPlus.ViewportManager.SetActiveViewportShowEdgeFaces(state)
		else:
			MaxPlus.ViewportManager.SetActiveViewportShowEdgeFaces(not currentState)



	previousSmoothPreviewLevel=int
	@staticmethod
	def toggleSmoothPreview():
		global previousSmoothPreviewLevel
		toggle = Slot.cycle([0,1], 'toggleSmoothPreview') #toggle 0/1

		geometry = rt.selection #if there is a selection; perform operation on those object/s
		if not len(geometry): #else: perform operation on all scene geometry.
			geometry = rt.geometry


		if toggle==0: #preview off
			# try: Init.setSubObjectLevel(previousSmoothPreviewLevel) #restore previous subObjectLevel
			# except: pass
			rt.showEndResult = False
			Init.displayWireframeOnMesh(True)

			for obj in geometry:
				try:
					mod = obj.modifiers['TurboSmooth'] or obj.modifiers['TurboSmooth_Pro'] or obj.modifiers['OpenSubDiv']
					mod.iterations = 0 #set subdivision levels to 0.
				except: pass

		else: #preview on
			# previousSmoothPreviewLevel = rt.subObjectLevel #store previous subObjectLevel
			# Init.setSubObjectLevel(0)
			rt.showEndResult = True
			Init.displayWireframeOnMesh(False)

			for obj in geometry:
				try:
					mod = obj.modifiers['TurboSmooth'] or obj.modifiers['TurboSmooth_Pro'] or obj.modifiers['OpenSubDiv']
					renderIters = mod.renderIterations #get renderIter value.
					mod.iterations = renderIters #apply to iterations value.
				except: pass

		rt.redrawViews() #refresh viewport. only those parts of the view that have changed are redrawn.



	@staticmethod
	def setSubObjectLevel(level):
		'''
		args:
			level=int  - set component mode
						0 - object mode
						1 - vertex
						2 - edge
						3 - border
						4 - face
						5 - element
		'''
		maxEval ('max modify mode')#set focus: modifier panel.

		sel = rt.selection

		for obj in sel:
			rt.modPanel.setCurrentObject (obj.baseObject)
			rt.subObjectLevel = level

			if level==0: #reset the modifier selection to the top of the stack.
				toggle = Slot.cycle([0,1], 'toggle_baseObjectLevel')
				if toggle:
					rt.modPanel.setCurrentObject(obj.baseObject)
				else:
					try: rt.modPanel.setCurrentObject(obj.modifiers[0])
					except: rt.modPanel.setCurrentObject(obj.baseObject) #if index error


	@staticmethod
	def undo(state=True):
		import pymxs
		pymxs.undo(state)
		return state



	# ------------------------------------------------
	' Ui'
	# ------------------------------------------------



	@staticmethod
	def maxUiSetChecked(id, table, item, state=True, query=False):
		#args: id='string' - actionMan ID
		#			table=int - actionMan table
		#			item=int - actionMan item number
		atbl = rt.actionMan.getActionTable(table)
		if atbl:
			aitm = atbl.getActionItem(item)
			if query:
				return aitm.isChecked
			else:
				if state: #check
					if not aitm.isChecked:
						rt.actionMan.executeAction(0, id)
						print aitm.isChecked
				else: #uncheck
					if aitm.isChecked:
						rt.actionMan.executeAction(0, id)
						print aitm.isChecked



	@staticmethod
	def viewPortMessage (message='', statusMessage='', assistMessage='', position='topCenter'):
		#args: statusMessage='string' - message to display (accepts html formatting).
		#			position='string' - position on screen. possible values are: topCenter","topRight","midLeft","midCenter","midCenterTop","midCenterBot","midRight","botLeft","botCenter","botRight"
		#ex. self.viewPortMessage("shutting down:<hl>"+str(timer)+"</hl>")
		message=statusMessage; statusMessage=''
		pm.inViewMessage(message=message, statusMessage=statusMessage, assistMessage=assistMessage, position=position, fontSize=10, fade=1, fadeInTime=0, fadeStayTime=1000, fadeOutTime=500, alpha=75) #1000ms = 1 sec









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------