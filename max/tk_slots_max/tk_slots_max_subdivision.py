import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init




class Subdivision(Init):
	def __init__(self, *args, **kwargs):
		super(Subdivision, self).__init__(*args, **kwargs)




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

	def b002(self):
		'''
		Subdiv Proxy Options

		'''
		mel.eval('performSmoothProxy 1;') #SubDiv Proxy Options;

	def b003(self):
		'''
		Polygon Display Options

		'''
		mel.eval("CustomPolygonDisplayOptions")
		# mel.eval("polysDisplaySetup 1;")

	def b004(self):
		'''
		Poly Reduce

		'''
		mel.eval("polyReduce -version 1 -keepCreaseEdgeWeight 1;")

	def b005(self):
		'''
		Reduce

		'''
		mel.eval("ReducePolygon;")

	def b006(self):
		'''
		Reduce Options

		'''
		mel.eval("ReducePolygonOptions;")

	def b007(self):
		'''
		Smooth Options

		'''
		mel.eval("SmoothPolygonOptions;")

	def b008(self):
		'''
		Add Divisions - Subdivide Mesh

		'''
		maxEval('macros.run \"Modifiers\" \"Tessellate\"')

	def b009(self):
		'''
		Smooth

		'''
		maxEval('macros.run \"Modifiers\" \"Smooth\"')

	def b010(self):
		'''
		Add Divisions Options

		'''
		maxEval('''
		Try 
		(
			local A = modPanel.getCurrentObject()
			A.popupDialog #Tessellate
		)
		Catch ()
		''')

	def b011(self):
		'''
		Apply Smooth Preview

		'''
		mel.eval("performSmoothMeshPreviewToPolygon;") #convert smooth mesh preview to polygons




#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------
	#b012

