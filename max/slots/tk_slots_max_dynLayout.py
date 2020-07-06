from __future__ import print_function
from tk_slots_max_init import *

import os.path




class DynLayout(Init):
	def __init__(self, *args, **kwargs):
		super(DynLayout, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('dynLayout')
		self.childUi = self.sb.getUi('dynLayout_submenu')


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

		if index=='setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def b000(self):
		'''
		

		'''
		pass





#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------