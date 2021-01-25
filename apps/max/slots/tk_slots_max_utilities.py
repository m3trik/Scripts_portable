from __future__ import print_function
from builtins import super
import os.path

from tk_slots_max_init import *



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
			list_ = ['']
			items = cmb.addItems_(list_, '')
			return

		if index>0:
			if index==cmb.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def b000(self):
		'''Measure
		'''
		maxEval('macros.run \"Tools\" \"two_point_dist\"')


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


	def b004(self):
		''''''
		pass


	def b005(self):
		''''''
		pass


	def b006(self):
		''''''
		pass


	def b007(self):
		''''''
		pass


	def b008(self):
		''''''
		pass


	def b009(self):
		''''''
		pass








#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------