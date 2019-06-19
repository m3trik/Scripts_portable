import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Symmetry(Init):
	def __init__(self, *args, **kwargs):
		super(Symmetry, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('symmetry')

		#symmetry: set initial checked state
		# state = pm.symmetricModelling(query=True, symmetry=True) #application symmetry state
		# axis = pm.symmetricModelling(query=True, axis=True)
		# if axis == "x":
		# 	self.ui.chk000.setChecked(state)
		# if axis == "y":
		# 	self.ui.chk001.setChecked(state)
		# if axis == "z":
		# 	self.ui.chk002.setChecked(state)




	def setSymmetry(self, state, axis):
		# if self.ui.chk005.isChecked():
		# 	space = "object"
		# if self.ui.chk006.isChecked():
		# 	space = "topo"
		# else:
		# 	space = "world"

		negative = self.ui.chk003.isChecked()

		if axis=='x':
			axis=0 #0(x), 1,(y), 2(z)
		if axis=='y':
			axis=1
		if axis=='z':
			axis=2

		for obj in rt.selection:
			#check if modifier exists
			mod = obj.modifiers[rt.Symmetry]
			if mod==None: #if not create
				mod = rt.symmetry()
				rt.addModifier (obj, mod)
		
			#set attributes
			mod.enabled = state
			mod.threshold = 0.01
			mod.axis = axis
			mod.flip = negative

		rt.redrawViews()


	def chk000(self):
		'''
		Symmetry X

		'''
		self.setButtons(self.ui, unchecked='chk001,chk002')
		state = self.ui.chk000.isChecked() #symmetry button state
		self.setSymmetry(state, 'x')


	def chk001(self):
		'''
		Symmetry Y

		'''
		self.setButtons(self.ui, unchecked='chk000,chk002')
		state = self.ui.chk001.isChecked() #symmetry button state
		self.setSymmetry(state, 'y')


	def chk002(self):
		'''
		Symmetry Z

		'''
		self.setButtons(self.ui, unchecked='chk000,chk001')
		state = self.ui.chk002.isChecked() #symmetry button state
		self.setSymmetry(state, 'z')


	def chk003(self):
		'''
		Symmetry Negative Axes

		'''
		state=True
		if self.ui.chk001.isChecked():	
			axis='x'
		elif self.ui.chk001.isChecked():
			axis='y'
		elif self.ui.chk002.isChecked():
			axis='z'
		else:
			axis='x'
			state=False
		
		self.setSymmetry(state, axis)


	def chk004(self):
		'''
		Symmetry: Object

		'''
		self.ui.chk006.setChecked(False) #uncheck symmetry:topological
	

	def chk005(self):
		'''
		Symmetry: Topo

		'''
		self.ui.chk005.setChecked(False) #uncheck symmetry:object space
		if any ([self.ui.chk000.isChecked(), self.ui.chk001.isChecked(), self.ui.chk002.isChecked()]): #(symmetry)
			pm.symmetricModelling(edit=True, symmetry=False)
			self.setButtons(self.ui, unchecked='chk000,chk001,chk002')
			print "# Warning: First select a seam edge and then check the symmetry button to enable topographic symmetry #"


	def chk007(self):
		'''
		Delete: Negative Axis. Set Text Mirror Axis

		'''
		axis = "X"
		if self.ui.chk009.isChecked():
			axis = "Y"
		if self.ui.chk010.isChecked():
			axis = "Z"
		if self.ui.chk007.isChecked():
			axis = '-'+axis
		self.ui.b000.setText('Mirror '+axis)
		self.ui.b008.setText('Delete '+axis)


	#set check states
	def chk008(self):
		'''
		Delete: X Axis

		'''
		self.setButtons(self.ui, unchecked='chk009,chk010')
		axis = "X"
		if self.ui.chk007.isChecked():
			axis = '-'+axis
		self.ui.b000.setText('Mirror '+axis)
		self.ui.b008.setText('Delete '+axis)


	def chk009(self):
		'''
		Delete: Y Axis

		'''
		self.setButtons(self.ui, unchecked='chk008,chk010')
		axis = "Y"
		if self.ui.chk007.isChecked():
			axis = '-'+axis
		self.ui.b000.setText('Mirror '+axis)
		self.ui.b008.setText('Delete '+axis)


	def chk010(self):
		'''
		Delete: Z Axis

		'''
		self.setButtons(self.ui, unchecked='chk008,chk009')
		axis = "Z"
		if self.ui.chk007.isChecked():
			axis = '-'+axis
		self.ui.b000.setText('Mirror '+axis)
		self.ui.b008.setText('Delete '+axis)


	def b000(self):
		'''
		Mirror Geometry

		'''
		mergeThreshold=0.005
		
		cutMesh = self.ui.chk006.isChecked() #cut
		instance = self.ui.chk021.isChecked()

		if self.ui.chk008.isChecked() and self.ui.chk007.isChecked(): #'-x'
			axisDirection = 1 #negative axis
			axis = 1 #0=x 1=y, 2=z
			x=1; y=1; z=1 #used to negaively scale instanced object
		else: #'x'
			axisDirection = 0 #positive axis
			axis = 0
			x=-1; y=1; z=1

		if self.ui.chk009.isChecked() and self.ui.chk007.isChecked(): #'-y'
			axisDirection = 1
			axis = 3
			x=1; y=1; z=1
		else: #'y'
			axisDirection = 0
			axis = 4
			x=1; y=-1; z=1
				
		if self.ui.chk010.isChecked() and self.ui.chk007.isChecked(): #'-z'
			axisDirection = 1
			axis = 5
			x=1; y=1; z=1
		else: #'z'
			axisDirection = 0
			axis = 4
			x=1; y=1; z=-1

		pm.undoInfo(openChunk=1)
		if cutMesh:
			self.b008() #delete mesh faces falling inside the specified axis
		if instance: #create instance and scale negatively
			inst = pm.instance() # bt_convertToMirrorInstanceMesh(0); #x=0, y=1, z=2, -x=3, -y=4, -z=5
			pm.scale(z,x,y, pivot=(0,0,0), relative=1) #zxy is not a typo
		else: #mirror
			pm.polyMirrorFace(mirrorAxis=axisDirection, direction=axis, mergeMode=1, mergeThresholdType=1, mergeThreshold=mergeThreshold, worldSpace=0, smoothingAngle=30, flipUVs=0, ch=0) #mirrorPosition x, y, z - This flag specifies the position of the custom mirror axis plane
		pm.undoInfo(closeChunk=1)


	def b001(self):
		'''
		

		'''
		pass


	def b002(self):
		'''
		Mirror Options

		'''
		maxEval('MirrorPolygonGeometryOptions;')


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
		

		'''
		maxEval('dR_symmetrize;')


	def b007(self):
		'''
		Mirror Instance Mesh

		'''
		mel.eval('bt_mirrorInstanceMesh;')


	def b008(self):
		'''
		Delete Along Axis
		'''
		selectionMask = pm.selectMode(query=True, component=True)
		maskVertex = pm.selectType(query=True, vertex=True)
		maskEdge = pm.selectType(query=True, edge=True)
		# maskFacet = pm.selectType (query=True, facet=True)

		selection = pm.ls(sl=1, objectsOnly=1)

		if self.ui.chk008.isChecked():
			axis = 'x'
		elif self.ui.chk009.isChecked():
			axis = 'y'
		elif self.ui.chk010.isChecked():
			axis = 'z'
		if self.ui.chk007.isChecked():
			axis = '-'+axis

		for obj in selection:
		# if selectionMask==0: #object mode /delete faces along axis
			faces = self.getAllFacesOnAxis(obj, axis)
			pm.delete(faces)
			self.viewPortMessage("delete faces on <hl>"+axis+"</hl>.")
			return axis






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------