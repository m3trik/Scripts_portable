from __future__ import print_function
from tk_slots_max_init import *

from datetime import datetime
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

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000

		if index=='setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


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









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------