import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Edit(Init):
	def __init__(self, *args, **kwargs):
		super(Edit, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('edit')

		
		
		


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
				pass
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Mesh Cleanup
		'''	
		isolatedVerts = self.ui.chk003.isChecked() #isolated vertices
		edgeAngle = self.ui.s006.value()
		nGons = self.ui.chk002.isChecked() #n-sided polygons
		repair = self.ui.chk004.isChecked() #auto repair errors

		self.meshCleanup(isolatedVerts=isolatedVerts, edgeAngle=edgeAngle, nGons=nGons, repair=repair)


	def b001(self):
		'''
		
		'''
		pass


	def b006(self):
		'''
		Delete History
		'''
		all_ = self.ui.chk018.isChecked()
		unusedNodes = self.ui.chk019.isChecked()
		deformers = self.ui.chk020.isChecked()
		objects = pm.ls (selection=1)
		if all_:
			objects = pm.ls (typ="mesh")

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


	def b007(self):
		'''
		Delete
		'''
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


	def b009(self):
		'''
		Crease Set Transfer: Transform Node
		'''
		if self.ui.b042.isChecked():
			creaseSet = str(pm.ls(selection=1)) #ex. [nt.CreaseSet(u'creaseSet1')]

			index1 = creaseSet.find("u")
			index2 = creaseSet.find(")")
			creaseSet = creaseSet[index1+1:index2].strip("'") #ex. creaseSet1

			if creaseSet != "[":
				self.ui.b042.setText(creaseSet)
			else:
				self.ui.b042.setText("must select set first")
				self.setButtons(self.ui, unchecked='b042')
			if self.ui.b043.isChecked():
				self.setButtons(self.ui, enable='b052')
		else:
			self.ui.b042.setText("Crease Set")


	def b010(self):
		'''
		Crease Set Transfer: Crease Set
		'''
		if self.ui.b043.isChecked():
			newObject = str(pm.ls(selection=1)) #ex. [nt.Transform(u'pSphere1')]

			index1 = newObject.find("u")
			index2 = newObject.find(")")
			newObject = newObject[index1+1:index2].strip("'") #ex. pSphere1

			if newObject != "[":
				self.ui.b043.setText(newObject)
			else:
				self.ui.b043.setText("must select obj first")
				self.setButtons(self.ui, unchecked='b043')
			if self.ui.b042.isChecked():
				self.setButtons(self.ui, enable='b052')
		else:
			self.ui.b043.setText("Object")


	def b011(self):
		'''
		Transfer Crease Edges
		'''
		# an updated version of this is in the maya python projects folder
		# the use of separate buttons for donor and target mesh are obsolete
		# add pm.polySoftEdge (angle=0, constructionHistory=0); #harden edge, when applying crease 

		creaseSet = str(self.ui.b042.text())
		newObject = str(self.ui.b043.text())

		sets = pm.sets (creaseSet, query=1)

		setArray = []
		for set_ in sets:
			name = str(set_)
			setArray.append(name)
		print setArray

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

		self.setButtons(self.ui, disable='b052', unchecked='b042')#,self.ui.b043])
		self.ui.b042.setText("Crease Set")
		# self.ui.b043.setText("Object")


	def b012(self):
		'''
		
		'''
		pass


	def b013(self):
		'''
		
		'''
		pass


	def b014(self):
		'''
		
		'''
		pass


	def b015(self):
		'''
		
		'''
		pass


	def b016(self):
		'''

		'''
		pass


	def b017(self):
		'''
		
		'''
		pass


	def b018(self):
		'''
		
		'''
		pass


	def b019(self):
		'''
		
		'''
		pass


	def b020(self):
		'''
		
		'''
		pass


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


	def b024(self):
		'''

		'''
		pass


	def b025(self):
		'''
		
		'''
		pass


	def b026(self):
		'''

		'''
		pass


	def b027(self):
		'''
		Shading Sets
		'''
		print 'no function'


	def b028(self):
		'''

		'''
		pass










#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

# maxEval('max array')

# maxEval('max mirror')