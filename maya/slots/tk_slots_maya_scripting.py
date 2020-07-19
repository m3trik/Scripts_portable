from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Scripting(Init):
	def __init__(self, *args, **kwargs):
		super(Scripting, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('scripting')
		self.childUi = self.sb.getUi('scripting_submenu')

		# tk_cmdScrollFieldReporter = pm.cmdScrollFieldReporter (
		# 														height=35,
		# 														backgroundColor=[0,0,0],
		# 														highlightColor=[0,0,0],
		# 														echoAllCommands=False,
		# 														filterSourceType="")

		# self.parentUi.plainTextEdit.appendPlainText(tk_cmdScrollFieldReporter)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state is 'setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000

		if index is 'setMenu':
			files = ['']
			contents = cmb.addItems_(files, '')
			return

		# if index>0:
		# 	if index==cmd.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def chk000(self, state=None):
		'''
		Toggle Mel/Python

		'''
		if self.parentUi.chk000.isChecked():
			self.parentUi.chk000.setText("python")
		else:
			self.parentUi.chk000.setText("MEL")


	def b000(self):
		'''
		Toggle Script Output Window

		'''
		state = pm.workspaceControl ("scriptEditorOutputWorkspace", query=1, visible=1)
		pm.workspaceControl ("scriptEditorOutputWorkspace", edit=1, visible=not state)

	def b001(self):
		'''
		Command Line Window

		'''
		mel.eval('commandLineWindow;')

	def b002(self):
		'''
		Script Editor

		'''
		mel.eval('ScriptEditor;')

	def b003(self):
		'''
		New Tab

		'''
		label = "MEL"
		if self.parentUi.chk000.isChecked():
			label = ".py"
		# self.parentUi.tabWidget.addTab(label)
		self.parentUi.tabWidget.insertTab(0, label)

	def b004(self):
		'''
		Delete Tab

		'''
		index = self.parentUi.tabWidget.currentIndex()
		self.parentUi.tabWidget.removeTab(index)

	def b005(self):
		'''
		

		'''
		mel.eval('')

	def b006(self):
		'''
		

		'''
		mel.eval('')

	def b007(self):
		'''
		

		'''
		mel.eval('')

	def b008(self):
		'''
		

		'''
		mel.eval("")

	def b009(self):
		'''
		

		'''
		mel.eval('')



#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------