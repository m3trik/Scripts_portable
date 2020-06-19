from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)


	def tree000(self, wItem=None, column=None):
		'''

		'''
		tree = self.parentUi.tree000

		if not any([wItem, column]):
			if not tree.refresh:
				tree.expandOnHover = True
				tree.convert(tree.getTopLevelItems(), 'QLabel') #construct the tree using the existing contents.

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









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------