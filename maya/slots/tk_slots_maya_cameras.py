from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Cameras(Init):
	def __init__(self, *args, **kwargs):
		super(Cameras, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('cameras')



	def tree000(self, wItem=None, column=None):
		'''

		'''
		tree = self.ui.tree000

		if not any([wItem, column]):
			if not tree.refresh:
				tree.expandOnHover = True
				tree.convert(tree.getTopLevelItems(), 'QLabel') #construct the tree using the existing contents.

			try:
				cameras = pm.ls(type=('camera'), l=True) #Get all cameras
				startup_cameras = [camera for camera in cameras if pm.camera(camera.parent(0), startupCamera=True, q=True)] #filter all startup / default cameras
				non_startup_cameras_pynodes = list(set(cameras) - set(startup_cameras)) #get non-default cameras. these are all PyNodes
				non_startup_cameras_transform_pynodes = map(lambda x: x.parent(0), non_startup_cameras_pynodes) #get respective transform names
				non_startup_cameras = map(str, non_startup_cameras_pynodes) #non-PyNode, regular string name list
				non_startup_cameras_transforms = map(str, non_startup_cameras_transform_pynodes)
			except AttributeError: non_startup_cameras=[]
			[tree.add('QLabel', 'Cameras', refresh=True, setText=s) for s in non_startup_cameras]

			l = ['Camera Sequencer', 'Camera Set Editor']
			[tree.add('QLabel', 'Editors', setText=s) for s in l]

		else:
			# widget = tree.getWidget(wItem, column)
			text = tree.getWidgetText(wItem, column)
			header = tree.getHeaderFromColumn(column)
			print(header, text, column)

			if header=='Create':
				if text=='Custom Camera':
					mel.eval('camera -centerOfInterest 5 -focalLength 35 -lensSqueezeRatio 1 -cameraScale 1 -horizontalFilmAperture 1.41732 -horizontalFilmOffset 0 -verticalFilmAperture 0.94488 -verticalFilmOffset 0 -filmFit Fill -overscan 1 -motionBlur 0 -shutterAngle 144 -nearClipPlane 0.1 -farClipPlane 10000 -orthographic 0 -orthographicWidth 30 -panZoomEnabled 0 -horizontalPan 0 -verticalPan 0 -zoom 1; objectMoveCommand; cameraMakeNode 1 "";')
				if text=='Set Custom Camera':
					mel.eval('string $homeName = `cameraView -camera persp`;') #cameraView -edit -camera persp -setCamera $homeName;
				if text=='Camera From View':
					mel.eval('print "--no code--"')

			if header=='Cameras':
				pm.select(text)
				pm.lookThru(text)

			if header=='Editors':
				if text=='Camera Sequencer':
					mel.eval('SequenceEditor;')
				if text=='Camera Set Editor':
					mel.eval('cameraSetEditor;')

			if header=='Options':
				if text=='Group Cameras':
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
					}''')


	def v000(self):
		'''
		Cameras: Back View

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
		Cameras: Top View

		'''
		pm.lookThru ("topShape")

	def v002(self):
		'''
		Cameras: Right View

		'''
		pm.lookThru ("sideShape")

	def v003(self):
		'''
		Cameras: Left View

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
		Cameras: Perspective View

		'''
		pm.lookThru ("perspShape")

	def v005(self):
		'''
		Cameras: Front View

		'''
		pm.lookThru ("frontShape")

	def v006(self):
		'''
		Cameras: Bottom View

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
		Cameras: Align View

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
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------




#deprecated -------------------------------------


	# def cmb000(self, index=None):
	# 	'''
	# 	Camera Editors

	# 	'''
	# 	cmb = self.ui.cmb000
		
	# 	list_ = ['Camera Sequencer', 'Camera Set Editor']
	# 	contents = cmb.addItems_(list_, ' ')

	# 	if not index:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		if index==1:
	# 			mel.eval('SequenceEditor;')
	# 		if index==2:
	# 			mel.eval('cameraSetEditor;')
	# 		cmb.setCurrentIndex(0)


	# def cmb001(self, index=None):
	# 	'''
	# 	Additional Cameras

	# 	'''
	# 	# Get all cameras first
	# 	cameras = pm.ls(type=('camera'), l=True)
	# 	# Let's filter all startup / default cameras
	# 	startup_cameras = [camera for camera in cameras if pm.camera(camera.parent(0), startupCamera=True, q=True)]
	# 	# non-default cameras are easy to find now. Please note that these are all PyNodes
	# 	non_startup_cameras_pynodes = list(set(cameras) - set(startup_cameras))
	# 	# Let's get their respective transform names, just in-case
	# 	non_startup_cameras_transform_pynodes = map(lambda x: x.parent(0), non_startup_cameras_pynodes)
	# 	# Now we can have a non-PyNode, regular string names list of them
	# 	non_startup_cameras = map(str, non_startup_cameras_pynodes)
	# 	non_startup_cameras_transforms = map(str, non_startup_cameras_transform_pynodes)

	# 	cmb = self.ui.cmb001
		
	# 	contents = cmb.addItems_(non_startup_cameras, "Cameras")

	# 	if not index:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		pm.select (contents[index])
	# 		cmb.setCurrentIndex(0)


	# def cmb002(self, index=None):
	# 	'''
	# 	Create

	# 	'''
	# 	cmb = self.ui.cmb002
		
	# 	list_ = ['Custom Camera', 'Set Custom Camera', 'Camera From View']
	# 	contents = cmb.addItems_(list_, "Create")

	# 	if not index:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		if index==1:
	# 			mel.eval('cameraView -edit -camera persp -setCamera $homeName;')
	# 		if index==2:
	# 			mel.eval('string $homeName = `cameraView -camera persp`;')
	# 		if index==3:
	# 			mel.eval('print "--no code--"')
	# 		cmb.setCurrentIndex(0)


	# def cmb003(self, index=None):
	# 	'''
	# 	Options

	# 	'''
	# 	cmb = self.ui.cmb003
		
	# 	list_ = ['Group Cameras']
	# 	contents = cmb.addItems_(list_, "Options")

	# 	if not index:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		if index==1:
	# 			mel.eval('''
	# 			if (`objExists cameras`)
	# 			{
	# 			  print "Group 'cameras' already exists";
	# 			}
	# 			else
	# 			{
	# 			  group -world -name cameras side front top persp;
	# 			  hide cameras;
	# 			  // Now add non-default cameras to group
	# 			  if (`objExists back`)
	# 			  {
	# 			  	parent back cameras;
	# 			  }
	# 			  if (`objExists bottom`)
	# 			  {
	# 			  	parent bottom cameras;
	# 			  }
	# 			  if (`objExists left`)
	# 			  {
	# 			  	parent left cameras;
	# 			  }
	# 			  if (`objExists alignToPoly`)
	# 			  {
	# 			  	parent alignToPoly cameras;
	# 			  }
	# 			}
	# 			''')
	# 		cmb.setCurrentIndex(0)
