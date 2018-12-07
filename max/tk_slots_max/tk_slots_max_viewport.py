import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Viewport(Init):
	def __init__(self, *args, **kwargs):
		super(Viewport, self).__init__(*args, **kwargs)

	def cmb000(self): #list scene cameras
		index = self.hotBox.ui.cmb000.currentIndex() #get current index before refreshing list
		cameras = [cam.name for cam in rt.cameras if 'Target' not in cam.name]
		items = self.comboBox (self.hotBox.ui.cmb000, cameras, "Cameras:")
		
		if index!=0:
			rt.select (rt.getNodeByName(items[index]))
			self.hotBox.ui.cmb000.setCurrentIndex(0)

	def v000(self): #viewport: back view
		maxEval("max vpt back")

	def v001(self): #viewport: top view
		maxEval("max vpt top")

	def v002(self): #viewport: right view
		maxEval("max vpt right")

	def v003(self): #viewport: left view
		maxEval("max vpt left")

	def v004(self): #viewport: perspective view
		maxEval("max vpt persp user")

	def v005(self): #viewport: front view
		maxEval("max vpt front")

	def v006(self): #viewport: bottom view
		maxEval("max vpt bottom")

	def v007(self): #viewport: align view
		maxEval('''
		max vpt iso user
		max align camera
		''')

	def v008(self): #camera: dolly/zoom
		maxEval("max dolly mode")

	def v009(self): #camera: roll
		maxEval("max roll")

	def v010(self): #camera: truck/pan
		maxEval("max truck")

	def v011(self): #camera: orbit
		maxEval("max pancamera")

	def v012(self): #
		pass

	def v013(self): #
		pass

	def v014(self): #
		pass

	def v015(self): #
		pass


#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

