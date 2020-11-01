from __future__ import print_function
from tk_slots_max_init import *

from datetime import datetime
import os.path



class File(Init):
	def __init__(self, *args, **kwargs):
		super(File, self).__init__(*args, **kwargs)


		#get recent file list. #convert to python
		maxEval('''
		Fn getRecentFiles =
			(
			local recentfiles = (getdir #maxData) + "RecentDocuments.xml"
			if doesfileexist recentfiles then
				(
				XMLArray = #()		
				xDoc = dotnetobject "system.xml.xmldocument"	
				xDoc.Load recentfiles
				Rootelement = xDoc.documentelement

				XMLArray = for i = 0 to rootelement.childnodes.item[4].childnodes.itemof[0].childnodes.count-1 collect 
					(
					rootelement.childnodes.item[4].childnodes.itemof[0].childnodes.itemof[i].childnodes.itemof[3].innertext	
					)
					
				Return XMLArray
				LRXML = Undefined
				XDoc = Undefined
				XDoc = nothing	
				)
			)
			''')


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.file.pin

		if state is 'setMenu':
			pin.contextMenu.add(QComboBox_, setObjectName='cmb005', setToolTip='')
			pin.contextMenu.add(QToolButton_, setObjectName='tb000', setText='Save', setToolTip='')
			pin.contextMenu.add(QLabel_, setObjectName='lbl001', setText='Minimize App', setToolTip='Minimize the main application.')
			pin.contextMenu.add(QLabel_, setObjectName='lbl002', setText='Maximize App', setToolTip='Restore the main application.')
			pin.contextMenu.add(QLabel_, setObjectName='lbl003', setText='Close App', setToolTip='Close the main application.')
			return


	def cmb000(self, index=None):
		'''
		Recent Files
		'''
		cmb = self.file.cmb000

		if index is 'setMenu':
			cmb.contextMenu.add('QPushButton', setObjectName='b001', setText='Last', setToolTip='Open the most recent file.')
			return

		recentFiles = [File.formatPath(f) for f in rt.getRecentfiles()]
		items = cmb.addItems_(recentFiles, 'Recent Files:', clear=True)

		#set the text for the open last file button to the last file's name.
		self.file_submenu.b001.setText(File.getNameFromFullPath(recentFiles[0])) if recentFiles else self.file_submenu.b001.setVisible(False)

		if index>0:
			# force=True; force if maxEval("maxFileName;") else not force #if sceneName prompt user to save; else force open.  also: checkForSave(); If the scene has been modified since the last file save (if any), calling this function displays the message box prompting the user that the scene has been modified and requests to save.
			rt.loadMaxFile(str(items[index]))
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Recent Projects
		'''
		cmb = self.file.cmb001

		if index is 'setMenu':
			return

		path = ''
		list_ = []#[f for f in os.listdir(path)]

		items = cmb.addItems_(list_, "Recent Projects", clear=True)

		if index>0:
			maxEval('setProject "'+items[index]+'"')
			cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Recent Autosave
		'''
		cmb = self.file.cmb002

		if index is 'setMenu':
			return

		path = MaxPlus.PathManager.GetAutobackDir()
		files = [f for f in os.listdir(path) if f.endswith('.max') or f.endswith('.bak')] #get list of max autosave files

		list_ = [f+'  '+datetime.fromtimestamp(os.path.getmtime(path+'\\'+f)).strftime('%H:%M  %m-%d-%Y') for f in files] #attach modified timestamp
		items = cmb.addItems_(sorted(list_, reverse=1), "Recent Autosave", clear=True)

		if index>0:
			rt.loadMaxFile(path+'\\'+str(files[index-1]))
			cmb.setCurrentIndex(0)


	def cmb003(self, index=None):
		'''
		Import
		'''
		cmb = self.file.cmb003

		if index is 'setMenu':
			cmb.addItems_(['Import file', 'Import Options', 'Merge', 'Replace', 'Link Revit', 'Link FBX', 'Link AutoCAD'], 'Import')
			return

		if index>0: #hide then perform operation
			self.tk.hide(force=1)
			if index == 1: #Import
				maxEval('max file import')
			elif index == 2: #Import options
				maxEval('')
			elif index == 3: #Merge
				maxEval('max file merge')
			elif index == 4: #Replace
				maxEval('max file replace')
			elif index == 5: #Manage Links: Link Revit File
				maxEval('actionMan.executeAction 769996349 "108"')
			elif index == 6: #Manage Links: Link FBX File
				maxEval('actionMan.executeAction 769996349 "109"')
			elif index == 7: #Manage Links: Link AutoCAD File
				maxEval('actionMan.executeAction 769996349 "110"')
			cmb.setCurrentIndex(0)


	def cmb004(self, index=None):
		'''
		Export
		'''
		cmb = self.file.cmb004

		if index is 'setMenu':
			list_ = ["Export Selection", "Export Options", "Unreal", "Unity", "GoZ", "Send to Maya: New Scene", "Send to Maya: Update Scene", "Send to Maya: Add to Scene"]
			cmb.addItems_(list_, "Export")
			return

		if index>0: #hide then perform operation
			self.tk.hide(force=1)
			if index==1: #Export selection
				maxEval('actionMan.executeAction 0 "40373"') #max file export
			elif index==2: #Export options
				maxEval('')
			elif index==3: #Unreal: File: Game Exporter
				maxEval('actionMan.executeAction 0 "40488"')
			elif index==4: #Unity: File: Game Exporter
				maxEval('actionMan.executeAction 0 "40488"')
			elif index==5: #GoZ
				print('GoZ')
				maxEval(''' 
					try (
						if (s_verbose) then print "\n === 3DS -> ZBrush === "
						local result = s_gozServer.GoToZBrush()
						) catch ();
					''')
			elif index==6: #One Click Maya: Send as New Scene to Maya
				maxEval('actionMan.executeAction 924213374 "0"')
			elif index==7: #One Click Maya: Update Current Scene in Maya
				maxEval('actionMan.executeAction 924213374 "1"')
			elif index==8: #One Click Maya: Add to Current Scene in Maya
				maxEval('actionMan.executeAction 924213374 "2"')

			cmb.setCurrentIndex(0)


	def cmb005(self, index=None):
		'''
		Editors
		'''
		cmb = self.file.cmb005

		if index is 'setMenu':
			list_ = ['Schematic View']
			cmb.addItems_(list_, '3dsMax File Editors')
			return

		if index>0:
			if index==cmb.items.index('Schematic View'):
				maxEval('schematicView.Open "Schematic View 1"')
			cmb.setCurrentIndex(0)


	def cmb006(self, index=None):
		'''
		Project Folder
		'''
		cmb = self.file.cmb006

		if index is 'setMenu':
			cmb.contextMenu.add(QComboBox_, setObjectName='cmb001', setToolTip='Current project directory root.')
			cmb.contextMenu.add(QLabel_, setObjectName='lbl000', setText='Set', setToolTip='Set the project directory.')
			cmb.contextMenu.add(QLabel_, setObjectName='lbl004', setText='Root', setToolTip='Open the project directory.')
			return

		path = File.formatPath(MaxPlus.PathManager.GetProjectFolderDir()) #current project path.
		list_ = [f for f in os.listdir(path)]

		project = File.getNameFromFullPath(path) #add current project path string to label. strip path and trailing '/'

		cmb.addItems_(list_, project, clear=True)

		if index>0:
			dir_ = path+list_[index-1] #reformat for network address
			os.startfile(dir_)
			cmb.setCurrentIndex(0)


	def tb000(self, state=None):
		'''
		Save
		'''
		tb = self.currentUi.tb000
		if state is 'setMenu':
			tb.menu_.add('QCheckBox', setText='ASCII', setObjectName='chk003', setChecked=True, setToolTip='Toggle ASCII or binary file type.')
			tb.menu_.add('QCheckBox', setText='Wireframe', setObjectName='chk000', setChecked=True, setToolTip='Set view to wireframe before save.')
			tb.menu_.add('QCheckBox', setText='Increment', setObjectName='chk001', setChecked=True, setToolTip='Append and increment a unique integer value.')
			tb.menu_.add('QCheckBox', setText='Quit', setObjectName='chk002', setToolTip='Quit after save.')
			return

		increment = tb.menu_.chk001.isChecked()
		ASCII = tb.menu_.chk003.isChecked()
		wireframe = tb.menu_.chk000.isChecked()
		quit = tb.menu_.chk002.isChecked()

		preSaveScript = ''
		postSaveScript = ''

		type_ = 'mayaBinary'
		if ASCII: #toggle ascii/ binary
			type_ = 'mayaAscii' #type: mayaAscii, mayaBinary, mel, OBJ, directory, plug-in, audio, move, EPS, Adobe(R) Illustrator(R)

		if wireframe:
			mel.eval('DisplayWireframe;')

		#get scene name and file path
		fullPath = str(mel.eval('file -query -sceneName;')) #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.maya/elise_mid.009.mb
		index = fullPath.rfind('/')+1
		curFullName = fullPath[index:] #ie. elise_mid.009.mb
		path = fullPath[:index] #ie. O:/Cloud/____Graphics/______project_files/elise.proj/elise.scenes/.maya/

		if increment: #increment filename
			newName = File.incrementFileName(curFullName)
			File.deletePreviousFiles(curFullName, path)
			pm.saveAs (path+newName, force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
			print('{0} {1}'.format('Result:', path+newName))
		else:	#save without renaming
			pm.saveFile (force=1, preSaveScript=preSaveScript, postSaveScript=postSaveScript, type=type_)
			print('{0} {1}'.format('Result:', path+currentName,))

		if quit: #quit maya
			import time
			for timer in range(5):
				self.viewPortMessage('Shutting Down:<hl>'+str(timer)+'</hl>')
				time.sleep(timer)
			mel.eval("quit;")
			# pm.Quit()


	@staticmethod
	def incrementFileName(fileName):
		'''
		Increment the given file name.

		args:
			fileName (str) = file name with extension. ie. elise_mid.ma

		returns:
			(str) incremented name. ie. elise_mid.000.ma
		'''
		import re

		#remove filetype extention
		currentName = fileName[:fileName.rfind('.')] #name without extension ie. elise_mid.009 from elise_mid.009.mb
		#get file number
		numExt = re.search(r'\d+$', currentName) #check if the last chars are numberic
		if numExt is not None:
			name = currentName[:currentName.rfind('.')] #strip off the number ie. elise_mid from elise_mid.009
			num = int(numExt.group())+1 #get file number and add 1 ie. 9 becomes 10
			prefix = '000'[:-len(str(num))]+str(num) #prefix '000' removing zeros according to num length ie. 009 becomes 010
			newName = name+'.'+prefix #ie. elise_mid.010
			
		else:
			newName = currentName+'.001'

		return newName


	@staticmethod
	def deletePreviousFiles(fileName, path, numberOfPreviousFiles=5):
		'''
		Delete older files.

		args:
			fileName (str) = file name with extension. ie. elise_mid.ma
			numberOfPreviousFiles (int) = Number of previous copies to keep.
		'''
		import re, os

		#remove filetype extention
		currentName = fileName[:fileName.rfind('.')] #name without extension ie. elise_mid.009 from elise_mid.009.mb
		#get file number
		numExt = re.search(r'\d+$', currentName) #check if the last chars are numberic
		if numExt is not None:
			name = currentName[:currentName.rfind('.')] #strip off the number ie. elise_mid from elise_mid.009
			num = int(numExt.group())+1 #get file number and add 1 ie. 9 becomes 10

			oldNum = num-numberOfPreviousFiles
			oldPrefix = '000'[:-len(str(oldNum))]+str(oldNum) #prefix the appropriate amount of zeros in front of the old number
			oldName = name+'.'+oldPrefix #ie. elise_mid.007
			try: #search recursively through the project folder and delete any old folders with the old filename
				dir_ =  os.path.abspath(os.path.join(path, "../.."))
				for root, directories, files in os.walk(dir_):
					for filename in files:
						if all([filename==oldName+ext for ext in ('.ma','.ma.swatches','.mb','.mb.swatches')]):
							try:
								import os
								os.remove(filename)
							except:
								pass
			except OSError:
				print('{0} {1}'.format('Error: Could not delete', path+oldName))
				pass


	def lbl000(self):
		'''
		Set Project
		'''
		try:
			MaxPlus.PathManager.SetProjectFolderDir()
		except:
			maxEval('macros.run "Tools" "SetProjectFolder"')

		self.cmb006() #refresh cmb006 items to reflect new project folder


	def lbl001(self):
		'''
		Minimize Main Application
		'''
		app = rt.createOLEObject('Shell.Application')
		maxEval('minimizeAll app')
		maxEval('undoMinimizeAll app')
		rt.releaseOLEObject(app)
		self.tk.hide(force=1)


	def lbl002(self):
		'''
		Restore Main Application
		'''
		pass


	def lbl003(self):
		'''
		Close Main Application
		'''
		# force=false #pymel has no attribute quit error.
		# exitcode=""
		# sceneName = str(mel.eval("file -query -sceneName -shortName;")) #if sceneName prompt user to save; else force close
		# mel.eval("quit;") if sceneName else mel.eval("quit -f;")
		# pm.quit (force=force, exitcode=exitcode)


	def lbl004(self):
		'''
		Open current project root
		'''
		dir_ = rt.getRecentfiles() #current project path.
		dir_ = File.formatPath(dir_) #reformat for network address
		os.startfile(dir_)


	def b001(self):
		'''
		Recent Files: Open Last
		'''
		# files = rt.getRecentfiles()
		# rt.loadMaxFile(str(files[0]))

		self.cmb000(index=1)
		self.tk.hide(force=1)


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
		from_ = str(self.file.t000.text()) #asterisk denotes startswith*, *endswith, *contains* 
		to = str(self.file.t001.text())
		replace = self.file.chk004.isChecked()
		selected = self.file.chk005.isChecked()

		# objects = pm.ls (from_) #Stores a list of all objects starting with 'from_'
		# if selected:
		# 	objects = pm.ls (selection=1) #if use selection option; get user selected objects instead
		# from_ = from_.strip('*') #strip modifier asterisk from user input

		# for obj in objects:
		# 	relatives = pm.listRelatives(obj, parent=1) #Get a list of it's direct parent
		# 	if 'group*' in relatives: #If that parent starts with group, it came in root level and is pasted in a group, so ungroup it
		# 		relatives[0].ungroup()

		# 	newName = to
		# 	if replace:
		# 		newName = obj.replace(from_, to)
		# 	pm.rename(obj, newName) #Rename the object with the new name


	@staticmethod
	def formatPath(dir_):
		'''
		Assure a given directory path string is formatted correctly.
		Replace any backslashes with forward slashes.
		'''
		formatted_dir = dir_.replace('/', '\\') #assure any single slash is forward.

		return formatted_dir


	@staticmethod
	def getNameFromFullPath(fullPath):
		'''
		Extract the file or dir name from a path string.

		args:
			fullPath (str) = A full path including file name.

		returns:
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