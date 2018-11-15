import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Slot
import tk_maya_shared_functions as func





# .8888b          
# 88   "          
# 88aaa  dP.  .dP 
# 88      `8bd8'  
# 88      .d88b.  
# dP     dP'  `dP 
#
class Fx(Slot):
	def __init__(self, *args, **kwargs):
		super(Fx, self).__init__(*args, **kwargs)

		#init widgets
		func.initWidgets(self)


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