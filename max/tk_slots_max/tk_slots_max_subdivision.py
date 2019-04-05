import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Subdivision(Init):
	def __init__(self, *args, **kwargs):
		super(Subdivision, self).__init__(*args, **kwargs)

		#initialize the smooth preview groupbox
		self.ui.gb000.setText('TurboSmooth')
		self.ui.txt000.setText('Iterations:')
		self.ui.txt001.setText('RenderIters:')
		self.ui.s000.setValue(0)
		self.ui.s001.setValue(0)




	def s000(self):
		'''
		Division Level

		'''
		value = self.ui.s000.getValue()

		geometry = rt.selection

		for obj in geometry:
			try:
				obj.modifiers['TurboSmooth'].iterations = value
			except: pass

	def s001(self):
		'''
		Tesselation Level

		'''
		value = self.ui.s001.getValue()

		geometry = rt.selection

		for obj in geometry:
			try:
				obj.modifiers['TurboSmooth'].renderIterations = value
			except: pass


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
		Convert Smooth Preview

		'''
		 #convert smooth mesh preview to polygons
		 geometry = rt.selection

		if not len(geometry):
			geometry = rt.geometry

		for obj in geometry:
			try:
				renderIters = obj.modifiers['TurboSmooth'].renderIterations
				obj.modifiers['TurboSmooth'].iterations = renderIters
			except: pass




#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------
	#b012

