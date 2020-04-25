from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Polygons(Init):
	def __init__(self, *args, **kwargs):
		super(Polygons, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('polygons')
		self.submenu = self.sb.getUi('polygons_submenu')



	def chk008(self):
		'''
		Split U
		'''
		self.toggleWidgets(self.ui, self.submenu, setChecked_False='chk010')


	def chk009(self):
		'''
		Split V
		'''
		self.toggleWidgets(self.ui, self.submenu, setChecked_False='chk010')


	def chk010(self):
		'''
		Tris
		'''
		self.toggleWidgets(self.ui, self.submenu, setChecked_False='chk008-9')


	def cmb000(self, index=None):
		'''
		Header comboBox
		'''
		cmb = self.ui.cmb000

		files = ['Extrude Options','Bevel Options','Bridge Options','Combine Options','Merge Vertex Options','Offset Edgeloop','Edit Edgeflow Options','Extract Curve Options','Poke Options','Wedge Options','Assign Invisible Options']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Extrude Options'):
				mel.eval("PolyExtrudeOptions;")
			if index==contents.index('Bevel Options'):
				mel.eval('BevelPolygonOptions;')
			if index==contents.index('Bridge Options'):
				mel.eval("BridgeEdgeOptions;")
			if index==contents.index('Combine Options'):
				mel.eval('CombinePolygonsOptions;')
			if index==contents.index('Merge Vertex Options'):
				mel.eval('PolyMergeOptions;')
			if index==contents.index('Offset Edgeloop'):
				mel.eval("DuplicateEdgesOptions;")
			if index==contents.index('Edit Edgeflow Options'):
				mel.eval("PolyEditEdgeFlowOptions;")
			if index==contents.index('Extract Curve Options'):
				mel.eval('CreateCurveFromPolyOptions;')
			if index==contents.index('Poke Options'):
				mel.eval("PokePolygonOptions;")
			if index==contents.index('Wedge Options'):
				mel.eval("WedgePolygonOptions;")
			if index==contents.index('Assign Invisible Options'):
				mel.eval("PolyAssignSubdivHoleOptions;")
			cmb.setCurrentIndex(0)


	def tb000(self, state=None):
		'''
		Merge Vertices
		'''
		tb = self.ui.tb000
		if state=='setMenu':
			tb.add('QDoubleSpinBox', setPrefix='Distance: ', setObjectName='s002', preset_='0.000-10 step.001', setValue=0.001, setToolTip='Merge Distance.')
			return

		tolerance = float(tb.s002.value())
		selection = pm.ls(selection=1, objectsOnly=1)

		if selection:
			if pm.selectMode(query=1, component=1): #merge selected components.
				if pm.filterExpand(selectionMask=31): #selectionMask=vertices
					pm.polyMergeVertex(distance=tolerance, alwaysMergeTwoVertices=True, constructionHistory=True)
				else: #if selection type =edges or facets:
					mel.eval("MergeToCenter;")

			else: #if object mode. merge all vertices on the selected object.
				for n, obj in enumerate(selection):
					if not self.ui.progressBar.step(n, len(selection)): #register progress while checking for cancellation:
						break

					# get number of vertices
					count = pm.polyEvaluate(obj, vertex=1)
					vertices = str(obj) + ".vtx [0:" + str(count) + "]" # mel expression: select -r geometry.vtx[0:1135];
					pm.polyMergeVertex(vertices, distance=tolerance, alwaysMergeTwoVertices=False, constructionHistory=False)

				#return to original state
				pm.select(clear=1)

				for obj in selection:
					pm.select(obj, add=1)
		else:
			print("# Warning: No object selected. Must select an object or component. #")
			return


	def tb001(self, state=None):
		'''
		Bridge
		'''
		tb = self.ui.tb001
		if state=='setMenu':
			tb.add('QSpinBox', setPrefix='Divisions: ', setObjectName='s003', preset_='0-10000 step1', setValue=0.001, setToolTip='Divisions.')
			return

		divisions = tb.s003.value()

		selection = pm.ls(sl=1)
		edges = pm.filterExpand(selection, selectionMask=32, expand=1) #get edges from selection

		pm.polyBridgeEdge(edges, divisions=divisions) #bridge edges
		pm.polyCloseBorder(edges) #fill edges if they lie on a border


	def tb002(self, state=None):
		'''
		Combine
		'''
		tb = self.ui.tb002
		if state=='setMenu':
			tb.add('QCheckBox', setText='Merge', setObjectName='chk000', setChecked=True, setToolTip='Combine selected meshes and merge any coincident verts/edges.')
			return

		# pm.polyUnite( 'plg1', 'plg2', 'plg3', name='result' ) #for future reference. if more functionality is needed use polyUnite
		if tb.chk000.isChecked():
			mel.eval('bt_mergeCombineMeshes;')
		else:
			mel.eval('CombinePolygons;')


	def tb003(self, state=None):
		'''
		Extrude
		'''
		tb = self.ui.tb003
		if state=='setMenu':
			tb.add('QCheckBox', setText='Keep Faces Together', setObjectName='chk002', setChecked=True, setToolTip='Keep edges/faces together.')
			return

		keepFacesTogether = tb.chk002.isChecked() #keep faces/edges together.

		if pm.selectType(query=1, facet=1): #face selection
			pm.polyExtrudeFacet(keepFacesTogether=keepFacesTogether)
		elif pm.selectType(query=1, edge=1): #edge selection
			pm.polyExtrudeEdge(keepFacesTogether=keepFacesTogether)


	def tb004(self, state=None):
		'''
		Bevel (Chamfer)
		'''
		tb = self.ui.tb004
		if state=='setMenu':
			tb.add('QDoubleSpinBox', setPrefix='Width: ', setObjectName='s000', preset_='0.00-100 step.01', setValue=0.01, setToolTip='Bevel Width.')
			return

		width = float(tb.s000.value())
		chamfer = True
		segments = 1

		pm.polyBevel3 (fraction=width, offsetAsFraction=1, autoFit=1, depth=1, mitering=0, 
			miterAlong=0, chamfer=chamfer, segments=segments, worldSpace=1, smoothingAngle=30, subdivideNgons=1,
			mergeVertices=1, mergeVertexTolerance=0.0001, miteringAngle=180, angleTolerance=180, ch=0)


	def tb005(self, state=None):
		'''
		Detach
		'''
		tb = self.ui.tb005
		if state=='setMenu':
			tb.add('QCheckBox', setText='Delete Original', setObjectName='chk007', setChecked=True, setToolTip='Delete original selected faces.')
			return

		vertexMask = pm.selectType (query=True, vertex=True)
		edgeMask = pm.selectType (query=True, edge=True)
		facetMask = pm.selectType (query=True, facet=True)

		if vertexMask:
			mel.eval("polySplitVertex()")

		if facetMask:
			maskVertex = pm.selectType (query=True, vertex=True)
			if maskVertex:
				mel.eval("DetachComponent;")
			else:
				selFace = pm.ls (ni=1, sl=1)
				selObj = pm.ls (objectsOnly=1, noIntermediate=1, sl=1) #to errorcheck if more than 1 obj selected

				if len(selFace) < 1:
					print("# Warning: Nothing selected. #")
					return
				if len(selObj) > 1:
					print("# Warning: Only components from a single object can be extracted. #")
					return
				else:
					pm.undoInfo (openChunk=1)
					sel = str(selFace[0]).split(".") #creates ex. ['polyShape', 'f[553]']
					print(sel)
					extractedObject = "extracted_"+sel[0]
					pm.duplicate (sel[0], name=extractedObject)
					if tb.chk007.isChecked(): #delete original
						pm.delete (selFace)

					allFace = [] #populate a list of all faces in the duplicated object
					numFaces = pm.polyEvaluate(extractedObject, face=1)
					num=0
					for _ in range(numFaces):
						allFace.append(extractedObject+".f["+str(num)+"]")
						num+=1

					extFace = [] #faces to keep
					for face in selFace:
						fNum = str(face.split(".")[0]) #ex. f[4]
						extFace.append(extractedObject+"."+fNum)

					delFace = [x for x in allFace if x not in extFace] #all faces not in extFace
					pm.delete (delFace)

					pm.select (extractedObject)
					pm.xform (cpc=1) #center pivot
					pm.undoInfo (closeChunk=1)
					return extractedObject


	def tb006(self, state=None):
		'''
		Inset Face Region
		'''
		tb = self.ui.tb006
		if state=='setMenu':
			tb.add('QDoubleSpinBox', setPrefix='Offset: ', setObjectName='s001', preset_='0.00-100 step.01', setValue=2.00, setToolTip='Offset amount.')
			return

		offset = float(tb.s001.value())
		pm.polyExtrudeFacet (keepFacesTogether=1, pvx=0, pvy=40.55638003, pvz=33.53797107, divisions=1, twist=0, taper=1, offset=offset, thickness=0, smoothingAngle=30)


	def tb007(self, state=None):
		'''
		Divide Facet
		'''
		tb = self.ui.tb007
		if state=='setMenu':
			tb.add('QCheckBox', setText='U', setObjectName='chk008', setChecked=True, setToolTip='Divide facet: U coordinate.')
			tb.add('QCheckBox', setText='V', setObjectName='chk009', setChecked=True, setToolTip='Divide facet: V coordinate.')
			tb.add('QCheckBox', setText='Tris', setObjectName='chk010', setToolTip='Divide facet: Tris.')
			return

		dv=u=v=0
		if tb.chk008.isChecked(): #Split U
			u=2
		if tb.chk009.isChecked(): #Split V
			v=2

		mode = 0 #The subdivision mode. 0=quads, 1=triangles
		subdMethod = 1 #subdivision type: 0=exponential(traditional subdivision) 1=linear(number of faces per edge grows linearly)
		if tb.chk010.isChecked(): #tris
			mode=dv=1
			subdMethod=0
		if all([tb.chk008.isChecked(), tb.chk009.isChecked()]): #subdivide once into quads
			dv=1
			subdMethod=0
			u=v=0
		#perform operation
		selectedFaces = pm.filterExpand (pm.ls(sl=1), selectionMask=34, expand=1)
		if selectedFaces:
			for face in selectedFaces: #when performing polySubdivideFacet on multiple faces, adjacent subdivided faces will make the next face an n-gon and therefore not able to be subdivided. 
				pm.polySubdivideFacet(face, divisions=0, divisionsU=2, divisionsV=2, mode=0, subdMethod=1)
		else:
			print('# Warning: No faces selected. #')


	def b000(self):
		'''
		Circularize
		'''
		pm.polyCircularize(constructionHistory=1, alignment=0, radialOffset=0, normalOffset=0, normalOrientation=0, smoothingAngle=30, evenlyDistribute=1, divisions=0, supportingEdges=0, twist=0, relaxInterior=1)


	def b001(self):
		'''
		Fill Holes
		'''
		mel.eval('FillHole;')


	def b002(self):
		'''
		Separate
		'''
		mel.eval('SeparatePolygon;')


	def b004(self):
		'''
		Slice
		'''
		maxEval('macros.run "Ribbon - Modeling" "CutsQuickSlice"')


	def b009(self):
		'''
		Collapse Component
		'''
		# mel.eval("MergeToCenter;") #collapse vertices
		mel.eval('PolygonCollapse;')


	def b010(self):
		'''
		Extract Curve
		'''
		# mel.eval('CreateCurveFromPoly;')
		pm.polyToCurve (form=2, degree=3, conformToSmoothMeshPreview=True) #degree: 1=linear,2= ,3=cubic,5= ,7=


	def b012(self):
		'''
		Multi-Cut Tool
		'''
		mel.eval('dR_multiCutTool;')


	def b015(self):
		'''
		Delete Edgeloop
		'''
		mel.eval("bt_polyDeleteEdgeLoopTool;")


	def b021(self):
		'''
		Connect Border Edges
		'''
		mel.eval("performPolyConnectBorders 0;")


	def b022(self):
		'''
		Attach
		'''
		mel.eval("dR_connectTool;")


	def b023(self):
		'''
		Boolean
		'''
		mel.eval("PolygonBooleanUnion;")


	def b028(self):
		'''
		Quad Draw
		'''
		mel.eval("dR_quadDrawTool;")


	def b032(self):
		'''
		Poke
		'''
		mel.eval("PokePolygon;")


	def b034(self):
		'''
		Wedge
		'''
		mel.eval("WedgePolygon;")


	def b038(self):
		'''
		Assign Invisible
		'''
		mel.eval("polyHole -assignHole 1;")


	def b043(self):
		'''
		Target Weld
		'''
		mel.eval("dR_targetWeldTool;")

		#max method:
		# for obj in rt.selection:
		# 	vertexNum = [i.index for i in obj.selectedVerts]
		# 	target = rt.polyOp.getVert(obj, index[-1])
			
		# 	for vNum in vertexNum:
		# 		rt.polyop.weldVerts (obj, vertexNum[0], vNum, target)


	def b045(self):
		'''
		Re-Order Vertices
		'''
		symmetryOn = pm.symmetricModelling(query=True, symmetry=True) #query symmetry state
		if symmetryOn:
			pm.symmetricModelling(symmetry=False)
		mel.eval("setPolygonDisplaySettings(\"vertIDs\");") #set vertex id on
		mel.eval("doBakeNonDefHistory( 1, {\"pre\"});") #history must be deleted
		mel.eval("performPolyReorderVertex;") #start vertex reorder ctx


	def b046(self):
		'''
		Split
		'''
		vertexMask = pm.selectType (query=True, vertex=True)
		edgeMask = pm.selectType (query=True, edge=True)
		facetMask = pm.selectType (query=True, facet=True)

		if facetMask:
			mel.eval("performPolyPoke 1;")

		if edgeMask:
			mel.eval("polySubdivideEdge -ws 0 -s 0 -dv 1 -ch 0;")

		if vertexMask:
			mel.eval("polyChamferVtx 0 0.25 0;")


	def b047(self):
		'''
		Insert Edgeloop
		'''
		mel.eval("SplitEdgeRingTool;")


	def b048(self):
		'''
		Collapse Edgering
		'''
		mel.eval("bt_polyCollapseEdgeRingTool;")


	def b049(self):
		'''
		Slide Edge Tool
		'''
		mel.eval("SlideEdgeTool;")


	def b050(self):
		'''
		Spin Edge
		'''
		mel.eval("bt_polySpinEdgeTool;")


	def b051(self):
		'''
		Offset Edgeloop
		'''
		mel.eval("performPolyDuplicateEdge 0;")


	def b053(self):
		'''
		Edit Edge Flow
		'''
		mel.eval("PolyEditEdgeFlow;")












#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------
#b008, b010, b011, b019, b024-27, b058, b059, b060