from __future__ import print_function
from builtins import super
import os.path

from tk_slots_max_init import **



class Scripting(Init):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# tk_cmdScrollFieldReporter = pm.cmdScrollFieldReporter (
		# 														height=35,
		# 														backgroundColor=[0,0,0],
		# 														highlightColor=[0,0,0],
		# 														echoAllCommands=False,
		# 														filterSourceType="")

		# self.scripting_ui.plainTextEdit.appendPlainText(tk_cmdScrollFieldReporter)
		

	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.scripting_ui.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.scripting_ui.cmb000

		if index is 'setMenu':
			files = ['']
			cmb.addItems_(files, '')
			return

		if index>0:
			if index==cmd.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def chk000(self, state=None):
		'''Toggle Mel/Python
		'''
		if self.scripting_ui.chk000.isChecked():
			self.scripting_ui.chk000.setText("python")
		else:
			self.scripting_ui.chk000.setText("MEL")


	def b000(self):
		'''Toggle Script Output Window
		'''
		state = pm.workspaceControl ("scriptEditorOutputWorkspace", query=1, visible=1)
		pm.workspaceControl ("scriptEditorOutputWorkspace", edit=1, visible=not state)


	def b001(self):
		'''Command Line Window
		'''
		maxEval('tk_commandLineWindow;')


	def b002(self):
		'''Script Editor
		'''
		maxEval('ScriptEditor;')


	def b003(self):
		'''New Tab
		'''
		label = "MEL"
		if self.scripting_ui.chk000.isChecked():
			label = ".py"
		# self.scripting_ui.tabWidget.addTab(label)
		self.scripting_ui.tabWidget.insertTab(0, label)


	def b004(self):
		'''Delete Tab
		'''
		index = self.scripting_ui.tabWidget.currentIndex()
		self.scripting_ui.tabWidget.removeTab(index)


	def b005(self):
		''''''
		pass


	def b006(self):
		''''''
		pass


	def b007(self):
		''''''
		pass

	def b008(self):
		''''''
		pass

	def b009(self):
		''''''
		pass









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------