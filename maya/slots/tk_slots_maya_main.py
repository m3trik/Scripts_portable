import maya.mel as mel
import pymel.core as pm

from PySide2 import QtWidgets

import os.path

from tk_slots_maya_init import Init



class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('main')






	def cmb000(self):
		'''
		Menu Set
		'''
		cmb = self.ui.cmb000
		
		list_ = ['Modeling', 'Normals', 'Materials', 'UV']
		contents = self.comboBox(cmb, list_, 'Menu Sets')

		index = cmb.currentIndex()
		buttons = self.getObject(self.sb.getUi('main'), 'v000-11')
		for i, button in enumerate(buttons):
			if index==1:
				button.setText(['Extrude','Bridge','Cut','Slice','Delete','Collapse','Insert Loop','Select Loop','Detach','Attach','Chamfer','Target Weld'][i])

			if index==2:
				button.setText(['','','','','','','','','','','',''][i])

			if index==3:
				button.setText(['','','','','','','','','','','',''][i])

			if index==4:
				button.setText(['','','','','','','','','','','',''][i])


	def cmb001(self):
		'''
		Convert To
		'''
		cmb = self.ui.cmb001

		list_ = ['NURBS to Polygons', 'NURBS to Subdiv', 'Polygons to Subdiv', 'Smooth Mesh Preview to Polygons', 'Polygon Edges to Curve', 'Type to Curves', 'Subdiv to Polygons', 'Subdiv to NURBS', 'NURBS Curve to Bezier', 'Bezier Curve to NURBS', 'Paint Effects to NURBS', 'Paint Effects to Curves', 'Texture to Geometry', 'Displacement to Polygons', 'Displacement to Polygons with History', 'Fluid to Polygons', 'nParticle to Polygons', 'Instance to Object', 'Geometry to Bounding Box', 'Convert XGen Primitives to Polygons'] 

		contents = self.comboBox (cmb, list_, 'Convert To')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('NURBS to Polygons'): #
				mel.eval('performnurbsToPoly 0;')
			if index==contents.index('NURBS to Subdiv'): #
				mel.eval('performSubdivCreate 0;')
			if index==contents.index('Polygons to Subdiv'): #
				mel.eval('performSubdivCreate 0;')
			if index==contents.index('Smooth Mesh Preview to Polygons'): #
				mel.eval('performSmoothMeshPreviewToPolygon;')
			if index==contents.index('Polygon Edges to Curve'): #
				mel.eval('polyToCurve -form 2 -degree 3 -conformToSmoothMeshPreview 1;')
			if index==contents.index('Type to Curves'): #
				mel.eval('convertTypeCapsToCurves;')
			if index==contents.index('Subdiv to Polygons'): #
				mel.eval('performSubdivTessellate  false;')
			if index==contents.index('Subdiv to NURBS'): #
				mel.eval('performSubdToNurbs 0;')
			if index==contents.index('NURBS Curve to Bezier'): #
				mel.eval('nurbsCurveToBezier;')
			if index==contents.index('Bezier Curve to NURBS'): #
				mel.eval('bezierCurveToNurbs;')
			if index==contents.index('Paint Effects to NURBS'): #
				mel.eval('performPaintEffectsToNurbs  false;')
			if index==contents.index('Paint Effects to Curves'): #
				mel.eval('performPaintEffectsToCurve  false;')
			if index==contents.index('Texture to Geometry'): #
				mel.eval('performTextureToGeom 0;')
			if index==contents.index('Displacement to Polygons'): #
				mel.eval('displacementToPoly;')
			if index==contents.index('Displacement to Polygons with History'): #
				mel.eval('setupAnimatedDisplacement;')
			if index==contents.index('Fluid to Polygons'): #
				mel.eval('fluidToPoly;')
			if index==contents.index('nParticle to Polygons'): #
				mel.eval('particleToPoly;')
			if index==contents.index('Instance to Object'): #
				mel.eval('convertInstanceToObject;')
			if index==contents.index('Geometry to Bounding Box'): #
				mel.eval('performGeomToBBox 0;')
			if index==contents.index('Convert XGen Primitives to Polygons'): #
				import xgenm.xmaya.xgmConvertPrimToPolygon as cpp
				cpp.convertPrimToPolygon(False)

			cmb.setCurrentIndex(0)


	def v000(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b006', 'polygons')()
		

	def v001(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b005', 'polygons')()


	def v002(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b012', 'polygons')()
			self.hotBox.hide()


	def v003(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b004', 'polygons')()


	def v004(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b007', 'edit')() #delete


	def v005(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b009', 'polygons')()


	def v006(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b047', 'polygons')()


	def v007(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b008', 'selection')()


	def v008(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b044', 'polygons')()


	def v009(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b022', 'polygons')()


	def v010(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b007', 'polygons')()


	def v011(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b043', 'polygons')()


	def v012(self):
		'''
		
		'''
		pass


	def v013(self):
		'''
		Minimize Main Application

		'''
		# index = 'Minimize'
		# self.ui.v008.setText(index)

		self.getMethod('b005', 'file')()


	def v022(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b006', 'selection')() #select similar


	def v023(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('b007', 'selection')() #select island


	def v024(self):
		'''
		Recent Command: 1
		'''
		self.sb.prevCommand(method=1, as_list=1)[-1]() #execute command at index


	def v025(self):
		'''
		Recent Command: 2
		'''
		self.sb.prevCommand(method=1, as_list=1)[-2]() #execute command at index
			

	def v026(self):
		'''
		Recent Command: 3
		'''
		self.sb.prevCommand(method=1, as_list=1)[-3]() #execute command at index


	def v027(self):
		'''
		Recent Command: 4
		'''
		self.sb.prevCommand(method=1, as_list=1)[-4]() #execute command at index


	def v028(self):
		'''
		Recent Command: 5
		'''
		self.sb.prevCommand(method=1, as_list=1)[-5]() #execute command at index


	def v029(self):
		'''
		Recent Command: 6
		'''
		self.sb.prevCommand(method=1, as_list=1)[-6]() #execute command at index











#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------