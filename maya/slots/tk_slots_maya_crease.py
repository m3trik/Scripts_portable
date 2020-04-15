from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Crease(Init):
	def __init__(self, *args, **kwargs):
		super(Crease, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('crease')
		self.submenu = self.sb.getUi('crease_submenu')



	def chk002(self):
		'''
		Un-Crease
		'''
		if self.ui.chk002.isChecked():
			self.ui.s003.setValue(0) #crease value
			self.ui.s004.setValue(180) #normal angle
			self.toggleWidgets(self.ui, self.submenu, setChecked_False='chk003')
		else:
			self.ui.s003.setValue(7.5) #crease value
			self.ui.s004.setValue(30) #normal angle


	def chk003(self):
		'''
		Crease: Max
		'''
		if self.ui.chk003.isChecked():
			self.ui.s003.setValue(10) #crease value
			self.ui.s004.setValue(30) #normal angle
			self.toggleWidgets(self.ui, self.submenu, setChecked_False='chk002')
		else:
			self.ui.s003.setValue(7.5) #crease value
			self.ui.s004.setValue(60) #normal angle


	def chk011(self):
		'''
		Crease: Auto
		'''
		if self.ui.chk011.isChecked():
			self.toggleWidgets(self.ui, self.submenu, setEnabled='s005,s006')
		else:
			self.toggleWidgets(self.ui, self.submenu, setDisabled='s005,s006')


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['Sets']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Crease Set Editor'):
				from maya.app.general import creaseSetEditor
				creaseSetEditor.showCreaseSetEditor()

			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Crease
		'''
		creaseAmount = float(self.ui.s003.value())
		normalAngle = int(self.ui.s004.value()) 

		if self.ui.chk011.isChecked(): #crease: Auto
			angleLow = int(self.ui.s005.value()) 
			angleHigh = int(self.ui.s006.value()) 

			mel.eval("PolySelectConvert 2;") #convert selection to edges
			contraint = pm.polySelectConstraint( mode=3, type=0x8000, angle=True, anglebound=(angleLow, angleHigh) ) # to get edges with angle between two degrees. mode=3 (All and Next) type=0x8000 (edge). 

		operation = 0 #Crease selected components
		pm.polySoftEdge (angle=0, constructionHistory=0) #Harden edge normal
		if self.ui.chk002.isChecked():
			objectMode = pm.selectMode (query=True, object=True)
			if objectMode: #if in object mode,
				operation = 2 #2-Remove all crease values from mesh
			else:
				operation = 1 #1-Remove crease from sel components
				pm.polySoftEdge (angle=180, constructionHistory=0) #soften edge normal

		if self.ui.chk004.isChecked(): #crease vertex point
			pm.polyCrease (value=creaseAmount, vertexValue=creaseAmount, createHistory=True, operation=operation)
		else:
			pm.polyCrease (value=creaseAmount, createHistory=True, operation=operation) #PolyCreaseTool;

		if self.ui.chk005.isChecked(): #adjust normal angle
			pm.polySoftEdge (angle=normalAngle)

		if self.ui.chk011.isChecked(): #crease: Auto
			pm.polySelectConstraint( angle=False ) # turn off angle constraint









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------
#b008, b010, b011, b019, b024-27, b058, b059, b060