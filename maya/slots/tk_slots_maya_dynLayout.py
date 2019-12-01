import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class DynLayout(Init):
	def __init__(self, *args, **kwargs):
		super(DynLayout, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('dynLayout')



	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = self.comboBox(cmb, files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				mel.eval('')
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		

		'''
		pass





#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------