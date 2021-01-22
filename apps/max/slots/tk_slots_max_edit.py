from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Edit(Init):
	def __init__(self, *args, **kwargs):
		super(Edit, self).__init__(*args, **kwargs)


	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.edit_ui.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.edit_ui.cmb000

		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		if index>0:
			if index==cmb.items.index(''):
				pass
			cmb.setCurrentIndex(0)
	

	def chk006_9(self):
		'''Set the toolbutton's text according to the checkstates.
		'''
		axis = self.getAxisFromCheckBoxes('chk006-9')
		self.edit_ui.tb003.setText('Delete '+axis)


	def tb000(self, state=None):
		'''Mesh Cleanup
		'''
		tb = self.ui.tb000
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='N-Gons', setObjectName='chk002', setToolTip='Find N-gons.')
			tb.menu_.add('QCheckBox', setText='Isolated Vertex', setObjectName='chk003', setChecked=True, setToolTip='Find isolated vertices within specified angle threshold.')
			tb.menu_.add('QSpinBox', setPrefix='Loose Vertex Angle: ', setObjectName='s006', setMinMax_='1-360 step1', setValue=15, setToolTip='Loose vertex search: Angle Threshold.')
			tb.menu_.add('QCheckBox', setText='Repair', setObjectName='chk004', setToolTip='Repair matching geometry. (else: select)')
			return

		isolatedVerts = tb.menu_.chk003.isChecked() #isolated vertices
		edgeAngle = tb.menu_.s006.value()
		nGons = tb.menu_.chk002.isChecked() #n-sided polygons
		repair = tb.menu_.chk004.isChecked() #attempt auto repair errors

		self.meshCleanup(isolatedVerts=isolatedVerts, edgeAngle=edgeAngle, nGons=nGons, repair=repair)


	@Slots.message
	def tb001(self, state=None):
		'''Delete History
		'''
		tb = self.ui.tb001
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='For All Objects', setObjectName='chk018', setChecked=True, setToolTip='Delete history on All objects or just those selected.')
			tb.menu_.add('QCheckBox', setText='Delete Unused Nodes', setObjectName='chk019', setChecked=True, setToolTip='Delete unused nodes.')
			tb.menu_.add('QCheckBox', setText='Delete Deformers', setObjectName='chk020', setToolTip='Delete deformers.')
			return

		all_ = tb.menu_.chk018.isChecked()
		unusedNodes = tb.menu_.chk019.isChecked()
		deformers = tb.menu_.chk020.isChecked()

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
				return 'Delete <hl>All</hl> History.'
			else:
				return 'Delete <hl>All Non-Deformer</hl> History.'
		else:
			if deformers:
				return 'Delete history on '+str(objects)
			else:
				return 'Delete <hl>Non-Deformer</hl> history on '+str(objects)


	def tb002(self, state=None):
		'''Delete
		'''
		tb = self.ui.tb002
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Delete Loop', setObjectName='chk001', setToolTip='Delete the entire edge loop of any components selected.')
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


	def b021(self):
		'''Tranfer Maps
		'''
		maxEval('performSurfaceSampling 1;')


	def b022(self):
		'''Transfer Vertex Order
		'''
		maxEval('TransferVertexOrder;')


	def b023(self):
		'''Transfer Attribute Values
		'''
		maxEval('TransferAttributeValues;')


	def b027(self):
		'''Shading Sets
		'''
		print('no function')


	@staticmethod
	def findNGons(obj):
		'''Get a list of faces of a given object having more than four sides.

		:Parameters:
			obj (obj) = polygonal object.

		:Return:
			(list) list containing any found N-Gons		
		'''
		faces = Init.getFaces(obj)

		Init.setSubObjectLevel(4)
				
		nGons = [f for f in faces if rt.polyop.getFaceDeg(obj, f)>4]
		return nGons


	@staticmethod
	def getVertexVectors(obj, vertices):
		'''Generator to query vertex vector angles.

		ex.
		vectors = Edit.getVertexVectors(obj, vertices)
		for _ in range(len(vertices)):
			vector = vectors.next()
		'''
		for vertex in vertices:
			try:
				edges = Init.bitArrayToArray(rt.polyop.getEdgesUsingVert(obj, vertex)) #get the edges that use the vertice
			except:
				edges = Init.bitArrayToArray(rt.getEdgesUsingVert(obj, vertex)) #get the edges that use the vertice

			if len(edges)==2:
				try:
					vertexPosition = rt.polyop.getVert(obj, vertex)
				except:
					vertexPosition = rt.getVert(obj, vertex)

				try:
					edgeVerts = Init.bitArrayToArray([rt.polyop.getVertsUsingEdge(obj, e) for e in edges])
				except:
					edgeVerts = Init.bitArrayToArray([rt.getVertsUsingEdge(obj, e) for e in edges])

				edgeVerts = [v for v in edgeVerts if not v==vertex]

				try:
					vector1 = rt.normalize(rt.polyop.getVert(obj, edgeVerts[0]) - vertexPosition)
					vector2 = rt.normalize(rt.polyop.getVert(obj, edgeVerts[1]) - vertexPosition)
				except:
					vector1 = rt.normalize(rt.getVert(obj, edgeVerts[0]) - vertexPosition)
					vector2 = rt.normalize(rt.getVert(obj, edgeVerts[1]) - vertexPosition)

				vector = rt.length(vector1 + vector2)
				yield vector


	@staticmethod
	def findIsolatedVertices(obj):
		'''Get a list of isolated vertices of a given object.

		:Parameters:
			obj (obj) = polygonal object.

		:Return:
			(list) list containing any found isolated verts.		
		'''
		vertices = Init.getVertices(obj) #get all vertices for the given object

		isolatedVerts=[]
		vectors = Edit.getVertexVectors(obj, vertices)
		for _ in range(len(vertices)):
			vector = vectors.next()
			if vector and vector <= float(edgeAngle) / 50:
				isolatedVerts.append(vector)

		return isolatedVerts


	def meshCleanup(self, isolatedVerts=False, edgeAngle=10, nGons=False, repair=False):
		'''Find mesh artifacts.

		:Parameters:
			isolatedVerts (bool) = find vertices with two edges which fall below a specified angle.
			edgeAngle (int) = used with isolatedVerts argument to specify the angle tolerance
			nGons (bool) = search for n sided polygon faces.
			repair (bool) = delete or auto repair any of the specified artifacts 
		'''
		for obj in rt.selection:
			if not rt.classof(obj)==rt.Editable_poly:
				print('Error: '+obj.name+' isn\'t an editable poly or nothing is selected.')

			obj.selectMode = 2 #multi-component selection preview

			if nGons: #Convert N-Sided Faces To Quads
				_nGons = Edit.findNGons(obj)

				print('Found '+str(len(_nGons))+' N-gons.')

				if repair:
					maxEval('macros.run \"Modifiers\" \"QuadifyMeshMod\"') #add the quadify mesh modifier to the stack
				else: #Find and select N-gons	
					rt.setFaceSelection(obj, _nGons)


			if isolatedVerts: #delete loose vertices
				_isolatedVerts = Edit.findIsolatedVertices(obj)

				Init.undo(True)
				try:
					rt.polyop.setVertSelection(obj, _isolatedVerts)
				except:
					rt.setVertSelection(obj, _isolatedVerts)

				print('Found '+str(len(_isolatedVerts))+' isolated vertices.')
				
				if repair:
					obj.EditablePoly.remove(selLevel='Vertex', flag=1)
					obj.selectMode = 0 #multi-component selection preview off
				rt.redrawViews()
				Init.undo(False)


	def tb003(self, state=None):
		'''Delete Along Axis
		'''
		tb = self.ui.tb003
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='-', setObjectName='chk006', setChecked=True, setToolTip='Perform delete along negative axis.')
			tb.menu_.add('QRadioButton', setText='X', setObjectName='chk007', setChecked=True, setToolTip='Perform delete along X axis.')
			tb.menu_.add('QRadioButton', setText='Y', setObjectName='chk008', setToolTip='Perform delete along Y axis.')
			tb.menu_.add('QRadioButton', setText='Z', setObjectName='chk009', setToolTip='Perform delete along Z axis.')

			self.connect_('chk006-9', 'toggled', self.chk006_9, tb.menu_)
			return

		# selection = pm.ls(sl=1, objectsOnly=1)
		# axis = self.getAxisFromCheckBoxes('chk006-9', tb.menu_)

		# pm.undoInfo(openChunk=1)
		# for obj in selection:
		# 	self.deleteAlongAxis(obj, axis) #Init.deleteAlongAxis - no max version.
		# pm.undoInfo(closeChunk=1)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

# maxEval('max array')

# maxEval('max mirror')