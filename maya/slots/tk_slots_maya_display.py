from tk_slots_maya_init import Init

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
				mel.eval('')
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		
		'''
		pass


	def b001(self):
		'''
		Toggle Visibility
		'''
		mel.eval('ToggleVisibilityAndKeepSelection();')


	def b002(self):
		'''
		Hide Selected
		'''
		mel.eval('HideSelectedObjects;')


	def b003(self):
		'''
		Show Selected
		'''
		mel.eval('ShowSelectedObjects;')


	def b004(self):
		'''
		Show Geometry
		'''
		mel.eval('hideShow -geometry -show;')


	def b005(self):
		'''
		Xray Selected
		'''
		mel.eval('''
		string $sel[] = `ls -sl -dag -s`;
		for ($object in $sel) 
			{
			int $xState[] = `displaySurface -query -xRay $object`;
			displaySurface -xRay ( !$xState[0] ) $object;
			}
		''')


	def b006(self):
		'''
		Un-Xray All
		'''
		mel.eval('''
		string $scene[] = `ls -visible -flatten -dag -noIntermediate -type surfaceShape`;
		for ($object in $scene)
			{
			int $state[] = `displaySurface -query -xRay $object`;
			if ($state[0] == 1)
				{
				displaySurface -xRay 0 $object;
				}
			}
		''')


	def b007(self):
		'''
		Xray Other
		'''
		mel.eval('''
		//xray all except currently selected
		{
		string $scene[] = `ls -visible -flatten -dag -noIntermediate -type surfaceShape`;
		string $selection[] = `ls -selection -dagObjects -shapes`;
		for ($object in $scene)
			{
			if (!stringArrayContains ($object, $selection))
				{
				int $state[] = `displaySurface -query -xRay $object`;
				displaySurface -xRay ( !$state[0] ) $object;
				}
			}
		}
		''')


	def b008(self):
		'''
		Filter Objects
		'''
		mel.eval("bt_filterActionWindow;")


	def b009(self):
		'''
		
		'''
		pass


	def b010(self):
		'''
		
		'''
		pass


	def b011(self):
		'''
		Toggle Component Id Display
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
		current_panel = pm.getPanel (withFocus=1)
		state = pm.modelEditor (current_panel, query=1, activeOnly=1)
		pm.modelEditor (current_panel, edit=1, activeOnly=not state)


	def b013(self):
		'''
		
		'''
		pass


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
		mel.eval("toggle -template;")


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
		
		'''
		pass






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------
	
