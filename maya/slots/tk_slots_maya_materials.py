from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Materials(Init):
	def __init__(self, *args, **kwargs):
		super(Materials, self).__init__(*args, **kwargs)

		self.currentMaterial=None
		self.materials=None
		self.randomMat=None


	# def cmb001(self, index=None):
	# 	'''
	# 	Editors

	# 	'''
	# 	cmb = self.parentUi.cmb001
		
	# 	files = ['Hypershade']
	# 	contents = cmb.addItems_(files, ' ')

	# 	if index is None:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		if index==contents.index('Hypershade'):
	# 			mel.eval('HypershadeWindow;')
	# 		cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Material list

		args:
			index (int) = parameter on activated, currentIndexChanged, and highlighted signals.
		'''
		cmb = self.parentUi.cmb002

		if not cmb.initialized:
			b008 = cmb.addToContext('QPushButton', setText='Rename', setObjectName='b008', setToolTip='Rename material.')
			b008.clicked.connect(self.b008)

		if self.parentUi.b008.isChecked(): #prevents refreshing contents when enter is pressed during renaming.
			return

		try:
			sceneMaterials = self.parentUi.tb001.chk000.isChecked()
			idMapMaterials = self.parentUi.tb001.chk001.isChecked()
		except: #if the toolbox hasn't been constructed yet: default to sceneMaterials
			sceneMaterials = True

		if sceneMaterials:
			materials = [m for m in pm.ls(materials=1) if not pm.nodeType(m)=='standardSurface']

		elif idMapMaterials:
			materials = [m for m in pm.ls(mat=1, flatten=1) if m.name().startswith('matID')]

		mats = sorted([mat for mat in set(materials)])
		matNames = [m.name() for m in mats]
		contents = cmb.addItems_(matNames)

		#create and set icons with color swatch
		for i in range(len(mats)):
			r = int(pm.getAttr(matNames[i]+'.colorR')*255) #convert from 0-1 to 0-255 value and then to an integer
			g = int(pm.getAttr(matNames[i]+'.colorG')*255)
			b = int(pm.getAttr(matNames[i]+'.colorB')*255)
			pixmap = QtGui.QPixmap(100,100)
			pixmap.fill(QtGui.QColor.fromRgb(r, g, b))
			cmb.setItemIcon(i, QtGui.QIcon(pixmap))

		if index is None:
			index = cmb.currentIndex()

		self.materials = {name:mats[i] for i, name in enumerate(matNames)} #add mat objects to materials dictionary. 'mat name'=key, <mat object>=value
		self.currentMaterial = mats[index] if len(mats)>index and index>=0 else None #store material.


	def tb000(self, state=None):
		'''
		Select By Material Id
		'''
		tb = self.currentUi.tb000
		if state=='setMenu':
			tb.add('QCheckBox', setText='Shell', setObjectName='chk005', setToolTip='Select entire shell.')
			tb.add('QCheckBox', setText='Invert', setObjectName='chk006', setToolTip='Invert Selection.')
			return

		shell = tb.chk005.isChecked() 
		invert = tb.chk006.isChecked()

		selection = pm.ls(selection=1)

		if not pm.nodeType(selection)=='VRayMultiSubTex': #if not a multimaterial
			mat = self.currentMaterial
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


	def tb001(self, state=None):
		'''
		Stored Material Options
		'''
		tb = self.currentUi.tb001
		if state=='setMenu':
			tb.add('QRadioButton', setText='All Scene Materials', setObjectName='chk000', setChecked=True, setToolTip='List all scene materials.') #Material mode: Scene Materials
			tb.add('QRadioButton', setText='ID Map Materials', setObjectName='chk001', setToolTip='List ID map materials.') #Material mode: ID Map Materials
			
			self.connect_([tb.chk000, tb.chk001], 'toggled', [self.cmb002, self.tb001])
			return

		if tb.chk000.isChecked():
			self.parentUi.group000.setTitle(tb.chk000.text())
		elif tb.chk001.isChecked():
			self.parentUi.group000.setTitle(tb.chk001.text())


	def tb002(self, state=None):
		'''
		Delete Material
		'''
		tb = self.currentUi.tb002
		if state=='setMenu':
			tb.add('QRadioButton', setText='Delete Current Material', setObjectName='chk003', setChecked=True, setToolTip='Delete the current material.')
			tb.add('QRadioButton', setText='Delete Unused Materials', setObjectName='chk004', setToolTip='Delete All unused materials.')
			return

		if tb.chk003.isChecked():
			if self.parentUi.tb001.chk001.isChecked: #delete mat ID material
				mat = self.materials[self.parentUi.cmb002.currentText()] #get object from string key
				pm.delete(mat)
			else: #delete stored material
				pm.delete(self.currentMaterial)
				self.currentMaterial = None

				self.comboBox(self.parentUi.cmb002, [], 'Stored Material: None') #init combobox

		if tb.chk004.isChecked(): #Delete Unused Materials
			print('-< no maya version coded >-')
			# defaultMaterial = rt.Standard(name='Default Material')
			
			# for mat in rt.scenematerials:
			# 	nodes = rt.refs().dependentnodes(mat) 
			# 	if nodes.count==0:
			# 		rt.replaceinstances(mat, defaultMaterial)
					
			# 	rt.gc()
			# 	rt.freeSceneBitmaps()


	def tb003(self, state=None):
		'''
		Assign Material
		'''
		tb = self.currentUi.tb003
		if state=='setMenu':
			tb.add('QRadioButton', setText='Current Material', setObjectName='chk007', setChecked=True, setToolTip='Re-Assign the current stored material.')
			tb.add('QRadioButton', setText='New Random Material', setObjectName='chk008', setToolTip='Assign a new random ID material.')
			return


		if tb.chk008.isChecked(): #Assign New random mat ID
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

				if self.parentUi.tb001.chk001.isChecked():
					self.cmb002() #refresh the combobox
				else:
					self.parentUi.tb001.chk001.setChecked(True) #set combobox to ID map mode. toggling the checkbox refreshes the combobox.
				self.parentUi.cmb002.setCurrent_(name) #set the combobox index to the new mat #self.cmb002.setCurrentIndex(self.cmb002.findText(name))
			else:
				print('# Error: No valid object/s selected. #')

		elif tb.chk007.isChecked(): #Assign current mat
				mat = self.materials[self.parentUi.cmb002.currentText()]
				for obj in pm.ls(selection=1, flatten=1):
					pm.hyperShade(obj, assign=mat)


	def b002(self):
		'''
		Store Material

		'''
		if pm.ls(selection=1):
			pm.hyperShade("", shaderNetworksSelectMaterialNodes=1) #selects the material node 
			mat = pm.ls(selection=1, materials=1)[0] #now add the selected node to a variable

			self.currentMaterial = mat #store material
			self.parentUi.tb001.chk000.setChecked(True) #put combobox in current material mode
			self.cmb002() #refresh combobox
		else:
			print('# Error: Nothing selected. #')


	def b007(self):
		'''
		Open material in editor

		'''
		if self.parentUi.tb001.chk001.isChecked(): #ID map mode
			try:
				mat = self.materials[self.parentUi.cmb002.currentText()] #get object from string key
			except:
				return '# Error: No stored material or no valid object selected. #'
		else: #Stored material mode
			if not self.currentMaterial: #get material from selected scene object
				if rt.selection:
					self.currentMaterial = rt.selection[0].material
				else:
					return '# Error: No stored material or no valid object selected. #'
			mat = self.currentMaterial

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


	def renameMaterial(self):
		'''
		Rename Material
		'''
		newMatName = self.parentUi.cmb002.currentText()

		if self.currentMaterial:
			if self.parentUi.tb001.chk001.isChecked(): #Rename ID map Material
				prefix = 'matID_'
				if not newMatName.startswith(prefix):
					newMatName = prefix+newMatName

			cmb.setItemText(cmb.currentIndex(), newMatName)
			pm.rename(self.currentMaterial.name(), newMatName)


	def b008(self):
		'''
		Toggle: Rename Material
		'''
		b = self.parentUi.b008

		if b.isChecked(): #set combobox as editable and disable widgets.
			self.currentMatName = self.parentUi.cmb002.currentText()

			if self.currentMatName=='ID Map: None' or self.currentMatName=='Current Material: None':
				b.setChecked(False)
			else:
				self.parentUi.cmb002.setEditable(True)
				self.toggleWidgets(self.parentUi, setDisabled='b002,b007,tb000,tb002-3')

		else: #rename material and re-enable widgets
			self.renameMaterial()
			self.parentUi.cmb002.setEditable(False)
			self.toggleWidgets(self.parentUi, setEnabled='b002,b007,tb000,tb002-3')









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