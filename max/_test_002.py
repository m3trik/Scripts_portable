from PySide2 import QtGui, QtCore, QtWidgets

import os.path


class PopupDialogMixin(object):  # will not work (with PySide at least) unless implemented as 'new style' class. I.e inherit from object
	def makePopup(callWidget):
		"""
		Turns the dialog into a popup dialog.
		callWidget is the widget responsible for calling the dialog (e.g. a toolbar button)
		"""
		self.setContentsMargins(0,0,0,0)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
		self.setObjectName('ImportDialog')

		# Move the dialog to the widget that called it
		point = callWidget.rect().bottomRight()
		global_point = callWidget.mapToGlobal(point)
		self.move(global_point - QtCore.QPoint(self.width(), 0))



#Your custom dialog would then inherit from both QtCore.QDialog and PopupDialogMixin. 
#This gives you the option to use your dialog in the 'normal' way or make it a popup dialog. e.g:
dlg = MyDialog(self)
dlg.makePopup(self.myButton)