import maya.mel as mel
import pymel.core as pm

import os.path


from tk_slots_maya_init import Init





class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)



	def v000(self): #Extrude
		self.hotBox.classDict['polygons'](self.hotBox).b006()
		print "# Result: perform extrude #"

	def v001(self): #Bridge
		self.hotBox.classDict['polygons'](self.hotBox).b005()
		print "# Result: bridge #"

	def v002(self): #Multi-cut tool
		self.hotBox.classDict['polygons'](self.hotBox).b012()
		print "# Result: multi-cut #"

	def v003(self): #Delete history
		self.hotBox.classDict['edit'](self.hotBox).b016()
		print "# Result: delete history #"

	def v004(self): #Delete
		self.hotBox.classDict['edit'](self.hotBox).b032()
		print "# Result: delete #"

	def v005(self): #
		pass

	def v006(self): #Toggle mode
		self.cycle('shortCutMode_01234')

	def v007(self): #Minimize main application
		mel.eval("minimizeApp;")
		self.hotBox.hbHide()



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------