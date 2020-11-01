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


	def cmb001(self, index=None):
		'''
		Display
		'''
		cmb = self.uv.cmb001

		if index is 'setMenu':
			cmb.popupStyle = 'qmenu'

			try:
				panel = pm.getPanel(scriptType='polyTexturePlacementPanel')
				checkered = pm.textureWindow(panel, displayCheckered=1, query=1)
				borders = True if pm.polyOptions(query=1, displayMapBorder=1) else False
				distortion = pm.textureWindow(panel, query=1, displayDistortion=1)

				cmb.menu_.add(QCheckBox_, setObjectName='chk014', setText='Checkered', setChecked=checkered, setToolTip='')
				cmb.menu_.add(QCheckBox_, setObjectName='chk015', setText='Borders', setChecked=borders, setToolTip='')
				cmb.menu_.add(QCheckBox_, setObjectName='chk016', setText='Distortion', setChecked=distortion, setToolTip='')

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
		tb = self.currentUi.tb001
		if state==0:
			tb.menu_.chk001.setText('Scale Mode 0')
		if state==1:
			tb.menu_.chk001.setText('Scale Mode 1')
			self.toggleWidgets(tb.menu_, setUnChecked='chk002-6')
		if state==2:
			tb.menu_.chk001.setText('Scale Mode 2')


	def chk014(self):
		'''
		Display: Checkered Pattern
		'''
		cmb = self.uv.cmb001
		state = cmb.menu_.chk014.isChecked()

		panel = pm.getPanel(scriptType='polyTexturePlacementPanel')
		pm.textureWindow(panel, edit=1, displayCheckered=state)


	def chk015(self):
		'''
		Display: Borders
		'''
		cmb = self.uv.cmb001
		state = cmb.menu_.chk015.isChecked()

		borderWidth = pm.optionVar(query='displayPolyBorderEdgeSize')[1]
		borders = pm.polyOptions(displayMapBorder=state, sizeBorder=borderWidth)


	def chk016(self):
		'''
		Display: Distortion
		'''
		cmb = self.uv.cmb001
		state = cmb.menu_.chk016.isChecked()

		panel = pm.getPanel(scriptType='polyTexturePlacementPanel')
		pm.textureWindow(panel, edit=1, displayDistortion=state)


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
			tb.menu_.add(QCheckBox_, setText='Pre-Scale Mode: 1', setObjectName='chk025', setTristate=True, setCheckState_=1, setToolTip='Allow shell scaling during packing.')
			tb.menu_.add(QCheckBox_, setText='Pre-Rotate Mode: 1', setObjectName='chk007', setTristate=True, setCheckState_=1, setToolTip='Allow shell rotation during packing.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='Rotate Step: ', setObjectName='s007', setMinMax_='0.0-360 step22.5', setValue=22.5, setToolTip='Set the allowed rotation increment contraint.')
			tb.menu_.add(QCheckBox_, setText='Stack Similar: 2', setObjectName='chk026', setTristate=True, setCheckState_=2, setToolTip='Find Similar shells. <br>state 1: Find similar shells, and pack one of each, ommiting the rest.<br>state 2: Find similar shells, and stack during packing (can be very slow).')
			tb.menu_.add('QDoubleSpinBox', setPrefix='Stack Similar Tolerance: ', setObjectName='s006', setMinMax_='0.0-10 step.1', setValue=1.0, setToolTip='Stack shells with uv\'s within the given range.')
			tb.menu_.add('QSpinBox', setPrefix='UDIM: ', setObjectName='s004', setMinMax_='1001-1200 step1', setValue=1001, setToolTip='Set the desired UDIM tile space.')
			tb.menu_.add('QSpinBox', setPrefix='Map Size: ', setObjectName='s005', setMinMax_='512-8192 step512', setValue=2048, setToolTip='UV map resolution.')

			tb.menu_.chk025.stateChanged.connect(lambda state: tb.menu_.chk025.setText('Pre-Scale Mode: '+str(state)))
			tb.menu_.chk007.stateChanged.connect(lambda state: tb.menu_.chk007.setText('Pre-Rotate Mode: '+str(state)))
			tb.menu_.chk026.stateChanged.connect(lambda state: tb.menu_.chk026.setText('Stack Similar: '+str(state)))
			return

		scale = tb.menu_.chk025.isChecked()
		rotate = tb.menu_.chk007.isChecked()
		rotateStep = tb.menu_.s007.value()
		UDIM = tb.menu_.s004.value()
		mapSize = tb.menu_.s005.value()
		similar = tb.menu_.chk026.checkState_()
		tolerance = tb.menu_.s006.value()

		U,D,I,M = [int(i) for i in str(UDIM)]

		sel = Uv.UvShellSelection() #assure the correct selection mask.
		if similar > 0:
			dissimilar = pm.polyUVStackSimilarShells(sel, tolerance=tolerance, onlyMatch=True)
			dissimilarUVs = [s.split(' ') for s in dissimilar] #
			dissimilarFaces = pm.polyListComponentConversion(dissimilarUVs, fromUV=1, toFace=1)
			pm.u3dLayout(dissimilarFaces, resolution=mapSize, preScaleMode=scale, preRotateMode=rotate, rotateStep=rotateStep, shellSpacing=.005, tileMargin=.005, packBox=[M-1, D, I, U]) #layoutScaleMode (int), multiObject (bool), mutations (int), packBox (float, float, float, float), preRotateMode (int), preScaleMode (int), resolution (int), rotateMax (float), rotateMin (float), rotateStep (float), shellSpacing (float), tileAssignMode (int), tileMargin (float), tileU (int), tileV (int), translate (bool)
		if similar is 2:
			pm.select(dissimilarFaces, toggle=1)
			similarFaces = pm.ls(sl=1)
			pm.polyUVStackSimilarShells(similarFaces, dissimilarFaces, tolerance=tolerance)

		else:
			pm.u3dLayout(sel, resolution=mapSize, preScaleMode=scale, preRotateMode=rotate, rotateStep=rotateStep, shellSpacing=.005, tileMargin=.005, packBox=[M-1, D, I, U]) #layoutScaleMode (int), multiObject (bool), mutations (int), packBox (float, float, float, float), preRotateMode (int), preScaleMode (int), resolution (int), rotateMax (float), rotateMin (float), rotateStep (float), shellSpacing (float), tileAssignMode (int), tileMargin (float), tileU (int), tileV (int), translate (bool)


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


	def tb002(self, state=None):
		'''
		Stack
		'''
		tb = self.currentUi.tb002
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Orient', setObjectName='chk021', setChecked=True, setToolTip='Orient UV shells to run parallel with the most adjacent U or V axis.')
			tb.menu_.add('QCheckBox', setText='Stack Similar', setObjectName='chk022', setChecked=True, setToolTip='Stack only shells that fall within the set tolerance.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='Tolerance: ', setObjectName='s000', setMinMax_='0.0-10 step.1', setValue=1.0, setToolTip='Stack shells with uv\'s within the given range.')
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

		Synopsis: u3dUnfold [flags] [String...]
		Flags:
		  -bi -borderintersection  on|off
		 -ite -iterations          Int
		  -ms -mapsize             Int
		   -p -pack                on|off
		  -rs -roomspace           Int
		  -tf -triangleflip        on|off

		Synopsis: u3dOptimize [flags] [String...]
		Flags:
		  -bi -borderintersection  on|off
		 -ite -iterations          Int
		  -ms -mapsize             Int
		 -pow -power               Int
		  -rs -roomspace           Int
		  -sa -surfangle           Float
		  -tf -triangleflip        on|off
		'''
		tb = self.currentUi.tb004
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Optimize', setObjectName='chk017', setToolTip='The Optimize UV Tool evens out the spacing between UVs on a mesh, fixing areas of distortion (overlapping UVs).')
			tb.menu_.add('QSpinBox', setPrefix='Optimize Amount: ', setObjectName='s008', setMinMax_='0-100 step1', setValue=25, setToolTip='The number of times to run optimize on the unfolded mesh.')
			return

		optimize = tb.menu_.chk017.isChecked()
		amount = tb.menu_.s008.value()

		pm.undo(openChunk=1)
		pm.u3dUnfold(iterations=1, pack=0, borderintersection=1, triangleflip=1, mapsize=2048, roomspace=0) #pm.mel.performUnfold(0)

		if optimize:
			u3dOptimize(iterations=amount, power=1, surfangle=1, borderintersection=0, triangleflip=1, mapsize=2048, roomspace=0) #pm.mel.performPolyOptimizeUV(0)
		pm.undo(closeChunk=1)


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

		if u and v:
			pm.mel.texStraightenUVs('UV', angle)
		elif u:
			pm.mel.texStraightenUVs('U', angle)
		elif v:
			pm.mel.texStraightenUVs('V', angle)

		if straightenShell:
			pm.mel.texStraightenShell()


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
			tb.menu_.add('QSpinBox', setPrefix='Map Size: ', setObjectName='s002', setMinMax_='512-8192 step512', setValue=2048, setToolTip='Set the map used as reference when getting texel density.')
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
		pm.mel.cutUvHardEdge()


	def b002(self):
		'''
		Transfer Uv's
		'''
		sel = pm.ls(orderedSelection=1, flatten=1)
		if len(sel)<2:
			Slots.messageBox('Error: The operation requires the selection of two polygon objects.')

		pm.undo(openChunk=1)
		from_ = sel[0]
		to = sel[1:]

		[pm.transferAttributes(from_, i, transferUVs=2) for i in to] # 0:no UV sets, 1:single UV set (specified by sourceUVSet and targetUVSet args), and 2:all UV sets are transferred.
		Slots.messageBox('Result: UV sets transferred from: {} to: {}.'.format(from_.name(), to.name()))
		pm.undo(closeChunk=1)


	def b005(self):
		'''
		Cut Uv'S
		'''
		objects = pm.ls(selection=1, objectsOnly=1, shapes=1, flatten=1)

		for obj in objects:
			sel = pm.ls(obj, sl=1)
			pm.polyMapCut(sel)


	@Init.attr
	def b011(self):
		'''
		Sew Uv'S
		'''
		objects = pm.ls(selection=1, objectsOnly=1, shapes=1, flatten=1)

		for obj in objects:
			sel = pm.ls(obj, sl=1)

			return pm.polyMapSew(sel) if len(objects)==1 else pm.polyMapSew(sel)
 

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
		sel = Uv.UvShellSelection() #assure the correct selection mask.

		pm.polyEditUV(sel, u=u, v=v, relative=relative)


	@staticmethod
	def UvShellSelection():
		'''
		Select all faces of any selected geometry, and switch the component mode to uv shell, 
		if the current selection is not maskFacet, maskUv, or maskUvShell.

		returns:
			(list) the selected faces.
		'''
		selection = pm.ls(sl=1)
		if not selection:
			Slots.messageBox('Error: Nothing selected.')

		objects = pm.ls(selection, objectsOnly=1)
		objectMode = pm.selectMode(query=1, object=1)

		maskFacet = pm.selectType(query=1, facet=1)
		maskUv = pm.selectType(query=1, polymeshUV=1)
		maskUvShell = pm.selectType(query=1, meshUVShell=1)

		if all((objects, objectMode)) or not any((objectMode, maskFacet, maskUv, maskUvShell)):

			for obj in objects:
				pm.selectMode(component=1)
				pm.selectType(meshUVShell=1)
				selection = Init.getComponents(obj, 'faces', flatten=False)
				pm.select(selection, add=True)

		return selection








#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------