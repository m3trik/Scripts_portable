from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Lighting(Init):
	def __init__(self, *args, **kwargs):
		super(Lighting, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('lighting')
		self.childUi = self.sb.getUi('lighting_submenu')


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
		# 	if index==cmd.items.index(''):
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
		mel.eval("")


	def b009(self):
		'''

		'''
		pass






#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------