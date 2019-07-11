import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Duplicate(Init):
	def __init__(self, *args, **kwargs):
		super(Duplicate, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('duplicate')
		
		self.ui.s000.valueChanged.connect(self.radialArray) #update radial array
		self.ui.s001.valueChanged.connect(self.radialArray) 

		self.ui.s002.valueChanged.connect(self.duplicateArray) #update duplicate array
		self.ui.s003.valueChanged.connect(self.duplicateArray)
		self.ui.s004.valueChanged.connect(self.duplicateArray)
		self.ui.s005.valueChanged.connect(self.duplicateArray)
		self.ui.s007.valueChanged.connect(self.duplicateArray) 
		self.ui.s008.valueChanged.connect(self.duplicateArray)
		self.ui.s009.valueChanged.connect(self.duplicateArray)



	def radialArray(self):
		'''
		Radial Array: Reset
		'''
		self.chk015() #calling chk015 directly from valueChanged would pass the returned spinbox value to the create arg


	def duplicateArray(self):
		'''
		Duplicate: Reset
		'''
		self.chk016() #calling chk015 directly from valueChanged would pass the returned spinbox value to the create arg


	def chk007(self):
		'''
		Duplicate: Translate To Components
		'''
		if self.ui.chk007.isChecked():
			self.setButtons(self.ui, enable='chk008,b034,cmb000',disable='chk000,chk009,s005')
			self.b008()
		else:
			self.setButtons(self.ui, disable='chk008,b034,cmb000',enable='chk000,chk009,s005')


	def chk010(self):
		'''
		Radial Array: Set Pivot
		'''
		global radialPivot
		radialPivot=[]
		#add support for averaging multiple components.
		if self.ui.chk010.isChecked():
			selection = pm.ls (selection=1, flatten=1)
			if selection:
				vertices = pm.filterExpand(selectionMask=31) #get selected vertices
				if vertices is not None and vertices==1: #if a single vertex is selected, query that vertex position.
					pivot = pm.xform (selection, query=1, translation=1, worldSpace=1)
				else: #else, get the center of the objects bounding box.
					bb = pm.xform (selection, query=1, boundingBox=1, worldSpace=1)
					pivot = bb[0]+bb[3]/2, bb[1]+bb[4]/2, bb[2]+bb[5]/2 #get median of bounding box coordinates. from [min xyz, max xyz]
			else:
				print "# Warning: Nothing selected. #"
				self.setButtons(self.ui, unchecked='chk010')
				return
			# radialPivot.extend ([pivot[0],pivot[1],pivot[2]])
			radialPivot.extend(pivot) #extend the list contents
			text = str(int(pivot[0]))+","+str(int(pivot[1]))+","+str(int(pivot[2]))
			self.ui.chk010.setText(text)
		else:
			del radialPivot[:]
			self.ui.chk010.setText("Set Pivot")


	def chk012(self):
		'''
		Radial Array: X Axis
		'''
		self.setButtons(self.ui, checked='chk012', unchecked='chk013,chk014')
		self.chk015()


	def chk013(self):
		'''
		Radial Array: Y Axis
		'''
		self.setButtons(self.ui, checked='chk013', unchecked='chk012,chk014')
		self.chk015()


	def chk014(self):
		'''
		Radial Array: Z Axis
		'''
		self.setButtons(self.ui, checked='chk014', unchecked='chk012,chk013')
		self.chk015()


	global radialArrayObjList
	radialArrayObjList=[]
	def chk015(self, create=False):
		'''
		Radial Array: Preview
		'''
		setPivot = self.ui.chk010.isChecked() #set pivot point
		instance = self.ui.chk011.isChecked() #instance object

		if self.ui.chk015.isChecked():
			self.setButtons(self.ui, enable='b003')

			selection = pm.ls (selection=1, type="transform", flatten=1)
			if selection:
				if radialArrayObjList:
					self.try_ ('pm.delete(arg1)', showError_=False, arg1=radialArrayObjList) #delete all the geometry in the list
					del radialArrayObjList[:] #clear the list
				for object_ in selection:
					pm.select (object_)
					objectName = str(object_)

					numDuplicates = int(self.ui.s000.value())
					angle = float(self.ui.s001.value())

					x=y=z = 0
					if self.ui.chk012.isChecked(): x = angle
					if self.ui.chk013.isChecked(): y = angle
					if self.ui.chk014.isChecked(): z = angle

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
								pm.rotate (x, y, z, relative=1, pivot=radialPivot) #euler=1
							else:
								print "# Warning: No pivot point set. #"
						else:
							pm.rotate (x, y, z, relative=1) #euler=1
						radialArrayObjList.append(name)
					#if in isolate select mode; add object	
					currentPanel = pm.paneLayout('viewPanes', q=True, pane1=True) #get the current modelPanel view
					if pm.isolateSelect (currentPanel, query=1, state=1):
						for obj_ in radialArrayObjList:
							pm.isolateSelect (currentPanel, addDagObject=obj_)
					#re-select the original selected object
					pm.select (objectName)
					pm.undoInfo (closeChunk=1)
			else: #if both lists objects are empty:
				print "# Warning: Nothing selected. #"
				self.setButtons(self.ui, disable='b003',unchecked='chk015')
				return
		else: #if chk015 is unchecked by user or by create button
			if create:
				originalObj = radialArrayObjList[0][:radialArrayObjList[0].rfind("_")] #remove the trailing _ins# or _dup#. ie. pCube1 from pCube1_inst1
				radialArrayObjList.append(originalObj)
				pm.polyUnite (radialArrayObjList, name=originalObj+"_array") #combine objects. using the original name results in a duplicate object error on deletion
				print "# Result: "+str(radialArrayObjList)+" #"
				pm.delete (radialArrayObjList); del radialArrayObjList[:] #delete all geometry and clear the list
				return
			self.try_ ('pm.delete(arg1)', showError_=False, arg1=radialArrayObjList) #delete all the geometry in the list
			del radialArrayObjList[:] #clear the list
			self.setButtons(self.ui, disable='b003')


	global duplicateObjList
	duplicateObjList=[]
	def chk016(self, create=False):
		'''
		Duplicate: Preview
		'''
		if self.ui.chk016.isChecked():
			self.setButtons(self.ui, enable='b002')

			instance = self.ui.chk000.isChecked()
			numOfDuplicates = int(self.ui.s005.value())
			keepFacesTogether = self.ui.chk009.isChecked()
			transXYZ = [float(self.ui.s002.value()),float(self.ui.s003.value()),float(self.ui.s004.value())]
			rotXYZ =  [float(self.ui.s007.value()),float(self.ui.s008.value()),float(self.ui.s009.value())]
			translateToComponent = self.ui.chk007.isChecked()
			alignToNormal = self.ui.chk008.isChecked()
			componentList = [self.ui.cmb000.itemText(i) for i in range(self.ui.cmb000.count())]
			
			try: pm.delete(duplicateObjList[1:]) #delete all the geometry in the list, except the original obj
			except e as error: print e
			del duplicateObjList[1:] #clear the list, leaving the original obj
			selection = pm.ls(selection=1, flatten=1, objectsOnly=1) #there will only be a selection when first called. After, the last selected item will have been deleted with the other duplicated objects, leaving only the original un-selected.

			if selection:
				obj = selection[0]
				duplicateObjList.insert(0, obj) #insert at first index
			elif duplicateObjList:
				obj = duplicateObjList[0]
				pm.select(obj)
			else:
				return '# Warning: Nothing selected. #'

			pm.undoInfo (openChunk=1)
			if translateToComponent:
				if componentList:
					for num, component in componentList.iteritems():
						vertexPoint = self.getComponentPoint(component)

						pm.xform (obj, rotation=[rotXYZ[0], rotXYZ[1], rotXYZ[2]])
						pm.xform (obj, translation=[vertexPoint[0]+transXYZ[0], vertexPoint[1]+transXYZ[1], vertexPoint[2]+transXYZ[2]])

						if component != componentList[len(componentList)-1]: #if not at the end of the list, create a new instance of the obj.
							name = str(obj)+"_inst"+str(num)
							duplicatedObject = pm.instance (obj, name=name)
						# print "component:",component,"\n", "normal:",normal,"\n", "vertexPoint:",vertexPoint,"\n"

						duplicateObjList.append(duplicatedObject) #append duplicated object to list
				else:
					return '# Warning: Component list empty. #'
			else:
				for _ in xrange(numOfDuplicates):
					if ".f" in str(obj): #face
						duplicatedObject = pm.duplicate(name="pExtract1")[0]

						selectedFaces=[duplicatedObject+"."+face.split(".")[1] for face in obj] #create a list of the original selected faces numbers but with duplicated objects name
						
						numFaces = pm.polyEvaluate(duplicatedObject, face=1)
						allFaces = [duplicatedObject+".f["+str(num)+"]" for num in range(numFaces)] #create a list of all faces on the duplicated object

						pm.delete(set(allFaces) -set(selectedFaces)) #delete faces in 'allFaces' that were not in the original obj 

					elif ".e" in str(obj): #edge
						duplicatedObject = pm.polyToCurve(form=2, degree=3, conformToSmoothMeshPreview=1)
					
					elif instance:
						duplicatedObject = pm.instance()

					else:
						duplicatedObject = pm.duplicate()

					pm.xform (duplicatedObject, rotation=rotXYZ, relative=1)
					pm.xform (duplicatedObject, translation=transXYZ, relative=1)

					duplicateObjList.append(duplicatedObject) #append duplicated object to list
					pm.select(duplicatedObject)
			pm.undoInfo (closeChunk=1)

		else: #if chk016 is unchecked by user or by create button
			if create:
				# originalObj = duplicateObjList[0][:duplicateObjList[0].rfind("_")] #remove the trailing _ins# or _dup#. ie. pCube1 from pCube1_inst1
				# duplicateObjList.append(originalObj)
				# pm.polyUnite (duplicateObjList, name=originalObj+"_array") #combine objects. using the original name results in a duplicate object error on deletion
				# print "# Result: "+str(duplicateObjList)+" #"
				# pm.delete(duplicateObjList) #delete all duplicated geometry
				del duplicateObjList[:] #clear the list
				return
			pm.delete(duplicateObjList[1:]) #delete all the geometry in the list, except the original obj
			pm.select(duplicateObjList[:1]) #re-select the original object
			del duplicateObjList[:] #clear the list
			self.setButtons(self.ui, disable='b002')


	def cmb001(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb001
		
		files = ['Duplicate Special']
		contents = self.comboBox (cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Duplicate Special'):
				mel.eval('DuplicateSpecialOptions;')
			cmb.setCurrentIndex(0)


	def b001(self):
		'''

		'''
		pass


	def b002(self):
		'''
		Duplicate: Create
		'''
		self.ui.chk016.setChecked(False) #must be in the false unchecked state to catch the create flag in chk015
		self.chk016(create=True)


	def b003(self):
		'''
		Radial Array: Create
		'''
		self.ui.chk015.setChecked(False) #must be in the false unchecked state to catch the create flag in chk015
		self.chk015(create=True)


	def b004(self):
		'''
		Select Instanced Objects
		'''
		if self.ui.chk017.isChecked(): #select all instances
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
				mel.eval('select `listRelatives -ap '+shapes[0]+'`;')
			except:
				print "# Warning: No valid object selected."


	def b005(self):
		'''
		Uninstance Selected Objects
		'''
		selectedObjects = pm.ls (sl=1)
		#uninstance:
		while len(selectedObjects):
			parent = pm.listRelatives(instances[0], parent=True)[0]
			pm.duplicate(parent, renameChildren=True)
			pm.delete(parent)
			instances = getInstances()


	def b008(self):
		'''
		Add Selected Components To cmb000
		'''
		self.comboBox (self.ui.cmb000, pm.ls (selection=1, flatten=1))








#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------
	# b008, b009, b011
