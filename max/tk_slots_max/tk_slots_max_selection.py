import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Selection(Init):
	def __init__(self, *args, **kwargs):
		super(Selection, self).__init__(*args, **kwargs)
		
		
		
		
		#set checked button states
		#chk004 ignore backfacing (camera based selection)
		# sel = rt.Filters.GetModOrObj()
		# state = sel.ignoreBackfacing
		# self.hotBox.ui.chk004.setChecked(state)

		#on click event
		self.hotBox.ui.chk003.clicked.connect(self.b001) #un-paint

		#symmetry: set initial checked state
		# state = pm.symmetricModelling(query=True, symmetry=True) #application symmetry state
		# axis = pm.symmetricModelling(query=True, axis=True)
		# if axis == "x":
		# 	self.hotBox.ui.chk000.setChecked(state)
		# if axis == "y":
		# 	self.hotBox.ui.chk001.setChecked(state)
		# if axis == "z":
		# 	self.hotBox.ui.chk002.setChecked(state)

	def setSymmetry(self, axis, symmetry):
		if self.hotBox.ui.chk005.isChecked():
			space = "object"
		if self.hotBox.ui.chk006.isChecked():
			space = "topo"
		else:
			space = "world"

		tolerance = float(self.hotBox.ui.s005.value())
		pm.symmetricModelling(edit=True, symmetry=symmetry, axis=axis, about=space, tolerance=tolerance)


	def t000(self):
		'''
		Select The Selection Set Itself (Not Members Of)

		'''
		name = str(self.hotBox.ui.t000.text())+"Set"
		pm.select (name, noExpand=1) #noExpand=select set itself

	def t001(self):
		'''
		Select By Name

		'''
		searchStr = str(self.hotBox.ui.t001.text()) #asterisk denotes startswith*, *endswith, *contains* 
		if searchStr:
			selection = pm.select (pm.ls (searchStr))

	def chk000(self):
		'''
		Symmetry X

		'''
		self.setButtons(self.hotBox.ui, unchecked='chk001,chk002')
		state = self.hotBox.ui.chk000.isChecked() #symmetry button state
		self.setSymmetry("x", symmetry=state)

	def chk001(self):
		'''
		Symmetry Y

		'''
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk002')
		state = self.hotBox.ui.chk001.isChecked() #symmetry button state
		self.setSymmetry("y", symmetry=state)

	def chk002(self):
		'''
		Symmetry Z

		'''
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk001')
		state = self.hotBox.ui.chk002.isChecked() #symmetry button state
		self.setSymmetry("z", symmetry=state)

	def chk004(self):
		'''
		Ignore Backfacing (Camera Based Selection)

		'''
		sel = rt.Filters.GetModOrObj()

		if self.hotBox.ui.chk004.isChecked():
			sel.ignoreBackfacing = True
			# self.viewPortMessage("Camera-based selection <hl>On</hl>.")
		else:
			sel.ignoreBackfacing = False
			# self.viewPortMessage("Camera-based selection <hl>Off</hl>.")

	def chk005(self):
		'''
		Symmetry: Object

		'''
		self.hotBox.ui.chk006.setChecked(False) #uncheck symmetry:topological
	
	def chk006(self):
		'''
		Symmetry: Topo

		'''
		self.hotBox.ui.chk005.setChecked(False) #uncheck symmetry:object space
		if any ([self.hotBox.ui.chk000.isChecked(), self.hotBox.ui.chk001.isChecked(), self.hotBox.ui.chk002.isChecked()]): #(symmetry)
			pm.symmetricModelling(edit=True, symmetry=False)
			self.setButtons(self.hotBox.ui, unchecked='chk000,chk001,chk002')
			print "# Warning: First select a seam edge and then check the symmetry button to enable topographic symmetry #"


	def cmb000(self):
		'''
		List Selection Sets

		'''
		cmb = self.hotBox.ui.cmb000
		index = cmb.currentIndex() #get current index before refreshing list
		
		selectionSets = [set for set in rt.selectionSets]
		
		sets = self.comboBox (cmb, [set.name for set in selectionSets], "Sets")

		
		if index!=0:
			rt.select(sets[index])
			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		

		'''
		pass

	def cmb002(self):
		'''
		Select All Of Type

		'''
		cmb = self.hotBox.ui.cmb001
		index = cmb.currentIndex() #get current index before refreshing list
		
		list_ = ['Geometry']
		self.comboBox (cmb, list_, 'Select by Type')

		if index!=0:
			if index==list_.index('Geometry') #Select all Geometry
				rt.select(rt.geometry)
			cmb.setCurrentIndex(0)


	def cmb003(self):
		'''
		Convert Selection to

		'''
		cmb = self.ui.cmb003

		list_ = ['Verts', 'Edge', 'Face', 'Border']
		files = self.comboBox (cmb, list_, 'Convert Selection to')

		sel= rt.selection

		if index!=0:
			if index==files.index('Verts'): #Convert Selection To Vertices
				if rt.subObjectLevel==2:
					sel.convertselection ('Edge', 'Vertices')
				if rt.subObjectLevel==4:
					sel.convertselection ('Face', 'Vertices')
				if rt.subObjectLevel==3:
					sel.convertselection ('Border', 'Vertices')
			if index==files.index('Edges'): #Convert Selection To Edges
				if rt.subObjectLevel==1:
					sel.convertselection ('Vertex', 'Edge')
				if rt.subObjectLevel==4:
					sel.convertselection ('Face', 'Edge')
				if rt.subObjectLevel==3:
					sel.convertselection ('Border', 'Edge')
			if index==files.index('Faces'): #Convert Selection To Faces
				if rt.subObjectLevel==2:
					sel.convertselection ('Edge', 'Faces')
				if rt.subObjectLevel==1:	
					sel.convertselection ('Vertex', 'Faces')
				if rt.subObjectLevel==3:	
					sel.convertselection ('Border', 'Faces')
			if index==files.index('Border'): #Convert Selection To Border
				if rt.subObjectLevel==2:	
					sel.convertselection ('Edge', 'Border')
				if rt.subObjectLevel==4:	
					sel.convertselection ('Face', 'Border')
				if rt.subObjectLevel==1:	
					sel.convertselection ('Vertex', 'Border')
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Create Selection Set

		'''
		name = str(self.hotBox.ui.t000.text())+"Set"
		if pm.objExists (name):
			pm.sets (name, clear=1)
			pm.sets (name, add=1) #if set exists; clear set and add current selection 
		else: #create set
			pm.sets (name=name, text="gCharacterSet")
			self.hotBox.ui.t000.clear()
			
	def b001(self):
		'''
		Paint Select

		'''
		if pm.contextInfo ("paintSelect", exists=True):
			pm.deleteUI ("paintSelect")

		radius = float(self.hotBox.ui.s001.value()) #Sets the size of the brush. C: Default is 1.0 cm. Q: When queried, it returns a float.
		lowerradius = 2.5 #Sets the lower size of the brush (only apply on tablet).
		selectop = "select"
		if self.hotBox.ui.chk003.isChecked():
			selectop = "unselect"

		pm.artSelectCtx ("paintSelect", selectop=selectop, radius=radius, lowerradius=lowerradius)#, beforeStrokeCmd=beforeStrokeCmd())
		pm.setToolTo ("paintSelect")

	def b002(self):
		'''
		

		'''
		pass

	def b003(self):
		'''
		

		'''
		pass

	def b004(self):
		'''
		

		'''
		pass

	def b005(self):
		'''
		

		'''
		pass

	def b006(self):
		'''
		Select Similar
		'''
		tolerance = str(self.hotBox.ui.s000.value()) #string value because mel.eval is sending a command string
		mel.eval("doSelectSimilar 1 {\""+ tolerance +"\"}")

	def b007(self):
		'''
		Select Polygon Face Island

		'''
		rangeX=rangeY=rangeZ = float(self.hotBox.ui.s002.value())

		curmod = rt.Modpanel.getcurrentObject()
		curmod.selectAngle=rangeX
		curmod.selectByAngle= not curmod.selectByAngle

		# $.selectAngle=rangeX
		# $.selectByAngle = on
		# sel = $.selectedfaces as bitarray #maintains current single selection. need to reselect with angle contraint active to make work.
		# $.selectByAngle = off
		# print sel
		# setFaceSelection sel #{}


	def b008(self):
		'''
		Select N-th in Loop
		'''
		if rt.subObjectLevel==2: #Edge
			mel.eval("selectEveryNEdge;")
		elif rt.subObjectLevel==4: #Face
			self.selectFaceLoop(tolerance=50)

	def b009(self):
		'''
		Select Edge Ring

		'''
		if rt.subObjectLevel==2: #Edge
			print "# Warning: add correct arguments for this tool #" 
			self.shortestEdgePath()
		elif rt.subObjectLevel==4: #Face
			pass

	def b10(self):
		'''
		Select Contigious Loop

		'''
		if rt.subObjectLevel==2: #Edge
			maxEval('''
			curmod = Modpanel.getcurrentObject()
			if ( Ribbon_Modeling.IsEditablePoly() ) then
			(
				curmod.SelectEdgeRing();
			)
			else
			(
				curmod.ButtonOp #SelectEdgeRing;
			)
			''')
		elif rt.subObjectLevel==4: #Face
			pass

	def b011(self):
		'''
		Shortest Edge Path

		'''
		self.shortestEdgePath()
		# maxEval('SelectShortestEdgePathTool;')

	def b012(self):
		'''
		Selection Constraints

		'''
		maxEval('PolygonSelectionConstraints;')

	def b013(self):
		'''
		Lasso Select

		'''
		mel.eval("LassoTool;")

	def b014(self):
		'''
		Grow Selection

		'''
		# expand functionalitly to grow according to selection type
		#grow line #PolytoolsSelect.Pattern7 1
		#grow loop #PolytoolsSelect.GrowLoop()
		#grow ring #PolytoolsSelect.GrowRing()
		for obj in rt.selection:
			obj.EditablePoly.GrowSelection()

	def b015(self):
		'''
		Shrink Selection

		'''
		for obj in rt.selection:
			obj.EditablePoly.ShrinkSelection()

	def b016(self):
		'''
		

		'''
		pass

	def b017(self):
		'''
		

		'''
		pass

	def b018(self):
		'''
		

		'''
		pass

	def b019(self):
		'''
		

		'''
		pass

	def b020(self):
		'''

		'''
		pass





		



		



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------