from __future__ import print_function
from tk_slots_max_init import *


import os.path



class Symmetry(Init):
	def __init__(self, *args, **kwargs):
		super(Symmetry, self).__init__(*args, **kwargs)

		self.ui = self.parentUi #self.ui = self.sb.getUi(self.__class__.__name__)

		#symmetry: set initial checked state
		# state = pm.symmetricModelling(query=True, symmetry=True) #application symmetry state
		# axis = pm.symmetricModelling(query=True, axis=True)
		# if axis == "x":
		# 	self.ui.chk000.setChecked(state)
		# if axis == "y":
		# 	self.ui.chk001.setChecked(state)
		# if axis == "z":
		# 	self.ui.chk002.setChecked(state)



	def setSymmetry(self, state, axis):
		'''

		'''
		# space = "world" #workd space
		# if self.ui.chk004.isChecked(): #object space
		# 	space = "object"
		# elif self.ui.chk005.isChecked(): #topological symmetry
		# 	space = "topo"

		if axis=='x':
			axis=0 #0(x), 1,(y), 2(z)
		if axis=='y':
			axis=1
		if axis=='z':
			axis=2

		for obj in rt.selection:
			#check if modifier exists
			mod = obj.modifiers[rt.Symmetry]
			if mod==None: #if not create
				mod = rt.symmetry()
				rt.addModifier (obj, mod)
		
			#set attributes
			mod.enabled = state
			mod.threshold = 0.01
			mod.axis = axis
			mod.flip = negative

		rt.redrawViews()
		# self.viewPortMessage("Symmetry:<hl>"+axis+' '+str(state)+"</hl>")


	def chk000(self):
		'''
		Symmetry X
		'''
		self.toggleWidgets(self.ui, self.childUi, self.childUi, setChecked_False='chk001,chk002')
		state = self.ui.chk000.isChecked() #symmetry button state
		self.setSymmetry(state, 'x')


	def chk001(self):
		'''
		Symmetry Y
		'''
		self.toggleWidgets(self.ui, self.childUi, self.childUi, setChecked_False='chk000,chk002')
		state = self.ui.chk001.isChecked() #symmetry button state
		self.setSymmetry(state, 'y')


	def chk002(self):
		'''
		Symmetry Z
		'''
		self.toggleWidgets(self.ui, self.childUi, self.childUi, setChecked_False='chk000,chk001')
		state = self.ui.chk002.isChecked() #symmetry button state
		self.setSymmetry(state, 'z')


	def chk004(self):
		'''
		Symmetry: Object
		'''
		self.ui.chk005.setChecked(False) #uncheck symmetry:topological
	

	def chk005(self):
		'''
		Symmetry: Topo
		'''
		self.ui.chk004.setChecked(False) #uncheck symmetry:object space
		if any ([self.ui.chk000.isChecked(), self.ui.chk001.isChecked(), self.ui.chk002.isChecked()]): #(symmetry)
			pm.symmetricModelling(edit=True, symmetry=False)
			self.toggleWidgets(self.ui, self.childUi, setChecked_False='chk000-2')
			print("# Warning: First select a seam edge and then check the symmetry button to enable topographic symmetry #")


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








#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------