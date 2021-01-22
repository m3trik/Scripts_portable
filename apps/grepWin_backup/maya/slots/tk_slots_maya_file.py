from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class File(Init):
	def __init__(self, *args, **kwargs):
		super(File, self).__init__(*args, **kwargs)


	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.file.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb005', setToolTip='')
			draggable_header.contextMenu.add(wgts.TkToolButton, setObjectName='tb000', setText='Save', setToolTip='')
			draggable_header.contextMenu.add(wgts.TkLabel, setObjectName='lbl001', setText='Minimize App', setToolTip='Minimize the main application.')
			draggable_header.contextMenu.add(wgts.TkLabel, setObjectName='lbl002', setText='Maximize App', setToolTip='Restore the main application.')
			draggable_header.contextMenu.add(wgts.TkLabel, setObjectName='lbl003', setText='Close App', setToolTip='Close the main application.')
			return


	def cmb000(self, index=None):
		'''Recent Files
		'''
		cmb = self.file.cmb000

		if index is 'setMenu':
			cmb.contextMenu.add('QPushButton', setObjectName='b001', setText='Last', setToolTip='Open the most recent file.')
			return

		recentFiles = [File.formatPath(f) for f in (list(reversed(pm.optionVar(query='RecentFilesList')))) if "Autosave" not in f]
		cmb.addItems_(recentFiles, "Recent Files", clear=True)

		#set the text for the open last file button to the last file's name.
		self.file_submenu.b001.setText(File.getNameFromFullPath(recentFiles[0])) if recentFiles else self.file_submenu.b001.setVisible(False)

		if index>0:
			force=True; force if str(pm.mel.file(query=1, sceneName=1, shortName=1)) else not force #if sceneName prompt user to save; else force open
			pm.openFile(cmb.items[index], open=1, force=force)
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''Recent Projects
		'''
		cmb = self.file.cmb001

		if index is 'setMenu':
			return

		files = (list(reversed(pm.optionVar(query='RecentProjectsList'))))
		cmb.addItems_(files, "Recent Projects", clear=True)

		if index>0:
			pm.mel.setProject(cmb.items[index]) #mel.eval('setProject "'+items[index]+'"')
			cmb.setCurrentIndex(0)


	@Slots.message
	def cmb002(self, index=None):
		'''Recent Autosave
		'''
		cmb = self.file.cmb002

		if index is 'setMenu':
			return

		dir1 = str(pm.workspace(query=1, rd=1))+'autosave' #current project path.
		dir2 = os.environ.get('MAYA_AUTOSAVE_FOLDER').split(';')[0] #get autosave dir path from env variable.

		files = File.getAbsoluteFilePaths(dir1) + File.getAbsoluteFilePaths(dir2)
		cmb.addItems_(files, 'Recent Autosave', clear=True)

		if index>0:
			force=True
			if str(pm.mel.file(query=1, sceneName=1, shortName=1)):
				force=False #if sceneName, prompt user to save; else force open

			pm.openFile(cmb.items[index], open=1, force=force)
			cmb.setCurrentIndex(0)

			return cmb.items[index]


	def cmb003(self, index=None):
		'''Import
		'''
		cmb = self.file.cmb003

		if index is 'setMenu':
			cmb.addItems_(['Import file', 'Import Options', 'FBX Import Presets', 'Obj Import Presets'], "Import")
			return

		if index>0: #hide then perform operation
			self.tk.hide(force=1)
			if index==1: #Import
				mel.eval('Import;')
			elif index==2: #Import options
				mel.eval('ImportOptions;')
			elif index==3: #FBX Import Presets
				mel.eval('FBXUICallBack -1 editImportPresetInNewWindow fbx;') #Fbx Presets
			elif index==4: #Obj Import Presets
				mel.eval('FBXUICallBack -1 editImportPresetInNewWindow obj;') #Obj Presets
			cmb.setCurrentIndex(0)


	def cmb004(self, index=None):
		'''Export
		'''
		cmb = self.file.cmb004

		if index is 'setMenu':
			list_ = ['Export Selection', 'Send to Unreal', 'Send to Unity', 'GoZ', 'Send to 3dsMax: As New Scene', 'Send to 3dsMax: Update Current', 
					'Send to 3dsMax: Add to Current', 'Export to Offline File', 'Export Options', 'FBX Export Presets', 'Obj Export Presets']
			cmb.addItems_(list_, 'Export')
			return

		if index>0: #hide then perform operation
			self.tk.hide(force=1)
			if index==1: #Export selection
				mel.eval('ExportSelection;')
			elif index==2: #Unreal
				mel.eval('SendToUnrealSelection;')
			elif index==3: #Unity 
				mel.eval('SendToUnitySelection;')
			elif index==4: #GoZ
				mel.eval('print("GoZ"); source"C:/Users/Public/Pixologic/GoZApps/Maya/GoZBrushFromMaya.mel"; source "C:/Users/Public/Pixologic/GoZApps/Maya/GoZScript.mel";')
			elif index==5: #Send to 3dsMax: As New Scene
				mel.eval('SendAsNewScene3dsMax;') #OneClickMenuExecute ("3ds Max", "SendAsNewScene"); doMaxFlow { "sendNew","perspShape","1" };
			elif index==6: #Send to 3dsMax: Update Current
				mel.eval('UpdateCurrentScene3dsMax;') #OneClickMenuExecute ("3ds Max", "UpdateCurrentScene"); doMaxFlow { "update","perspShape","1" };
			elif index==7: #Send to 3dsMax: Add to Current
				mel.eval('AddToCurrentScene3dsMax;') #OneClickMenuExecute ("3ds Max", "AddToScene"); doMaxFlow { "add","perspShape","1" };
			elif index==8: #Export to Offline File
				mel.eval('ExportOfflineFileOptions;') #ExportOfflineFile
			elif index==9: #Export options
				mel.eval('ExportSelectionOptions;')
			elif index==10: #FBX Export Presets
				mel.eval('FBXUICallBack -1 editExportPresetInNewWindow fbx;') #Fbx Presets
			elif index==11: #Obj Export Presets
				mel.eval('FBXUICallBack -1 editExportPresetInNewWindow obj;') #Obj Presets
			cmb.setCurrentIndex(0)



	def cmb005(self, index=None):
		'''Editors
		'''
		cmb = self.file.cmb005

		if index is 'setMenu':
			list_ = []
			cmb.addItems_(list_, 'Maya File Editors')
			return

		if index>0:
			if index==cmb.items.index(''):
				mel.eval('') #
			if index==cmb.items.index(''):
				mel.eval('') #
			if index==cmb.items.index(''):
				mel.eval('') #
			cmb.setCurrentIndex(0)


	def cmb006(self, index=None):
		'''Project Folder
		'''
		cmb = self.file.cmb006

		if index is 'setMenu':
			cmb.contextMenu.add(wgts.TkComboBox, setObjectName='cmb001', setToolTip='Current project directory root.')
			cmb.contextMenu.add(wgts.TkLabel, setObjectName='lbl000', setText='Set', setToolTip='Set the project directory.')
			cmb.contextMenu.add(wgts.TkLabel, setObjectName='lbl004', setText='Root', setToolTip='Open the project directory.')
			return

		path = File.formatPath(pm.workspace(query=1, rd=1)) #current project path.
		list_ = [f for f in os.listdir(path)]

		project = File.getNameFromFullPath(path) #add current project path string to label. strip path and trailing '/'

		cmb.addItems_(list_, project, clear=True)

		if index>0:
			os.startfile(path+list_[index-1])
			cmb.setCurrentIndex(0)


	def tb000(self, state=None):
		'''Save
		'''
		tb = self.current_ui.tb000
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='Wireframe', setObjectName='chk000', setToolTip='Set view to wireframe before save.')
			tb.menu_.add('QCheckBox', setText='Increment', setObjectName='chk001', setChecked=True, setToolTip='Append and increment a unique integer value.')
			tb.menu_.add('QCheckBox', setText='Quit', setObjectName='chk002', setToolTip='Quit after save.')
			return

		wireframe = tb.menu_.chk000.isChecked()
		increment = tb.menu_.chk001.isChecked()
		quit = tb.menu_.chk002.isChecked()

		if wireframe:
			pm.mel.DisplayWireframe()

		if increment:
			pm.mel.IncrementAndSave()

		if quit: #quit maya
			import time
			for timer in range(5):
				self.viewPortMessage('Shutting Down:<hl>'+str(timer)+'</hl>')
				time.sleep(timer)
			pm.mel.quit() # pm.Quit()


	def lbl000(self):
		'''Set Project
		'''
		newProject = mel.eval("SetProject;")

		self.cmb006() #refresh cmb006 items to reflect new project folder


	def lbl001(self):
		'''Minimize Main Application
		'''
		mel.eval("minimizeApp;")
		self.tk.hide(force=1)


	def lbl002(self):
		'''Restore Main Application
		'''
		pass


	def lbl003(self):
		'''Close Main Application
		'''
		# force=false #pymel has no attribute quit error.
		# exitcode=""
		sceneName = str(mel.eval("file -query -sceneName -shortName;")) #if sceneName prompt user to save; else force close
		mel.eval("quit;") if sceneName else mel.eval("quit -f;")
		# pm.quit (force=force, exitcode=exitcode)


	def lbl004(self):
		'''Open current project root
		'''
		dir_ = pm.workspace(query=1, rd=1) #current project path.
		os.startfile(File.formatPath(dir_))


	def b001(self):
		'''Recent Files: Open Last
		'''
		# files = [file_ for file_ in (list(reversed(pm.optionVar(query='RecentFilesList')))) if "Autosave" not in file_]

		# force=True
		# if str(mel.eval("file -query -sceneName -shortName;")):
		# 	force=False #if sceneName, prompt user to save; else force open
		# pm.openFile(files[0], open=1, force=force)

		self.cmb000(index=1)
		self.tk.hide(force=1)


	def b007(self):
		'''Import file
		'''
		self.cmb003(index=1)


	def b008(self):
		'''Export Selection
		'''
		self.cmb004(index=1)


	def b015(self):
		'''Remove String From Object Names.
		'''
		from_ = str(self.file.t000.text()) #asterisk denotes startswith*, *endswith, *contains* 
		to = str(self.file.t001.text())
		replace = self.file.chk004.isChecked()
		selected = self.file.chk005.isChecked()

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


	@staticmethod
	def getAbsoluteFilePaths(directory, endingWith=['mb', 'ma']):
		'''Get the absolute paths of all the files in a directory and it's sub-folders.

		directory (str) = Root directory path.
		endingWith (list) = Extension types (as strings) to include. ex. ['mb', 'ma']
		
		:Return:
			(list) absolute file paths
		'''
		paths=[]
		for dirpath, _, filenames in os.walk(directory):
			for f in filenames:
				if f.split('.')[-1] in endingWith:
					paths.append(os.path.abspath(os.path.join(dirpath, f)))

		return paths


	@staticmethod
	def formatPath(dir_):
		'''Assure a given directory path string is formatted correctly.
		Replace any backslashes with forward slashes.
		'''
		formatted_dir = dir_.replace('/', '\\') #assure any single slash is forward.

		return formatted_dir


	@staticmethod
	def getNameFromFullPath(fullPath):
		'''Extract the file or dir name from a path string.

		:Parameters:
			fullPath (str) = A full path including file name.

		:Return:
			(str) the dir or file name including extension.
		'''
		name = fullPath.split('/')[-1]
		if len(fullPath)==len(name):
			name = fullPath.split('\\')[-1]
			if not name:
				name = fullPath.split('\\')[-2]

		return name









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------



# deprecated:


	# def tb000(self, state=None):
	# 	'''
	# 	Save
	# 	'''
	# 	tb = self.current_ui.tb000
	# 	if state is 'setMenu':
	# 		tb.menu_.add('QCheckBox', setText='ASCII', setObjectName='chk003', setChecked=True, setToolTip='Toggle ASCII or binary file type.')
	# 		tb.menu_.add('QCheckBox', setText='Wireframe', setObjectName='chk000', setChecked=True, setToolTip='Set view to wireframe before save.')
	# 		tb.menu_.add('QCheckBox', setText='Increment', setObjectName='chk001', setChecked=True, setToolTip='Append and increment a unique integer value.')
	# 		tb.menu_.add('QCheckBox', setText='Quit', setObjectName='chk002', setToolTip='Quit after save.')
	# 		return

	# 	increment = tb.menu_.chk001.isChecked()
	# 	ASCII = tb.menu_.chk003.isChecked()
	# 	wireframe = tb.menu_.chk000.isChecked()
	# 	quit = tb.menu_.chk002.isChecked()

	# 	preSaveScript = ''
	# 	postSaveScript = ''

	# 	type_ = 'mayaBinary'
	# 	if ASCII: #toggle ascii/ binary
	# 		type_ = 'mayaAscii' #type: mayaAscii, mayaBinary, mel, OBJ, directory, plug-in, audio, move, EPS, Adobe(R) Illustrator(R)

	# 	if wireframe:
	# 		mel.eval('DisplayWireframe;')

	# 	#get scene name and file path
	# 	fullPath = str(mel.eval('file -query -sceneName;')) #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.maya/elise_mid.009.mb
	# 	index = fullPath.rfind('/')+1
	# 	curFullName = fullPath[index:] #ie. elise_mid.009.mb
	# 	path = fullPath[:index] #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.maya/

	# 	if increment: #increment filename
	# 		newName = File.incrementFileName(curFullName)
	# 		File.deletePreviousFiles(curFullName, path)
	# 		pm.saveAs (path+newName, force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
	# 		print('{0} {1}'.format('Result:', path+newName))
	# 	else:	#save without renaming
	# 		pm.saveFile (force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
	# 		print('{0} {1}'.format('Result:', path+currentName,))

	# 	if quit: #quit maya
	# 		import time
	# 		for timer in range(5):
	# 			self.viewPortMessage('Shutting Down:<hl>'+str(timer)+'</hl>')
	# 			time.sleep(timer)
	# 		mel.eval("quit;")
	# 		# pm.Quit()


	# @staticmethod
	# def incrementFileName(fileName):
	# 	'''
	# 	Increment the given file name.

	# 	:Parameters:
	# 		fileName (str) = file name with extension. ie. elise_mid.ma

	# 	:Return:
	# 		(str) incremented name. ie. elise_mid.000.ma
	# 	'''
	# 	import re

	# 	#remove filetype extention
	# 	currentName = fileName[:fileName.rfind('.')] #name without extension ie. elise_mid.009 from elise_mid.009.mb
	# 	#get file number
	# 	numExt = re.search(r'\d+$', currentName) #check if the last chars are numberic
	# 	if numExt is not None:
	# 		name = currentName[:currentName.rfind('.')] #strip off the number ie. elise_mid from elise_mid.009
	# 		num = int(numExt.group())+1 #get file number and add 1 ie. 9 becomes 10
	# 		prefix = '000'[:-len(str(num))]+str(num) #prefix '000' removing zeros according to num length ie. 009 becomes 010
	# 		newName = name+'.'+prefix #ie. elise_mid.010
			
	# 	else:
	# 		newName = currentName+'.001'

	# 	return newName


	# @staticmethod
	# def deletePreviousFiles(fileName, path, numberOfPreviousFiles=5):
	# 	'''
	# 	Delete older files.

	# 	:Parameters:
	# 		fileName (str) = file name with extension. ie. elise_mid.ma
	# 		numberOfPreviousFiles (int) = Number of previous copies to keep.
	# 	'''
	# 	import re, os

	# 	#remove filetype extention
	# 	currentName = fileName[:fileName.rfind('.')] #name without extension ie. elise_mid.009 from elise_mid.009.mb
	# 	#get file number
	# 	numExt = re.search(r'\d+$', currentName) #check if the last chars are numberic
	# 	if numExt is not None:
	# 		name = currentName[:currentName.rfind('.')] #strip off the number ie. elise_mid from elise_mid.009
	# 		num = int(numExt.group())+1 #get file number and add 1 ie. 9 becomes 10

	# 		oldNum = num-numberOfPreviousFiles
	# 		oldPrefix = '000'[:-len(str(oldNum))]+str(oldNum) #prefix the appropriate amount of zeros in front of the old number
	# 		oldName = name+'.'+oldPrefix #ie. elise_mid.007
	# 		try: #search recursively through the project folder and delete any old folders with the old filename
	# 			dir_ =  os.path.abspath(os.path.join(path, "../.."))
	# 			for root, directories, files in os.walk(dir_):
	# 				for filename in files:
	# 					if all([filename==oldName+ext for ext in ('.ma','.ma.swatches','.mb','.mb.swatches')]):
	# 						try:
	# 							import os
	# 							os.remove(filename)
	# 						except:
	# 							pass
	# 		except OSError:
	# 			print('{0} {1}'.format('Error: Could not delete', path+oldName))
	# 			pass