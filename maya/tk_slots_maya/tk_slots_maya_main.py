import maya.mel as mel
import pymel.core as pm

import os.path
from pydoc import locate

from tk_slots_maya_init import Init




#                     oo          
#                           
# 88d8b.d8b. .d8888b. dP 88d888b. 
# 88'`88'`88 88'  `88 88 88'  `88 
# 88  88  88 88.  .88 88 88    88 
# dP  dP  dP `88888P8 dP dP    dP 
#
class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)




	def v000(self): #Extrude
		print "# Result: perform extrude #"
		locate('Polygons(self.hotBox).b006()')

	def v001(self): #Bridge
		print "# Result: bridge #"
		locate('Polygons(self.hotBox).b005()')

	def v002(self): #Multi-cut tool
		print "# Result: multi-cut #"
		locate('Polygons(self.hotBox).b012()')

	def v003(self): #Delete history
		print "# Result: delete history #"
		locate('Edit(self.hotBox).b016()')

	def v004(self): #Delete
		print "# Result: delete #"
		locate('Edit(self.hotBox).b032()')

	def v005(self): #
		pass

	def v006(self): #Toggle mode
		self.cycle('shortCutMode_01234')

	def v007(self): #Minimize main application
		mel.eval("minimizeApp;")
		self.hotBox.hbHide()



#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------