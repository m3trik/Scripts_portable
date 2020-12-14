from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Pivot(Init):
	def __init__(self, *args, **kwargs):
		super(Pivot, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('pivot')
		self.childUi = self.sb.getUi('pivot_submenu')


	def d000(self, state=None):
		'''
		Context menu
		'''
		d000 = self.parentUi.d000

		if state is 'setMenu':
			d000.contextMenu.add(widgets.TkComboBox, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000

		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Center Pivot
		'''
		cmb = self.parentUi.cmb001

		if index is 'setMenu':
			list_ = ['Component', 'Object', 'World']
			cmb.addItems_(list_, 'Center Pivot')
			return

		if index>0:
			if index==cmb.items.index('Component'): #Set pivot points to the center of the component's bounding box.
				pm.xform(centerPivotsOnComponents=1)
			elif index==cmb.items.index('Object'): ##Set pivot points to the center of the object's bounding box
				pm.xform(centerPivots=1)
			elif index==cmb.items.index('World'):
				pm.xform(worldSpace=1, pivots=[0,0,0])
			cmb.setCurrentIndex(0)


	@Slots.message
	def tb000(self, state=None):
		'''
		Reset Pivot
		'''
		tb = self.currentUi.tb000
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Reset Pivot Position', setObjectName='chk000', setChecked=True, setToolTip='')
			tb.menu_.add('QCheckBox', setText='Reset Pivot Orientation', setObjectName='chk001', setChecked=True, setToolTip='')
			return

		resetPivotPosition = tb.menu_.chk000.isChecked() #Reset Pivot Position
		resetPivotOrientation = tb.menu_.chk001.isChecked() #Reset Pivot Orientation

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