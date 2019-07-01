import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Selection(Init):
	def __init__(self, *args, **kwargs):
		super(Selection, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('selection')

		#set checked button states
		#chk004 ignore backfacing (camera based selection)
		state = pm.selectPref(query=True, useDepth=True)
		self.ui.chk004.setChecked(state)

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
		Select Nth: uncheck other checkboxes
		'''
		self.setButtons(self.ui, unchecked='chk001-2')


	def chk001(self):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.setButtons(self.ui, unchecked='chk000,chk002')


	def chk002(self):
		'''
		Select Nth: uncheck other checkboxes
		'''
		self.setButtons(self.ui, unchecked='chk000-1')


	def chk004(self):
		'''
		Ignore Backfacing (Camera Based Selection)
		'''
		if self.ui.chk004.isChecked():
			pm.selectPref(useDepth=True)
			self.viewPortMessage("Camera-based selection <hl>On</hl>.")
		else:
			pm.selectPref(useDepth=False)
			self.viewPortMessage("Camera-based selection <hl>Off</hl>.")


	def cmb000(self):
		'''
		List Selection Sets
		'''
		cmb = self.ui.cmb000

		contents = self.comboBox (cmb, [str(set_) for set_ in pm.ls (et="objectSet", flatten=1)], "Sets")

		index = cmb.currentIndex()
		if index!=0:
			pm.select (contents[index])
			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb001
		
		files = ['']
		contents = self.comboBox(cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				mel.eval('')
			cmb.setCurrentIndex(0)


	def cmb002(self):
		'''
		Select All Of Type
		'''
		cmb = self.ui.cmb002	

		list_ = []
		contents = self.comboBox (cmb, list_, "")

		index = cmb.currentIndex()
		if index!=0:
			cmb.setCurrentIndex(0)
		
		#Select all Geometry
		geometry = pm.ls(geometry=True)
		transforms = pm.listRelatives(geometry, p=True, path=True)
		pm.select(transforms)


	def cmb003(self):
		'''
		Convert Selection to
		'''
		cmb = self.ui.cmb003

		list_ = ['Verts', 'Edge', 'Face', 'Ring']
		contents = self.comboBox (cmb, list_, 'Convert Selection to')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Verts'): #Convert Selection To Vertices
				mel.eval('PolySelectConvert 3;')
			if index==contents.index('Edges'): #Convert Selection To Edges
				mel.eval('PolySelectConvert 2;')
			if index==contents.index('Faces'): #Convert Selection To Faces
				mel.eval('PolySelectConvert 1;')
			if index==contents.index('Ring'): #Convert Selection To Edge Ring
				mel.eval('SelectEdgeRingSp;')
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Create Selection Set
		'''
		name = str(self.ui.t000.text())+"Set"
		if pm.objExists (name):
			pm.sets (name, clear=1)
			pm.sets (name, add=1) #if set exists; clear set and add current selection 
		else: #create set
			pm.sets (name=name, text="gCharacterSet")
			self.ui.t000.clear()


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

		mel.eval("tk_selectPolyFaceIsland("+str(rangeX)+","+str(rangeY)+","+str(rangeZ)+")")


	def b008(self):
		'''
		Select Nth
		'''
		step = self.ui.s003.value()


		if self.ui.chk000.isChecked(): #Select Ring
			print "# Warning: add correct arguments for this tool #" 
			self.shortestEdgePath()

		if self.ui.chk001.isChecked(): #Select contigious
			# mel.eval('SelectContiguousEdges;')
			mel.eval('SelectContiguousEdgesOptions;') #Select contigious edge loop options
		
		if self.ui.chk002.isChecked(): #Shortest Edge Path
			self.shortestEdgePath()
			# maxEval('SelectShortestEdgePathTool;')

		else: #Select Loop
			mel.eval("selectEveryNEdge;")
		

	def b009(self):
		'''
		
		'''
		pass


	def b10(self):
		'''
		
		'''
		pass


	def b011(self):
		'''
		
		'''
		pass


	def b012(self):
		'''
		Selection Constraints
		'''
		mel.eval('PolygonSelectionConstraints;')


	def b013(self):
		'''
		Lasso Select
		'''
		mel.eval("LassoTool;")


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


	def b020(self):
		'''

		'''
		pass






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------