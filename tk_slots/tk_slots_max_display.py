import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path
import traceback

from tk_slots_max_init import Init


#        dP oo                   dP                   
#        88                      88                   
#  .d888b88 dP .d8888b. 88d888b. 88 .d8888b. dP    dP 
#  88'  `88 88 Y8ooooo. 88'  `88 88 88'  `88 88    88 
#  88.  .88 88       88 88.  .88 88 88.  .88 88.  .88 
#  `88888P8 dP `88888P' 88Y888P' dP `88888P8 `8888P88 
#                       88                        .88 
#                       dP                    d8888P  
#
class Display(Init):
	def __init__(self, *args, **kwargs):
		super(Display, self).__init__(*args, **kwargs)

		#init widgets
		func.initWidgets(self)


	def chk000(self): #division level 1
		func.setAttributesOnSelected (attribute=".smoothLevel", value=1)
		pm.optionVar (intValue=["proxyDivisions",1]) #subDiv proxy options: 'divisions' 
		func.setButtons(self.ui, unchecked='chk001,chk002,chk003,chk004')

	def chk001(self): #division level 2
		func.setAttributesOnSelected (attribute=".smoothLevel", value=2)
		pm.optionVar (intValue=["proxyDivisions",2]) #subDiv proxy options: 'divisions' 
		func.setButtons(self.ui, unchecked='chk000,chk002,chk003,chk004')

	def chk002(self): #division level 3
		func.setAttributesOnSelected (attribute=".smoothLevel", value=3)
		pm.optionVar (intValue=["proxyDivisions",3]) #subDiv proxy options: 'divisions' 
		func.setButtons(self.ui, unchecked='chk000,chk001,chk003,chk004')

	def chk003(self): #division level 4
		func.setAttributesOnSelected (attribute=".smoothLevel", value=4)
		pm.optionVar (intValue=["proxyDivisions",4]) #subDiv proxy options: 'divisions' 
		func.setButtons(self.ui, unchecked='chk000,chk001,chk002,chk004')

	def chk004(self): #division level 5
		func.setAttributesOnSelected (attribute=".smoothLevel", value=5)
		pm.optionVar (intValue=["proxyDivisions",5]) #subDiv proxy options: 'divisions'
		func.setButtons(self.ui, unchecked='chk000,chk001,chk002,chk003')

	def chk005(self): #tessellation level 6
		func.setAttributesOnSelected (attribute=".smoothTessLevel", value=6)
		func.setButtons(self.ui, unchecked='chk006,chk007,chk008,chk009')

	def chk006(self): #tessellation level 7
		func.setAttributesOnSelected (attribute=".smoothTessLevel", value=7)
		func.setButtons(self.ui, unchecked='chk005,chk007,chk008,chk009')

	def chk007(self): #tessellation level 8
		func.setAttributesOnSelected (attribute=".smoothTessLevel", value=8)
		func.setButtons(self.ui, unchecked='chk005,chk006,chk008,chk009')

	def chk008(self): #tessellation level 9
		func.setAttributesOnSelected (attribute=".smoothTessLevel", value=9)
		func.setButtons(self.ui, unchecked='chk005,chk006,chk007,chk009')

	def chk009(self): #tessellation level 10
		func.setAttributesOnSelected (attribute=".smoothTessLevel", value=10)
		func.setButtons(self.ui, unchecked='chk005,chk006,chk007,chk008')


	def b000(self): #Toggle subdiv proxy display
		state = func.cycle('subdivProxy_110')
		try:
			mel.eval("smoothingDisplayToggle "+str(state))
		except:
			traceback.print_exc()
			print "// Warning: Nothing Selected\n"

	def b001(self): #Toggle visibility
		maxEval('ToggleVisibilityAndKeepSelection();')

	def b002(self): #Hide Selected
		maxEval('HideSelectedObjects;')

	def b003(self): #Show selected
		maxEval('ShowSelectedObjects;')

	def b004(self): #Show Geometry
		maxEval('hideShow -geometry -show;')

	def b005(self): #Xray selected
		maxEval('''
		string $sel[] = `ls -sl -dag -s`;
		for ($object in $sel) 
			{
			int $xState[] = `displaySurface -query -xRay $object`;
			displaySurface -xRay ( !$xState[0] ) $object;
			}
		''')

	def b006(self): #Un-Xray all
		maxEval('''
		string $scene[] = `ls -visible -flatten -dag -noIntermediate -type surfaceShape`;
		for ($object in $scene)
			{
			int $state[] = `displaySurface -query -xRay $object`;
			if ($state[0] == 1)
				{
				displaySurface -xRay 0 $object;
				}
			}
		''')

	def b007(self): #Xray other
		maxEval('''
		//xray all except currently selected
		{
		string $scene[] = `ls -visible -flatten -dag -noIntermediate -type surfaceShape`;
		string $selection[] = `ls -selection -dagObjects -shapes`;
		for ($object in $scene)
			{
			if (!stringArrayContains ($object, $selection))
				{
				int $state[] = `displaySurface -query -xRay $object`;
				displaySurface -xRay ( !$state[0] ) $object;
				}
			}
		}
		''')

	def b008(self): #Filter objects
		mel.eval("bt_filterActionWindow;")

	def b009(self): #Subdiv proxy
		global polySmoothBaseMesh
		polySmoothBaseMesh=[]
		#disable creating seperate layers for subdiv proxy
		pm.optionVar (intValue=["polySmoothLoInLayer",0])
		pm.optionVar (intValue=["polySmoothHiInLayer",0])
		#query smooth proxy state.
		sel = mel.eval("polyCheckSelection \"polySmoothProxy\" \"o\" 0")
		
		if len(sel)==0 and len(polySmoothBaseMesh)==0:
			print "// Warning: Nothing selected."
			return
		if len(sel)!=0:
			del polySmoothBaseMesh[:]
			for object_ in sel:
				polySmoothBaseMesh.append(object_)
		elif len(polySmoothBaseMesh) != 0:
			sel = polySmoothBaseMesh

		transform = pm.listRelatives (sel[0], fullPath=1, parent=1)
		shape = pm.listRelatives (transform[0], pa=1, shapes=1)

		#check shape for an existing output to a smoothProxy
		attachedSmoothProxies = pm.listConnections (shape[0], type="polySmoothProxy", s=0, d=1)
		if len(attachedSmoothProxies) == 0: #subdiv on
			func.setButtons(self.ui, enable='b000', checked='b009')
		else:
			func.setButtons(self.ui, disable='b000', unchecked='b009')
			mel.eval("smoothingDisplayToggle 0;")

		#toggle performSmoothProxy
		mel.eval("performSmoothProxy 0;") #toggle SubDiv Proxy;

	def b010(self): #Subdiv proxy options
		maxEval('performSmoothProxy 1;') #SubDiv Proxy Options;

	def b011(self): #toggle component ID display
		index = func.cycle('componentID_01234')

		visible = pm.polyOptions (query=1, displayItemNumbers=1)
		dinArray = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

		if index == 4:
			i=0
			for _ in range(4):
				if visible[i] == True:
					pm.polyOptions (relative=1, displayItemNumbers=dinArray[i], activeObjects=1)
				i+=1

		if visible[index] != True and index != 4:
			pm.polyOptions (relative=1, displayItemNumbers=dinArray[index], activeObjects=1)

			i=0
			for _ in range(4):
				if visible[i] == True and i != index:
					pm.polyOptions (relative=1, displayItemNumbers=dinArray[i], activeObjects=1)
				i+=1

		if index == 0:
			func.viewPortMessage("[1,0,0,0] <hl>vertIDs</hl>.")
		if index == 1:
			func.viewPortMessage("[0,1,0,0] <hl>edgeIDs</hl>.")
		if index == 2:
			func.viewPortMessage("[0,0,1,0] <hl>faceIDs</hl>.")
		if index == 3:
			func.viewPortMessage("[0,0,0,1] <hl>compIDs(UV)</hl>.")
		if index == 4:
			func.viewPortMessage("component ID <hl>Off</hl>.")

	def b012(self): #wireframe non active (wireframe all but the selected item)
		current_panel = pm.getPanel (withFocus=1)
		state = pm.modelEditor (current_panel, query=1, activeOnly=1)
		pm.modelEditor (current_panel, edit=1, activeOnly=not state)

	def b013(self): #
		pass

	def b014(self): #
		pass

	def b015(self): #
		pass

	def b016(self): #
		pass

	def b017(self): #
		pass

	def b018(self): #
		pass

	def b019(self): #
		pass

	def b020(self): #
		pass

	def b021(self): #Template selected
		mel.eval("toggle -template;")

	def b022(self): #
		pass

	def b023(self): #
		pass

	def b024(self): #polygon display options
		mel.eval("CustomPolygonDisplayOptions")
		# mel.eval("polysDisplaySetup 1;")


#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------
	#b012

