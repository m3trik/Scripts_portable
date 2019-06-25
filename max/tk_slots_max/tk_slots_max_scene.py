import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os
from datetime import datetime

from tk_slots_max_init import Init




class Scene(Init):
	def __init__(self, *args, **kwargs):
		super(Scene, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('scene')

		self.ui.t000.returnPressed.connect(self.t001) #preform rename on returnPressed

		self.cmb006() #refresh cmb006 contents to reflect the current project folder


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


	def getTrailingIntegers(self, string, increment=0):
		'''
		args: increment=int - optional step amount

		Returns 'string' - any integers from the end of the given string.
		'''
		num='' #get trailing integers
		for char in reversed(str(string)): #work from the back of the string
			if str.isdigit(char):
				num = num+char
			else: #when a non-integer char is found return any integers as a string.
				if not num:
					num='0'
				num = int(num[::-1])+increment #re-reverse the string and increment.
				return '000'[:-len(str(num))]+str(num) #prefix '000' removing zeros according to num length ie. 009 becomes 010


	def t001(self):
		'''
		Rename

		*find* - search contains chars
		*find - search endswith chars
		find* - search startswith chars
		find|find - search any of.  can be used in conjuction with other modifiers

		*to* - replace only 'find'
		*to - replace suffix
		to* - replace prefix
		**to - replace suffix', moves any integers in front of replacement chars
		'''
		find = str(self.ui.t000.text()) #asterisk denotes startswith*, *endswith, *contains* 
		to = str(self.ui.t001.text())


		if rt.selection: #if selection; operate on only the selected objects.
			lists = [[o for o in rt.selection if rt.matchPattern(o.name, pattern=f, ignoreCase=0)] for f in find.split('|')] #objects in current selection that match criteria
		else:
			lists = [[o for o in rt.objects if rt.matchPattern(o.name, pattern=f, ignoreCase=0)] for f in find.split('|')] #all objects that match criteria
		objects = set([i for sublist in lists for i in sublist]) #flatten and remove any duplicates.


		for obj in objects:
			f = [f for f in find.split('|') if f.strip('*') in obj.name][0] #get the objects that contain the chars in find.split('|')
			
			# relatives = pm.listRelatives(obj.name, parent=1) #Get a list of it's direct parent
			# if 'group*' in relatives: #If that parent starts with group, it came in root level and is pasted in a group, so ungroup it
			# 	relatives[0].ungroup()

			#find modifiers
			if to.startswith('*') and to.endswith('*'): #replace chars
				f = f.replace('*', '') #remove modifiers
				newName = obj.name.replace(f, to)

			elif to.startswith('*'): #replace suffix
				newName = obj.name+to

			elif to.endswith('*'): #replace prefix
				f = f.replace('*', '') #remove modifiers
				newName = obj.name.replace(f, to, 1) #1=replace only the first occurance

			elif to.startswith('**'): #replace suffix and move any trailing integers
				num = self.getTrailingIntegers(obj.name)
				stripped = obj.name.rstrip(f+'0123456789')
				newName = stripped+num+to

			else: #replace whole name
				newName = rt.uniqueName(to.replace('*', ''))

			newName = newName.replace('*', '') #remove modifiers
			while [o for o in rt.objects if o.name==newName]:
				num = self.getTrailingIntegers(newName, increment=1)
				newName = newName.rstrip('0123456789')+num

			obj.name = newName #Rename the object with the new name


	def cmb000(self):
		'''
		Recent Files

		'''
		cmb = self.ui.cmb000
		
		list_ = rt.getRecentfiles()
		contents = self.comboBox (cmb, list_, "Recent Files")

		index = cmb.currentIndex()
		if index!=0:
			# force=True; force if maxEval("maxFileName;") else not force #if sceneName prompt user to save; else force open.  also: checkForSave(); If the scene has been modified since the last file save (if any), calling this function displays the message box prompting the user that the scene has been modified and requests to save.
			rt.loadMaxFile(str(contents[index]))
			self.hotBox.hide_()
			cmb.setCurrentIndex(0)


	def cmb001(self):
		'''
		Recent Projects

		'''
		cmb = self.ui.cmb001
		
		path = ''
		list_ = []#[f for f in os.listdir(path)]

		contents = self.comboBox (cmb, list_, "Recent Projects")

		index = cmb.currentIndex()
		if index!=0:
			maxEval('setProject "'+contents[index]+'"')
			cmb.setCurrentIndex(0)


	def cmb002(self):
		'''
		Recent Autosave

		'''
		cmb = self.ui.cmb002
		
		path = MaxPlus.PathManager.GetAutobackDir()
		files = [f for f in os.listdir(path) if f.endswith('.max') or f.endswith('.bak')] #get list of max autosave files

		list_ = [f+'  '+datetime.fromtimestamp(os.path.getmtime(path+'\\'+f)).strftime('%H:%M  %m-%d-%Y') for f in files] #attach modified timestamp
		list_ = sorted(list_, reverse=1)
		
		contents = self.comboBox (cmb, list_, "Recent Autosave")

		index = cmb.currentIndex()
		if index!=0:
			rt.loadMaxFile(path+'\\'+str(files[index-1]))
			self.hotBox.hide_()
			cmb.setCurrentIndex(0)


	def cmb003(self):
		'''
		Import

		'''
		cmb = self.ui.cmb003
		
		contents = self.comboBox (cmb, ["Import file", "Import Options"], "Import")
		
		index = cmb.currentIndex()
		if index!=0: #hide hotBox then perform operation
			self.hotBox.hide_()
			if index == 1: #Import
				maxEval('Import;')
			if index == 2: #Import options
				maxEval('ImportOptions;')
			cmb.setCurrentIndex(0)


	def cmb004(self):
		'''
		Export

		'''
		cmb = self.ui.cmb004
		
		list_ = ["Export Selection", "Export Options", "Unreal", "Unity", "GoZ", "Send to Maya: New Scene", "Send to Maya: Update Scene", "Send to Maya: Add to Scene"]

		self.comboBox (cmb, list_, "Export")

		index = cmb.currentIndex()
		if index !=0: #hide hotBox then perform operation
			self.hotBox.hide_()
			if index==1: #Export selection
				maxEval('ExportSelection;')
			if index==2: #Export options
				maxEval('ExportSelectionOptions;')
			if index==3: #Unreal
				maxEval('SendToUnrealSelection;')
			if index==4: #Unity 
				maxEval('SendToUnitySelection;')
			if index==5: #GoZ
				print 'GoZ'
				maxEval(''' 
					try (
						if (s_verbose) then print "\n === 3DS -> ZBrush === "
						local result = s_gozServer.GoToZBrush()
						) catch ();
					''')
			if index==6: #sent to maya: new scene
				maxEval('actionMan.executeAction 924213374 "0"  -- One Click Maya: Send as New Scene to Maya')
			if index==7: #sent to maya: update scene
				maxEval('actionMan.executeAction 924213374 "1"  -- One Click Maya: Update Current Scene in Maya')
			if index==8: #sent to maya: add to scene
				maxEval('actionMan.executeAction 924213374 "2"  -- One Click Maya: Add to Current Scene in Maya')
			
			cmb.setCurrentIndex(0)


	def cmb005(self):
		'''
		Editors

		'''
		cmb = self.ui.cmb005
		
		files = ['Schematic View']
		contents = self.comboBox (cmb, files, "Editors")

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Schematic View'):
				maxEval('schematicView.Open "Schematic View 1"')
			cmb.setCurrentIndex(0)


	def cmb006(self):
		'''
		Project Folder

		'''
		cmb = self.ui.cmb006
		
		path = MaxPlus.PathManager.GetProjectFolderDir() #current project path.
		list_ = [f for f in os.listdir(path)]

		project = MaxPlus.PathManager.GetProjectFolderDir().split('\\')[-1] #add current project path string to label. strip path and trailing '/'

		contents = self.comboBox (cmb, list_, project)

		index = cmb.currentIndex()
		if index!=0:
			dir_= path+list_[index-1]
			os.startfile(dir_)
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
								self.try_('os.remove(filename)')
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
		Recent Files: Open Last
		'''
		files = rt.getRecentfiles()
		
		rt.loadMaxFile(str(files[0]))
		self.hotBox.hide_()


	def b002(self):
		'''
		

		'''
		pass


	def b003(self):
		'''
		

		'''
		pass


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