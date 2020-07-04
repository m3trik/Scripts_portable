from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Selection(Init):
	def __init__(self, *args, **kwargs):
		super(Selection, self).__init__(*args, **kwargs)

		# try: #set initial checked button states
		# 	state = pm.selectPref(query=True, useDepth=True)
		# 	self.toggleWidgets(setChecked='chk004') #chk004 ignore backfacing (camera based selection)

		# 	#selection style: set initial checked state
		# 	ctx = pm.currentCtx() #flags (ctx, c=True) get the context's class.
		# 	if ctx == 'lassoContext':
		# 		self.cmb004(index=1)
		# 		self.childUi.chk006.setChecked(True)
		# 	elif ctx == 'paintContext':
		# 		self.cmb004(index=2)
		# 		self.childUi.chk007.setChecked(True)
		# 	else: #selectContext
		# 		self.cmb004(index=0)
		# 		self.childUi.chk005.setChecked(True)
		# except NameError:
		# 	pass


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb001', setToolTip='')
			pin.add(QComboBox_, setObjectName='cmb004', setToolTip='Set the select tool type.')
			pin.add('QCheckBox', setText='Ignore Backfacing', setObjectName='chk004', setToolTip='Ignore backfacing components during selection.')
			pin.add(QLabel_, setText='Grow Selection', setObjectName='lbl003', setToolTip='Grow the current selection.')
			pin.add(QLabel_, setText='Shrink Selection', setObjectName='lbl004', setToolTip='Shrink the current selection.')
			return


	@Slots.message
	def txt000(self):
		'''
		Create Selection Set
		'''
		name = str(self.parentUi.txt000.text())+"Set"

		


	def txt001(self):
		'''
		Select By Name
		'''
		searchStr = str(self.parentUi.txt001.text()) #asterisk denotes startswith*, *endswith, *contains* 
		if searchStr:
			selection = rt.select(searchStr)


	def lbl000(self):
		'''
		Selection Sets: Create New
		'''
		cmb = self.parentUi.cmb000
		if not cmb.isEditable():
			cmb.insertItem(0, '')
			cmb.setEditable(True)
			cmb.lineEdit().setPlaceholderText('New Set:')
		else:
			name = cmb.currentText()
			self.creatNewSelectionSet(name)
			self.cmb000() #refresh the sets comboBox
			cmb.setCurrentIndex(0)


	def lbl001(self):
		'''
		Selection Sets: Modify Current
		'''
		cmb = self.parentUi.cmb000
		if not cmb.isEditable():
			cmb.setEditable(True)
			cmb.lineEdit().setPlaceholderText(cmb.currentText())
		else:
			name = cmb.currentText()
			self.modifySet(name)
			cmb.setItemText(cmb.currentIndex(), name)
			# self.cmb000() #refresh the sets comboBox


	def lbl002(self):
		'''
		Selection Sets: Delete Current
		'''
		cmb = self.parentUi.cmb000
		name = cmb.currentText()
		rt.delete(name)

		index = cmb.currentIndex()
		self.cmb000() #refresh the sets comboBox


	def lbl003(self):
		'''
		Selection Sets: Select Current
		'''
		cmb = self.parentUi.cmb000
		name = cmb.currentText()
		if cmb.currentIndex()>0:
			rt.select(name) # pm.select(name, noExpand=1) #Select The Selection Set Itself (Not Members Of) (noExpand=select set)



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
		self.toggleWidgets(setUnChecked='chk001-2')


	def chk001(self):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.toggleWidgets(setUnChecked='chk000,chk002')


	def chk002(self):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.toggleWidgets(setUnChecked='chk000-1')


	@Slots.message
	def chk004(self):
		'''
		Ignore Backfacing (Camera Based Selection)
		'''
		for obj in rt.selection:
			if self.childUi.chk004.isChecked():
				sel.ignoreBackfacing = True
				return 'Camera-based selection <hl>On</hl>.'
			else:
				sel.ignoreBackfacing = False
				return 'Camera-based selection <hl>Off</hl>.'


	@Slots.message
	def chk005(self):
		'''
		Select Style: Marquee
		'''
		self.toggleWidgets(setChecked='chk005', setUnChecked='chk006-7')
		self.parentUi.cmb004.setCurrentIndex(0)
		return 'Select Style: <hl>Marquee</hl>'


	@Slots.message
	def chk006(self):
		'''
		Select Style: Lasso
		'''
		self.toggleWidgets(setChecked='chk006', setUnChecked='chk005,chk007')
		self.parentUi.cmb004.setCurrentIndex(3)
		return 'Select Style: <hl>Lasso</hl>'


	@Slots.message
	def chk007(self):
		'''
		Select Style: Paint
		'''
		self.toggleWidgets(setChecked='chk007', setUnChecked='chk005-6')
		self.parentUi.cmb004.setCurrentIndex(4)
		return 'Select Style: <hl>Paint</hl>'


	def cmb000(self, index=None):
		'''
		List Selection Sets
		'''
		cmb = self.parentUi.cmb000

		if index=='setMenu':
			cmb.addToContext(QLabel_, setText='Select', setObjectName='lbl003', setToolTip='Select the current set elements.')
			cmb.addToContext(QLabel_, setText='New', setObjectName='lbl000', setToolTip='Create a new selection set.')
			cmb.addToContext(QLabel_, setText='Modify', setObjectName='lbl001', setToolTip='Modify the current set by renaming and/or changing the selection.')
			cmb.addToContext(QLabel_, setText='Delete', setObjectName='lbl002', setToolTip='Delete the current set.')
			cmb.returnPressed.connect(lambda m=cmb.lastActiveChild: getattr(self, m(name=1))())
			return

		selectionSets = [s for s in rt.selectionSets]
		items = cmb.addItems_([s.name for s in selectionSets])

		self._currentSet = cmb.currentText()


	def cmb001(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb001
		
		if index=='setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Select All Of Type
		'''
		cmb = self.parentUi.cmb002
	
		if index=='setMenu':
			list_ = ['Geometry', 'Shapes', 'Lights', 'Cameras', 'Helpers', 'Space Warps', 'Particle Systems', 'Bone Objects']
			cmb.addItems_(list_, 'Select by Type:')
			return

		if index>0:
			if index==cmb.items.index('Geometry'): #Select all Geometry
				rt.select(rt.geometry)
			elif index==cmb.items.index('Shapes'): #Select all Geometry
				rt.select(rt.shapes)
			elif index==cmb.items.index('Lights'): #Select all Geometry
				rt.select(rt.lights)
			elif index==cmb.items.index('Cameras'): #Select all Geometry
				rt.select(rt.cameras)
			elif index==cmb.items.index('Helpers'): #Select all Geometry
				rt.select(rt.helpers)
			elif index==cmb.items.index('Space Warps'): #Select all Geometry
				rt.select(rt.spacewarps)
			elif index==cmb.items.index('Particle Systems'): #Select all Geometry
				rt.select(rt.particelsystems)
			elif index==cmb.items.index('Bone Objects'): #Select all Geometry
				rt.select(rt.boneobjects)

			cmb.setCurrentIndex(0)


	def cmb003(self, index=None):
		'''
		Convert To
		'''
		cmb = self.parentUi.cmb003

		if index=='setMenu':
			list_ = ['Vertex', 'Edge', 'Border', 'Face', 'Element']
			cmb.addItems_(list_, 'Convert To:')
			return

		if index>0:
			for obj in rt.selection:
				for i in list_:
					if index==cmb.items.index(i):
						obj.convertSelection('CurrentLevel', i) #Convert current selection to index of string i
						# rt.setSelectionLevel(obj, i) #Change component mode to i
						rt.subObjectLevel = items.index(i)
			cmb.setCurrentIndex(0)


	def cmb004(self, index=None):
		'''
		Select Style: Set Context
		'''
		cmb = self.parentUi.cmb004

		if index=='setMenu':
			list_ = ['Marquee', 'Circular', 'Fence', 'Lasso', 'Paint'] 
			cmb.addItems_(list_, 'Select Tool Style:')
			return

		if index>0:
			if index==cmb.items.index('Marquee'):
				maxEval('actionMan.executeAction 0 "59232"') #Rectangular select region
			elif index==cmb.items.index('Circular'):
				maxEval('actionMan.executeAction 0 "59233"') #Circular select region
			elif index==cmb.items.index('Fence'):
				maxEval('actionMan.executeAction 0 "59234"') #Fence select region
			elif index==cmb.items.index('Lasso'):
				maxEval('actionMan.executeAction 0 "59235"') #Lasso select region
			elif index==cmb.items.index('Paint'):
				maxEval('actionMan.executeAction 0 "59236"') #Paint select region
			cmb.setCurrentIndex(0)


	def cmb005(self, index=None):
		'''
		Selection Contraints
		'''
		cmb = self.parentUi.cmb005

		if index=='setMenu':
			list_ = ['Off', 'Angle', 'Border', 'Edge Loop', 'Edge Ring', 'Shell', 'UV Edge Loop']
			cmb.addItems_(list_, 'Off')
			return

		# if index>0:
		# 	if index==cmb.items.index('Angle'):
		# 		mel.eval('dR_selConstraintAngle;') #dR_DoCmd("selConstraintAngle");
		# 	elif index==cmb.items.index('Border'):
		# 		mel.eval('dR_selConstraintBorder;') #dR_DoCmd("selConstraintBorder");
		# 	elif index==cmb.items.index('Edge Loop'):
		# 		mel.eval('dR_selConstraintEdgeLoop;') #dR_DoCmd("selConstraintEdgeLoop");
		# 	elif index==cmb.items.index('Edge Ring'):
		# 		mel.eval('dR_selConstraintEdgeRing;') #dR_DoCmd("selConstraintEdgeRing");
		# 	elif index==cmb.items.index('Shell'):
		# 		mel.eval('dR_selConstraintElement;') #dR_DoCmd("selConstraintElement");
		# 	elif index==cmb.items.index('UV Edge Loop'):
		# 		mel.eval('dR_selConstraintUVEdgeLoop;') #dR_DoCmd("selConstraintUVEdgeLoop");
		# else:
		# 	mel.eval('dR_selConstraintOff;') #dR_DoCmd("selConstraintOff");


	def tb000(self, state=None):
		'''
		Select Nth
		'''
		tb = self.currentUi.tb000
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='Component Ring', setObjectName='chk000', setToolTip='Select component ring.')
			tb.add('QCheckBox', setText='Component Loop', setObjectName='chk001', setChecked=True, setToolTip='Select all contiguous components that form a loop with the current selection.')
			tb.add('QCheckBox', setText='Shortest Path', setObjectName='chk002', setToolTip='Shortest component path between two selected vertices or UV\'s.')
			tb.add('QSpinBox', setPrefix='Step: ', setObjectName='s003', minMax_='1-100 step1', setValue=1, setToolTip='Step Amount.')
			if state=='setMenu':
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
		if not tb.containsMenuItems:
			tb.add('QDoubleSpinBox', setPrefix='Tolerance: ', setObjectName='s000', minMax_='0.0-10 step.1', setValue=0.3, setToolTip='Select similar objects or components, depending on selection mode.')
			if state=='setMenu':
				return

		tolerance = str(tb.s000.value()) #string value because mel.eval is sending a command string
		# mel.eval("doSelectSimilar 1 {\""+ tolerance +"\"}")


	def tb002(self, state=None):
		'''
		Select Island: Select Polygon Face Island
		'''
		tb = self.currentUi.tb002
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='Lock Values', setObjectName='chk003', setChecked=True, setToolTip='Keep values in sync.')
			tb.add('QDoubleSpinBox', setPrefix='x: ', setObjectName='s002', minMax_='0.00-1 step.01', setValue=0.01, setToolTip='Normal X range.')
			tb.add('QDoubleSpinBox', setPrefix='y: ', setObjectName='s004', minMax_='0.00-1 step.01', setValue=0.01, setToolTip='Normal Y range.')
			tb.add('QDoubleSpinBox', setPrefix='z: ', setObjectName='s005', minMax_='0.00-1 step.01', setValue=0.01, setToolTip='Normal Z range.')
			if state=='setMenu':
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
		# print(sel)
		# setFaceSelection sel #{}


	def lbl003(self):
		'''
		Grow Selection
		'''
		# expand functionalitly to grow according to selection type
		#grow line #PolytoolsSelect.Pattern7 1
		#grow loop #PolytoolsSelect.GrowLoop()
		#grow ring #PolytoolsSelect.GrowRing()
		for obj in rt.selection:
			obj.EditablePoly.GrowSelection()


	def lbl004(self):
		'''
		Shrink Selection
		'''
		for obj in rt.selection:
			obj.EditablePoly.ShrinkSelection()


	@Slots.message
	def creatNewSelectionSet(self, name=None):
		'''
		Selection Sets: Create a new selection set.
		'''
		if rt.isValidObj(name): # obj!=rt.undefined
			return 'Error: Set with name <hl>{}</hl> already exists.'.format(name)

		else: #create set
			sel = rt.selection
			if sel:
				if not name: #name=='set#Set': #generate a generic name based on obj.name
					num = self.cycle(list(range(99)), 'selectionSetNum')
					name=sel[0].name+'Set'+str(num)

				rt.selectionSets[name]
			else:
				return 'Error: No valid objects selected.'


	@Slots.message
	def modifySet(self, name):
		'''
		Selection Sets: Modify Current by renaming or changing the set members.
		'''
		node = rt.getNodeByName(self._currentSet)
		node.name = name

		if pm.objExists(name):
			rt.selectionSets[name]





		




#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------