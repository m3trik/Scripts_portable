import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Texturing(Init):
	def __init__(self, *args, **kwargs):
		super(Texturing, self).__init__(*args, **kwargs)


		

	def cmb000(self):
		'''
		Existing Materials

		'''
		cmb = self.ui.cmb000
		index = cmb.currentIndex() #get current index before refreshing list
		materials = [mat for mat in rt.sceneMaterials]
		materialNames = [mat.name for mat in materials]
		self.comboBox (cmb, materialNames, "Scene Materials")

		if index!=0:
			print materials[index]
			for obj in rt.selection:
				obj.material = materials[index]
			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		Editors

		'''
		cmb = self.ui.cmb001
		index = cmb.currentIndex() #get current index before refreshing list
		files = ['Hypershade']
		self.comboBox (cmb, files, "Editors")

		if index!=0:
			if index==files.index('Hypershade'):
				mel.eval("HypershadeWindow;")
			cmb.setCurrentIndex(0)


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

		maxEval('''
		if subobjectlevel == undefined then
			max modify mode; \
		if subobjectlevel != 4 then 
			subobjectlevel = 4; \
		Try(ApplyOperation Edit_Patch PatchOps.SelectByMatID)Catch();
		''')

		# if self.try_('pm.ls(selection=1, objectsOnly=1)[0]', 'print "# Warning: Nothing selected #"'):
		# 	pm.hyperShade (pm.ls(sl=1, objectsOnly=1, visible=1)[0], shaderNetworksSelectMaterialNodes=1) #get material node from selection
		# 	pm.hyperShade (objects="") #select all with material. "" defaults to currently selected materials.

		# 	faces = pm.filterExpand (selectionMask=34, expand=1)
		# 	transforms = [node.replace('Shape','') for node in pm.ls(sl=1, objectsOnly=1, visible=1)] #get transform node name from shape node
		# 	pm.select (faces, deselect=1)

		# 	if shell or invert: #deselect so that the selection can be modified.
		# 		pm.select (faces, deselect=1)

		# 	if shell:
		# 		for shell in transforms:
		# 			pm.select (shell, add=1)
			
		# 	if invert:
		# 		for shell in transforms:
		# 			allFaces = [shell+".f["+str(num)+"]" for num in range(pm.polyEvaluate (shell, face=1))] #create a list of all faces per shell
		# 			pm.select (list(set(allFaces)-set(faces)), add=1) #get inverse of previously selected faces from allFaces


	def b001(self):
		'''
		

		'''
		pass


	def b002(self):
		'''
		Store Material Id

		'''
		matName = rt.selection[0].material.name
		self.ui.lbl000.setText(str(matName)) #store material name in text label

		
	def b003(self):
		'''
		Assign Material Id

		'''
		matName = str(self.ui.lbl000.text())
		mat = [mat for mat in rt.sceneMaterials if matName in mat.name][0] #use string to get material

		for obj in rt.selection:
			obj.material=mat #select and assign material per object in selection


	def b004(self):
		'''
		Assign Random Material

		'''
		maxEval('''
		string $selection[] = `ls -selection`;

		int $d = 2; //decimal places to round to
		$r = rand (0,1);
		$r = trunc($r*`pow 10 $d`+0.5)/`pow 10 $d`;
		$g = rand (0,1);
		$g = trunc($g*`pow 10 $d`+0.5)/`pow 10 $d`;
		$b = rand (0,1);
		$b = trunc($b*`pow 10 $d`+0.5)/`pow 10 $d`;

		string $rgb = ("_"+$r+"_"+$g+"_"+$b);
		$rgb = substituteAllString($rgb, "0.", "");

		$name = ("matID"+$rgb);

		string $matID = `shadingNode -asShader lambert -name $name`;
		setAttr ($name + ".colorR") $r;
		setAttr ($name + ".colorG") $g;
		setAttr ($name + ".colorB") $b;

		for ($object in $selection)
			{
			select $object;
			hyperShade -assign $matID;
			}
		 ''')


	def b005(self):
		'''
		Re-Assign Random Id Material

		'''
		maxEval('''
		string $objList[] = `ls -selection -flatten`;
		$material = `hyperShade -shaderNetworksSelectMaterialNodes ""`;
		string $matList[] = `ls -selection -flatten`;

		hyperShade -objects $material;
		string $selection[] = `ls -selection`;
		//delete the old material and shader group nodes
		for($i=0; $i<size($matList); $i++)
			{
			string $matSGplug[] = `connectionInfo -dfs ($matList[$i] + ".outColor")`;
			$SGList[$i] = `match "^[^\.]*" $matSGplug[0]`;
			print $matList; print $SGList;
			delete $matList[$i];
			delete $SGList[$i];
			}
		//create new random material
		int $d = 2; //decimal places to round to
		$r = rand (0,1);
		$r = trunc($r*`pow 10 $d`+0.5)/`pow 10 $d`;
		$g = rand (0,1);
		$g = trunc($g*`pow 10 $d`+0.5)/`pow 10 $d`;
		$b = rand (0,1);
		$b = trunc($b*`pow 10 $d`+0.5)/`pow 10 $d`;

		string $rgb = ("_"+$r+"_"+$g+"_"+$b+"");
		$rgb = substituteAllString($rgb, "0.", "");

		$name = ("matID"+$rgb);

		string $matID = `shadingNode -asShader lambert -name $name`;
		setAttr ($name + ".colorR") $r;
		setAttr ($name + ".colorG") $g;
		setAttr ($name + ".colorB") $b;

		for ($object in $selection)
			{
			select $object;
			hyperShade -assign $matID;
			}
		''')


	def b006(self):
		'''
		

		'''
		pass

	def b007(self):
		'''
		

		'''
		pass

	def b008(self):
		'''
		

		'''
		pass

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