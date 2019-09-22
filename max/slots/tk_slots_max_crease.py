import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Crease(Init):
	def __init__(self, *args, **kwargs):
		super(Crease, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('crease')

		




	def chk002(self):
		'''
		Un-Crease
		'''
		if self.ui.chk002.isChecked():
			self.ui.s003.setValue(0) #crease value
			self.ui.s004.setValue(180) #normal angle
			self.setButtons(self.ui, unchecked='chk003')
		else:
			self.ui.s003.setValue(5) #crease value
			self.ui.s004.setValue(60) #normal angle


	def chk003(self):
		'''
		Crease: Max
		'''
		if self.ui.chk003.isChecked():
			self.ui.s003.setValue(10) #crease value
			self.ui.s004.setValue(30) #normal angle
			self.setButtons(self.ui, unchecked='chk002')
		else:
			self.ui.s003.setValue(5) #crease value
			self.ui.s004.setValue(60) #normal angle


	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = self.comboBox (cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Crease
		'''
		creaseAmount = int(self.ui.s003.value())
		normalAngle = int(self.ui.s004.value())

		creaseAmount = creaseAmount*0.1 #convert to max 0-1 range

		for obj in rt.selection:
			if rt.classOf(obj)=='Editable_Poly':

				if self.ui.chk011.isChecked(): #crease: Auto
					minAngle = int(self.ui.s005.value()) 
					maxAngle = int(self.ui.s006.value()) 

					edgelist = self.getEdgesByAngle(minAngle, maxAngle)
					rt.polyOp.setEdgeSelection(obj, edgelist)

				if self.ui.chk004.isChecked(): #crease vertex point
					pass
				else: #crease edge
					obj.EditablePoly.setEdgeData(1, creaseAmount)

				if self.ui.chk005.isChecked(): #adjust normal angle
					edges = rt.polyop.getEdgeSelection(obj)
					for edge in edges:
						edgeVerts = rt.polyop.getEdgeVerts(obj, edge)
						normal = rt.averageSelVertNormal(obj)
						for vertex in edgeVerts:
							rt.setNormal(obj, vertex, normal)
		else:
			print '# Warning: object type '+rt.classOf(obj)+' is not supported. #'









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------