import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Nurbs(Init):
	def __init__(self, *args, **kwargs):
		super(Nurbs, self).__init__(*args, **kwargs)


		

	def b000(self): #Ep curve tool
		maxEval('EPCurveTool;')

	def b001(self): #Ep curve tool options
		maxEval('EPCurveToolOptions;')

	def b002(self): #Bezier curve tool
		maxEval('CreateBezierCurveTool;')

	def b003(self): #Bezier curve tool options
		maxEval('CreateBezierCurveToolOptions')

	def b004(self): #Cv curve tool
		maxEval('CVCurveTool')

	def b005(self): #Cv curve tool options
		maxEval('CVCurveToolOptions')

	def b006(self): #Pencil curve tool
		maxEval('PencilCurveTool;')

	def b007(self): #Pencil curve tool options
		maxEval('PencilCurveToolOptions;')

	def b008(self): #2 point circular arc
		mel.eval("TwoPointArcTool;")

	def b009(self): #2 point circular arc options
		maxEval('TwoPointArcToolOptions;')

	def b010(self): #3 point circular arc
		mel.eval("ThreePointArcTool;")

	def b011(self): #3 point circular arc options
		mel.eval("ThreePointArcToolOptions;")

	def b012(self): #project curve
		mel.eval("projectCurve;") #ProjectCurveOnMesh;

	def b013(self): #project curve options
		mel.eval("ProjectCurveOnSurfaceOptions;")

	def b014(self): #duplicate curve
		mel.eval("DuplicateCurve;")

	def b015(self): #duplicate curve options
		mel.eval("DuplicateCurveOptions;")

	def b016(self): #extract curve
		mel.eval("CreateCurveFromPoly")

	def b017(self): #extract curve options
		mel.eval("CreateCurveFromPolyOptions")

	def b018(self): #Lock curve
		mel.eval("LockCurveLength;")

	def b019(self): #Unlock curve
		mel.eval("UnlockCurveLength;")

	def b020(self): #bend curve
		mel.eval("BendCurves;")

	def b021(self): #bend curve options
		mel.eval("BendCurvesOptions;")

	def b022(self): #curl curve
		mel.eval("CurlCurves;")

	def b023(self): #curl curve options
		mel.eval("CurlCurvesOptions;")

	def b024(self): #modify curve curvature
		mel.eval("ScaleCurvature;")

	def b025(self): #modify curve curvature options
		mel.eval("ScaleCurvatureOptions;")

	def b026(self): #Smooth curve
		mel.eval("SmoothHairCurves;")

	def b027(self): #Smooth curve options
		mel.eval("SmoothHairCurvesOptions;")

	def b028(self): #Straighten curve
		mel.eval("StraightenCurves;")

	def b029(self): #Straighten curve options
		mel.eval("StraightenCurvesOptions;")

	def b030(self): #Extrude
		mel.eval("Extrude;")

	def b031(self): #Extrude options
		mel.eval("ExtrudeOptions;")

	def b032(self): #Revolve
		mel.eval("Revolve;")

	def b033(self): #Revolve options
		mel.eval("RevolveOptions;")

	def b034(self): #Loft
		mel.eval("loft")

	def b035(self): #Loft options
		mel.eval("LoftOptions;")

	def b036(self): #Planar
		mel.eval("Planar;")

	def b037(self): #Planar options
		mel.eval("PlanarOptions;")

	def b038(self): #Insert isoparm
		mel.eval("InsertIsoparms;")

	def b039(self): #Insert isoparm options
		mel.eval("InsertIsoparmsOptions;")

	def b040(self): #Edit curve tool
		mel.eval("CurveEditTool;")

	def b041(self): #Attach curve
		mel.eval("AttachCurveOptions;")

	def b042(self): #Detach curve
		mel.eval("DetachCurve;")

	def b043(self): #Extend curve
		mel.eval("ExtendCurveOptions;")

	def b044(self): #
		mel.eval("")

	def b045(self): #Cut curve
		mel.eval("CutCurve;")

	def b046(self): #Open/Close curve
		mel.eval("OpenCloseCurve;")

	def b047(self): #Insert knot
		mel.eval("InsertKnot;")

	def b048(self): #Insert knot options
		mel.eval("InsertKnotOptions;")

	def b049(self): #Add points tool
		mel.eval("AddPointsTool;")

	def b050(self): #Rebuild curve options
		mel.eval("RebuildCurveOptions;")

	def b051(self): #Reverse curve
		mel.eval("reverse;")

	def b052(self): #Extend curve
		mel.eval("ExtendCurve;")

	def b053(self): #Extend curve options
		mel.eval("ExtendCurveOptions;")

	def b054(self): #Extend on surface
		mel.eval("ExtendCurveOnSurface;")

	def b055(self): #Extend on surface options
		mel.eval("ExtendCurveOnSurfaceOptions;")



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------