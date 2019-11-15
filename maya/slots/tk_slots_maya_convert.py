import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Convert(Init):
	def __init__(self, *args, **kwargs):
		super(Convert, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('convert')

		




	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = self.comboBox(cmb, files, ' ')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


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


	def b000(self):
		'''
		
		'''
		pass


	def b001(self):
		'''
		
		'''
		pass


	def b002(self):
		'''
		
		'''
		pass


	def b003(self):
		'''
		
		'''
		pass


	def b004(self):
		'''
		
		'''
		pass


	def b005(self):
		'''
		
		'''
		pass


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
		
		'''
		pass


	def b009(self):
		'''
		
		'''
		pass







#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------