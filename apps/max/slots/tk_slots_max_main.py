from __future__ import print_function
from builtins import super
import os.path

from tk_slots_maya_init import *



class Main(Init):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def tree000(self, wItem=None, column=None):
		''''''
		tree = self.main_ui.tree000

		if wItem is 'setMenu':
			tree.expandOnHover = True
			tree.convert(tree.getTopLevelItems(), 'QLabel') #construct the tree using the existing contents.
			return

		if not any([wItem, column]): #refresh list items -----------------------------
			recentCommandInfo = self.sb.prevCommand(docString=1, toolTip=1, as_list=1) #Get a list of any recent command names and their toolTips
			[tree.add('QLabel', 'Recent Commands', refresh=True, setText=s[0], setToolTip=s[1]) for s in recentCommandInfo]

			selection = rt.selection
			if selection:
				history = selection
				for node in history:
					parent = tree.add('QLabel', 'Node History', childHeader=node.name, refresh=1, setText=node.name)

					attributes = Init.getAttributesMax(node) #get dict containing attributes:values of the history node.
					spinboxes = [tree.add('QDoubleSpinBox', parent, refresh=1, setSpinBoxByValue_=[k, v])
						for k, v in attributes.items() 
							if isinstance(v, (float, int, bool))]

					#set signal/slot connections:
					[w.valueChanged.connect(
						lambda value, widget=w, obj=node: self.setAttributesMzx(node, {widget.prefix().rstrip(': '):value})) 
						for w in spinboxes] #set signal/slot connections
			return

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
		'''Minimize Main Application

		'''
		self.sb.getMethod('file', 'b005')()


	def v024(self):
		'''Recent Command: 1
		'''
		self.sb.prevCommand(method=1, as_list=1)[-1]() #execute command at index


	def v025(self):
		'''Recent Command: 2
		'''
		self.sb.prevCommand(method=1, as_list=1)[-2]() #execute command at index
			

	def v026(self):
		'''Recent Command: 3
		'''
		self.sb.prevCommand(method=1, as_list=1)[-3]() #execute command at index


	def v027(self):
		'''Recent Command: 4
		'''
		self.sb.prevCommand(method=1, as_list=1)[-4]() #execute command at index


	def v028(self):
		'''Recent Command: 5
		'''
		self.sb.prevCommand(method=1, as_list=1)[-5]() #execute command at index


	def v029(self):
		'''Recent Command: 6
		'''
		self.sb.prevCommand(method=1, as_list=1)[-6]() #execute command at index







#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------