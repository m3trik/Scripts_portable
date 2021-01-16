from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Subdivision(Init):
	def __init__(self, *args, **kwargs):
		super(Subdivision, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('subdivision')
		self.childUi = self.sb.getUi('subdivision_submenu')

		#Set 3ds Max specific naming
		self.parentUi.gb000.setTitle('TurboSmooth')
		self.parentUi.s000.setPrefix('Iterations:  ')
		self.parentUi.s001.setPrefix('RenderIters: ')
		self.parentUi.s000.setValue(0)
		self.parentUi.s001.setValue(0)


	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.parentUi.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb000', setToolTip='Subdivision Modifiers')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.parentUi.cmb000

		if index is 'setMenu':
			list_ = ['TurboSmooth','TurboSmooth Pro','OpenSubDiv','Subdivide','Subdivide (WSM)','MeshSmooth','Optimize','Pro Optimizer','Add Divisions']
			cmb.addItems_(list_, '3dsMax Subdivision Modifiers')
			return

		if index>0:
			if index==1: #TurboSmooth
				mod = rt.TurboSmooth()
				mod.iterations = 0
				mod.renderIterations = 1
				mod.useRenderIterations = True
				mod.explicitNormals = True
				mod.sepByMats = True
				rt.modpanel.addModToSelection(mod)

			if index==2: #TurboSmooth Pro
				mod = TurboSmooth_Pro()
				mod.iterations = 0
				mod.renderIterations = 1
				mod.useRenderIterations = True
				mod.explicitNormals = True
				mod.visualizeCreases = True
				mod.smmoothCorners = False
				mod.creaseSmoothingGroups = True
				mod.creaseMaterials = True
				rt.modpanel.addModToSelection(mod)

			if index==3: #OpenSubDiv
				mod = OpenSubdiv()
				mod.iterations = 0
				mod.renderIterations = 1
				mod.useRenderIterations = True
				rt.modpanel.addModToSelection(mod)

			if index==4: #Subdivide
				mod = subdivide()
				mod.size = 0.075
				rt.modpanel.addModToSelection(mod)

			if index==5: #Subdivide (WSM)
				mod = subdivideSpacewarpModifier()
				mod.size = 40
				rt.modpanel.addModToSelection(mod)

			if index==6: #MeshSmooth
				mod = meshsmooth()
				mod.iterations = 0
				mod.renderIterations = 1
				mod.useRenderIterations = True
				mod.useRenderSmoothness = True
				rt.modpanel.addModToSelection(mod)

			if index==7: #Optimize
				mod = optimize()
				rt.modpanel.addModToSelection(mod)

			if index==8: #Pro optimizer
				mod = ProOptimizer()
				rt.modpanel.addModToSelection(mod)

			if index==cmb.items.index('Add Divisions'):
				maxEval('''
				Try 
				(
					local A = modPanel.getCurrentObject()
					A.popupDialog #Tessellate
				)
				Catch ()
				''')
			cmb.setCurrentIndex(0)


	def s000(self, value=None):
		'''Division Level
		'''
		value = self.parentUi.s000.getValue()

		geometry = rt.selection

		for obj in geometry:
			try:
				obj.modifiers['TurboSmooth'].iterations = value
			except: pass


	def s001(self, value=None):
		'''Tesselation Level
		'''
		value = self.parentUi.s001.getValue()

		geometry = rt.selection

		for obj in geometry:
			try:
				obj.modifiers['TurboSmooth'].renderIterations = value
			except: pass


	def b005(self):
		'''Reduce
		'''
		mel.eval("ReducePolygon;")


	def b008(self):
		'''Add Divisions - Subdivide Mesh
		'''
		maxEval('macros.run \"Modifiers\" \"Tessellate\"')


	def b009(self):
		'''Smooth
		'''
		maxEval('macros.run \"Modifiers\" \"Smooth\"')


	def b010(self):
		''''''
		pass


	def b011(self):
		'''Convert Smooth Preview
		'''
		#convert smooth mesh preview to polygons
		geometry = rt.selection

		if not len(geometry):
			geometry = rt.geometry

		for obj in geometry:
			try:
				renderIters = obj.modifiers['TurboSmooth'].renderIterations
				obj.modifiers['TurboSmooth'].iterations = renderIters

				modifiers = [mod.name for mod in obj.modifiers]
				if modifiers:
					index = modifiers.index('TurboSmooth') +1
				rt.maxOps.CollapseNodeTo(obj, index, False)
			except: pass









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------