import maya.mel as mel
import pymel.core as pm

import os.path
import traceback

from tk_slots_maya_init import Init




class Subdivision(Init):
	def __init__(self, *args, **kwargs):
		super(Subdivision, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('subdivision')



	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['Reduce Polygons','Add Divisions','Smooth','SubDiv Proxy']
		contents = self.comboBox (cmb, files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Reduce Polygons'):
				mel.eval("ReducePolygonOptions;")
			if index==contents.index('Add Divisions'):
				mel.eval("SubdividePolygonOptions")
			if index==contents.index('Smooth'):
				mel.eval("SmoothPolygonOptions;")
			if index==contents.index('SubDiv Proxy'):
				mel.eval('performSmoothProxy 1;') #SubDiv Proxy Options;
			cmb.setCurrentIndex(0)


	def s000(self):
		'''
		Division Level
		'''
		value = self.ui.s000.value()

		self.setAttributesOnSelected (attribute=".smoothLevel", value=value)
		pm.optionVar (intValue=["proxyDivisions",1]) #subDiv proxy options: 'divisions'


	def s001(self):
		'''
		Tesselation Level
		'''
		value = self.ui.s001.value()

		self.setAttributesOnSelected (attribute=".smoothTessLevel", value=value)


	def b000(self):
		'''
		Toggle Subdiv Proxy Display

		'''
		state = self.cycle([1,1,0], 'subdivProxy')
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
			self.setButtons(self.tk.ui, enable='b000', checked='b009')
		else:
			self.setButtons(self.tk.ui, disable='b000', unchecked='b009')
			mel.eval("smoothingDisplayToggle 0;")

		#toggle performSmoothProxy
		mel.eval("performSmoothProxy 0;") #toggle SubDiv Proxy;

	def b002(self):
		'''
		
		'''
		pass

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
		
		'''
		pass


	def b007(self):
		'''
		
		'''
		pass


	def b008(self):
		'''
		Add Divisions - Subdivide Mesh

		'''
		mel.eval('SubdividePolygon')

	def b009(self):
		'''
		Smooth

		'''
		mel.eval('SmoothPolygon;')

	def b010(self):
		'''
		
		'''
		pass

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

