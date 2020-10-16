from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Uv(Init):
	def __init__(self, *args, **kwargs):
		super(Uv, self).__init__(*args, **kwargs)


	@property
	def uvModifier():
		'''
		Get the UV modifier for the current object.
		If one doesn't exist, a UV modifier will be added to the selected object.

		returns:
			(obj) uv modifier.
		'''
		selection = rt.selection
		if not selection:
			Slots.messageBox('Error: Nothing selected.')

		mod = self.getModifier(selection[0], 'Unwrap_UVW', -1) #get/set the uv xform modifier.
		return mod


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.uv.pin

		if state is 'setMenu':
			pin.contextMenu.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya UV Editors')
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


	def tb000(self, state=None):
		'''
		Pack UV's

		#pack command: Lets you pack the texture vertex elements so that they fit within a square space.
		# --method - 0 is a linear packing algorithm fast but not that efficient, 1 is a recursive algorithm slower but more efficient.
		# --spacing - the gap between cluster in percentage of the edge distance of the square
		# --normalize - determines whether the clusters will be fit to 0 to 1 space.
		# --rotate - determines whether a cluster will be rotated so it takes up less space.
		# --fillholes - determines whether smaller clusters will be put in the holes of the larger cluster.
		'''
		tb = self.currentUi.tb000
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Rotate', setObjectName='chk007', setToolTip='Allow shell rotation during packing.')
			return

		rotate = tb.menu_.chk007.isChecked()

		obj = rt.selection[0]

		self.uvModifier.pack(1, 0.01, True, rotate, True)


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

		objects = rt.selection

		for obj in objects:
			if standardUnwrap:
				try:
					self.uvModifier.FlattenBySmoothingGroup(scaleMode, False, 0.2)

				except Exception as error:
					print(error)


	def b000(self):
		'''
		Cut Uv Hard Edges
		'''
		pass


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
				uv = self.uvModifier #get/set the uv xform modifier.
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
			Slots.messageBox('Error: The operation requires the selection of two polygon objects.')

		from_ = sel[0]
		to = sel[-1]
		pm.transferAttributes(from_, to, transferUVs=2) # 0:no UV sets, 1:single UV set (specified by sourceUVSet and targetUVSet args), and 2:all UV sets are transferred.
		Slots.messageBox('Result: UV sets transferred from: {} to: {}.'.format(from_.name(), to.name()))


	def b005(self):
		'''
		Cut Uv'S
		'''
		self.uvModifier.breakSelected()


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
		mod = self.uvModifier #get/set the uv modifier.

		state = mod.localDistortion
		mod.localDistortion = not state
		return '{0}{1}'.format('localDistortion:', not state)


	def b011(self):
		'''
		Sew Uv'S
		'''
		self.uvModifier.stitchVerts(True, 1.0) #(align, bias) --Bias of 0.0 the vertices will move to the source and 1.0 they will move to the target. 


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
		self.uvModifier.relax(1, 0.01, True, True)


	def b019(self):
		'''
		Optimize Uv'S
		'''
		# self.uvModifier.

	def b021(self):
		'''
		Straighten Uv
		'''
		self.uvModifier.Straighten()


	def b022(self):
		'''
		Stack Similar
		'''
		# self.uvModifier.


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
		mod = self.uvModifier

		pm.polyEditUV(sel, u=u, v=v, relative=relative)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

#apply uv map
# maxEval('modPanel.addModToSelection (Uvwmap ()) ui:on')