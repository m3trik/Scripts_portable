from tk_slots_maya_init import Init

import os.path



class Scripting(Init):
	def __init__(self, *args, **kwargs):
		super(Scripting, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('scripting')

		# tk_cmdScrollFieldReporter = pm.cmdScrollFieldReporter (
		# 														height=35,
		# 														backgroundColor=[0,0,0],
		# 														highlightColor=[0,0,0],
		# 														echoAllCommands=False,
		# 														filterSourceType="")

		# self.ui.plainTextEdit.appendPlainText(tk_cmdScrollFieldReporter)



	def chk000(self):
		'''
		Toggle Mel/Python

		'''
		if self.ui.chk000.isChecked():
			self.ui.chk000.setText("python")
		else:
			self.ui.chk000.setText("MEL")


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				mel.eval('')
			cmb.setCurrentIndex(0)


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
		if self.ui.chk000.isChecked():
			label = ".py"
		# self.ui.tabWidget.addTab(label)
		self.ui.tabWidget.insertTab(0, label)

	def b004(self):
		'''
		Delete Tab

		'''
		index = self.ui.tabWidget.currentIndex()
		self.ui.tabWidget.removeTab(index)

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
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------