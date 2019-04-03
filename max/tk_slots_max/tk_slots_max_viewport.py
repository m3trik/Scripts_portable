import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Viewport(Init):
	def __init__(self, *args, **kwargs):
		super(Viewport, self).__init__(*args, **kwargs)



	def cmb000(self):
		'''
		Editors

		'''
		cmb = self.hotBox.ui.cmb000
		index = cmb.currentIndex() #get current index before refreshing list
		list_ = ['Camera Sequencer', 'Camera Set Editor']
		self.comboBox (cmb, list_, "Editors")

		if index!=0:
			if index==1:
				mel.eval('SequenceEditor;')
			if index==2:
				mel.eval('cameraSetEditor;')
			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		Cameras

		'''
		cmb = self.hotBox.ui.cmb001
		index = cmb.currentIndex() #get current index before refreshing list
		cameras = [cam.name for cam in rt.cameras if 'Target' not in cam.name] #List scene Cameras
		items = self.comboBox (cmb, cameras, "Cameras:")
		
		if index!=0:
			cam = rt.getNodeByName(items[index])
			rt.select (cam) #select the camera
			rt.viewport.setCamera (cam) #set viewport to camera
			cmb.setCurrentIndex(0)


	def cmb002(self):
		'''
		Options

		'''
		cmb = self.hotBox.ui.cmb002
		index = cmb.currentIndex() #get current index before refreshing list
		list_ = ['Create: Custom Camera','Create: Set Custom Camera','Create: Camera From View','Group Cameras']
		self.comboBox (cmb, list_, "Options")

		if index!=0:
			if index==1:
				mel.eval('cameraView -edit -camera persp -setCamera $homeName;')
			if index==2:
				mel.eval('string $homeName = `cameraView -camera persp`;')
			if index==3:
				mel.eval('print "--no code--"')
			if index==4:
				mel.eval('''
				if (`objExists cameras`)
				{
				  print "Group 'cameras' already exists";
				}
				else
				{
				  group -world -name cameras side front top persp;
				  hide cameras;
				  // Now add non-default cameras to group
				  if (`objExists back`)
				  {
				  	parent back cameras;
				  }
				  if (`objExists bottom`)
				  {
				  	parent bottom cameras;
				  }
				  if (`objExists left`)
				  {
				  	parent left cameras;
				  }
				  if (`objExists alignToPoly`)
				  {
				  	parent alignToPoly cameras;
				  }
				}
				''')
			cmb.setCurrentIndex(0)




	def v000(self):
		'''
		Viewport: Back View

		'''
		maxEval("max vpt back")

	def v001(self):
		'''
		Viewport: Top View

		'''
		maxEval("max vpt top")

	def v002(self):
		'''
		Viewport: Right View

		'''
		maxEval("max vpt right")

	def v003(self):
		'''
		Viewport: Left View

		'''
		maxEval("max vpt left")

	def v004(self):
		'''
		Viewport: Perspective View

		'''
		maxEval("max vpt persp user")

	def v005(self):
		'''
		Viewport: Front View

		'''
		maxEval("max vpt front")

	def v006(self):
		'''
		Viewport: Bottom View

		'''
		maxEval("max vpt bottom")

	def v007(self):
		'''
		Viewport: Align View

		'''
		maxEval('''
		max vpt iso user
		max align camera
		''')

	def v008(self):
		'''

		'''
		pass

	def v009(self):
		'''

		'''
		pass

	def v010(self):
		'''
		Camera: Dolly
		'''
		maxEval("max dolly mode")

	def v011(self):
		'''
		Camera: Roll
		'''
		maxEval("max roll")

	def v012(self):
		'''
		Camera: Truck

		'''
		maxEval("max truck")

	def v013(self):
		'''
		Camera: Orbit

		'''
		maxEval("max pancamera")

	def v014(self):
		'''
		

		'''
		pass

	def v015(self):
		'''
		

		'''
		pass


	# ------------------------------------





#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

