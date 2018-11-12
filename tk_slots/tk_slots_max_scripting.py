import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots import Slot
import tk_max_shared_functions as func



#                            oo            dP   oo                   
#                                          88                        
# .d8888b. .d8888b. 88d888b. dP 88d888b. d8888P dP 88d888b. .d8888b. 
# Y8ooooo. 88'  `"" 88'  `88 88 88'  `88   88   88 88'  `88 88'  `88 
#       88 88.  ... 88       88 88.  .88   88   88 88    88 88.  .88 
# `88888P' `88888P' dP       dP 88Y888P'   dP   dP dP    dP `8888P88 
#                               88                               .88 
#                               dP                           d8888P 
#
class Scripting(Slot):
	def __init__(self, *args, **kwargs):
		super(Scripting, self).__init__(*args, **kwargs)

		#init widgets
		func.initWidgets(self)


		tk_cmdScrollFieldReporter = pm.cmdScrollFieldReporter (
																height=35,
																backgroundColor=[0,0,0],
																highlightColor=[0,0,0],
																echoAllCommands=False,
																filterSourceType="")

		self.ui.plainTextEdit.appendPlainText(tk_cmdScrollFieldReporter)
		

	def chk000(self): #toggle mel/python
		if self.ui.chk000.isChecked():
			self.ui.chk000.setText("python")
		else:
			self.ui.chk000.setText("MEL")


	def b000(self): #toggle script output window
		state = pm.workspaceControl ("scriptEditorOutputWorkspace", query=1, visible=1)
		pm.workspaceControl ("scriptEditorOutputWorkspace", edit=1, visible=not state)

	def b001(self): #command line window
		maxEval('tk_commandLineWindow;')

	def b002(self): #script editor
		maxEval('ScriptEditor;')

	def b003(self): #new tab
		label = "MEL"
		if self.ui.chk000.isChecked():
			label = ".py"
		# self.ui.tabWidget.addTab(label)
		self.ui.tabWidget.insertTab(0, label)

	def b004(self): #delete tab
		index = self.ui.tabWidget.currentIndex()
		self.ui.tabWidget.removeTab(index)

	def b005(self): #
		maxEval('')

	def b006(self): #
		maxEval('')

	def b007(self): #
		maxEval('')

	def b008(self): #
		mel.eval("")

	def b009(self): #
		maxEval('')



#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------