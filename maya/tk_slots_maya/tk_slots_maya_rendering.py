import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





#                                  dP                   oo                   
#                                  88                                        
# 88d888b. .d8888b. 88d888b. .d888b88 .d8888b. 88d888b. dP 88d888b. .d8888b. 
# 88'  `88 88ooood8 88'  `88 88'  `88 88ooood8 88'  `88 88 88'  `88 88'  `88 
# 88       88.  ... 88    88 88.  .88 88.  ... 88       88 88    88 88.  .88 
# dP       `88888P' dP    dP `88888P8 `88888P' dP       dP dP    dP `8888P88 
#                                                                        .88 
#                                                                    d8888P  
#
class Rendering(Init):
	def __init__(self, *args, **kwargs):
		super(Rendering, self).__init__(*args, **kwargs)


		

		#checkable comboBox not working
		comboBox = self.CheckableComboBox(self.hotBox.ui.cmb000)
		for num in range(6):
			comboBox.addItem("checkbox " + str(num))
		comboBox.checkIndex(1)
		comboBox.checkIndex(2)

	def b000(self): #render current frame
		mel.eval('RenderIntoNewWindow;')

	def b001(self): #Open render settings window
		mel.eval('unifiedRenderGlobalsWindow;')

	def b002(self): #Redo previous render
		mel.eval('redoPreviousRender render;')

	def b003(self): #Editor: Render setup
		mel.eval('RenderSetupWindow;')

	def b004(self): #Editor: Rendering flags
		mel.eval('renderFlagsWindow;')

	def b005(self): #Apply VRay attributes to selected objects
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

	def b006(self): #load vray plugin
		vray = ['vrayformaya.mll','vrayformayapatch.mll']
		if pm.pluginInfo ('vrayformaya.mll', query=1, loaded=1):
			try:
				pm.unloadPlugin(vray)
			except:
				print "# Result: Force unloadPlugin:"+str(vray)+" #"
				pm.unloadPlugin(vray, force=1)
		else:
			pm.loadPlugin (vray)

	def b007(self): #
		mel.eval('')

	def b008(self): #
		mel.eval("")

	def b009(self): #
		mel.eval('')



#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------