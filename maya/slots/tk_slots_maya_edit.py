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
		self.parentUi.tb003.setText('Delete '+axis)


	def tb000(self, state=None):
		'''
		Mesh Cleanup
		'''
		tb = self.currentUi.tb000
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='All Geometry', setObjectName='chk005', setToolTip='Clean All scene geometry.')
			tb.add('QCheckBox', setText='Repair', setObjectName='chk004', setToolTip='Repair matching geometry. (else: select)')
			tb.add('QCheckBox', setText='N-Gons', setObjectName='chk002', setChecked=True, setToolTip='Find N-gons.')
			tb.add('QCheckBox', setText='Non-Manifold Geometry', setObjectName='chk017', setChecked=True, setToolTip='Check for nonmanifold polys.')
			tb.add('QCheckBox', setText='Quads', setObjectName='chk010', setToolTip='Check for quad sided polys.')
			tb.add('QCheckBox', setText='Concave', setObjectName='chk011', setToolTip='Check for concave polys.')
			tb.add('QCheckBox', setText='Non-Planar', setObjectName='chk003', setToolTip='Check for non-planar polys.')
			tb.add('QCheckBox', setText='Holed', setObjectName='chk012', setToolTip='Check for holed polys.')
			tb.add('QCheckBox', setText='Lamina', setObjectName='chk018', setToolTip='Check for lamina polys.')
			tb.add('QCheckBox', setText='Shared UV\'s', setObjectName='chk016', setToolTip='Unshare uvs that are shared across vertices.')
			# tb.add('QCheckBox', setText='Invalid Components', setObjectName='chk019', setToolTip='Check for invalid components.')
			tb.add('QCheckBox', setText='Zero Face Area', setObjectName='chk013', setToolTip='Check for 0 area faces.')
			tb.add('QDoubleSpinBox', setPrefix='Face Area Tolerance:   ', setObjectName='s006', minMax_='0.0-10 step.001', setValue=0.001, setToolTip='Tolerance for face areas.')
			tb.add('QCheckBox', setText='Zero Length Edges', setObjectName='chk014', setToolTip='Check for 0 length edges.')
			tb.add('QDoubleSpinBox', setPrefix='Edge Length Tolerance: ', setObjectName='s007', minMax_='0.0-10 step.001', setValue=0.001, setToolTip='Tolerance for edge length.')
			tb.add('QCheckBox', setText='Zero UV Face Area', setObjectName='chk015', setToolTip='Check for 0 uv face area.')
			tb.add('QDoubleSpinBox', setPrefix='UV Face Area Tolerance:', setObjectName='s008', minMax_='0.0-10 step.001', setValue=0.001, setToolTip='Tolerance for uv face areas.')
			if state=='setMenu':
				return

		allMeshes = int(tb.chk005.isChecked()) #[0] All selectable meshes
		selectOnly = int(not tb.chk004.isChecked())+1 #[1] Only perform a selection [0:clean, 1:select and clean, 2:select]
		historyOn = 1 #[2] keep construction history
		quads = int(tb.chk010.isChecked()) #[3] check for quads polys
		nsided = int(tb.chk002.isChecked()) #[4] check for n-sided polys
		concave = int(tb.chk011.isChecked()) #[5] check for concave polys
		holed = int(tb.chk012.isChecked()) #[6] check for holed polys
		nonplanar = int(tb.chk003.isChecked()) #[7] check for non-planar polys
		zeroGeom = int(tb.chk013.isChecked()) #[8] check for 0 area faces
		zeroGeomTol = tb.s006.value() #[9] tolerance for face areas
		zeroEdge = int(tb.chk014.isChecked()) #[10] check for 0 length edges
		zeroEdgeTol = tb.s007.value() #[11] tolerance for edge length
		zeroMap = int(tb.chk015.isChecked()) #[12] check for 0 uv face area
		zeroMapTol = tb.s008.value() #[13] tolerance for uv face areas
		sharedUVs = int(tb.chk016.isChecked()) #[14] Unshare uvs that are shared across vertices
		nonmanifold = int(tb.chk017.isChecked()) #[15] check for nonmanifold polys
		lamina = -int(tb.chk018.isChecked()) #[16] check for lamina polys [default -1]
		invalidComponents = 0 #int(tb.chk019.isChecked()) #[17] a guess what this arg does. not checked. default is 0.

		# if tb.chk005.isChecked(): #All Geometry. Select components for cleanup from all visible geometry in the scene
		# 	scene = pm.ls(visible=1, geometry=1)
		# 	[pm.select (geometry, add=1) for geometry in scene]

		arg_list = '"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}","{14}","{15}","{16}","{17}"'.format(
				allMeshes, selectOnly, historyOn, quads, nsided, concave, holed, nonplanar, zeroGeom, 
				zeroGeomTol, zeroEdge, zeroEdgeTol, zeroMap, zeroMapTol, sharedUVs, nonmanifold, lamina, invalidComponents)
		command = 'polyCleanupArgList 4 {'+arg_list+'}' # command = 'polyCleanup '+arg_list #(not used because of arg count error, also the quotes in the arg list would need to be removed). 
		print (command)
		mel.eval(command)


	def tb001(self, state=None):
		'''
		Delete History
		'''
		tb = self.currentUi.tb001
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='All', setObjectName='chk018', setChecked=True, setToolTip='Delete history on All objects.')
			tb.add('QCheckBox', setText='Delete Unused Nodes', setObjectName='chk019', setChecked=True, setToolTip='Delete unused nodes.')
			tb.add('QCheckBox', setText='Delete Deformers', setObjectName='chk020', setToolTip='Delete deformers.')
			if state=='setMenu':
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
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='Delete Loop', setObjectName='chk001', setToolTip='Delete the entire edge loop of any components selected.')
			if state=='setMenu':
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
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='-', setObjectName='chk006', setChecked=True, setToolTip='Perform delete along negative axis.')
			tb.add('QRadioButton', setText='X', setObjectName='chk007', setChecked=True, setToolTip='Perform delete along X axis.')
			tb.add('QRadioButton', setText='Y', setObjectName='chk008', setToolTip='Perform delete along Y axis.')
			tb.add('QRadioButton', setText='Z', setObjectName='chk009', setToolTip='Perform delete along Z axis.')

			self.connect_('chk006-9', 'toggled', self.chk006_9, tb)
			if state=='setMenu':
				return

		selection = pm.ls(sl=1, objectsOnly=1)
		axis = self.getAxisFromCheckBoxes('chk006-9', tb)

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
