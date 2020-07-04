from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Rigging(Init):
	def __init__(self, *args, **kwargs):
		super(Rigging, self).__init__(*args, **kwargs)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya Rigging Editors')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000

		if index=='setMenu':
			list_ = ['Quick Rig','HumanIK','Expression Editor','Shape Editor','Connection Editor','Channel Control Editor','Set Driven Key']
			cmb.addItems_(list_, 'Maya Rigging Editors')
			return

		if index>0:
			if index==cmb.items.index('Quick Rig'):
				mel.eval('QuickRigEditor;') #Quick Rig
			elif index==cmb.items.index('HumanIK'):
				mel.eval('HIKCharacterControlsTool;') #HumanIK
			elif index==cmb.items.index('Expression Editor'):
				mel.eval('ExpressionEditor;') #Expression Editor
			elif index==cmb.items.index('Shape Editor'):
				mel.eval('ShapeEditor;') #Shape Editor
			elif index==cmb.items.index('Connection Editor'):
				mel.eval('ConnectionEditor;') #Connection Editor
			elif index==cmb.items.index('Channel Control Editor'):
				mel.eval('ChannelControlEditor;') #Channel Control Editor
			elif index==cmb.items.index('Set Driven Key'):
				mel.eval('SetDrivenKeyOptions;') #Set Driven Key
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Create
		'''
		cmb = self.parentUi.cmb001

		if index=='setMenu':
			list_ = ['Joints','Locator','IK Handle', 'Lattice', 'Cluster']
			cmb.addItems_(list_, "Create")
			return

		if index>0:
			if index==cmb.items.index('Joints'):
				pm.setToolTo('jointContext') #create joint tool
			elif index==cmb.items.index('Locator'):
				pm.spaceLocator(p=[0,0,0]) #locator
			elif index==cmb.items.index('IK Handle'):
				pm.setToolTo('ikHandleContext') #create ik handle
			elif index==cmb.items.index('Lattice'):
				pm.lattice(divisions=[2,5,2], objectCentered=1, ldv=[2,2,2]) ##create lattice
			elif index==cmb.items.index('Cluster'):
				mel.eval('CreateCluster;') #create cluster
			cmb.setCurrentIndex(0)


	def chk000(self):
		'''
		Scale Joint
		'''
		self.toggleWidgets(setUnChecked='chk001-2')
		self.parentUi.tb000.s000.setValue(pm.jointDisplayScale(query=1)) #init global joint display size


	def chk001(self):
		'''
		Scale IK
		'''
		self.toggleWidgets(setUnChecked='chk000, chk002')
		self.parentUi.s000.setValue(pm.ikHandleDisplayScale(query=1)) #init IK handle display size
		

	def chk002(self):
		'''
		Scale IK/FK
		'''
		self.toggleWidgets(setUnChecked='chk000-1')
		self.parentUi.s000.setValue(pm.jointDisplayScale(query=1, ikfk=1)) #init IKFK display size


	def s000(self):
		'''
		Scale Joint/IK/FK
		'''
		value = self.parentUi.s000.value()

		if self.parentUi.chk000.isChecked():
			pm.jointDisplayScale(value) #set global joint display size
		elif self.parentUi.chk001.isChecked():
			pm.ikHandleDisplayScale(value) #set global IK handle display size
		else: #self.parentUi.chk002.isChecked():
			pm.jointDisplayScale(value, ikfk=1) #set global IKFK display size


	def tb000(self, state=None):
		'''
		Toggle Display Local Rotation Axes
		'''
		tb = self.currentUi.tb000
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='Joints', setObjectName='chk000', setChecked=True, setToolTip='Display Joints.')
			tb.add('QCheckBox', setText='IK', setObjectName='chk001', setChecked=True, setToolTip='Display IK.')
			tb.add('QCheckBox', setText='IK\\FK', setObjectName='chk002', setChecked=True, setToolTip='Display IK\\FK.')
			tb.add('QDoubleSpinBox', setPrefix='Tolerance: ', setObjectName='s000', minMax_='0.00-10 step.5', setValue=1.0, setToolTip='Global Display Scale for the selected type.')
			
			try:
				self.chk000() #init scale joint value
			except NameError:
				pass
			if state=='setMenu':
				return

		joints = pm.ls(type="joint") #get all scene joints

		state = pm.toggle(joints[0], query=1, localAxis=1)
		if tb.isChecked():
			if not state:
				toggle=True
		else:
			if state:
				toggle=True

		if toggle:
			pm.toggle(joints, localAxis=1) #set display off

		self.viewPortMessage("Display Local Rotation Axes:<hl>"+str(state)+"</hl>")


	def tb001(self, state=None):
		'''
		Orient Joints
		'''
		tb = self.currentUi.tb001
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='Align world', setObjectName='chk003', setToolTip='Align joints with the worlds transform.')
			if state=='setMenu':
				return

		orientJoint = 'xyz' #orient joints
		if tb.isChecked():
			orientJoint = 'none' #orient joint to world

		pm.joint(edit=1, orientJoint=orientJoint, zeroScaleOrient=1, ch=1)


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
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------