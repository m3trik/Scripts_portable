from tk_slots_maya_init import Init

import os.path



class Rigging(Init):
	def __init__(self, *args, **kwargs):
		super(Rigging, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('rigging')
		self.submenu = self.sb.getUi('rigging_submenu')

		self.chk000() #init scale joint value



	def chk000(self):
		'''
		Scale Joint
		'''
		self.toggleWidgets(self.ui, setChecked_False='chk001-2')
		self.ui.s000.setValue(pm.jointDisplayScale(query=1)) #init global joint display size


	def chk001(self):
		'''
		Scale IK
		'''
		self.toggleWidgets(self.ui, setChecked_False='chk000, chk002')
		self.ui.s000.setValue(pm.ikHandleDisplayScale(query=1)) #init IK handle display size
		

	def chk002(self):
		'''
		Scale IK/FK
		'''
		self.toggleWidgets(self.ui, setChecked_False='chk000-1')
		self.ui.s000.setValue(pm.jointDisplayScale(query=1, ikfk=1)) #init IKFK display size


	def s000(self):
		'''
		Scale Joint/IK/FK
		'''
		value = self.ui.s000.value()

		if self.ui.chk000.isChecked():
			pm.jointDisplayScale(value) #set global joint display size
		elif self.ui.chk001.isChecked():
			pm.ikHandleDisplayScale(value) #set global IK handle display size
		else: #self.ui.chk002.isChecked():
			pm.jointDisplayScale(value, ikfk=1) #set global IKFK display size


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000

		files = ['Quick Rig','HumanIK','Expression Editor','Shape Editor','Connection Editor','Channel Control Editor','Set Driven Key']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Quick Rig'):
				mel.eval('QuickRigEditor;') #Quick Rig
			if index==contents.index('HumanIK'):
				mel.eval('HIKCharacterControlsTool;') #HumanIK
			if index==contents.index('Expression Editor'):
				mel.eval('ExpressionEditor;') #Expression Editor
			if index==contents.index('Shape Editor'):
				mel.eval('ShapeEditor;') #Shape Editor
			if index==contents.index('Connection Editor'):
				mel.eval('ConnectionEditor;') #Connection Editor
			if index==contents.index('Channel Control Editor'):
				mel.eval('ChannelControlEditor;') #Channel Control Editor
			if index==contents.index('Set Driven Key'):
				mel.eval('SetDrivenKeyOptions;') #Set Driven Key
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Create
		'''
		cmb = self.ui.cmb001

		files = ['Joints','Locator','IK Handle', 'Lattice', 'Cluster']
		contents = cmb.addItems_(files, "Create")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Joints'):
				pm.setToolTo('jointContext') #create joint tool
			if index==contents.index('Locator'):
				pm.spaceLocator(p=[0,0,0]) #locator
			if index==contents.index('IK Handle'):
				pm.setToolTo('ikHandleContext') #create ik handle
			if index==contents.index('Lattice'):
				pm.lattice(divisions=[2,5,2], objectCentered=1, ldv=[2,2,2]) ##create lattice
			if index==contents.index('Cluster'):
				mel.eval('CreateCluster;') #create cluster
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Toggle Display Local Rotation Axes
		'''
		joints = pm.ls(type="joint") #get all scene joints

		state = pm.toggle(joints[0], query=1, localAxis=1)
		if self.ui.b000.isChecked():
			if not state:
				toggle=True
		else:
			if state:
				toggle=True

		if toggle:
			pm.toggle(joints, localAxis=1) #set display off

		self.viewPortMessage("Display Local Rotation Axes:<hl>"+str(state)+"</hl>")


	def b001(self):
		'''
		Connect Joints
		'''
		pm.connectJoint(cm=1)


	def b002(self):
		'''
		Insert Joint Tool
		'''
		pm.setToolTo('insertJointContext') #insert joint tool


	def b003(self):
		'''
		Orient Joints
		'''
		orientJoint = 'xyz' #orient joints
		if self.ui.chk003.isChecked():
			orientJoint = 'none' #orient joint to world

		pm.joint(edit=1, orientJoint=orientJoint, zeroScaleOrient=1, ch=1)


	def b004(self):
		'''
		Reroot
		'''
		pm.reroot() #re-root joints


	def b005(self):
		'''
		Constraint: Parent
		'''
		pm.parentConstraint(mo=1, weight=1)


	def b006(self):
		'''
		Constraint: Point
		'''
		pm.pointConstraint(offset=[0,0,0], weight=1)


	def b007(self):
		'''
		Constraint: Scale
		'''
		pm.scaleConstraint(offset=[1,1,1], weight=1)


	def b008(self):
		'''
		Constraint: Orient
		'''
		pm.orientConstraint(offset=[0,0,0], weight=1)


	def b009(self):
		'''
		Constraint: Aim
		'''
		pm.aimConstraint(offset=[0,0,0], weight=1, aimVector=[1,0,0], upVector=[0,1,0], worldUpType="vector", worldUpVector=[0,1,0])


	def b010(self):
		'''
		Constraint: Pole Vector
		'''
		pm.orientConstraint(offset=[0,0,0], weight=1)






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------