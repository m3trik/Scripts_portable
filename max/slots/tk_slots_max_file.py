from tk_slots_max_init import *


from datetime import datetime
import os.path
from widgets.qWidget_MultiWidget import QWidget_MultiWidget as MultiWidget


class File(Init):
	def __init__(self, *args, **kwargs):
		super(File, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('file')

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


	def cmb000(self, index=None):
		'''
		Recent Files
		'''
		cmb = self.ui.cmb000

		list_ = rt.getRecentfiles()
		contents = cmb.addItems_(list_, "Recent Files")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			# force=True; force if maxEval("maxFileName;") else not force #if sceneName prompt user to save; else force open.  also: checkForSave(); If the scene has been modified since the last file save (if any), calling this function displays the message box prompting the user that the scene has been modified and requests to save.
			rt.loadMaxFile(str(contents[index]))
			cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Recent Projects
		'''
		cmb = self.ui.cmb001

		path = ''
		list_ = []#[f for f in os.listdir(path)]

		contents = cmb.addItems_(list_, "Recent Projects")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			maxEval('setProject "'+contents[index]+'"')
			cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Recent Autosave
		'''
		cmb = self.ui.cmb002

		path = MaxPlus.PathManager.GetAutobackDir()
		files = [f for f in os.listdir(path) if f.endswith('.max') or f.endswith('.bak')] #get list of max autosave files

		list_ = [f+'  '+datetime.fromtimestamp(os.path.getmtime(path+'\\'+f)).strftime('%H:%M  %m-%d-%Y') for f in files] #attach modified timestamp

		contents = cmb.addItems_(sorted(list_, reverse=1), "Recent Autosave")

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			rt.loadMaxFile(path+'\\'+str(files[index-1]))
			cmb.setCurrentIndex(0)


	def cmb003(self, index=None):
		'''
		Import
		'''
		cmb = self.ui.cmb003

		contents = cmb.addItems_(['Import file', 'Import Options', 'Merge', 'Replace', 'Link Revit', 'Link FBX', 'Link AutoCAD'], 'Import')

		if not index:
			index = cmb.currentIndex()
		if index!=0: #hide then perform operation
			print index
			self.tk.hide(force=1)
			if index == 1: #Import
				maxEval('max file import')
			if index == 2: #Import options
				maxEval('')
			if index == 3: #Merge
				maxEval('max file merge')
			if index == 4: #Replace
				maxEval('max file replace')
			if index == 5: #Manage Links: Link Revit File
				maxEval('actionMan.executeAction 769996349 "108"')
			if index == 6: #Manage Links: Link FBX File
				maxEval('actionMan.executeAction 769996349 "109"')
			if index == 7: #Manage Links: Link AutoCAD File
				maxEval('actionMan.executeAction 769996349 "110"')
			cmb.setCurrentIndex(0)


	def cmb004(self, index=None):
		'''
		Export
		'''
		cmb = self.ui.cmb004

		list_ = ["Export Selection", "Export Options", "Unreal", "Unity", "GoZ", "Send to Maya: New Scene", "Send to Maya: Update Scene", "Send to Maya: Add to Scene"]

		cmb.addItems_(list_, "Export")

		if not index:
			index = cmb.currentIndex()
		if index !=0: #hide then perform operation
			self.tk.hide(force=1)
			if index==1: #Export selection
				maxEval('max file export')
			if index==2: #Export options
				maxEval('')
			if index==3: #Unreal: File: Game Exporter
				maxEval('actionMan.executeAction 0 "40488"')
			if index==4: #Unity: File: Game Exporter
				maxEval('actionMan.executeAction 0 "40488"')
			if index==5: #GoZ
				print 'GoZ'
				maxEval(''' 
					try (
						if (s_verbose) then print "\n === 3DS -> ZBrush === "
						local result = s_gozServer.GoToZBrush()
						) catch ();
					''')
			if index==6: #One Click Maya: Send as New Scene to Maya
				maxEval('actionMan.executeAction 924213374 "0"')
			if index==7: #One Click Maya: Update Current Scene in Maya
				maxEval('actionMan.executeAction 924213374 "1"')
			if index==8: #One Click Maya: Add to Current Scene in Maya
				maxEval('actionMan.executeAction 924213374 "2"')

			cmb.setCurrentIndex(0)


	def cmb005(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb005

		files = ['Schematic View']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Schematic View'):
				maxEval('schematicView.Open "Schematic View 1"')
			cmb.setCurrentIndex(0)


	def cmb006(self, index=None):
		'''
		Project Folder
		'''
		cmb = self.ui.cmb006

		path = MaxPlus.PathManager.GetProjectFolderDir() #current project path.
		list_ = [f for f in os.listdir(path)]

		project = MaxPlus.PathManager.GetProjectFolderDir().split('\\')[-1] #add current project path string to label. strip path and trailing '/'

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
		tb = self.ui.tb000
		if state=='setMenu':
			tb.add('QCheckBox', setText='ASCII', setObjectName='chk003', setChecked=True, setToolTip='Toggle ASCII or binary file type.')
			tb.add('QCheckBox', setText='Wireframe', setObjectName='chk000', setChecked=True, setToolTip='Set view to wireframe before save.')
			tb.add('QCheckBox', setText='Increment', setObjectName='chk001', setChecked=True, setToolTip='Append and increment a unique integer value.')
			tb.add('QCheckBox', setText='Quit', setObjectName='chk002', setToolTip='Quit after save.')
			return

		preSaveScript = ""
		postSaveScript = ""

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
									os.remove(filename)
								except:
									pass
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

		if tb.chk002.isChecked(): #quit
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
		# files = rt.getRecentfiles()
		# rt.loadMaxFile(str(files[0]))

		self.tk.hide(force=1)
		self.cmb000(index=1)


	def b002(self):
		'''
		Fbx Presets
		'''
		maxEval('FBXUICallBack -1 editExportPresetInNewWindow fbx;')


	def b003(self):
		'''
		Obj Presets
		'''
		maxEval('FBXUICallBack -1 editExportPresetInNewWindow obj;')


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
		app = rt.createOLEObject('Shell.Application')
		maxEval('minimizeAll app')
		maxEval('undoMinimizeAll app')
		rt.releaseOLEObject(app)
		self.tk.hide(force=1)


	def b006(self):
		'''
		Restore Main Application
		'''
		pass


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
		try:
			MaxPlus.PathManager.SetProjectFolderDir()
		except:
			maxEval('macros.run "Tools" "SetProjectFolder"')

		self.cmb006() #refresh cmb006 contents to reflect new project folder






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------