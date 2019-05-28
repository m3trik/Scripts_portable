import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Texturing(Init):
	def __init__(self, *args, **kwargs):
		super(Texturing, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('texturing')
		
		self.ui.t000.hide()
		self.ui.t001.hide()
		
		self.ui.cmb001.removeEventFilter(self.signal)
		self.ui.cmb002.removeEventFilter(self.signal)

		self.storedMaterial=None
		self.storedID_mats=None
		self.randomMat=None



	def t000(self):
		'''
		Rename Stored Material textfield
		'''
		self.ui.b008.setChecked(False)
		self.b008()


	def t001(self):
		'''
		Rename ID Material textfield
		'''
		self.ui.b009.setChecked(False)
		self.b009()


	def cmb000(self):
		'''
		Existing Materials

		'''
		cmb = self.ui.cmb000
		
		materials = [mat for mat in rt.sceneMaterials if 'Multimaterial' not in mat.name and 'BlendMtl' not in mat.name and not mat.name.startswith('Material')]
		materialNames = sorted([mat.name for mat in materials])
		
		contents = self.comboBox(cmb, materialNames, 'Scene Materials:')

		index = cmb.currentIndex()
		if index!=0:
			mat = [m for m in materials if m.name==contents[index]][0]

			self.storedMaterial = mat #store material
			self.cmb002() #refresh combobox

			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		Editors

		'''
		cmb = self.ui.cmb001
		
		files = ['Material Editor']
		contents = self.comboBox(cmb, files, 'Editors')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Material Editor'):
				maxEval('max mtledit')
			cmb.setCurrentIndex(0)


	def cmb002(self):
		'''
		Stored Material
		'''
		cmb = self.ui.cmb002
		
		mat = self.storedMaterial
		if not mat:
			return

		matName = mat.name
		
		subMaterials = [rt.getSubMtl(mat, id) for id in range(1, rt.getNumSubMtls(mat)+1)] #get the material using the matID index. modify index range for index starting at 1.
		subMatNames = [s.name for s in subMaterials if s is not None]
		
		contents = self.comboBox(cmb, subMatNames, matName)

		index = cmb.currentIndex()
		if index!=0:
			self.storedMaterial = subMaterials[index-1]
		else:
			self.storedMaterial = mat


	def cmb003(self):
		'''
		Stored ID map
		'''
		cmb = self.ui.cmb003

		matID_mats = [m for m in rt.sceneMaterials if m.name.startswith('matID')]
		matID_names = [m.name for m in matID_mats]
		if not matID_names: 
			matID_names = ['ID Map: None']

		contents = self.comboBox(cmb, matID_names)

		if matID_names[0]!='ID Map: None': #add mat objects to storedID_mats dict. 'mat name'=key, <mat object>=value
			self.storedID_mats = {n:matID_mats[i] for i, n in enumerate(matID_names)}


	def chk000(self):
		self.ui.chk001.setChecked(False)


	def chk001(self):
		self.ui.chk000.setChecked(False)


	def b000(self):
		'''
		Select By Material Id

		'''
		shell = self.ui.chk000.isChecked() 
		invert = self.ui.chk001.isChecked()

		if not rt.getNumSubMtls(self.storedMaterial): #if not a multimaterial
			mat = self.storedMaterial
		else:
			return '# Error: No valid stored material. If material is a multimaterial, select a submaterial. #'

		sel = rt.selection
		if not sel: #if not selection; use all scene geometry
			sel = rt.geometry

		for obj in sel:
			if shell: #set to base object level
				rt.modPanel.setCurrentObject(obj.baseObject)
			else: #set object level to face
				self.setSubObjectLevel(4)
			m = obj.material
			multimaterial = rt.getNumSubMtls(m)

			same=[] #list of faces with the same material
			other=[] #list of all other faces

			faces = list(range(1, obj.faces.count))
			for f in faces:
				if multimaterial:
					id = obj.GetFaceMaterial(f) #Returns the material ID of the specified face.
					m = rt.getSubMtl(m, id) #get the material using the matID index

				if m==mat:
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
					rt.polyop.setFaceSelection(obj, other) #select the faces
				else:
					rt.polyop.setFaceSelection(obj, same) #select the faces
			# print same
			# print other


	def b001(self):
		'''
		Delete Material

		'''
		self.storedMaterial = rt.Standard(name="Default Material") #replace with standard material
		self.storedMaterial = None

		self.comboBox(self.ui.cmb002, [], 'Stored Material: None') #init combobox


	def b002(self):
		'''
		Store Material

		'''
		obj = rt.selection[0]
		mat = obj.material #get material from selection

		if obj:
			if rt.subObjectLevel == 4: #if face selection check for multimaterial
				if rt.getNumSubMtls(mat): #if multimaterial; use selected face to get material ID
					f = rt.bitArrayToArray(rt.getFaceSelection(obj))[0] #get selected faces
					id_ = obj.GetFaceMaterial(f) #Returns the material ID of the specified face.
					mat = rt.getSubMtl(mat, id_) #get material from mat ID

			self.storedMaterial = mat #store material
			self.cmb002() #refresh combobox
		else:
			print '# Error: Nothing selected. #'


	def b003(self):
		'''
		Assign Material

		'''
		for obj in rt.selection:
			obj.material = self.storedMaterial #assign material per object in selection
		rt.redrawViews()


	def b004(self):
		'''
		Assign New random mat ID

		'''
		import random

		selection = rt.selection

		if selection:
			prefix = 'matID'
			rgb = [random.randint(0, 255) for _ in range(3)] #generate a list containing 3 values between 0-255

			#format name
			name = '_'.join([prefix, str(rgb[0]), str(rgb[1]), str(rgb[2])])
			#create shader
			mat = rt.StandardMaterial()
	 		mat.name = name
			mat.diffuse = rt.color(rgb[0], rgb[1], rgb[2])

			for obj in selection:
				obj.material = mat

			#delete previous shader
			if self.randomMat:
				self.randomMat = None #replace with standard material

			self.randomMat = mat

			rt.redrawViews()
		else:
			print '# Error: No valid object/s selected. #'


	def b005(self):
		'''
		Assign Existing mat ID

		'''
		name = self.ui.cmb003.currentText()
		mat = self.storedID_mats[name]
		
		for obj in rt.selection:
				obj.material = mat

		rt.redrawViews()


	def b006(self):
		'''
		Delete Unused Materials

		'''
		defaultMat = rt.Standard(name='Default Material')
		count = 0
		for mat in rt.scenematerials
			rt.undo(False)
			nodes = refs.dependentnodes mat 
			if nodes.count == 0 do 
				replaceinstances mat def_material
				count += 1
				
			rt.gc()
			rt.freeSceneBitmaps()
			count
			''')


	def b007(self):
		'''
		Open material in editor

		'''
		if not self.storedMaterial: #get material from selected scene object
			if rt.selection:
				self.storedMaterial = rt.selection[0].material
			else:
				return '# Error: No stored material and no valid object selected. #'
		mat = self.storedMaterial

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


	def b008(self):
		'''
		Rename Stored Material

		'''
		if self.ui.b008.isChecked():
			self.ui.t000.setText(self.ui.cmb002.currentText())
			if self.ui.t000.text()=='Stored Material: None':
				self.ui.b008.setChecked(False)
			else:
				self.ui.t000.show()
		else:
			if self.storedMaterial:
				self.storedMaterial.name = self.ui.t000.text()

			self.cmb002() #refresh combobox
			self.ui.t000.hide()


	def b009(self):
		'''
		Rename ID map Material

		'''
		if self.ui.b009.isChecked():
			self.ui.t001.setText(self.ui.cmb003.currentText())
			if self.ui.t001.text()=='ID Map: None':
				self.ui.b009.setChecked(False)
			else:
				self.ui.t001.show()
		else:
			prefix='matID_'
			newName=self.ui.t001.text()

			matName = self.ui.cmb003.currentText()
			mat = self.storedID_mats[matName]
			if not newName.startswith(prefix):
				mat.name = prefix+newName
			else:
				mat.name = newName

			self.cmb002() #refresh combobox
			self.ui.t001.hide()


	def b010(self):
		'''
		

		'''
		pass






		


#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------