import maya.mel as mel
import pymel.core as pm

import os

from tk_slots_maya_init import Init





class Scene(Init):
	def __init__(self, *args, **kwargs):
		super(Scene, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('scene')

		

		self.ui.t000.returnPressed.connect(self.t001) #preform rename on returnPressed




	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = self.comboBox(cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				mel.eval('')
			cmb.setCurrentIndex(0)


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
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------