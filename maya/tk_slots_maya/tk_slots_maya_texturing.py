import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





#    dP                       dP                     oo                   
#    88                       88                                          
#  d8888P .d8888b. dP.  .dP d8888P dP    dP 88d888b. dP 88d888b. .d8888b. 
#    88   88ooood8  `8bd8'    88   88    88 88'  `88 88 88'  `88 88'  `88 
#    88   88.  ...  .d88b.    88   88.  .88 88       88 88    88 88.  .88 
#    dP   `88888P' dP'  `dP   dP   `88888P' dP       dP dP    dP `8888P88 
#                                                                     .88 
#                                                                 d8888P
#
class Texturing(Init):
	def __init__(self, *args, **kwargs):
		super(Texturing, self).__init__(*args, **kwargs)

		

	def cmb000(self): #existing materials
		index = self.hotBox.ui.cmb000.currentIndex() #get current index before refreshing list
		materials = self.comboBox (self.hotBox.ui.cmb000, [str(mat) for mat in pm.ls(materials=1)], "Existing Materials")

		if index!=0:
			print materials[index]
			# shader = pm.shadingNode (mat, asShader=1) #asShader, asTexture, asLight
			pm.hyperShade (assign=materials[index])
			self.hotBox.ui.cmb000.setCurrentIndex(0)


	def chk000(self):
		self.hotBox.ui.chk001.setChecked(False)

	def chk001(self):
		self.hotBox.ui.chk000.setChecked(False)


	def b000(self): #Select by material ID
		shell = self.hotBox.ui.chk000.isChecked()
		invert = self.hotBox.ui.chk001.isChecked()

		if self.try_('pm.ls(selection=1, objectsOnly=1)[0]', 'print "# Warning: Nothing selected #"'):
			pm.hyperShade (pm.ls(sl=1, objectsOnly=1, visible=1)[0], shaderNetworksSelectMaterialNodes=1) #get material node from selection
			pm.hyperShade (objects="") #select all with material. "" defaults to currently selected materials.

			faces = pm.filterExpand (selectionMask=34, expand=1)
			transforms = [node.replace('Shape','') for node in pm.ls(sl=1, objectsOnly=1, visible=1)] #get transform node name from shape node
			pm.select (faces, deselect=1)

			if shell or invert: #deselect so that the selection can be modified.
				pm.select (faces, deselect=1)

			if shell:
				for shell in transforms:
					pm.select (shell, add=1)
			
			if invert:
				for shell in transforms:
					allFaces = [shell+".f["+str(num)+"]" for num in range(pm.polyEvaluate (shell, face=1))] #create a list of all faces per shell
					pm.select (list(set(allFaces)-set(faces)), add=1) #get inverse of previously selected faces from allFaces


	def b001(self): #
		pass


	def b002(self): #Store material Id
		pm.hyperShade("", shaderNetworksSelectMaterialNodes=1) #selects the material node 
		matID = pm.ls(selection=1, materials=1)[0] #now add the selected node to a variable
		self.hotBox.ui.lbl000.setText(str(matID))

		
	def b003(self): #Assign material Id
		matID = str(self.hotBox.ui.lbl000.text())

		for obj in pm.ls(selection=1):
			pm.hyperShade(obj, assign=matID) #select and assign material per object in selection


	def b004(self): #Assign random material
		mel.eval('''
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


	def b005(self): #Re-Assign random ID material
		mel.eval('''
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


	def b006(self): #
		pass

	def b007(self): #
		pass

	def b008(self): #
		pass

	def b009(self): #
		pass

	def b010(self): #
		pass

	def b011(self): #
		pass

	def b012(self): #
		pass

	def b013(self): #
		pass

	def b014(self): #
		pass

	def b015(self): #
		pass

	def b016(self): #
		pass

	def b017(self): #
		pass

	def b018(self): #
		pass

	def b019(self): #hyperShade editor
		mel.eval("HypershadeWindow;")



#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------