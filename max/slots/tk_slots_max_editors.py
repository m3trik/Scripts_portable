import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

from PySide2 import QtWidgets

import os.path

from tk_slots_max_init import Init





class Editors(Init):
	def __init__(self, *args, **kwargs):
		super(Editors, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('editors')

		#construct stacked widget from maya layouts
		self.widgetList = ['MainAttributeEditorLayout','MainChannelBoxLayout','ToggledOutlinerLayout','MainToolSettingsLayout','LayerEditorDisplayLayerLayout']
		print self.getWidget(allWindows=1)
		print self.getWindow(allWidgets=1)
		self.stackedWidget = QtWidgets.QStackedWidget()
		# for w in self.widgetList:
		# 	self.stackedWidget.addWidget(self.getWidget(w))


		self.sb.getUi('dynLayout').setCentralWidget(self.stackedWidget)
		# self.sb.getUi('dynLayout').addWidget(self.stackedWidget)




	def setWidgetIndex(self, name):
		'''
		Set the active widget on the dynLayout ui.
		args:
			name='string' - name of widget
		returns:
			the current widget object from the stacked widget.
		'''
		index = self.widgetList.index(name)
		self.stackedWidget.setCurrentIndex(index)
		currentWidget = self.stackedWidget.currentWidget()
		currentWidget.adjustSize()
		self.hotBox.layoutStack('dynLayout') #change layout
		# self.hotBox.resize(currentWidget.minimumSizeHint())
		# self.hotBox.resize(currentWidget.sizeHint())
		return currentWidget


	def v000(self):
		'''
		Attributes
		'''
		self.setWidgetIndex('MainAttributeEditorLayout')


	def v001(self):
		'''
		Outliner
		'''
		self.setWidgetIndex('ToggledOutlinerLayout')


	def v002(self):
		'''
		Tool
		'''
		self.setWidgetIndex('MainToolSettingsLayout')


	def v003(self):
		'''
		Layers
		'''
		self.setWidgetIndex('LayerEditorDisplayLayerLayout')


	def v004(self):
		'''
		Channels
		'''
		self.setWidgetIndex('MainChannelBoxLayout')









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------