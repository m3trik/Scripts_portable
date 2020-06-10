from __future__ import print_function
from tk_slots_maya_init import *

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
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya UV Editors')

			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000
		
		list_ = ['UV Editor','UV Set Editor','UV Tool Kit','UV Linking: Texture-Centric','UV Linking: UV-Centric','UV Linking: Paint Effects/UV','UV Linking: Hair/UV','Flip UV']
		items = cmb.addItems_(list_, 'Maya UV Editors')

		if not index:
			index = cmb.currentIndex()
		if index !=0: #hide tk then perform operation
			self.tk.hide()
			if index == 1: #UV Editor
				mel.eval('TextureViewWindow;') 
			if index == 2: #UV Set Editor
				mel.eval('uvSetEditor;')
			if index == 3: #UV Tool Kit
				mel.eval('toggleUVToolkit;')
			if index == 4: #UV Linking: Texture-Centric
				mel.eval('textureCentricUvLinkingEditor;')
			if index == 5: #UV Linking: UV-Centric
				mel.eval('uvCentricUvLinkingEditor;')
			if index == 6: #UV Linking: Paint Effects/UV
				mel.eval('pfxUVLinkingEditor;')
			if index == 7: #UV Linking: Hair/UV
				mel.eval('hairUVLinkingEditor;')
			if index==items.index('Flip UV'):
				mel.eval("performPolyForceUV flip 1;")
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Cut Uv Hard Edges
		'''
		mel.eval("cutUvHardEdge ();")


	def b001(self):
		'''
		Flip Uv
		'''
		mel.eval("performPolyForceUV flip 0;")


	def b002(self):
		'''
		
		'''
		pass


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
		pm.polyMapCut()


	def b006(self):
		'''
		Pack UV's
		'''
		rotate = self.parentUi.chk001.isChecked() #rotate uv's
		rotateMax = 0.0
		if rotate:
			rotateMax = 360.0

		obj = pm.ls(sl=1)
		pm.u3dLayout(obj, resolution=2048, preScaleMode=1, packBox=[0,1,0,1], rotateMax=rotateMax) #layoutScaleMode (int), multiObject (bool), mutations (int), packBox (float, float, float, float), preRotateMode (int), preScaleMode (int), resolution (int), rotateMax (float), rotateMin (float), rotateStep (float), shellSpacing (float), tileAssignMode (int), tileMargin (float), tileU (int), tileV (int), translate (bool)


	def b007(self):
		'''
		Display Checkered Pattern
		'''
		mel.eval('''
		$state = `textureWindow -query -displayCheckered polyTexturePlacementPanel1`;
		textureWindow -edit -displayCheckered (!$state) polyTexturePlacementPanel1;
		''')		


	def b008(self):
		'''
		Adjust Checkered Size
		'''
		mel.eval("bt_textureEditorCheckerSize;")


	def b009(self):
		'''
		Borders
		'''
		mel.eval('''
		textureWindowCreatePopupContextMenu "polyTexturePlacementPanel1popupMenusShift";
		int $borders[] = `polyOptions -query -displayMapBorder`;
		float $borderWidth[] = `optionVar -query displayPolyBorderEdgeSize`;
		polyOptions -displayMapBorder (!$borders[0]) -sizeBorder $borderWidth[1];
		''')


	def b010(self):
		'''
		Distortion
		'''
		mel.eval('''
		string $winName[] = `getPanel -scriptType polyTexturePlacementPanel`;
		int $state = `textureWindow -query -displayDistortion $winName[0]`;
		if ($state != 1)
			textureWindow -edit -displayDistortion 1 $winName[0];
		else
			textureWindow -edit -displayDistortion 0 $winName[0];
		''')


	def b011(self):
		'''
		Sew Uv'S
		'''
		pm.polyMapSew()


	def b012(self):
		'''
		Auto Unwrap
		'''
		scaleMode = self.parentUi.chk000.isChecked() #0 No scale is applied. 1 Uniform scale to fit in unit square. 2 Non proportional scale to fit in unit square.
		objects = pm.ls(selection=1, objectsOnly=1, flatten=1) #get shape nodes

		for obj in objects:
			try:
				pm.polyAutoProjection (obj, layoutMethod=0, optimize=1, insertBeforeDeformers=1, scaleMode=scaleMode, createNewMap=False, #Create a new UV set, as opposed to editing the current one, or the one given by the -uvSetName flag.
					projectBothDirections=0, #If "on" : projections are mirrored on directly opposite faces. If "off" : projections are not mirrored on opposite faces. 
					layout=2, #0 UV pieces are set to no layout. 1 UV pieces are aligned along the U axis. 2 UV pieces are moved in a square shape.
					planes=6, #intermediate projections used. Valid numbers are 4, 5, 6, 8, and 12
					percentageSpace=0.2, #percentage of the texture area which is added around each UV piece.
					worldSpace=0) #1=world reference. 0=object reference.
			except Exception as error:
				print(error)
 

	def b013(self):
		'''
		Auto Map Multiple
		'''
		mel.eval('bt_autoMapMultipleMeshes;')


	def b014(self):
		'''
		Rotate On Last
		'''
		mel.eval('bt_checkSelectionOrderPref; bt_rotateUVsAroundLastWin;')


	def b015(self):
		'''
		Flip Horizontally On Last
		'''
		mel.eval('bt_checkSelectionOrderPref; bt_polyflipUVsAcrossLast 0;')


	def b016(self):
		'''
		Flip Vertically On Last
		'''
		mel.eval('bt_checkSelectionOrderPref; bt_polyflipUVsAcrossLast 1;')


	def b017(self):
		'''
		Align Uv Shells
		'''
		from AlignUVShells import *
		AlignUVShellsWindow()


	def b018(self):
		'''
		Unfold Uv'S
		'''
		mel.eval('performUnfold 0;')


	def b019(self):
		'''
		Optimize Uv'S
		'''
		mel.eval('performPolyOptimizeUV 0;')


	def b020(self):
		'''
		Move To Uv Space
		'''
		u = str(self.parentUi.s000.value())
		v = str(self.parentUi.s001.value())

		pm.polyEditUV (u=u, v=v)


	def b021(self):
		'''
		Straighten Uv
		'''
		mel.eval('texStraightenUVs "UV" 30;')


	def b022(self):
		'''
		Stack Similar
		'''
		obj = pm.ls(sl=1)
		pm.polyUVStackSimilarShells(obj, to=0.1)








#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------