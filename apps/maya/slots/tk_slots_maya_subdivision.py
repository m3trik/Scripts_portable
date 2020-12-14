from __future__ import print_function
from tk_slots_maya_init import *

import traceback
import os.path


class Subdivision(Init):
	def __init__(self, *args, **kwargs):
		super(Subdivision, self).__init__(*args, **kwargs)


	def d000(self, state=None):
		'''
		Context menu
		'''
		d000 = self.subdivision.d000

		if state is 'setMenu':
			d000.contextMenu.add(widgets.TkComboBox, setObjectName='cmb000', setToolTip='Maya Subdivision Editiors.')
			d000.contextMenu.add(widgets.TkComboBox, setObjectName='cmb002', setToolTip='Maya Subdivision Operations.')
			d000.contextMenu.add(widgets.TkComboBox, setObjectName='cmb001', setToolTip='Smooth Proxy.')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.subdivision.cmb000

		if index is 'setMenu':
			list_ = ['Polygon Display Options']
			cmb.addItems_(list_, 'Subdivision Editiors')
			return

		if index>0:
			if index==cmb.items.index('Polygon Display Options'):
				pm.mel.CustomPolygonDisplayOptions() #Polygon Display Options #mel.eval("polysDisplaySetup 1;")
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Smooth Proxy
		'''
		cmb = self.subdivision.cmb001
		
		if index is 'setMenu':
			list_ = ['Create Subdiv Proxy','Remove Subdiv Proxy Mirror','Crease Tool','Toggle Subdiv Proxy Display', 'Both Proxy and Subdiv Display']
			cmb.addItems_(list_, 'Smooth Proxy')
			return

		if index>0:
			if index==cmb.items.index('Create Subdiv Proxy'):
				pm.mel.SmoothProxyOptions() #'Add polygons to the selected proxy objects.' #performSmoothProxy 1;
			elif index==cmb.items.index('Remove Subdiv Proxy Mirror'):
				pm.mel.UnmirrorSmoothProxyOptions() #'Create a single low resolution mesh for a mirrored proxy setup.' #performUnmirrorSmoothProxy 1;
			elif index==cmb.items.index('Crease Tool'):
				pm.mel.polyCreaseProperties() #'Harden or soften the edges of a smooth mesh preview.' #polyCreaseValues polyCreaseContext;
			elif index==cmb.items.index('Toggle Subdiv Proxy Display'):
				pm.mel.SmoothingDisplayToggle()	#'Toggle the display of smooth shapes.' #smoothingDisplayToggle 1;
			elif index==cmb.items.index('Both Proxy and Subdiv Display'):
				pm.mel.SmoothingDisplayShowBoth() #'Display both smooth shapes' #smoothingDisplayToggle 0;
			cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Maya Subdivision Operations
		'''
		cmb = self.subdivision.cmb002

		if index is 'setMenu':
			list_ = ['Reduce Polygons','Add Divisions','Smooth']
			cmb.addItems_(list_, 'Maya Subdivision Operations')
			return

		if index>0:
			if index is cmb.items.index('Reduce Polygons'):
				pm.mel.ReducePolygonOptions()
			elif index is cmb.items.index('Add Divisions'):
				pm.mel.SubdividePolygonOptions()
			elif index is cmb.items.index('Smooth'):
				pm.mel.performPolySmooth(1)
			cmb.setCurrentIndex(0)


	def s000(self, value=None):
		'''
		Division Level
		'''
		value = self.subdivision.s000.value()

		shapes = pm.ls(sl=1, dag=1, leaf=1)
		transforms = pm.listRelatives(shapes, p=True)
		for obj in transforms:
			if hasattr(obj, 'smoothLevel'):
				self.setAttributesMEL(obj, {'smoothLevel':value})
				pm.optionVar(intValue=['proxyDivisions', 1]) #subDiv proxy options: 'divisions'
				print(obj+': Division Level: <hl>'+str(value)+'</hl>')


	def s001(self, value=None):
		'''
		Tesselation Level
		'''
		value = self.subdivision.s001.value()

		shapes = pm.ls(sl=1, dag=1, leaf=1)
		transforms = pm.listRelatives(shapes, p=True)
		for obj in transforms:
			if hasattr(obj, 'smoothLevel'):
				self.setAttributesMEL(obj, {'smoothTessLevel':value})
				print(obj+': Tesselation Level: <hl>'+str(value)+'</hl>')


	def b004(self):
		'''
		Poly Reduce
		'''
		pm.mel.polyReduce(version=1, keepCreaseEdgeWeight=1)


	def b005(self):
		'''
		Reduce
		'''
		pm.mel.ReducePolygon()


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
		pm.mel.SubdividePolygon()

	def b009(self):
		'''
		Smooth

		'''
		pm.mel.SmoothPolygon()

	def b010(self):
		'''
		
		'''
		pass

	def b011(self):
		'''
		Apply Smooth Preview

		'''
		pm.mel.performSmoothMeshPreviewToPolygon() #convert smooth mesh preview to polygons


	@staticmethod
	def smoothProxy():
		'''
		Subdiv Proxy
		'''
		global polySmoothBaseMesh
		polySmoothBaseMesh=[]
		#disable creating seperate layers for subdiv proxy
		pm.optionVar (intValue=["polySmoothLoInLayer",0])
		pm.optionVar (intValue=["polySmoothHiInLayer",0])
		#query smooth proxy state.
		sel = pm.mel.polyCheckSelection("polySmoothProxy", "o", 0) #mel.eval("polyCheckSelection \"polySmoothProxy\" \"o\" 0")
		
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
		attachedSmoothProxies = pm.listConnections(shape[0], type="polySmoothProxy", s=0, d=1)
		if len(attachedSmoothProxies) != 0: #subdiv off
			pm.mel.smoothingDisplayToggle(0)

		#toggle performSmoothProxy
		pm.mel.performSmoothProxy(0) #toggle SubDiv Proxy;









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------
	#b012

