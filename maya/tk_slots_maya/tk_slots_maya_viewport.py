import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Viewport(Init):
	def __init__(self, *args, **kwargs):
		super(Viewport, self).__init__(*args, **kwargs)


	def cmb000(self): #Editors
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


	def cmb001(self): #Cameras
		# Get all cameras first
		cameras = pm.ls(type=('camera'), l=True)
		# Let's filter all startup / default cameras
		startup_cameras = [camera for camera in cameras if pm.camera(camera.parent(0), startupCamera=True, q=True)]
		# non-default cameras are easy to find now. Please note that these are all PyNodes
		non_startup_cameras_pynodes = list(set(cameras) - set(startup_cameras))
		# Let's get their respective transform names, just in-case
		non_startup_cameras_transform_pynodes = map(lambda x: x.parent(0), non_startup_cameras_pynodes)
		# Now we can have a non-PyNode, regular string names list of them
		non_startup_cameras = map(str, non_startup_cameras_pynodes)
		non_startup_cameras_transforms = map(str, non_startup_cameras_transform_pynodes)

		cmb = self.hotBox.ui.cmb001
		index = cmb.currentIndex() #get current index before refreshing list
		self.comboBox (cmb, non_startup_cameras, "Cameras")

		if index!=0:
			pm.select (non_startup_cameras[index])
			cmb.setCurrentIndex(0)


	def cmb002(self): #Options
		cmb = self.hotBox.ui.cmb002
		index = cmb.currentIndex() #get current index before refreshing list
		list_ = ['Create: Custom Camera','Create: Set Custom Camera','Create: Camera From View''Group Cameras']
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


	def cmb003(self): #Camera settings
		cmb = self.hotBox.ui.cmb003
		index = cmb.currentIndex() #get current index before refreshing list
		list_ = ['Dolly', 'Roll', 'Truck', 'Pan']
		self.comboBox (cmb, list_, "Settings")

		if index!=0:
			if index==1: #camera: dolly/zoom
				maxEval("max dolly mode")
			if index==2: #camera: roll
				maxEval("max roll")
			if index==1: #camera: truck/pan
				maxEval("max truck")
			if index==2: #camera: orbit
				maxEval("max pancamera")
			cmb.setCurrentIndex(0)



	def v000(self): #viewport: back view
		mel.eval('''
		if (`objExists back`)
		{
		  lookThru back;
		}
		else
		{
		  //create camera
		  string $cameraName[] = `camera`;
		  //cameraName[0] = camera node
		  //cameraName[1] = camera shape node

		  //rename camera node
		  rename($cameraName[0], "back");
		  lookThru back;

		  //initialize the camera view
		  viewSet -back;

		  //add to camera group
		  if (`objExists cameras`)
		  {
			parent back cameras;
		  }
		}
		''')

	def v001(self): #viewport: top view
		pm.lookThru ("topShape")

	def v002(self): #viewport: right view
		pm.lookThru ("sideShape")

	def v003(self): #viewport: left view
		mel.eval('''
		if (`objExists left`)
		{
		  lookThru left;
		}
		else
		{
		  string $cameraName[] = `camera`;
		  //cameraName[0] = camera node
		  //cameraName[1] = camera shape node

		  rename($cameraName[0], "left");
		  lookThru left;

		  //initialize the camera view
		  viewSet -leftSide;

		  //add to camera group
		  if (`objExists cameras`)
		  {
			parent left cameras;
		  }
		}
		''')

	def v004(self): #viewport: perspective view
		pm.lookThru ("perspShape")

	def v005(self): #viewport: front view
		pm.lookThru ("frontShape")

	def v006(self): #viewport: bottom view
		mel.eval('''
		if (`objExists bottom`)
		{
		  lookThru bottom;
		}
		else
		{
		  //create camera
		  string $cameraName[] = `camera`;
		  //cameraName[0] = camera node
		  //cameraName[1] = camera shape node

		  //rename camera node
		  rename($cameraName[0], "bottom");
		  lookThru bottom;

		  //initialize the camera view
		  viewSet -bottom;

		  //add to camera group
		  if (`objExists cameras`)
		  {
			parent bottom cameras;
		  }
		}
		''')

	def v007(self): #viewport: align view
		mel.eval('''
		$cameraExists = `objExists alignToPoly`; //check exists if not create camera
		if ($cameraExists != 1)
		{ 
			string $camera[] = `camera`;
			string $cameraShape = $camera[1];

			rename $camera[0] ("alignToPoly");
			hide alignToPoly;
		}

		int $isPerspective = !`camera -query -orthographic alignToPoly`; //check if camera view is orthoraphicz
		if ($isPerspective) 
		{
			viewPlace -ortho alignToPoly;
		}

		lookThru alignToPoly;
		AlignCameraToPolygon;
		viewFit -fitFactor 5.0;

		//add to camera group
		if (`objExists cameras`)
		{
			parent alignToPoly cameras;
		}
		''')

	def v008(self): #
		pass

	def v009(self): #
		pass

	def v010(self): #
		pass

	def v011(self): #
		pass

	def v012(self): #
		pass

	def v013(self): #
		pass

	def v014(self): #
		pass

	def v015(self): #
		pass


	# ------------------------------------






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------