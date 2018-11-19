import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Fx(Init):
	def __init__(self, *args, **kwargs):
		super(Fx, self).__init__(*args, **kwargs)

		#init widgets
		self.initWidgets(self)


	def b000(self): #
		maxEval('')

	def b001(self): #
		maxEval('')

	def b002(self): #
		maxEval('')

	def b003(self): #
		maxEval('')

	def b004(self): #
		maxEval('')

	def b005(self): #
		maxEval('')

	def b006(self): #
		maxEval('')

	def b007(self): #
		maxEval('')

	def b008(self): #
		mel.eval("")

	def b009(self): #
		maxEval('')


#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------