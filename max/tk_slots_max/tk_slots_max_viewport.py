import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Viewport(Init):
	def __init__(self, *args, **kwargs):
		super(Viewport, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('viewport')



		
	def cmb000(self):
		'''
		Editors

		'''
		cmb = self.ui.cmb000
		
		list_ = ['Camera Sequencer', 'Camera Set Editor']
		contents = self.comboBox (cmb, list_, "Editors")

		index = cmb.currentIndex()
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
		cmb = self.ui.cmb001
		
		cameras = [cam.name for cam in rt.cameras if 'Target' not in cam.name] #List scene Cameras
		contents = self.comboBox (cmb, cameras, "Cameras:")
		
		index = cmb.currentIndex()
		if index!=0:
			cam = rt.getNodeByName(contents[index])
			rt.select (cam) #select the camera
			rt.viewport.setCamera (cam) #set viewport to camera
			cmb.setCurrentIndex(0)
			rt.redrawViews()


	def cmb002(self):
		'''
		Create

		'''
		cmb = self.ui.cmb002
		
		list_ = ['Custom Camera','Set Custom Camera','Camera From View']
		contents = self.comboBox (cmb, list_, "Create")

		index = cmb.currentIndex()
		if index!=0:
			if index==1:
				rt.StartObjectCreation(rt.Physical_Camera)
			if index==2:
				maxEval('Try(viewport.setcamera $) Catch()')
			if index==3:
				maxEval('macros.run "Lights and Cameras" "PhysicalCamera_CreateFromView"')
			cmb.setCurrentIndex(0)


	def cmb003(self):
		'''
		Options

		'''
		cmb = self.ui.cmb003
		
		list_ = ['Group Cameras']
		contents = self.comboBox (cmb, list_, "Options")

		index = cmb.currentIndex()
		if index!=0:
			if index==1:
				cameras = [cam for cam in rt.cameras] #List scene Cameras

				layer = rt.LayerManager.getLayerFromName ("Cameras")
				if not layer:
					layer = rt.LayerManager.NewLayerFromName("Cameras")

				for cam in cameras:
					layer.addnode(cam)
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

