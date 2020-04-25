from __future__ import print_function
from tk_slots_max_init import *


import traceback
import os.path


class Display(Init):
	def __init__(self, *args, **kwargs):
		super(Display, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('display')



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


	def b000(self):
		'''
		Toggle Subdiv Proxy Display
		'''
		state = self.cycle([1,1,0], 'subdivProxy')
		try:
			mel.eval("smoothingDisplayToggle "+str(state))
		except:
			traceback.print_exc()
			print("# Warning: Nothing Selected. #")


	def b001(self):
		'''
		Toggle Visibility
		'''
		sel = [s for s in rt.getCurrentSelection()]

		for obj in sel:
			if obj.visibility == True:
				obj.visibility = False
			else:
				obj.visibility = True


	def b002(self):
		'''
		Hide Selected
		'''
		sel = [s for s in rt.getCurrentSelection()]
	
		for obj in sel:
			if not obj.isHiddenInVpt:
				obj.isHidden = True


	def b003(self):
		'''
		Show Selected
		'''
		sel = [s for s in rt.getCurrentSelection()]
	
		for obj in sel:
			if obj.isHiddenInVpt:
				obj.isHidden = False


	def b004(self):
		'''
		Show Geometry
		'''
		geometry = rt.geometry

		for obj in geometry:
			if obj.isHiddenInVpt:
				obj.isHidden = False


	def b005(self):
		'''
		Xray Selected
		'''
		sel = [s for s in rt.getCurrentSelection()]

		for s in sel:
			s.xray = True


	def b006(self):
		'''
		Un-Xray All
		'''
		geometry = [g for g in rt.geometry]

		for g in geometry:
			g.xray = False


	def b007(self):
		'''
		Xray Other
		'''
		sel = [s for s in rt.getCurrentSelection()]
		geometry = [g for g in rt.geometry]

		for g in geometry:
			if g not in sel:
				g.xray = True


	def b008(self):
		'''
		Filter Objects
		'''
		mel.eval("bt_filterActionWindow;")


	def b009(self):
		'''
		Override Material
		'''
		if self.ui.chk000.isChecked(): #override with UV checker material
			self.toggleMaterialOverride(checker=1)
		else:
			self.toggleMaterialOverride()


	def b010(self):
		'''
		
		'''
		pass


	def b011(self):
		'''
		Toggle Component ID Display
		'''
		index = self.cycle([0,1,2,3,4], 'componentID')

		visible = pm.polyOptions (query=1, displayItemNumbers=1)
		dinArray = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

		if index == 4:
			i=0
			for _ in range(4):
				if visible[i] == True:
					pm.polyOptions (relative=1, displayItemNumbers=dinArray[i], activeObjects=1)
				i+=1

		if visible[index] != True and index != 4:
			pm.polyOptions (relative=1, displayItemNumbers=dinArray[index], activeObjects=1)

			i=0
			for _ in range(4):
				if visible[i] == True and i != index:
					pm.polyOptions (relative=1, displayItemNumbers=dinArray[i], activeObjects=1)
				i+=1

		if index == 0:
			self.viewPortMessage("[1,0,0,0] <hl>vertIDs</hl>.")
		if index == 1:
			self.viewPortMessage("[0,1,0,0] <hl>edgeIDs</hl>.")
		if index == 2:
			self.viewPortMessage("[0,0,1,0] <hl>faceIDs</hl>.")
		if index == 3:
			self.viewPortMessage("[0,0,0,1] <hl>compIDs(UV)</hl>.")
		if index == 4:
			self.viewPortMessage("component ID <hl>Off</hl>.")


	def b012(self):
		'''
		Wireframe Non Active (Wireframe All But The Selected Item)
		'''
		viewport = rt.viewport.activeViewport

		state = self.cycle([0,1], 'wireframeInactive')

		if state:
			if not rt.viewport.isWire():
				self.maxUiSetChecked("415", 62, 163, True) #set viewport to wireframe
			self.maxUiSetChecked("40212", 62, 130, True) #Shade selected objects Checked
		else:
			self.maxUiSetChecked("40212", 62, 130, False) #Shade selected objects unchecked


	def b013(self):
		'''
		Viewport Configuration
		'''
		maxEval('actionMan.executeAction 0 "40023"')


	def b014(self):
		'''
		
		'''
		pass


	def b015(self):
		'''
		
		'''
		pass


	def b016(self):
		'''
		
		'''
		pass


	def b017(self):
		'''
		
		'''
		pass


	def b018(self):
		'''
		
		'''
		pass


	def b019(self):
		'''
		
		'''
		pass


	def b020(self):
		'''
		
		'''
		pass


	def b021(self):
		'''
		Template Selected
		'''
		sel = [s for s in rt.getCurrentSelection()]

		for obj in sel:
			if obj.isFrozen == True:
				obj.isFrozen = False
			else:
				obj.isFrozen = True


	def b022(self):
		'''
		
		'''
		pass


	def b023(self):
		'''
		
		'''
		pass


	def b024(self):
		'''
		Polygon Display Options
		'''
		mel.eval("CustomPolygonDisplayOptions")
		# mel.eval("polysDisplaySetup 1;")








#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------


