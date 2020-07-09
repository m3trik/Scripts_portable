from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Materials(Init):
	def __init__(self, *args, **kwargs):
		super(Materials, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('materials')
		self.childUi = self.sb.getUi('materials_submenu')

		self.materials=None
		self.randomMat=None


	@property
	def currentMaterial(self):
		'''
		Get the current material using the current index of the materials combobox.
		'''
		text = self.parentUi.cmb002.currentText()
		return self.materials[text]


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb001', setToolTip='Maya Material Editors')
			pin.add(QLabel_, setText='Material Attributes', setObjectName='lbl004', setToolTip='Show the material attributes in the attribute editor.')
			return


	def chk007(self):
		'''
		'''
		self.parentUi.tb002.setText('Assign Current')


	def chk008(self):
		'''
		'''
		self.parentUi.tb002.setText('Assign Random')


	def chk009(self):
		'''
		'''
		self.parentUi.tb002.setText('Assign New')


	def cmb001(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb001

		if index=='setMenu':
			files = ['Hypershade']
			cmb.addItems_(files, 'Maya Material Editors')
			return

		if index>0:
			if index==cmb.items.index('Hypershade'):
				mel.eval('HypershadeWindow;')
			cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Material list

		args:
			index (int) = parameter on activated, currentIndexChanged, and highlighted signals.
		'''
		cmb = self.parentUi.cmb002

		if index=='setMenu':
			cmb.addToContext(QLabel_, setText='Open in Editor', setObjectName='lbl000', setToolTip='Open material in editor.')
			cmb.addToContext(QLabel_, setText='Rename', setObjectName='lbl001', setToolTip='Rename the current material.')
			cmb.addToContext(QLabel_, setText='Delete', setObjectName='lbl002', setToolTip='Delete the current material.')
			cmb.addToContext(QLabel_, setText='Delete All Unused Materials', setObjectName='lbl003', setToolTip='Delete All unused materials.')
			cmb.addToContext(QLabel_, setText='Refresh', setObjectName='cmb002', setToolTip='Refresh materials list')
			return

		if cmb.lineEdit():
			self.renameMaterial()
			self.lbl001(setEditable=False)
			return

		try:
			sceneMaterials = self.parentUi.tb001.chk000.isChecked()
			idMapMaterials = self.parentUi.tb001.chk001.isChecked()
			favoriteMaterials = self.parentUi.tb001.chk002.isChecked()
		except: #if the toolbox hasn't been constructed yet: default to sceneMaterials
			sceneMaterials = True

		if sceneMaterials:
			materials = self.getSceneMaterials()

		elif idMapMaterials:
			materials = self.getSceneMaterials(startingWith=['ID_'])

		elif favoriteMaterials:
			materials = self.getFavoriteMaterials()

		mats = sorted([mat for mat in set(materials)])
		matNames = [m.name() if hasattr(m,'name') else str(m) for m in mats]
		contents = cmb.addItems_(matNames, clear=True)

		#create and set icons with color swatch
		for i in range(len(mats)):
			try:
				r = int(pm.getAttr(matNames[i]+'.colorR')*255) #convert from 0-1 to 0-255 value and then to an integer
				g = int(pm.getAttr(matNames[i]+'.colorG')*255)
				b = int(pm.getAttr(matNames[i]+'.colorB')*255)
				pixmap = QtGui.QPixmap(100,100)
				pixmap.fill(QtGui.QColor.fromRgb(r, g, b))
				cmb.setItemIcon(i, QtGui.QIcon(pixmap))
			except AttributeError:
				pass

		if index is None:
			index = cmb.currentIndex()

		self.materials = {name:mats[i] for i, name in enumerate(matNames)} #add mat objects to materials dictionary. 'mat name'=key, <mat object>=value


	@Slots.message
	def tb000(self, state=None):
		'''
		Select By Material Id
		'''
		tb = self.currentUi.tb000
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='Shell', setObjectName='chk005', setToolTip='Select entire shell.')
			tb.add('QCheckBox', setText='Invert', setObjectName='chk006', setToolTip='Invert Selection.')
			if state=='setMenu':
				return

		shell = tb.chk005.isChecked() #Select by material: shell
		invert = tb.chk006.isChecked() #Select by material: invert

		if not self.currentMaterial:
			return 'Error: No Material Selection.'

		self.selectByMaterialID(self.currentMaterial, pm.ls(selection=1))


	def tb001(self, state=None):
		'''
		Stored Material Options
		'''
		tb = self.currentUi.tb001
		if not tb.containsMenuItems:
			tb.add('QRadioButton', setText='All Scene Materials', setObjectName='chk000', setChecked=True, setToolTip='List all scene materials.') #Material mode: Scene Materials
			tb.add('QRadioButton', setText='ID Map Materials', setObjectName='chk001', setToolTip='List ID map materials.') #Material mode: ID Map Materials
			tb.add('QRadioButton', setText='Favorite Materials', setObjectName='chk002', setToolTip='List Favorite materials.') #Material mode: Favorite Materials

			self.connect_([tb.chk000, tb.chk001], 'toggled', [self.cmb002, self.tb001])
			if state=='setMenu':
				return

		if tb.chk000.isChecked():
			self.parentUi.group000.setTitle(tb.chk000.text())
		elif tb.chk001.isChecked():
			self.parentUi.group000.setTitle(tb.chk001.text())
		elif tb.chk002.isChecked():
			self.parentUi.group000.setTitle(tb.chk002.text())


	@Slots.message
	def tb002(self, state=None):
		'''
		Assign Material
		'''
		tb = self.currentUi.tb002
		if not tb.containsMenuItems:
			tb.add('QRadioButton', setText='Current Material', setObjectName='chk007', setChecked=True, setToolTip='Re-Assign the current stored material.')
			tb.add('QRadioButton', setText='New Material', setObjectName='chk009', setToolTip='Assign a new material.')
			tb.add('QRadioButton', setText='New Random Material', setObjectName='chk008', setToolTip='Assign a new random ID material.')
			if state=='setMenu':
				return

		selection = pm.ls(selection=1, flatten=1)
		if not selection:
			return 'Error: No renderable object is selected for assignment.'

		if tb.chk007.isChecked(): #Assign current mat
			self.assignMaterial(selection, self.currentMaterial)

		elif tb.chk008.isChecked(): #Assign New random mat ID
			mat = self.createRandomMaterial(prefix='ID_')
			self.assignMaterial(selection, mat)

			#delete previous shader
			# if self.randomMat:
			# 	pm.delete(self.randomMat)

			self.randomMat = mat

			if self.parentUi.tb001.chk001.isChecked():
				self.cmb002() #refresh the combobox
			else:
				self.parentUi.tb001.chk001.setChecked(True) #set combobox to ID map mode. toggling the checkbox refreshes the combobox.
			self.parentUi.cmb002.setCurrentItem(mat.name()) #set the combobox index to the new mat #self.cmb002.setCurrentIndex(self.cmb002.findText(name))

		elif tb.chk009.isChecked(): #Assign New Material
			mel.eval('buildObjectMenuItemsNow "MainPane|viewPanes|modelPanel4|modelPanel4|modelPanel4|modelPanel4ObjectPop";')
			mel.eval('createAssignNewMaterialTreeLister "";')


	@Slots.message
	def lbl000(self):
		'''
		Open material in editor
		'''
		if self.parentUi.tb001.chk001.isChecked(): #ID map mode
			try:
				mat = self.materials[self.parentUi.cmb002.currentText()] #get object from string key
			except:
				return '# Error: No stored material or no valid object selected.'
		else: #Stored material mode
			if not self.currentMaterial: #get material from selected scene object
				if pm.ls(sl=1, objectsOnly=1):
					pm.hyperShade('', shaderNetworksSelectMaterialNodes=1) #selects the material node. doesnt return anything. optional first argument=obj with material.
					self.currentMaterial = pm.ls(selection=1, materials=1)[0]
				else:
					return '# Error: No stored material or no valid object selected.'
			mat = self.currentMaterial

		#open the hypershade editor
		mel.eval("HypershadeWindow;")


	def lbl001(self, setEditable=True):
		'''
		Rename Material: Set cmb002 as editable and disable widgets.
		'''
		if setEditable:
			self.parentUi.cmb002.setEditable(True)
			# self.parentUi.cmb002.lineEdit().returnPressed.connect(self.renameMaterial)
			self.toggleWidgets(self.parentUi, setDisabled='b002,lbl000,tb000,tb002')
		else:
			self.parentUi.cmb002.setEditable(False)
			self.toggleWidgets(self.parentUi, setEnabled='b002,lbl000,tb000,tb002')


	def lbl002(self):
		'''
		Delete Material
		'''
		mat = self.currentMaterial
		mat = pm.delete(mat)

		index = self.parentUi.cmb002.currentIndex()
		self.parentUi.cmb002.setItemText(index, 'None') #self.parentUi.cmb002.removeItem(index)


	def lbl003(self):
		'''
		Delete Unused Materials
		'''
		mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
		self.cmb002() #refresh the combobox


	def lbl004(self):
		'''
		Material Attributes: Show Material Attributes in the Attribute Editor.
		'''
		if self.currentMaterial and hasattr(self.currentMaterial, 'name'):
			mel.eval('showSG '+self.currentMaterial.name())


	@Slots.message
	def b002(self):
		'''
		Store Material

		'''
		selection = pm.ls(selection=1)
		if not selection:
			return 'Error: Nothing selected.'

		mat = self.getMaterial()

		self.parentUi.tb001.chk000.setChecked(True) #set the combobox to show all scene materials
		cmb = self.parentUi.cmb002
		self.cmb002() #refresh the combobox
		cmb.setCurrentIndex(cmb.items().index(mat.name()))


	def renameMaterial(self):
		'''
		Rename Material
		'''
		cmb = self.parentUi.cmb002 #scene materials
		newMatName = cmb.currentText()

		if self.currentMaterial and self.currentMaterial.name!=newMatName:
			if self.parentUi.tb001.chk001.isChecked(): #Rename ID map Material
				prefix = 'ID_'
				if not newMatName.startswith(prefix):
					newMatName = prefix+newMatName

			cmb.setItemText(cmb.currentIndex(), newMatName)
			try:
				pm.rename(self.currentMaterial.name(), newMatName)
			except RuntimeError as error:
				cmb.setItemText(cmb.currentIndex(), str(error.strip('\n')))


	@Slots.message
	def selectByMaterialID(self, material, objects=None, shell=False, invert=False):
		'''
		Select By Material Id
	
		material (obj) = The material to search and select for.
		objects (list) = Faces or mesh objects as a list. If no objects are given, all geometry in the scene will be searched.
		shell (bool) = Select the entire shell.
		invert (bool) = Invert the final selection.R

		#ex call:
		selectByMaterialID(material)
		'''
		if pm.nodeType(material)=='VRayMultiSubTex': #if not a multimaterial
			return 'Error: If material is a multimaterial, select a submaterial.'
		else:
			mat = material

		# if not objects: #if not selection; use all scene geometry
		# 	shapes = pm.ls(type="mesh")
		# 	objects = pm.listRelatives(shapes, parent=True) #transforms

		pm.select(mat)
		pm.hyperShade(objects='') #select all with material. "" defaults to currently selected materials.

		faces = pm.filterExpand(selectionMask=34, expand=1)
		transforms = pm.listRelatives(faces, p=True) #[node.replace('Shape','') for node in pm.ls(sl=1, objectsOnly=1, visible=1)] #get transform node name from shape node

		if shell or invert: #deselect so that the selection can be modified.
			pm.select(faces, deselect=1)

		if shell:
			for shell in transforms:
				pm.select(shell, add=1)
		
		if invert:
			for shell in transforms:
				allFaces = [shell+".f["+str(num)+"]" for num in range(pm.polyEvaluate (shell, face=1))] #create a list of all faces per shell
				pm.select(list(set(allFaces)-set(faces)), add=1) #get inverse of previously selected faces from allFaces


	@staticmethod
	def getSceneMaterials(startingWith=[''], exclude=['standardSurface']):
		'''
		Get All Materials from the current scene.

		args:
			startingWith (list) = Filters material names starting with any of the strings in the given list. ie. ['ID_']
			exclude (list) = Node types to exclude.
		returns:
			(list) materials.
		'''
		materials = [m for m in pm.ls(mat=1, flatten=1) if filter(str(m.name()).startswith, startingWith) and not pm.nodeType(m) in exclude]

		return materials


	@staticmethod
	def getFavoriteMaterials():
		'''
		Get Maya Favorite Materials List.

		returns:
			(list) materials.
		'''
		import maya.app.general.tlfavorites as _fav
		path = os.path.expandvars(r"%USERPROFILE%/Documents/maya/2020/prefs/renderNodeTypeFavorites")
		renderNodeTypeFavorites = _fav.readFavorites(path)
		materials = [i for i in renderNodeTypeFavorites if '/' not in i]
		del _fav
		return materials


	@staticmethod
	def getMaterial():
		'''
		Get the material from the selected face.

		returns:
			(list) material
		'''
		pm.hyperShade("", shaderNetworksSelectMaterialNodes=1) #selects the material node 
		mats = pm.ls(selection=1, materials=1) #now add the selected node to a variable

		return mats[0]


	@staticmethod
	def createRandomMaterial(name=None, prefix=''):
		'''
		Creates a random material.

		args:
			name (str) = material name.
			prefix (str) = name prefix.
		returns:
			(obj) material
		'''
		import random
		rgb = [random.randint(0, 255) for _ in range(3)] #generate a list containing 3 values between 0-255

		if name is None: #create name from rgb values
			name = '_'.join([str(rgb[0]), str(rgb[1]), str(rgb[2])])
		name = prefix+name

		#create shader
		mat = pm.shadingNode('lambert', asShader=1, name=name)
		#convert RGB to 0-1 values and assign to shader
		convertedRGB = [round(float(v)/255, 3) for v in rgb]
		pm.setAttr(name+'.color', convertedRGB)
		#assign to selected geometry
		# pm.select(selection) #initial selection is lost upon node creation
		# pm.hyperShade(assign=mat)

		return mat


	@Slots.message
	def assignMaterial(self, objects, mat):
		'''
		Assign Material

		objects (list) = Faces or mesh objects as a list.
		material (obj) = The material to search and select for.
		'''
		if not mat:
			return 'Error: Material Not Assigned. No material given.'

		try: #if the mat is a not a known type; try and create the material.
			pm.nodeType(mat)
		except:
			mat = pm.shadingNode(mat, asShader=1)

		pm.undoInfo(openChunk=1)
		for obj in objects:
			pm.select(obj) #hyperShade works more reliably with an explicit selection.
			pm.hyperShade(obj, assign=mat)
		pm.undoInfo(closeChunk=1)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

#depricated

# elif storedMaterial:
# 	mat = self.currentMaterial
# 	if not mat:
# 		cmb.addItems_(['Stored Material: None'])
# 		return

# 	matName = mat.name()

# 	if pm.nodeType(mat)=='VRayMultiSubTex':
# 		subMaterials = pm.hyperShade(mat, listUpstreamShaderNodes=1) #get any connected submaterials
# 		subMatNames = [s.name() for s in subMaterials if s is not None]
# 	else:
# 		subMatNames=[]

# 	contents = cmb.addItems_(subMatNames, matName)

# 	if index is None:
# 		index = cmb.currentIndex()
# 	if index!=0:
# 		self.currentMaterial = subMaterials[index-1]
# 	else:
# 		self.currentMaterial = mat

# def cmb000(self, index=None):
	# 	'''
	# 	Existing Materials

	# 	'''
	# 	cmb = self.parentUi.cmb000

	# 	mats = [m for m in pm.ls(materials=1)]
	# 	matNames = [m.name() for m in mats]

	# 	contents = cmb.addItems_(matNames, "Scene Materials")

	# 	if index is None:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		print contents[index]
			
	# 		self.currentMaterial = mats[index-1] #store material
	# 		self.cmb002() #refresh combobox

	# 		cmb.setCurrentIndex(0)


	



#assign random
	# mel.eval('''
# 		string $selection[] = `ls -selection`;

# 		int $d = 2; //decimal places to round to
# 		$r = rand (0,1);
# 		$r = trunc($r*`pow 10 $d`+0.5)/`pow 10 $d`;
# 		$g = rand (0,1);
# 		$g = trunc($g*`pow 10 $d`+0.5)/`pow 10 $d`;
# 		$b = rand (0,1);
# 		$b = trunc($b*`pow 10 $d`+0.5)/`pow 10 $d`;

# 		string $rgb = ("_"+$r+"_"+$g+"_"+$b);
# 		$rgb = substituteAllString($rgb, "0.", "");

# 		$name = ("ID_"+$rgb);

# 		string $ID_ = `shadingNode -asShader lambert -name $name`;
# 		setAttr ($name + ".colorR") $r;
# 		setAttr ($name + ".colorG") $g;
# 		setAttr ($name + ".colorB") $b;

# 		for ($object in $selection)
# 			{
# 			select $object;
# 			hyperShade -assign $ID_;
# 			}
# 		 ''')

#re-assign random
	# mel.eval('''
		# string $objList[] = `ls -selection -flatten`;
		# $material = `hyperShade -shaderNetworksSelectMaterialNodes ""`;
		# string $matList[] = `ls -selection -flatten`;

		# hyperShade -objects $material;
		# string $selection[] = `ls -selection`;
		# //delete the old material and shader group nodes
		# for($i=0; $i<size($matList); $i++)
		# 	{
		# 	string $matSGplug[] = `connectionInfo -dfs ($matList[$i] + ".outColor")`;
		# 	$SGList[$i] = `match "^[^\.]*" $matSGplug[0]`;
		# 	print $matList; print $SGList;
		# 	delete $matList[$i];
		# 	delete $SGList[$i];
		# 	}
		# //create new random material
		# int $d = 2; //decimal places to round to
		# $r = rand (0,1);
		# $r = trunc($r*`pow 10 $d`+0.5)/`pow 10 $d`;
		# $g = rand (0,1);
		# $g = trunc($g*`pow 10 $d`+0.5)/`pow 10 $d`;
		# $b = rand (0,1);
		# $b = trunc($b*`pow 10 $d`+0.5)/`pow 10 $d`;

		# string $rgb = ("_"+$r+"_"+$g+"_"+$b+"");
		# $rgb = substituteAllString($rgb, "0.", "");

		# $name = ("ID_"+$rgb);

		# string $ID_ = `shadingNode -asShader lambert -name $name`;
		# setAttr ($name + ".colorR") $r;
		# setAttr ($name + ".colorG") $g;
		# setAttr ($name + ".colorB") $b;

		# for ($object in $selection)
		# 	{
		# 	select $object;
		# 	hyperShade -assign $ID_;
		# 	}
		# ''')