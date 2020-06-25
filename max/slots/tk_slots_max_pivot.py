from __future__ import print_function
from tk_slots_max_init import *

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
			if index==items.index('Component'):
				self.centerPivot(rt.selection)
			if index==items.index('Object'):
				self.centerPivot(rt.selection)
			if index==items.index('World'):
				rt.selection.pivot = [0,0,0]
			cmb.setCurrentIndex(0)


	@Slots.message
	def tb000(self, state=None):
		'''
		Reset Pivot
		'''
		tb = self.currentUi.tb000
		# if not tb.containsMenuItems:
		# 	tb.add('QCheckBox', setText='Reset Pivot Position', setObjectName='chk000', setChecked=True, setToolTip='')
		# 	tb.add('QCheckBox', setText='Reset Pivot Orientation', setObjectName='chk001', setChecked=True, setToolTip='')
		# 	if state=='setMenu':
		# 		return

		# resetPivotPosition = tb.chk000.isChecked() #Reset Pivot Position
		# resetPivotOrientation = tb.chk001.isChecked() #Reset Pivot Orientation
		print ('no function')
		# pm.manipPivotReset(resetPivotPosition, resetPivotOrientation)
		# return 'Reset Pivot Position <hl>{0}</hl>.\nReset Pivot Orientation <hl>{1}</hl>.'.format(int(resetPivotPosition), int(resetPivotOrientation)).replace('0', 'Off').replace('1', 'On')


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
		print ('no function')


	@staticmethod
	def centerPivot(objects):
		'''
		Center the rotation pivot on the given objects.
		'''
		for obj in objects:
			rt.toolMode.coordsys(obj) #Center Pivot Object
			obj.pivot = obj.center





	





#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

# maxEval('max tti')

# maxEval('macros.run \"PolyTools\" \"TransformTools\")

