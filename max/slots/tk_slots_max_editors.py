from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Editors(Init):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.dynLayout = self.sb.getUi('dynLayout')
		self.stackedWidget = self.dynLayout.stackedWidget


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.editors.pin

		if state is 'setMenu':
			pin.contextMenu.add(QComboBox_, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.editors.cmb000
		
		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		if index>0:
			if index==cmb.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def getEditorWidget(self, name):
		'''
		Get a maya widget from a given name.

		args:
			name (str) = name of widget
		'''
		_name = '_'+name
		if not hasattr(self, _name):
			w = self.convertToWidget(name)
			self.stackedWidget.addWidget(w)
			setattr(self, _name, w)

		return getattr(self, _name)


	def showEditor(self, name, width=640, height=480):
		'''
		Show, resize, and center the given editor.

		args:
			name (str) = The name of the editor.
			width (int) = The editor's desired width.
			height (int) = The editor's desired height.

		returns:
			(obj) The editor as a QWidget.
		'''
		w = self.getEditorWidget(name)

		self.tk.setUi('dynLayout')
		self.stackedWidget.setCurrentWidget(w)
		self.tk.resize(width, height)
		self.tk.move(QtGui.QCursor.pos() - self.tk.rect().center()) #move window to cursor position and offset from left corner to center

		return w


	def v000(self):
		'''
		Attributes
		'''
		name = mel.eval('$tmp=$gAttributeEditorForm')
		self.showEditor(name, 640, 480)


	def v001(self):
		'''
		Outliner
		'''
		name = mel.eval('$tmp=$gOutlinerForm')
		self.showEditor(name, 260, 640)


	def v002(self):
		'''
		Tool
		'''
		name = mel.eval('$tmp=$gToolSettingsForm')
		self.showEditor(name, 461, 480)


	def v003(self):
		'''
		Layers
		'''
		name = mel.eval('$tmp=$gLayerEditorForm')
		self.showEditor(name, 261, 480)


	def v004(self):
		'''
		Channels
		'''
		name = mel.eval('$tmp=$gChannelsForm')
		self.showEditor(name, 640, 480)


	def v006(self):
		'''
		Script
		'''
		name = mel.eval('$tmp=$gScriptEditorPanel')
		self.showEditor(name, 640, 480)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------