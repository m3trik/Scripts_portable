from __future__ import print_function
from tk_slots_max_init import *

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
			pin.add(QComboBox_, setObjectName='cmb001', setToolTip='3dsMax Material Editors')
			return


	def chk007(self):
		'''
		'''
		self.parentUi.tb002.setText('Assign Current')


	def chk008(self):
		'''
		'''
		self.parentUi.tb002.setText('Assign Random')


	def cmb001(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb001

		if index=='setMenu':
			list_ = ['Material Editor']
			cmb.addItems_(list_, '3dsMax Material Editors')
			return

		if index>0:
			if index==cmd.items.index('Material Editor'):
				maxEval('max mtledit')
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
		except: #if the toolbox hasn't been built yet: default to sceneMaterials
			sceneMaterials = True

		if sceneMaterials:
			materials = self.getSceneMaterials()

		elif idMapMaterials:
			materials = self.getSceneMaterials(startingWith=['ID_'])

		mats = sorted([mat for mat in set(materials)])
		matNames = [mat.name for mat in mats]
		contents = cmb.addItems_(matNames, clear=True)

		#create and set icons with color swatch
		for i in range(len(mats)): #create icons with color swatch
			try:
				r = int(mats[i].diffuse.r) #convert from float value
				g = int(mats[i].diffuse.g)
				b = int(mats[i].diffuse.b)
				pixmap = QtGui.QPixmap(100,100)
				pixmap.fill(QtGui.QColor.fromRgb(r, g, b))
				cmb.setItemIcon(i, QtGui.QIcon(pixmap))
			except AttributeError:
				pass

		if index is None:
			index = cmb.currentIndex()
		# else:
		# 	cmb.setCurrentIndex(index):

		self.materials = {name:mats[i] for i, name in enumerate(matNames)} #add mat objects to materials dictionary. 'mat name'=key, <mat object>=value


	@Slots.message
	def tb000(self, state=None):
		'''
		Select By: Material Id
		'''
		tb = self.currentUi.tb000
		if not tb.containsMenuItems:
			tb.add('QRadioButton', setText='Shell', setObjectName='chk005', setToolTip='Select entire shell.')
			tb.add('QRadioButton', setText='Invert', setObjectName='chk006', setToolTip='Invert Selection.')
			if state=='setMenu':
				return

		shell = tb.chk005.isChecked() #Select by material: shell
		invert = tb.chk006.isChecked() #Select by material: invert

		if not self.currentMaterial:
			return 'Error: No Material Selection.'

		self.selectByMaterialID(self.currentMaterial, rt.selection)


	def tb001(self, state=None):
		'''
		Stored Material Options
		'''
		tb = self.currentUi.tb001
		if not tb.containsMenuItems:
			tb.add('QRadioButton', setText='All Scene Materials', setObjectName='chk000', setChecked=True, setToolTip='List all scene materials.') #Material mode: Stored Materials
			tb.add('QRadioButton', setText='ID Map Materials', setObjectName='chk001', setToolTip='List ID map materials.') #Material mode: ID Map Materials

			self.connect_([tb.chk000, tb.chk001], 'toggled', [self.cmb002, self.tb001])
			if state=='setMenu':
				return

		if tb.chk000.isChecked():
			self.parentUi.group000.setTitle(tb.chk000.text())
		elif tb.chk001.isChecked():
			self.parentUi.group000.setTitle(tb.chk001.text())


	@Slots.message
	def tb002(self, state=None):
		'''
		Assign Material
		'''
		tb = self.currentUi.tb002
		if not tb.containsMenuItems:
			tb.add('QRadioButton', setText='Current Material', setObjectName='chk007', setChecked=True, setToolTip='Re-Assign the current stored material.')
			tb.add('QRadioButton', setText='New Random Material', setObjectName='chk008', setToolTip='Assign a new random ID material.')
			if state=='setMenu':
				return

		selection = rt.selection

		if tb.chk008.isChecked(): #Assign New random mat ID
			if selection:
				mat = self.createRandomMaterial(prefix='ID_')
				self.assignMaterial(selection, mat)

				#delete previous shader
				if self.randomMat:
					self.randomMat = None #replace with standard material

				self.randomMat = mat

				if self.parentUi.tb001.chk001.isChecked():
					self.cmb002() #refresh the combobox
				else:
					self.parentUi.tb001.chk001.setChecked(True) #set combobox to ID map mode. toggling the checkbox refreshes the combobox.
				self.parentUi.cmb002.setCurrentItem(name) #set the combobox index to the new mat #self.cmb002.setCurrentIndex(self.cmb002.findText(name))
			else:
				return 'Error: No valid object/s selected.'

		elif tb.chk007.isChecked(): #Assign current mat
			self.assignMaterial(selection, self.currentMaterial)

		rt.redrawViews()


	@Slots.message
	def lbl000(self):
		'''
		Open material in editor
		'''
		if self.parentUi.tb001.chk001.isChecked(): #ID map mode
			try:
				mat = self.materials[self.parentUi.cmb002.currentText()] #get object from string key
			except:
				return 'Error: No stored material or no valid object selected.'
		else: #Stored material mode
			if not self.currentMaterial: #get material from selected scene object
				if rt.selection:
					self.currentMaterial = rt.selection[0].material
				else:
					return 'Error: No stored material or no valid object selected.'
			mat = self.currentMaterial

		#open the slate material editor
		if not rt.SME.isOpen():
			rt.SME.open()

		#create a temp view in the material editor
		if rt.SME.GetViewByName('temp'):
			rt.SME.DeleteView(rt.SME.GetViewByName('temp'), False)
		index = rt.SME.CreateView('temp')
		view = rt.SME.GetView(index)

		#show node and corresponding parameter rollout
		node = view.CreateNode(mat, rt.point2(0, 0))
		rt.SME.SetMtlInParamEditor(mat)

		rt.redrawViews()


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
				self.currentMaterial.name = newMatName
			except RuntimeError as error:
				cmb.setItemText(cmb.currentIndex(), str(error.strip('\n')))


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
		mat = rt.Standard(name="Default Material") #replace with standard material

		index = self.parentUi.cmb002.currentIndex()
		self.parentUi.cmb002.setItemText(index, mat.name) #self.parentUi.cmb002.removeItem(index)


	def lbl003(self):
		'''
		Delete Unused Materials
		'''
		defaultMaterial = rt.Standard(name='Default Material')
		
		for mat in rt.sceneMaterials:
			nodes = rt.refs().dependentnodes(mat) 
			if nodes.count==0:
				rt.replaceinstances(mat, defaultMaterial)
				
			rt.gc()
			rt.freeSceneBitmaps()


	@Slots.message
	def b002(self):
		'''
		Set Material: Set the Currently Selected Material as the currentMaterial.
		'''
		try: 
			obj = rt.selection[0]
		except IndexError:
			return 'Error: Nothing selected.'

		mat = self.getMaterial(obj)

		self.parentUi.tb001.chk000.setChecked(True) #set the combobox to show all scene materials
		cmb = self.parentUi.cmb002
		self.cmb002() #refresh the combobox
		cmb.setCurrentIndex(cmb.items().index(mat.name))


	@Slots.message
	def selectByMaterialID(self, material, objects=None, shell=False, invert=False):
		'''
		Select By Material Id
	
		material (obj) = The material to search and select for.
		objects (list) = Faces or mesh objects as a list. If no objects are given, all geometry in the scene will be searched.
		shell (bool) = Select the entire shell.
		invert (bool) = Invert the final selection.

		#ex call:
		selectByMaterialID(material)
		'''
		if not rt.getNumSubMtls(material): #if not a multimaterial
			mat = material
		else:
			return 'Error: No valid stored material. If material is a multimaterial, select a submaterial.'

		if not objects: #if not selection; use all scene geometry
			objects = rt.geometry

		for obj in objects:
			if not any([rt.isKindOf(obj, rt.Editable_Poly), rt.isKindOf(obj, rt.Editable_mesh)]):
				print('Error: '+str(obj.name)+' skipped. Operation requires an Editable_Poly or Editable_mesh.')
			else:
				if shell: #set to base object level
					rt.modPanel.setCurrentObject(obj.baseObject)
				else: #set object level to face
					Init.setSubObjectLevel(4)
				m = obj.material
				multimaterial = rt.getNumSubMtls(m)

				same=[] #list of faces with the same material
				other=[] #list of all other faces

				faces = list(range(1, obj.faces.count))
				for f in faces:
					if multimaterial:
						try: #get material from face
							index = rt.GetFaceId_(obj, f) #Returns the material ID of the specified face.
						except RuntimeError: #try procedure for polygon object
							index = rt.polyop.GetFaceId_(obj, f) #Returns the material ID of the specified face.
						m = obj.material[index-1] #m = rt.getSubMtl(m, id) #get the material using the ID_ index (account for maxscript arrays starting at index 1)

					if m==mat: #single material
						if shell: #append obj to same and break loop
							same.append(obj)
							break
						else: #append face ID to same
							same.append(f)
					else:
						if shell: #append obj to other and break loop
							other.append(obj)
							break
						else: #append face ID to other
							other.append(f)

				if shell:
					if invert:
						(rt.select(i) for i in other)
					else:
						(rt.select(i) for i in same)
				else:
					if invert:
						try:
							rt.setFaceSelection(obj, other) #select inverse of the faces for editable mesh.
						except RuntimeError:
							rt.polyop.setFaceSelection(obj, other) #select inverse of the faces for polygon object.
					else:
						try:
							rt.setFaceSelection(obj, same) #select the faces for editable mesh.
						except RuntimeError:
							rt.polyop.setFaceSelection(obj, same) #select the faces for polygon object.
				# print same
				# print other


	@staticmethod
	def getSceneMaterials(startingWith=['']):
		'''
		Get All Materials from the current scene.

		args:
			startingWith (list) = Filters material names starting with any of the strings in the given list. ie. ['ID_']
		returns:
			(list) materials.
		'''
		materials=[] #get any scene material that does not start with 'Material'
		for mat in rt.sceneMaterials:
			if rt.getNumSubMtls(mat): #if material is a submaterial; search submaterials
				for i in range(1, rt.getNumSubMtls(mat)+1):
					subMat = rt.getSubMtl(mat, i)
					if subMat and filter(subMat.name.startswith, startingWith):
						materials.append(subMat)
			elif filter(mat.name.startswith, startingWith):
				materials.append(mat)

		return materials


	@Slots.message
	def getMaterial(self, obj, face=None):
		'''
		Get the material from the given object or face components.

		args:
			obj (obj) = Mesh object.
			face (int) = Face number.
		returns:
			(obj) material
		'''
		mat = obj.material #get material from selection

		if rt.subObjectLevel==4: #if face selection check for multimaterial
			if rt.getNumSubMtls(mat): #if multimaterial; use selected face to get material ID
				if face is None:
					face = rt.bitArrayToArray(rt.getFaceSelection(obj))[0] #get selected face

				if rt.classOf(obj)==rt.Editable_Poly:
					ID_ = rt.polyop.GetFaceId_(obj, face) #Returns the material ID of the specified face.
				else:
					try:
						ID_ = rt.GetFaceId_(obj, face) #Returns the material ID of the specified face.
					except RuntimeError:
						return 'Error: Object must be of type Editable_Poly or Editable_mesh.'

				mat = rt.getSubMtl(mat, ID_) #get material from mat ID

		return mat


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
			name = '_'.join([prefix, str(rgb[0]), str(rgb[1]), str(rgb[2])])
		name = prefix+name
		
		#create shader
		mat = rt.StandardMaterial()
 		mat.name = name
		mat.diffuse = rt.color(rgb[0], rgb[1], rgb[2])

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

		for obj in objects:
			if rt.getNumSubMtls(mat): #if multimaterial
				mat.materialList.count = mat.numsubs+1 #add slot to multimaterial
				mat.materialList[-1] = material #assign new material to slot
			else:
				obj.material = mat

		rt.redrawViews()








#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------


# deprecated