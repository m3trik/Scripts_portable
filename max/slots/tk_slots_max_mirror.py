from tk_slots_max_init import *


import os.path



class Mirror(Init):
	def __init__(self, *args, **kwargs):
		super(Mirror, self).__init__(*args, **kwargs)

		self.ui = self.parentUi #self.ui = self.sb.getUi(self.__class__.__name__)


	def chkxxx(self):
		'''
		Set the toolbutton's text according to the checkstates.
		'''
		axis = self.getAxisFromCheckBoxes('chk000-3')
		self.ui.tb000.setText('Mirror '+axis)

		axis = self.getAxisFromCheckBoxes('chk006-9')
		self.ui.tb001.setText('Delete '+axis)


	# def cmb000(self, index=None):
	# 	'''
	# 	Editors
	# 	'''
	# 	cmb = self.ui.cmb000

	# 	files = ['']
	# 	contents = cmb.addItems_(files, ' ')

	# 	if not index:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		if index==contents.index(''):
	# 			mel.eval('')
	# 		cmb.setCurrentIndex(0)


	def tb000(self, state=None):
		'''
		Mirror Geometry
		'''
		tb = self.currentUi.tb000
		if state=='setMenu':
			tb.add('QCheckBox', setText='-', setObjectName='chk000', setChecked=True, setToolTip='Perform mirror along negative axis.')
			tb.add('QRadioButton', setText='X', setObjectName='chk001', setChecked=True, setToolTip='Perform mirror along X axis.')
			tb.add('QRadioButton', setText='Y', setObjectName='chk002', setToolTip='Perform mirror along Y axis.')
			tb.add('QRadioButton', setText='Z', setObjectName='chk003', setToolTip='Perform mirror along Z axis.')
			tb.add('QCheckBox', setText='Instance', setObjectName='chk004', setToolTip='Instance object.')
			tb.add('QCheckBox', setText='Cut', setObjectName='chk005', setChecked=True, setToolTip='Perform a delete along specified axis before mirror.')
			tb.add('QDoubleSpinBox', setPrefix='Merge Threshold: ', setObjectName='s000', preset_='0.000-10 step.001', setValue=0.005, setToolTip='Merge vertex distance.')

			self.connect('chk000-3', 'toggled', self.chkxxx, tb)
			return

		axis = self.getAxisFromCheckBoxes('chk000-3')
		cutMesh = tb.chk005.isChecked() #cut
		instance = tb.chk004.isChecked()
		mergeThreshold = tb.s000.value()

		# negAxis = tb.chk000.isChecked() #mirror on negative axis

		if axis=='X': #'x'
			axisDirection = 0 #positive axis
			a = 0
			x=-1; y=1; z=1
			if axis=='-X': #'-x'
				axisDirection = 1 #negative axis
				a = 1 #0=-x, 1=x, 2=-y, 3=y, 4=-z, 5=z 
				x=-1; y=1; z=1 #if instance: used to negatively scale

		if axis=='Y': #'y'
			axisDirection = 0
			a = 2
			x=1; y=-1; z=1
			if axis=='-Y': #'-y'
				axisDirection = 1
				a = 3
				x=1; y=-1; z=1

		if axis=='Z': #'z'
			axisDirection = 0
			a = 4
			x=1; y=1; z=-1
			if axis=='-Z': #'-z'
				axisDirection = 1
				a = 5
				x=1; y=1; z=-1

		selection = pm.ls(sl=1, objectsOnly=1)
		if selection:
			pm.undoInfo(openChunk=1)
			for obj in [n for n in pm.listRelatives(selection, allDescendents=1) if pm.objectType(n, isType='mesh')]: #get any mesh type child nodes of obj.
				if cutMesh:
					self.deleteAlongAxis(obj, axis) #delete mesh faces that fall inside the specified axis.
				if instance: #create instance and scale negatively
					inst = pm.instance(obj) # bt_convertToMirrorInstanceMesh(0); #x=0, y=1, z=2, -x=3, -y=4, -z=5
					pm.xform(inst, scale=[x,y,z]) #pm.scale(z,x,y, pivot=(0,0,0), relative=1) #swap the xyz values to transform the instanced node
				else: #mirror
					pm.polyMirrorFace(obj, mirrorAxis=axisDirection, direction=a, mergeMode=1, mergeThresholdType=1, mergeThreshold=mergeThreshold, worldSpace=0, smoothingAngle=30, flipUVs=0, ch=0) #mirrorPosition x, y, z - This flag specifies the position of the custom mirror axis plane
			pm.undoInfo(closeChunk=1)
		else:
			print('# Warning: Nothing Selected.')


	def tb001(self, state=None):
		'''
		Delete Along Axis
		'''
		tb = self.currentUi.tb001
		if state=='setMenu':
			tb.add('QCheckBox', setText='-', setObjectName='chk006', setChecked=True, setToolTip='Perform delete along negative axis.')
			tb.add('QRadioButton', setText='X', setObjectName='chk007', setChecked=True, setToolTip='Perform delete along X axis.')
			tb.add('QRadioButton', setText='Y', setObjectName='chk008', setToolTip='Perform delete along Y axis.')
			tb.add('QRadioButton', setText='Z', setObjectName='chk009', setToolTip='Perform delete along Z axis.')

			self.connect('chk006-9', 'toggled', self.chkxxx, tb)
			return

		selection = pm.ls(sl=1, objectsOnly=1)
		axis = self.getAxisFromCheckBoxes('chk006-9')

		pm.undoInfo(openChunk=1)
		for obj in selection:
			self.deleteAlongAxis(obj, axis)
		pm.undoInfo(closeChunk=1)


	def deleteAlongAxis(self, obj, axis):
		'''
		Delete components of the given mesh object along the specified axis.

		args:
			obj (obj) = Mesh object.
			axis (str) = Axis to delete on. ie. '-x' Components belonging to the mesh object given in the 'obj' arg, that fall on this axis, will be deleted. 
		'''
		for node in [n for n in pm.listRelatives(obj, allDescendents=1) if pm.objectType(n, isType='mesh')]: #get any mesh type child nodes of obj.
			faces = self.getAllFacesOnAxis(node, axis)
			if len(faces)==pm.polyEvaluate(node, face=1): #if all faces fall on the specified axis.
				pm.delete(node) #delete entire node
			else:
				pm.delete(faces) #else, delete any individual faces.
		

		self.viewPortMessage("Delete faces on <hl>"+axis.upper()+"</hl>.")









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------


#deprecated:

	# def chk000(self):
	# 	'''
	# 	Delete: Negative Axis. Set Text Mirror Axis
	# 	'''
	# 	axis = "X"
	# 	if self.ui.chk002.isChecked():
	# 		axis = "Y"
	# 	if self.ui.chk003.isChecked():
	# 		axis = "Z"
	# 	if self.ui.chk000.isChecked():
	# 		axis = '-'+axis
	# 	self.ui.b000.setText('Mirror '+axis)
	# 	self.ui.b008.setText('Delete '+axis)


	# #set check states
	# def chk001(self):
	# 	'''
	# 	Delete: X Axis
	# 	'''
	# 	self.toggleWidgets(self.ui, self.childUi, setChecked_False='chk002,chk003')
	# 	axis = "X"
	# 	if self.ui.chk000.isChecked():
	# 		axis = '-'+axis
	# 	self.ui.b000.setText('Mirror '+axis)
	# 	self.ui.b008.setText('Delete '+axis)


	# def chk002(self):
	# 	'''
	# 	Delete: Y Axis
	# 	'''
	# 	self.toggleWidgets(self.ui, self.childUi, setChecked_False='chk001,chk003')
	# 	axis = "Y"
	# 	if self.ui.chk000.isChecked():
	# 		axis = '-'+axis
	# 	self.ui.b000.setText('Mirror '+axis)
	# 	self.ui.b008.setText('Delete '+axis)


	# def chk003(self):
	# 	'''
	# 	Delete: Z Axis
	# 	'''
	# 	self.toggleWidgets(self.ui, self.childUi, setChecked_False='chk001,chk002')
	# 	axis = "Z"
	# 	if self.ui.chk000.isChecked():
	# 		axis = '-'+axis
	# 	self.ui.b000.setText('Mirror '+axis)
	# 	self.ui.b008.setText('Delete '+axis)