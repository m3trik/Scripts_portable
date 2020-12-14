from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Fx(Init):
	def __init__(self, *args, **kwargs):
		super(Fx, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('fx')
		self.childUi = self.sb.getUi('fx_submenu')


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


	def b000(self):
		'''
		
		'''
		pass


	def b001(self):
		'''
		
		'''
		pass


	def b002(self):
		'''
		
		'''
		pass


	def b003(self):
		'''
		
		'''
		pass


	def b004(self):
		'''
		
		'''
		pass


	def b005(self):
		'''
		
		'''
		pass


	def b006(self):
		'''
		
		'''
		pass


	def b007(self):
		'''
		
		'''
		pass


	def b008(self):
		'''
		
		'''
		pass


	def b009(self):
		'''
		
		'''
		pass








#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------