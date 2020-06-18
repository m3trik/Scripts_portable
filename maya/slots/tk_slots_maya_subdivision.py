from __future__ import print_function
from tk_slots_maya_init import *

import traceback
import os.path


class Subdivision(Init):
	def __init__(self, *args, **kwargs):
		super(Subdivision, self).__init__(*args, **kwargs)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya Subdivision Editiors')

			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000
		
		files = ['Reduce Polygons','Add Divisions','Smooth','SubDiv Proxy']
		contents = cmb.addItems_(files, 'Maya Subdivision Editiors')

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
		value = self.parentUi.s000.value()

		shapes = pm.ls(sl=1, dag=1, leaf=1)
		transforms = pm.listRelatives(shapes, p=True)
		for obj in transforms:
			if hasattr(obj, 'smoothLevel'):
				self.setAttributesMEL(obj, {'smoothLevel':value})
				pm.optionVar(intValue=['proxyDivisions', 1]) #subDiv proxy options: 'divisions'
				print(obj+': Division Level: <hl>'+str(value)+'</hl>')


	def s001(self):
		'''
		Tesselation Level
		'''
		value = self.parentUi.s001.value()

		shapes = pm.ls(sl=1, dag=1, leaf=1)
		transforms = pm.listRelatives(shapes, p=True)
		for obj in transforms:
			if hasattr(obj, 'smoothLevel'):
				self.setAttributesMEL(obj, {'smoothTessLevel':value})
				print(obj+': Tesselation Level: <hl>'+str(value)+'</hl>')


	@Slots.message
	def b000(self):
		'''
		Toggle Subdiv Proxy Display

		'''
		state = self.cycle([1,1,0], 'subdivProxy')
		try:
			mel.eval("smoothingDisplayToggle "+str(state))
		except:
			traceback.print_exc()
			return 'Error: Nothing Selected.'


	@Slots.message
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
			return 'Error: Nothing selected.'

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
			self.toggleWidgets(self.parentUi, self.childUi, setEnabled='b000', setChecked='b009')
		else:
			self.toggleWidgets(self.parentUi, self.childUi, setDisabled='b000', setUnChecked='b009')
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
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------
	#b012

