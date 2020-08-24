from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Selection(Init):
	def __init__(self, *args, **kwargs):
		super(Selection, self).__init__(*args, **kwargs)


		# try: #set initial checked button states
		# 	state = pm.selectPref(query=True, useDepth=True)
		# 	self.selection_submenu.chk004.setChecked(state) #chk004 ignore backfacing (camera based selection)

		# 	#selection style: set initial checked state
		# 	ctx = pm.currentCtx() #flags (ctx, c=True) get the context's class.
		# 	if ctx == 'lassoContext':
		# 		self.cmb004(index=2)
		# 		self.selection_submenu.chk006.setChecked(True)
		# 	elif ctx == 'paintContext':
		# 		self.cmb004(index=3)
		# 		self.selection_submenu.chk007.setChecked(True)
		# 	else: #selectContext
		# 		self.cmb004(index=1)
		# 		self.selection_submenu.chk005.setChecked(True)
		# except NameError:
		# 	pass


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.selection.pin

		if state is 'setMenu':
			pin.contextMenu.add(QComboBox_, setObjectName='cmb001', setToolTip='')
			pin.contextMenu.add(QComboBox_, setObjectName='cmb004', setToolTip='Set the select tool type.')
			pin.contextMenu.add('QCheckBox', setText='Ignore Backfacing', setObjectName='chk004', setToolTip='Ignore backfacing components during selection.')
			pin.contextMenu.add('QCheckBox', setText='Soft Selection', setObjectName='chk008', setToolTip='Toggle soft selection mode.')
			pin.contextMenu.add(QLabel_, setText='Grow Selection', setObjectName='lbl003', setToolTip='Grow the current selection.')
			pin.contextMenu.add(QLabel_, setText='Shrink Selection', setObjectName='lbl004', setToolTip='Shrink the current selection.')
			return


	def txt001(self):
		'''
		Select By Name
		'''
		searchStr = str(self.selection.txt001.text()) #asterisk denotes startswith*, *endswith, *contains* 
		if searchStr:
			selection = pm.select(pm.ls (searchStr))


	def lbl000(self):
		'''
		Selection Sets: Create New
		'''
		cmb = self.selection.cmb000
		if not cmb.isEditable():
			cmb.addItems_('', ascending=True)
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
		cmb = self.selection.cmb000
		if not cmb.isEditable():
			name = cmb.currentText()
			self._oldSetName = name
			cmb.setEditable(True)
			cmb.lineEdit().setPlaceholderText(name)
		else:
			name = cmb.currentText()
			self.modifySet(self._oldSetName)
			cmb.setItemText(cmb.currentIndex(), name)
			# self.cmb000() #refresh the sets comboBox


	def lbl002(self):
		'''
		Selection Sets: Delete Current
		'''
		cmb = self.selection.cmb000
		name = cmb.currentText()

		pm.delete(name)

		self.cmb000() #refresh the sets comboBox


	def lbl003(self):
		'''
		Grow Selection
		'''
		mel.eval('GrowPolygonSelectionRegion;')


	def lbl004(self):
		'''
		Shrink Selection
		'''
		mel.eval('ShrinkPolygonSelectionRegion;')


	def lbl005(self):
		'''
		Selection Sets: Select Current
		'''
		cmb = self.selection.cmb000
		name = cmb.currentText()

		if cmb.currentIndex()>0:
			pm.select(name) # pm.select(name, noExpand=1) #Select The Selection Set Itself (Not Members Of) (noExpand=select set)


	def s002(self, value=None):
		'''
		Select Island: tolerance x
		'''
		tb = self.currentUi.tb002
		if tb.menu_.chk003.isChecked():
			text = tb.menu_.s002.value()
			tb.menu_.s004.setValue(text)
			tb.menu_.s005.setValue(text)


	def s004(self, value=None):
		'''
		Select Island: tolerance y
		'''
		tb = self.currentUi.tb002
		if tb.menu_.chk003.isChecked():
			text = tb.menu_.s004.value()
			tb.menu_.s002.setValue(text)
			tb.menu_.s005.setValue(text)


	def s005(self, value=None):
		'''
		Select Island: tolerance z
		'''
		tb = self.currentUi.tb002
		if tb.menu_.chk003.isChecked():
			text = tb.menu_.s005.value()
			tb.menu_.s002.setValue(text)
			tb.menu_.s004.setValue(text)


	def chk000(self, state=None):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.toggleWidgets(setUnChecked='chk001-2')


	def chk001(self, state=None):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.toggleWidgets(setUnChecked='chk000,chk002')


	def chk002(self, state=None):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.toggleWidgets(setUnChecked='chk000-1')


	@Slots.message
	def chk004(self, state=None):
		'''
		Ignore Backfacing (Camera Based Selection)
		'''
		if self.selection_submenu.chk004.isChecked():
			pm.selectPref(useDepth=True)
			return 'Camera-based selection <hl>On</hl>.'
		else:
			pm.selectPref(useDepth=False)
			return 'Camera-based selection <hl>Off</hl>.'


	def chk005(self, state=None):
		'''
		Select Style: Marquee
		'''
		self.setSelectionStyle('selectContext')
		self.toggleWidgets(setChecked='chk005', setUnChecked='chk006-7')
		self.selection.cmb004.setCurrentIndex(0)
		self.viewPortMessage('Select Style: <hl>Marquee</hl>')


	def chk006(self, state=None):
		'''
		Select Style: Lasso
		'''
		self.setSelectionStyle('lassoContext')
		self.toggleWidgets(setChecked='chk006', setUnChecked='chk005,chk007')
		self.selection.cmb004.setCurrentIndex(1)
		self.viewPortMessage('Select Style: <hl>Lasso</hl>')


	def chk007(self, state=None):
		'''
		Select Style: Paint
		'''
		self.setSelectionStyle('paintContext')
		self.toggleWidgets(setChecked='chk007', setUnChecked='chk005-6')
		self.selection.cmb004.setCurrentIndex(2)
		self.viewPortMessage('Select Style: <hl>Paint</hl>')


	@Slots.message
	def chk008(self, state=None):
		'''
		Toggle Soft Selection
		'''
		if self.selection_submenu.chk008.isChecked():
			pm.softSelect(edit=1, softSelectEnabled=True)
			return 'Soft Select <hl>On</hl>.'
		else:
			pm.softSelect(edit=1, softSelectEnabled=False)
			return 'Soft Select <hl>Off</hl>.'


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


	def cmb000(self, index=None):
		'''
		Selection Sets
		'''
		cmb = self.selection.cmb000

		if index is 'setMenu':
			cmb.contextMenu.add(QLabel_, setText='Select', setObjectName='lbl005', setToolTip='Select the current set elements.')
			cmb.contextMenu.add(QLabel_, setText='New', setObjectName='lbl000', setToolTip='Create a new selection set.')
			cmb.contextMenu.add(QLabel_, setText='Modify', setObjectName='lbl001', setToolTip='Modify the current set by renaming and/or changing the selection.')
			cmb.contextMenu.add(QLabel_, setText='Delete', setObjectName='lbl002', setToolTip='Delete the current set.')
			cmb.returnPressed.connect(lambda m=cmb.contextMenu.lastActiveChild: getattr(self, m(name=1))()) #connect to the last pressed child widget's corresponding method after return pressed. ie. self.lbl000 if cmb.lbl000 was clicked last.
			cmb.currentIndexChanged.connect(self.lbl005) #select current set on index change.
			cmb.beforePopupShown.connect(self.cmb000) #refresh comboBox contents before showing it's popup.
			return

		list_ = [str(s) for s in pm.ls(et='objectSet', flatten=1)]
		cmb.addItems_(list_, clear=True)


	def cmb001(self, index=None):
		'''
		Editors
		'''
		cmb = self.selection.cmb001
		
		if index is 'setMenu':
			list_ = ['Polygon Selection Constraints']
			cmb.addItems_(list_, 'Selection Editors:')
			return

		if index>0:
			if index==cmb.items.index('Polygon Selection Constraints'):
				mel.eval('PolygonSelectionConstraints;')
			cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Select by Type
		'''
		cmb = self.selection.cmb002	

		if index is 'setMenu':
			list_ = ['IK Handles','Joints','Clusters','Lattices','Sculpt Objects','Wires','Transforms','Geometry','NURBS Curves','NURBS Surfaces','Polygon Geometry','Cameras','Lights','Image Planes','Assets','Fluids','Particles','Rigid Bodies','Rigid Constraints','Brushes','Strokes','Dynamic Constraints','Follicles','nCloths','nParticles','nRigids']
			cmb.addItems_(list_, 'By Type:')
			return

		if index>0:
			if index==cmb.items.index('IK Handles'): #
				type_ = pm.ls(type=['ikHandle', 'hikEffector'])
			if index==cmb.items.index('Joints'): #
				type_ = pm.ls(type='joint')
			if index==cmb.items.index('Clusters'): #
				type_ = pm.listTransforms(type='clusterHandle')
			if index==cmb.items.index('Lattices'): #
				type_ = pm.listTransforms(type='lattice')
			if index==cmb.items.index('Sculpt Objects'): #
				type_ = pm.listTransforms(type=['implicitSphere', 'sculpt'])
			if index==cmb.items.index('Wires'): #
				type_ = pm.ls(type='wire')
			if index==cmb.items.index('Transforms'): #
				type_ = pm.ls(type='transform')
			if index==cmb.items.index('Geometry'): #Select all Geometry
				geometry = pm.ls(geometry=True)
				type_ = pm.listRelatives(geometry, p=True, path=True) #pm.listTransforms(type='nRigid')
			if index==cmb.items.index('NURBS Curves'): #
				type_ = pm.listTransforms(type='nurbsCurve')
			if index==cmb.items.index('NURBS Surfaces'): #
				type_ = pm.ls(type='nurbsSurface')
			if index==cmb.items.index('Polygon Geometry'): #
				type_ = pm.listTransforms(type='mesh')
			if index==cmb.items.index('Cameras'): #
				type_ = pm.listTransforms(cameras=1)
			if index==cmb.items.index('Lights'): #
				type_ = pm.listTransforms(lights=1)
			if index==cmb.items.index('Image Planes'): #
				type_ = pm.ls(type='imagePlane')
			if index==cmb.items.index('Assets'): #
				type_ = pm.ls(type=['container', 'dagContainer'])
			if index==cmb.items.index('Fluids'): #
				type_ = pm.listTransforms(type='fluidShape')
			if index==cmb.items.index('Particles'): #
				type_ = pm.listTransforms(type='particle')
			if index==cmb.items.index('Rigid Bodies'): #
				type_ = pm.listTransforms(type='rigidBody')
			if index==cmb.items.index('Rigid Constraints'): #
				type_ = pm.ls(type='rigidConstraint')
			if index==cmb.items.index('Brushes'): #
				type_ = pm.ls(type='brush')
			if index==cmb.items.index('Strokes'): #
				type_ = pm.listTransforms(type='stroke')
			if index==cmb.items.index('Dynamic Constraints'): #
				type_ = pm.listTransforms(type='dynamicConstraint')
			if index==cmb.items.index('Follicles'): #
				type_ = pm.listTransforms(type='follicle')
			if index==cmb.items.index('nCloths'): #
				type_ = pm.listTransforms(type='nCloth')
			if index==cmb.items.index('nParticles'): #
				type_ = pm.listTransforms(type='nParticle')
			if index==cmb.items.index('nRigids'): #
				type_ = pm.listTransforms(type='nRigid')

			pm.select(type_)
			cmb.setCurrentIndex(0)


	def cmb003(self, index=None):
		'''
		Convert To
		'''
		cmb = self.selection.cmb003

		if index is 'setMenu':
			list_ = ['Verts', 'Vertex Faces', 'Vertex Perimeter', 'Edges', 'Edge Loop', 'Edge Ring', 'Contained Edges', 'Edge Perimeter', 'Border Edges', 'Faces', 'Face Path', 'Contained Faces', 'Face Perimeter', 'UV\'s', 'UV Shell', 'UV Shell Border', 'UV Perimeter', 'UV Edge Loop', 'Shell', 'Shell Border'] 
			cmb.addItems_(list_, 'Convert To:')
			return

		if index>0:
			if index==cmb.items.index('Verts'): #Convert Selection To Vertices
				mel.eval('PolySelectConvert 3;')
			if index==cmb.items.index('Vertex Faces'): #
				mel.eval('PolySelectConvert 5;')
			if index==cmb.items.index('Vertex Perimeter'): #
				mel.eval('ConvertSelectionToVertexPerimeter;')
			if index==cmb.items.index('Edges'): #Convert Selection To Edges
				mel.eval('PolySelectConvert 2;')
			if index==cmb.items.index('Edge Loop'): #
				mel.eval('polySelectSp -loop;')
			if index==cmb.items.index('Edge Ring'): #Convert Selection To Edge Ring
				mel.eval('SelectEdgeRingSp;')
			if index==cmb.items.index('Contained Edges'): #
				mel.eval('PolySelectConvert 20;')
			if index==cmb.items.index('Edge Perimeter'): #
				mel.eval('ConvertSelectionToEdgePerimeter;')
			if index==cmb.items.index('Border Edges'): #
				pm.select(self.getBorderEdgeFromFace())
			if index==cmb.items.index('Faces'): #Convert Selection To Faces
				mel.eval('PolySelectConvert 1;')
			if index==cmb.items.index('Face Path'): #
				mel.eval('polySelectEdges edgeRing;')
			if index==cmb.items.index('Contained Faces'): #
				mel.eval('PolySelectConvert 10;')
			if index==cmb.items.index('Face Perimeter'): #
				mel.eval('polySelectFacePerimeter;')
			if index==cmb.items.index('UV\'s'): #
				mel.eval('PolySelectConvert 4;')
			if index==cmb.items.index('UV Shell'): #
				mel.eval('polySelectBorderShell 0;')
			if index==cmb.items.index('UV Shell Border'): #
				mel.eval('polySelectBorderShell 1;')
			if index==cmb.items.index('UV Perimeter'): #
				mel.eval('ConvertSelectionToUVPerimeter;')
			if index==cmb.items.index('UV Edge Loop'): #
				mel.eval('polySelectEdges edgeUVLoopOrBorder;')
			if index==cmb.items.index('Shell'): #
				mel.eval('polyConvertToShell;')
			if index==cmb.items.index('Shell Border'): #
				mel.eval('polyConvertToShellBorder;')
			cmb.setCurrentIndex(0)


	def cmb004(self, index=None):
		'''
		Select Style: Set Context
		'''
		cmb = self.selection.cmb004

		if index is 'setMenu':
			list_ = ['Marquee', 'Lasso', 'Paint'] 
			cmb.addItems_(list_, 'Select Tool Style:')
			return

		if index>0:
			if index==cmb.items.index('Marquee'): #
				self.chk005()
			if index==cmb.items.index('Lasso'): #
				self.chk006()
			if index==cmb.items.index('Paint'): #
				self.chk007()
			cmb.setCurrentIndex(0)


	def cmb005(self, index=None):
		'''
		Selection Contraints
		'''
		cmb = self.selection.cmb005

		if index is 'setMenu':
			list_ = ['Angle', 'Border', 'Edge Loop', 'Edge Ring', 'Shell', 'UV Edge Loop']
			items = cmb.addItems_(list_, 'Off')
			return

		if index>0:
			if index==cmb.items.index('Angle'):
				mel.eval('dR_selConstraintAngle;') #dR_DoCmd("selConstraintAngle");
			elif index==cmb.items.index('Border'):
				mel.eval('dR_selConstraintBorder;') #dR_DoCmd("selConstraintBorder");
			elif index==cmb.items.index('Edge Loop'):
				mel.eval('dR_selConstraintEdgeLoop;') #dR_DoCmd("selConstraintEdgeLoop");
			elif index==cmb.items.index('Edge Ring'):
				mel.eval('dR_selConstraintEdgeRing;') #dR_DoCmd("selConstraintEdgeRing");
			elif index==cmb.items.index('Shell'):
				mel.eval('dR_selConstraintElement;') #dR_DoCmd("selConstraintElement");
			elif index==cmb.items.index('UV Edge Loop'):
				mel.eval('dR_selConstraintUVEdgeLoop;') #dR_DoCmd("selConstraintUVEdgeLoop");
		else:
			mel.eval('dR_selConstraintOff;') #dR_DoCmd("selConstraintOff");


	def cmb006(self, index=None):
		'''
		Selected Objects
		'''
		cmb = self.selection.cmb006

		if index is 'setMenu':
			cmb.popupStyle = 'qmenu'
			cmb.beforePopupShown.connect(self.cmb006) #refresh comboBox contents before showing it's popup.
			return

		cmb.clear()
		list_ = [str(i) for i in pm.ls(sl=1, flatten=1)]
		widgets = [cmb.menu_.add('QCheckBox', setText=t, setChecked=1) for t in list_[:50]] #selection list is capped with a slice at 50 elements.

		for w in widgets:
			try:
				w.disconnect() #disconnect all previous connections.
			except TypeError:
				pass #if no connections are present; pass
			w.toggled.connect(lambda state, widget=w: self.chkxxx(state=state, widget=widget))


	def chkxxx(self, **kwargs):
		'''
		Transform Constraints: Constraint CheckBoxes
		'''
		try:
			pm.select(kwargs['widget'].text(), deselect=(not kwargs['state']))
		except KeyError:
			pass


	@Slots.message
	def tb000(self, state=None):
		'''
		Select Nth
		'''
		tb = self.currentUi.tb000
		if state is 'setMenu':
			tb.menu_.add('QRadioButton', setText='Component Ring', setObjectName='chk000', setToolTip='Select component ring.')
			tb.menu_.add('QRadioButton', setText='Component Loop', setObjectName='chk001', setChecked=True, setToolTip='Select all contiguous components that form a loop with the current selection.')
			tb.menu_.add('QRadioButton', setText='Shortest Path', setObjectName='chk002', setToolTip='Shortest component path between two selected vertices or UV\'s.')
			tb.menu_.add('QSpinBox', setPrefix='Step: ', setObjectName='s003', setMinMax_='1-100 step1', setValue=1, setToolTip='Step Amount.')
			return

		step = tb.menu_.s003.value()

		selectionMask = pm.selectMode (query=True, component=True)
		maskVertex = pm.selectType (query=True, vertex=True)
		maskEdge = pm.selectType (query=True, edge=True)
		maskFacet = pm.selectType (query=True, facet=True)

		objects = pm.ls(sl=1)
		for obj in objects:
			if pm.objectType(obj, isType='mesh'): 
				if tb.menu_.chk000.isChecked(): #Select Ring
					if all([selectionMask==1, maskEdge==1]):
						pm.polySelect(edgeRing=True)

				elif tb.menu_.chk002.isChecked(): #Shortest Edge Path
					if all([selectionMask==1, maskEdge==1]):
						import re
						vertices = [pm.ls(pm.polyListComponentConversion(e, fromEdge=1, toVertex=1), flatten=1) for e in pm.ls(sl=1)]
						closestVerts = self.getClosestVerts(vertices[0], vertices[1])
						vertexNumbers = [int(re.findall(r'(?<=\[)[0-9]+(?=:?])', str(s))[0]) for s in closestVerts] #get the vertex numbers as integer values. ie. [818, 1380]
						pm.polySelect(shortestEdgePath=(vertexNumbers[0], vertexNumbers[1]))

				elif tb.menu_.chk001.isChecked(): #Select Loop
					if all([selectionMask==1, maskEdge==1]):
						pm.polySelect(edgeLoop=True)


	def tb001(self, state=None):
		'''
		Select Similar
		'''
		tb = self.currentUi.tb001
		if state is 'setMenu':
			tb.menu_.add('QDoubleSpinBox', setPrefix='Tolerance: ', setObjectName='s000', setMinMax_='0.0-10 step.1', setValue=0.3, setToolTip='Select similar objects or components, depending on selection mode.')
			return

		tolerance = str(tb.menu_.s000.value()) #string value because mel.eval is sending a command string

		mel.eval("doSelectSimilar 1 {\""+ tolerance +"\"}")


	@Slots.message
	def tb002(self, state=None):
		'''
		Select Island: Select Polygon Face Island
		'''
		tb = self.currentUi.tb002
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Lock Values', setObjectName='chk003', setChecked=True, setToolTip='Keep values in sync.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='x: ', setObjectName='s002', setMinMax_='0.00-1 step.01', setValue=0.01, setToolTip='Normal X range.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='y: ', setObjectName='s004', setMinMax_='0.00-1 step.01', setValue=0.01, setToolTip='Normal Y range.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='z: ', setObjectName='s005', setMinMax_='0.00-1 step.01', setValue=0.01, setToolTip='Normal Z range.')
			return

		rangeX = float(tb.menu_.s002.value())
		rangeY = float(tb.menu_.s004.value())
		rangeZ = float(tb.menu_.s005.value())
		selectedFaces = pm.filterExpand(sm=34)

		if selectedFaces:
			pm.undoInfo(openChunk=1)
			similarFaces = self.getFacesWithSimilarNormals(selectedFaces, rangeX=rangeX, rangeY=rangeY, rangeZ=rangeZ)
			islands = self.getContigiousIslands(similarFaces)

			for island in islands: #select the islands that contain faces from the original selection.
				for face in selectedFaces:
					if face in island:
						pm.select(island, add=1)
						break
			pm.undoInfo(closeChunk=1)
		else:
			return 'Warning: No faces selected.'


	def b016(self):
		'''
		Convert Selection To Vertices
		'''
		mel.eval('PolySelectConvert 3;')


	def b017(self):
		'''
		Convert Selection To Edges
		'''
		mel.eval('PolySelectConvert 2;')


	def b018(self):
		'''
		Convert Selection To Faces
		'''
		mel.eval('PolySelectConvert 1;')


	def b019(self):
		'''
		Convert Selection To Edge Ring
		'''
		mel.eval('SelectEdgeRingSp;')


	def generateUniqueSetName(self):
		'''
		Generate a generic name based on the object's name.

		<objectName>_Set<int>
		'''
		num = self.cycle(list(range(99)), 'selectionSetNum')
		name = '{0}_Set{1}'.format(rt.selection[0].name, num) #ie. pCube1_Set0
		return name


	@Slots.message
	def creatNewSelectionSet(self, name=None):
		'''
		Selection Sets: Create a new selection set.
		'''
		if pm.objExists (name):
			return 'Error: Set with name <hl>{}</hl> already exists.'.format(name)

		else: #create set
			if not name: #name=='set#Set': #generate a generic name based on obj.name
				name = self.generateUniqueSetName()

			pm.sets(name=name, text="gCharacterSet")


	@Slots.message
	def modifySet(self, name):
		'''
		Selection Sets: Modify Current by renaming or changing the set members.
		'''
		newName = self.selection.cmb000.currentText()
		if not newName:
			newName = self.generateUniqueSetName()
		name = pm.rename(name, newName)

		if pm.objExists(name):
			pm.sets(name, clear=1)
			pm.sets(name, add=1) #if set exists; clear set and add current selection









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------