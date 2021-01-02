from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Nurbs(Init):
	def __init__(self, *args, **kwargs):
		super(Nurbs, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('nurbs')
		self.childUi = self.sb.getUi('nurbs_submenu')


	def d000(self, state=None):
		'''Context menu
		'''
		d000 = self.parentUi.d000

		if state is 'setMenu':
			d000.contextMenu.add(widgets.TkComboBox, setObjectName='cmb000', setToolTip='Maya Curve Operations')

			return


	def cmb000(self, index=None):
		'''Maya Curve Operations
		'''
		cmb = self.parentUi.cmb000

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
		cmb = self.parentUi.cmb001

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


	def b012(self):
		'''Project Curve
		'''
		mel.eval("projectCurve;") #ProjectCurveOnMesh;


	def b013(self):
		''''''
		pass


	def b014(self):
		'''Duplicate Curve
		'''
		mel.eval("DuplicateCurve;")


	def b015(self):
		''''''
		pass


	def b016(self):
		'''Extract Curve
		'''
		mel.eval("CreateCurveFromPoly")


	def b017(self):
		''''''
		pass


	def b018(self):
		'''Lock Curve
		'''
		mel.eval("LockCurveLength;")


	def b019(self):
		'''Unlock Curve
		'''
		mel.eval("UnlockCurveLength;")


	def b020(self):
		'''Bend Curve
		'''
		mel.eval("BendCurves;")


	def b021(self):
		''''''
		pass


	def b022(self):
		'''Curl Curve
		'''
		mel.eval("CurlCurves;")


	def b023(self):
		''''''
		pass


	def b024(self):
		'''Modify Curve Curvature
		'''
		mel.eval("ScaleCurvature;")

	def b025(self):
		''''''
		pass


	def b026(self):
		'''Smooth Curve
		'''
		mel.eval("SmoothHairCurves;")


	def b027(self):
		''''''
		pass


	def b028(self):
		'''Straighten Curve

		'''
		mel.eval("StraightenCurves;")


	def b029(self):
		''''''
		pass


	def b030(self):
		'''Extrude

		'''
		mel.eval("Extrude;")


	def b031(self):
		''''''
		pass


	def b032(self):
		'''Revolve
		'''
		mel.eval("Revolve;")


	def b033(self):
		''''''
		pass


	def b034(self):
		'''Loft
		'''
		mel.eval("loft")


	def b035(self):
		''''''
		pass


	def b036(self):
		'''Planar
		'''
		mel.eval("Planar;")


	def b037(self):
		''''''
		pass


	def b038(self):
		'''Insert Isoparm
		'''
		mel.eval("InsertIsoparms;")


	def b039(self):
		''''''
		pass


	def b040(self):
		'''Edit Curve Tool
		'''
		mel.eval("CurveEditTool;")


	def b041(self):
		'''Attach Curve
		'''
		mel.eval("AttachCurveOptions;")


	def b042(self):
		'''Detach Curve
		'''
		mel.eval("DetachCurve;")


	def b043(self):
		'''Extend Curve
		'''
		mel.eval("ExtendCurveOptions;")


	def b044(self):
		''''''
		mel.eval("")


	def b045(self):
		'''Cut Curve
		'''
		mel.eval("CutCurve;")


	def b046(self):
		'''Open/Close Curve
		'''
		mel.eval("OpenCloseCurve;")


	def b047(self):
		'''Insert Knot
		'''
		mel.eval("InsertKnot;")


	def b048(self):
		''''''
		pass


	def b049(self):
		'''Add Points Tool
		'''
		mel.eval("AddPointsTool;")


	def b050(self):
		''''''
		pass


	def b051(self):
		'''Reverse Curve

		'''
		mel.eval("reverse;")


	def b052(self):
		'''Extend Curve
		'''
		mel.eval("ExtendCurve;")


	def b053(self):
		''''''
		pass


	def b054(self):
		'''Extend On Surface
		'''
		mel.eval("ExtendCurveOnSurface;")


	def b055(self):
		''''''
		pass



#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------