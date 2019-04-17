import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Symmetry(Init):
	def __init__(self, *args, **kwargs):
		super(Symmetry, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('symmetry')

		#symmetry: set initial checked state
		state = pm.symmetricModelling(query=True, symmetry=True) #application symmetry state
		axis = pm.symmetricModelling(query=True, axis=True)
		if axis == "x":
			self.ui.chk000.setChecked(state)
		if axis == "y":
			self.ui.chk001.setChecked(state)
		if axis == "z":
			self.ui.chk002.setChecked(state)

	def setSymmetry(self, state, axis):
		if self.ui.chk005.isChecked():
			space = "object"
		if self.ui.chk006.isChecked():
			space = "topo"
		else:
			space = "world"

		tolerance = float(self.ui.s005.value())
		pm.symmetricModelling(edit=True, symmetry=state, axis=axis, about=space, tolerance=tolerance)



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
		if self.ui.chk002.isChecked():
			axis = "X"
			if self.ui.chk001.isChecked():
				axis = "-X"
		if self.ui.chk003.isChecked():
			axis = "Y"
			if self.ui.chk001.isChecked():
				axis = "-Y"
		if self.ui.chk004.isChecked():
			axis = "Z"
			if self.ui.chk001.isChecked():
				axis = "-Z"
		self.ui.b000.setText("Mirror "+axis)

	#set check states
	def chk008(self):
		'''
		Delete: X Axis

		'''
		self.setButtons(self.ui, unchecked='chk003,chk004')
		axis = "X"
		if self.ui.chk001.isChecked():
			axis = "-X"
		self.ui.b000.setText("Mirror "+axis)

	def chk009(self):
		'''
		Delete: Y Axis

		'''
		self.setButtons(self.ui, unchecked='chk002,chk004')
		axis = "Y"
		if self.ui.chk001.isChecked():
			axis = "-Y"
		self.ui.b000.setText("Mirror "+axis)

	def chk010(self):
		'''
		Delete: Z Axis

		'''
		self.setButtons(self.ui, unchecked='chk003,chk002')
		axis = "Z"
		if self.ui.chk001.isChecked():
			axis = "-Z"
		self.ui.b000.setText("Mirror "+axis)

	def b000(self):
		'''
		Mirror Geometry

		'''
		mergeThreshold=0.005
		axis = 0 #0=x 1=y, 2=z
		y=z= 1; x=-1 #used to negaively scale instanced object
		cutMesh = self.ui.chk005.isChecked() #cut
		axisStr = self.ui.b000.text()
		instance = self.ui.chk021.isChecked()
		if axisStr == "Mirror Y" or axisStr == "Mirror -Y":
			axis=1; y=-1; x=1
		if axisStr == "Mirror Z" or axisStr == "Mirror -Z":
			axis=2; z=-1; x=1
		if not instance:
			pm.polyMirrorFace (cutMesh=cutMesh, axis=axis, axisDirection=1, mergeMode=1, mergeThresholdType=1, mergeThreshold=mergeThreshold, mirrorAxis=1, mirrorPosition=0, smoothingAngle=30, flipUVs=0, ch=0)
		else:
			pm.undoInfo(openChunk=1)
			if cutMesh:
				self.b032()
			instance = pm.instance() # bt_convertToMirrorInstanceMesh(0); #x=0, y=1, z=2, -x=3, -y=4, -z=5
			pm.scale (z,x,y, pivot=(0,0,0), relative=1) #zxy
			pm.undoInfo(closeChunk=1)
	
	def b001(self):
		'''
		

		'''
		pass

	def b002(self):
		'''
		Mirror Options

		'''
		mel.eval('MirrorPolygonGeometryOptions;')

	def b003(self):
		'''
		

		'''
		mel.eval('')

	def b004(self):
		'''
		

		'''
		mel.eval('')

	def b005(self):
		'''
		

		'''
		mel.eval('')

	def b006(self):
		'''
		Maya Bonus Tools: Symmetrize

		'''
		maxEval('dR_symmetrize;')

	def b007(self):
		'''
		Mirror Instance Mesh

		'''
		mel.eval('bt_mirrorInstanceMesh;')

	def b008(self):
		'''
		Delete Component Or If Object Selected, Along Axis   
		'''
		selectionMask = pm.selectMode (query=True, component=True)
		maskVertex = pm.selectType (query=True, vertex=True)
		maskEdge = pm.selectType (query=True, edge=True)
		# maskFacet = pm.selectType (query=True, facet=True)

		if all([selectionMask==1, maskEdge==1]): #delete edges
			pm.polyDelEdge (cleanVertices=True)
			self.viewPortMessage("delete <hl>edge(s)</hl>.")

		if all([selectionMask==1, maskVertex==1]): #delete vertices
			pm.polyDelVertex()
			self.viewPortMessage("delete <hl>vertice(s)</hl>.")

		if selectionMask==0: #object mode /delete faces along axis
			if self.ui.chk002.isChecked():
				axis = "x"
				if self.ui.chk001.isChecked():
					axis = "-x"
			if self.ui.chk003.isChecked():
				axis = "y"
				if self.ui.chk001.isChecked():
					axis = "-y"
			if self.ui.chk004.isChecked():
				axis = "z"
				if self.ui.chk001.isChecked():
					axis = "-z"

			faces = self.getAllFacesOnAxis (axis)
			pm.delete(faces)
			self.viewPortMessage("delete faces on <hl>"+axis+"</hl>.")
			return axis

		else:
			pm.delete()
			self.viewPortMessage("delete.")

	def b009(self):
		'''
		

		'''
		mel.eval('')


#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------