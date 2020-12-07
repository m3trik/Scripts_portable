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

		:Return:
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
			pin.contextMenu.add(widgets.TkComboBox, setObjectName='cmb000', setToolTip='Maya UV Editors')
			pin.contextMenu.add('QPushButton', setText='Create UV Snapshot', setObjectName='b001', setToolTip='Save an image file of the current UV layout.')
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
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Display
		'''
		cmb = self.uv.cmb001

		if index is 'setMenu':
			cmb.popupStyle = 'qmenu'

			try:
				checkered = pm.textureWindow('polyTexturePlacementPanel1', displayCheckered=1, query=1)
				borders = pm.polyOptions(query=1, displayMapBorder=1)
				distortion = pm.textureWindow(pm.getPanel(scriptType='polyTexturePlacementPanel'), query=1, displayDistortion=1)

				cmb.menu_.add(widgets.TkCheckBox, setObjectName='chk014', setText='Checkered', setChecked=checkered, setToolTip='')
				cmb.menu_.add(widgets.TkCheckBox, setObjectName='chk015', setText='Borders', setChecked=borders, setToolTip='')
				cmb.menu_.add(widgets.TkCheckBox, setObjectName='chk016', setText='Distortion', setChecked=distortion, setToolTip='')

			except NameError as error:
				print(error)
			return


	def cmb002(self, index=None):
		'''
		Transform
		'''
		cmb = self.uv.cmb002

		if index is 'setMenu':
			list_ = ['Flip U', 'Flip V', 'Align U Left', 'Align U Middle', 'Align U Right', 'Align V Top', 'Align V Middle', 'Align V Bottom', 'Linear Align']
			cmb.addItems_(list_, 'Transform:')
			return

		if index>0:
			self.tk.hide() #hide hotbox then perform operation
			if index==cmb.items.index('Flip U'):
				pm.polyFlipUV(flipType=0, local=1, usePivot=1, pivotU=0, pivotV=0)
			elif index==cmb.items.index('Flip V'):
				pm.polyFlipUV(flipType=1, local=1, usePivot=1, pivotU=0, pivotV=0)
			elif index==cmb.items.index('Align U Left'):
				pm.mel.performAlignUV('minU')
			elif index==cmb.items.index('Align U Middle'):
				pm.mel.performAlignUV('avgU')
			elif index==cmb.items.index('Align U Right'):
				pm.mel.performAlignUV('maxU')
			elif index==cmb.items.index('Align U Top'):
				pm.mel.performAlignUV('maxV')
			elif index==cmb.items.index('Align U Middle'):
				pm.mel.performAlignUV('avgV')
			elif index==cmb.items.index('Align U Bottom'):
				pm.mel.performAlignUV('minV')
			elif index==cmb.items.index('Linear Align'):
				pm.mel.performLinearAlignUV()
			cmb.setCurrentIndex(0)


	def chk001(self, state):
		'''
		Auto Unwrap: Scale Mode CheckBox
		'''
		pass


	def chk014(self):
		'''
		Display: Checkered Pattern
		'''
		cmb = self.uv.cmb001
		state = cmb.menu_.chk014.isChecked()

		self.toggleMaterialOverride(checker=state)


	def chk015(self):
		'''
		Display: Borders
		'''
		cmb = self.uv.cmb001
		state = cmb.menu_.chk015.isChecked()

		borderWidth = pm.optionVar(query='displayPolyBorderEdgeSize')[1]
		borders = pm.polyOptions(displayMapBorder=state, sizeBorder=borderWidth)


	@Slots.message
	def chk016(self):
		'''
		Display: Distortion
		'''
		cmb = self.uv.cmb001
		state = cmb.menu_.chk016.isChecked()

		# actionMan.executeAction 2077580866 "40177"  -- Unwrap UVW: Show Edge Distortion
		mod = self.uvModifier #get/set the uv modifier.

		mod.localDistortion = state
		return '{0}{1}'.format('localDistortion:', state)


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
			tb.menu_.add('QCheckBox', setText='Scale', setObjectName='chk025', setChecked=True, setToolTip='Allow shell scaling during packing.')
			tb.menu_.add('QCheckBox', setText='Rotate', setObjectName='chk007', setChecked=True, setToolTip='Allow shell rotation during packing.')
			return

		scale = tb.menu_.chk025.isChecked()
		rotate = tb.menu_.chk007.isChecked()

		obj = rt.selection[0]

		self.uvModifier.pack(1, 0.01, scale, rotate, True) #(method, spacing, normalize, rotate, fillholes)


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


	def tb002(self, state=None):
		'''
		Stack
		'''
		tb = self.currentUi.tb002
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Orient', setObjectName='chk021', setChecked=True, setToolTip='Orient UV shells to run parallel with the most adjacent U or V axis.')
			tb.menu_.add('QCheckBox', setText='Stack Similar', setObjectName='chk022', setChecked=True, setToolTip='Stack only shells that fall within the set tolerance.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='Tolerance: ', setObjectName='s000', setMinMax_='0.0-10 step.05', setValue=0.05, setToolTip='Stack shells with uv\'s within the given range.')
			return

		orient = tb.menu_.chk021.isChecked()
		stackSimilar = tb.menu_.chk022.isChecked()
		tolerance = tb.menu_.s000.value()
		sel = Uv.UvShellSelection() #assure the correct selection mask.

		if stackSimilar:
			pm.polyUVStackSimilarShells(sel, tolerance=tolerance)
		else:
			pm.mel.texStackShells([])
		if orient:
			pm.mel.texOrientShells()


	def tb003(self, state=None):
		'''
		Select By Type
		'''
		tb = self.currentUi.tb003
		if state is 'setMenu':
			tb.menu_.add('QRadioButton', setText='Back-Facing', setObjectName='chk008', setToolTip='Select all back-facing (using counter-clockwise winding order) components for the current selection.')
			tb.menu_.add('QRadioButton', setText='Front-Facing', setObjectName='chk009', setToolTip='Select all front-facing (using counter-clockwise winding order) components for the current selection.')
			tb.menu_.add('QRadioButton', setText='Overlapping', setObjectName='chk010', setToolTip='Select all components that share the same uv space.')
			tb.menu_.add('QRadioButton', setText='Non-Overlapping', setObjectName='chk011', setToolTip='Select all components that do not share the same uv space.')
			tb.menu_.add('QRadioButton', setText='Texture Borders', setObjectName='chk012', setToolTip='Select all components on the borders of uv shells.')
			tb.menu_.add('QRadioButton', setText='Unmapped', setObjectName='chk013', setChecked=True, setToolTip='Select unmapped faces in the current uv set.')
			return

		back_facing = self.uv.chk008.isChecked()
		front_facing = self.uv.chk009.isChecked()
		overlapping = self.uv.chk010.isChecked()
		nonOverlapping = self.uv.chk011.isChecked()
		textureBorders = self.uv.chk012.isChecked()
		unmapped = self.uv.chk013.isChecked()

		if back_facing:
			pm.mel.selectUVFaceOrientationComponents({}, 0, 2, 1)
		elif front_facing:
			pm.mel.selectUVFaceOrientationComponents({}, 0, 1, 1)
		elif overlapping:
			pm.mel.selectUVOverlappingComponents(1, 0)
		elif nonOverlapping:
			pm.mel.selectUVOverlappingComponents(0, 0)
		elif textureBorders:
			pm.mel.selectUVBorderComponents({}, "", 1)
		elif unmapped:
			pm.mel.selectUnmappedFaces()


	def tb004(self, state=None):
		'''
		Unfold
		'''
		tb = self.currentUi.tb004
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Optimize', setObjectName='chk017', setChecked=True, setToolTip='The Optimize UV Tool evens out the spacing between UVs on a mesh, fixing areas of distortion (overlapping UVs).')
			return

		optimize = self.tb.menu_.chk017.isChecked()

		# if optimize:
		# 	# self.uvModifier.
		# else:
		self.uvModifier.relax(1, 0.01, True, True)


	def tb005(self, state=None):
		'''
		Straighten Uv
		'''
		tb = self.currentUi.tb005
		if state is 'setMenu':
			tb.menu_.add('QSpinBox', setPrefix='Angle: ', setObjectName='s001', setMinMax_='0-360 step1', setValue=30, setToolTip='Set the maximum angle used for straightening uv\'s.')
			tb.menu_.add('QCheckBox', setText='Straighten U', setObjectName='chk018', setChecked=True, setToolTip='Unfold UV\'s along a horizonal contraint.')
			tb.menu_.add('QCheckBox', setText='Straighten V', setObjectName='chk019', setChecked=True, setToolTip='Unfold UV\'s along a vertical constaint.')
			tb.menu_.add('QCheckBox', setText='Straighten Shell', setObjectName='chk020', setToolTip='Straighten a UV shell by unfolding UV\'s around a selected UV\'s edgeloop.')
			return

		u = tb.menu_.chk018.isChecked()
		v = tb.menu_.chk019.isChecked()
		angle = tb.menu_.s001.value()
		straightenShell = tb.menu_.chk020.isChecked()

		# if u:
		# 	contraint = 'U'
		# if v:
		# 	constaint = 'V' if not u else 'UV'

		self.uvModifier.Straighten()

		# if straightenShell:
		# 	pm.mel.texStraightenShell()


	def tb006(self, state=None):
		'''
		Distribute
		'''
		tb = self.currentUi.tb006
		if state is 'setMenu':
			tb.menu_.add('QRadioButton', setText='Distribute U', setObjectName='chk023', setChecked=True, setToolTip='Distribute along U.')
			tb.menu_.add('QRadioButton', setText='Distribute V', setObjectName='chk024', setToolTip='Distribute along V.')
			return

		u = tb.menu_.chk023.isChecked()
		v = tb.menu_.chk024.isChecked()
		
		if u:
			pm.mel.texDistributeShells(0, 0, "right", []) #'left', 'right'
		if v:
			pm.mel.texDistributeShells(0, 0, "down", []) #'up', 'down'


	def tb007(self, state=None):
		'''
		Set Texel Density
		'''
		tb = self.currentUi.tb007
		if state is 'setMenu':
			tb.menu_.add('QSpinBox', setPrefix='Map Size: ', setObjectName='s002', setMinMax_='512-32768 step1024', setValue=2048, setToolTip='Set the map used as reference when getting texel density.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='Texel Density: ', setObjectName='s003', setMinMax_='0.00-128 step8', setValue=32, setToolTip='Set the desired texel density.')
			tb.menu_.add('QPushButton', setText='Get Texel Density', setObjectName='b099', setChecked=True, setToolTip='Get the average texel density of any selected faces.')

			tb.menu_.b099.released.connect(lambda: tb.menu_.s003.setValue(float(pm.mel.texGetTexelDensity(tb.menu_.s002.value())))) #get and set texel density value.
			return

		mapSize = tb.menu_.s002.value()
		density = tb.menu_.s003.value()

		pm.mel.texSetTexelDensity(density, mapSize)


	def b000(self):
		'''
		Cut Uv Hard Edges
		'''
		pass


	def b001(self):
		'''
		Create UV Snapshot
		'''
		pass


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


	def b011(self):
		'''
		Sew Uv'S
		'''
		self.uvModifier.stitchVerts(True, 1.0) #(align, bias) --Bias of 0.0 the vertices will move to the source and 1.0 they will move to the target. 


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

		:Parameters:
			u (int) = u coordinate.
			v (int) = v coordinate.
			relative (bool) = Move relative or absolute.
		'''
		mod = self.uvModifier

		pm.polyEditUV(sel, u=u, v=v, relative=relative)


	@staticmethod
	def flipUV(objects=None):
		'''
		
		'''
		u = 1
		v = 0
		w = 0

		if not objects:
			objects = rt.selection

		for obj in objects:
			try:
				uv = self.uvModifier #get/set the uv xform modifier.
				uv.U_Flip = u
				uv.V_Flip = v
				uv.W_Flip = w

			except Exception as error:
				print(error)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

#apply uv map
# maxEval('modPanel.addModToSelection (Uvwmap ()) ui:on')