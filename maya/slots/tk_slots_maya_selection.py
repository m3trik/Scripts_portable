from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Selection(Init):
	def __init__(self, *args, **kwargs):
		super(Selection, self).__init__(*args, **kwargs)

		try:
			#set checked button states
			#chk004 ignore backfacing (camera based selection)
			state = pm.selectPref(query=True, useDepth=True)
			self.parentUi.chk004.setChecked(state)

			#selection style: set initial checked state
			ctx = pm.currentCtx() #flags (ctx, c=True) get the context's class.
			if ctx == 'lassoContext':
				self.cmb004(index=1)
				self.childUi.chk006.setChecked(True)
			elif ctx == 'paintContext':
				self.cmb004(index=2)
				self.childUi.chk007.setChecked(True)
			else: #selectContext
				self.cmb004(index=0)
				self.childUi.chk005.setChecked(True)
		except NameError:
			pass


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb001', setToolTip='')

			return


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
			selection = pm.select (pm.ls (searchStr))


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
		if self.parentUi.chk004.isChecked():
			pm.selectPref(useDepth=True)
			self.viewPortMessage("Camera-based selection <hl>On</hl>.")
		else:
			pm.selectPref(useDepth=False)
			self.viewPortMessage("Camera-based selection <hl>Off</hl>.")


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

		contents = cmb.addItems_([str(set_) for set_ in pm.ls (et="objectSet", flatten=1)], "Sets")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			pm.select (contents[index])
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb001
		
		files = ['Selection Constraints']
		contents = cmb.addItems_(files, '')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Selection Constraints'):
				mel.eval('PolygonSelectionConstraints;')
			cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Select by Type
		'''
		cmb = self.parentUi.cmb002	

		list_ = ['IK Handles','Joints','Clusters','Lattices','Sculpt Objects','Wires','Transforms','Geometry','NURBS Curves','NURBS Surfaces','Polygon Geometry','Cameras','Lights','Image Planes','Assets','Fluids','Particles','Rigid Bodies','Rigid Constraints','Brushes','Strokes','Dynamic Constraints','Follicles','nCloths','nParticles','nRigids']
		contents = cmb.addItems_(list_, 'By Type')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('IK Handles'): #
				type_ = pm.ls(type=['ikHandle', 'hikEffector'])
			if index==contents.index('Joints'): #
				type_ = pm.ls(type='joint')
			if index==contents.index('Clusters'): #
				type_ = pm.listTransforms(type='clusterHandle')
			if index==contents.index('Lattices'): #
				type_ = pm.listTransforms(type='lattice')
			if index==contents.index('Sculpt Objects'): #
				type_ = pm.listTransforms(type=['implicitSphere', 'sculpt'])
			if index==contents.index('Wires'): #
				type_ = pm.ls(type='wire')
			if index==contents.index('Transforms'): #
				type_ = pm.ls(type='transform')
			if index==contents.index('Geometry'): #Select all Geometry
				geometry = pm.ls(geometry=True)
				type_ = pm.listRelatives(geometry, p=True, path=True) #pm.listTransforms(type='nRigid')
			if index==contents.index('NURBS Curves'): #
				type_ = pm.listTransforms(type='nurbsCurve')
			if index==contents.index('NURBS Surfaces'): #
				type_ = pm.ls(type='nurbsSurface')
			if index==contents.index('Polygon Geometry'): #
				type_ = pm.listTransforms(type='mesh')
			if index==contents.index('Cameras'): #
				type_ = pm.listTransforms(cameras=1)
			if index==contents.index('Lights'): #
				type_ = pm.listTransforms(lights=1)
			if index==contents.index('Image Planes'): #
				type_ = pm.ls(type='imagePlane')
			if index==contents.index('Assets'): #
				type_ = pm.ls(type=['container', 'dagContainer'])
			if index==contents.index('Fluids'): #
				type_ = pm.listTransforms(type='fluidShape')
			if index==contents.index('Particles'): #
				type_ = pm.listTransforms(type='particle')
			if index==contents.index('Rigid Bodies'): #
				type_ = pm.listTransforms(type='rigidBody')
			if index==contents.index('Rigid Constraints'): #
				type_ = pm.ls(type='rigidConstraint')
			if index==contents.index('Brushes'): #
				type_ = pm.ls(type='brush')
			if index==contents.index('Strokes'): #
				type_ = pm.listTransforms(type='stroke')
			if index==contents.index('Dynamic Constraints'): #
				type_ = pm.listTransforms(type='dynamicConstraint')
			if index==contents.index('Follicles'): #
				type_ = pm.listTransforms(type='follicle')
			if index==contents.index('nCloths'): #
				type_ = pm.listTransforms(type='nCloth')
			if index==contents.index('nParticles'): #
				type_ = pm.listTransforms(type='nParticle')
			if index==contents.index('nRigids'): #
				type_ = pm.listTransforms(type='nRigid')

			pm.select(type_)
			cmb.setCurrentIndex(0)


	def cmb003(self, index=None):
		'''
		Convert To
		'''
		cmb = self.parentUi.cmb003

		list_ = ['Verts', 'Vertex Faces', 'Vertex Perimeter', 'Edges', 'Edge Loop', 'Edge Ring', 'Contained Edges', 'Edge Perimeter', 'Border Edges', 'Faces', 'Face Path', 'Contained Faces', 'Face Perimeter', 'UV\'s', 'UV Shell', 'UV Shell Border', 'UV Perimeter', 'UV Edge Loop', 'Shell', 'Shell Border'] 

		contents = cmb.addItems_(list_, 'Convert To')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Verts'): #Convert Selection To Vertices
				mel.eval('PolySelectConvert 3;')
			if index==contents.index('Vertex Faces'): #
				mel.eval('PolySelectConvert 5;')
			if index==contents.index('Vertex Perimeter'): #
				mel.eval('ConvertSelectionToVertexPerimeter;')
			if index==contents.index('Edges'): #Convert Selection To Edges
				mel.eval('PolySelectConvert 2;')
			if index==contents.index('Edge Loop'): #
				mel.eval('polySelectSp -loop;')
			if index==contents.index('Edge Ring'): #Convert Selection To Edge Ring
				mel.eval('SelectEdgeRingSp;')
			if index==contents.index('Contained Edges'): #
				mel.eval('PolySelectConvert 20;')
			if index==contents.index('Edge Perimeter'): #
				mel.eval('ConvertSelectionToEdgePerimeter;')
			if index==contents.index('Border Edges'): #
				pm.select(self.getBorderEdgeFromFace())
			if index==contents.index('Faces'): #Convert Selection To Faces
				mel.eval('PolySelectConvert 1;')
			if index==contents.index('Face Path'): #
				mel.eval('polySelectEdges edgeRing;')
			if index==contents.index('Contained Faces'): #
				mel.eval('PolySelectConvert 10;')
			if index==contents.index('Face Perimeter'): #
				mel.eval('polySelectFacePerimeter;')
			if index==contents.index('UV\'s'): #
				mel.eval('PolySelectConvert 4;')
			if index==contents.index('UV Shell'): #
				mel.eval('polySelectBorderShell 0;')
			if index==contents.index('UV Shell Border'): #
				mel.eval('polySelectBorderShell 1;')
			if index==contents.index('UV Perimeter'): #
				mel.eval('ConvertSelectionToUVPerimeter;')
			if index==contents.index('UV Edge Loop'): #
				mel.eval('polySelectEdges edgeUVLoopOrBorder;')
			if index==contents.index('Shell'): #
				mel.eval('polyConvertToShell;')
			if index==contents.index('Shell Border'): #
				mel.eval('polyConvertToShellBorder;')
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


	@Slots.message
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
			self.shortestEdgePath()
			return 'Warning: Add correct arguments for this tool.'

		if tb.chk001.isChecked(): #Select contigious
			# mel.eval('SelectContiguousEdges;')
			mel.eval('SelectContiguousEdgesOptions;') #Select contigious edge loop options
		
		if tb.chk002.isChecked(): #Shortest Edge Path
			self.shortestEdgePath()
			# maxEval('SelectShortestEdgePathTool;')

		else: #Select Loop
			mel.eval("selectEveryNEdge;")


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


	def b000(self):
		'''
		Create Selection Set
		'''
		name = str(self.parentUi.t000.text())+"Set"
		if pm.objExists (name):
			pm.sets (name, clear=1)
			pm.sets (name, add=1) #if set exists; clear set and add current selection 
		else: #create set
			pm.sets (name=name, text="gCharacterSet")
			self.parentUi.t000.clear()


	@Slots.message
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


	def b014(self):
		'''
		Grow Selection
		'''
		mel.eval('GrowPolygonSelectionRegion;')


	def b015(self):
		'''
		Shrink Selection
		'''
		mel.eval('ShrinkPolygonSelectionRegion;')


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






#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------