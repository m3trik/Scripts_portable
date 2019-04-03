import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Nurbs(Init):
	def __init__(self, *args, **kwargs):
		super(Nurbs, self).__init__(*args, **kwargs)


		

	def b000(self):
		'''
		Ep Curve Tool

		'''
		mel.eval('EPCurveTool;')

	def b001(self):
		'''
		Ep Curve Tool Options

		'''
		mel.eval('EPCurveToolOptions;')

	def b002(self):
		'''
		Bezier Curve Tool

		'''
		mel.eval('CreateBezierCurveTool;')

	def b003(self):
		'''
		Bezier Curve Tool Options

		'''
		mel.eval('CreateBezierCurveToolOptions')

	def b004(self):
		'''
		Cv Curve Tool

		'''
		mel.eval('CVCurveTool')

	def b005(self):
		'''
		Cv Curve Tool Options

		'''
		mel.eval('CVCurveToolOptions')

	def b006(self):
		'''
		Pencil Curve Tool

		'''
		mel.eval('PencilCurveTool;')

	def b007(self):
		'''
		Pencil Curve Tool Options

		'''
		mel.eval('PencilCurveToolOptions;')

	def b008(self):
		'''
		2 Point Circular Arc

		'''
		mel.eval("TwoPointArcTool;")

	def b009(self):
		'''
		2 Point Circular Arc Options

		'''
		mel.eval('TwoPointArcToolOptions;')

	def b010(self):
		'''
		3 Point Circular Arc

		'''
		mel.eval("ThreePointArcTool;")

	def b011(self):
		'''
		3 Point Circular Arc Options

		'''
		mel.eval("ThreePointArcToolOptions;")

	def b012(self):
		'''
		Project Curve

		'''
		mel.eval("projectCurve;") #ProjectCurveOnMesh;

	def b013(self):
		'''
		Project Curve Options

		'''
		mel.eval("ProjectCurveOnSurfaceOptions;")

	def b014(self):
		'''
		Duplicate Curve

		'''
		mel.eval("DuplicateCurve;")

	def b015(self):
		'''
		Duplicate Curve Options

		'''
		mel.eval("DuplicateCurveOptions;")

	def b016(self):
		'''
		Extract Curve

		'''
		mel.eval("CreateCurveFromPoly")

	def b017(self):
		'''
		Extract Curve Options

		'''
		mel.eval("CreateCurveFromPolyOptions")

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
		Bend Curve Options

		'''
		mel.eval("BendCurvesOptions;")

	def b022(self):
		'''
		Curl Curve

		'''
		mel.eval("CurlCurves;")

	def b023(self):
		'''
		Curl Curve Options

		'''
		mel.eval("CurlCurvesOptions;")

	def b024(self):
		'''
		Modify Curve Curvature

		'''
		mel.eval("ScaleCurvature;")

	def b025(self):
		'''
		Modify Curve Curvature Options

		'''
		mel.eval("ScaleCurvatureOptions;")

	def b026(self):
		'''
		Smooth Curve

		'''
		mel.eval("SmoothHairCurves;")

	def b027(self):
		'''
		Smooth Curve Options

		'''
		mel.eval("SmoothHairCurvesOptions;")

	def b028(self):
		'''
		Straighten Curve

		'''
		mel.eval("StraightenCurves;")

	def b029(self):
		'''
		Straighten Curve Options

		'''
		mel.eval("StraightenCurvesOptions;")

	def b030(self):
		'''
		Extrude

		'''
		mel.eval("Extrude;")

	def b031(self):
		'''
		Extrude Options

		'''
		mel.eval("ExtrudeOptions;")

	def b032(self):
		'''
		Revolve

		'''
		mel.eval("Revolve;")

	def b033(self):
		'''
		Revolve Options

		'''
		mel.eval("RevolveOptions;")

	def b034(self):
		'''
		Loft

		'''
		mel.eval("loft")

	def b035(self):
		'''
		Loft Options

		'''
		mel.eval("LoftOptions;")

	def b036(self):
		'''
		Planar

		'''
		mel.eval("Planar;")

	def b037(self):
		'''
		Planar Options

		'''
		mel.eval("PlanarOptions;")

	def b038(self):
		'''
		Insert Isoparm

		'''
		mel.eval("InsertIsoparms;")

	def b039(self):
		'''
		Insert Isoparm Options

		'''
		mel.eval("InsertIsoparmsOptions;")

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
		Insert Knot Options

		'''
		mel.eval("InsertKnotOptions;")

	def b049(self):
		'''
		Add Points Tool

		'''
		mel.eval("AddPointsTool;")

	def b050(self):
		'''
		Rebuild Curve Options

		'''
		mel.eval("RebuildCurveOptions;")

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
		Extend Curve Options

		'''
		mel.eval("ExtendCurveOptions;")

	def b054(self):
		'''
		Extend On Surface

		'''
		mel.eval("ExtendCurveOnSurface;")

	def b055(self):
		'''
		Extend On Surface Options

		'''
		mel.eval("ExtendCurveOnSurfaceOptions;")



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------