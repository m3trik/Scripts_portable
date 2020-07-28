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
		pin = self.edit.pin

		if state is 'setMenu':
			pin.contextMenu.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya Editors')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.edit.cmb000

		if index is 'setMenu':
			list_ = ['Cleanup', 'Transfer: Attribute Values', 'Transfer: Shading Sets']
			cmb.addItems_(list_, 'Maya Editors')
			return

		if index>0:
			if index==cmb.items.index('Cleanup'):
				mel.eval('CleanupPolygonOptions;')
			if index==cmb.items.index('Transfer: Attribute Values'):
				mel.eval('TransferAttributeValuesOptions;')
				# mel.eval('performTransferAttributes 1;') #Transfer Attributes Options
			if index==cmb.items.index('Transfer: Shading Sets'):
				mel.eval('performTransferShadingSets 1;')
			cmb.setCurrentIndex(0)


	def chk006_9(self):
		'''
		Set the toolbutton's text according to the checkstates.
		'''
		tb = self.ui.tb003
		axis = self.getAxisFromCheckBoxes('chk006-9', tb.menu_)
		tb.setText('Delete '+axis)


	def tb000(self, state=None):
		'''
		Mesh Cleanup
		'''
		tb = self.ui.tb000
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='All Geometry', setObjectName='chk005', setToolTip='Clean All scene geometry.')
			tb.menu_.add('QCheckBox', setText='Repair', setObjectName='chk004', setToolTip='Repair matching geometry. (else: select)')
			tb.menu_.add('QCheckBox', setText='N-Gons', setObjectName='chk002', setChecked=True, setToolTip='Find N-gons.')
			tb.menu_.add('QCheckBox', setText='Non-Manifold Geometry', setObjectName='chk017', setChecked=True, setToolTip='Check for nonmanifold polys.')
			tb.menu_.add('QCheckBox', setText='Quads', setObjectName='chk010', setToolTip='Check for quad sided polys.')
			tb.menu_.add('QCheckBox', setText='Concave', setObjectName='chk011', setToolTip='Check for concave polys.')
			tb.menu_.add('QCheckBox', setText='Non-Planar', setObjectName='chk003', setToolTip='Check for non-planar polys.')
			tb.menu_.add('QCheckBox', setText='Holed', setObjectName='chk012', setToolTip='Check for holed polys.')
			tb.menu_.add('QCheckBox', setText='Lamina', setObjectName='chk018', setToolTip='Check for lamina polys.')
			tb.menu_.add('QCheckBox', setText='Shared UV\'s', setObjectName='chk016', setToolTip='Unshare uvs that are shared across vertices.')
			# tb.menu_.add('QCheckBox', setText='Invalid Components', setObjectName='chk019', setToolTip='Check for invalid components.')
			tb.menu_.add('QCheckBox', setText='Zero Face Area', setObjectName='chk013', setToolTip='Check for 0 area faces.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='Face Area Tolerance:   ', setObjectName='s006', minMax_='0.0-10 step.001', setValue=0.001, setToolTip='Tolerance for face areas.')
			tb.menu_.add('QCheckBox', setText='Zero Length Edges', setObjectName='chk014', setToolTip='Check for 0 length edges.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='Edge Length Tolerance: ', setObjectName='s007', minMax_='0.0-10 step.001', setValue=0.001, setToolTip='Tolerance for edge length.')
			tb.menu_.add('QCheckBox', setText='Zero UV Face Area', setObjectName='chk015', setToolTip='Check for 0 uv face area.')
			tb.menu_.add('QDoubleSpinBox', setPrefix='UV Face Area Tolerance:', setObjectName='s008', minMax_='0.0-10 step.001', setValue=0.001, setToolTip='Tolerance for uv face areas.')
			return

		allMeshes = int(tb.menu_.chk005.isChecked()) #[0] All selectable meshes
		selectOnly = int(not tb.menu_.chk004.isChecked())+1 #[1] Only perform a selection [0:clean, 1:select and clean, 2:select]
		historyOn = 1 #[2] keep construction history
		quads = int(tb.menu_.chk010.isChecked()) #[3] check for quads polys
		nsided = int(tb.menu_.chk002.isChecked()) #[4] check for n-sided polys
		concave = int(tb.menu_.chk011.isChecked()) #[5] check for concave polys
		holed = int(tb.menu_.chk012.isChecked()) #[6] check for holed polys
		nonplanar = int(tb.menu_.chk003.isChecked()) #[7] check for non-planar polys
		zeroGeom = int(tb.menu_.chk013.isChecked()) #[8] check for 0 area faces
		zeroGeomTol = tb.menu_.s006.value() #[9] tolerance for face areas
		zeroEdge = int(tb.menu_.chk014.isChecked()) #[10] check for 0 length edges
		zeroEdgeTol = tb.menu_.s007.value() #[11] tolerance for edge length
		zeroMap = int(tb.menu_.chk015.isChecked()) #[12] check for 0 uv face area
		zeroMapTol = tb.menu_.s008.value() #[13] tolerance for uv face areas
		sharedUVs = int(tb.menu_.chk016.isChecked()) #[14] Unshare uvs that are shared across vertices
		nonmanifold = int(tb.menu_.chk017.isChecked()) #[15] check for nonmanifold polys
		lamina = -int(tb.menu_.chk018.isChecked()) #[16] check for lamina polys [default -1]
		invalidComponents = 0 #int(tb.menu_.chk019.isChecked()) #[17] a guess what this arg does. not checked. default is 0.

		# if tb.menu_.chk005.isChecked(): #All Geometry. Select components for cleanup from all visible geometry in the scene
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
		tb = self.ui.tb002
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Delete Edge Loop', setObjectName='chk001', setToolTip='Delete the edge loops of any edges selected.')
			tb.menu_.add('QCheckBox', setText='Delete Edge Ring', setObjectName='chk000', setToolTip='Delete the edge rings of any edges selected.')
			tb.menu_.add('QCheckBox', setText='Delete Edge Border', setObjectName='chk021', setToolTip='Delete the edge rings of any edges selected.')
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
					if tb.menu_.chk000.isChecked(): #delete ring.
						pm.polySelect(edgeRing=True) #select the edge ring.
					if tb.menu_.chk001.isChecked(): #delete loop.
						pm.polySelect(edgeLoop=True) #select the edge loop.
					if tb.menu_.chk021.isChecked(): #delete border.
						pm.polySelect(edgeBorder=True) #select connected border edges.
					pm.polyDelEdge(cleanVertices=True) #delete edges

				elif all([selectionMask==1, maskVertex==1]):
					pm.polyDelVertex() #try delete vertices
					if pm.ls(sl=1)==objects: #if nothing was deleted:
						mel.eval('polySelectSp -loop;') #convert selection to edge loop
						pm.polyDelEdge(cleanVertices=True) #delete edges

				else: #all([selectionMask==1, maskFacet==1]):
					pm.delete(obj) #delete faces\mesh objects


	def tb003(self, state=None):
		'''
		Delete Along Axis
		'''
		tb = self.ui.tb003
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='-', setObjectName='chk006', setChecked=True, setToolTip='Perform delete along negative axis.')
			tb.menu_.add('QRadioButton', setText='X', setObjectName='chk007', setChecked=True, setToolTip='Perform delete along X axis.')
			tb.menu_.add('QRadioButton', setText='Y', setObjectName='chk008', setToolTip='Perform delete along Y axis.')
			tb.menu_.add('QRadioButton', setText='Z', setObjectName='chk009', setToolTip='Perform delete along Z axis.')

			self.connect_('chk006-9', 'toggled', self.chk006_9, tb.menu_)
			return

		selection = pm.ls(sl=1, objectsOnly=1)
		axis = self.getAxisFromCheckBoxes('chk006-9', tb.menu_)

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
