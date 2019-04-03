import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Utilities(Init):
	def __init__(self, *args, **kwargs):
		super(Utilities, self).__init__(*args, **kwargs)




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
		maxEval('')

	def b005(self):
		'''
		

		'''
		maxEval('')

	def b006(self):
		'''
		

		'''
		maxEval('')

	def b007(self):
		'''
		

		'''
		maxEval('')

	def b008(self):
		'''
		

		'''
		mel.eval("")

	def b009(self):
		'''
		

		'''
		maxEval('')


#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------