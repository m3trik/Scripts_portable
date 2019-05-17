import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Texturing(Init):
	def __init__(self, *args, **kwargs):
		super(Texturing, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('texturing')

		self.selectedMaterial = None #currently stored material


	def t000(self):
		'''
		Material Name
		'''
		print self.selectedMaterial.name+' renamed to '+self.ui.t000.text()
		self.selectedMaterial.name = self.ui.t000.text()


	def cmb000(self):
		'''
		Existing Materials

		'''
		cmb = self.ui.cmb000
		
		materials = [mat for mat in rt.sceneMaterials if 'Multimaterial' not in mat.name and 'BlendMtl' not in mat.name and not mat.name.startswith('Material')]
		materialNames = sorted([mat.name for mat in materials])
		
		contents = self.comboBox (cmb, materialNames, "Scene Materials:")

		index = cmb.currentIndex()
		if index!=0:
			self.selectedMaterial = [m for m in materials if m.name==contents[index]][0]
			print self.selectedMaterial

			for obj in rt.selection: #if an object is selected; assign material
				obj.material = self.selectedMaterial #assign material to any selected object

			self.ui.t000.setText(cmb.currentText()) #str(self.selectedMaterial.name)) #store material name in text label
			rt.redrawViews()
			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		Editors

		'''
		cmb = self.ui.cmb001
		
		files = ['Material Editor']
		contents = self.comboBox (cmb, files, "Editors")

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Material Editor'):
				maxEval('max mtledit')
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


	def b001(self):
		'''
		Delete Material

		'''
		# self.selectedMaterial = rt.Standard(name="Default Material") #replace with standard material
		self.selectedMaterial = None

		self.ui.t000.clear()


	def b002(self):
		'''
		Store Material Id

		'''
		self.selectedMaterial = rt.selection[0].material #get material from selection
		self.ui.t000.setText(str(self.selectedMaterial.name)) #store material name in text label

		
	def b003(self):
		'''
		Assign Material Id

		'''
		for obj in rt.selection:
			obj.material = self.selectedMaterial #assign material per object in selection
		rt.redrawViews()


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
		Delete Unused Materials

		'''
		maxEval('''
			def_material = Standard name:"Default Material"
			count = 0
			for mat in scenematerials do undo off
			(
				nodes = refs.dependentnodes mat 
				if nodes.count == 0 do 
				(
					replaceinstances mat def_material
					count += 1
				)
			)
			gc()
			freeSceneBitmaps()
			count
			''')

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