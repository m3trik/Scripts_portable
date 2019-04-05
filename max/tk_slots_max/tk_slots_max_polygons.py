import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Polygons(Init):
	def __init__(self, *args, **kwargs):
		super(Polygons, self).__init__(*args, **kwargs)




	def chk002(self):
		'''
		Un-Crease

		'''
		if self.hotBox.ui.chk002.isChecked():
			self.hotBox.ui.s003.setValue(0) #crease value
			self.hotBox.ui.s004.setValue(180) #normal angle
			self.setButtons(self.hotBox.ui, unchecked='chk003')
		else:
			self.hotBox.ui.s003.setValue(7.5) #crease value
			self.hotBox.ui.s004.setValue(30) #normal angle

	def chk008(self):
		'''
		Split U

		'''
		self.setButtons(self.hotBox.ui, unchecked='chk010')

	def chk009(self):
		'''
		Split V

		'''
		self.setButtons(self.hotBox.ui, unchecked='chk010')

	def chk010(self):
		'''
		Tris

		'''
		self.setButtons(self.hotBox.ui, unchecked='chk008,chk009')

	def chk003(self):
		'''
		Crease: Max

		'''
		if self.hotBox.ui.chk003.isChecked():
			self.hotBox.ui.s003.setValue(10) #crease value
			self.hotBox.ui.s004.setValue(30) #normal angle
			self.setButtons(self.hotBox.ui, unchecked='chk002')
		else:
			self.hotBox.ui.s003.setValue(7.5) #crease value
			self.hotBox.ui.s004.setValue(60) #normal angle

	def chk006(self):
		'''
		

		'''
		if self.hotBox.ui.chk006.isChecked():
			self.hotBox.ui.s001.setSingleStep(.01)
		else:
			self.hotBox.ui.s001.setSingleStep(.5)

	def b000(self):
		'''
		Merge Vertex Options

		'''
		maxEval('macros.run \"Modifiers\" \"VertexWeld\"')

	def b001(self):
		'''
		Fill Holes

		'''
		maxEval('macros.run \"Modifiers\" \"Cap_Holes\"')

	def b002(self):
		'''
		Separate

		'''
		sel = makeSelection ("Current", 1, classInfo)
		detachElement(sel)

	def b003(self):
		'''
		Combine

		'''
		if self.hotBox.ui.chk000.isChecked():
			pass
			#from maya:
		# 	maxEval('bt_mergeCombineMeshes;')
		# else:
		# 	maxEval('CombinePolygons;')
		sel = makeSelection ("Current", 0)
		maxEval('''
		j = 1;
		count = sel.count;

		undo off;

		while sel.count > 1 do
		(
			if classof sel != Editable_Poly then converttopoly sel
			(
				polyop.attach sel sel;
			  deleteItem sel (j+1);

			  j += 1;

			  if (j + 1) > sel.count then 
			  (
			      j = 1
			  )
			)
		)
		''')

	def b004(self):
		'''
		

		'''
		pass
		
	def b005(self):
		'''
		Bridge

		'''
		rt.selection.EditablePoly.Bridge() #perform bridge
		rt.redrawViews() #redraw changes in viewport


	def b006(self):
		'''
		Extrude

		'''
		sel = makeSelection("Current", 0)
    	
		if (sel != "noSelection"):
			for obj in sel:
				extrudeObject(obj)
				# classInfo = classInfo(obj)
				# componentArray = []

				# if classInfo[9] == 4
				#		subObject = ""
				#		componentArray.append(subObject)
				#		extrudeObject(obj)
				#	option #maxEval('maxOps.CollapseNode $ off; --collapse modifier stack')

	def b007(self):
		'''
		Bevel \Chamfer

		'''
		width = float(self.hotBox.ui.s000.value())
		chamfer = True
		if chamfer:
			maxEval('macros.run \"Modifiers\" \"ChamferMod\"')
		else: #bevel
			maxEval('modPanel.addModToSelection (Bevel ()) ui:on')

	def b008(self):
		'''
		

		'''
		pass

	def b009(self):
		'''
		Collapse Component

		'''
		#--[mesh] 0=object level,1=vertex level,2=edge level,3=face,4=polygon,5=element,
		#--[poly] 0=object level,1=vertex level,2=edge level,3=border,4=polygon,5=element
		
		if (rt.subObjectLevel == 1): #--vertex level
			maxEval('''
			$.EditablePoly.collapse #Vertex
			''')
		if (rt.subObjectLevel == 2): #--edge level
			maxEval('''
			$.EditablePoly.collapse #Edge
			''')
		if (rt.subObjectLevel == 3): #--face level
			maxEval('''
			$.EditablePoly.collapse #Face
			''')

	def b010(self):
		'''
		Extract Curve

		'''
		maxEval('')

	def b011(self):
		'''
		Extract Curve Options

		'''
		maxEval('')

	def b012(self):
		'''
		Multi-Cut Tool

		'''
		maxEval('''
		Try
		(
			If SubObjectLevel == undefined then Max Modify Mode
			local A = Filters.GetModOrObj()
			if (Filters.Is_This_EditPolyMod A) then (A.ToggleCommandMode #Cut)
			else (A.toggleCommandMode #CutVertex)   -- (Really a general Cut mode.)
		)
		Catch (print "# Error: invalid multi-cut Selection Type. #")
		''')

	def b013(self):
		'''
		Combine Polygon Options

		'''
		maxEval('CombinePolygonsOptions;')

	def b014(self):
		'''
		 Bevel Options

		'''
		maxEval('')

	def b015(self):
		'''
		Delete Edgeloop

		'''
		maxEval('$.EditablePoly.Remove ()')

	def b016(self):
		'''
		Inset Face Region

		'''
		offset = float(self.hotBox.ui.s001.value())
		maxEval('''
		Try 
		(
			If SubObjectLevel == undefined then Max Modify Mode
			local A = modPanel.getCurrentObject()
			if keyboard.shiftpressed then A.popupDialog #Inset
			else A.toggleCommandMode #InsetFace
		)
		Catch()
		''')

	def b017(self):
		'''
		Bridge Options

		'''
		maxEval('''
		if Ribbon_Modeling.ValidSOMode() and (subobjectlevel == 2 or subobjectlevel == 3) then
		(
			curmod = Modpanel.getcurrentObject()
			if subobjectlevel == 2 then
			(   
			    curmod.popupDialog #BridgeEdge
			)
			else 
			(
			    curmod.popupDialog #BridgeBorder
			)
		)
		''')

	def b018(self):
		'''
		Extrude Options

		'''
		maxEval('''
		If SubObjectLevel == undefined then Max Modify Mode
		-- default to Face level:
		if subobjectLevel == 0 then subobjectLevel = 4
		local A = modPanel.getCurrentObject()
		if (Filters.Is_This_EditPolyMod A) then
		(
			local level = A.GetMeshSelLevel()
			if (level == #Vertex) then (A.PopupDialog #ExtrudeVertex)
			else if (level == #Edge) then (A.PopupDialog #ExtrudeEdge)
			else if (level == #Face) then (A.PopupDialog #ExtrudeFace)
		)
		else (A.popupDialog #Extrude)
		''')

	def b019(self):
		'''
		

		'''
		pass

	def b020(self):
		'''
		

		'''
		pass

	def b021(self):
		'''
		Connect Border Edges

		'''
		mel.eval("performPolyConnectBorders 0;")

	def b022(self):
		'''
		Connect

		'''
		mel.eval("dR_connectTool;")

	def b023(self):
		'''
		Boolean

		'''
		mel.eval("PolygonBooleanUnion;")

	def b024(self):
		'''
		

		'''
		pass

	def b025(self):
		'''
		

		'''
		pass

	def b026(self):
		'''
		

		'''
		pass

	def b027(self):
		'''
		

		'''
		pass

	def b028(self):
		'''
		Quad Draw

		'''
		mel.eval("dR_quadDrawTool;")

	def b029(self):
		'''
		Divide Facet

		'''
		dv=u=v=0
		if self.hotBox.ui.chk008.isChecked(): #Split U
			u=2
		if self.hotBox.ui.chk009.isChecked(): #Split V
			v=2

		mode = 0 #The subdivision mode. 0=quads, 1=triangles
		subdMethod = 1 #subdivision type: 0=exponential(traditional subdivision) 1=linear(number of faces per edge grows linearly)
		if self.hotBox.ui.chk010.isChecked(): #tris
			mode=dv=1
			subdMethod=0
		if all([self.hotBox.ui.chk008.isChecked(), self.hotBox.ui.chk009.isChecked()]): #subdivide once into quads
			dv=1
			subdMethod=0
			u=v=0
		#perform operation
		for face in selectedFaces: #when performing polySubdivideFacet on multiple faces, adjacent subdivided faces will make the next face an n-gon and therefore not able to be subdivided. 
			pm.polySubdivideFacet (face, divisions=0, divisionsU=2, divisionsV=2, mode=0, subdMethod=1)

	def b030(self):
		'''
		

		'''
		pass

	def b031(self):
		'''
		

		'''
		pass

	def b032(self):
		'''
		Poke

		'''
		mel.eval("PokePolygon;")

	def b033(self):
		'''
		Poke Options

		'''
		mel.eval("PokePolygonOptions;")

	def b034(self):
		'''
		Wedge

		'''
		mel.eval("WedgePolygon;")

	def b035(self):
		'''
		Wedge Options

		'''
		mel.eval("WedgePolygonOptions;")

	def b036(self):
		'''
		

		'''
		pass

	def b037(self):
		'''
		

		'''
		pass

	def b038(self):
		'''
		Assign Invisible

		'''
		mel.eval("polyHole -assignHole 1;")

	def b039(self):
		'''
		Assign Invisible Options

		'''
		mel.eval("PolyAssignSubdivHoleOptions;")

	def b040(self):
		'''
		Merge All Vertices

		'''
		floatXYZ = float(self.hotBox.ui.s002.value())
		mergeAll = self.hotBox.ui.chk006.isChecked()

		selection = pm.ls(selection=1, objectsOnly=1)

		if len(selection)<1:
			print "// Warning: No object selected. Must select an object or component"
			return

		if mergeAll:
			for obj in selection:
				# get number of vertices
				count = pm.polyEvaluate(obj, vertex=1)
				vertices = str(obj) + ".vtx [0:" + str(count) + "]" # mel expression: select -r geometry.vtx[0:1135];
				pm.polyMergeVertex(vertices, distance=floatXYZ, alwaysMergeTwoVertices=False, constructionHistory=False)

			#return to original state
			pm.select(clear=1)
			for obj in selection:
				pm.select(obj, add=1)
		else:
			pm.polyMergeVertex(distance=floatXYZ, alwaysMergeTwoVertices=True, constructionHistory=True)

	def b041(self):
		'''
		

		'''
		pass

	def b042(self):
		'''
		Merge Vertices Center

		'''
		mel.eval("MergeToCenter;")

	def b043(self):
		'''
		Target Weld

		'''
		mel.eval("dR_targetWeldTool;")

	def b044(self):
		'''
		Detach

		'''
		maxEval('''
		if subObjectLevel == 4 then
			$.EditablePoly.detachToElement #Face keepOriginal:off --element
			--$.EditablePoly.detachToElement #Face keepOriginal:on --clone
		if subObjectLevel == 2 then
			$.EditablePoly.detachToElement #Edge keepOriginal:off --element
			--$.EditablePoly.detachToElement #Face keepOriginal:on --clone
		''')

	def b045(self):
		'''
		Re-Order Vertices

		'''
		symmetryOn = pm.symmetricModelling(query=True, symmetry=True) #query symmetry state
		if symmetryOn:
			pm.symmetricModelling(symmetry=False)
		mel.eval("setPolygonDisplaySettings(\"vertIDs\");") #set vertex id on
		mel.eval("doBakeNonDefHistory( 1, {\"pre\"});") #history must be deleted
		mel.eval("performPolyReorderVertex;") #start vertex reorder ctx

	def b046(self):
		'''
		Split

		'''
		vertexMask = pm.selectType (query=True, vertex=True)
		edgeMask = pm.selectType (query=True, edge=True)
		facetMask = pm.selectType (query=True, facet=True)

		if facetMask:
			mel.eval("performPolyPoke 1;")

		if edgeMask:
			mel.eval("polySubdivideEdge -ws 0 -s 0 -dv 1 -ch 0;")

		if vertexMask:
			mel.eval("polyChamferVtx 0 0.25 0;")

	def b047(self):
		'''
		Insert Edgeloop

		'''
		mel.eval("SplitEdgeRingTool;")

	def b048(self):
		'''
		Collapse Edgering

		'''
		mel.eval("bt_polyCollapseEdgeRingTool;")

	def b049(self):
		'''
		Slide Edge Tool

		'''
		mel.eval("SlideEdgeTool;")

	def b050(self):
		'''
		Spin Edge

		'''
		mel.eval("bt_polySpinEdgeTool;")

	def b051(self):
		'''
		Offset Edgeloop

		'''
		mel.eval("performPolyDuplicateEdge 0;")

	def b052(self):
		'''
		Offset Edgeloop Options

		'''
		mel.eval("DuplicateEdgesOptions;")

	def b053(self):
		'''
		Edit Edge Flow

		'''
		mel.eval("PolyEditEdgeFlow;")

	def b054(self):
		'''
		Edit Edge Flow Options

		'''
		mel.eval("PolyEditEdgeFlowOptions;")

	def b055(self):
		'''
		Crease

		'''
		creaseAmount = float(self.hotBox.ui.s003.value())
		normalAngle = int(self.hotBox.ui.s004.value()) 

		operation = 0 #Crease selected components
		pm.polySoftEdge (angle=0, constructionHistory=0) #Harden edge normal
		if self.hotBox.ui.chk002.isChecked():
			objectMode = pm.selectMode (query=True, object=True)
			if objectMode: #if in object mode,
				operation = 2 #2-Remove all crease values from mesh
			else:
				operation = 1 #1-Remove crease from sel components
				pm.polySoftEdge (angle=180, constructionHistory=0) #soften edge normal

		if self.hotBox.ui.chk004.isChecked(): #crease vertex point
			pm.polyCrease (value=creaseAmount, vertexValue=creaseAmount, createHistory=True, operation=operation)
		else:
			pm.polyCrease (value=creaseAmount, createHistory=True, operation=operation) #PolyCreaseTool;

		if self.hotBox.ui.chk005.isChecked(): #adjust normal angle
			pm.polySoftEdge (angle=normalAngle)

	def b056(self):
		'''
		Split Vertices

		'''
		obj = rt.selection[0]
		verts = rt.polyop.getVertSelection(obj)

		rt.polyop.breakVerts (obj, verts)
		print 'breakVerts: ', verts

	def b057(self):
		'''
		Trifill

		'''
		pm.undoInfo (openChunk=True)
		selectTypeEdge = pm.filterExpand(selectionMask=32) #returns True if selectionMask=Edges

		symmetryOn = pm.symmetricModelling(query=True, symmetry=True) #query symmetry state
		if symmetryOn:
			axis = pm.symmetricModelling(query=True, axis=True) #query the symmetry axis and assign which vertex point position in list to query later in order to filter and perform an operation on them seperately 
			if axis == "x":
				axisInt = 0
			if axis == "y":
				axisInt = 1
			if axis == "z":
				axisInt = 2

		if (selectTypeEdge): #if selection is polygon edges, convert to vertices.
			mel.eval("PolySelectConvert 3;")

		selected = pm.ls (selection=True, flatten=True) #now that the selection is converted, get selected vertices
		if (len(selected)>0): #check to see if there is anything selected
			object_ = selected[0].split('.vtx')[0] #strip .vtx from the vertex name to get the object (shape) name
		else:
			print "// Warning: Nothing Selected. You must select two edges that share a vertex or at least three vertices. //"

		shadingEngines = pm.listConnections(object_, type="shadingEngine") #get the connected "shadingEngines"
		materials = pm.ls(pm.listConnections(shadingEngines), materials=True) #list the connected materials (shaders)

		vertexList = []
		vertexListNeg = []
		for vertex in selected:
			vertexPosition =  pm.pointPosition(vertex)
			if symmetryOn:
				if vertexPosition[axisInt]<0: #if symmetry on, seperate negative vertices on which ever axis is being used
					vertexListNeg.append(vertexPosition)
				else:
					vertexList.append(vertexPosition)
			else:
				vertexList.append(vertexPosition)

		def createFacetAndUnite(vertices):
			tempTriangle = "___fillTemp___" #create a polygon face using the list of vertex points and give it a temp name
			pm.polyCreateFacet (point=vertices, texture=1, name=tempTriangle) #0-None; 1-Normalize; 2-Unitize

			if (self.hotBox.ui.chk001.isChecked()):
				pm.polyNormal(tempTriangle, normalMode=4) #3-reverse and cut, 4-reverse and propagate

			pm.select(tempTriangle, add=True) #select and assign material from main object
			pm.hyperShade(assign=materials[0])
			pm.select(tempTriangle, clear=True)

			tempObject = "___objTemp___" #combine with main mesh, assigning a temp name so that the original name can be freed up and the object can then be renamed to the original name
			pm.polyUnite (object_, tempTriangle, constructionHistory=False, name=tempObject)
			pm.rename (tempObject, object_)

		if symmetryOn:
			createFacetAndUnite(vertexList)
			createFacetAndUnite(vertexListNeg)
		else:
			createFacetAndUnite(vertexList)

		pm.hilite (object_, replace=True)

		if (selectTypeEdge): #if original selection was edges, convert back to edges.
			mel.eval("PolySelectConvert 2;")
			pm.selectType(edge=True)
		pm.undoInfo (closeChunk=True)

	def b058(self):
		'''
		

		'''
		pass

	def b059(self):
		'''
		Crease Editor

		'''
		print "crease"
		from maya.app.general import creaseSetEditor
		creaseSetEditor.showCreaseSetEditor()

	def b060(self):
		'''
		

		'''
		pass






		

		






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

# #slice plane
# maxEval('''
# 		local retValue = false
# 		if( Ribbon_Modeling.ValidSOMode() ) then
# 		(
# 			curmod = Modpanel.getcurrentObject()
# 			retValue = (curmod.getCommandMode() == #SlicePlane)
# 		)
# 		retValue
# 		''')

# #quick slice
# 		maxEval('''
# 		if( Ribbon_Modeling.ValidSelection() ) then
# 		(
# 			curmod = Modpanel.getcurrentObject()
# 			(curmod.getCommandMode() == #QuickSlice)
# 		)
# 		else
# 		(
# 			false
# 		)
# 		''')

# #inset options
# maxEval('''
#  		local A = modPanel.getCurrentObject()
# 		A.popupDialog #Inset
# 		''')