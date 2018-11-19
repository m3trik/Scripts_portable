import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Viewport(Init):
	def __init__(self, *args, **kwargs):
		super(Viewport, self).__init__(*args, **kwargs)

		#init widgets
		self.initWidgets(self)
	

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

	def v008(self): #component mode:vertex
		pm.selectMode (component=True)
		pm.selectType (subdivMeshPoint=1, polymeshVertex=True)
		self.viewPortMessage("<hl>vertex</hl> mask.")

	def v009(self): #component mode:edge
		pm.selectMode (component=True)
		pm.selectType (subdivMeshEdge=1, polymeshEdge=True)
		self.viewPortMessage("<hl>edge</hl> mask.")

	def v010(self): #component mode:facet
		pm.selectMode (component=True)
		pm.selectType (subdivMeshFace=1, polymeshFace=True)
		self.viewPortMessage("<hl>facet</hl> mask.")

	def v011(self): #object mode
		pm.selectMode (object=True)
		self.viewPortMessage("<hl>object</hl> mode.")

	def v012(self): #component mode:uv
		pm.selectMode (component=True)
		pm.selectType (subdivMeshUV=True, polymeshUV=True)
		self.viewPortMessage("<hl>UV</hl> mask.")

	def v013(self): #
		pass

	def v014(self): #
		pass

	def v015(self): #
		pass





#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------