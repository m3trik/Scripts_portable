from __future__ import print_function
from tk_slots_max_init import *


import os.path



class Edit(Init):
	def __init__(self, *args, **kwargs):
		super(Edit, self).__init__(*args, **kwargs)


	def chk006_9(self):
		'''
		Set the toolbutton's text according to the checkstates.
		'''
		axis = self.getAxisFromCheckBoxes('chk006-9')
		self.parentUi.tb003.setText('Along Axis '+axis)


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
			# if index==contents.index(''):
			# 	pass
			cmb.setCurrentIndex(0)


	def tb000(self, state=None):
		'''
		Mesh Cleanup
		'''
		tb = self.currentUi.tb000
		if state=='setMenu':
			tb.add('QCheckBox', setText='N-Gons', setObjectName='chk002', setToolTip='Find N-gons.')
			tb.add('QCheckBox', setText='Isolated Vertex', setObjectName='chk003', setChecked=True, setToolTip='Find isolated vertices within specified angle threshold.')
			tb.add('QSpinBox', setPrefix='Loose Vertex Angle: ', setObjectName='s006', preset_='1-360 step1', setValue=15, setToolTip='Loose vertex search: Angle Threshold.')
			tb.add('QCheckBox', setText='Repair', setObjectName='chk004', setToolTip='Repair matching geometry. (else: select)')
			return

		isolatedVerts = tb.chk003.isChecked() #isolated vertices
		edgeAngle = tb.s006.value()
		nGons = tb.chk002.isChecked() #n-sided polygons
		repair = tb.chk004.isChecked() #attempt auto repair errors

		self.meshCleanup(isolatedVerts=isolatedVerts, edgeAngle=edgeAngle, nGons=nGons, repair=repair)


	def tb001(self, state=None):
		'''
		Delete History
		'''
		tb = self.currentUi.tb001
		if state=='setMenu':
			tb.add('QCheckBox', setText='All', setObjectName='chk018', setChecked=True, setToolTip='Delete history on All objects.')
			tb.add('QCheckBox', setText='Delete Unused Nodes', setObjectName='chk019', setChecked=True, setToolTip='Delete unused nodes.')
			tb.add('QCheckBox', setText='Delete Deformers', setObjectName='chk020', setToolTip='Delete deformers.')
			return

		all_ = tb.chk018.isChecked()
		unusedNodes = tb.chk019.isChecked()
		deformers = tb.chk020.isChecked()

		objects = pm.ls(selection=1)
		if all_:
			objects = pm.ls(typ="mesh")

		for obj in objects:
			try:
				if all_:
					pm.delete (obj, constructionHistory=1)
				else:
					pm.bakePartialHistory (obj, prePostDeformers=1)
			except:
				pass
		if unusedNodes:
			maxEval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

		#display viewPort messages
		if all_:
			if deformers:
				self.viewPortMessage("delete <hl>all</hl> history.")
			else:
				self.viewPortMessage("delete <hl>all non-deformer</hl> history.")
		else:
			if deformers:
				self.viewPortMessage("delete history on "+str(objects))
			else:
				self.viewPortMessage("delete <hl>non-deformer</hl> history on "+str(objects))


	def tb002(self, state=None):
		'''
		Delete 
		'''
		tb = self.currentUi.tb002
		if state=='setMenu':
			tb.add('QCheckBox', setText='Delete Loop', setObjectName='chk001', setToolTip='Delete the entire edge loop of any components selected.')
			return

		level = rt.subObjectLevel

		for obj in rt.selection:
			if level==1: #vertices
				obj.EditablePoly.remove(selLevel='Vertex', flag=1)

			if level==2: #edges
				edges = rt.polyop.getEdgeSelection(obj)
				verts = rt.polyop.getVertsUsingEdge(obj, edges)
				rt.polyop.setVertSelection(obj, verts) #set vertex selection to be used by meshCleanup
				
				obj.EditablePoly.remove(selLevel='Edge', flag=1)
				self.meshCleanup(isolatedVerts=1, repair=1) #if any isolated verts exist: delete them

			if level==4: #faces
				faces = rt.polyop.getFaceSelection(obj)
				rt.polyop.deleteFaces(obj, faces, delIsoVerts=1)


	def tb003(self, state=None):
		'''
		Delete Along Axis
		'''
		tb = self.currentUi.tb003
		if state=='setMenu':
			tb.add('QCheckBox', setText='-', setObjectName='chk006', setChecked=True, setToolTip='Perform delete along negative axis.')
			tb.add('QRadioButton', setText='X', setObjectName='chk007', setChecked=True, setToolTip='Perform delete along X axis.')
			tb.add('QRadioButton', setText='Y', setObjectName='chk008', setToolTip='Perform delete along Y axis.')
			tb.add('QRadioButton', setText='Z', setObjectName='chk009', setToolTip='Perform delete along Z axis.')

			self.connect('chk006-9', 'toggled', self.chk006_9, tb)
			return

		selection = pm.ls(sl=1, objectsOnly=1)
		axis = self.getAxisFromCheckBoxes('chk006-9')

		pm.undoInfo(openChunk=1)
		for obj in selection:
			self.deleteAlongAxis(obj, axis) #Init.deleteAlongAxis - no max version.
		pm.undoInfo(closeChunk=1)


	def b009(self):
		'''
		Crease Set Transfer: Transform Node
		'''
		if self.parentUi.b042.isChecked():
			creaseSet = str(pm.ls(selection=1)) #ex. [nt.CreaseSet(u'creaseSet1')]

			index1 = creaseSet.find("u")
			index2 = creaseSet.find(")")
			creaseSet = creaseSet[index1+1:index2].strip("'") #ex. creaseSet1

			if creaseSet != "[":
				self.parentUi.b042.setText(creaseSet)
			else:
				self.parentUi.b042.setText("must select set first")
				self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='b042')
			if self.parentUi.b043.isChecked():
				self.toggleWidgets(self.parentUi, self.childUi, setEnabled='b052')
		else:
			self.parentUi.b042.setText("Crease Set")


	def b010(self):
		'''
		Crease Set Transfer: Crease Set
		'''
		if self.parentUi.b043.isChecked():
			newObject = str(pm.ls(selection=1)) #ex. [nt.Transform(u'pSphere1')]

			index1 = newObject.find("u")
			index2 = newObject.find(")")
			newObject = newObject[index1+1:index2].strip("'") #ex. pSphere1

			if newObject != "[":
				self.parentUi.b043.setText(newObject)
			else:
				self.parentUi.b043.setText("must select obj first")
				self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='b043')
			if self.parentUi.b042.isChecked():
				self.toggleWidgets(self.parentUi, self.childUi, setEnabled='b052')
		else:
			self.parentUi.b043.setText("Object")


	def b011(self):
		'''
		Transfer Crease Edges
		'''
		# an updated version of this is in the maya python projects folder
		# the use of separate buttons for donor and target mesh are obsolete
		# add pm.polySoftEdge (angle=0, constructionHistory=0); #harden edge, when applying crease 

		creaseSet = str(self.parentUi.b042.text())
		newObject = str(self.parentUi.b043.text())

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
			# print "crease:", name
		pm.undoInfo (closeChunk=1)

		self.toggleWidgets(self.parentUi, self.childUi, setDisabled='b052', setChecked_False='b042')#,self.parentUi.b043])
		self.parentUi.b042.setText("Crease Set")
		# self.parentUi.b043.setText("Object")


	def b021(self):
		'''
		Tranfer Maps
		'''
		maxEval('performSurfaceSampling 1;')


	def b022(self):
		'''
		Transfer Vertex Order
		'''
		maxEval('TransferVertexOrder;')


	def b023(self):
		'''
		Transfer Attribute Values
		'''
		maxEval('TransferAttributeValues;')


	def b027(self):
		'''
		Shading Sets
		'''
		print('no function')










#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

# maxEval('max array')

# maxEval('max mirror')