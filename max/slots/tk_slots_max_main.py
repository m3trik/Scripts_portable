from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('main')


	def tree000(self, wItem=None, column=None):
		'''

		'''
		tree = self.parentUi.tree000

		if not any([wItem, column]):
			if not tree.refresh: #static list items -----------
				tree.expandOnHover = True
				tree.convert(tree.getTopLevelItems(), 'QLabel') #construct the tree using the existing contents.

			#refreshed list items -----------------------------
			recentCommandNames = self.sb.prevCommand(docString=1, as_list=1) #Get a list of any recent command names
			[tree.add('QLabel', 'Recent Commands', refresh=True, setText=s) for s in recentCommandNames]

			# l = []
			# [tree.add('QLabel', '', setText=s) for s in l]
			# return

		# widget = tree.getWidget(wItem, column)
		header = tree.getHeaderFromColumn(column)
		text = tree.getWidgetText(wItem, column)
		index = tree.getIndexFromWItem(wItem, column)

		if header=='Recent Commands':
			recentCommands = self.sb.prevCommand(method=1, as_list=1) #Get a list of any recent commands
			method = recentCommands[index]
			if callable(method):
				method()

		# if header=='':
		# 	if text=='':
		# 		mel.eval('')
		# 	if text=='':
		# 		mel.eval('')


	def v013(self):
		'''
		Minimize Main Application

		'''
		self.sb.getMethod('file', 'b005')()


	def v024(self):
		'''
		Recent Command: 1
		'''
		self.sb.prevCommand(method=1, as_list=1)[-1]() #execute command at index


	def v025(self):
		'''
		Recent Command: 2
		'''
		self.sb.prevCommand(method=1, as_list=1)[-2]() #execute command at index
			

	def v026(self):
		'''
		Recent Command: 3
		'''
		self.sb.prevCommand(method=1, as_list=1)[-3]() #execute command at index


	def v027(self):
		'''
		Recent Command: 4
		'''
		self.sb.prevCommand(method=1, as_list=1)[-4]() #execute command at index


	def v028(self):
		'''
		Recent Command: 5
		'''
		self.sb.prevCommand(method=1, as_list=1)[-5]() #execute command at index


	def v029(self):
		'''
		Recent Command: 6
		'''
		self.sb.prevCommand(method=1, as_list=1)[-6]() #execute command at index







#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------