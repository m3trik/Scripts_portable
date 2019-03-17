import maya.mel as mel
import pymel.core as pm

import os.path
import traceback

from tk_slots_maya_init import Init




class Subdivision(Init):
	def __init__(self, *args, **kwargs):
		super(Subdivsion, self).__init__(*args, **kwargs)




	def chk000(self): #division level 1
		self.setAttributesOnSelected (attribute=".smoothLevel", value=1)
		pm.optionVar (intValue=["proxyDivisions",1]) #subDiv proxy options: 'divisions' 
		self.setButtons(self.hotBox.ui, unchecked='chk001,chk002,chk003,chk004')

	def chk001(self): #division level 2
		self.setAttributesOnSelected (attribute=".smoothLevel", value=2)
		pm.optionVar (intValue=["proxyDivisions",2]) #subDiv proxy options: 'divisions' 
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk002,chk003,chk004')

	def chk002(self): #division level 3
		self.setAttributesOnSelected (attribute=".smoothLevel", value=3)
		pm.optionVar (intValue=["proxyDivisions",3]) #subDiv proxy options: 'divisions' 
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk001,chk003,chk004')

	def chk003(self): #division level 4
		self.setAttributesOnSelected (attribute=".smoothLevel", value=4)
		pm.optionVar (intValue=["proxyDivisions",4]) #subDiv proxy options: 'divisions' 
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk001,chk002,chk004')

	def chk004(self): #division level 5
		self.setAttributesOnSelected (attribute=".smoothLevel", value=5)
		pm.optionVar (intValue=["proxyDivisions",5]) #subDiv proxy options: 'divisions'
		self.setButtons(self.hotBox.ui, unchecked='chk000,chk001,chk002,chk003')

	def chk005(self): #tessellation level 6
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=6)
		self.setButtons(self.hotBox.ui, unchecked='chk006,chk007,chk008,chk009')

	def chk006(self): #tessellation level 7
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=7)
		self.setButtons(self.hotBox.ui, unchecked='chk005,chk007,chk008,chk009')

	def chk007(self): #tessellation level 8
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=8)
		self.setButtons(self.hotBox.ui, unchecked='chk005,chk006,chk008,chk009')

	def chk008(self): #tessellation level 9
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=9)
		self.setButtons(self.hotBox.ui, unchecked='chk005,chk006,chk007,chk009')

	def chk009(self): #tessellation level 10
		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=10)
		self.setButtons(self.hotBox.ui, unchecked='chk005,chk006,chk007,chk008')


	def b000(self): #Toggle subdiv proxy display
		state = self.cycle('subdivProxy_110')
		try:
			mel.eval("smoothingDisplayToggle "+str(state))
		except:
			traceback.print_exc()
			print "// Warning: Nothing Selected\n"

	def b001(self): #Subdiv proxy
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

	def b002(self): #Subdiv proxy options
		mel.eval('performSmoothProxy 1;') #SubDiv Proxy Options;

	def b003(self): #polygon display options
		mel.eval("CustomPolygonDisplayOptions")
		# mel.eval("polysDisplaySetup 1;")

	def b004(self): #Poly reduce
		mel.eval("polyReduce -version 1 -keepCreaseEdgeWeight 1;")

	def b005(self): #Reduce
		mel.eval("ReducePolygon;")

	def b006(self): #Reduce options
		mel.eval("ReducePolygonOptions;")

	def b007(self): #Smooth options
		mel.eval("SmoothPolygonOptions;")

	def b008(self): #Add Divisions - subdivide mesh
		mel.eval('SubdividePolygon')

	def b009(self): #Smooth
		mel.eval('SmoothPolygon;')

	def b010(self): #add divisions options
		mel.eval("SubdividePolygonOptions")

	def b011(self): #Apply smooth preview
		mel.eval("performSmoothMeshPreviewToPolygon;") #convert smooth mesh preview to polygons




#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------
	#b012

