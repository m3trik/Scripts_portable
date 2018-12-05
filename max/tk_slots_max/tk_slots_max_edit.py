import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Edit(Init):
	def __init__(self, *args, **kwargs):
		super(Edit, self).__init__(*args, **kwargs)


		

		self.hotBox.ui.s000.valueChanged.connect(self.chk011) #update radial array
		self.hotBox.ui.s001.valueChanged.connect(self.chk011) 

	def chk001(self): #delete: negative axis. set text mirror axis
		if self.hotBox.ui.chk002.isChecked():
			axis = "X"
			if self.hotBox.ui.chk001.isChecked():
				axis = "-X"
		if self.hotBox.ui.chk003.isChecked():
			axis = "Y"
			if self.hotBox.ui.chk001.isChecked():
				axis = "-Y"
		if self.hotBox.ui.chk004.isChecked():
			axis = "Z"
			if self.hotBox.ui.chk001.isChecked():
				axis = "-Z"
		self.hotBox.ui.b000.setText("Mirror "+axis)

	#set check states
	def chk002(self): #delete: x axis
		self.setButtons(self.hotBox.ui, unchecked='chk003,chk004')
		axis = "X"
		if self.hotBox.ui.chk001.isChecked():
			axis = "-X"
		self.hotBox.ui.b000.setText("Mirror "+axis)

	def chk003(self): #delete: y axis
		self.setButtons(self.hotBox.ui, unchecked='chk002,chk004')
		axis = "Y"
		if self.hotBox.ui.chk001.isChecked():
			axis = "-Y"
		self.hotBox.ui.b000.setText("Mirror "+axis)

	def chk004(self): #delete: z axis
		self.setButtons(self.hotBox.ui, unchecked='chk003,chk002')
		axis = "Z"
		if self.hotBox.ui.chk001.isChecked():
			axis = "-Z"
		self.hotBox.ui.b000.setText("Mirror "+axis)

	def chk007(self): #delete: translate to components
		if self.hotBox.ui.chk007.isChecked():
			self.setButtons(self.hotBox.ui, enable='chk008,b034,cmb000',disable='chk000,chk009,s005')
			self.b034()
		else:
			self.setButtons(self.hotBox.ui, disable='chk008,b034,cmb000',enable='chk000,chk009,s005')

	def chk010(self): #Radial Array: set pivot
		global radialPivot
		radialPivot=[]
		#add support for averaging multiple components.
		if self.hotBox.ui.chk010.isChecked():
			selection = pm.ls (selection=1, flatten=1)
			try:
				pivot = pm.xform (selection, query=1, translation=1, relative=1)
			except:
				print "# Warning: Nothing selected. #"
				self.setButtons(self.hotBox.ui, unchecked='chk010')
				return
			# radialPivot.extend ([pivot[0],pivot[1],pivot[2]])
			radialPivot.extend (pivot) #extend the list contents
			text = str(int(pivot[0]))+","+str(int(pivot[1]))+","+str(int(pivot[2])) #convert to int to
			self.hotBox.ui.chk010.setText(text)
		else:
			del radialPivot[:]
			self.hotBox.ui.chk010.setText("Set Pivot")

	def chk011(self): #Radial array: instance/duplicate toggle
		self.chk015() #calling chk015 directly from valueChanged would pass the returned spinbox value to the create arg

	def chk012(self): #Radial array: x axis
		self.setButtons(self.hotBox.ui, checked='chk012', unchecked='chk013,chk014')
		self.chk015()

	def chk013(self): #Radial array: y axis
		self.setButtons(self.hotBox.ui, checked='chk013', unchecked='chk012,chk014')
		self.chk015()

	def chk014(self): #Radial array: z axis
		self.setButtons(self.hotBox.ui, checked='chk014', unchecked='chk012,chk013')
		self.chk015()

	def chk015(self, create=False): #Duplicate radial array.
		global radialArrayObjList
		radialArrayObjList=[]
		setPivot = self.hotBox.ui.chk010.isChecked() #set pivot point
		instance = self.hotBox.ui.chk011.isChecked() #instance object

		if self.hotBox.ui.chk015.isChecked():
			self.setButtons(self.hotBox.ui, enable='b008')

			selection = pm.ls (selection=1, type="transform", flatten=1)
			if len(selection):				
				objectName = str(selection[0])
				if len(radialArrayObjList):
					self.try_ ('pm.delete (radialArrayObjList)')
					del radialArrayObjList[:]

				numDuplicates = int(self.hotBox.ui.s000.value())
				angle = float(self.hotBox.ui.s001.value())

				x=y=z = 0
				if self.hotBox.ui.chk012.isChecked():
					x = angle
				if self.hotBox.ui.chk013.isChecked():
					y = angle
				if self.hotBox.ui.chk014.isChecked():
					z = angle

				pm.undoInfo (openChunk=1)
				for i in xrange(1,numDuplicates):
					if instance:
						name = objectName+"_ins"+str(i)
						pm.instance (name=name)
					else:
						name = objectName+"_dup"+str(i)
						pm.duplicate (returnRootsOnly=1, name=name)
					if setPivot:
						if len(radialPivot):
							pm.rotate (x, y, z, relative=1, pivot=radialPivot)
						else:
							print "# Warning: No pivot point set. #"
					else:
						pm.rotate (x, y, z, relative=1)
					radialArrayObjList.append(name)
				#if in isolate select mode; add object	
				currentPanel = pm.paneLayout('viewPanes', q=True, pane1=True) #get the current modelPanel view
				if pm.isolateSelect (currentPanel, query=1, state=1):
					for obj in radialArrayObjList:
						pm.isolateSelect (currentPanel, addDagObject=obj)
				#re-select the original selected object
				pm.select (objectName)
				pm.undoInfo (closeChunk=1)
			else: #if both lists objects are empty:
				print "# Warning: Nothing selected. #"
				self.setButtons(self.hotBox.ui, disable='b008',unchecked='chk015')
				return
		else: #if chk015 is unchecked by user or by create button
			if create:
				originalObj = radialArrayObjList[0][:radialArrayObjList[0].rfind("_")] #remove the trailing _ins# or _dup#. ie. pCube1 from pCube1_inst1
				radialArrayObjList.append(originalObj)
				pm.polyUnite (radialArrayObjList, name=originalObj+"_array") #combine objects. using the original name results in a duplicate object error on deletion
				print "# Result: "+str(radialArrayObjList)+" #"
				pm.delete (radialArrayObjList); del radialArrayObjList[:]
				return
			self.try_('pm.delete (radialArrayObjList)'); del radialArrayObjList[:]
			self.setButtons(self.hotBox.ui, disable='b008')
			

	def b000(self): #Mirror geometry
		mergeThreshold=0.005
		axis = 0 #0=x 1=y, 2=z
		y=z= 1; x=-1 #used to negaively scale instanced object
		cutMesh = self.hotBox.ui.chk005.isChecked() #cut
		axisStr = self.hotBox.ui.b000.text()
		instance = self.hotBox.ui.chk021.isChecked()
		if axisStr == "Mirror Y" or axisStr == "Mirror -Y":
			axis=1; y=-1; x=1
		if axisStr == "Mirror Z" or axisStr == "Mirror -Z":
			axis=2; z=-1; x=1
		if not instance:
			pm.polyMirrorFace (cutMesh=cutMesh, axis=axis, axisDirection=1, mergeMode=1, mergeThresholdType=1, mergeThreshold=mergeThreshold, mirrorAxis=1, mirrorPosition=0, smoothingAngle=30, flipUVs=0, ch=0)
		else:
			pm.undoInfo(openChunk=1)
			if cutMesh:
				self.b032()
			instance = pm.instance() # bt_convertToMirrorInstanceMesh(0); #x=0, y=1, z=2, -x=3, -y=4, -z=5
			pm.scale (z,x,y, pivot=(0,0,0), relative=1) #zxy
			pm.undoInfo(closeChunk=1)
		
	def b002(self): #Mirror options
		maxEval('MirrorPolygonGeometryOptions;')

	def b003(self): #Convert N-sided faces to quads
		maxEval('macros.run \"Modifiers\" \"QuadifyMeshMod\"')

	def b004(self): #Measure
		maxEval('macros.run \"Tools\" \"two_point_dist\"')

	def b005(self): #
		pass

	def b006(self): #Maya bonus tools: Symmetrize
		maxEval('dR_symmetrize;')

	def b007(self): #Mirror instance mesh
		maxEval('bt_mirrorInstanceMesh;')

	def b008(self): #create radial array
		self.hotBox.ui.chk015.setChecked(False) #must be in the false unchecked state to catch the create flag in chk015
		self.chk015(create=True)
		
	def b009(self): #select instanced objects
		if self.hotBox.ui.chk016.isChecked(): #select all instances
			import maya.OpenMaya as om
			#get all Instanced objects
			instances = []
			iterDag = om.MItDag(om.MItDag.kBreadthFirst)
			while not iterDag.isDone():
				instanced = om.MItDag.isInstanced(iterDag)
				if instanced:
					instances.append(iterDag.fullPathName())
				iterDag.next()
			pm.select (instances)
		else:
			try:
				selectedObj = pm.ls (sl=1)[0]
				pm.select (selectedObj, deselect=1)
				shapes = pm.listRelatives (selectedObj, s=1)
				maxEval('select `listRelatives -ap '+shapes[0]+'`;')
			except:
				print "# Warning: No valid object selected."

	def b010(self): #uninstance selected objects
		selectedObjects = pm.ls (sl=1)
		#uninstance:
		while len(selectedObjects):
			parent = pm.listRelatives(instances[0], parent=True)[0]
			pm.duplicate(parent, renameChildren=True)
			pm.delete(parent)
			instances = getInstances()

	def b011(self): #Duplicate special
		maxEval('DuplicateSpecialOptions;')

	def b012(self): #Find and select N-gons
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

	def b013(self): #Select components for cleanup from all visible geometry in the scene
		scene = pm.ls (visible=1, geometry=1)
		[pm.select (geometry, add=1) for geometry in scene]
		mel.eval(r'polyCleanupArgList 3 { "0","2","1","0","1","0","0","0","0","1e-005","1","1e-005","0","1e-005","0","1","1" };')

	def b014(self): #Cleanup
		scene = pm.ls (visible=1, geometry=1)
		[pm.select (geometry, add=1) for geometry in scene]
		mel.eval(r'polyCleanupArgList 4 { "0","1","1","0","1","0","1","0","0","1e-005","1","0.0001","0","1e-005","0","1","1","0" };')

	def b015(self): #Cleanup options
		maxEval('CleanupPolygonOptions;')

	def b016(self): #Delete history
		all_ = self.hotBox.ui.chk018.isChecked()
		unusedNodes = self.hotBox.ui.chk019.isChecked()
		deformers = self.hotBox.ui.chk020.isChecked()
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

	def b017(self): #
		pass

	def b018(self): #
		pass

	def b019(self): #
		pass

	def b020(self): #
		pass

	def b021(self): #Tranfer maps
		maxEval('performSurfaceSampling 1;')

	def b022(self): #Transfer vertex order
		maxEval('TransferVertexOrder;')

	def b023(self): #Transfer attribute values
		maxEval('TransferAttributeValues;')

	def b024(self): #Transfer attribute values options
		maxEval('TransferAttributeValuesOptions;')

	def b025(self): #Batch transfer attributes
		maxEval('tk_batchTransform();')

	def b026(self): #Transfer attributes options
		maxEval('performTransferAttributes 1;')

	def b027(self): #Shading sets
		maxEval('performTransferShadingSets 0;')

	def b028(self): #Shading sets options
		maxEval('performTransferShadingSets 1;')

	def b029(self): #Annotation
		maxEval('CreateAnnotateNode;')

	def b030(self): #Calculator
		maxEval('calculator;')

	def b031(self): #Grease Pencil
		maxEval('greasePencilCtx;')

	def b032(self): #Delete component or if object selected, along axis   #maxEval('polyMirrorCut 1 1 0.001;')
		selectionMask = pm.selectMode (query=True, component=True)
		maskVertex = pm.selectType (query=True, vertex=True)
		maskEdge = pm.selectType (query=True, edge=True)
		# maskFacet = pm.selectType (query=True, facet=True)

		if all([selectionMask==1, maskEdge==1]): #delete edges
			pm.polyDelEdge (cleanVertices=True)
			self.viewPortMessage("delete <hl>edge(s)</hl>.")

		if all([selectionMask==1, maskVertex==1]): #delete vertices
			pm.polyDelVertex()
			self.viewPortMessage("delete <hl>vertice(s)</hl>.")

		if selectionMask==0: #object mode /delete faces along axis
			if self.hotBox.ui.chk002.isChecked():
				axis = "x"
				if self.hotBox.ui.chk001.isChecked():
					axis = "-x"
			if self.hotBox.ui.chk003.isChecked():
				axis = "y"
				if self.hotBox.ui.chk001.isChecked():
					axis = "-y"
			if self.hotBox.ui.chk004.isChecked():
				axis = "z"
				if self.hotBox.ui.chk001.isChecked():
					axis = "-z"

			faces = self.getAllFacesOnAxis (axis)
			pm.delete(faces)
			self.viewPortMessage("delete faces on <hl>"+axis+"</hl>.")
			return axis

		else:
			pm.delete()
			self.viewPortMessage("delete.")

	def b033(self): #duplicate
			instance = self.hotBox.ui.chk000.isChecked()
			amount = int(self.hotBox.ui.s005.value())
			keepFacesTogether = self.hotBox.ui.chk009.isChecked()
			transXYZ = [float(self.hotBox.ui.s002.value()),float(self.hotBox.ui.s003.value()),float(self.hotBox.ui.s004.value())]
			transRelative = self.hotBox.ui.chk017.isChecked() #xform translate relative or absolute
			translateToComponent = self.hotBox.ui.chk007.isChecked()
			alignToNormal = self.hotBox.ui.chk008.isChecked()
			componentList = [self.hotBox.ui.cmb000.itemText(i) for i in range(self.hotBox.ui.cmb000.count())]

			selection = pm.ls (selection=1, flatten=1)

			if len(selection)>0:
				pm.undoInfo (openChunk=1)
				if translateToComponent:
					object_ = selection[0]
					if translateToComponent and len(componentList)!=0:
						num=0
						for component in componentList:
							if ".vtx" in str(component):
								x = pm.polyNormalPerVertex (component, query=1, x=1)
								y = pm.polyNormalPerVertex (component, query=1, y=1)
								z = pm.polyNormalPerVertex (component, query=1, z=1)
								xyz = [sum(x) / float(len(x)), sum(y) / float(len(y)), sum(z) / float(len(z))] #get average
							elif ".e" in str(component):
								componentName = str(component).split(".")[0]
								vertices = pm.polyInfo (component, edgeToVertex=1)[0]
								vertices = vertices.split()
								vertices = [componentName+".vtx["+vertices[2]+"]",componentName+".vtx["+vertices[3]+"]"]
								x=[];y=[];z=[]
								for vertex in vertices:
									x_ = pm.polyNormalPerVertex (vertex, query=1, x=1)
									x.append(sum(x_) / float(len(x_)))
									y_ = pm.polyNormalPerVertex (vertex, query=1, y=1)
									x.append(sum(y_) / float(len(y_)))
									z_ = pm.polyNormalPerVertex (vertex, query=1, z=1)
									x.append(sum(z_) / float(len(z_)))
								xyz = [sum(x) / float(len(x)), sum(y) / float(len(y)), sum(z) / float(len(z))] #get average
							else:# elif ".f" in str(component):
								xyz = pm.polyInfo (component, faceNormals=1)
								xyz = xyz[0].split()
								xyz = [float(xyz[2]), float(xyz[3]), float(xyz[4])]

							if alignToNormal: #normal constraint
								normal = mel.eval("unit <<"+str(xyz[0])+", "+str(xyz[1])+", "+str(xyz[2])+">>;") #normalize value using MEL
								# normal = [round(i-min(xyz)/(max(xyz)-min(xyz)),6) for i in xyz] #normalize and round value using python

								constraint = pm.normalConstraint(component, object_,aimVector=normal,upVector=[0,1,0],worldUpVector=[0,1,0],worldUpType="vector") # "scene","object","objectrotation","vector","none"
								pm.delete(constraint) #orient object_ then remove constraint.

							vertexPoint = pm.xform (component, query=1, translation=1) #average vertex points on destination to get component center.
							x = vertexPoint [0::3]
							y = vertexPoint [1::3]
							z = vertexPoint [2::3]
							vertexPoint = [round(sum(x) / float(len(x)),4), round(sum(y) / float(len(y)),4), round(sum(z) / float(len(z)),4)]

							pm.xform (object_, translation=[vertexPoint[0]+transXYZ[0], vertexPoint[1]+transXYZ[1], vertexPoint[2]+transXYZ[2]])

							if component != componentList[len(componentList)-1]: #if not at the end of the list, create a new instance of the object_.
								name = str(object_)+"_inst"+str(num)
								pm.instance (object_, name=name)
							num+=1
							# print "component:",component,"\n", "normal:",normal,"\n", "vertexPoint:",vertexPoint,"\n"
					else:
						print "# Warning: Component list empty. #"
				else:
					for _ in xrange(amount):
						if ".f" in str(selection):
							objectName = pm.ls (selection=1, flatten=1, objectsOnly=1)[0]
							duplicatedObject = pm.duplicate(objectName, name="pExtract1")[0]

							selectedFaces = [] #create a list of the original selected faces numbers but with duplicated objects name
							for face in selection:
								selectedFaces.append(duplicatedObject+"."+face.split(".")[1])

							allFaces = [] #create a list of all faces on the duplicated object
							numFaces = pm.polyEvaluate(duplicatedObject, face=1)
							for num in range(numFaces):
								allFaces.append(duplicatedObject+".f["+str(num)+"]")

							pm.delete (set(allFaces) -set(selectedFaces)) #delete faces in 'allFaces' that were not in the original selection 
							selection = pm.select (duplicatedObject)
						elif ".e" in str(selection):
							pm.polyToCurve (form=2, degree=3, conformToSmoothMeshPreview=1)
						elif instance:
							pm.instance()
						else:
							pm.duplicate()
						if any([transXYZ[0]!=0, transXYZ[1]!=0, transXYZ[2]!=0]): #if anything other than 0 is input into the texfields; transform
							pm.xform (relative=transRelative, translation=transXYZ)
				pm.undoInfo (closeChunk=1)
			else:
				print "# Warning: Nothing selected. #"

	def b034(self): #add selected components to cmb000
		self.comboBox (self.hotBox.ui.cmb000, pm.ls (selection=1, flatten=1))

	def b035(self): #
		pass

	def b036(self): #
		pass

	def b037(self): #
		pass

	def b038(self): #
		pass

	def b039(self): #
		pass

	def b040(self): #
		pass

	def b041(self): #
		pass

	def b042(self): #hold crease set name for crease set transfer
		if self.hotBox.ui.b042.isChecked():
			creaseSet = str(pm.ls(selection=1)) #ex. [nt.CreaseSet(u'creaseSet1')]

			index1 = creaseSet.find("u")
			index2 = creaseSet.find(")")
			creaseSet = creaseSet[index1+1:index2].strip("'") #ex. creaseSet1

			if creaseSet != "[":
				self.hotBox.ui.b042.setText(creaseSet)
			else:
				self.hotBox.ui.b042.setText("must select set first")
				self.setButtons(self.hotBox.ui, unchecked='b042')
			if self.hotBox.ui.b043.isChecked():
				self.setButtons(self.hotBox.ui, enable='b052')
		else:
			self.hotBox.ui.b042.setText("Crease Set")

	def b043(self): #hold transform node name for crease set transfer
		if self.hotBox.ui.b043.isChecked():
			newObject = str(pm.ls(selection=1)) #ex. [nt.Transform(u'pSphere1')]

			index1 = newObject.find("u")
			index2 = newObject.find(")")
			newObject = newObject[index1+1:index2].strip("'") #ex. pSphere1

			if newObject != "[":
				self.hotBox.ui.b043.setText(newObject)
			else:
				self.hotBox.ui.b043.setText("must select obj first")
				self.setButtons(self.hotBox.ui, unchecked='b043')
			if self.hotBox.ui.b042.isChecked():
				self.setButtons(self.hotBox.ui, enable='b052')
		else:
			self.hotBox.ui.b043.setText("Object")

	def b044(self): #Poly reduce
		mel.eval("polyReduce -version 1 -keepCreaseEdgeWeight 1;")

	def b045(self): #Reduce
		mel.eval("ReducePolygon;")

	def b046(self): #Reduce options
		mel.eval("ReducePolygonOptions;")

	def b047(self): #Smooth options
		mel.eval("SmoothPolygonOptions;")

	def b048(self): #Add Divisions - subdivide mesh
		maxEval('macros.run \"Modifiers\" \"Tessellate\"')

	def b049(self): #Smooth
		maxEval('macros.run \"Modifiers\" \"Smooth\"')

	def b050(self): #add divisions options
		maxEval('''
		Try 
		(
			local A = modPanel.getCurrentObject()
			A.popupDialog #Tessellate
		)
		Catch ()
		''')

	def b051(self): #Apply smooth preview
		mel.eval("performSmoothMeshPreviewToPolygon;") #convert smooth mesh preview to polygons

	def b052(self): #transfer crease edges
		'''
		an updated version of this is in the maya python projects folder
		the use of separate buttons for donar and target mesh are obsolete
		add pm.polySoftEdge (angle=0, constructionHistory=0); #harden edge, when applying crease 
		'''
		creaseSet = str(self.hotBox.ui.b042.text())
		newObject = str(self.hotBox.ui.b043.text())

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

		self.setButtons(self.hotBox.ui, disable='b052', unchecked='b042')#,self.hotBox.ui.b043])
		self.hotBox.ui.b042.setText("Crease Set")
		# self.hotBox.ui.b043.setText("Object")









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

# maxEval('max array')

# maxEval('max mirror')