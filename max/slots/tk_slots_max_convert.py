import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Convert(Init):
	def __init__(self, *args, **kwargs):
		super(Convert, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('convert')

		




	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000

		files = ['']
		contents = self.comboBox(cmb, files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Convert To
		'''
		cmb = self.ui.cmb001

		list_ = ['NURBS to Polygons', 'NURBS to Subdiv', 'Polygons to Subdiv', 'Smooth Mesh Preview to Polygons', 'Polygon Edges to Curve', 'Type to Curves', 'Subdiv to Polygons', 'Subdiv to NURBS', 'NURBS Curve to Bezier', 'Bezier Curve to NURBS', 'Paint Effects to NURBS', 'Paint Effects to Curves', 'Texture to Geometry', 'Displacement to Polygons', 'Displacement to Polygons with History', 'Fluid to Polygons', 'nParticle to Polygons', 'Instance to Object', 'Geometry to Bounding Box', 'Convert XGen Primitives to Polygons'] 

		contents = self.comboBox (cmb, list_, 'Convert To')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('NURBS to Polygons'): #1
				mel.eval('performnurbsToPoly 0;')
			elif index==contents.index('NURBS to Subdiv'): #2
				mel.eval('performSubdivCreate 0;')
			elif index==contents.index('Polygons to Subdiv'): #3
				mel.eval('performSubdivCreate 0;')
			elif index==contents.index('Smooth Mesh Preview to Polygons'): #4
				mel.eval('performSmoothMeshPreviewToPolygon;')
			elif index==contents.index('Polygon Edges to Curve'): #5
				mel.eval('polyToCurve -form 2 -degree 3 -conformToSmoothMeshPreview 1;')
			elif index==contents.index('Type to Curves'): #6
				mel.eval('convertTypeCapsToCurves;')
			elif index==contents.index('Subdiv to Polygons'): #7
				mel.eval('performSubdivTessellate  false;')
			elif index==contents.index('Subdiv to NURBS'): #8
				mel.eval('performSubdToNurbs 0;')
			elif index==contents.index('NURBS Curve to Bezier'): #9
				mel.eval('nurbsCurveToBezier;')
			elif index==contents.index('Bezier Curve to NURBS'): #10
				mel.eval('bezierCurveToNurbs;')
			elif index==contents.index('Paint Effects to NURBS'): #11
				mel.eval('performPaintEffectsToNurbs  false;')
			elif index==contents.index('Paint Effects to Curves'): #12
				mel.eval('performPaintEffectsToCurve  false;')
			elif index==contents.index('Texture to Geometry'): #13
				mel.eval('performTextureToGeom 0;')
			elif index==contents.index('Displacement to Polygons'): #14
				mel.eval('displacementToPoly;')
			elif index==contents.index('Displacement to Polygons with History'): #15
				mel.eval('setupAnimatedDisplacement;')
			elif index==contents.index('Fluid to Polygons'): #16
				mel.eval('fluidToPoly;')
			elif index==contents.index('nParticle to Polygons'): #17
				mel.eval('particleToPoly;')
			elif index==contents.index('Instance to Object'): #18
				mel.eval('convertInstanceToObject;')
			elif index==contents.index('Geometry to Bounding Box'): #19
				mel.eval('performGeomToBBox 0;')
			elif index==contents.index('Convert XGen Primitives to Polygons'): #20
				import xgenm.xmaya.xgmConvertPrimToPolygon as cpp
				cpp.convertPrimToPolygon(False)

			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Polygon Edges to Curve
		'''
		self.cmb001(index=5)


	def b001(self):
		'''
		Instance to Object
		'''
		self.cmb001(index=18)


	def b002(self):
		'''
		NURBS to Polygons
		'''
		self.cmb001(index=1)


	def b003(self):
		'''
		Smooth Mesh Preview to Polygons
		'''
		self.cmb001(index=4)


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