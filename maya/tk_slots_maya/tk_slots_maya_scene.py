import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Scene(Init):
	def __init__(self, *args, **kwargs):
		super(Scene, self).__init__(*args, **kwargs)




		self.ui.lbl000.setText(pm.workspace (query=1, rd=1).split('/')[-2]) #add current project path string to label. strip path and trailing '/'
		


	def cmb000(self):
		'''
		Recent Files

		'''
		cmb = self.ui.cmb000
		
		files = [file_ for file_ in (list(reversed(mel.eval("optionVar -query RecentFilesList;")))) if "Autosave" not in file_]
		contents = self.comboBox (cmb, files, "Recent Files")

		index = cmb.currentIndex()
		if index!=0:
			force=True; force if str(mel.eval("file -query -sceneName -shortName;")) else not force #if sceneName prompt user to save; else force open
			pm.openFile (contents[index], open=1, force=force)
			cmb.setCurrentIndex(0)

	def cmb001(self):
		'''
		Recent Projects

		'''
		cmb = self.ui.cmb001
		
		files = (list(reversed(mel.eval("optionVar -query RecentProjectsList;"))))
		contents = self.comboBox (cmb, files, "Recent Projects")

		index = cmb.currentIndex()
		if index!=0:
			mel.eval('setProject "'+contents[index]+'"')
			cmb.setCurrentIndex(0)

	def cmb002(self):
		'''
		Recent Autosave

		'''
		cmb = self.ui.cmb002
		
		files = [file_ for file_ in (list(reversed(mel.eval("optionVar -query RecentFilesList;")))) if "Autosave" in file_]
		contents = self.comboBox (cmb, files, "Recent Autosave")

		index = cmb.currentIndex()
		if index!=0:
			force=True; force if str(mel.eval("file -query -sceneName -shortName;")) else not force #if sceneName prompt user to save; else force open
			pm.openFile (contents[index], open=1, force=force)
			cmb.setCurrentIndex(0)
			
	def cmb003(self):
		'''
		Import

		'''
		cmb = self.ui.cmb003
		
		contents = self.comboBox (cmb,["Import file", "Import Options"], "Import")
		
		index = cmb.currentIndex()
		if index!=0: #hide hotBox then perform operation
			self.hotBox.hide_()
			if index == 1: #Import
				mel.eval('Import;')
			if index == 2: #Import options
				mel.eval('ImportOptions;')
			cmb.setCurrentIndex(0)

	def cmb004(self):
		'''
		Export

		'''
		cmb = self.ui.cmb004
		
		contents = self.comboBox (cmb, ["Export Selection", "Export Options", "Unreal", "Unity", "GoZ"], "Export")

		index = cmb.currentIndex()
		if index !=0: #hide hotBox then perform operation
			self.hotBox.hide_()
			if index == 1: #Export selection
				mel.eval('ExportSelection;')
			if index == 2: #Export options
				mel.eval('ExportSelectionOptions;')
			if index == 3: #Unreal
				mel.eval('SendToUnrealSelection;')
			if index == 4: #Unity 
				mel.eval('SendToUnitySelection;')
			if index == 5: #GoZ
				mel.eval('print("GoZ"); source"C:/Users/Public/Pixologic/GoZApps/Maya/GoZBrushFromMaya.mel"; source "C:/Users/Public/Pixologic/GoZApps/Maya/GoZScript.mel";')
			cmb.setCurrentIndex(0)

	def b000(self):
		'''
		Save

		'''
		preSaveScript = ""
		postSaveScript = ""

		type_ = "mayaBinary"
		if self.ui.chk003.isChecked(): #toggle ascii/ binary
			type_ = "mayaAscii" #type: mayaAscii, mayaBinary, mel, OBJ, directory, plug-in, audio, move, EPS, Adobe(R) Illustrator(R)

		if self.ui.chk000.isChecked():
			mel.eval("DisplayWireframe;")

		#get scene name and file path
		fullPath = str(mel.eval("file -query -sceneName;")) #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.maya/elise_mid.009.mb
		index = fullPath.rfind("/")+1
		curFullName = fullPath[index:] #ie. elise_mid.009.mb
		currentPath = fullPath[:index] #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.maya/
		
		if self.ui.chk001.isChecked(): #increment filename
			import re, os, fnmatch, shutil
			incrementAmount = 5

			#remove filetype extention
			currentName = curFullName[:curFullName.rfind(".")] #name without extension ie. elise_mid.009 from elise_mid.009.mb
			#rename
			numExt = re.search(r'\d+$', currentName) #check if the last chars are numberic
			if numExt is not None:
				name = currentName[:currentName.rfind('.')] #strip off the number ie. elise_mid from elise_mid.009
				num = int(numExt.group())+1 #get file number and add 1 ie. 9 becomes 10
				prefix = '000'[:-len(str(num))]+str(num) #prefix '000' removing zeros according to num length ie. 009 becomes 010
				newName = name+'.'+prefix #ie. elise_mid.010

				#delete older files if they exist:
				oldNum = num-incrementAmount
				oldPrefix = '000'[:-len(str(oldNum))]+str(oldNum) #prefix the appropriate amount of zeros in front of the old number
				oldName = name+'.'+oldPrefix #ie. elise_mid.007
				try: #search recursively through the project folder and delete any old folders with the old filename
					dir_ =  os.path.abspath(os.path.join(currentPath, "../.."))
					for root, directories, files in os.walk(dir_):
						for filename in files:
							if all([filename==oldName+ext for ext in ('.ma','.ma.swatches','.mb','.mb.swatches')]):
								self.try_('import os; os.remove(arg)', arg=filename)
				except OSError:
					print "# Warning: could not delete "+currentPath+oldName+" #"
					pass
			else:
				newName = currentName+".001"
			pm.saveAs (currentPath+newName, force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
			print "// Result: ", currentPath+newName
		else:	#save without renaming
			pm.saveFile (force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
			print "// Result: ", currentPath+currentName

		if self.ui.chk002.isChecked(): #quit maya
			import time
			for timer in range(5):
				self.viewPortMessage("shutting down:<hl>"+str(timer)+"</hl>")
				time.sleep(timer)
			mel.eval("quit;")
			# pm.Quit()

	def b001(self):
		'''
		Hypergraph: Hierarchy

		'''
		mel.eval("hyperGraphWindow \"\" \"DAG\";")

	def b002(self):
		'''
		Hypergraph: Input/Output

		'''
		mel.eval('hyperGraphWindow \"\" \"DG\";')

	def b003(self):
		'''
		Node Editor

		'''
		mel.eval("nodeEditorWindow;")

	def b004(self):
		'''
		Close Main Application

		'''
		# force=false #pymel has no attribute quit error.
		# exitcode=""
		sceneName = str(mel.eval("file -query -sceneName -shortName;")) #if sceneName prompt user to save; else force close
		mel.eval("quit;") if sceneName else mel.eval("quit -f;")
		# pm.quit (force=force, exitcode=exitcode)

	def b005(self):
		'''
		Minimize Main Application

		'''
		mel.eval("minimizeApp;")
		self.hotBox.hbHide()

	def b006(self):
		'''
		Restore Main Application

		'''
		pass

	def b007(self):
		'''
		

		'''
		pass

	def b015(self):
		'''
		Remove String From Object Names.

		'''
		from_ = str(self.ui.t000.text()) #asterisk denotes startswith*, *endswith, *contains* 
		to = str(self.ui.t001.text())
		replace = self.ui.chk004.isChecked()
		selected = self.ui.chk005.isChecked()

		objects = pm.ls (from_) #Stores a list of all objects starting with 'from_'
		if selected:
			objects = pm.ls (selection=1) #if use selection option; get user selected objects instead
		from_ = from_.strip('*') #strip modifier asterisk from user input

		for obj in objects:
			relatives = pm.listRelatives(obj, parent=1) #Get a list of it's direct parent
			if 'group*' in relatives: #If that parent starts with group, it came in root level and is pasted in a group, so ungroup it
				relatives[0].ungroup()

			newName = to
			if replace:
				newName = obj.replace(from_, to)
			pm.rename(obj, newName) #Rename the object with the new name

	def b016(self):
		'''
		

		'''
		pass

	def b017(self):
		'''
		Set Project

		'''
		mel.eval ("SetProject;")


#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------