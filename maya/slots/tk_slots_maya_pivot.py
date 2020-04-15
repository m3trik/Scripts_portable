from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Pivot(Init):
	def __init__(self, *args, **kwargs):
		super(Pivot, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('pivot')



	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				mel.eval('')
			cmb.setCurrentIndex(0)

		
	def b000(self):
		'''
		Center Pivot Object

		'''
		mel.eval("CenterPivot;")


	def b001(self):
		'''
		Center Pivot Component

		'''
		[pm.xform (s, centerPivot=1) for s in pm.ls (sl=1, objectsOnly=1, flatten=1)]
		# mel.eval("moveObjectPivotToComponentCentre;")

	def b002(self):
		'''
		Center Pivot World

		'''
		mel.eval("xform -worldSpace -pivots 0 0 0;")

	def b003(self):
		'''
		Set To Bounding Box

		'''
		mel.eval("bt_alignPivotToBoundingBoxWin;")

	def b004(self):
		'''
		Bake Pivot

		'''
		mel.eval("BakeCustomPivot;")


	def b005(self):
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