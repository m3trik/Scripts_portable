import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Symmetry(Init):
	def __init__(self, *args, **kwargs):
		super(Symmetry, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('symmetry')

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

		negative = self.ui.chk003.isChecked()

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
		self.setButtons(self.ui, unchecked='chk001,chk002')
		state = self.ui.chk000.isChecked() #symmetry button state
		self.setSymmetry(state, 'x')


	def chk001(self):
		'''
		Symmetry Y
		'''
		self.setButtons(self.ui, unchecked='chk000,chk002')
		state = self.ui.chk001.isChecked() #symmetry button state
		self.setSymmetry(state, 'y')


	def chk002(self):
		'''
		Symmetry Z
		'''
		self.setButtons(self.ui, unchecked='chk000,chk001')
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
			self.setButtons(self.ui, unchecked='chk000,chk001,chk002')
			print "# Warning: First select a seam edge and then check the symmetry button to enable topographic symmetry #"


	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = self.comboBox(cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				mel.eval('')
			cmb.setCurrentIndex(0)


	def b001(self):
		'''
		
		'''
		pass


	def b002(self):
		'''

		'''
		pass


	def b003(self):
		'''
		
		'''
		pass


	def b004(self):
		'''
		
		'''
		pass


	def b005(self):
		'''
		
		'''
		pass


	def b006(self):
		'''
		
		'''
		pass








#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------