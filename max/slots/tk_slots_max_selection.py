from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Selection(Init):
	def __init__(self, *args, **kwargs):
		super(Selection, self).__init__(*args, **kwargs)

		#set checked button states
		#chk004 ignore backfacing (camera based selection)
		# sel = rt.Filters.GetModOrObj()
		# state = sel.ignoreBackfacing
		# self.parentUi.chk004.setChecked(state)

		# #selection style: set initial checked state
		# ctx = pm.currentCtx() #flags (ctx, c=True) get the context's class.
		# if ctx == 'lassoContext':
		# 	self.cmb004(index=1)
		# 	self.childUi.chk006.setChecked(True)
		# elif ctx == 'paintContext':
		# 	self.cmb004(index=2)
		# 	self.childUi.chk007.setChecked(True)
		# else: #selectContext
		# 	self.cmb004(index=0)
		# 	self.childUi.chk005.setChecked(True)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb001', setToolTip='')

			return


	def cmb001(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb001
		
		files = ['']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	def t000(self):
		'''
		Select The Selection Set Itself (Not Members Of)
		'''
		name = str(self.parentUi.t000.text())+"Set"
		pm.select (name, noExpand=1) #noExpand=select set itself


	def t001(self):
		'''
		Select By Name
		'''
		searchStr = str(self.parentUi.t001.text()) #asterisk denotes startswith*, *endswith, *contains* 
		if searchStr:
			selection = rt.select(searchStr)


	def s002(self):
		'''
		Select Island: tolerance x
		'''
		tb = self.currentUi.tb002
		if tb.chk003.isChecked():
			text = tb.s002.value()
			tb.s004.setValue(text)
			tb.s005.setValue(text)


	def s004(self):
		'''
		Select Island: tolerance y
		'''
		tb = self.currentUi.tb002
		if tb.chk003.isChecked():
			text = tb.s004.value()
			tb.s002.setValue(text)
			tb.s005.setValue(text)


	def s005(self):
		'''
		Select Island: tolerance z
		'''
		tb = self.currentUi.tb002
		if tb.chk003.isChecked():
			text = tb.s005.value()
			tb.s002.setValue(text)
			tb.s004.setValue(text)


	def chk000(self):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk001-2')


	def chk001(self):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk000,chk002')


	def chk002(self):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk000-1')


	def chk004(self):
		'''
		Ignore Backfacing (Camera Based Selection)
		'''
		for obj in rt.selection:
			if self.parentUi.chk004.isChecked():
				sel.ignoreBackfacing = True
				# self.viewPortMessage("Camera-based selection <hl>On</hl>.")
			else:
				sel.ignoreBackfacing = False
				# self.viewPortMessage("Camera-based selection <hl>Off</hl>.")


	def chk005(self):
		'''
		Select Style: Marquee
		'''
		self.setSelectionStyle('selectContext')
		self.toggleWidgets(self.parentUi, self.childUi, setChecked='chk005', setChecked_False='chk006-7')
		self.parentUi.cmb004.setCurrentIndex(0)


	def chk006(self):
		'''
		Select Style: Lasso
		'''
		self.setSelectionStyle('lassoContext')
		self.toggleWidgets(self.parentUi, self.childUi, setChecked='chk006', setChecked_False='chk005,chk007')
		self.parentUi.cmb004.setCurrentIndex(1)


	def chk007(self):
		'''
		Select Style: Paint
		'''
		self.setSelectionStyle('paintContext')
		self.toggleWidgets(self.parentUi, self.childUi, setChecked='chk007', setChecked_False='chk005-6')
		self.parentUi.cmb004.setCurrentIndex(2)


	def setSelectionStyle(self, ctx):
		'''
		Set the selection style context.
		args:
			ctx (str) = Selection style context. Possible values include: 'marquee', 'lasso', 'drag'.
		'''
		if pm.contextInfo(ctx, exists=True):
			pm.deleteUI(ctx)

		if ctx=='selectContext':
			ctx = pm.selectContext(ctx)
		elif ctx=='lassoContext':
			ctx = pm.lassoContext(ctx)
		elif ctx=='paintContext':
			ctx = pm.artSelectCtx(ctx)

		pm.setToolTo(ctx)
		self.viewPortMessage('Select Style: <hl>'+ctx+'</hl>')


	def cmb000(self, index=None):
		'''
		List Selection Sets
		'''
		cmb = self.parentUi.cmb000

		selectionSets = [set for set in rt.selectionSets]
		contents = cmb.addItems_([set.name for set in selectionSets], "Sets")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			rt.select(contents[index])
			cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Select All Of Type
		'''
		cmb = self.parentUi.cmb002
	
		list_ = ['Geometry', 'Shapes', 'Lights', 'Cameras', 'Helpers', 'Space Warps', 'Particle Systems', 'Bone Objects']
		contents = cmb.addItems_(list_, 'Select by Type:')

		if not index:
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


	def cmb003(self, index=None):
		'''
		Convert To
		'''
		cmb = self.parentUi.cmb003

		list_ = ['Vertex', 'Edge', 'Border', 'Face', 'Element']
		contents = cmb.addItems_(list_, 'Convert To')
		
		if not index:
			index = cmb.currentIndex()
		if index!=0:
			for obj in rt.selection:
				for i in list_:
					if index==contents.index(i):
						obj.convertSelection('CurrentLevel', i) #Convert current selection to index of string i
						# rt.setSelectionLevel(obj, i) #Change component mode to i
						rt.subObjectLevel = contents.index(i)
			cmb.setCurrentIndex(0)


	def cmb004(self, index=None):
		'''
		Select Style: Set Context
		'''
		cmb = self.parentUi.cmb004

		list_ = ['Marquee', 'Lasso', 'Paint'] 

		contents = cmb.addItems_(list_)

		if not index:
			index = cmb.currentIndex()

		if index==contents.index('Marquee'): #
			self.chk005()
		if index==contents.index('Lasso'): #
			self.chk006()
		if index==contents.index('Paint'): #
			self.chk007()


	def tb000(self, state=None):
		'''
		Select Nth
		'''
		tb = self.currentUi.tb000
		if state=='setMenu':
			tb.add('QCheckBox', setText='Component Ring', setObjectName='chk000', setToolTip='Select component ring.')
			tb.add('QCheckBox', setText='Component Loop', setObjectName='chk001', setChecked=True, setToolTip='Select all contiguous components that form a loop with the current selection.')
			tb.add('QCheckBox', setText='Shortest Path', setObjectName='chk002', setToolTip='Shortest component path between two selected vertices or UV\'s.')
			tb.add('QSpinBox', setPrefix='Step: ', setObjectName='s003', minMax_='1-100 step1', setValue=1, setToolTip='Step Amount.')
			return

		step = tb.s003.value()

		if tb.chk000.isChecked(): #Select Ring
			rt.macros.run('PolyTools', 'Ring')

		elif tb.chk001.isChecked(): #Select contigious
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

		elif tb.chk002.isChecked(): #Shortest Edge Path
			self.shortestEdgePath()
			# maxEval('SelectShortestEdgePathTool;')

		else: #Select Loop
			rt.macros.run('PolyTools', 'Loop')
			
			# if rt.subObjectLevel==2: #Edge
			# 	mel.eval("selectEveryNEdge;")
			# elif rt.subObjectLevel==4: #Face
			# 	self.selectFaceLoop(tolerance=50)


	def tb001(self, state=None):
		'''
		Select Similar
		'''
		tb = self.currentUi.tb001
		if state=='setMenu':
			tb.add('QDoubleSpinBox', setPrefix='Tolerance: ', setObjectName='s000', minMax_='0.0-10 step.1', setValue=0.3, setToolTip='Select similar objects or components, depending on selection mode.')
			return

		tolerance = str(tb.s000.value()) #string value because mel.eval is sending a command string
		mel.eval("doSelectSimilar 1 {\""+ tolerance +"\"}")


	def tb002(self, state=None):
		'''
		Select Island: Select Polygon Face Island
		'''
		tb = self.currentUi.tb002
		if state=='setMenu':
			tb.add('QCheckBox', setText='Lock Values', setObjectName='chk003', setChecked=True, setToolTip='Keep values in sync.')
			tb.add('QDoubleSpinBox', setPrefix='x: ', setObjectName='s002', minMax_='0.00-1 step.01', setValue=0.01, setToolTip='Normal X range.')
			tb.add('QDoubleSpinBox', setPrefix='y: ', setObjectName='s004', minMax_='0.00-1 step.01', setValue=0.01, setToolTip='Normal Y range.')
			tb.add('QDoubleSpinBox', setPrefix='z: ', setObjectName='s005', minMax_='0.00-1 step.01', setValue=0.01, setToolTip='Normal Z range.')
			return

		rangeX = float(tb.s002.value())
		rangeY = float(tb.s004.value())
		rangeZ = float(tb.s005.value())

		curmod = rt.Modpanel.getcurrentObject()
		curmod.selectAngle = rangeX
		curmod.selectByAngle = not curmod.selectByAngle

		# $.selectAngle=rangeX
		# $.selectByAngle = on
		# sel = $.selectedfaces as bitarray #maintains current single selection. need to reselect with angle contraint active to make work.
		# $.selectByAngle = off
		# print sel
		# setFaceSelection sel #{}


	def b000(self):
		'''
		Create Selection Set
		'''
		name = str(self.parentUi.t000.text())+"Set"

		sel = rt.selection

		if sel:
			if name=='set#Set': #generate a generic name based on obj.name
				num = self.cycle(list(range(99)), 'selectionSetNum')
				name=sel[0].name+'Set'+str(num)
				rt.selectionSets[name]
			else:
				rt.selectionSets[name] #if set exists, overwrite set; else create set
		else:
			print('# Warning: No valid objects selected. #')


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





		




#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------