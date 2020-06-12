from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Edit(Init):
	def __init__(self, *args, **kwargs):
		super(Edit, self).__init__(*args, **kwargs)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya Editors')

			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000

		files = ['Cleanup', 'Transfer: Attribute Values', 'Transfer: Shading Sets']
		contents = cmb.addItems_(files, 'Maya Editors')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Cleanup'):
				mel.eval('CleanupPolygonOptions;')
			if index==contents.index('Transfer: Attribute Values'):
				mel.eval('TransferAttributeValuesOptions;')
				# mel.eval('performTransferAttributes 1;') #Transfer Attributes Options
			if index==contents.index('Transfer: Shading Sets'):
				mel.eval('performTransferShadingSets 1;')
			cmb.setCurrentIndex(0)


	def chk006_9(self):
		'''
		Set the toolbutton's text according to the checkstates.
		'''
		axis = self.getAxisFromCheckBoxes('chk006-9')
		self.parentUi.tb003.setText('Along Axis '+axis)


	def tb000(self, state=None):
		'''
		Mesh Cleanup
		'''
		tb = self.currentUi.tb000
		if state=='setMenu':
			tb.add('QCheckBox', setText='N-Gons', setObjectName='chk002', setToolTip='Find N-gons.')
			tb.add('QCheckBox', setText='Isolated Vertex', setObjectName='chk003', setChecked=True, setToolTip='Find isolated vertices within specified angle threshold.')
			tb.add('QSpinBox', setPrefix='Loose Vertex Angle: ', setObjectName='s006', minMax_='1-360 step1', setValue=15, setToolTip='Loose vertex search: Angle Threshold.')
			tb.add('QCheckBox', setText='Repair', setObjectName='chk004', setToolTip='Repair matching geometry. (else: select)')
			tb.add('QCheckBox', setText='All Geometry', setObjectName='chk005', setToolTip='Clean All scene geometry.')
			return

		isolatedVerts = tb.chk003.isChecked() #isolated vertices
		edgeAngle = tb.s006.value()
		nGons = tb.chk002.isChecked() #n-sided polygons
		repair = tb.chk004.isChecked() #attempt auto repair errors
		allGeometry = tb.chk005.isChecked() #clean all scene geometry

		#Select components for cleanup from all visible geometry in the scene
		if allGeometry:
			scene = pm.ls(visible=1, geometry=1)
			[pm.select (geometry, add=1) for geometry in scene]

		if repair: #auto repair errors
			mel.eval(r'polyCleanupArgList 4 { "0","1","1","0","1","0","1","0","0","1e-005","1","0.0001","0","1e-005","0","1","1","0" };')
		else:
			mel.eval(r'polyCleanupArgList 3 { "0","2","1","0","1","0","0","0","0","1e-005","1","1e-005","0","1e-005","0","1","1" };')

		if nGons: #N-Sided Faces
			if repair: #Maya Bonus Tools: Convert N-Sided Faces To Quads
				mel.eval('bt_polyNSidedToQuad;')
			else: #Find And Select N-Gons
				#Change to Component mode to retain object highlighting for better visibility
				pm.changeSelectMode (component=1)
				#Change to Face Component Mode
				pm.selectType (smp=0, sme=1, smf=0, smu=0, pv=0, pe=1, pf=0, puv=0)
				#Select Object/s and Run Script to highlight N-Gons
				pm.polySelectConstraint (mode=3, type=0x0008, size=3)
				pm.polySelectConstraint (disable=1)
				#Populate an in-view message
				nGons = pm.polyEvaluate (faceComponent=1)
				self.viewPortMessage("<hl>"+str(nGons[0])+"</hl> N-Gon(s) found.")


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
			mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

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

		selectionMask = pm.selectMode (query=True, component=True)
		maskVertex = pm.selectType (query=True, vertex=True)
		maskEdge = pm.selectType (query=True, edge=True)
		maskFacet = pm.selectType (query=True, facet=True)

		objects = pm.ls(sl=1)

		for obj in objects:
			if pm.objectType(obj, isType='joint'):
				pm.removeJoint(obj) #remove joints

			elif pm.objectType(obj, isType='mesh'): 
				if all([selectionMask==1, maskEdge==1]):
					pm.polyDelEdge(cleanVertices=True) #delete edges

				elif all([selectionMask==1, maskVertex==1]):
					pm.polyDelVertex() #try delete vertices
					if pm.ls(sl=1)==objects: #if nothing was deleted:
						mel.eval('polySelectSp -loop;') #convert selection to edge loop
						pm.polyDelEdge(cleanVertices=True) #delete edges

				else: #all([selectionMask==1, maskFacet==1]):
					pm.delete(obj) #delete faces\mesh objects
		
		self.viewPortMessage('Delete <hl>'+str(objects)+'</hl>.')


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

			self.connect_('chk006-9', 'toggled', self.chk006_9, tb)
			return

		selection = pm.ls(sl=1, objectsOnly=1)
		axis = self.getAxisFromCheckBoxes('chk006-9')

		pm.undoInfo(openChunk=1)
		for obj in selection:
			self.deleteAlongAxis(obj, axis)
		pm.undoInfo(closeChunk=1)


	def b001(self):
		'''

		'''
		pass


	def b021(self):
		'''
		Tranfer Maps
		'''
		mel.eval('performSurfaceSampling 1;')


	def b022(self):
		'''
		Transfer Vertex Order
		'''
		mel.eval('TransferVertexOrder;')


	def b023(self):
		'''
		Transfer Attribute Values
		'''
		mel.eval('TransferAttributeValues;')


	def b027(self):
		'''
		Shading Sets
		'''
		mel.eval('performTransferShadingSets 0;')






#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------
	# b008, b009, b011
