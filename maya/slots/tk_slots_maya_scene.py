from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Scene(Init):
	def __init__(self, *args, **kwargs):
		super(Scene, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('scene')
		self.childUi = self.sb.getUi('scene_submenu')

		self.parentUi.t000.returnPressed.connect(self.t001) #preform rename on returnPressed


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state is 'setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='Maya Scene Editors')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000

		if index is 'setMenu':
			list_ = ['Node Editor', 'Outlinder', 'Content Browser', 'Optimize Scene Size', 'Prefix Hierarchy Names', 'Search and Replace Names']
			cmb.addItems_(list_, 'Maya Scene Editors')
			return

		if index>0:
			if index==contents.index('Node Editor'):
				mel.eval('NodeEditorWindow;') #
			elif index==contents.index('Outlinder'):
				mel.eval('OutlinerWindow;') #
			elif index==contents.index('Content Browser'):
				mel.eval('ContentBrowserWindow;') #
			elif index==contents.index('Optimize Scene Size'):
				mel.eval('cleanUpScene 2;')
			elif index==contents.index('Prefix Hierarchy Names'):
				mel.eval('prefixHierarchy;') #Add a prefix to all hierarchy names.
			elif index==contents.index('Search and Replace Names'):
				mel.eval('SearchAndReplaceNames;') #performSearchReplaceNames 1; #Rename objects in the scene.
			cmb.setCurrentIndex(0)


	def getTrailingIntegers(self, string, increment=0):
		'''
		args: increment(int) = optional step amount

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
		find = str(self.parentUi.t000.text()) #asterisk denotes startswith*, *endswith, *contains* 
		to = str(self.parentUi.t001.text())


		if pm.ls(selection=1): #if selection; operate on only the selected objects.
			if find:
				lists = [pm.ls(f, sl=1) for f in find.split('|')] #objects in current selection that match criteria
			else:
				lists = [pm.ls(sl=1)] #if 'find' field is blank, use all currently selected objects
		else:
			if find:
				lists = [pm.ls(f) for f in find.split('|')] # objects = pm.ls(find) #Stores a list of all objects containing 'find'
			else:
				lists = [pm.ls()] #if find field is blank, and nothing is selected, get all objects
		objects = set([i for sublist in lists for i in sublist]) #flatten and remove any duplicates.


		pm.undoInfo (openChunk=1)
		for obj in objects:
			f = [f for f in find.split('|') if f.strip('*') in obj.name()][0] #get the objects that contain the chars in find.split('|')
			
			relatives = pm.listRelatives(obj, parent=1) #Get a list of it's direct parent
			if 'group*' in relatives: #If that parent starts with group, it came in root level and is pasted in a group, so ungroup it
				relatives[0].ungroup()

			#find modifiers
			if to.startswith('*') and to.endswith('*'): #replace chars
				f = f.replace('*', '') #remove modifiers
				newName = obj.name().replace(f, to)

			elif to.startswith('*'): #replace suffix
				newName = obj.name()+to

			elif to.endswith('*'): #replace prefix
				f = f.replace('*', '') #remove modifiers
				newName = obj.name().replace(f, to, 1) #1=replace only the first occurance

			elif to.startswith('**'): #replace suffix and move any trailing integers
				num = self.getTrailingIntegers(obj.name())
				stripped = obj.name().rstrip(f+'0123456789')
				newName = stripped+num+to

			else: #replace whole name
				newName = to

			newName = newName.replace('*', '') #remove modifiers
			while pm.objExists(newName):
				num = self.getTrailingIntegers(newName, increment=1)
				newName = newName.rstrip('0123456789')+num

			name = pm.rename(obj, newName) #Rename the object with the new name
		pm.undoInfo (closeChunk=1)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------