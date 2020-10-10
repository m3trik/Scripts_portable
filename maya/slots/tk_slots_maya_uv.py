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


	def chk001(self, state):
		'''
		Auto Unwrap: Scale Mode CheckBox
		'''
		tb = self.currentUi.tb001
		if state==0:
			tb.menu_.chk001.setText('Scale Mode 0')
		if state==1:
			tb.menu_.chk001.setText('Scale Mode 1')
			self.toggleWidgets(tb.menu_, setUnChecked='chk002-6')
		if state==2:
			tb.menu_.chk001.setText('Scale Mode 2')


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


	def tb000(self, state=None):
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
		tb = self.currentUi.tb000
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Rotate', setObjectName='chk007', setChecked=True, setToolTip='Allow shell rotation during packing.')
			return

		rotate = tb.menu_.chk007.isChecked()

		rotateMax = 0.0
		if rotate:
			rotateMax = 360.0

		sel = pm.ls(sl=1)
		packUv = pm.u3dLayout(sel, resolution=2048, preScaleMode=1, shellSpacing=.005, tileMargin=.005, packBox=[0,1,0,1], rotateMax=rotateMax) #layoutScaleMode (int), multiObject (bool), mutations (int), packBox (float, float, float, float), preRotateMode (int), preScaleMode (int), resolution (int), rotateMax (float), rotateMin (float), rotateStep (float), shellSpacing (float), tileAssignMode (int), tileMargin (float), tileU (int), tileV (int), translate (bool)


	@Init.attr
	def tb001(self, state=None):
		'''
		Auto Unwrap
		'''
		tb = self.currentUi.tb001
		if state is 'setMenu':
			tb.menu_.add('QRadioButton', setText='Standard', setObjectName='chk000', setChecked=True, setToolTip='Create UV texture coordinates for the selected object or faces by automatically finding the best UV placement using simultanious projections from multiple planes.')
			tb.menu_.add('QCheckBox', setText='Scale Mode 1', setObjectName='chk001', setTristate=True, setChecked=True, setToolTip='0 - No scale is applied.<br>1 - Uniform scale to fit in unit square.<br>2 - Non proportional scale to fit in unit square.')
			tb.menu_.add('QRadioButton', setText='Seam Only', setObjectName='chk002', setToolTip='Cut seams only.')
			tb.menu_.add('QRadioButton', setText='Planar', setObjectName='chk003', setToolTip='Create UV texture coordinates for the current selection by using a planar projection shape.')
			tb.menu_.add('QRadioButton', setText='Cylindrical', setObjectName='chk004', setToolTip='Create UV texture coordinates for the current selection, using a cylidrical projection that gets wrapped around the mesh.<br>Best suited for completely enclosed cylidrical shapes with no holes or projections on the surface.')
			tb.menu_.add('QRadioButton', setText='Spherical', setObjectName='chk005', setToolTip='Create UV texture coordinates for the current selection, using a spherical projection that gets wrapped around the mesh.<br>Best suited for completely enclosed spherical shapes with no holes or projections on the surface.')
			tb.menu_.add('QRadioButton', setText='Normal-Based', setObjectName='chk006', setToolTip='Create UV texture coordinates for the current selection by creating a planar projection based on the average vector of it\'s face normals.')

			# tb.menu_.chk001.toggled.connect(lambda state: self.toggleWidgets(tb.menu_, setUnChecked='chk002-3') if state==1 else None)
			return

		standardUnwrap = self.uv.chk000.isChecked()
		scaleMode = self.uv.chk001.isChecked()
		seamOnly = self.uv.chk002.isChecked()
		planarUnwrap = self.uv.chk003.isChecked()
		cylindricalUnwrap = self.uv.chk004.isChecked()
		sphericalUnwrap = self.uv.chk005.isChecked()
		normalBasedUnwrap = self.uv.chk006.isChecked()

		selection = pm.ls(selection=1, flatten=1)
		for obj in selection:
			try:
				if seamOnly:
					autoSeam = pm.u3dAutoSeam(obj, s=0, p=1)
					return autoSeam if len(selection)==1 else autoSeam

				elif any((cylindricalUnwrap, sphericalUnwrap, planarUnwrap)):
					unwrapType = 'Planar'
					if cylindricalUnwrap:
						unwrapType = 'Cylindrical'
					elif sphericalUnwrap:
						unwrapType = 'Spherical'
					objFaces = Init.getSelectedComponents('faces', obj)
					if not objFaces:
						objFaces = Init.getComponents(obj, 'faces')
					pm.polyProjection(objFaces, type=unwrapType, insertBeforeDeformers=1, smartFit=1)

				elif normalBasedUnwrap:
					pm.mel.texNormalProjection(1, 1, obj) #Normal-Based unwrap

				elif standardUnwrap:
					polyAutoProjection = pm.polyAutoProjection (obj, layoutMethod=0, optimize=1, insertBeforeDeformers=1, scaleMode=scaleMode, createNewMap=False, #Create a new UV set, as opposed to editing the current one, or the one given by the -uvSetName flag.
						projectBothDirections=0, #If "on" : projections are mirrored on directly opposite faces. If "off" : projections are not mirrored on opposite faces. 
						layout=2, #0 UV pieces are set to no layout. 1 UV pieces are aligned along the U axis. 2 UV pieces are moved in a square shape.
						planes=6, #intermediate projections used. Valid numbers are 4, 5, 6, 8, and 12
						percentageSpace=0.2, #percentage of the texture area which is added around each UV piece.
						worldSpace=0) #1=world reference. 0=object reference.

					return polyAutoProjection if len(selection)==1 else polyAutoProjection

			except Exception as error:
				print(error)


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
		objects = pm.ls(selection=1, objectsOnly=1, shapes=1, flatten=1)

		for obj in objects:
			sel = pm.ls(obj, sl=1)
			pm.polyMapCut(sel)


	def b007(self):
		'''
		Display: Checkered Pattern
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
		Display: Borders
		'''
		pm.mel.textureWindowCreatePopupContextMenu("polyTexturePlacementPanel1popupMenusShift")
		borders = pm.polyOptions(query=1, displayMapBorder=1)
		borderWidth = pm.optionVar(query='displayPolyBorderEdgeSize')
		pm.polyOptions(displayMapBorder=(not borders[0]), sizeBorder=borderWidth[1])


	def b010(self):
		'''
		Display: Distortion
		'''
		winName = pm.getPanel(scriptType='polyTexturePlacementPanel')
		state = int(pm.textureWindow(winName[0], query=1, displayDistortion=1))

		if state!=1:
			pm.textureWindow(winName[0], edit=1, displayDistortion=1)
		else:
			pm.textureWindow(winName[0], edit=1, displayDistortion=0)


	@Init.attr
	def b011(self):
		'''
		Sew Uv'S
		'''
		objects = pm.ls(selection=1, objectsOnly=1, shapes=1, flatten=1)

		for obj in objects:
			sel = pm.ls(obj, sl=1)

			return pm.polyMapSew(sel) if len(objects)==1 else pm.polyMapSew(sel)
 

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


	def b021(self):
		'''
		Straighten Uv
		'''
		pm.mel.texStraightenUVs("UV", 30)


	def b022(self):
		'''
		Stack Similar
		'''
		tol = 0.5
		obj = pm.ls(sl=1)

		similar = pm.polyUVStackSimilarShells(obj, tolerance=tol)


	def b023(self):
		'''
		Move To Uv Space: Left
		'''
		Uv.moveSelectedToUvSpace(-1, 0) #move left


	def b024(self):
		'''
		Move To Uv Space: Down
		'''
		Uv.moveSelectedToUvSpace(0, -1) #move down


	def b025(self):
		'''
		Move To Uv Space: Up
		'''
		Uv.moveSelectedToUvSpace(0, 1) #move up


	def b026(self):
		'''
		Move To Uv Space: Right
		'''
		Uv.moveSelectedToUvSpace(1, 0) #move right


	@staticmethod
	def moveSelectedToUvSpace(u, v, relative=True):
		'''
		Move sny selected objects to the given u and v coordinates.

		args:
			u (int) = u coordinate.
			v (int) = v coordinate.
			relative (bool) = Move relative or absolute.
		'''
		selection = pm.ls(sl=1)
		if not selection:
			print('# Error: Nothing selected. #')

		objects = pm.ls(sl=1, objectsOnly=1)
		objectMode = pm.selectMode(query=1, object=1)

		if objects and objectMode:
			for obj in objects:
				pm.selectMode(component=1)
				pm.selectType(meshUVShell=1)
				faces = Init.getComponents(obj, 'faces', flatten=False)
				pm.select(faces, add=True)

		pm.polyEditUV(u=u, v=v, relative=relative)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------