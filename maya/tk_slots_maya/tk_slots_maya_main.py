import maya.mel as mel
import pymel.core as pm

import os.path


from tk_slots_maya_init import Init




class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)



	def v000(self): #Extrude
		self.hotBox.sb.getMethod('polygons','b006')
		print "# Result: perform extrude #"

	def v001(self): #Bridge
		self.hotBox.sb.getMethod('polygons','b005')
		print "# Result: bridge #"

	def v002(self): #Multi-cut tool
		self.hotBox.sb.getMethod('polygons','b012')
		print "# Result: multi-cut #"

	def v003(self): #Delete history
		self.hotBox.sb.getMethod('edit','b016')
		print "# Result: delete history #"

	def v004(self): #Delete
		pm.delete()
		# self.hotBox.sb.getMethod('edit','b032')
		print "# Result: delete #"

	def v005(self): #
		pass

	def v006(self): #Toggle mode
		self.cycle('shortCutMode_01234')

	def v007(self): #Minimize main application
		mel.eval("minimizeApp;")
		self.hotBox.hbHide()


	def cmb000(self): #Display
		cmb = self.hotBox.ui.cmb000
		index = cmb.currentIndex() #get current index before refreshing list
		list_ = [
		'Toggle visibility', 
		'Hide Selected',
		'Show Selected',
		'Show Geometry',
		'XRay Selected',
		'Un-XRay All',
		'XRay Other',
		'Filter Objects',
		'Toggle Component ID Display',
		'Wireframe Non-Active',
		'Template selected',
		]
		self.comboBox (cmb, list_, "Display")

		if index!=0:
			if index==1: #Toggle visibility
				mel.eval('ToggleVisibilityAndKeepSelection();')

			if index==2: #Hide Selected
				mel.eval('HideSelectedObjects;')

			if index==3: #Show selected
				mel.eval('ShowSelectedObjects;')

			if index==4: #Show Geometry
				mel.eval('hideShow -geometry -show;')

			if index==5: #Xray selected
				mel.eval('''
				string $sel[] = `ls -sl -dag -s`;
				for ($object in $sel) 
					{
					int $xState[] = `displaySurface -query -xRay $object`;
					displaySurface -xRay ( !$xState[0] ) $object;
					}
				''')

			if index==6: #Un-Xray all
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

			if index==7: #Xray other
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

			if index==8: #Filter objects
				mel.eval("bt_filterActionWindow;")

			if index==9: #toggle component ID display
				index = self.cycle('componentID_01234')

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

			if index==10: #wireframe non active (wireframe all but the selected item)
				current_panel = pm.getPanel (withFocus=1)
				state = pm.modelEditor (current_panel, query=1, activeOnly=1)
				pm.modelEditor (current_panel, edit=1, activeOnly=not state)

			if index==11: #Template selected
				mel.eval("toggle -template;")

			if index==12:
				pass

			if index==13:
				pass

			if index==14:
				pass

			if index==15:
				pass

			cmb.setCurrentIndex(0)



	def cmb001(self): #Recent Commands
		cmb = self.hotBox.ui.cmb001
		index = cmb.currentIndex() #get current index before refreshing list
		list_ = [dict_.values() for dict_ in self.hotBox.prevCommand] #ie. get value 'muti-cut tool' form [{'b000':'multi-cut tool'}]
		self.comboBox (cmb, list_, "Recent")

		if index!=0:
			for key in self.hotBox.prevCommand[index]:
				key()
			cmb.setCurrentIndex(0)




#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------