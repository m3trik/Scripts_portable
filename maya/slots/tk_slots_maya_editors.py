from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Editors(Init):
	def __init__(self, *args, **kwargs):
		super(Editors, self).__init__(*args, **kwargs)

		#construct stacked widget from maya layouts
		# self.widgetList = ['MainAttributeEditorLayout','MainChannelBoxLayout','ToggledOutlinerLayout','MainToolSettingsLayout','LayerEditorDisplayLayerLayout']
		self.stackedWidget = self.sb.getUi('dynLayout').stackedWidget
		# self.stackedWidget = self.sb.getUi('dynLayout').stackedWidget
		# for w in self.widgetList:
		# 	self.stackedWidget.addWidget(self.sb.qApp_getWidget(w))
			# self.stackedWidget.addWidget(self.sb.qApp_getWidget(w))


		# self.sb.getUi('dynLayout').setCentralWidget(self.stackedWidget)
		# self.sb.getUi('dynLayout').addWidget(self.stackedWidget)

		# print(pm.lsUI(
		# 		numWidgets=True,	#[bool, create]  Reports the number of QT widgets used by Maya.
		# 		dumpWidgets=True	#[bool, create]  Dump all QT widgets used by Maya.
		# 		))


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000
		
		if index=='setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def setWidgetIndex(self, name):
		'''
		Set the active widget in the dynLayout ui.
		args:
			name (str) = name of widget
		returns:
			the current widget object from the stacked widget.
		'''
		print(8*' -')
		self.stackedWidget.addWidget(self.sb.getWidget(name=name))
		self.stackedWidget.setCurrentWidget(name)
		currentWidget = self.stackedWidget.currentWidget()
		currentWidget.adjustSize()
		# self.tk.resize(currentWidget.minimumSizeHint())
		# self.tk.resize(currentWidget.sizeHint())
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
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------