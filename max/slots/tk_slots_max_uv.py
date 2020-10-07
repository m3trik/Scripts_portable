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
		pin = self.uv.pin

		if state is 'setMenu':
			pin.contextMenu.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya UV Editors')
			pin.contextMenu.add(QLabel_, setObjectName='lbl000', setToolTip='Select Type: UV')
			pin.contextMenu.add(QLabel_, setObjectName='lbl001', setToolTip='Select Type: UV Shell')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.uv.cmb000

		if index is 'setMenu':
			list_ = ["UV Editor", "UV Set Editor", "UV Tool Kit", "UV Linking: Texture-Centric", "UV Linking: UV-Centric", "UV Linking: Paint Effects/UV", "UV Linking: Hair/UV"]
			cmb.addItems_(list_, '3dsMax UV Editors')
			return

		if index>0: #hide hotbox then perform operation
			self.tk.hide()
			if index==1: #UV Editor
				maxEval('TextureViewWindow;') 
			elif index==2: #UV Set Editor
				maxEval('uvSetEditor;')
			elif index==3: #UV Tool Kit
				maxEval('toggleUVToolkit;')
			elif index==4: #UV Linking: Texture-Centric
				maxEval('textureCentricUvLinkingEditor;')
			elif index==5: #UV Linking: UV-Centric
				maxEval('uvCentricUvLinkingEditor;')
			elif index==6: #UV Linking: Paint Effects/UV
				maxEval('pfxUVLinkingEditor;')
			elif index==7: #UV Linking: Hair/UV
				maxEval('hairUVLinkingEditor;')
			self.uv.cmb000.setCurrentIndex(0)


	# def chk001(self, state):
	# 	'''
	# 	Auto Unwrap: Scale Mode CheckBox
	# 	'''
	# 	tb = self.currentUi.tb001
	# 	if state==0:
	# 		tb.menu_.chk001.setText('Scale Mode 0')
	# 	if state==1:
	# 		tb.menu_.chk001.setText('Scale Mode 1')
	# 		self.toggleWidgets(tb.menu_, setUnChecked='chk002-6')
	# 	if state==2:
	# 		tb.menu_.chk001.setText('Scale Mode 2')


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
			tb.menu_.add('QCheckBox', setText='Rotate', setObjectName='chk000', setToolTip='Allow shell rotation during packing.')
			return

		rotate = tb.menu_.chk000.isChecked()

		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.
		uv.pack(1, 0.01, True, rotate, True) #Lets you pack the texture vertex elements so that they fit within a square space.
		# --method - 0 is a linear packing algorithm fast but not that efficient, 1 is a recursive algorithm slower but more efficient.
		# --spacing - the gap between cluster in percentage of the edge distance of the square
		# --normalize - determines whether the clusters will be fit to 0 to 1 space.
		# --rotate - determines whether a cluster will be rotated so it takes up less space.
		# --fillholes - determines whether smaller clusters will be put in the holes of the larger cluster.


	@Init.attr
	def tb001(self, state=None):
		'''
		Auto Unwrap
		'''
		tb = self.currentUi.tb001
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Scale Mode 0', setObjectName='chk001', setTristate=True, setToolTip='0 - No scale is applied.<br>1 - Uniform scale to fit in unit square.<br>2 - Non proportional scale to fit in unit square.')
			tb.menu_.add('QRadioButton', setText='Seam Only', setObjectName='chk002', setToolTip='Cut seams only.')
			tb.menu_.add('QRadioButton', setText='Planar', setObjectName='chk003', setToolTip='Create UV texture coordinates for the current selection by using a planar projection shape.')
			tb.menu_.add('QRadioButton', setText='Cylindrical', setObjectName='chk004', setToolTip='Create UV texture coordinates for the current selection, using a cylidrical projection that gets wrapped around the mesh.<br>Best suited for completely enclosed cylidrical shapes with no holes or projections on the surface.')
			tb.menu_.add('QRadioButton', setText='Spherical', setObjectName='chk005', setToolTip='Create UV texture coordinates for the current selection, using a spherical projection that gets wrapped around the mesh.<br>Best suited for completely enclosed spherical shapes with no holes or projections on the surface.')
			tb.menu_.add('QRadioButton', setText='Normal-Based', setObjectName='chk006', setToolTip='Create UV texture coordinates for the current selection by creating a planar projection based on the average vector of it\'s face normals.')
			
			# tb.menu_.chk001.toggled.connect(lambda state: self.toggleWidgets(tb.menu_, setUnChecked='chk002-3') if state==1 else None)
			return

		scaleMode = self.uv.chk001.isChecked()
		seamOnly = self.uv.chk002.isChecked()
		planarUnwrap = self.uv.chk003.isChecked()
		cylindricalUnwrap = self.uv.chk004.isChecked()
		sphericalUnwrap = self.uv.chk005.isChecked()
		normalBasedUnwrap = self.uv.chk006.isChecked()

		objects = rt.selection

		for obj in objects:
			try:
				uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.
				uv.FlattenBySmoothingGroup(scaleMode, False, 0.2)

			except Exception as error:
				print(error)


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
		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.
		uv.breakSelected()


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


	@Slots.message
	def b010(self):
		'''
		Distortion
		'''
		# actionMan.executeAction 2077580866 "40177"  -- Unwrap UVW: Show Edge Distortion
		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.

		state = uv.localDistortion
		uv.localDistortion = not state
		return '{0}{1}'.format('localDistortion:', not state)


	def b011(self):
		'''
		Sew Uv'S
		'''
		obj = rt.selection[0]

		uv = self.getModifier(obj, 'Unwrap_UVW', -1) #get/set the uv modifier.
		uv.stitchVerts(True, 1.0) #(align, bias) --Bias of 0.0 the vertices will move to the source and 1.0 they will move to the target. 


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
		u = int(self.uv.s000.value())
		v = int(self.uv.s001.value())

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