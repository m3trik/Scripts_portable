from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Nurbs(Init):
	def __init__(self, *args, **kwargs):
		super(Nurbs, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('nurbs')
		self.childUi = self.sb.getUi('nurbs_submenu')


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state is 'setMenu':
			pin.contextMenu.add(widgets.TkComboBox, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000

		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Create: Curve
		'''
		cmb = self.parentUi.cmb001

		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, 'Create Curve')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		mel.eval('')
		# 	cmb.setCurrentIndex(0)


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
		pass


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
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------