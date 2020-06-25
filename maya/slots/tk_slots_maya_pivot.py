from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Pivot(Init):
	def __init__(self, *args, **kwargs):
		super(Pivot, self).__init__(*args, **kwargs)


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

		# if not index:
		# 	index = cmb.currentIndex()
		# if index!=0:
		# 	if index==items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Center Pivot
		'''
		cmb = self.parentUi.cmb001

		list_ = ['Component', 'Object', 'World']
		items = cmb.addItems_(list_, 'Center Pivot')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==items.index('Component'): #Set pivot points to the center of the component's bounding box.
				pm.xform(centerPivotsOnComponents=1)
			if index==items.index('Object'): ##Set pivot points to the center of the object's bounding box
				pm.xform(centerPivots=1)
			if index==items.index('World'):
				pm.xform(worldSpace=1, pivots=[0,0,0])
			cmb.setCurrentIndex(0)


	@Slots.message
	def tb000(self, state=None):
		'''
		Reset Pivot
		'''
		tb = self.currentUi.tb000
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='Reset Pivot Position', setObjectName='chk000', setChecked=True, setToolTip='')
			tb.add('QCheckBox', setText='Reset Pivot Orientation', setObjectName='chk001', setChecked=True, setToolTip='')
			if state=='setMenu':
				return

		resetPivotPosition = tb.chk000.isChecked() #Reset Pivot Position
		resetPivotOrientation = tb.chk001.isChecked() #Reset Pivot Orientation

		mel.eval('manipPivotReset({0},{1})'.format(int(resetPivotPosition), int(resetPivotOrientation)))
		return 'Reset Pivot Position <hl>{0}</hl>.<br>Reset Pivot Orientation <hl>{1}</hl>.'.format(resetPivotPosition, resetPivotOrientation)


	def b000(self):
		'''
		Center Pivot: Object
		'''
		self.cmb001(index=2)


	def b001(self):
		'''
		Center Pivot: Component
		'''
		self.cmb001(index=1)


	def b002(self):
		'''
		Center Pivot: World
		'''
		self.cmb001(index=3)


	def b003(self):
		'''
		Center Pivot: Bounding Box
		'''
		self.cmb001(index=4)


	def b004(self):
		'''
		Bake Pivot

		'''
		mel.eval("BakeCustomPivot;")


	@staticmethod
	def resetPivotTransforms(objects):
		'''
		Reset Pivot Transforms

		'''
		mel.eval('''
		{ string $objs[] = `ls -sl -type transform -type geometryShape`;
		if (size($objs) > 0) { xform -cp; } manipPivot -rp -ro; };
		''')




#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------