import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Selection(Init):
	def __init__(self, *args, **kwargs):
		super(Selection, self).__init__(*args, **kwargs)
		
		
		self.ui = self.sb.getUi('selection')
		
		#set checked button states
		#chk004 ignore backfacing (camera based selection)
		# sel = rt.Filters.GetModOrObj()
		# state = sel.ignoreBackfacing
		# self.ui.chk004.setChecked(state)

		#on click event
		self.ui.chk003.clicked.connect(self.b001) #un-paint




	def t000(self):
		'''
		Select The Selection Set Itself (Not Members Of)

		'''
		name = str(self.ui.t000.text())+"Set"
		pm.select (name, noExpand=1) #noExpand=select set itself

	def t001(self):
		'''
		Select By Name

		'''
		searchStr = str(self.ui.t001.text()) #asterisk denotes startswith*, *endswith, *contains* 
		if searchStr:
			selection = pm.select (pm.ls (searchStr))

	def chk000(self):
		'''
		

		'''
		pass

	def chk001(self):
		'''
		

		'''
		pass

	def chk002(self):
		'''
		

		'''
		pass

	def chk004(self):
		'''
		Ignore Backfacing (Camera Based Selection)

		'''
		sel = rt.Filters.GetModOrObj()

		if self.ui.chk004.isChecked():
			sel.ignoreBackfacing = True
			# self.viewPortMessage("Camera-based selection <hl>On</hl>.")
		else:
			sel.ignoreBackfacing = False
			# self.viewPortMessage("Camera-based selection <hl>Off</hl>.")

	def chk005(self):
		'''
		

		'''
		pass
	
	def chk006(self):
		'''
		

		'''
		pass

	def cmb000(self):
		'''
		List Selection Sets

		'''
		cmb = self.ui.cmb000
		
		selectionSets = [set for set in rt.selectionSets]
		contents = self.comboBox (cmb, [set.name for set in selectionSets], "Sets")

		index = cmb.currentIndex()
		if index!=0:
			rt.select(contents[index])
			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		List current selection

		'''
		cmb = self.ui.cmb001
		
		if rt.subObjectLevel==1:
			type_ = 'Vertices'
			sel = self.bitArrayIndex(rt.polyop.getVertSelection(obj))
		elif rt.subObjectLevel==2:
			type_ = 'Edges'
			sel = self.bitArrayIndex(rt.polyop.getEdgeSelection(obj))
		elif rt.subObjectLevel==4:
			type_ = 'Faces'
			sel = self.bitArrayIndex(rt.polyop.getFaceSelection(obj))
		else:
			type_ = 'Objects'
			sel = [obj for obj in rt.selection]

		contents = self.comboBox (cmb, sel, 'Selected '+type_+':')

		index = cmb.currentIndex()
		if index!=0:
			rt.select(contents[index])
			cmb.setCurrentIndex(0)


	def cmb002(self):
		'''
		Select All Of Type

		'''
		cmb = self.ui.cmb002
		
		list_ = ['Geometry', 'Shapes', 'Lights', 'Cameras', 'Helpers', 'Space Warps', 'Particle Systems', 'Bone Objects']
		contents = self.comboBox (cmb, list_, 'Select by Type:')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Geometry'): #Select all Geometry
				rt.select(rt.geometry)
			if index==contents.index('Shapes'): #Select all Geometry
				rt.select(rt.shapes)
			if index==contents.index('Lights'): #Select all Geometry
				rt.select(rt.lights)
			if index==contents.index('Cameras'): #Select all Geometry
				rt.select(rt.cameras)
			if index==contents.index('Helpers'): #Select all Geometry
				rt.select(rt.helpers)
			if index==contents.index('Space Warps'): #Select all Geometry
				rt.select(rt.spacewarps)
			if index==contents.index('Particle Systems'): #Select all Geometry
				rt.select(rt.particelsystems)
			if index==contents.index('Bone Objects'): #Select all Geometry
				rt.select(rt.boneobjects)

			cmb.setCurrentIndex(0)


	def cmb003(self):
		'''
		Convert Selection to

		'''
		cmb = self.ui.cmb003

		list_ = ['Verts', 'Edge', 'Face', 'Border']
		contents = self.comboBox (cmb, list_, 'Convert to')
		
		sel= rt.selection
		
		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Verts'): #Convert Selection To Vertices
				if rt.subObjectLevel==2:
					sel.convertselection ('Edge', 'Vertices')
				if rt.subObjectLevel==4:
					sel.convertselection ('Face', 'Vertices')
				if rt.subObjectLevel==3:
					sel.convertselection ('Border', 'Vertices')
			elif index==contents.index('Edges'): #Convert Selection To Edges
				if rt.subObjectLevel==1:
					sel.convertselection ('Vertex', 'Edge')
				if rt.subObjectLevel==4:
					sel.convertselection ('Face', 'Edge')
				if rt.subObjectLevel==3:
					sel.convertselection ('Border', 'Edge')
			elif index==contents.index('Faces'): #Convert Selection To Faces
				if rt.subObjectLevel==2:
					sel.convertselection ('Edge', 'Faces')
				if rt.subObjectLevel==1:	
					sel.convertselection ('Vertex', 'Faces')
				if rt.subObjectLevel==3:	
					sel.convertselection ('Border', 'Faces')
			elif index==contents.index('Border'): #Convert Selection To Border
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
		name = str(self.ui.t000.text())+"Set"

		sel = rt.selection

		if sel:
			if name=='set#Set': #generate a generic name based on obj.name
				num = self.cycle(list(range(99)), 'selectionSetNum')
				name=sel[0].name+'Set'+str(num)
				rt.selectionSets[name]
			else:
				rt.selectionSets[name] #if set exists, overwrite set; else create set
		else:
			print '# Warning: No valid objects selected. #'


	def b001(self):
		'''
		Paint Select

		'''
		if pm.contextInfo ("paintSelect", exists=True):
			pm.deleteUI ("paintSelect")

		radius = float(self.ui.s001.value()) #Sets the size of the brush. C: Default is 1.0 cm. Q: When queried, it returns a float.
		lowerradius = 2.5 #Sets the lower size of the brush (only apply on tablet).
		selectop = "select"
		if self.ui.chk003.isChecked():
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
		tolerance = str(self.ui.s000.value()) #string value because mel.eval is sending a command string
		mel.eval("doSelectSimilar 1 {\""+ tolerance +"\"}")

	def b007(self):
		'''
		Select Polygon Face Island

		'''
		rangeX=rangeY=rangeZ = float(self.ui.s002.value())

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
		Select Loop
		'''
		maxEval('macros.run "PolyTools" "Loop"')
		
		# if rt.subObjectLevel==2: #Edge
		# 	mel.eval("selectEveryNEdge;")
		# elif rt.subObjectLevel==4: #Face
		# 	self.selectFaceLoop(tolerance=50)

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