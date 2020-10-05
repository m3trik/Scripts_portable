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
		pin = self.uv.pin

		if state is 'setMenu':
			pin.contextMenu.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya UV Editors')
			pin.contextMenu.add(QLabel_, setObjectName='lbl000', setText='Select Type: UV', setToolTip='Select Type: UV')
			pin.contextMenu.add(QLabel_, setObjectName='lbl001', setText='Select Type: UV Shell', setToolTip='Select Type: UV Shell')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.uv.cmb000

		if index is 'setMenu':
			list_ = ['UV Editor','UV Set Editor','UV Tool Kit','UV Linking: Texture-Centric','UV Linking: UV-Centric','UV Linking: Paint Effects/UV','UV Linking: Hair/UV','Flip UV']
			cmb.addItems_(list_, 'Maya UV Editors')
			return

		if index>0: #hide tk then perform operation
			self.tk.hide()
			if index==1: #UV Editor
				mel.eval('TextureViewWindow;') 
			elif index==2: #UV Set Editor
				mel.eval('uvSetEditor;')
			elif index==3: #UV Tool Kit
				mel.eval('toggleUVToolkit;')
			elif index==4: #UV Linking: Texture-Centric
				mel.eval('textureCentricUvLinkingEditor;')
			elif index==5: #UV Linking: UV-Centric
				mel.eval('uvCentricUvLinkingEditor;')
			elif index==6: #UV Linking: Paint Effects/UV
				mel.eval('pfxUVLinkingEditor;')
			elif index==7: #UV Linking: Hair/UV
				mel.eval('hairUVLinkingEditor;')
			elif index==cmb.items.index('Flip UV'):
				mel.eval("performPolyForceUV flip 1;")
			cmb.setCurrentIndex(0)


	def lbl000(self):
		'''
		Uv Shell Selection Mask
		'''
		pm.selectMode(component=1)
		pm.selectType(meshUVShell=1)


	def lbl001(self):
		'''
		Uv Selection Mask
		'''
		pm.selectMode(component=1)
		pm.selectType(polymeshUV=1)


	def b000(self):
		'''
		Cut Uv Hard Edges
		'''
		pm.mel.cutUvHardEdge()


	def b001(self):
		'''
		Flip Uv
		'''
		pm.mel.performPolyForceUV('flip', 0)


	def b002(self):
		'''
		Transfer Uv's
		'''
		sel = pm.ls(orderedSelection=1, flatten=1)
		if len(sel)<2:
			return 'Error: The operation requires the selection of two polygon objects.'

		from_ = sel[0]
		to = sel[-1]
		pm.transferAttributes(from_, to, transferUVs=2) # 0:no UV sets, 1:single UV set (specified by sourceUVSet and targetUVSet args), and 2:all UV sets are transferred.
		return 'Result: UV sets transferred from: {} to: {}.'.format(from_.name(), to.name())


	def b005(self):
		'''
		Cut Uv'S
		'''
		objects = pm.ls(selection=1, objectsOnly=1, flatten=1)

		for obj in objects:
			sel = pm.ls(obj, sl=1)
			pm.polyMapCut()


	@Init.attr
	def b006(self):
		'''
		Pack UV's

		pm.u3dLayout:
			layoutScaleMode (int),
			multiObject (bool),
			mutations (int),
			packBox (float, float, float, float),
			preRotateMode (int),
			preScaleMode (int),
			resolution (int),
			rotateMax (float),
			rotateMin (float),
			rotateStep (float),
			shellSpacing (float),
			tileAssignMode (int),
			tileMargin (float),
			tileU (int),
			tileV (int),
			translate (bool)
		'''
		rotate = self.uv.chk001.isChecked() #rotate uv's
		rotateMax = 0.0
		if rotate:
			rotateMax = 360.0

		obj = pm.ls(sl=1)
		return pm.u3dLayout(obj, resolution=2048, preScaleMode=1, shellSpacing=.75, tileMargin=.75, packBox=[0,1,0,1], rotateMax=rotateMax) #layoutScaleMode (int), multiObject (bool), mutations (int), packBox (float, float, float, float), preRotateMode (int), preScaleMode (int), resolution (int), rotateMax (float), rotateMin (float), rotateStep (float), shellSpacing (float), tileAssignMode (int), tileMargin (float), tileU (int), tileV (int), translate (bool)


	def b007(self):
		'''
		Display Checkered Pattern
		'''
		state = pm.textureWindow('polyTexturePlacementPanel1', displayCheckered=1, query=1)
		pm.textureWindow('polyTexturePlacementPanel1', edit=1, displayCheckered=(not state))	


	def b008(self):
		'''
		Adjust Checkered Size
		'''
		pm.mel.bt_textureEditorCheckerSize()


	def b009(self):
		'''
		Borders
		'''
		pm.mel.textureWindowCreatePopupContextMenu("polyTexturePlacementPanel1popupMenusShift")
		borders = pm.polyOptions(query=1, displayMapBorder=1)
		borderWidth = pm.optionVar(query='displayPolyBorderEdgeSize')
		pm.polyOptions(displayMapBorder=(not borders[0]), sizeBorder=borderWidth[1])


	def b010(self):
		'''
		Distortion
		'''
		winName = pm.getPanel(scriptType='polyTexturePlacementPanel')
		state = int(pm.textureWindow(winName[0], query=1, displayDistortion=1))

		if state!=1:
			pm.textureWindow(winName[0], edit=1, displayDistortion=1)
		else:
			pm.textureWindow(winName[0], edit=1, displayDistortion=0)


	def b011(self):
		'''
		Sew Uv'S
		'''
		objects = pm.ls(selection=1, objectsOnly=1, flatten=1)

		for obj in objects:
			sel = pm.ls(obj, sl=1)
			pm.polyMapSew(sel)


	@Init.attr
	def b012(self):
		'''
		Auto Unwrap
		'''
		scaleMode = self.uv.chk000.isChecked() #0 No scale is applied. 1 Uniform scale to fit in unit square. 2 Non proportional scale to fit in unit square.
		objects = pm.ls(selection=1, objectsOnly=1, flatten=1) #get shape nodes

		for obj in objects:
			try:
				return pm.polyAutoProjection (obj, layoutMethod=0, optimize=1, insertBeforeDeformers=1, scaleMode=scaleMode, createNewMap=False, #Create a new UV set, as opposed to editing the current one, or the one given by the -uvSetName flag.
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
		pm.mel.bt_autoMapMultipleMeshes()


	def b014(self):
		'''
		Rotate On Last
		'''
		pm.mel.bt_checkSelectionOrderPref()
		pm.mel.bt_rotateUVsAroundLastWin()


	def b015(self):
		'''
		Flip Horizontally On Last
		'''
		pm.mel.bt_checkSelectionOrderPref()
		pm.mel.bt_polyflipUVsAcrossLast(0)


	def b016(self):
		'''
		Flip Vertically On Last
		'''
		pm.mel.bt_checkSelectionOrderPref()
		pm.mel.bt_polyflipUVsAcrossLast(1)


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
		pm.mel.performUnfold(0)


	def b019(self):
		'''
		Optimize Uv'S
		'''
		pm.mel.performPolyOptimizeUV(0)


	@Init.attr
	def b020(self):
		'''
		Move To Uv Space
		'''
		u = int(self.uv.s000.value())
		v = int(self.uv.s001.value())

		return pm.polyEditUV(u=u, v=v, relative=True)


	def b021(self):
		'''
		Straighten Uv
		'''
		pm.mel.texStraightenUVs("UV", 30)


	def b022(self):
		'''
		Stack Similar
		'''
		obj = pm.ls(sl=1)
		similar = pm.polyUVStackSimilarShells(obj, to=0.1)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------