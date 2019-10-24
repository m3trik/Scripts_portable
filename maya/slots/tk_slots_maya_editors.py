import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init




class Editors(Init):
	def __init__(self, *args, **kwargs):
		super(Editors, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('editors')

		#construct stacked widget from maya layouts
		# self.widgetList = ['MainAttributeEditorLayout','MainChannelBoxLayout','ToggledOutlinerLayout','MainToolSettingsLayout','LayerEditorDisplayLayerLayout']
		self.stackedWidget = self.sb.getUi('dynLayout').stackedWidget
		# self.stackedWidget = self.sb.getUi('dynLayout').stackedWidget
		# for w in self.widgetList:
		# 	self.stackedWidget.addWidget(self.sb.qApp_getWidget(w))
			# self.stackedWidget.addWidget(self.sb.qApp_getWidget(w))


		# self.sb.getUi('dynLayout').setCentralWidget(self.stackedWidget)
		# self.sb.getUi('dynLayout').addWidget(self.stackedWidget)

		print pm.lsUI(
				numWidgets=True,	//#[bool, create]  Reports the number of QT widgets used by Maya.
				dumpWidgets=True	//#[bool, create]  Dump all QT widgets used by Maya.
				)



	def setWidgetIndex(self, name):
		'''
		Set the active widget in the dynLayout ui.
		args:
			name='string' - name of widget
		returns:
			the current widget object from the stacked widget.
		'''
		print 8*' -'
		self.stackedWidget.addWidget(self.sb.getWidget(name=name))
		self.stackedWidget.setCurrentWidget(name)
		currentWidget = self.stackedWidget.currentWidget()
		currentWidget.adjustSize()
		# self.hotBox.resize(currentWidget.minimumSizeHint())
		# self.hotBox.resize(currentWidget.sizeHint())
		return currentWidget


	def i000(self):
		'''
		Attributes
		'''
		self.setWidgetIndex('MainAttributeEditorLayout')


	def i001(self):
		'''
		Outliner
		'''
		self.setWidgetIndex('ToggledOutlinerLayout')


	def i002(self):
		'''
		Tool
		'''
		self.setWidgetIndex('MainToolSettingsLayout')


	def i003(self):
		'''
		Layers
		'''
		self.setWidgetIndex('LayerEditorDisplayLayerLayout')


	def i004(self):
		'''
		Channels
		'''
		self.setWidgetIndex('MainChannelBoxLayout')









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------