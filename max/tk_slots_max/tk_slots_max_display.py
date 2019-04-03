import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path
import traceback

from tk_slots_max_init import Init




class Display(Init):
	def __init__(self, *args, **kwargs):
		super(Display, self).__init__(*args, **kwargs)




	def chk000(self):
		'''
		Division Level 1

		'''
		self.setAttributesOnSelected (attribute=".smoothLevel", value=1)
		pm.optionVar (intValue=["proxyDivisions",1]) #subDiv proxy options: 'divisions' 
		self.setButtons(self.hotBox.ui, unchecked='chk001,chk002,chk003,chk004')

	def chk001(self):
		'''
		Division Level 2

		'''
		self.setAttributesOnSelected (attribute=".smoothLevel", value=2)
		pm.optionVar (intValue=["proxyDivisions",2]) #subDiv proxy options: 'divisions' 
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk002,chk003,chk004')

	def chk002(self):
		'''
		Division Level 3

		'''
		self.setAttributesOnSelected (attribute=".smoothLevel", value=3)
		pm.optionVar (intValue=["proxyDivisions",3]) #subDiv proxy options: 'divisions' 
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk001,chk003,chk004')

	def chk003(self):
		'''
		Division Level 4

		'''
		self.setAttributesOnSelected (attribute=".smoothLevel", value=4)
		pm.optionVar (intValue=["proxyDivisions",4]) #subDiv proxy options: 'divisions' 
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk001,chk002,chk004')

	def chk004(self):
		'''
		Division Level 5

		'''
		self.setAttributesOnSelected (attribute=".smoothLevel", value=5)
		pm.optionVar (intValue=["proxyDivisions",5]) #subDiv proxy options: 'divisions'
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk001,chk002,chk003')

	def chk005(self):
		'''
		Tessellation Level 6

		'''
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=6)
		self.setButtons(self.hotBox.ui, unchecked='chk006,chk007,chk008,chk009')

	def chk006(self):
		'''
		Tessellation Level 7

		'''
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=7)
		self.setButtons(self.hotBox.ui, unchecked='chk005,chk007,chk008,chk009')

	def chk007(self):
		'''
		Tessellation Level 8

		'''
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=8)
		self.setButtons(self.hotBox.ui, unchecked='chk005,chk006,chk008,chk009')

	def chk008(self):
		'''
		Tessellation Level 9

		'''
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=9)
		self.setButtons(self.hotBox.ui, unchecked='chk005,chk006,chk007,chk009')

	def chk009(self):
		'''
		Tessellation Level 10

		'''
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=10)
		self.setButtons(self.hotBox.ui, unchecked='chk005,chk006,chk007,chk008')


	def b000(self):
		'''
		Toggle Subdiv Proxy Display

		'''
		state = self.cycle('subdivProxy_110')
		try:
			mel.eval("smoothingDisplayToggle "+str(state))
		except:
			traceback.print_exc()
			print "// Warning: Nothing Selected\n"

	def b001(self):
		'''
		Toggle Visibility

		'''
		sel = [s for s in rt.getCurrentSelection()]

		for obj in sel:
			if obj.visibility == True:
				obj.visibility = False
			else:
				obj.visibility = True

	def b002(self):
		'''
		Hide Selected

		'''
		sel = [s for s in rt.getCurrentSelection()]
	
		for obj in sel:
			if not obj.isHiddenInVpt:
				obj.isHidden = True

	def b003(self):
		'''
		Show Selected

		'''
		sel = [s for s in rt.getCurrentSelection()]
	
		for obj in sel:
			if obj.isHiddenInVpt:
				obj.isHidden = False

	def b004(self):
		'''
		Show Geometry

		'''
		geometry = rt.geometry

		for obj in geometry:
			if obj.isHiddenInVpt:
				obj.isHidden = False

	def b005(self):
		'''
		Xray Selected

		'''
		sel = [s for s in rt.getCurrentSelection()]

		for s in sel:
			s.xray = True

	def b006(self):
		'''
		Un-Xray All

		'''
		geometry = [g for g in rt.geometry]

		for g in geometry:
			g.xray = False

	def b007(self):
		'''
		Xray Other

		'''
		sel = [s for s in rt.getCurrentSelection()]
		geometry = [g for g in rt.geometry]

		for g in geometry:
			if g not in sel:
				g.xray = True

	def b008(self):
		'''
		Filter Objects

		'''
		mel.eval("bt_filterActionWindow;")

	def b009(self):
		'''
		Subdiv Proxy

		'''
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
			self.setButtons(self.hotBox.ui, enable='b000', checked='b009')
		else:
			self.setButtons(self.hotBox.ui, disable='b000', unchecked='b009')
			mel.eval("smoothingDisplayToggle 0;")

		#toggle performSmoothProxy
		mel.eval("performSmoothProxy 0;") #toggle SubDiv Proxy;

	def b010(self):
		'''
		Subdiv Proxy Options

		'''
		maxEval('performSmoothProxy 1;') #SubDiv Proxy Options;

	def b011(self):
		'''
		Toggle Component Id Display

		'''
		index = self.cycle('componentID_01234')

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
			self.viewPortMessage("[1,0,0,0] <hl>vertIDs</hl>.")
		if index == 1:
			self.viewPortMessage("[0,1,0,0] <hl>edgeIDs</hl>.")
		if index == 2:
			self.viewPortMessage("[0,0,1,0] <hl>faceIDs</hl>.")
		if index == 3:
			self.viewPortMessage("[0,0,0,1] <hl>compIDs(UV)</hl>.")
		if index == 4:
			self.viewPortMessage("component ID <hl>Off</hl>.")

	def b012(self):
		'''
		Wireframe Non Active (Wireframe All But The Selected Item)

		'''
		viewport = rt.viewport.activeViewport

		state = self.cycle('wireframeInactive_01')

		if state:
			if not rt.viewport.isWire():
				self.maxUiSetChecked("415", 62, 163, True) #set viewport to wireframe
			self.maxUiSetChecked("40212", 62, 130, True) #Shade selected objects Checked
		else:
			self.maxUiSetChecked("40212", 62, 130, False) #Shade selected objects unchecked

	def b013(self):
		'''
		Viewport Configuration

		'''
		maxEval('actionMan.executeAction 0 "40023"')

	def b014(self):
		'''
		

		'''
		pass

	def b015(self):
		'''
		

		'''
		pass

	def b016(self):
		'''
		

		'''
		pass

	def b017(self):
		'''
		

		'''
		pass

	def b018(self):
		'''
		

		'''
		pass

	def b019(self):
		'''
		

		'''
		pass

	def b020(self):
		'''
		

		'''
		pass

	def b021(self):
		'''
		Template Selected

		'''
		sel = [s for s in rt.getCurrentSelection()]

		for obj in sel:
			if obj.isFrozen == True:
				obj.isFrozen = False
			else:
				obj.isFrozen = True

	def b022(self):
		'''
		

		'''
		pass

	def b023(self):
		'''
		

		'''
		pass

	def b024(self):
		'''
		Polygon Display Options

		'''
		mel.eval("CustomPolygonDisplayOptions")
		# mel.eval("polysDisplaySetup 1;")






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------


	# def cmb000(self):
	# 	'''
	# 	Display

	# 	'''
	# 	cmb = self.hotBox.ui.cmb000
	# 	index = cmb.currentIndex() #get current index before refreshing list
	# 	list_ = [
	# 	'Toggle visibility', 
	# 	'Hide Selected',
	# 	'Show Selected',
	# 	'Show Geometry',
	# 	'XRay Selected',
	# 	'Un-XRay All',
	# 	'XRay Other',
	# 	'Filter Objects',
	# 	'Toggle Component ID Display',
	# 	'Wireframe Non-Active',
	# 	'Template selected',
	# 	]
	# 	self.comboBox (cmb, list_, "Display")

	# 	if index!=0:
	# 		if index==1: #Toggle visibility
	# 			sel = [s for s in rt.getCurrentSelection()]

	# 			for obj in sel:
	# 				if obj.visibility == True:
	# 					obj.visibility = False
	# 				else:
	# 					obj.visibility = True

	# 		if index==2: #Hide Selected
	# 			sel = [s for s in rt.getCurrentSelection()]
	
	# 			for obj in sel:
	# 				if not obj.isHiddenInVpt:
	# 					obj.isHidden = True

	# 		if index==3: #Show selected
	# 			sel = [s for s in rt.getCurrentSelection()]
	
	# 			for obj in sel:
	# 				if obj.isHiddenInVpt:
	# 					obj.isHidden = False

	# 		if index==4: #Show Geometry
	# 			geometry = rt.geometry

	# 			for obj in geometry:
	# 				if obj.isHiddenInVpt:
	# 					obj.isHidden = False

	# 		if index==5: #Xray selected
	# 			sel = [s for s in rt.getCurrentSelection()]

	# 			for s in sel:
	# 				s.xray = True

	# 		if index==6: #Un-Xray all
	# 			geometry = [g for g in rt.geometry]

	# 			for g in geometry:
	# 				g.xray = False

	# 		if index==7: #Xray other
	# 			sel = [s for s in rt.getCurrentSelection()]

	# 			geometry = [g for g in rt.geometry]

	# 			for g in geometry:
	# 				if g not in sel:
	# 					g.xray = True

	# 		if index==8: #Filter objects
	# 			pass

	# 		if index==9: #toggle component ID display
	# 			index = self.cycle('componentID_01234')

	# 			visible = pm.polyOptions (query=1, displayItemNumbers=1)
	# 			dinArray = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

	# 			if index == 4:
	# 				i=0
	# 				for _ in range(4):
	# 					if visible[i] == True:
	# 						pm.polyOptions (relative=1, displayItemNumbers=dinArray[i], activeObjects=1)
	# 					i+=1

	# 			if visible[index] != True and index != 4:
	# 				pm.polyOptions (relative=1, displayItemNumbers=dinArray[index], activeObjects=1)

	# 				i=0
	# 				for _ in range(4):
	# 					if visible[i] == True and i != index:
	# 						pm.polyOptions (relative=1, displayItemNumbers=dinArray[i], activeObjects=1)
	# 					i+=1

	# 			if index == 0:
	# 				self.viewPortMessage("[1,0,0,0] <hl>vertIDs</hl>.")
	# 			if index == 1:
	# 				self.viewPortMessage("[0,1,0,0] <hl>edgeIDs</hl>.")
	# 			if index == 2:
	# 				self.viewPortMessage("[0,0,1,0] <hl>faceIDs</hl>.")
	# 			if index == 3:
	# 				self.viewPortMessage("[0,0,0,1] <hl>compIDs(UV)</hl>.")
	# 			if index == 4:
	# 				self.viewPortMessage("component ID <hl>Off</hl>.")

	# 		if index==10: #wireframe non active (wireframe all but the selected item)
	# 			viewport = rt.viewport.activeViewport

	# 			state = self.cycle('wireframeInactive_01')

	# 			if state:
	# 				if not rt.viewport.isWire():
	# 					self.maxUiSetChecked("415", 62, 163, True) #set viewport to wireframe
	# 				self.maxUiSetChecked("40212", 62, 130, True) #Shade selected objects Checked
	# 			else:
	# 				self.maxUiSetChecked("40212", 62, 130, False) #Shade selected objects unchecked

	# 		if index==11: #Template selected
	# 			sel = [s for s in rt.getCurrentSelection()]

	# 			for obj in sel:
	# 				if obj.isFrozen == True:
	# 					obj.isFrozen = False
	# 				else:
	# 					obj.isFrozen = True

	# 		if index==12:
	# 			pass

	# 		if index==13:
	# 			pass

	# 		if index==14:
	# 			pass

	# 		if index==15:
	# 			pass

	# 		cmb.setCurrentIndex(0)



	# def cmb001(self):
	# 	'''
	# 	Recent Commands

	# 	'''
	# 	cmb = self.hotBox.ui.cmb001
	# 	index = cmb.currentIndex() #get current index before refreshing list
	# 	list_ = self.hotBox.sb.prevCommand(methodList=1) #ie. get the list of previous command methods
	# 	self.comboBox (cmb, list_, "Recent")

	# 	if index!=0:
	# 		print self.hotBox.sb.prevCommand(docString=1)[index] #prevCommand docString
	# 		self.hotBox.sb.prevCommand(methodList=1)[index]() #execute command at index
	# 		cmb.setCurrentIndex(0)