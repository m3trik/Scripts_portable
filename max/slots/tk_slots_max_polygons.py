import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init






class Polygons(Init):
	def __init__(self, *args, **kwargs):
		super(Polygons, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('polygons')






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


	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['Bridge','Extrude']
		contents = self.comboBox (cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Bridge'):
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
			if index==contents.index('Extrude'):
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
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		
		'''
		pass


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


	def b012(self):
		'''
		Multi-Cut Tool
		'''
		self.setSubObjectLevel(4)
		rt.macros.run('Ribbon - Modeling', 'CutsCut')
		# obj = rt.Filters.GetModOrObj()
		# if obj:
		# 	obj.ToggleCommandMode('CutVertex') #cut vertex tool
		

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


	def b032(self):
		'''
		Poke
		'''
		mel.eval("PokePolygon;")


	def b034(self):
		'''
		Wedge
		'''
		mel.eval("WedgePolygon;")


	def b038(self):
		'''
		Assign Invisible
		'''
		mel.eval("polyHole -assignHole 1;")


	def b040(self):
		'''
		Merge Vertices
		'''
		tolerance = float(self.ui.s002.value())
		selection = rt.selection

		self.progressBar(init=1) #initialize the progress bar
		if selection:
			for obj in selection:
				self.progressBar(len(selection)) #register progress
				vertSelection = rt.getVertSelection(obj)
				if rt.subObjectLevel==1 and vertSelection>1: #merge selected components.
					obj.weldThreshold = tolerance
					rt.polyop.weldVertsByThreshold(obj, vertSelection)

				else: #if object mode. merge all vertices on the selected object.
					rt.polyop.weldVertsByThreshold(obj, obj.verts)
		else:
			print "// Warning: No object selected. Must select an object or component"
			return


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


	def b053(self):
		'''
		Edit Edge Flow
		'''
		mel.eval("PolyEditEdgeFlow;")











#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------