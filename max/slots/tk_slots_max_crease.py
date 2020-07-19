from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Crease(Init):
	def __init__(self, *args, **kwargs):
		super(Crease, self).__init__(*args, **kwargs)

		self.creaseValue = 10


	@Slots.sync
	def s003(self, value=None):
		'''
		Crease Amount
		Tracks the standard crease amount while toggles such as un-crease, and crease max temporarily change the spinbox value. 
		'''
		if not self.crease.chk002.isChecked(): #un-crease
			if not self.crease.chk003.isChecked(): #toggle max
				self.creaseValue = self.crease.s003.value()
				text = self.ui.tb000.text().split(' ')[0]
				self.ui.tb000.setText('{} {}'.format(text, self.creaseValue))


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.crease.pin

		if state is 'setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.crease.cmb000

		if index is 'setMenu':
			list_ = ['']
			items = cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	@Slots.sync
	def chk002(self, state=None):
		'''
		Un-Crease
		'''
		if self.ui.chk002.isChecked():
			self.crease.s003.setValue(0) #crease value
			self.crease.s004.setValue(180) #normal angle
			self.toggleWidgets(setChecked='chk002', setUnChecked='chk003')
			self.crease.s003.setDisabled(True)
			self.ui.tb000.setText('Un-Crease 0')
		else:
			self.crease.s003.setValue(self.creaseValue) #crease value
			self.crease.s004.setValue(30) #normal angle
			self.crease.s003.setEnabled(True)
			self.ui.tb000.setText('{} {}'.format('Crease', self.creaseValue))


	@Slots.sync
	def chk003(self, state=None):
		'''
		Crease: Max
		'''
		if self.ui.chk003.isChecked():
			self.crease.s003.setValue(10) #crease value
			self.crease.s004.setValue(30) #normal angle
			self.toggleWidgets(setChecked='chk003', setUnChecked='chk002')
			self.crease.s003.setDisabled(True)
			self.ui.tb000.setText('Crease 10')
		else:
			self.crease.s003.setValue(self.creaseValue) #crease value
			self.crease.s004.setValue(60) #normal angle
			self.crease.s003.setEnabled(True)
			self.ui.tb000.setText('{} {}'.format('Crease', self.creaseValue))


	@Slots.sync
	def chk011(self, state=None):
		'''
		Crease: Auto
		'''
		if self.ui.chk011.isChecked():
			self.toggleWidgets(setEnabled='s005,s006')
		else:
			self.toggleWidgets(setDisabled='s005,s006')


	def tb000(self, state=None):
		'''
		Crease
		'''
		tb = self.ui.tb000
		if state is 'setMenu':
			tb.add('QSpinBox', setPrefix='Crease Amount: ', setObjectName='s003', minMax_='0-10 step1', setValue=10, setToolTip='Crease amount 0-10. Overriden if "max" checked.')
			tb.add('QCheckBox', setText='Toggle Max', setObjectName='chk003', setToolTip='Toggle crease amount from it\'s current value to the maximum amount.')
			tb.add('QCheckBox', setText='Un-Crease', setObjectName='chk002', setToolTip='Un-crease selected components or If in object mode, uncrease all.')
			tb.add('QCheckBox', setText='Perform Normal Edge Hardness', setObjectName='chk005', setChecked=True, setToolTip='Toggle perform normal edge hardness.')
			tb.add('QSpinBox', setPrefix='Edge Hardness Angle: ', setObjectName='s004', minMax_='0-180 step1', setValue=30, setToolTip='Normal edge hardness 0-180.')
			tb.add('QCheckBox', setText='Crease Vertex Points', setObjectName='chk004', setToolTip='Crease vertex points.')
			tb.add('QCheckBox', setText='Auto Crease', setObjectName='chk011', setToolTip='Auto crease selected object(s) within the set angle tolerance.')
			tb.add('QSpinBox', setPrefix='Auto Crease: Low: ', setObjectName='s005', minMax_='0-180 step1', setValue=85, setToolTip='Auto crease: low angle constraint.')
			tb.add('QSpinBox', setPrefix='Auto Crease: high: ', setObjectName='s006', minMax_='0-180 step1', setValue=95, setToolTip='Auto crease: max angle constraint.')
			
			self.toggleWidgets(tb, setDisabled='s005,s006')
			return

		creaseAmount = int(tb.s003.value())
		normalAngle = int(tb.s004.value())

		# if tb.chk011.isChecked(): #crease: Auto
		# 	angleLow = int(tb.s005.value()) 
		# 	angleHigh = int(tb.s006.value()) 

		# 	mel.eval("PolySelectConvert 2;") #convert selection to edges
		# 	contraint = pm.polySelectConstraint( mode=3, type=0x8000, angle=True, anglebound=(angleLow, angleHigh) ) # to get edges with angle between two degrees. mode=3 (All and Next) type=0x8000 (edge). 

		creaseAmount = creaseAmount*0.1 #convert to max 0-1 range

		for obj in rt.selection:
			if rt.classOf(obj)=='Editable_Poly':

				if tb.chk011.isChecked(): #crease: Auto
					minAngle = int(tb.s005.value()) 
					maxAngle = int(tb.s006.value()) 

					edgelist = self.getEdgesByAngle(minAngle, maxAngle)
					rt.polyOp.setEdgeSelection(obj, edgelist)

				if tb.chk004.isChecked(): #crease vertex point
					obj.EditablePoly.setVertexData(1, creaseAmount)
				else: #crease edge
					obj.EditablePoly.setEdgeData(1, creaseAmount)

				if tb.chk005.isChecked(): #adjust normal angle
					edges = rt.polyop.getEdgeSelection(obj)
					for edge in edges:
						edgeVerts = rt.polyop.getEdgeVerts(obj, edge)
						normal = rt.averageSelVertNormal(obj)
						for vertex in edgeVerts:
							rt.setNormal(obj, vertex, normal)
			else:
				print('Error: object type '+rt.classOf(obj)+' is not supported.')


	def b000(self):
		'''
		Crease Set Transfer: Transform Node
		'''
		if self.crease.b000.isChecked():
			creaseSet = str(pm.ls(selection=1)) #ex. [nt.CreaseSet(u'creaseSet1')]

			index1 = creaseSet.find("u")
			index2 = creaseSet.find(")")
			creaseSet = creaseSet[index1+1:index2].strip("'") #ex. creaseSet1

			if creaseSet != "[":
				self.crease.b000.setText(creaseSet)
			else:
				self.crease.b000.setText("must select set first")
				self.toggleWidgets(setUnChecked='b000')
			if self.crease.b001.isChecked():
				self.toggleWidgets(setEnabled='b052')
		else:
			self.crease.b000.setText("Crease Set")


	def b001(self):
		'''
		Crease Set Transfer: Crease Set
		'''
		if self.crease.b001.isChecked():
			newObject = str(pm.ls(selection=1)) #ex. [nt.Transform(u'pSphere1')]

			index1 = newObject.find("u")
			index2 = newObject.find(")")
			newObject = newObject[index1+1:index2].strip("'") #ex. pSphere1

			if newObject != "[":
				self.crease.b001.setText(newObject)
			else:
				self.crease.b001.setText("must select obj first")
				self.toggleWidgets(setUnChecked='b001')
			if self.crease.b000.isChecked():
				self.toggleWidgets(setEnabled='b052')
		else:
			self.crease.b001.setText("Object")


	def b002(self):
		'''
		Transfer Crease Edges
		'''
		# an updated version of this is in the maya python projects folder
		# the use of separate buttons for donor and target mesh are obsolete
		# add pm.polySoftEdge (angle=0, constructionHistory=0); #harden edge, when applying crease 

		creaseSet = str(self.crease.b000.text())
		newObject = str(self.crease.b001.text())

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

		self.toggleWidgets(setDisabled='b052', setUnChecked='b000')#,self.crease.b001])
		self.crease.b000.setText("Crease Set")
		# self.crease.b001.setText("Object")








#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------