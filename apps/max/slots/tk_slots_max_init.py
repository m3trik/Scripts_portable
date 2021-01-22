from __future__ import print_function
from builtins import super
import os

from PySide2 import QtGui, QtWidgets, QtCore

from ui import widgets as wgts
from tk_slots import Slots

# 3ds Max dependancies
try:
	import MaxPlus
	from pymxs import runtime as rt
	maxEval = MaxPlus.Core.EvalMAXScript

except ImportError as error:
	print(error)
	def p(s): pass
	maxEval = p
	rt = None



class Init(Slots):
	'''App specific methods inherited by all other slot classes.
	'''
	def __init__(self, *args, **kwargs):
		super(Init, self).__init__(*args, **kwargs)

		try:
			self.init_ui.hud.shown.connect(self.construct_hud)
		except AttributeError: #(an inherited class)
			pass


	def construct_hud(self):
		'''Add current scene attributes to a lineEdit.
		Only those with relevant values will be displayed.
		'''
		hud = self.init_ui.hud

		try:
			selection = rt.selection
		except AttributeError:
			return

		if selection:
			if len(selection) is 1:
				obj = selection[0]
				symmetry = obj.modifiers[rt.Symmetry]
				if symmetry:
					int_ = symmetry.axis
					axis = {0:'x', 1:'y', 2:'z'}
					hud.insertText('Symmetry Axis: <font style="color: Yellow;">{}'.format(axis[int_].upper())) #symmetry axis

			level = rt.subObjectLevel
			if level==0: #object level
				name_and_type = ['<font style="color: Yellow;">{0}<font style="color: LightGray;">:{1}'.format(obj.name, rt.classOf(obj.baseObject)) for obj in selection]
				name_and_type_str = str(name_and_type).translate(None, '[]\'') #format as single string.
				hud.insertText('Selected: <font style="color: Yellow;">{}'.format(name_and_type_str)) #currently selected objects

				# xformConstraint = pm.xformConstraint(query=True, type=True)
				# if xformConstraint=='none':
				# 	xformConstraint=None
				# if xformConstraint:
				# 	hud.insertText('Xform Constrait: <font style="color: Yellow;">{}'.format(xformConstraint)) #transform constraits

			elif level>0: #component level
				obj = selection[0]
				objType = rt.classOf(obj.baseObject)
				if objType=='Editable_Poly' or objType=='Edit_Poly':
					if level==1: #get vertex info
						type_ = 'Verts'
						selected = Init.bitArrayToArray(rt.polyop.getVertSelection(obj))
						total_num = rt.polyop.getNumVerts(obj)

					elif level==2: #get edge info
						type_ = 'Edges'
						selected = Init.bitArrayToArray(rt.polyop.getEdgeSelection(obj))
						total_num = rt.polyop.getNumEdges(obj)

					elif level==3: #get border info
						type_ = 'Borders'
						# rt.polyop.SetSelection #Edge ((polyOp.getOpenEdges $) as bitarray)
						selected = Init.bitArrayToArray(rt.polyop.getBorderSelection(obj))
						total_num = rt.polyop.getNumBorders(obj)

					elif level==4: #get face info
						type_ = 'Faces'
						selected = Init.bitArrayToArray(rt.polyop.getFaceSelection(obj))
						total_num = rt.polyop.getNumFaces(obj)

					elif level==5: #get element info
						type_ = 'Elements'
						selected = Init.bitArrayToArray(rt.polyop.getElementSelection(obj))
						total_num = rt.polyop.getNumElements(obj)

					num_selected = len(selected)
					if all((type_, num_selected, total_num)):
						hud.insertText('Selected {}: <font style="color: Yellow;">{} <font style="color: LightGray;">/{}'.format(type_, num_selected, total_num)) #selected components


		prevCommand = self.sb.prevCommand(docString=True)
		if prevCommand:
			hud.insertText('Prev Command: <font style="color: Yellow;">{}'.format(prevCommand))  #get button text from last used command

		# prevUi = self.sb.previousName(omitLevel=[0,1,2])
		# hud.insertText('Prev UI: {}'.format(prevUi.replace('_', '').title())) #get the last level 3 ui name string.

		# prevCamera = self.sb.prevCamera(docString=True)
		# hud.insertText('Prev Camera: {}'.format(prevCamera)) #get the previously used camera.






	# # ------------------------------------------------
	' DAG Objects'
	# # ------------------------------------------------


	@staticmethod
	def getAttributesMax(node, include=[], exclude=[]):
		'''Get node attributes and their corresponding values as a dict.

		:Parameters:
			node (obj) = Transform node.
			include (list) = Attributes to include. All other will be omitted. Exclude takes dominance over include. Meaning, if the same attribute is in both lists, it will be excluded.
			exclude (list) = Attributes to exclude from the returned dictionay. ie. [u'Position',u'Rotation',u'Scale',u'renderable',u'isHidden',u'isFrozen',u'selected']

		:Return:
			(dict) {'string attribute': current value}

		# print (rt.showProperties(obj))
		# print (rt.getPropNames(obj))
		'''
		if not all((include, exclude)):
			exclude = ['getmxsprop', 'setmxsprop', 'typeInHeight', 'typeInLength', 'typeInPos', 'typeInWidth', 'typeInDepth', 
				'typeInRadius', 'typeInRadius1', 'typeInRadius2', 'typeinCreationMethod', 'edgeChamferQuadIntersections', 
				'edgeChamferType', 'hemisphere', 'realWorldMapSize', 'mapcoords']

		attributes = {attr:node.getmxsprop(attr) for attr in [str(n) for n in rt.getPropNames(node)] 
				if not attr in exclude and (attr in include if include else attr not in include)}

		return attributes


	@staticmethod
	def setAttributesMax(node, attributes):
		'''Set history node attributes using the transform node.

		:Parameters:
			node (obj) = Transform node.
			attributes (dict) = Attributes and their correponding value to set. ie. {'string attribute': value}
		'''
		[setattr(node, attribute, value) for attribute, value in attributes.items() 
		if attribute and value]

		rt.redrawViews()






	# ------------------------------------------------
	' Geometry'
	# ------------------------------------------------

	@staticmethod
	def selectFaceLoop(tolerance, includeOpenEdges=False):
		'''
		:Parameters:
			tolerance (float) = Face normal tolerance.
			includeOpenEdges (bool) = 
		'''
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


	def circularize(self):
		'''Circularize a set of vertices on a circle or an elipse.

		tm = (matrix3 [-0.99596,0.022911,-0.0868241] [-0.0229109,0.870065,0.492404] [0.086824,0.492404,-0.866025] [-18.3751,-66.1508,30.969])
		c = [-18.3751,-66.1508,30.969]
		s = [-123.81,-63.7254,21.7775]
		u = [0.086824,0.492404,-0.866025]

		pCircle = pointCircle c s u 20
		'''
		maxEval('''
		fn pointCircle center startPoint upVector n = (
			rad = distance center startPoint
			dir = normalize (startPoint - center)
			crossVector = normalize (cross (normalize (startPoint - center)) upVector)
			tm = (matrix3 upVector crossVector dir center)

			p3Array = #()

			for i = 1 to n do (
				preRotateX tm (360.0 / n)
				append p3Array ([0,0,rad] * tm)
			)

			return p3Array
		)
		pointCircle()
		''')


	@staticmethod
	def getEdgesByAngle(minAngle, maxAngle):
		'''Get edges between min and max angle.

		:Parameters:
			minAngle (float) = minimum search angle tolerance.
			maxAngle (float) = maximum search angle tolerance.

		:Return:
			(list) edges within the given range.
		'''
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


	@Slots.message
	def detachElement(self, obj):
		'''Detach editable_mesh elements into new objects.

		:Parameters:
			obj (obj) = polygon object.

		:Return:
			(list) detached objects.
		'''
		elementArray = []

		print(obj[0]) #object
		print(obj[6]) #baseObject class TYPE |string|
		print(obj[7]) #isValidNode

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
			return 'Error: Object must be an Editable_Poly.'
		
		return elementArray


	@property
	def currentSelection(self):
		'''Gets the currently selected objects or object components.

		:Return:
			(array) current selection as a maxscript array.
		'''
		sel = rt.selection
		if not sel:
			return 'Error: Nothing Selected.'

		level = rt.subObjectLevel
		if level in (0, None): #objs
			s = [i for i in sel]
		elif level==1: #verts
			s = Init.getSelectedVertices(sel[0])
		elif level==2: #edges
			s = Init.getSelectedEdges(sel[0])
		elif level==3: #borders
			s = rt.getBorderSelection(sel[0])
		elif level==4: #faces
			s = Init.getSelectedFaces(sel[0])

		return rt.array(*s) #unpack list s and convert to an array.


	@staticmethod
	def getVertices(obj):
		'''Get a list of vertices of a given object whether it is an editable mesh or polygon.

		:Parameters:
			obj (obj) = polygon or mesh object.

		:Return:
			(list) vertex list.		
		'''
		try:
			vertices = Init.bitArrayToArray(rt.polyop.getVertSelection(obj)) #polygon
		except:
			vertices = Init.bitArrayToArray(rt.getVertSelection(obj)) #mesh

		return vertices


	@staticmethod
	def getSelectedVertices(obj):
		'''Get a list of the selected vertices of a given object whether it is an editable mesh or polygon.

		:Parameters:
			obj (obj) = polygon or mesh object.

		:Return:
			(list) vertex list.		
		'''
		try:
			vertices = list(range(1, rt.polyop.getNumVerts(obj)))
		except:
			vertices = list(range(1, rt.getNumVerts(obj)))

		return vertices


	@staticmethod
	def getEdges(obj):
		'''Get a list of faces of a given object whether it is an editable mesh or polygon.

		:Parameters:
			obj (obj) = polygon or mesh object.

		:Return:
			(list) edge list.		
		'''
		try:
			edges = list(range(1, rt.polyop.getNumEdges(obj)))
		except:
			edges = list(range(1, obj.edges.count))

		return edges


	@staticmethod
	def getSelectedEdges(obj):
		'''Get a list of the selected edges of a given object whether it is an editable mesh or polygon.

		:Parameters:
			obj (obj) = polygon or mesh object.

		:Return:
			(list) edge list.		
		'''
		try:
			edges = Init.bitArrayToArray(rt.polyop.getEdgeSelection(obj)) #polygon
		except:
			edges = Init.bitArrayToArray(rt.getEdgeSelection(obj)) #mesh

		return edges


	@staticmethod
	def getFaces(obj):
		'''Get a list of faces of a given object whether it is an editable mesh or polygon.

		:Parameters:
			obj (obj) = polygon or mesh object.

		:Return:
			(list) facet list.		
		'''
		try:
			faces = list(range(1, rt.polyop.getNumFaces(obj)))
		except:
			faces = list(range(1, obj.faces.count))

		return faces


	@staticmethod
	def getSelectedFaces(obj):
		'''Get a list of the selected faces of a given object whether it is an editable mesh or polygon.

		:Parameters:
			obj (obj) = polygon or mesh object.

		:Return:
			(list) facet list.		
		'''
		try:
			faces = Init.bitArrayToArray(rt.polyop.getFaceSelection(obj)) #polygon
		except:
			faces = Init.bitArrayToArray(rt.getFaceSelection(obj)) #mesh

		return faces


	@Slots.message
	def alignVertices(self, selection, mode):
		'''Align Vertices

		Align all vertices at once by putting each vert index and coordinates in a dict (or two arrays) then if when iterating through a vert falls within the tolerance specified in a textfield align that vert in coordinate. then repeat the process for the other coordinates x,y,z specified by checkboxes. using edges may be a better approach. or both with a subObjectLevel check
		create edge alignment tool and then use subObjectLevel check to call either that function or this one from the same buttons.
		to save ui space; have a single align button, x, y, z, and align 'all' checkboxes and a tolerance textfield.

		:Parameters:
			selection (list) = vertex selection
			mode (int) = valid values are: 0 (YZ), 1 (XZ), 2 (XY), 3 (X), 4 (Y), 5 (Z)

		notes:
		'vertex.pos.x = vertPosX' ect doesnt work. had to use maxscript
		'''
		# maxEval('undo "alignVertices" on')
		componentArray = selection.selectedVerts
		
		if len(componentArray) == 0:
			return 'Error: No vertices selected.'
		
		if len(componentArray) < 2:
			return 'Error: Selection must contain at least two vertices.'

		lastSelected = componentArray[-1]#3ds max re-orders array by vert index, so this doesnt work for aligning to last selected
		#~ print(lastSelected.pos)
		aX = lastSelected.pos[0]
		aY = lastSelected.pos[1]
		aZ = lastSelected.pos[2]
		
		for vertex in componentArray:
			#~ print(vertex.pos)
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
			
			print(100*"-")
			print("vertex.index:", vertex.index)
			print("position:", vX, vY, vZ)
			print("align:   ", aX, aY, aZ)
			
			rt.alignXYZ(mode, vertex, vX, vY, vZ, aX, aY, aZ)

			return '{0}{1}{2}{3}'.format("result: ", vertex.pos[0], vertex.pos[1], vertex.pos[2])


	@staticmethod
	def scaleObject (size, x, y ,z):
		'''
		:Parameters:
			size (float) = Scale amount
			x (bool) = Scale in the x direction.
			y (bool) = Scale in the y direction.
			z (bool) = Scale in the z direction.

		Basically working except for final 'obj.scale([s, s, s])' command in python. variable definitions included for debugging.
		to get working an option is to use the maxEval method in the alignVertices function.
		'''
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
		selection = rt.selection

		for obj in selection:
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
	#	[0] --object
	#	[1] --baseObject
	#	[4] --baseObject class
	#	[6] --baseObject class type string. eg. Editable,Shape,Geometry
	#notes: in another function; if selection (subobjectlevel) is == face or edge, store that face if necessary in an array and then extrude by a certain amount (if needed surface normal direction). then switch to move tool (calling a center pivot on component if needed) so that the extrude can be manipulated with widget instead of spinner.
	# @staticmethod
	# def extrudeObject (objects):
	# 	if (objects == rt.undefined or objects == "noSelection"):
	# 		print "# Error: Nothing selected. Returned string: noSelection #"
	# 		return "noSelection"

	# 	for obj in objects:
			
	# 		classString = classInfo(obj)
			
	# 		if (classString[6] == "Editable_Poly" or classString[4] == rt.Editable_mesh): #had to add Editable_mesh explicitly, here and in the error catch, because the keyword was unknown to pymxs.runtime. added it to the called function anyhow in case they fix it at some point
	# 			maxEval('macros.run "Modifiers" "Face_Extrude")
	# 			print classString[4]
				
	# 		if (classString[6] == "Shape"):
	# 			#if 'convert to mesh object' checkbox true convert currently selected:
	# 			if (tk_isChecked_000 == True):
	# 				maxEval('''
	# 				convertTo $ PolyMeshObject; --convert to poly
	# 				macros.run "Modifiers" "Face_Extrude"; --extrude modifier
	# 				''')
	# 			else:
	# 				maxEval('macros.run "Modifiers" "Extrude")
	# 			print classString[4]

	# 		if (classString[6] == "Geometry"):
	# 			#if 'convert to mesh object' checkbox true convert currently selected:
	# 			if (tk_isChecked_000 == True):
	# 				maxEval('''
	# 				convertTo $ TriMeshGeometry; --convert to mesh object
	# 				maxEval('macros.run "Modifiers" "Face_Extrude"; --extrude
	# 				''')

	# 		#else, if undefined..
	# 		else:
	# 			print "::unknown object type::"
	# 			print classString[4]

	# 		if (objects.count > 1):
	# 			rt.deselect(classString[0])
			
	# 	if (objects.count > 1): #reselect all initially selected nodes
	# 		rt.clearSelection()
	# 		for obj in objects:
	# 			rt.selectMore(obj)



	#--centerPivotOnSelection----------------------------------------------------------------

	# @staticmethod
	# def centerPivotOnSelection ():

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


	@Slots.message
	def deleteAlongAxis(self, obj, axis):
		'''Delete components of the given mesh object along the specified axis.

		:Parameters:
			obj (obj) = Mesh object.
			axis (str) = Axis to delete on. ie. '-x' Components belonging to the mesh object given in the 'obj' arg, that fall on this axis, will be deleted. 
		'''
		# for node in [n for n in pm.listRelatives(obj, allDescendents=1) if pm.objectType(n, isType='mesh')]: #get any mesh type child nodes of obj.
		# 	faces = self.getAllFacesOnAxis(node, axis)
		# 	if len(faces)==pm.polyEvaluate(node, face=1): #if all faces fall on the specified axis.
		# 		pm.delete(node) #delete entire node
		# 	else:
		# 		pm.delete(faces) #else, delete any individual faces.

		# return 'Delete faces on <hl>'+axis.upper()+'</hl>.'


	@staticmethod
	def bitArrayToArray(bitArray):
		'''
		:Parameters:
			bitArray=bit array
				*or list of bit arrays

		:Return:
			(list) containing values of the indices of the on (True) bits.
		'''
		if len(bitArray):
			if type(bitArray[0])!=bool: #if list of bitArrays: flatten
				list_=[]
				for array in bitArray:
					list_.append([i+1 for i, bit in enumerate(array) if bit==1])
				return [bit for array in list_ for bit in array]

			return [i+1 for i, bit in enumerate(bitArray) if bit==1]


	try:
		'''
		Alternate bitArray to array function.

		:Parameters:
			bitArray=bit array
		
		ie. rt.bitArrayToArray(bitArray)
		'''
		MaxPlus.Core.EvalMAXScript('''
			fn bitArrayToArray bitArray = 
				(return bitArray as Array)
			''')
	except Exception as error:
		print(error)


	@staticmethod
	def convertToEditPoly(prompt=False):
		'''
		:Parameters:
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
		''''''
		toggle = Slots.cycle([0,1], 'toggleXraySelected') #toggle 0/1

		for obj in rt.selection:
			obj.xray = toggle


	@staticmethod
	def toggleBackfaceCull():
		''''''
		toggle = Slots.cycle([0,1], 'toggleBackfaceCull') #toggle 0/1

		for obj in rt.Geometry:
			obj.backfacecull = toggle


	@staticmethod
	def toggleMaterialOverride(checker=False):
		'''Toggle override all materials in the scene.

		:Parameters:
			checker (bool) = Override with UV checkered material.
		'''
		state = Slots.cycle([0,1], 'OverrideMateridal') #toggle 0/1
		if state:
			rt.actionMan.executeAction(0, "63574") #Views: Override Off	
		else:
			if checker:
				rt.actionMan.executeAction(0, "63573") #Views: Override with UV Checker
			else:	
				rt.actionMan.executeAction(0, "63572") #Views: Override with Fast Shader
		rt.redrawViews


	@staticmethod
	def displayWireframeOnMesh(state=None, query=False):
		'''
		:Parameters:
			state=bool - display wireframe on mesh in viewport True/False
			query=bool - return current state
		:Return:
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
		''''''
		global previousSmoothPreviewLevel
		toggle = Slots.cycle([0,1], 'toggleSmoothPreview') #toggle 0/1

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
					obj.showcage = True #Show cage on
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
					obj.showcage = False #Show cage off
				except: pass

		rt.redrawViews() #refresh viewport. only those parts of the view that have changed are redrawn.


	@staticmethod
	def setSubObjectLevel(level):
		'''
		:Parameters:
			level (int) = set component mode. 0(object), 1(vertex), 2(edge), 3(border), 4(face), 5(element)
		'''
		maxEval ('max modify mode') #set focus: modifier panel.

		selection = rt.selection

		for obj in selection:
			rt.modPanel.setCurrentObject(obj.baseObject)
			rt.subObjectLevel = level

			if level==0: #reset the modifier selection to the top of the stack.
				toggle = Slots.cycle([0,1], 'toggle_baseObjectLevel')
				if toggle:
					rt.modPanel.setCurrentObject(obj.baseObject)
				else:
					try: rt.modPanel.setCurrentObject(obj.modifiers[0])
					except: rt.modPanel.setCurrentObject(obj.baseObject) #if index error


	@staticmethod
	def getModifier(obj, modifier, index=0):
		'''Gets (and sets (if needed)) the given modifer for the given object at the given index.
		
		:Parameters:
			obj = <object> - the object to add or retrieve the modifier from.
			modifier (str) = modifier name.
			index (int) = place modifier before given index. default is at the top of the stack.
						Negative indices place the modifier from the bottom of the stack.
		:Return:
			modifier
		'''
		m = obj.modifiers[modifier] #check the stack for the given modifier.
		
		if not m:
			m = getattr(rt, modifier)()
			if index<0:
				index = index+len(obj.modifiers)+1 #place from the bottom index.
			rt.addModifier(obj, m, before=index)
		
		if not rt.modPanel.getCurrentObject()==m:
			rt.modPanel.setCurrentObject(m) #set modifier in stack (if it is not currently active).

		return m


	@staticmethod
	def undo(state=True):
		import pymxs
		pymxs.undo(state)
		return state



	# ------------------------------------------------
	' Ui'
	# ------------------------------------------------


	@classmethod
	def attr(cls, fn):
		'''Decorator for objAttrWindow.
		'''
		def wrapper(self, *args, **kwargs):
			self.setAttributeWindow(fn(self, *args, **kwargs))
		return wrapper

	def setAttributeWindow(self, obj, include=[], exclude=[]):
		'''Launch a popup window containing the given objects attributes.

		:Parameters:
			obj (obj) = The object to get the attributes of.
			include (list) = Attributes to include. All other will be omitted. Exclude takes dominance over include. Meaning, if the same attribute is in both lists, it will be excluded.
			exclude (list) = Attributes to exclude from the returned dictionay. ie. [u'Position',u'Rotation',u'Scale',u'renderable',u'isHidden',u'isFrozen',u'selected']
		'''
		if obj is None:
			return

		if isinstance(obj, (list, set, tuple)):
			obj = obj[0]

		if not all((include, exclude)):
			exclude = []

		attributes = self.getAttributesMax(obj, include=include, exclude=exclude)
		self.objAttrWindow(obj, attributes, self.setAttributesMax)


	@Slots.message
	def maxUiSetChecked(self, id, table, item, state=True, query=False):
		'''
		:Parameters:
			id (str) = actionMan ID
			table (int) = actionMan table
			item (int) = actionMan item number
		'''
		atbl = rt.actionMan.getActionTable(table)
		if atbl:
			aitm = atbl.getActionItem(item)
			if query:
				return aitm.isChecked
			else:
				if state: #check
					if not aitm.isChecked:
						rt.actionMan.executeAction(0, id)
						return aitm.isChecked
				else: #uncheck
					if aitm.isChecked:
						rt.actionMan.executeAction(0, id)
						return aitm.isChecked









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

#deprecated:

	# @staticmethod
	# def splitNonManifoldVertex(obj, vertex):
	# 	'''
	# 	Separate a connected vertex of non-manifold geometry where the faces share a single vertex.

	# 	:Parameters:
	# 		obj (obj) = A polygon object.
	# 		vertex (int) = A single vertex number of the given polygon object.
	# 	'''
	# 	connected_faces = rt.polyop.getFacesUsingVert(obj, vertex)

	# 	rt.polyop.breakVerts(obj, vertex)

	# 	#get a list for the vertices of each face that is connected to the original vertex.
	# 	verts_sorted_by_face=[]
	# 	for face in Init.bitArrayToArray(connected_faces):
	# 		connected_verts = rt.polyop.getVertsUsingFace(obj, face)
	# 		verts_sorted_by_face.append(Init.bitArrayToArray(connected_verts))


	# 	out=[] #1) take first set A from list. 2) for each other set B in the list do if B has common element(s) with A join B into A; remove B from list. 3) repeat 2. until no more overlap with A. 4) put A into outpup. 5) repeat 1. with rest of list.
	# 	while len(verts_sorted_by_face)>0:
	# 		first, rest = verts_sorted_by_face[0], verts_sorted_by_face[1:] #first, *rest = edges
	# 		first = set(first)

	# 		lf = -1
	# 		while len(first)>lf:
	# 			lf = len(first)

	# 			rest2=[]
	# 			for r in rest:
	# 				if len(first.intersection(set(r)))>0:
	# 					first |= set(r)
	# 				else:
	# 					rest2.append(r)     
	# 			rest = rest2

	# 		out.append(first)
	# 		verts_sorted_by_face = rest


	# 	for vertex_set in out:
	# 		obj.weldThreshold = 0.001
	# 		rt.polyop.weldVertsByThreshold(obj, list(vertex_set))


	# 	rt.polyop.setVertSelection(obj, vertex)



	# def setComboBox(self, comboBox, index):
	# 	'''
	# 	Set the given comboBox's index using a text string.
	# 	:Parameters:
	# 		comboBox (str) = comboBox name (will also be used as the methods name).
	# 		index = int or 'string' - text of the index to switch to.
	# 	'''
	# 	cmb = getattr(self.init_ui, comboBox)
	# 	method = getattr(self, comboBox)
	# 	cmb.currentIndexChanged.connect(method)
	# 	if not type(index)==int:
	# 		index = cmb.findText(index)
	# 	cmb.setCurrentIndex(index)