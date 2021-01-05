from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Cameras(Init):
	def __init__(self, *args, **kwargs):
		super(Cameras, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('cameras')
		self.childUi = self.sb.getUi('cameras_submenu')


	@property
	def clippingMenu(self):
		'''Menu: Camera clip plane settings.

		:Return:
			(obj) menu as a property.
		'''
		if not hasattr(self, '_clippingMenu'):
			self._clippingMenu = wgts.TkMenu(self.currentUi, position='cursorPos')

			self._clippingMenu.add(wgts.TkLabel, setText='Viewport Clip', setObjectName='lbl000', setToolTip='Toggle the clipping controls for the current viewport camera.')
			self._clippingMenu.add('QPushButton', setText='Auto Clip', setObjectName='chk000', setCheckable=True, setToolTip='When Auto Clip is ON, geometry closer to the camera than 3 units is not displayed. Turn OFF to manually define.')
			self._clippingMenu.add('QDoubleSpinBox', setPrefix='Far Clip:  ', setObjectName='s000', setMinMax_='.01-10 step.1', setToolTip='Adjust the current cameras near clipping plane.')
			self._clippingMenu.add('QSpinBox', setPrefix='Near Clip: ', setObjectName='s001', setMinMax_='10-10000 step1', setToolTip='Adjust the current cameras far clipping plane.')

		#set widget states for the current activeCamera
		activeCamera = rt.getActiveCamera()
		if not activeCamera:
			self.toggleWidgets(self._clippingMenu, setDisabled='s000-1,chk000')
		elif activeCamera.clipManually: #if clipManually is active:
			self._clippingMenu.chk000.setChecked(True)
			self.toggleWidgets(self._clippingMenu, setDisabled='s000-1')
		nearClip = activeCamera.nearClip if activeCamera else 1.0
		farClip = activeCamera.farClip  if activeCamera else 1000.0

		self._clippingMenu.s000.setValue(nearClip)
		self._clippingMenu.s001.setValue(farClip)

		return self._clippingMenu


	def lbl000(self):
		'''Camera Clipping: Viewport
		'''
		maxEval('actionMan.executeAction 0 "374"') #Tools: Viewport Clipping


	@Slots.message
	def chk000(self, state=None):
		'''Camera Clipping: Auto Clip
		'''
		if self.clippingMenu.chk000.isChecked():
			self.toggleWidgets(self.clippingMenu, setDisabled='s000-1')
		else:
			self.toggleWidgets(self.clippingMenu, setEnabled='s000-1')

		activeCamera = rt.getActiveCamera()
		if not activeCamera:
			return 'Error: No Active Camera.'

		activeCamera.clipManually(False)


	def s000(self, value=None):
		'''Camera Clipping: Near Clip
		'''
		value = self.clippingMenu.s000.value()

		activeCamera = rt.getActiveCamera()
		if not activeCamera:
			return 'Error: No Active Camera.'

		activeCamera.nearClip = value


	def s001(self, value=None):
		'''Camera Clipping: Far Clip
		'''
		value = self.clippingMenu.s001.value()

		activeCamera = rt.getActiveCamera()
		if not activeCamera:
			return 'Error: No Active Camera.'

		activeCamera.farClip = value


	def tree000(self, wItem=None, column=None):
		''''''
		tree = self.parentUi.tree000

		if wItem is 'setMenu':
			tree.expandOnHover = True
			tree.convert(tree.getTopLevelItems(), 'QLabel') #convert any existing contents.

			l = []
			[tree.add('QLabel', 'Editors', setText=s) for s in l]
			return

		if not any([wItem, column]): #refresh list items -----------------------------
			try:
				l = [str(cam.name) for cam in rt.cameras if 'Target' not in cam.name] #List scene Cameras
			except AttributeError:
				l=[]
			[tree.add('QLabel', 'Cameras', refresh=True, setText=s) for s in l]
			return

		widget = tree.getWidget(wItem, column)
		text = tree.getWidgetText(wItem, column)
		header = tree.getHeaderFromColumn(column)

		if header=='Create':
			if text=='Custom Camera':
				rt.StartObjectCreation(rt.Physical_Camera)
			if text=='Set Custom Camera':
				maxEval('Try(viewport.setcamera $) Catch()')
			if text=='Camera From View':
				maxEval('macros.run "Lights and Cameras" "PhysicalCamera_CreateFromView"')

		if header=='Cameras':
			cam = rt.getNodeByName(text)
			rt.select(cam) #select the camera
			rt.viewport.setCamera(cam) #set viewport to camera
			rt.redrawViews()

		if header=='Options':
			if text=='Group Cameras':
				self.groupCameras()
			if text=='Adjust Clipping':
				self.clippingMenu.show()
			if text=='Toggle Safe Frames':
				maxEval('actionMan.executeAction 0 "219"') #Tools: Viewport Safeframes Toggle


	def v000(self):
		'''Cameras: Back View
		'''
		maxEval("max vpt back")


	def v001(self):
		'''Cameras: Top View
		'''
		maxEval("max vpt top")


	def v002(self):
		'''Cameras: Right View
		'''
		maxEval("max vpt right")


	def v003(self):
		'''Cameras: Left View
		'''
		maxEval("max vpt left")


	def v004(self):
		'''Cameras: Perspective View
		'''
		maxEval("max vpt persp user")


	def v005(self):
		'''Cameras: Front View
		'''
		maxEval("max vpt front")


	def v006(self):
		'''Cameras: Bottom View
		'''
		maxEval("max vpt bottom")


	def v007(self):
		'''Cameras: Align View
		'''
		maxEval('''
		max vpt iso user
		max align camera
		''')


	def v008(self):
		''''''
		pass


	def v009(self):
		''''''
		pass


	def v010(self):
		'''Camera: Dolly
		'''
		maxEval("max dolly mode")


	def v011(self):
		'''Camera: Roll
		'''
		maxEval("max roll")


	def v012(self):
		'''Camera: Truck
		'''
		maxEval("max truck")


	def v013(self):
		'''Camera: Orbit
		'''
		maxEval("max pancamera")


	def v014(self):
		''''''
		pass


	def v015(self):
		''''''
		pass


	@staticmethod
	def groupCameras():
		'''Group Cameras
		'''
		cameras = [cam for cam in rt.cameras] #List scene Cameras

		layer = rt.LayerManager.getLayerFromName("Cameras")
		if not layer:
			layer = rt.LayerManager.NewLayerFromName("Cameras")

		for cam in cameras:
			layer.addnode(cam)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------



# deprecated ------------------------------------


# def tree000(self, wItem=None, column=None):
# 		'''
		
# 		'''
# 		tree = self.parentUi.tree000

# 		if not any([wItem, column]): #populate the tree columns.
# 			if not tree.refresh: #static list items -----------
# 				tree.expandOnHover = True
# 				tree.convert(tree.getTopLevelItems(), 'QLabel') #convert any existing contents.

# 				l = []
# 				[tree.add('QLabel', 'Editors', setText=s) for s in l]

# 			#refreshed list items -----------------------------
# 			try:
# 				l = [str(cam.name) for cam in rt.cameras if 'Target' not in cam.name] #List scene Cameras
# 			except AttributeError: l=[]
# 			[tree.add('QLabel', 'Cameras', refresh=True, setText=s) for s in l]

# 			return

# 		widget = tree.getWidget(wItem, column)
# 		text = tree.getWidgetText(wItem, column)
# 		header = tree.getHeaderFromColumn(column)

# 		if header=='Create':
# 			if text=='Custom Camera':
# 				rt.StartObjectCreation(rt.Physical_Camera)
# 			if text=='Set Custom Camera':
# 				maxEval('Try(viewport.setcamera $) Catch()')
# 			if text=='Camera From View':
# 				maxEval('macros.run "Lights and Cameras" "PhysicalCamera_CreateFromView"')

# 		if header=='Cameras':
# 			cam = rt.getNodeByName(text)
# 			rt.select(cam) #select the camera
# 			rt.viewport.setCamera(cam) #set viewport to camera
# 			rt.redrawViews()

# 		if header=='Options':
# 			if text=='Group Cameras':
# 				self.groupCameras()
# 			if text=='Adjust Clipping':
# 				self.clippingMenu.show()
# 			if text=='Toggle Safe Frames':
# 				maxEval('actionMan.executeAction 0 "219"') #Tools: Viewport Safeframes Toggle



	# def cmb001(self, index=None):
	# 	'''
	# 	Cameras
	# 	'''
	# 	cmb = self.parentUi.cmb001
		
	# 	cameras = [cam.name for cam in rt.cameras if 'Target' not in cam.name] #List scene Cameras
	# 	contents = cmb.addItems_(cameras, "Cameras:")
		
	# 	if not index:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		cam = rt.getNodeByName(contents[index])
	# 		rt.select (cam) #select the camera
	# 		rt.viewport.setCamera (cam) #set viewport to camera
	# 		cmb.setCurrentIndex(0)
	# 		rt.redrawViews()


	# def cmb002(self, index=None):
	# 	'''
	# 	Create
	# 	'''
	# 	cmb = self.parentUi.cmb002
		
	# 	list_ = ['Custom Camera','Set Custom Camera','Camera From View']
	# 	contents = cmb.addItems_(list_, "Create")

	# 	if not index:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		if index==1:
	# 			rt.StartObjectCreation(rt.Physical_Camera)
	# 		if index==2:
	# 			maxEval('Try(viewport.setcamera $) Catch()')
	# 		if index==3:
	# 			maxEval('macros.run "Lights and Cameras" "PhysicalCamera_CreateFromView")
	# 		cmb.setCurrentIndex(0)


	# def cmb003(self, index=None):
	# 	'''
	# 	Options
	# 	'''
	# 	cmb = self.parentUi.cmb003
		
	# 	list_ = ['Group Cameras']
	# 	contents = cmb.addItems_(list_, "Options")

	# 	if not index:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		if index==1:
	# 			cameras = [cam for cam in rt.cameras] #List scene Cameras

	# 			layer = rt.LayerManager.getLayerFromName ("Cameras")
	# 			if not layer:
	# 				layer = rt.LayerManager.NewLayerFromName("Cameras")

	# 			for cam in cameras:
	# 				layer.addnode(cam)
	# 		cmb.setCurrentIndex(0)


