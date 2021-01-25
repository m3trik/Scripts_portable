from __future__ import print_function
from builtins import super
import os.path

from tk_slots_max_init import **



class Nurbs(Init):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.nurbs_ui.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb000', setToolTip='Maya Curve Operations')
			return


	def cmb000(self, index=None):
		'''Maya Curve Operations
		'''
		cmb = self.nurbs_ui.cmb000

		if index is 'setMenu':
			list_ = ['Project Curve','Duplicate Curve','Create Curve from Poly','Bend Curve', 'Curl Curve','Modify Curve Curvature','Smooth Curve','Straighten Curves','Extrude Curves','Revolve Curves','Loft Curves','Planar Curves','Insert Isoparms','Insert Knot','Rebuild Curve','Extend Curve', 'Extend Curve On Surface']
			cmb.addItems_(list_, 'Maya Curve Operations')
			return

		if index>0:
			if index==cmb.items.index('Project Curve'):
				mel.eval("ProjectCurveOnSurfaceOptions;")
			elif index==cmb.items.index('Duplicate Curve'):
				mel.eval("DuplicateCurveOptions;")
			elif index==cmb.items.index('Create Curve from Poly'):
				mel.eval("CreateCurveFromPolyOptions")
			elif index==cmb.items.index('Bend Curve'):
				mel.eval("BendCurvesOptions;")
			elif index==cmb.items.index('Curl Curve'):
				mel.eval("CurlCurvesOptions;")
			elif index==cmb.items.index('Modify Curve Curvature'):
				mel.eval("ScaleCurvatureOptions;")
			elif index==cmb.items.index('Smooth Curve'):
				mel.eval("SmoothHairCurvesOptions;")
			elif index==cmb.items.index('Straighten Curves'):
				mel.eval("StraightenCurvesOptions;")
			elif index==cmb.items.index('Extrude Curves'):
				mel.eval("ExtrudeOptions;")
			elif index==cmb.items.index('Revolve Curves'):
				mel.eval("RevolveOptions;")
			elif index==cmb.items.index('Loft Curves'):
				mel.eval("LoftOptions;")
			elif index==cmb.items.index('Planar Curves'):
				mel.eval("PlanarOptions;")
			elif index==cmb.items.index('Insert Isoparms'):
				mel.eval("InsertIsoparmsOptions;")
			elif index==cmb.items.index('Insert Knot'):
				mel.eval("InsertKnotOptions;")
			elif index==cmb.items.index('Rebuild Curve'):
				mel.eval("RebuildCurveOptions;")
			elif index==cmb.items.index('Extend Curve'):
				mel.eval("ExtendCurveOptions;")
			elif index==cmb.items.index('Extend Curve On Surface'):
				mel.eval("ExtendCurveOnSurfaceOptions;")
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''Create: Curve
		'''
		cmb = self.nurbs_ui.cmb001

		if index is 'setMenu':
			list_ = ['Ep Curve Tool','CV Curve Tool','Bezier Curve Tool','Pencil Curve Tool','2 Point Circular Arc','3 Point Circular Arc']
			cmb.addItems_(list_, 'Create Curve')
			return

		if index>0:
			if index==cmb.items.index('Ep Curve Tool'):
				mel.eval('EPCurveToolOptions;') #mel.eval('EPCurveTool;')
			elif index==cmb.items.index('CV Curve Tool'):
				mel.eval('CVCurveToolOptions') #mel.eval('CVCurveTool')
			elif index==cmb.items.index('Bezier Curve Tool'):
				mel.eval('CreateBezierCurveToolOptions') #mel.eval('CreateBezierCurveTool;')
			elif index==cmb.items.index('Pencil Curve Tool'):
				mel.eval('PencilCurveToolOptions;') #mel.eval('PencilCurveTool;')
			elif index==cmb.items.index('2 Point Circular Arc'):
				mel.eval('TwoPointArcToolOptions;') #mel.eval("TwoPointArcTool;")
			elif index==cmb.items.index('3 Point Circular Arc'):
				mel.eval("ThreePointArcToolOptions;") #mel.eval("ThreePointArcTool;")
			cmb.setCurrentIndex(0)


	@Init.attr
	def tb000(self, state=None):
		'''Revolve
		'''
		tb = self.nurbs_ui.tb000
		if state is 'setMenu':
			tb.menu_.add('QSpinBox', setText='Degree', setObjectName='s002', setValue=3, setToolTip='The degree of the resulting surface.')
			tb.menu_.add('QSpinBox', setText='Start Sweep', setObjectName='s003', setValue=3, setMinMax_='0-360step1', setToolTip='	The value for the start sweep angle.')
			tb.menu_.add('QSpinBox', setText='End Sweep', setObjectName='s004', setValue=3, setMinMax_='0-360step1', setToolTip='The value for the end sweep angle.')
			tb.menu_.add('QSpinBox', setText='Sections', setObjectName='s005', setValue=8, setToolTip='The number of surface spans between consecutive curves in the loft.')
			tb.menu_.add('QCheckBox', setText='Range', setObjectName='chk006', setChecked=False, setToolTip='Force a curve range on complete input curve.')
			tb.menu_.add('QCheckBox', setText='Polygon', setObjectName='chk007', setChecked=True, setToolTip='The object created by this operation.')
			tb.menu_.add('QCheckBox', setText='Auto Correct Normal', setObjectName='chk008', setChecked=False, setToolTip='Attempt to reverse the direction of the axis in case it is necessary to do so for the surface normals to end up pointing to the outside of the object.')
			tb.menu_.add('QCheckBox', setText='Use Tolerance', setObjectName='chk009', setChecked=False, setToolTip='Use the tolerance, or the number of sections to control the sections.')
			tb.menu_.add('QDoubleSpinBox', setText='Tolerance', setObjectName='s006', setValue=0.001, setMinMax_='0-9999step.001', setToolTip='Tolerance to build to (if useTolerance attribute is set).')
			return

		degree = tb.menu_.s002.value()
		startSweep = tb.menu_.s003.value()
		endSweep = tb.menu_.s004.value()
		sections = tb.menu_.s005.value()
		range_ = tb.menu_.chk006.isChecked()
		polygon = 1 if tb.menu_.chk007.isChecked() else 0
		autoCorrectNormal = tb.menu_.chk008.isChecked()
		useTolerance = tb.menu_.chk009.isChecked()
		tolerance = tb.menu_.s006.value()

		return pm.revolve(curves, po=polygon, rn=range_, ssw=startSweep, esw=endSweep, ut=useTolerance, tol=tolerance, degree=degree, s=sections, ulp=1, ax=[0,1,0])


	@Init.attr
	def tb001(self, state=None):
		'''Loft
		'''
		tb = self.nurbs_ui.tb001
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Uniform', setObjectName='chk000', setChecked=True, setToolTip='The resulting surface will have uniform parameterization in the loft direction. If set to false, the parameterization will be chord length.')
			tb.menu_.add('QCheckBox', setText='Close', setObjectName='chk001', setChecked=False, setToolTip='The resulting surface will be closed (periodic) with the start (end) at the first curve. If set to false, the surface will remain open.')
			tb.menu_.add('QSpinBox', setText='Degree', setObjectName='s000', setValue=3, setToolTip='The degree of the resulting surface.')
			tb.menu_.add('QCheckBox', setText='Auto Reverse', setObjectName='chk002', setChecked=False, setToolTip='The direction of the curves for the loft is computed automatically. If set to false, the values of the multi-use reverse flag are used instead.')
			tb.menu_.add('QSpinBox', setText='Section Spans', setObjectName='s001', setValue=1, setToolTip='The number of surface spans between consecutive curves in the loft.')
			tb.menu_.add('QCheckBox', setText='Range', setObjectName='chk003', setChecked=False, setToolTip='Force a curve range on complete input curve.')
			tb.menu_.add('QCheckBox', setText='Polygon', setObjectName='chk004', setChecked=True, setToolTip='The object created by this operation.')
			tb.menu_.add('QCheckBox', setText='Reverse Surface Normals', setObjectName='chk005', setChecked=False, setToolTip='The surface normals on the output NURBS surface will be reversed. This is accomplished by swapping the U and V parametric directions.')
			tb.menu_.add('QCheckBox', setText='Angle Loft Between Two Curves', setObjectName='chk010', setChecked=False, setToolTip='Perform a loft at an angle between two selected curves or polygon edges (that will be extracted as curves).')
			tb.menu_.add('QSpinBox', setText='Angle Loft: Spans', setObjectName='s007', setValue=6, setMinMax_='2-9999step1', setToolTip='Angle loft: Number of duplicated points (spans).')
			return

		uniform = tb.menu_.chk000.isChecked()
		close = tb.menu_.chk001.isChecked()
		degree = tb.menu_.s000.value()
		autoReverse = tb.menu_.chk002.isChecked()
		sectionSpans = tb.menu_.s001.value()
		range_ = tb.menu_.chk003.isChecked()
		polygon = 1 if tb.menu_.chk004.isChecked() else 0
		reverseSurfaceNormals = tb.menu_.chk005.isChecked()
		angleLoftBetweenTwoCurves = tb.menu_.chk010.isChecked()
		angleLoftSpans = tb.menu_.s007.value()

		if angleLoftBetweenTwoCurves:
			start, end = pm.ls(sl=1)[:2] #get the first two selected edge loops or curves.
			return Init.angleLoftBetweenTwoCurves(start, end, count=angleLoftSpans, cleanup=True, uniform=uniform, close=close, autoReverse=autoReverse, degree=degree, sectionSpans=sectionSpans, range=range_, polygon=polygon, reverseSurfaceNormals=reverseSurfaceNormals)

		return pm.loft(curves, u=uniform, c=close, ar=autoReverse, d=degree, ss=sectionSpans, rn=range_, po=polygon, rsn=reverseSurfaceNormals)


	def b012(self):
		'''Project Curve
		'''
		mel.eval("projectCurve;") #ProjectCurveOnMesh;


	def b014(self):
		'''Duplicate Curve
		'''
		pm.mel.DuplicateCurve()


	def b016(self):
		'''Extract Curve
		'''
		pm.mel.CreateCurveFromPoly()


	def b018(self):
		'''Lock Curve
		'''
		pm.mel.LockCurveLength()


	def b019(self):
		'''Unlock Curve
		'''
		pm.mel.UnlockCurveLength()


	def b020(self):
		'''Bend Curve
		'''
		pm.mel.BendCurves()


	def b022(self):
		'''Curl Curve
		'''
		pm.mel.CurlCurves()


	def b024(self):
		'''Modify Curve Curvature
		'''
		pm.mel.ScaleCurvature()


	def b026(self):
		'''Smooth Curve
		'''
		pm.mel.SmoothHairCurves()


	def b028(self):
		'''Straighten Curve

		'''
		pm.mel.StraightenCurves()


	def b030(self):
		'''Extrude

		'''
		pm.mel.Extrude()


	def b036(self):
		'''Planar
		'''
		pm.mel.Planar()


	def b038(self):
		'''Insert Isoparm
		'''
		pm.mel.InsertIsoparms()


	def b040(self):
		'''Edit Curve Tool
		'''
		pm.mel.CurveEditTool()


	def b041(self):
		'''Attach Curve
		'''
		pm.mel.AttachCurveOptions()


	def b042(self):
		'''Detach Curve
		'''
		pm.mel.DetachCurve()


	def b043(self):
		'''Extend Curve
		'''
		pm.mel.ExtendCurveOptions()


	def b045(self):
		'''Cut Curve
		'''
		pm.mel.CutCurve()


	def b046(self):
		'''Open/Close Curve
		'''
		pm.mel.OpenCloseCurve()


	def b047(self):
		'''Insert Knot
		'''
		pm.mel.InsertKnot()


	def b049(self):
		'''Add Points Tool
		'''
		pm.mel.AddPointsTool()


	def b051(self):
		'''Reverse Curve

		'''
		mel.eval("reverse;")


	def b052(self):
		'''Extend Curve
		'''
		pm.mel.ExtendCurve()


	def b054(self):
		'''Extend On Surface
		'''
		pm.mel.ExtendCurveOnSurface()









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------