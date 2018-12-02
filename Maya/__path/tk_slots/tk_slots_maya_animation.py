import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





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




	def chk000(self): #pin open a separate instance of the ui in a new window
		if self.hotBox.ui.chk000.isChecked():
			self.hotBox.pin()
		else:
			self.hotBox.pin.hide()

	def b000(self): #
		mel.eval('')

	def b001(self): #
		mel.eval('')

	def b002(self): #
		mel.eval('')

	def b003(self): #
		mel.eval('')

	def b004(self): #
		mel.eval('')

	def b005(self): #
		mel.eval('')

	def b006(self): #
		mel.eval('')

	def b007(self): #
		mel.eval('')

	def b008(self): #
		mel.eval("")

	def b009(self): #
		mel.eval('')



#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------