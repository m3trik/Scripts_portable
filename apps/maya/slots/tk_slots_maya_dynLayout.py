from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class DynLayout(Init):
	def __init__(self, *args, **kwargs):
		super(DynLayout, self).__init__(*args, **kwargs)


	def d000(self, state=None):
		'''Context menu
		'''
		d000 = self.dynLayout.d000

		if state is 'setMenu':
			d000.contextMenu.add(widgets.TkComboBox, setObjectName='cmb000', setToolTip='')
			d000.contextMenu.add('QPushButton', setText='Delete History', setObjectName='b000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.dynLayout.cmb000
		
		if index is 'setMenu':
			list_ = []
			cmb.addItems_(list_, '')
			return

		if index>0:
			if index==cmb.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		'''
		self.sb.getMethod('edit', 'tb001')()









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------