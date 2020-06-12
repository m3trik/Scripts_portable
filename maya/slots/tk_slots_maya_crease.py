from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Crease(Init):
	def __init__(self, *args, **kwargs):
		super(Crease, self).__init__(*args, **kwargs)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya Crease Editors')

			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000
		
		files = ['Sets']
		contents = cmb.addItems_(files, 'Maya Crease Editors')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Crease Set Editor'):
				from maya.app.general import creaseSetEditor
				creaseSetEditor.showCreaseSetEditor()

			cmb.setCurrentIndex(0)


	def chk002(self):
		'''
		Un-Crease
		'''
		if self.parentUi.chk002.isChecked():
			self.parentUi.s003.setValue(0) #crease value
			self.parentUi.s004.setValue(180) #normal angle
			self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk003')
		else:
			self.parentUi.s003.setValue(7.5) #crease value
			self.parentUi.s004.setValue(30) #normal angle


	def chk003(self):
		'''
		Crease: Max
		'''
		if self.parentUi.chk003.isChecked():
			self.parentUi.s003.setValue(10) #crease value
			self.parentUi.s004.setValue(30) #normal angle
			self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk002')
		else:
			self.parentUi.s003.setValue(7.5) #crease value
			self.parentUi.s004.setValue(60) #normal angle


	def chk011(self):
		'''
		Crease: Auto
		'''
		if self.parentUi.chk011.isChecked():
			self.toggleWidgets(self.parentUi, self.childUi, setEnabled='s005,s006')
		else:
			self.toggleWidgets(self.parentUi, self.childUi, setDisabled='s005,s006')


	def tb000(self, state=None):
		'''
		Crease
		'''
		tb = self.currentUi.tb000
		if state=='setMenu':
			tb.add('QSpinBox', setPrefix='Crease Amount: ', setObjectName='s003', minMax_='0-10 step1', setValue=10, setToolTip='Crease amount 0-10. Overriden if "max" checked.')
			tb.add('QCheckBox', setText='Toggle Max', setObjectName='chk003', setChecked=True, setToolTip='Toggle crease amount from it\'s current value to the maximum amount.')
			tb.add('QCheckBox', setText='Un-Crease', setObjectName='chk002', setToolTip='Un-crease selected components or If in object mode, uncrease all.')
			tb.add('QCheckBox', setText='Perform Normal Edge Hardness', setObjectName='chk005', setChecked=True, setToolTip='Toggle perform normal edge hardness.')
			tb.add('QSpinBox', setPrefix='Edge Hardness Angle: ', setObjectName='s004', minMax_='0-180 step1', setValue=30, setToolTip='Normal edge hardness 0-180.')
			tb.add('QCheckBox', setText='Crease Vertex Points', setObjectName='chk004', setChecked=True, setToolTip='Crease vertex points.')
			tb.add('QCheckBox', setText='Auto Crease', setObjectName='chk011', setToolTip='Auto crease selected object(s) within the set angle tolerance.')
			tb.add('QSpinBox', setPrefix='Auto Crease: Low: ', setObjectName='s005', minMax_='0-180 step1', setValue=85, setToolTip='Auto crease: low angle constraint.')
			tb.add('QSpinBox', setPrefix='Auto Crease: high: ', setObjectName='s006', minMax_='0-180 step1', setValue=95, setToolTip='Auto crease: max angle constraint.')
			return

		creaseAmount = float(tb.s003.value())
		normalAngle = int(tb.s004.value()) 

		if tb.chk011.isChecked(): #crease: Auto
			angleLow = int(tb.s005.value()) 
			angleHigh = int(tb.s006.value()) 

			mel.eval("PolySelectConvert 2;") #convert selection to edges
			contraint = pm.polySelectConstraint( mode=3, type=0x8000, angle=True, anglebound=(angleLow, angleHigh) ) # to get edges with angle between two degrees. mode=3 (All and Next) type=0x8000 (edge). 

		operation = 0 #Crease selected components
		pm.polySoftEdge (angle=0, constructionHistory=0) #Harden edge normal
		if tb.chk002.isChecked():
			objectMode = pm.selectMode (query=True, object=True)
			if objectMode: #if in object mode,
				operation = 2 #2-Remove all crease values from mesh
			else:
				operation = 1 #1-Remove crease from sel components
				pm.polySoftEdge (angle=180, constructionHistory=0) #soften edge normal

		if tb.chk004.isChecked(): #crease vertex point
			pm.polyCrease (value=creaseAmount, vertexValue=creaseAmount, createHistory=True, operation=operation)
		else:
			pm.polyCrease (value=creaseAmount, createHistory=True, operation=operation) #PolyCreaseTool;

		if tb.chk005.isChecked(): #adjust normal angle
			pm.polySoftEdge (angle=normalAngle)

		if tb.chk011.isChecked(): #crease: Auto
			pm.polySelectConstraint( angle=False ) # turn off angle constraint


	def b000(self):
		'''
		Crease Set Transfer: Transform Node
		'''
		if self.parentUi.b001.isChecked():
			newObject = str(pm.ls(selection=1)) #ex. [nt.Transform(u'pSphere1')]

			index1 = newObject.find("u")
			index2 = newObject.find(")")
			newObject = newObject[index1+1:index2].strip("'") #ex. pSphere1

			if newObject != "[":
				self.parentUi.b001.setText(newObject)
			else:
				self.parentUi.b001.setText("must select obj first")
				self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='b001')
			if self.parentUi.b000.isChecked():
				self.toggleWidgets(self.parentUi, self.childUi, setEnabled='b052')
		else:
			self.parentUi.b001.setText("Object")


	def b001(self):
		'''
		Crease Set Transfer: Crease Set
		'''
		if self.parentUi.b000.isChecked():
			creaseSet = str(pm.ls(selection=1)) #ex. [nt.CreaseSet(u'creaseSet1')]

			index1 = creaseSet.find("u")
			index2 = creaseSet.find(")")
			creaseSet = creaseSet[index1+1:index2].strip("'") #ex. creaseSet1

			if creaseSet != "[":
				self.parentUi.b000.setText(creaseSet)
			else:
				self.parentUi.b000.setText("must select set first")
				self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='b000')
			if self.parentUi.b001.isChecked():
				self.toggleWidgets(self.parentUi, self.childUi, setEnabled='b052')
		else:
			self.parentUi.b000.setText("Crease Set")


	def b002(self):
		'''
		Transfer Crease Edges
		'''
		# an updated version of this is in the maya python projects folder
		# the use of separate buttons for donor and target mesh are obsolete
		# add pm.polySoftEdge (angle=0, constructionHistory=0); #harden edge, when applying crease
		
		creaseSet = str(self.parentUi.b000.text())
		newObject = str(self.parentUi.b001.text())

		sets = pm.sets (creaseSet, query=1)

		setArray = []
		for set_ in sets:
			name = str(set_)
			setArray.append(name)
		print(setArray)

		pm.undoInfo (openChunk=1)
		for set_ in setArray:
			oldObject = ''.join(set_.partition('.')[:1]) #ex. pSphereShape1 from pSphereShape1.e[260:299]
			pm.select (set_, replace=1)
			value = pm.polyCrease (query=1, value=1)[0]
			name = set_.replace(oldObject, newObject)
			pm.select (name, replace=1)
			pm.polyCrease (value=value, vertexValue=value, createHistory=True)
			# print("crease:", name)
		pm.undoInfo (closeChunk=1)

		self.toggleWidgets(self.parentUi, self.childUi, setDisabled='b052', setChecked_False='b000')#,self.parentUi.b001])
		self.parentUi.b000.setText("Crease Set")
		# self.parentUi.b001.setText("Object")









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------
#b008, b010, b011, b019, b024-27, b058, b059, b060