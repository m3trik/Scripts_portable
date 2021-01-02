from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Materials(Init):
	def __init__(self, *args, **kwargs):
		super(Materials, self).__init__(*args, **kwargs)

		self.currentMats=None
		self.randomMat=None

		self.materials_submenu.b003.setVisible(False)


	@property
	def currentMat(self):
		'''Get the current material using the current index of the materials combobox.
		'''
		text = self.materials.cmb002.currentText()
		return self.currentMats[text] if text else None


	def d000(self, state=None):
		'''Context menu
		'''
		d000 = self.materials.d000

		if state is 'setMenu':
			d000.contextMenu.add(widgets.TkComboBox, setObjectName='cmb001', setToolTip='3dsMax Material Editors')
			return


	def chk007(self, state=None):
		'''Assign Material: Current
		'''
		self.materials.tb002.setText('Assign Current')


	def chk008(self, state=None):
		'''Assign Material: Random
		'''
		self.materials.tb002.setText('Assign Random')


	def chk009(self, state=None):
		'''Assign Material: New
		'''
		self.materials.tb002.setText('Assign New')


	def cmb001(self, index=None):
		'''Editors
		'''
		cmb = self.materials.cmb001
		if index is 'setMenu':
			list_ = ['Material Editor']
			cmb.addItems_(list_, '3dsMax Material Editors')
			return

		if index>0:
			if index==cmd.items.index('Material Editor'):
				maxEval('max mtledit')
			cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''Material list

		:Parameters:
			index (int) = parameter on activated, currentIndexChanged, and highlighted signals.
		'''
		cmb = self.materials.cmb002
		tb = self.materials.tb001
		b = self.materials_submenu.b003

		if index is 'setMenu':
			cmb.contextMenu.add(widgets.TkLabel, setText='Open in Editor', setObjectName='lbl000', setToolTip='Open material in editor.')
			cmb.contextMenu.add(widgets.TkLabel, setText='Rename', setObjectName='lbl001', setToolTip='Rename the current material.')
			cmb.contextMenu.add(widgets.TkLabel, setText='Delete', setObjectName='lbl002', setToolTip='Delete the current material.')
			cmb.contextMenu.add(widgets.TkLabel, setText='Delete All Unused Materials', setObjectName='lbl003', setToolTip='Delete All unused materials.')
			cmb.beforePopupShown.connect(self.cmb002) #refresh comboBox contents before showing it's popup.
			cmb.returnPressed.connect(lambda: self.lbl001(setEditable=False))
			return
 
		try:
			sceneMaterials = tb.menu_.chk000.isChecked()
			idMapMaterials = tb.menu_.chk001.isChecked()
		except: #if the toolbox hasn't been built yet: default to sceneMaterials
			sceneMaterials = True

		if sceneMaterials:
			materials = self.getSceneMaterials()

		elif idMapMaterials:
			materials = self.getSceneMaterials(startingWith=['ID_'])


		self.currentMats = {mat.name:mat for mat in sorted(list(set(materials))) if hasattr(mat,'name')}
		cmb.addItems_(self.currentMats.keys(), clear=True)

		#create and set icons with color swatch
		for i, mat in enumerate(self.currentMats.keys()):
			icon = Materials.getColorSwatchIcon(mat)
			cmb.setItemIcon(i, icon) if icon else None

		#set submenu assign material button attributes
		b.setText('Assign '+cmb.currentText())
		icon = Materials.getColorSwatchIcon(cmb.currentText(), [15, 15])
		b.setIcon(icon) if icon else None
		b.setMinimumWidth(b.minimumSizeHint().width()+25)
		b.setVisible(True if cmb.currentText() else False)


	@staticmethod
	def getColorSwatchIcon(mat, size=[20, 20]):
		'''Get an icon with a color fill matching the given materials RBG value.

		:Parameters:
			mat (obj)(str) = The material or the material's name.
			size (list) = Desired icon size. [width, height]

		:Return:
			(obj) pixmap icon.
		'''
		try:
			mat = next(m for m in Materials.getSceneMaterials() if m.name==mat) if isinstance(mat, (str, unicode)) else mat #get the mat object if a string name is given.
			r = int(mat.diffuse.r) #convert from float value
			g = int(mat.diffuse.g)
			b = int(mat.diffuse.b)
			pixmap = QtGui.QPixmap(size[0],size[1])
			pixmap.fill(QtGui.QColor.fromRgb(r, g, b))

			return QtGui.QIcon(pixmap)

		except (StopIteration, AttributeError):
			pass


	@Slots.message
	def tb000(self, state=None):
		'''Select By Material Id
		'''
		tb = self.ui.tb000
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Current Material', setObjectName='chk010', setChecked=True, setToolTip='Use the current material, <br>else use the current viewport selection to get a material.')
			tb.menu_.add('QCheckBox', setText='All Objects', setObjectName='chk003', setToolTip='Search all scene objects, or only those currently selected.')
			tb.menu_.add('QCheckBox', setText='Shell', setObjectName='chk005', setToolTip='Select entire shell.')
			tb.menu_.add('QCheckBox', setText='Invert', setObjectName='chk006', setToolTip='Invert Selection.')
			return

		if not self.currentMat:
			return 'Error: No Material Selection.'

		shell = tb.menu_.chk005.isChecked() #Select by material: shell
		invert = tb.menu_.chk006.isChecked() #Select by material: invert
		allObjects = tb.menu_.chk003.isChecked() #Search all scene objects
		currentMaterial = tb.menu_.chk010.isChecked() #Use the current material instead of the material of the current viewport selection.

		objects = rt.selection if not allObjects else None
		material = self.currentMat if currentMaterial else None

		self.selectByMaterialID(self.currentMat, objects, shell=shell, invert=invert)


	def tb001(self, state=None):
		'''Stored Material Options
		'''
		tb = self.materials.tb001
		if state is 'setMenu':
			tb.menu_.add('QRadioButton', setText='All Scene Materials', setObjectName='chk000', setChecked=True, setToolTip='List all scene materials.') #Material mode: Stored Materials
			tb.menu_.add('QRadioButton', setText='ID Map Materials', setObjectName='chk001', setToolTip='List ID map materials.') #Material mode: ID Map Materials

			self.connect_([tb.menu_.chk000, tb.menu_.chk001], 'toggled', [self.cmb002, self.tb001])
			return

		if tb.menu_.chk000.isChecked():
			self.materials.group000.setTitle(tb.menu_.chk000.text())
		elif tb.menu_.chk001.isChecked():
			self.materials.group000.setTitle(tb.menu_.chk001.text())


	@Slots.message
	def tb002(self, state=None):
		'''Assign Material
		'''
		tb = self.materials.tb002
		if state is 'setMenu':
			tb.menu_.add('QRadioButton', setText='Current Material', setObjectName='chk007', setChecked=True, setToolTip='Re-Assign the current stored material.')
			tb.menu_.add('QRadioButton', setText='New Material', setObjectName='chk009', setToolTip='Assign a new material.')
			tb.menu_.add('QRadioButton', setText='New Random Material', setObjectName='chk008', setToolTip='Assign a new random ID material.')
			return

		selection = rt.selection

		assignCurrent = tb.menu_.chk007.isChecked()
		assignRandom = tb.menu_.chk008.isChecked()
		assignNew = tb.menu_.chk009.isChecked()

		if assignRandom: #Assign New random mat ID
			if selection:
				mat = self.createRandomMaterial(prefix='ID_')
				self.assignMaterial(selection, mat)

				#delete previous shader
				if self.randomMat:
					self.randomMat = None #replace with standard material

				self.randomMat = mat

				if self.materials.tb001.menu_.chk001.isChecked(): #ID map materials mode.
					self.cmb002() #refresh the combobox
				else:
					self.materials.tb001.menu_.chk001.setChecked(True) #set comboBox to ID map mode. toggling the checkbox refreshes the combobox.
				self.materials.cmb002.setCurrentItem(mat.name) #set the comboBox index to the new mat #self.cmb002.setCurrentIndex(self.cmb002.findText(name))
			else:
				return 'Error: No valid object/s selected.'

		elif assignCurrent: #Assign current mat
			self.assignMaterial(selection, self.currentMat)

		elif assignNew: #Assign New Material
			pass

		rt.redrawViews()


	@Slots.message
	def lbl000(self):
		'''Open material in editor
		'''
		if self.materials.tb001.menu_.chk001.isChecked(): #ID map mode
			try:
				mat = self.currentMats[self.materials.cmb002.currentText()] #get object from string key
			except:
				return 'Error: No stored material or no valid object selected.'
		else: #Stored material mode
			if not self.currentMat: #get material from selected scene object
				if rt.selection:
					self.currentMat = rt.selection[0].material
				else:
					return 'Error: No stored material or no valid object selected.'
			mat = self.currentMat

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


	def lbl001(self, setEditable=True):
		'''Rename Material: Set cmb002 as editable and disable widgets.
		'''
		if setEditable:
			self._mat = self.currentMat
			self.materials.cmb002.setEditable(True)
			# self.materials.cmb002.lineEdit().returnPressed.connect(self.renameMaterial)
			self.toggleWidgets(self.materials, setDisabled='b002,lbl000,tb000,tb002')
		else:
			mat = self._mat
			newMatName = cmb.currentText()
			self.renameMaterial(mat, newMatName)
			self.materials.cmb002.setEditable(False)
			self.toggleWidgets(self.materials, setEnabled='b002,lbl000,tb000,tb002')


	def lbl002(self):
		'''Delete Material
		'''
		mat = self.currentMat
		mat = rt.Standard(name="Default Material") #replace with standard material

		index = self.materials.cmb002.currentIndex()
		self.materials.cmb002.setItemText(index, mat.name) #self.materials.cmb002.removeItem(index)


	def lbl003(self):
		'''Delete Unused Materials
		'''
		defaultMaterial = rt.Standard(name='Default Material')
		
		for mat in rt.sceneMaterials:
			nodes = rt.refs().dependentnodes(mat) 
			if nodes.count==0:
				rt.replaceinstances(mat, defaultMaterial)
				
			rt.gc()
			rt.freeSceneBitmaps()


	def b000(self):
		'''Material List: Delete
		'''
		self.lbl002()


	def b001(self):
		'''Material List: Edit
		'''
		self.lbl000()


	@Slots.message
	def b002(self):
		'''Set Material: Set the Currently Selected Material as the currentMaterial.
		'''
		try: 
			obj = rt.selection[0]
		except IndexError:
			return 'Error: Nothing selected.'

		mat = self.getMaterial(obj)

		self.materials.tb001.menu_.chk000.setChecked(True) #set the combobox to show all scene materials
		cmb = self.materials.cmb002
		self.cmb002() #refresh the combobox
		cmb.setCurrentIndex(cmb.items.index(mat.name))


	def b003(self):
		'''Assign: Assign Current
		'''
		self.materials.tb002.menu_.chk007.setChecked(True)
		self.materials.tb002.setText('Assign Current')
		self.tb002()


	def b004(self):
		'''Assign: Assign Random
		'''
		self.materials.tb002.menu_.chk008.setChecked(True)
		self.materials.tb002.setText('Assign Random')
		self.tb002()


	def b005(self):
		'''Assign: Assign New
		'''
		self.materials.tb002.menu_.chk009.setChecked(True)
		self.materials.tb002.setText('Assign New')
		self.tb002()


	def renameMaterial(self, mat, newMatName):
		'''Rename Material
		'''
		cmb = self.materials.cmb002 #scene materials

		curMatName = mat.name
		if curMatName!=newMatName:
			cmb.setItemText(cmb.currentIndex(), newMatName)
			try:
				curMatName = newMatName
			except RuntimeError as error:
				cmb.setItemText(cmb.currentIndex(), str(error.strip('\n')))


	@Slots.message
	def selectByMaterialID(self, material=None, objects=None, shell=False, invert=False):
		'''Select By Material Id
	
		material (obj) = The material to search and select for.
		objects (list) = Faces or mesh objects as a list. If no objects are given, all geometry in the scene will be searched.
		shell (bool) = Select the entire shell.
		invert (bool) = Invert the final selection.

		#ex call:
		selectByMaterialID(material)
		'''
		if rt.getNumSubMtls(material): #if not a multimaterial
			return 'Error: No valid stored material. If material is a multimaterial, select a submaterial.'

		if not material:
			material = self.getMaterial()

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

					if m==material: #single material
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
		'''Get All Materials from the current scene.

		:Parameters:
			startingWith (list) = Filters material names starting with any of the strings in the given list. ie. ['ID_']
		:Return:
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
	def getMaterial(self, obj=None, face=None):
		'''Get the material from the given object or face components.

		:Parameters:
			obj (obj) = Mesh object.
			face (int) = Face number.
		:Return:
			(obj) material
		'''
		if not obj:
			selection = rt.selection
			if not selection:
				return 'Error: Nothing selected. Select an object face, or choose the option: current material.'
			obj = selection[0]

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
		'''Creates a random material.

		:Parameters:
			name (str) = material name.
			prefix (str) = Optional string to be appended to the beginning of the name.

		:Return:
			(obj) material
		'''
		import random
		rgb = [random.randint(0, 255) for _ in range(3)] #generate a list containing 3 values between 0-255

		if name is None: #create name from rgb values
			name = '_'.join([prefix, str(rgb[0]), str(rgb[1]), str(rgb[2])])
		
		#create shader
		mat = rt.StandardMaterial()
 		mat.name = name
		mat.diffuse = rt.color(rgb[0], rgb[1], rgb[2])

		return mat


	@Slots.message
	def assignMaterial(self, objects, mat):
		'''Assign Material

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