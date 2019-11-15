import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Utilities(Init):
	def __init__(self, *args, **kwargs):
		super(Utilities, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('utilities')

		




	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = self.comboBox(cmb, files, ' ')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				mel.eval('')
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
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------