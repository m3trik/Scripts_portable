import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





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
		list_ = ['Custom Camera','Set Custom Camera','Camera From View']
		self.comboBox (self.hotBox.ui.cmb001, list_, "")

		if index!=0:
			if index==1:
				mel.eval('cameraView -edit -camera persp -setCamera $homeName;')
			if index==2:
				mel.eval('string $homeName = `cameraView -camera persp`;')
			if index==3:
				mel.eval('print "--no code--"')
			self.hotBox.ui.cmb001.setCurrentIndex(0)


	def cmb002(self): #Modify
		index = self.hotBox.ui.cmb001.currentIndex() #get current index before refreshing list
		list_ = ['Group Cameras']
		self.comboBox (self.hotBox.ui.cmb001, list_, "")

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
			self.hotBox.ui.cmb001.setCurrentIndex(0)


	def cmb003(self): #Editors
		index = self.hotBox.ui.cmb001.currentIndex() #get current index before refreshing list
		list_ = ['Camera Sequencer',Camera Set Editor]
		self.comboBox (self.hotBox.ui.cmb001, list_, "")

		if index!=0:
			if index==1:
				mel.eval('SequenceEditor;')
			if index==2:
				mel.eval('cameraSetEditor;')
			self.hotBox.ui.cmb001.setCurrentIndex(0)



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

	# g009 camera transforms -------------
	def b000(self): #camera: dolly/zoom
		pass

	def b001(self): #camera: roll
		pass

	def b002(self): #camera: truck/pan
		pass

	def b003(self): #camera: orbit
		pass
	# ------------------------------------






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------