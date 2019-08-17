import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init

from PySide2 import QtGui




class Materials(Init):
	def __init__(self, *args, **kwargs):
		super(Materials, self).__init__(*args, **kwargs)

		
		self.ui = self.sb.getUi('materials')

		self.ui.progressBar.hide()

		self.ui.t000.hide()
		
		self.ui.cmb001.removeEventFilter(self.signal)
		self.ui.cmb002.removeEventFilter(self.signal)

		self.storedMaterial=None
		self.storedID_mats=None
		self.randomMat=None



	def t000(self):
		'''
		Rename Material textfield
		'''
		self.ui.b008.setChecked(False)
		self.b008()


	def cmb000(self):
		'''
		Existing Materials

		'''
		cmb = self.ui.cmb000

		mats = [m for m in pm.ls(materials=1)]
		matNames = [m.name() for m in mats]

		contents = self.comboBox (cmb, matNames, "Scene Materials")

		index = cmb.currentIndex()
		if index!=0:
			print contents[index]
			
			self.storedMaterial = mats[index-1] #store material
			self.cmb002() #refresh combobox

			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		Editors

		'''
		cmb = self.ui.cmb001
		
		files = ['Hypershade']
		contents = self.comboBox (cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Hypershade'):
				mel.eval('HypershadeWindow;')
			cmb.setCurrentIndex(0)


	def cmb002(self):
		'''
		Stored Material
		'''
		cmb = self.ui.cmb002

		if self.ui.chk002.isChecked(): #ID map mode
			mats = [m for m in pm.ls(mat=1, flatten=1) if m.name().startswith('matID')]
			matNames = [m.name() for m in mats]
			if not matNames: 
				matNames = ['ID Map: None']

			contents = self.comboBox(cmb, matNames)
			
			if matNames[0]!='ID Map: None': #add mat objects to storedID_mats dict. 'mat name'=key, <mat object>=value
				self.storedID_mats = {n:mats[i] for i, n in enumerate(matNames)}

			#create icons with color swatch
			for index in range(len(mats)):
				r = int(pm.getAttr(matNames[index]+'.colorR')*255) #convert from 0-1 to 0-255 value and then to an integer
				g = int(pm.getAttr(matNames[index]+'.colorG')*255)
				b = int(pm.getAttr(matNames[index]+'.colorB')*255)
				pixmap = QtGui.QPixmap(100,100)
				pixmap.fill(QtGui.QColor.fromRgb(r, g, b))
				cmb.setItemIcon(index, QtGui.QIcon(pixmap))

		else: #Stored Material
			mat = self.storedMaterial
			if not mat:
				return

			matName = mat.name()

			if pm.nodeType(mat)=='VRayMultiSubTex':
				subMaterials = pm.hyperShade(mat, listUpstreamShaderNodes=1) #get any connected submaterials
				subMatNames = [s.name() for s in subMaterials if s is not None]
			else:
				subMatNames = []

			contents = self.comboBox(cmb, subMatNames, matName)

			index = cmb.currentIndex()
			if index!=0:
				self.storedMaterial = subMaterials[index-1]
			else:
				self.storedMaterial = mat
		

	def chk000(self): #Select by material: invert
		self.hotBox.ui.chk001.setChecked(False)


	def chk001(self): #Select by material: shell
		self.hotBox.ui.chk000.setChecked(False)


	def chk002(self): #toggle stored material or ID map mode
		self.cmb002()


	def b000(self):
		'''
		Select By Material Id

		'''
		shell = self.hotBox.ui.chk000.isChecked()
		invert = self.hotBox.ui.chk001.isChecked()

		selection = pm.ls(selection=1)

		if not pm.nodeType(selection)=='VRayMultiSubTex': #if not a multimaterial
			mat = self.storedMaterial
		else:
			return '# Error: No valid stored material. If material is a multimaterial, select a submaterial. #'

		pm.select(mat)
		pm.hyperShade (objects='') #select all with material. "" defaults to currently selected materials.

		faces = pm.filterExpand (selectionMask=34, expand=1)
		transforms = [node.replace('Shape','') for node in pm.ls(sl=1, objectsOnly=1, visible=1)] #get transform node name from shape node
		# pm.select (faces, deselect=1)

		if shell or invert: #deselect so that the selection can be modified.
			pm.select (faces, deselect=1)

		if shell:
			for shell in transforms:
				pm.select (shell, add=1)
		
		if invert:
			for shell in transforms:
				allFaces = [shell+".f["+str(num)+"]" for num in range(pm.polyEvaluate (shell, face=1))] #create a list of all faces per shell
				pm.select(list(set(allFaces)-set(faces)), add=1) #get inverse of previously selected faces from allFaces


	def b001(self):
		'''
		Delete Material

		'''
		if self.ui.chk002.isChecked: #delete mat ID material
			mat = self.storedID_mats[self.ui.cmb002.currentText()] #get object from string key
			pm.delete(mat)
		else: #delete stored material
			pm.delete(self.storedMaterial)
			self.storedMaterial = None

			self.comboBox(self.ui.cmb002, [], 'Stored Material: None') #init combobox


	def b002(self):
		'''
		Store Material

		'''
		self.ui.chk002.setChecked(False) #put combobox in stored material mode

		if pm.ls(selection=1):
			pm.hyperShade("", shaderNetworksSelectMaterialNodes=1) #selects the material node 
			mat = pm.ls(selection=1, materials=1)[0] #now add the selected node to a variable

			self.storedMaterial = mat #store material
			self.cmb002() #refresh combobox
		else:
			print '# Error: Nothing selected. #'


	def b003(self):
		'''
		Assign Material

		'''
		if self.ui.chk002.isChecked(): #Assign Existing mat ID
			mat = self.storedID_mats[self.ui.cmb002.currentText()]
			for obj in pm.ls(selection=1, flatten=1):
				pm.hyperShade(obj, assign=mat)
		else: #assign stored material
			for obj in pm.ls(selection=1):
				pm.hyperShade(obj, assign=self.storedMaterial) #select and assign material per object in selection


	def b004(self):
		'''
		Assign New random mat ID

		'''
		self.ui.chk002.setChecked(True) #set combobox to ID map mode

		import random

		selection = pm.ls(selection=1, flatten=1)

		if selection:
			prefix = 'matID'
			rgb = [random.randint(0, 255) for _ in range(3)] #generate a list containing 3 values between 0-255

			#format name
			name = '_'.join([prefix, str(rgb[0]), str(rgb[1]), str(rgb[2])])
			#create shader
			mat = pm.shadingNode('lambert', asShader=1, name=name)
			#convert RGB to 0-1 values and assign to shader
			convertedRGB = [round(float(v)/255, 3) for v in rgb]
			pm.setAttr(name+'.color', convertedRGB)
			#assign to selected geometry
			pm.select(selection) #initial selection is lost upon node creation
			pm.hyperShade(assign=mat)

			#delete previous shader
			# if self.randomMat:
			# 	pm.delete(self.randomMat)

			self.randomMat = mat

			self.cmb002() #refresh combobox
		else:
			print '# Error: No valid object/s selected. #'


	def b005(self):
		'''
		
		'''
		pass


	def b006(self):
		'''
		Delete Unused Materials

		'''
		print '-< no maya version coded >-'


	def b007(self):
		'''
		Open material in editor

		'''
		if self.ui.chk002.isChecked(): #ID map mode
			try:
				mat = self.storedID_mats[self.ui.cmb002.currentText()] #get object from string key
			except:
				return '# Error: No stored material or no valid object selected. #'
		else: #Stored material mode
			if not self.storedMaterial: #get material from selected scene object
				if rt.selection:
					self.storedMaterial = rt.selection[0].material
				else:
					return '# Error: No stored material or no valid object selected. #'
			mat = self.storedMaterial

		#open the hypershade editor
		mel.eval("HypershadeWindow;")

		# #create a temp view in the material editor
		# if rt.SME.GetViewByName('temp'):
		# 	rt.SME.DeleteView(rt.SME.GetViewByName('temp'), False)
		# index = rt.SME.CreateView('temp')
		# view = rt.SME.GetView(index)

		# #show node and corresponding parameter rollout
		# node = view.CreateNode(mat, rt.point2(0, 0))
		# rt.SME.SetMtlInParamEditor(mat)


	def b008(self):
		'''
		Rename Material

		'''
		if self.ui.b008.isChecked(): #(rename checkbox)
			self.ui.t000.setText(self.ui.cmb002.currentText())
			if self.ui.t000.text()=='ID Map: None' or self.ui.t000.text()=='Stored Material: None':
				self.ui.b008.setChecked(False)
			else:
				self.ui.t000.show()
		else:
			if self.ui.chk002.isChecked(): #Rename ID map Material
				prefix='matID_'
				newName=self.ui.t000.text()
				 
				mat = self.storedID_mats[self.ui.cmb002.currentText()] #get object from string key
				if not newName.startswith(prefix):
					pm.rename(mat, prefix+newName) 
				else:
					pm.rename(mat, newName)
			else: #Rename Stored Material
				if self.storedMaterial:
					pm.rename(self.storedMaterial.name(), self.ui.t000.text())

			self.cmb002() #refresh combobox
			self.ui.t000.hide()


	def b009(self):
		'''
		

		'''
		pass


	def b010(self):
		'''
		

		'''
		pass




#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

#depricated

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

# 		$name = ("matID"+$rgb);

# 		string $matID = `shadingNode -asShader lambert -name $name`;
# 		setAttr ($name + ".colorR") $r;
# 		setAttr ($name + ".colorG") $g;
# 		setAttr ($name + ".colorB") $b;

# 		for ($object in $selection)
# 			{
# 			select $object;
# 			hyperShade -assign $matID;
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

		# $name = ("matID"+$rgb);

		# string $matID = `shadingNode -asShader lambert -name $name`;
		# setAttr ($name + ".colorR") $r;
		# setAttr ($name + ".colorG") $g;
		# setAttr ($name + ".colorB") $b;

		# for ($object in $selection)
		# 	{
		# 	select $object;
		# 	hyperShade -assign $matID;
		# 	}
		# ''')