from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Pivot(Init):
	def __init__(self, *args, **kwargs):
		super(Pivot, self).__init__(*args, **kwargs)


	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.pivot.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.pivot.cmb000

		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		if index>0:
			if index==cmb.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	@Slots.message
	def tb000(self, state=None):
		'''Reset Pivot
		'''
		tb = self.current_ui.tb000
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Reset Pivot Position', setObjectName='chk000', setChecked=True, setToolTip='')
			tb.menu_.add('QCheckBox', setText='Reset Pivot Orientation', setObjectName='chk001', setChecked=True, setToolTip='')
			return

		resetPivotPosition = tb.menu_.chk000.isChecked() #Reset Pivot Position
		resetPivotOrientation = tb.menu_.chk001.isChecked() #Reset Pivot Orientation

		mel.eval('manipPivotReset({0},{1})'.format(int(resetPivotPosition), int(resetPivotOrientation)))
		return 'Reset Pivot Position <hl>{0}</hl>.<br>Reset Pivot Orientation <hl>{1}</hl>.'.format(resetPivotPosition, resetPivotOrientation)


	def tb001(self, state=None):
		'''Center Pivot
		'''
		tb = self.pivot.tb001
		if state is 'setMenu':
			tb.menu_.add('QRadioButton', setText='Component', setObjectName='chk002', setToolTip='Center the pivot on the center of the selected component\'s bounding box')
			tb.menu_.add('QRadioButton', setText='Object', setObjectName='chk003', setChecked=True, setToolTip='Center the pivot on the center of the object\'s bounding box')
			tb.menu_.add('QRadioButton', setText='World', setObjectName='chk004', setToolTip='Center the pivot on world origin.')
			return

		component = tb.menu_.chk002.isChecked()
		object_ = tb.menu_.chk003.isChecked()
		world = tb.menu_.chk004.isChecked()

		if component: #Set pivot points to the center of the component's bounding box.
			pm.xform(centerPivotsOnComponents=1)
		elif object_: ##Set pivot points to the center of the object's bounding box
			pm.xform(centerPivots=1)
		elif world:
			pm.xform(worldSpace=1, pivots=[0,0,0])


	def b000(self):
		'''Center Pivot: Object
		'''
		tb = self.pivot.tb001
		tb.menu_.chk003.setChecked()
		self.tb001()


	def b001(self):
		'''Center Pivot: Component
		'''
		tb = self.pivot.tb001
		tb.menu_.chk002.setChecked()
		self.tb001()


	def b002(self):
		'''Center Pivot: World
		'''
		tb = self.pivot.tb001
		tb.menu_.chk004.setChecked()
		self.tb001()


	def b004(self):
		'''Bake Pivot
		'''
		mel.eval("BakeCustomPivot;")


	@staticmethod
	def resetPivotTransforms(objects):
		'''Reset Pivot Transforms
		'''
		objs = pm.ls(type=['transform', 'geometryShape'], sl=1)

		if len(objs)>0:
			pm.xform(cp=1)
			
		pm.manipPivot(ro=1, rp=1)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------