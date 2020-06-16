from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Mirror(Init):
	def __init__(self, *args, **kwargs):
		super(Mirror, self).__init__(*args, **kwargs)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='')

			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000
		
		list_ = ['']
		items = cmb.addItems_(list_, '')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def chk000_3(self):
		'''
		Set the tb000's text according to the checkstates.
		'''
		axis = self.getAxisFromCheckBoxes('chk000-3')
		self.parentUi.tb000.setText('Mirror '+axis)


	@Slots.message
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
			tb.add('QDoubleSpinBox', setPrefix='Merge Threshold: ', setObjectName='s000', minMax_='0.000-10 step.001', setValue=0.005, setToolTip='Merge vertex distance.')

			self.connect_('chk000-3', 'toggled', self.chk000_3, tb)
			return

		axis = self.getAxisFromCheckBoxes('chk000-3')
		cutMesh = tb.chk005.isChecked() #cut
		instance = tb.chk004.isChecked()
		mergeThreshold = tb.s000.value()

		if axis=='X': #'x'
			axisDirection = 0 #positive axis
			a = 0
			x=-1; y=1; z=1

		elif axis=='-X': #'-x'
			axisDirection = 1 #negative axis
			a = 1 #0=-x, 1=x, 2=-y, 3=y, 4=-z, 5=z 
			x=-1; y=1; z=1 #if instance: used to negatively scale

		elif axis=='Y': #'y'
			axisDirection = 0
			a = 2
			x=1; y=-1; z=1

		elif axis=='-Y': #'-y'
			axisDirection = 1
			a = 3
			x=1; y=-1; z=1

		elif axis=='Z': #'z'
			axisDirection = 0
			a = 4
			x=1; y=1; z=-1

		elif axis=='-Z': #'-z'
			axisDirection = 1
			a = 5
			x=1; y=1; z=-1

		selection = pm.ls(sl=1, objectsOnly=1)
		if not selection:
			return 'Warning: Nothing Selected.'

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









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------


#deprecated:

	# def chk000(self):
	# 	'''
	# 	Delete: Negative Axis. Set Text Mirror Axis
	# 	'''
	# 	axis = "X"
	# 	if self.parentUi.chk002.isChecked():
	# 		axis = "Y"
	# 	if self.parentUi.chk003.isChecked():
	# 		axis = "Z"
	# 	if self.parentUi.chk000.isChecked():
	# 		axis = '-'+axis
	# 	self.parentUi.b000.setText('Mirror '+axis)
	# 	self.parentUi.b008.setText('Delete '+axis)


	# #set check states
	# def chk001(self):
	# 	'''
	# 	Delete: X Axis
	# 	'''
	# 	self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk002,chk003')
	# 	axis = "X"
	# 	if self.parentUi.chk000.isChecked():
	# 		axis = '-'+axis
	# 	self.parentUi.b000.setText('Mirror '+axis)
	# 	self.parentUi.b008.setText('Delete '+axis)


	# def chk002(self):
	# 	'''
	# 	Delete: Y Axis
	# 	'''
	# 	self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk001,chk003')
	# 	axis = "Y"
	# 	if self.parentUi.chk000.isChecked():
	# 		axis = '-'+axis
	# 	self.parentUi.b000.setText('Mirror '+axis)
	# 	self.parentUi.b008.setText('Delete '+axis)


	# def chk003(self):
	# 	'''
	# 	Delete: Z Axis
	# 	'''
	# 	self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk001,chk002')
	# 	axis = "Z"
	# 	if self.parentUi.chk000.isChecked():
	# 		axis = '-'+axis
	# 	self.parentUi.b000.setText('Mirror '+axis)
	# 	self.parentUi.b008.setText('Delete '+axis)