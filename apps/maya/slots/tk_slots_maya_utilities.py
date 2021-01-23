from __future__ import print_function
from builtins import super
import os.path

from tk_slots_maya_init import *



class Utilities(Init):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.utilities_ui.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.utilities_ui.cmb000

		if index is 'setMenu':
			files = ['']
			cmb.addItems_(files, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def b000(self):
		'''Measure
		'''
		mel.eval("DistanceTool;")


	def b001(self):
		'''Annotation
		'''
		mel.eval('CreateAnnotateNode;')


	def b002(self):
		'''Calculator
		'''
		mel.eval('calculator;')


	def b003(self):
		'''Grease Pencil
		'''
		mel.eval('greasePencilCtx;')









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------