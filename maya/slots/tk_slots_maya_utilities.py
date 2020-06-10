from __future__ import print_function
from tk_slots_maya_init import *

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
		
		files = ['']
		contents = cmb.addItems_(files, '')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Measure

		'''
		mel.eval("DistanceTool;")


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
		mel.eval('')


	def b005(self):
		'''
		

		'''
		mel.eval('')


	def b006(self):
		'''
		

		'''
		mel.eval('')


	def b007(self):
		'''
		

		'''
		mel.eval('')


	def b008(self):
		'''
		

		'''
		mel.eval("")


	def b009(self):
		'''
		

		'''
		mel.eval('')


#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------