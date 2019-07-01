import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





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
				pass
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
		maxEval('tk_commandLineWindow;')


	def b002(self):
		'''
		Script Editor
		'''
		maxEval('ScriptEditor;')


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
		pass


	def b006(self):
		'''
		
		'''
		pass


	def b007(self):
		'''
		
		'''
		pass

	def b008(self):
		'''
		
		'''
		pass

	def b009(self):
		'''
		
		'''
		pass








#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------