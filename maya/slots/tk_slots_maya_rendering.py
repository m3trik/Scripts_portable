from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Rendering(Init):
	def __init__(self, *args, **kwargs):
		super(Rendering, self).__init__(*args, **kwargs)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb001', setToolTip='')

			return


	def cmb001(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000
		
		files = ['']
		contents = cmb.addItems_(files, '')

		# if not index:
		# 	index = cmb.currentIndex()
		# if index!=0:
		# 	if index==contents.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def cmb000(self):
		'''
		Render: camera
		'''
		cmb = self.parentUi.cmb000

		# self.cams = [cam for cam in rt.cameras if 'Target' not in str(cam)]
		# if self.cams:
		# 	list_ = [str(cam.name) for cam in self.cams] #camera names
		# 	contents = cmb.addItems_(list_)


	def b000(self):
		'''
		Render Current Frame
		'''
		cmb = self.parentUi.cmb000
		index = cmb.currentIndex()

		try:
			rt.render (camera=self.cams[index]) #render with selected camera
		except:
			mel.eval('RenderIntoNewWindow;')


	def b001(self):
		'''
		Open Render Settings Window
		'''
		mel.eval('unifiedRenderGlobalsWindow;')


	def b002(self):
		'''
		Redo Previous Render
		'''
		mel.eval('redoPreviousRender render;')


	def b003(self):
		'''
		Editor: Render Setup
		'''
		mel.eval('RenderSetupWindow;')


	def b004(self):
		'''
		Editor: Rendering Flags
		'''
		mel.eval('renderFlagsWindow;')


	def b005(self):
		'''
		Apply Vray Attributes To Selected Objects
		'''
		selection = pm.ls(selection=1)
		currentID=1
		for obj in selection:
			# get renderable shape nodes relative to transform, iterate through and apply subdivision
			shapes = pm.listRelatives(obj,s=1,ni=1)
			if shapes:
				for shape in shapes:
					mel.eval ("vray addAttributesFromGroup "+shape+" vray_subdivision 1;")
					mel.eval ("vray addAttributesFromGroup "+shape+" vray_subquality 1;")
			# apply object ID to xform. i don't like giving individual shapes IDs.
			mel.eval ("vray addAttributesFromGroup "+obj+" vray_objectID 1;")
			pm.setAttr(obj+'.vrayObjectID',currentID)
			currentID+=1


	@Slots.message
	def b006(self):
		'''
		Load Vray Plugin
		'''
		vray = ['vrayformaya.mll','vrayformayapatch.mll']
		if pm.pluginInfo ('vrayformaya.mll', query=1, loaded=1):
			try:
				pm.unloadPlugin(vray)
			except:
				pm.unloadPlugin(vray, force=1)
				return '{0}{1}{2}'.format(" Result: Force unloadPlugin:", str(vray), " ")
		else:
			pm.loadPlugin (vray)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------