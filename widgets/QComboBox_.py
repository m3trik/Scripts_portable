from PySide2 import QtCore, QtGui, QtWidgets

import sys



'''
Promoting a widget in designer to use a custom class:
>	In Qt Designer, select all the widgets you want to replace, 
		then right-click them and select 'Promote to...'. 

>	In the dialog:
		Base Class:		Class from which you inherit. ie. QWidget
		Promoted Class:	Name of the class. ie. "MyWidget"
		Header File:	Path of the file (changing the extension .py to .h)  ie. myfolder.mymodule.mywidget.h

>	Then click "Add", "Promote", 
		and you will see the class change from "QWidget" to "MyWidget" in the Object Inspector pane.
'''



class QComboBox_(QtWidgets.QComboBox):
	'''
	
	'''
	sb = None

	def __init__(self, parent=None):
		super(QComboBox_, self).__init__(parent)



	def showPopup(self):
		# self.setMaximumSize(999,999)

		# width = self.minimumSizeHint().width()
		# self.view().setMinimumWidth(width)

		super(QComboBox_, self).showPopup()


	def hidePopup(self):
		# self.setMaximumSize(self.minimumSize())

		super(QComboBox_, self).hidePopup()


	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if not self.sb:
			try:
				from tk_switchboard import Switchboard
				self.sb = Switchboard()
				# self.tk = self.sb.getClassInstance('tk')
			except Exception as error:
				print error

		method = self.sb.getMethod(self.sb.getUiName(), self.objectName())
		if callable(method):
			method()

		return QtWidgets.QComboBox.showEvent(self, event)


	def enterEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__enterEvent'
		self.setStyleSheet('''
			QComboBox {
				background-color: rgba(82,133,166,200);
				color: white;
			}''')

		return QtWidgets.QComboBox.enterEvent(self, event)


	def leaveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__leaveEvent'
		self.setStyleSheet('''
			QComboBox {
				background-color: rgba(100,100,100,200);
				color: white;
			}''')

		# self.hidePopup()

		return QtWidgets.QComboBox.leaveEvent(self, event)






if __name__ == "__main__":
	qApp = QtWidgets.QApplication(sys.argv)
		
	w = QComboBox_()
	w.show()
	sys.exit(qApp.exec_())



# -----------------------------------------------
# Notes
# -----------------------------------------------


	# def mouseMoveEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''
	# 	# print '__mouseMoveEvent_1'
	# 	if not self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
	# 		self.hidePopup()

	# 	return QtWidgets.QComboBox.mouseMoveEvent(self, event)



	# def mouseReleaseEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''
	# 	# print '__mouseReleaseEvent_1'
	# 	if self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
	# 		self.showPopup()

	# 	return QtWidgets.QComboBox.mouseReleaseEvent(self, event)
