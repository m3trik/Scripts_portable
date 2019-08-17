import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Nurbs(Init):
	def __init__(self, *args, **kwargs):
		super(Nurbs, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('nurbs')

		self.ui.progressBar.hide()




	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['Project Curve','Duplicate Curve','Create Curve from Poly','Bend Curve', 'Curl Curve','Modify Curve Curvature','Smooth Curve','Straighten Curves','Extrude Curves','Revolve Curves','Loft Curves','Planar Curves','Insert Isoparms','Insert Knot','Rebuild Curve','Extend Curve']
		contents = self.comboBox (cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Project Curve'):
				mel.eval("ProjectCurveOnSurfaceOptions;")
			if index==contents.index('Duplicate Curve'):
				mel.eval("DuplicateCurveOptions;")
			if index==contents.index('Create Curve from Poly'):
				mel.eval("CreateCurveFromPolyOptions")
			if index==contents.index('Bend Curve'):
				mel.eval("BendCurvesOptions;")
			if index==contents.index('Curl Curve'):
				mel.eval("CurlCurvesOptions;")
			if index==contents.index('Modify Curve Curvature'):
				mel.eval("ScaleCurvatureOptions;")
			if index==contents.index('Smooth Curve'):
				mel.eval("SmoothHairCurvesOptions;")
			if index==contents.index('Straighten Curves'):
				mel.eval("StraightenCurvesOptions;")
			if index==contents.index('Extrude Curves'):
				mel.eval("ExtrudeOptions;")
			if index==contents.index('Revolve Curves'):
				mel.eval("RevolveOptions;")
			if index==contents.index('Loft Curves'):
				mel.eval("LoftOptions;")
			if index==contents.index('Planar Curves'):
				mel.eval("PlanarOptions;")
			if index==contents.index('Insert Isoparms'):
				mel.eval("InsertIsoparmsOptions;")
			if index==contents.index('Insert Knot'):
				mel.eval("InsertKnotOptions;")
			if index==contents.index('Rebuild Curve'):
				mel.eval("RebuildCurveOptions;")
			if index==contents.index('Extend Curve'):
				mel.eval("ExtendCurveOptions;")
			if index==contents.index('Extend Curve On Surface'):
				mel.eval("ExtendCurveOnSurfaceOptions;")
			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		Create: Curve
		'''
		cmb = self.ui.cmb001
		
		files = ['Ep Curve Tool','CV Curve Tool','Bezier Curve Tool','Pencil Curve Tool','2 Point Circular Arc','3 Point Circular Arc']
		contents = self.comboBox(cmb, files, 'Create Curve')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Ep Curve Tool'):
				mel.eval('EPCurveToolOptions;') #mel.eval('EPCurveTool;')
			if index==contents.index('CV Curve Tool'):
				mel.eval('CVCurveToolOptions') #mel.eval('CVCurveTool')
			if index==contents.index('Bezier Curve Tool'):
				mel.eval('CreateBezierCurveToolOptions') #mel.eval('CreateBezierCurveTool;')
			if index==contents.index('Pencil Curve Tool'):
				mel.eval('PencilCurveToolOptions;') #mel.eval('PencilCurveTool;')
			if index==contents.index('2 Point Circular Arc'):
				mel.eval('TwoPointArcToolOptions;') #mel.eval("TwoPointArcTool;")
			if index==contents.index('3 Point Circular Arc'):
				mel.eval("ThreePointArcToolOptions;") #mel.eval("ThreePointArcTool;")
			cmb.setCurrentIndex(0)


	def b012(self):
		'''
		Project Curve
		'''
		mel.eval("projectCurve;") #ProjectCurveOnMesh;


	def b013(self):
		'''
		
		'''
		pass


	def b014(self):
		'''
		Duplicate Curve
		'''
		mel.eval("DuplicateCurve;")


	def b015(self):
		'''
		
		'''
		pass


	def b016(self):
		'''
		Extract Curve
		'''
		mel.eval("CreateCurveFromPoly")


	def b017(self):
		'''

		'''
		pass


	def b018(self):
		'''
		Lock Curve
		'''
		mel.eval("LockCurveLength;")


	def b019(self):
		'''
		Unlock Curve
		'''
		mel.eval("UnlockCurveLength;")


	def b020(self):
		'''
		Bend Curve
		'''
		mel.eval("BendCurves;")


	def b021(self):
		'''
		
		'''
		pass


	def b022(self):
		'''
		Curl Curve
		'''
		mel.eval("CurlCurves;")


	def b023(self):
		'''
		
		'''
		pass


	def b024(self):
		'''
		Modify Curve Curvature
		'''
		mel.eval("ScaleCurvature;")

	def b025(self):
		'''

		'''
		pass


	def b026(self):
		'''
		Smooth Curve
		'''
		mel.eval("SmoothHairCurves;")


	def b027(self):
		'''
		
		'''
		pass


	def b028(self):
		'''
		Straighten Curve

		'''
		mel.eval("StraightenCurves;")


	def b029(self):
		'''
		
		'''
		pass


	def b030(self):
		'''
		Extrude

		'''
		mel.eval("Extrude;")


	def b031(self):
		'''
		
		'''
		pass


	def b032(self):
		'''
		Revolve
		'''
		mel.eval("Revolve;")


	def b033(self):
		'''
		
		'''
		pass


	def b034(self):
		'''
		Loft
		'''
		mel.eval("loft")


	def b035(self):
		'''
		
		'''
		pass


	def b036(self):
		'''
		Planar
		'''
		mel.eval("Planar;")


	def b037(self):
		'''
		
		'''
		pass


	def b038(self):
		'''
		Insert Isoparm
		'''
		mel.eval("InsertIsoparms;")


	def b039(self):
		'''
		
		'''
		pass


	def b040(self):
		'''
		Edit Curve Tool
		'''
		mel.eval("CurveEditTool;")


	def b041(self):
		'''
		Attach Curve
		'''
		mel.eval("AttachCurveOptions;")


	def b042(self):
		'''
		Detach Curve
		'''
		mel.eval("DetachCurve;")


	def b043(self):
		'''
		Extend Curve
		'''
		mel.eval("ExtendCurveOptions;")


	def b044(self):
		'''
		
		'''
		mel.eval("")


	def b045(self):
		'''
		Cut Curve
		'''
		mel.eval("CutCurve;")


	def b046(self):
		'''
		Open/Close Curve
		'''
		mel.eval("OpenCloseCurve;")


	def b047(self):
		'''
		Insert Knot
		'''
		mel.eval("InsertKnot;")


	def b048(self):
		'''
		
		'''
		pass


	def b049(self):
		'''
		Add Points Tool
		'''
		mel.eval("AddPointsTool;")


	def b050(self):
		'''
		
		'''
		pass


	def b051(self):
		'''
		Reverse Curve

		'''
		mel.eval("reverse;")


	def b052(self):
		'''
		Extend Curve
		'''
		mel.eval("ExtendCurve;")


	def b053(self):
		'''
		
		'''
		pass


	def b054(self):
		'''
		Extend On Surface
		'''
		mel.eval("ExtendCurveOnSurface;")


	def b055(self):
		'''
		
		'''
		pass



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------