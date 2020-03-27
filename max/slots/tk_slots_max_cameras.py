from __future__ import print_function
from tk_slots_max_init import Init
maxEval = Init.maxEval

import os.path



class Cameras(Init):
	def __init__(self, *args, **kwargs):
		super(Cameras, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('cameras')

		self.tree000()


	def tree000(self, wItem=None, column=None):
		'''
		Cameras
		'''
		tree = self.ui.tree000

		if not any([wItem, column]):
			tree.convert(tree.getTopLevelItems(), 'QPushButton')

			l = ['Custom Camera','Set Custom Camera','Camera From View']
			[tree.add('QPushButton', 'Create', setText=t) for t in l]

			l = ['camera'+str(i) for i in range(8)] #List scene Cameras
			[tree.add('QPushButton', 'Cameras', setText=t) for t in l]
			# l = [cam.name for cam in rt.cameras if 'Target' not in cam.name] #List scene Cameras
			# [w.add('QPushButton', 'Cameras', setText=t) for t in l]

			l = ['test'+str(i) for i in range(6)]
			test = tree.add('QPushButton', 'Cameras', parent_='Test', setText='Options')
			[tree.add('QPushButton', test, setText=t) for t in l]

		else:
			# widget = tree.getWidget(wItem, column)
			text = tree.getWidgetText(wItem, column)
			header = tree.getHeaderFromColumn(column)
			print(header, text, column)

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
				cmb.setCurrentIndex(0)
				rt.redrawViews()


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	# def cmb001(self, index=None):
	# 	'''
	# 	Cameras
	# 	'''
	# 	cmb = self.ui.cmb001
		
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
	# 	cmb = self.ui.cmb002
		
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
	# 			maxEval('macros.run "Lights and Cameras" "PhysicalCamera_CreateFromView"')
	# 		cmb.setCurrentIndex(0)


	def cmb003(self, index=None):
		'''
		Options
		'''
		cmb = self.ui.cmb003
		
		list_ = ['Group Cameras']
		contents = cmb.addItems_(list_, "Options")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==1:
				cameras = [cam for cam in rt.cameras] #List scene Cameras

				layer = rt.LayerManager.getLayerFromName ("Cameras")
				if not layer:
					layer = rt.LayerManager.NewLayerFromName("Cameras")

				for cam in cameras:
					layer.addnode(cam)
			cmb.setCurrentIndex(0)



	def v000(self):
		'''
		Cameras: Back View
		'''
		maxEval("max vpt back")


	def v001(self):
		'''
		Cameras: Top View
		'''
		maxEval("max vpt top")


	def v002(self):
		'''
		Cameras: Right View
		'''
		maxEval("max vpt right")


	def v003(self):
		'''
		Cameras: Left View
		'''
		maxEval("max vpt left")


	def v004(self):
		'''
		Cameras: Perspective View
		'''
		maxEval("max vpt persp user")


	def v005(self):
		'''
		Cameras: Front View
		'''
		maxEval("max vpt front")


	def v006(self):
		'''
		Cameras: Bottom View
		'''
		maxEval("max vpt bottom")


	def v007(self):
		'''
		Cameras: Align View
		'''
		maxEval('''
		max vpt iso user
		max align camera
		''')


	def v008(self):
		'''

		'''
		pass


	def v009(self):
		'''

		'''
		pass


	def v010(self):
		'''
		Camera: Dolly
		'''
		maxEval("max dolly mode")


	def v011(self):
		'''
		Camera: Roll
		'''
		maxEval("max roll")


	def v012(self):
		'''
		Camera: Truck
		'''
		maxEval("max truck")


	def v013(self):
		'''
		Camera: Orbit
		'''
		maxEval("max pancamera")


	def v014(self):
		'''
		
		'''
		pass


	def v015(self):
		'''
		
		'''
		pass








#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

