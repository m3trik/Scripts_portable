from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Symmetry(Init):
	def __init__(self, *args, **kwargs):
		super(Symmetry, self).__init__(*args, **kwargs)

		try: #symmetry: set initial checked state
			state = pm.symmetricModelling(query=True, symmetry=True) #application symmetry state
			axis = pm.symmetricModelling(query=True, axis=True)
			if axis == "x":
				self.parentUi.chk000.setChecked(state)
				self.childUi.chk000.setChecked(state)
			if axis == "y":
				self.parentUi.chk001.setChecked(state)
				self.childUi.chk001.setChecked(state)
			if axis == "z":
				self.parentUi.chk002.setChecked(state)
				self.childUi.chk002.setChecked(state)
		except NameError:
			pass


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
		
		files = ['']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	def setSymmetry(self, state, axis):
		space = "world" #workd space
		if self.parentUi.chk004.isChecked(): #object space
			space = "object"
		elif self.parentUi.chk005.isChecked(): #topological symmetry
			space = "topo"

		tolerance = 0.25
		pm.symmetricModelling(edit=True, symmetry=state, axis=axis, about=space, tolerance=tolerance)
		self.viewPortMessage("Symmetry:<hl>"+axis+' '+str(state)+"</hl>")


	def chk000(self):
		'''
		Symmetry X
		'''
		self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk001,chk002')
		state = self.parentUi.chk000.isChecked() #symmetry button state
		self.setSymmetry(state, 'x')


	def chk001(self):
		'''
		Symmetry Y
		'''
		self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk000,chk002')
		state = self.parentUi.chk001.isChecked() #symmetry button state
		self.setSymmetry(state, 'y')


	def chk002(self):
		'''
		Symmetry Z
		'''
		self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk000,chk001')
		state = self.parentUi.chk002.isChecked() #symmetry button state
		self.setSymmetry(state, 'z')


	def chk004(self):
		'''
		Symmetry: Object
		'''
		self.parentUi.chk005.setChecked(False) #uncheck symmetry:topological
	

	def chk005(self):
		'''
		Symmetry: Topo
		'''
		self.parentUi.chk004.setChecked(False) #uncheck symmetry:object space
		if any ([self.parentUi.chk000.isChecked(), self.parentUi.chk001.isChecked(), self.parentUi.chk002.isChecked()]): #(symmetry)
			pm.symmetricModelling(edit=True, symmetry=False)
			self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk000,chk001,chk002')
			print("# Note: First select a seam edge and then check the symmetry button to enable topographic symmetry #")









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------