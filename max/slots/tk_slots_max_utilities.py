from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Utilities(Init):
	def __init__(self, *args, **kwargs):
		super(Utilities, self).__init__(*args, **kwargs)


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
			items = cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Measure
		'''
		maxEval('macros.run \"Tools\" \"two_point_dist\"')


	def b001(self):
		'''
		Annotation
		'''
		mel.eval('CreateAnnotateNode;')


	def b002(self):
		'''
		Calculator
		'''
		mel.eval('calculator;')


	def b003(self):
		'''
		Grease Pencil
		'''
		mel.eval('greasePencilCtx;')


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