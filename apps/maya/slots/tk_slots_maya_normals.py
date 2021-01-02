from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Normals(Init):
	def __init__(self, *args, **kwargs):
		super(Normals, self).__init__(*args, **kwargs)


	def d000(self, state=None):
		'''Context menu
		'''
		d000 = self.normals.d000

		if state is 'setMenu':
			d000.contextMenu.add(widgets.TkComboBox, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.normals.cmb000

		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		if index>0:
			if index==cmd.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def tb000(self, state=None):
		'''Display Face Normals
		'''
		tb = self.currentUi.tb000
		if state is 'setMenu':
			tb.menu_.add('QSpinBox', setPrefix='Display Size: ', setObjectName='s001', setMinMax_='1-100 step1', setValue=1, setToolTip='Normal display size.')
			return

		size = float(tb.menu_.s001.value())
		# state = pm.polyOptions (query=True, displayNormal=True)
		state = self.cycle([1,2,3,0], 'displayNormals')
		if state ==0: #off
			pm.polyOptions (displayNormal=0, sizeNormal=0)
			pm.polyOptions (displayTangent=False)
			self.viewPortMessage("Normals Display <hl>Off</hl>.")

		if state ==1: #facet
			pm.polyOptions (displayNormal=1, facet=True, sizeNormal=size)
			pm.polyOptions (displayTangent=False)
			self.viewPortMessage("<hl>Facet</hl> Normals Display <hl>On</hl>.")

		if state ==2: #Vertex
			pm.polyOptions (displayNormal=1, point=True, sizeNormal=size)
			pm.polyOptions (displayTangent=False)
			self.viewPortMessage("<hl>Vertex</hl> Normals Display <hl>On</hl>.")

		if state ==3: #tangent
			pm.polyOptions (displayTangent=True)
			pm.polyOptions (displayNormal=0)
			self.viewPortMessage("<hl>Tangent</hl> Display <hl>On</hl>.")


	def tb001(self, state=None):
		'''Harden Creased Edges
		'''
		tb = self.currentUi.tb001
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Soften non-creased', setObjectName='chk000', setToolTip='Soften all non-creased edges.')
			return

		soften = tb.menu_.chk000.isChecked()

		mel.eval("PolySelectConvert 2")
		edges = pm.polyListComponentConversion(toEdge=1)
		edges = pm.ls(edges, flatten=1)

		pm.undoInfo(openChunk=1)
		self.mainProgressBar(len(edges))

		for edge in edges:
			pm.progressBar("tk_progressBar", edit=1, step=1)
			if pm.progressBar("tk_progressBar", query=1, isCancelled=1):
				break

			crease = pm.polyCrease (edge, query=1, value=1)
			# print(edge, crease[0])
			if crease[0]>0:
				pm.polySoftEdge (edge, angle=30)
			elif soften:
				pm.polySoftEdge (edge, angle=180)

		pm.progressBar("tk_progressBar", edit=1, endProgress=1)
		pm.undoInfo(closeChunk=1)


	@Init.attr
	def tb002(self, state=None):
		'''Set Normals By Angle
		'''
		tb = self.currentUi.tb002
		if state is 'setMenu':
			tb.menu_.add('QSpinBox', setPrefix='Angle: ', setObjectName='s000', setMinMax_='1-180 step1', setValue=30, setToolTip='Angle degree.')
			return

		normalAngle = str(tb.menu_.s000.value())

		objects = pm.ls(selection=1, objectsOnly=1, flatten=1)
		for obj in objects:
			sel = pm.ls(obj, sl=1)
			pm.polySetToFaceNormal(sel, setUserNormal=1) #reset to face
			polySoftEdge = pm.polySoftEdge(sel, angle=normalAngle) #smooth if angle is lower than specified amount. default 30
			return polySoftEdge if len(objects)==1 else polySoftEdge


	@Slots.message
	def tb003(self, state=None):
		'''Lock/Unlock Vertex Normals
		'''
		tb = self.currentUi.tb003
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='All', setObjectName='chk001', setChecked=True, setToolTip='Lock/Unlock: all.')
			return

		all_ = tb.menu_.chk001.isChecked()
		state = self.tk.ui.chk002.isChecked()#pm.polyNormalPerVertex(vertex, query=1, freezeNormal=1)
		selection = pm.ls (selection=1, objectsOnly=1)
		maskObject = pm.selectMode (query=1, object=1)
		maskVertex = pm.selectType (query=1, vertex=1)

		if len(selection)>0:
			if (all_ and maskVertex) or maskObject:
				for obj in selection:
					count = pm.polyEvaluate(obj, vertex=1) #get number of vertices
					vertices = [vertices.append(str(obj) + ".vtx ["+str(num)+"]") for num in xrange(count)] #geometry.vtx[0]
					for vertex in vertices:
						if state:
							pm.polyNormalPerVertex(vertex, unFreezeNormal=1)
						else:
							pm.polyNormalPerVertex(vertex, freezeNormal=1)
					if state:
						self.viewPortMessage("Normals <hl>UnLocked</hl>.")
					else:
						self.viewPortMessage("Normals <hl>Locked</hl>.")
			elif maskVertex and not maskObject:
				if state:
					pm.polyNormalPerVertex(unFreezeNormal=1)
					self.viewPortMessage("Normals <hl>UnLocked</hl>.")
				else:
					pm.polyNormalPerVertex(freezeNormal=1)
					self.viewPortMessage("Normals <hl>Locked</hl>.")
			else:
				return 'Warning: Selection must be object or vertex.'
		else:
			return 'Warning: No object selected.'


	def tb004(self, state=None):
		'''Average Normals
		'''
		tb = self.currentUi.tb004
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='By UV Shell', setObjectName='chk003', setToolTip='Average the normals of each object\'s faces per UV shell.')
			return

		byUvShell = tb.menu_.chk003.isChecked()

		pm.undoInfo(openChunk=1)

		objects = pm.ls(selection=1, objectsOnly=1, flatten=1)
		for obj in objects:

			if byUvShell:
				obj = pm.ls(obj, transforms=1)
				sets_ = Init.getUvShellSets(obj)
				for set_ in sets_:
					pm.polySetToFaceNormal(set_)
					pm.polyAverageNormal(set_)
			else:
				sel = pm.ls(obj, sl=1)
				if not sel:
					sel = obj
				pm.polySetToFaceNormal(sel)
				pm.polyAverageNormal(sel)

		pm.undoInfo(closeChunk=1)


	def b001(self):
		'''Soften Edge Normal
		'''
		pm.polySoftEdge(angle=180, constructionHistory=0)


	def b002(self):
		'''Harden Edge Normal
		'''
		pm.polySoftEdge(angle=0, constructionHistory=0)


	def b003(self):
		'''Soft Edge Display
		'''
		g_cond = pm.polyOptions(q=1, ae=1)
		if g_cond[0]:
			pm.polyOptions(se=1)
		else:
			pm.polyOptions(ae=1)


	def b005(self):
		'''Maya Bonus Tools: Adjust Vertex Normals
		'''
		pm.mel.bgAdjustVertexNormalsWin()


	def b006(self):
		'''Set To Face
		'''
		pm.polySetToFaceNormal()


	def b009(self):
		'''Harden Uv Edges
		'''
		selection = pm.ls(sl=True, l=True)

		uv_border_edges = Init.getUvShellBorderEdges(selection)
		pm.polySoftEdge(uv_border_edges, angle=0, ch=1)

		pm.select(uv_border_edges)


	def b010(self):
		'''Reverse Normals
		'''
		pm.mel.ReversePolygonNormals()



		





#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------
