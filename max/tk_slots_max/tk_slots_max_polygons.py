import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Polygons(Init):
	def __init__(self, *args, **kwargs):
		super(Polygons, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('polygons')




	def chk002(self):
		'''
		Un-Crease

		'''
		if self.ui.chk002.isChecked():
			self.ui.s003.setValue(0) #crease value
			self.ui.s004.setValue(180) #normal angle
			self.setButtons(self.ui, unchecked='chk003')
		else:
			self.ui.s003.setValue(5) #crease value
			self.ui.s004.setValue(60) #normal angle


	def chk008(self):
		'''
		Split U

		'''
		self.setButtons(self.ui, unchecked='chk010')


	def chk009(self):
		'''
		Split V

		'''
		self.setButtons(self.ui, unchecked='chk010')


	def chk010(self):
		'''
		Tris

		'''
		self.setButtons(self.ui, unchecked='chk008,chk009')


	def chk003(self):
		'''
		Crease: Max

		'''
		if self.ui.chk003.isChecked():
			self.ui.s003.setValue(10) #crease value
			self.ui.s004.setValue(30) #normal angle
			self.setButtons(self.ui, unchecked='chk002')
		else:
			self.ui.s003.setValue(5) #crease value
			self.ui.s004.setValue(60) #normal angle


	def chk006(self):
		'''
		

		'''
		if self.ui.chk006.isChecked():
			self.ui.s001.setSingleStep(.01)
		else:
			self.ui.s001.setSingleStep(.5)


	def b000(self):
		'''
		Merge Vertex Options

		'''
		rt.macros.run('Modifiers', 'VertexWeld')


	def b001(self):
		'''
		Fill Holes

		'''
		rt.macros.run('Modifiers', 'Cap_Holes')


	def b002(self):
		'''
		Separate

		'''
		pass
		# rt.detachElement(obj)


	def b003(self):
		'''
		Combine

		'''
		if self.ui.chk000.isChecked():
			pass

		sel = rt.selection
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
		Slice

		'''
		rt.macros.run('Ribbon - Modeling', 'CutsQuickSlice')
		

	def b005(self):
		'''
		Bridge

		'''
		for obj in rt.selection:
			obj.EditablePoly.Bridge() #perform bridge
		rt.redrawViews() #redraw changes in viewport


	def b006(self):
		'''
		Extrude

		'''
		rt.macros.run('Ribbon - Modeling', 'EPoly_Extrude')
		# for obj in rt.selection:
		# 	self.extrudeObject(obj)


	def b007(self):
		'''
		Bevel (Chamfer)

		'''
		rt.macros.run('Ribbon - Modeling', 'EPoly_Chamfer')
		# width = float(self.ui.s000.value())
		# chamfer = True

		# if chamfer:
		# rt.macros.run('Modifiers', 'ChamferMod')
		# else: #bevel
		# 	maxEval('modPanel.addModToSelection (Bevel ()) ui:on')


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
		
		level = rt.subObjectLevel

		for obj in rt.selection:
			if level == 1: #--vertex level
				obj.EditablePoly.collapse('Vertex')

			if level == 2: #--edge level
				obj.EditablePoly.collapse('Edge')

			if level == 4: #--face level
				obj.EditablePoly.collapse('Face')

		# rt.macros.run('Ribbon - Modeling', 'GeometryCollapse')


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
		self.setSubObjectLevel(4)
		rt.macros.run('Ribbon - Modeling', 'CutsCut')
		# obj = rt.Filters.GetModOrObj()
		# if obj:
		# 	obj.ToggleCommandMode('CutVertex') #cut vertex tool
		

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
		offset = float(self.ui.s001.value())
		maxEval('''
		Try 
		(
			If subObjectLevel == undefined then Max Modify Mode
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
		if Ribbon - Modeling.ValidSOMode() and (subObjectLevel == 2 or subObjectLevel == 3) then
		(
			curmod = Modpanel.getcurrentObject()
			if subObjectLevel == 2 then
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
		If subObjectLevel == undefined then Max Modify Mode
		-- default to Face level:
		if subObjectLevel == 0 then subObjectLevel = 4
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
		Attach

		'''
		rt.macros.run('Ribbon - Modeling', 'AttachMode')


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
		if self.ui.chk008.isChecked(): #Split U
			u=2
		if self.ui.chk009.isChecked(): #Split V
			v=2

		mode = 0 #The subdivision mode. 0=quads, 1=triangles
		subdMethod = 1 #subdivision type: 0=exponential(traditional subdivision) 1=linear(number of faces per edge grows linearly)
		if self.ui.chk010.isChecked(): #tris
			mode=dv=1
			subdMethod=0
		if all([self.ui.chk008.isChecked(), self.ui.chk009.isChecked()]): #subdivide once into quads
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
		tolerance = float(self.ui.s002.value())
		mergeAll = self.ui.chk006.isChecked()

		sel = rt.selection

		if not sel:
			print "// Warning: No object selected. Must select an object or component"
			return

		for obj in sel:
			if mergeAll:
				rt.polyop.weldVertsByThreshold(obj, obj.verts)
				
			else:
				vertices = rt.getVertSelection(obj)
				obj.weldThreshold = tolerance
				rt.polyop.weldVertsByThreshold(obj, vertices)


	def b041(self):
		'''
		

		'''
		pass


	def b042(self):
		'''
		

		'''
		pass


	def b043(self):
		'''
		Target Weld

		'''
		self.setSubObjectLevel(1) #set component mode to vertex
		rt.macros.run('Editable Polygon Object', 'EPoly_TargetWeld')
		

	def b044(self):
		'''
		Detach

		'''
		#rt.macros.run('Ribbon - Modeling', 'GeometryDetach')
		level = rt.subObjectLevel

		
		for obj in rt.selection:
			if level==1: #vertices
				vertices = rt.getVertSelection(obj)
				for v in vertices:
					obj.EditablePoly.breakVerts(v)

			if level==2: #edges
				pass #add function to detach edge. likely as spline.

			if level==4: #faces
				element=rt.polyop.getElementsUsingFace(obj, 1)
				if rt.queryBox('Detach as Element?', title='Detach'): #detach as element
					rt.polyop.detachFaces(obj, element, delete=False, asNode=False)
				else: #detach as separate object
					rt.polyop.detachFaces(obj, element, delete=True, asNode=True)
				

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
		level = rt.subObjectLevel

		for obj in rt.selection:
			if level==1:
				mel.eval("performPolyPoke 1;")

			if level==2:
				position = 0.5

				edges = rt.getEdgeSelection(obj)
				for edge in self.bitArrayToArray(edges):
					rt.polyop.divideEdge(obj, edge, position)

			if level==4:
				mel.eval("polyChamferVtx 0 0.25 0;")

		rt.redrawViews


	def b047(self):
		'''
		Insert Edgeloop

		'''
		self.setSubObjectLevel(0)
		rt.macros.run('PolyTools', 'SwiftLoop')


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
		creaseAmount = int(self.ui.s003.value())
		normalAngle = int(self.ui.s004.value())

		creaseAmount = creaseAmount*0.1 #convert to max 0-1 range

		for obj in rt.selection:
			if rt.classOf(obj)=='Editable_Poly':

				if self.ui.chk011.isChecked(): #crease: Auto
					minAngle = int(self.ui.s005.value()) 
					maxAngle = int(self.ui.s006.value()) 

					edgelist = self.getEdgesByAngle(minAngle, maxAngle)
					rt.polyOp.setEdgeSelection(obj, edgelist)

				if self.ui.chk004.isChecked(): #crease vertex point
					pass
				else: #crease edge
					obj.EditablePoly.setEdgeData(1, creaseAmount)

				if self.ui.chk005.isChecked(): #adjust normal angle
					edges = rt.polyop.getEdgeSelection(obj)
					for edge in edges:
						edgeVerts = rt.polyop.getEdgeVerts(obj, edge)
						normal = rt.averageSelVertNormal(obj)
						for vertex in edgeVerts:
							rt.setNormal(obj, vertex, normal)
		else:
			print '# Warning: object type '+rt.classOf(obj)+' is not supported. #'


	def b056(self):
		'''
		

		'''
		pass


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

			if (self.ui.chk001.isChecked()):
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

