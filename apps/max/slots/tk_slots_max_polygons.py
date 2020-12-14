from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Polygons(Init):
	def __init__(self, *args, **kwargs):
		super(Polygons, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('polygons')
		self.childUi = self.sb.getUi('polygons_submenu')


	def chk008(self, state=None):
		'''
		Divide Facet: Split U
		'''
		self.toggleWidgets(setUnChecked='chk010')


	def chk009(self, state=None):
		'''
		Divide Facet: Split V
		'''
		self.toggleWidgets(setUnChecked='chk010')


	def chk010(self, state=None):
		'''
		Divide Facet: Tris
		'''
		self.toggleWidgets(setUnChecked='chk008,chk009')


	def d000(self, state=None):
		'''
		Context menu
		'''
		d000 = self.parentUi.d000

		if state is 'setMenu':
			d000.contextMenu.add(widgets.TkComboBox, setObjectName='cmb000', setToolTip='')

			return


	def cmb000(self, index=None):
		'''
		3dsMax Polygon Operations
		'''
		cmb = self.polygons.d000.contextMenu.cmb000

		if index is 'setMenu':
			list_ = ['Bridge','Extrude']
			cmb.addItems_(list_, '3dsMax Polygon Operations')
			return

		if index>0:
			if index==cmb.items.index('Bridge'):
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
			if index==cmb.items.index('Extrude'):
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


	@Slots.message
	def tb000(self, state=None):
		'''
		Merge Vertices
		'''
		tb = self.currentUi.tb000
		if state is 'setMenu':
			tb.menu_.add('QDoubleSpinBox', setPrefix='Distance: ', setObjectName='s002', setMinMax_='0.0000-10 step.001', setValue=0.001, setToolTip='Merge Distance.')
			return

		tolerance = float(tb.menu_.s002.value())
		selection = rt.selection

		if selection:
			for n, obj in enumerate(selection):
				if not self.parentUi.progressBar.step(n, len(selection)): #register progress while checking for cancellation:
					break

				vertSelection = rt.getVertSelection(obj)
				if rt.subObjectLevel==1 and vertSelection>1: #merge selected components.
					obj.weldThreshold = tolerance
					rt.polyop.weldVertsByThreshold(obj, vertSelection)

				else: #if object mode. merge all vertices on the selected object.
					rt.polyop.weldVertsByThreshold(obj, obj.verts)
		else:
			return 'Error: No object selected.'


	def tb001(self, state=None):
		'''
		Bridge
		'''
		tb = self.currentUi.tb001
		if state is 'setMenu':
			tb.menu_.add('QSpinBox', setPrefix='Divisions: ', setObjectName='s003', setMinMax_='0-10000 step1', setValue=0.001, setToolTip='Divisions.')
			return

		divisions = tb.menu_.s003.value()

		for obj in rt.selection:
			obj.EditablePoly.Bridge() #perform bridge
		rt.redrawViews() #redraw changes in viewport


	def tb002(self, state=None):
		'''
		Combine
		'''
		tb = self.currentUi.tb002
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Merge', setObjectName='chk000', setChecked=True, setToolTip='Combine selected meshes and merge any coincident verts/edges.')
			return

		if tb.menu_.chk000.isChecked():
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


	def tb003(self, state=None):
		'''
		Extrude
		'''
		tb = self.currentUi.tb003
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Keep Faces Together', setObjectName='chk002', setChecked=True, setToolTip='Keep edges/faces together.')
			return

		keepFacesTogether = tb.menu_.chk002.isChecked() #keep faces/edges together.

		rt.macros.run('Ribbon - Modeling', 'EPoly_Extrude')
		# for obj in rt.selection:
		# 	self.extrudeObject(obj)


	def tb004(self, state=None):
		'''
		Bevel (Chamfer)
		'''
		tb = self.currentUi.tb004
		if state is 'setMenu':
			tb.menu_.add('QDoubleSpinBox', setPrefix='Width: ', setObjectName='s000', setMinMax_='0.00-100 step.01', setValue=0.01, setToolTip='Bevel Width.')
			return

		width = float(tb.menu_.s000.value())

		rt.macros.run('Ribbon - Modeling', 'EPoly_Chamfer')
		# width = float(self.parentUi.s000.value())
		# chamfer = True

		# if chamfer:
		# rt.macros.run('Modifiers', 'ChamferMod')
		# else: #bevel
		# 	maxEval('modPanel.addModToSelection (Bevel ()) ui:on')


	def tb005(self, state=None):
		'''
		Detach
		'''
		tb = self.currentUi.tb005
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Delete Original', setObjectName='chk007', setChecked=True, setToolTip='Delete original selected faces.')
			return

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
	

	def tb006(self, state=None):
		'''
		Inset Face Region
		'''
		tb = self.currentUi.tb006
		if state is 'setMenu':
			tb.menu_.add('QDoubleSpinBox', setPrefix='Offset: ', setObjectName='s001', setMinMax_='0.00-100 step.01', setValue=2.00, setToolTip='Offset amount.')
			return

		offset = float(tb.menu_.s001.value())
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


	def tb007(self, state=None):
		'''
		Divide Facet
		'''
		tb = self.currentUi.tb007
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='U', setObjectName='chk008', setChecked=True, setToolTip='Divide facet: U coordinate.')
			tb.menu_.add('QCheckBox', setText='V', setObjectName='chk009', setChecked=True, setToolTip='Divide facet: V coordinate.')
			tb.menu_.add('QCheckBox', setText='Tris', setObjectName='chk010', setToolTip='Divide facet: Tris.')
			return

		dv=u=v=0
		if tb.menu_.chk008.isChecked(): #Split U
			u=2
		if tb.menu_.chk009.isChecked(): #Split V
			v=2

		mode = 0 #The subdivision mode. 0=quads, 1=triangles
		subdMethod = 1 #subdivision type: 0=exponential(traditional subdivision) 1=linear(number of faces per edge grows linearly)
		if tb.menu_.chk010.isChecked(): #tris
			mode=dv=1
			subdMethod=0
		if all([tb.menu_.chk008.isChecked(), tb.menu_.chk009.isChecked()]): #subdivide once into quads
			dv=1
			subdMethod=0
			u=v=0
		#perform operation
		selectedFaces = rt.getFaceSelection()
		# for face in selectedFaces: #when performing polySubdivideFacet on multiple faces, adjacent subdivided faces will make the next face an n-gon and therefore not able to be subdivided. 
		# 	pm.polySubdivideFacet(face, divisions=0, divisionsU=2, divisionsV=2, mode=0, subdMethod=1)


	def tb008(self, state=None):
		'''
		Boolean Operation
		'''
		tb = self.currentUi.tb008
		if state is 'setMenu':
			tb.menu_.add('QRadioButton', setText='Union', setObjectName='chk011', setToolTip='Fuse two objects together.')
			tb.menu_.add('QRadioButton', setText='Difference', setObjectName='chk012', setChecked=True, setToolTip='Indents one object with the shape of another at the point of their intersection.')
			tb.menu_.add('QRadioButton', setText='Intersection', setObjectName='chk013', setToolTip='Keep only the interaction point of two objects.')
			return

		# if tb.menu_.chk011.isChecked(): #union
		# 	mel.eval("polyPerformBooleanAction 1 o 0;") #PolygonBooleanIntersection;

		# if tb.menu_.chk012.isChecked(): #difference
		# 	mel.eval("polyPerformBooleanAction 2 o 0;") #PolygonBooleanDifference;

		# if tb.menu_.chk013.isChecked(): #intersection
		# 	mel.eval("polyPerformBooleanAction 3 o 0;") #PolygonBooleanIntersection;


	@Slots.message
	def tb009(self, state=None):
		'''
		Snap Closest Verts
		'''
		tb = self.ui.tb009
		if state is 'setMenu':
			tb.menu_.add('QDoubleSpinBox', setPrefix='Tolerance: ', setObjectName='s005', setMinMax_='.000-100 step.05', setValue=10, setToolTip='Set the max Snap Distance. Vertices with a distance exceeding this value will be ignored.')
			tb.menu_.add('QCheckBox', setText='Freeze Transforms', setObjectName='chk016', setChecked=True, setToolTip='Freeze Transformations on the object that is being snapped to.')
			return

		tolerance = tb.menu_.s005.value()
		freezetransforms = tb.menu_.chk016.isChecked()

		selection = pm.ls(sl=1, objectsOnly=1)
		if len(selection)>1:
			obj1, obj2 = selection
			Init.snapClosestVerts(obj1, obj2, tolerance, freezetransforms)
		else:
			return 'Error: Operation requires at least two selected objects.'


	def b000(self):
		'''
		Circularize
		'''
		obj = rt.selection[0]
		vertices = rt.polyop.getVertSelection(obj)
		
		Init.circularize(vertices)


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
		Symmetrize
		'''
		pm.mel.Symmetrize()


	def b004(self):
		'''
		Slice
		'''
		rt.macros.run('Ribbon - Modeling', 'CutsQuickSlice')


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


	def b028(self):
		'''
		Quad Draw
		'''
		mel.eval("dR_quadDrawTool;")


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


	def b043(self):
		'''
		Target Weld
		'''
		self.setSubObjectLevel(1) #set component mode to vertex
		rt.macros.run('Editable Polygon Object', 'EPoly_TargetWeld')
		

	def b045(self):
		'''
		Re-Order Vertices
		'''
		# symmetryOn = pm.symmetricModelling(query=True, symmetry=True) #query symmetry state
		
		# if symmetryOn:
		# 	pm.symmetricModelling(symmetry=False)
		# mel.eval("setPolygonDisplaySettings(\"vertIDs\");") #set vertex id on
		# mel.eval("doBakeNonDefHistory( 1, {\"pre\"});") #history must be deleted
		# mel.eval("performPolyReorderVertex;") #start vertex reorder ctx


	def b046(self):
		'''
		Split
		'''
		level = rt.subObjectLevel

		for obj in rt.selection:
			if level==1:
				vertex = rt.polyop.getVertSelection(obj)
				rt.polyop.breakVerts(obj, vertex)

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
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------