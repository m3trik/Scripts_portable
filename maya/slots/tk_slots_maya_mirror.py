from __future__ import print_function
from tk_slots_maya_init import *

import traceback





class Mirror(Init):
	def __init__(self, *args, **kwargs):
		super(Mirror, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('mirror')
		self.submenu = self.sb.getUi('mirror_submenu')



	def chk000(self):
		'''
		Delete: Negative Axis. Set Text Mirror Axis
		'''
		axis = "X"
		if self.ui.chk002.isChecked():
			axis = "Y"
		if self.ui.chk003.isChecked():
			axis = "Z"
		if self.ui.chk000.isChecked():
			axis = '-'+axis
		self.ui.b000.setText('Mirror '+axis)
		self.ui.b008.setText('Delete '+axis)


	#set check states
	def chk001(self):
		'''
		Delete: X Axis
		'''
		self.toggleWidgets(self.ui, self.submenu, setChecked_False='chk002,chk003')
		axis = "X"
		if self.ui.chk000.isChecked():
			axis = '-'+axis
		self.ui.b000.setText('Mirror '+axis)
		self.ui.b008.setText('Delete '+axis)


	def chk002(self):
		'''
		Delete: Y Axis
		'''
		self.toggleWidgets(self.ui, self.submenu, setChecked_False='chk001,chk003')
		axis = "Y"
		if self.ui.chk000.isChecked():
			axis = '-'+axis
		self.ui.b000.setText('Mirror '+axis)
		self.ui.b008.setText('Delete '+axis)


	def chk003(self):
		'''
		Delete: Z Axis
		'''
		self.toggleWidgets(self.ui, self.submenu, setChecked_False='chk001,chk002')
		axis = "Z"
		if self.ui.chk000.isChecked():
			axis = '-'+axis
		self.ui.b000.setText('Mirror '+axis)
		self.ui.b008.setText('Delete '+axis)


	def chk005(self):
		'''
		Mirror: Cut
		'''
		#keep menu and submenu in sync:
		# if self.submenu.chk005.isChecked():
		# 	self.toggleWidgets(self.ui, self.submenu, setChecked='chk005')
		# else:
		# 	self.toggleWidgets(self.ui, self.submenu, setChecked_False='chk005')


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['Mirror Options', 'Mirror Instance Mesh']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Mirror Options'):
				mel.eval('MirrorPolygonGeometryOptions;')
			if index==contents.index('Mirror Instance Mesh'):
				mel.eval('bt_mirrorInstanceMesh;')
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Mirror Geometry
		'''
		mergeThreshold=0.005
		
		cutMesh = self.ui.chk005.isChecked() #cut
		instance = self.ui.chk004.isChecked()

		negAxis = self.ui.chk000.isChecked() #mirror on negative axis

		if self.ui.chk001.isChecked(): #'x'
			axisDirection = 0 #positive axis
			axis = 0
			x=-1; y=1; z=1
			if negAxis: #'-x'
				axisDirection = 1 #negative axis
				axis = 1 #0=-x, 1=x, 2=-y, 3=y, 4=-z, 5=z 
				x=-1; y=1; z=1 #if instance: used to negatively scale

		if self.ui.chk002.isChecked(): #'y'
			axisDirection = 0
			axis = 2
			x=1; y=-1; z=1
			if negAxis: #'-y'
				axisDirection = 1
				axis = 3
				x=1; y=-1; z=1

		if self.ui.chk003.isChecked(): #'z'
			axisDirection = 0
			axis = 4
			x=1; y=1; z=-1
			if negAxis: #'-z'
				axisDirection = 1
				axis = 5
				x=1; y=1; z=-1

		selection = pm.ls(sl=1, objectsOnly=1)
		if selection:
			pm.undoInfo(openChunk=1)
			if cutMesh:
				self.b008() #delete mesh faces that fall inside the specified axis
			for obj in [n for n in pm.listRelatives(selection, allDescendents=1) if pm.objectType(n, isType='mesh')]: #get any mesh type child nodes of obj.
				if instance: #create instance and scale negatively
					inst = pm.instance(obj) # bt_convertToMirrorInstanceMesh(0); #x=0, y=1, z=2, -x=3, -y=4, -z=5
					pm.xform(inst, scale=[x,y,z]) #pm.scale(z,x,y, pivot=(0,0,0), relative=1) #swap the xyz values to transform the instanced node
				else: #mirror
					pm.polyMirrorFace(obj, mirrorAxis=axisDirection, direction=axis, mergeMode=1, mergeThresholdType=1, mergeThreshold=mergeThreshold, worldSpace=0, smoothingAngle=30, flipUVs=0, ch=0) #mirrorPosition x, y, z - This flag specifies the position of the custom mirror axis plane
			pm.undoInfo(closeChunk=1)
		else:
			print '# Warning: Nothing Selected.'


	def b001(self):
		'''
		
		'''
		pass


	def b002(self):
		'''
		Mirror Options

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
		
		'''
		pass


	def b007(self):
		'''
		

		'''
		pass


	def b008(self):
		'''
		Delete Along Axis
		'''
		selection = pm.ls(sl=1, objectsOnly=1)

		if self.ui.chk001.isChecked():
			axis = 'x'
		elif self.ui.chk002.isChecked():
			axis = 'y'
		elif self.ui.chk003.isChecked():
			axis = 'z'
		if self.ui.chk000.isChecked():
			axis = '-'+axis

		pm.undoInfo(openChunk=1)
		for obj in selection:
			for node in [n for n in pm.listRelatives(obj, allDescendents=1) if pm.objectType(n, isType='mesh')]: #get any mesh type child nodes of obj.
				faces = self.getAllFacesOnAxis(node, axis)
				if len(faces)==pm.polyEvaluate(node, face=1): #if all faces fall on the specified axis.
					pm.delete(node) #delete entire node
				else:
					pm.delete(faces) #else, delete any individual faces.
		pm.undoInfo(closeChunk=1)

		self.viewPortMessage("Delete faces on <hl>"+axis.upper()+"</hl>.")







#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------