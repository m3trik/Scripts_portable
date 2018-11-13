import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





#                    oo                       dP   oo                   
#                                             88                        
#  .d8888b. 88d888b. dP 88d8b.d8b. .d8888b. d8888P dP .d8888b. 88d888b. 
#  88'  `88 88'  `88 88 88'`88'`88 88'  `88   88   88 88'  `88 88'  `88 
#  88.  .88 88    88 88 88  88  88 88.  .88   88   88 88.  .88 88    88 
#  `88888P8 dP    dP dP dP  dP  dP `88888P8   dP   dP `88888P' dP    dP 
#                                                       
class Animation(Init):
	def __init__(self, *args, **kwargs):
		super(Animation, self).__init__(*args, **kwargs)

		#init widgets
		func.initWidgets(self)


	def chk000(self): #pin open a separate instance of the ui in a new window
		if self.ui.chk000.isChecked():
			self.hotBox.pin()
		else:
			self.hotBox.pin.hide()

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