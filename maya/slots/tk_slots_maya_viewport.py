import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Viewport(Init):
	def __init__(self, *args, **kwargs):
		super(Viewport, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('viewport')





		
	def cmb000(self):
		'''
		Camera Editors

		'''
		cmb = self.ui.cmb000
		
		list_ = ['Camera Sequencer', 'Camera Set Editor']
		contents = self.comboBox(cmb, list_, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==1:
				mel.eval('SequenceEditor;')
			if index==2:
				mel.eval('cameraSetEditor;')
			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		Additional Cameras

		'''
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

		cmb = self.ui.cmb001
		
		contents = self.comboBox (cmb, non_startup_cameras, "Cameras")

		index = cmb.currentIndex()
		if index!=0:
			pm.select (contents[index])
			cmb.setCurrentIndex(0)


	def cmb002(self):
		'''
		Create

		'''
		cmb = self.ui.cmb002
		
		list_ = ['Custom Camera', 'Set Custom Camera', 'Camera From View']
		contents = self.comboBox (cmb, list_, "Create")

		index = cmb.currentIndex()
		if index!=0:
			if index==1:
				mel.eval('cameraView -edit -camera persp -setCamera $homeName;')
			if index==2:
				mel.eval('string $homeName = `cameraView -camera persp`;')
			if index==3:
				mel.eval('print "--no code--"')
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

	def v001(self):
		'''
		Viewport: Top View

		'''
		pm.lookThru ("topShape")

	def v002(self):
		'''
		Viewport: Right View

		'''
		pm.lookThru ("sideShape")

	def v003(self):
		'''
		Viewport: Left View

		'''
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

	def v004(self):
		'''
		Viewport: Perspective View

		'''
		pm.lookThru ("perspShape")

	def v005(self):
		'''
		Viewport: Front View

		'''
		pm.lookThru ("frontShape")

	def v006(self):
		'''
		Viewport: Bottom View

		'''
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

	def v007(self):
		'''
		Viewport: Align View

		'''
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
		pass

	def v011(self):
		'''
		Camera: Roll

		'''
		pass

	def v012(self):
		'''
		Camera: Truck

		'''
		pass

	def v013(self):
		'''
		Camera: Orbit

		'''
		pass

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