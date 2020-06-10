from __future__ import print_function
from tk_slots_max_init import *

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
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='')

			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000
		
		list_ = ['']
		items = cmb.addItems_(list_, '')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def chk002(self):
		'''
		Un-Crease
		'''
		if self.parentUi.chk002.isChecked():
			self.parentUi.s003.setValue(0) #crease value
			self.parentUi.s004.setValue(180) #normal angle
			self.toggleWidgets(self.parentUi, self.childUi, setChecked='chk002', setChecked_False='chk003')
		else:
			self.parentUi.s003.setValue(5) #crease value
			self.parentUi.s004.setValue(60) #normal angle


	def chk003(self):
		'''
		Crease: Max
		'''
		if self.parentUi.chk003.isChecked():
			self.parentUi.s003.setValue(10) #crease value
			self.parentUi.s004.setValue(30) #normal angle
			self.toggleWidgets(self.parentUi, self.childUi, setChecked='chk003', setChecked_False='chk002')
		else:
			self.parentUi.s003.setValue(5) #crease value
			self.parentUi.s004.setValue(60) #normal angle


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

		creaseAmount = int(tb.s003.value())
		normalAngle = int(tb.s004.value())

		creaseAmount = creaseAmount*0.1 #convert to max 0-1 range

		for obj in rt.selection:
			if rt.classOf(obj)=='Editable_Poly':

				if tb.chk011.isChecked(): #crease: Auto
					minAngle = int(tb.s005.value()) 
					maxAngle = int(tb.s006.value()) 

					edgelist = self.getEdgesByAngle(minAngle, maxAngle)
					rt.polyOp.setEdgeSelection(obj, edgelist)

				if tb.chk004.isChecked(): #crease vertex point
					pass
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









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------