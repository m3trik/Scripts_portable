from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class DynLayout(Init):
	def __init__(self, *args, **kwargs):
		super(DynLayout, self).__init__(*args, **kwargs)


	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.dynLayout_ui.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb000', setToolTip='')
			draggable_header.contextMenu.add('QPushButton', setText='Delete History', setObjectName='b000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.dynLayout_ui.cmb000
		
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