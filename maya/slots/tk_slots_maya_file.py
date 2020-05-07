from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class File(Init):
	def __init__(self, *args, **kwargs):
		super(File, self).__init__(*args, **kwargs)

		self.ui = self.parentUi #self.ui = self.sb.getUi(self.__class__.__name__)

		try:
			self.cmb006() #refresh cmb006 contents to reflect the current project folder
		except NameError:
			pass


	def cmb000(self, index=None):
		'''
		Recent Files

		'''
		cmb = self.ui.cmb000
		
		files = [file_ for file_ in (list(reversed(mel.eval("optionVar -query RecentFilesList;")))) if "Autosave" not in file_]
		contents = cmb.addItems_(files, "Recent Files")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			force=True; force if str(mel.eval("file -query -sceneName -shortName;")) else not force #if sceneName prompt user to save; else force open
			pm.openFile(contents[index], open=1, force=force)
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Recent Projects

		'''
		cmb = self.ui.cmb001
		
		files = (list(reversed(mel.eval("optionVar -query RecentProjectsList;"))))
		contents = cmb.addItems_(files, "Recent Projects")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			mel.eval('setProject "'+contents[index]+'"')
			cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Recent Autosave

		'''
		cmb = self.ui.cmb002

		path = os.environ.get('MAYA_AUTOSAVE_FOLDER').split(';')[0] #get autosave dir path from env variable.
		files = [f for f in os.listdir(path) if f.endswith('.mb') or f.endswith('.ma')] #[file_ for file_ in (list(reversed(mel.eval("optionVar -query RecentFilesList;")))) if "Autosave" in file_]
		contents = cmb.addItems_(files, "Recent Autosave")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			force=True
			if str(mel.eval("file -query -sceneName -shortName;")):
				force=False #if sceneName, prompt user to save; else force open
			pm.openFile(path+contents[index], open=1, force=force)
			print(path+contents[index])
			cmb.setCurrentIndex(0)


	def cmb003(self, index=None):
		'''
		Import

		'''
		cmb = self.ui.cmb003

		contents = cmb.addItems_(["Import file", "Import Options"], "Import")

		if not index:
			index = cmb.currentIndex()
		if index!=0: #hide then perform operation
			self.tk.hide(force=1)
			if index == 1: #Import
				mel.eval('Import;')
			if index == 2: #Import options
				mel.eval('ImportOptions;')
			cmb.setCurrentIndex(0)


	def cmb004(self, index=None):
		'''
		Export

		'''
		cmb = self.ui.cmb004
		
		list_ = ["Export Selection", "Export Options", "Unreal", "Unity", "GoZ", 'Send to 3dsMax: As New Scene', 'Send to 3dsMax: Update Current', 'Send to 3dsMax: Add to Current']
		contents = cmb.addItems_(list_, "Export")

		if not index:
			index = cmb.currentIndex()
		if index !=0: #hide then perform operation
			self.tk.hide(force=1)
			if index==1: #Export selection
				mel.eval('ExportSelection;')
			if index==2: #Export options
				mel.eval('ExportSelectionOptions;')
			if index==3: #Unreal
				mel.eval('SendToUnrealSelection;')
			if index==4: #Unity 
				mel.eval('SendToUnitySelection;')
			if index==5: #GoZ
				mel.eval('print("GoZ"); source"C:/Users/Public/Pixologic/GoZApps/Maya/GoZBrushFromMaya.mel"; source "C:/Users/Public/Pixologic/GoZApps/Maya/GoZScript.mel";')
			if index==6: #Send to 3dsMax: As New Scene
				mel.eval('SendAsNewScene3dsMax;') #OneClickMenuExecute ("3ds Max", "SendAsNewScene"); doMaxFlow { "sendNew","perspShape","1" };
			if index==7: #Send to 3dsMax: Update Current
				mel.eval('UpdateCurrentScene3dsMax;') #OneClickMenuExecute ("3ds Max", "UpdateCurrentScene"); doMaxFlow { "update","perspShape","1" };
			if index==8: #Send to 3dsMax: Add to Current
				mel.eval('AddToCurrentScene3dsMax;') #OneClickMenuExecute ("3ds Max", "AddToScene"); doMaxFlow { "add","perspShape","1" };
			cmb.setCurrentIndex(0)


	def cmb005(self, index=None):
		'''
		Editors

		'''
		cmb = self.ui.cmb005
		
		files = ['Node Editor', 'Outlinder', 'Content Browser']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Node Editor'):
				mel.eval('NodeEditorWindow;') #
			if index==contents.index('Outlinder'):
				mel.eval('OutlinerWindow;') #
			if index==contents.index('Content Browser'):
				mel.eval('ContentBrowserWindow;') #
			cmb.setCurrentIndex(0)


	def cmb006(self, index=None):
		'''
		Project Folder

		'''
		cmb = self.ui.cmb006
		
		path = pm.workspace(query=1, rd=1) #current project path.
		list_ = [f for f in os.listdir(path)]

		project = pm.workspace(query=1, rd=1).split('/')[-2] #add current project path string to label. strip path and trailing '/'

		contents = cmb.addItems_(list_, project)

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			dir_= path+list_[index-1]
			if dir_.startswith('//'): #reformat for server address
				dir_ = dir_.replace('/', '\\')
			os.startfile(dir_)
			cmb.setCurrentIndex(0)


	def tb000(self, state=None):
		'''
		Save
		'''
		tb = self.currentUi.tb000
		if state=='setMenu':
			tb.add('QCheckBox', setText='ASCII', setObjectName='chk003', setChecked=True, setToolTip='Toggle ASCII or binary file type.')
			tb.add('QCheckBox', setText='Wireframe', setObjectName='chk000', setChecked=True, setToolTip='Set view to wireframe before save.')
			tb.add('QCheckBox', setText='Increment', setObjectName='chk001', setChecked=True, setToolTip='Append and increment a unique integer value.')
			tb.add('QCheckBox', setText='Quit', setObjectName='chk002', setToolTip='Quit after save.')
			return

		preSaveScript = ''
		postSaveScript = ''

		type_ = "mayaBinary"
		if tb.chk003.isChecked(): #toggle ascii/ binary
			type_ = "mayaAscii" #type: mayaAscii, mayaBinary, mel, OBJ, directory, plug-in, audio, move, EPS, Adobe(R) Illustrator(R)

		if tb.chk000.isChecked():
			mel.eval("DisplayWireframe;")

		#get scene name and file path
		fullPath = str(mel.eval("file -query -sceneName;")) #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.maya/elise_mid.009.mb
		index = fullPath.rfind("/")+1
		curFullName = fullPath[index:] #ie. elise_mid.009.mb
		currentPath = fullPath[:index] #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.maya/
		
		if tb.chk001.isChecked(): #increment filename
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
								try:
									import os
									os.remove(filename)
								except:
									pass
				except OSError:
					print("# Warning: could not delete ", currentPath+oldName, " #")
					pass
			else:
				newName = currentName+".001"
			pm.saveAs (currentPath+newName, force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
			print("# Result: ", currentPath+newName, " #")
		else:	#save without renaming
			pm.saveFile (force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
			print("# Result: ", currentPath+currentName, " #")

		if tb.chk002.isChecked(): #quit maya
			import time
			for timer in range(5):
				self.viewPortMessage("shutting down:<hl>"+str(timer)+"</hl>")
				time.sleep(timer)
			mel.eval("quit;")
			# pm.Quit()


	def b001(self):
		'''
		Recent Files: Open Last
		'''
		# files = [file_ for file_ in (list(reversed(mel.eval("optionVar -query RecentFilesList;")))) if "Autosave" not in file_]

		# force=True
		# if str(mel.eval("file -query -sceneName -shortName;")):
		# 	force=False #if sceneName, prompt user to save; else force open
		# pm.openFile(files[0], open=1, force=force)

		self.tk.hide(force=1)
		self.cmb000(index=1)


	def b002(self):
		'''
		Fbx Presets

		'''
		mel.eval('FBXUICallBack -1 editExportPresetInNewWindow fbx;')


	def b003(self):
		'''
		Obj Presets

		'''
		mel.eval('FBXUICallBack -1 editExportPresetInNewWindow obj;')


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
		self.tk.hide(force=1)


	def b006(self):
		'''
		Restore Main Application

		'''
		pass


	def setComboBox(self, comboBox, text):
		'''
		Set the given comboBox's index using a text string.
		args:
			comboBox (str) = comboBox name (will also be used as the methods name).
			text (str) = text of the index to switch to.
		'''
		cmb = getattr(self.ui, comboBox)
		method = getattr(self, comboBox)
		cmb.currentIndexChanged.connect(method)
		cmb.setCurrentIndex(cmb.findText(text))


	def b007(self):
		'''
		Import file
		'''
		self.cmb003(index=1)


	def b008(self):
		'''
		Export Selection
		'''
		self.cmb004(index=1)


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


	def b017(self):
		'''
		Set Project

		'''
		newProject = mel.eval("SetProject;")

		self.cmb006() #refresh cmb006 contents to reflect new project folder







#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------