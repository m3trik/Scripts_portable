from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Uv(Init):
	def __init__(self, *args, **kwargs):
		super(Uv, self).__init__(*args, **kwargs)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='3dsMax UV Editors')

			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000

		list_ = ["UV Editor", "UV Set Editor", "UV Tool Kit", "UV Linking: Texture-Centric", "UV Linking: UV-Centric", "UV Linking: Paint Effects/UV", "UV Linking: Hair/UV"]
		items = cmb.addItems_(list_, '3dsMax UV Editors')

		if not index:
			index = cmb.currentIndex()
		if index !=0: #hide hotbox then perform operation
			self.tk.hide()
			if index == 1: #UV Editor
				maxEval('TextureViewWindow;') 
			if index == 2: #UV Set Editor
				maxEval('uvSetEditor;')
			if index == 3: #UV Tool Kit
				maxEval('toggleUVToolkit;')
			if index == 4: #UV Linking: Texture-Centric
				maxEval('textureCentricUvLinkingEditor;')
			if index == 5: #UV Linking: UV-Centric
				maxEval('uvCentricUvLinkingEditor;')
			if index == 6: #UV Linking: Paint Effects/UV
				maxEval('pfxUVLinkingEditor;')
			if index == 7: #UV Linking: Hair/UV
				mel.evel('hairUVLinkingEditor;')
			self.parentUi.cmb000.setCurrentIndex(0)


	def b000(self):
		'''
		Cut Uv Hard Edges
		'''


	def b001(self):
		'''
		Flip UV
		'''
		u = 1
		v = 0
		w = 0

		objects = rt.selection

		for obj in objects:
			try:
				uv = self.getModifier(obj, 'UVW_Xform', -1) #get/set the uv xform modifier.
				uv.U_Flip = u
				uv.V_Flip = v
				uv.W_Flip = w
			except Exception as error:
				print(error)


	def b002(self):
		'''
		
		'''


	def b003(self):
		'''
		Uv Shell Selection Mask
		'''
		pm.selectType (meshUVShell=1)


	def b004(self):
		'''
		Uv Selection Mask
		'''
		pm.selectType (polymeshUV=1)


	def b005(self):
		'''
		Cut Uv'S
		'''
		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.
		uv.breakSelected()


	def b006(self):
		'''
		Pack UV's
		'''
		rotate = self.parentUi.chk001.isChecked() #rotate uv's
		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.
		uv.pack(1, 0.01, True, rotate, True) #Lets you pack the texture vertex elements so that they fit within a square space.
		# --method - 0 is a linear packing algorithm fast but not that efficient, 1 is a recursive algorithm slower but more efficient.
		# --spacing - the gap between cluster in percentage of the edge distance of the square
		# --normalize - determines whether the clusters will be fit to 0 to 1 space.
		# --rotate - determines whether a cluster will be rotated so it takes up less space.
		# --fillholes - determines whether smaller clusters will be put in the holes of the larger cluster.


	def b007(self):
		'''
		Display Checkered Pattern
		'''
		self.toggleMaterialOverride(checker=1)		


	def b008(self):
		'''
		Adjust Checkered Size
		'''


	def b009(self):
		'''
		Borders
		'''
		'''
		textureWindowCreatePopupContextMenu "polyTexturePlacementPanel1popupMenusShift";
		int $borders[] = `polyOptions -query -displayMapBorder`;
		float $borderWidth[] = `optionVar -query displayPolyBorderEdgeSize`;
		polyOptions -displayMapBorder (!$borders[0]) -sizeBorder $borderWidth[1];
		'''


	def b010(self):
		'''
		Distortion
		'''
		# actionMan.executeAction 2077580866 "40177"  -- Unwrap UVW: Show Edge Distortion
		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.

		state = uv.localDistortion
		uv.localDistortion = not state
		print('localDistortion:', not state)


	def b011(self):
		'''
		Sew Uv'S
		'''
		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.
		uv.stitchVerts(True, 1.0) #(align, bias) --Bias of 0.0 the vertices will move to the source and 1.0 they will move to the target. 


	def b012(self):
		'''
		Auto Unwrap
		'''
		scaleMode = self.parentUi.chk000.isChecked() #0 No scale is applied. 1 Uniform scale to fit in unit square. 2 Non proportional scale to fit in unit square.
		objects = rt.selection

		for obj in objects:
			try:
				uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.
				uv.FlattenBySmoothingGroup(scaleMode, False, 0.2)
			except Exception as error:
				print(error)


	def b013(self):
		'''
		Auto Map Multiple
		'''


	def b014(self):
		'''
		Rotate On Last
		'''


	def b015(self):
		'''
		Flip Horizontally On Last
		'''


	def b016(self):
		'''
		Flip Vertically On Last
		'''


	def b017(self):
		'''
		Align Uv Shells
		'''


	def b018(self):
		'''
		Unfold Uv'S
		'''
		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv xform modifier.
		uv.relax(1, 0.01, True, True)


	def b019(self):
		'''
		Optimize Uv'S
		'''


	def b020(self):
		'''
		Move To Uv Space
		'''
		u = str(self.parentUi.s000.value())
		v = str(self.parentUi.s001.value())

		pm.polyEditUV(u=u, v=v)


	def b021(self):
		'''
		Straighten Uv
		'''
		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv xform modifier.
		uv.Straighten()


	def b022(self):
		'''
		Stack Similar
		'''










#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

#apply uv map
# maxEval('modPanel.addModToSelection (Uvwmap ()) ui:on')