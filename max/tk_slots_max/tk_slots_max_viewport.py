import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Viewport(Init):
	def __init__(self, *args, **kwargs):
		super(Viewport, self).__init__(*args, **kwargs)





	def cmb000(self): #Scene Cameras
		index = self.hotBox.ui.cmb001.currentIndex() #get current index before refreshing list
		list_ = []
		self.comboBox (self.hotBox.ui.cmb001, list_, "")

		if index!=0:
			
			self.hotBox.ui.cmb001.setCurrentIndex(0)


	def cmb001(self): #Create
		index = self.hotBox.ui.cmb001.currentIndex() #get current index before refreshing list
		list_ = []
		self.comboBox (self.hotBox.ui.cmb001, list_, "")

		if index!=0:
			
			self.hotBox.ui.cmb001.setCurrentIndex(0)


	def cmb002(self): #Modify
		index = self.hotBox.ui.cmb001.currentIndex() #get current index before refreshing list
		list_ = []
		self.comboBox (self.hotBox.ui.cmb001, list_, "")

		if index!=0:
			
			self.hotBox.ui.cmb001.setCurrentIndex(0)


	def cmb003(self): #Editors
		index = self.hotBox.ui.cmb001.currentIndex() #get current index before refreshing list
		list_ = []
		self.comboBox (self.hotBox.ui.cmb001, list_, "")

		if index!=0:
			
			self.hotBox.ui.cmb001.setCurrentIndex(0)



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

	def v008(self):
		pass

	def v009(self):
		pass

	def v010(self):
		pass

	def v011(self):
		pass

	def v012(self): #
		pass

	def v013(self): #
		pass

	def v014(self): #
		pass

	def v015(self): #
		pass

	# g009 camera transforms --------------
	def b000(self): #camera: dolly/zoom
		maxEval("max dolly mode")

	def b001(self): #camera: roll
		maxEval("max roll")

	def b002(self): #camera: truck/pan
		maxEval("max truck")

	def b003(self): #camera: orbit
		maxEval("max pancamera")
	# ------------------------------------





#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

