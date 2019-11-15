import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Animation(Init):
	def __init__(self, *args, **kwargs):
		super(Animation, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('animation')



	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000

		files = ['']
		contents = self.comboBox(cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


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
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------