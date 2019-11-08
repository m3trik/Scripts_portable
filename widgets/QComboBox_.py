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
	Under construction.
	'''
	def __init__(self, parent=None):
		super(QComboBox_, self).__init__(parent)



	def refreshContents(self):
		'''
		Change index to refresh contents.
		'''
		index = self.currentIndex()
		self.blockSignals(True)
		self.setCurrentIndex(-1) #switch the index before opening to initialize the contents of the comboBox
		self.blockSignals(False)
		self.setCurrentIndex(index) #change index back to refresh contents



	# def showPopup(self):
	# 	self.setStyleSheet('''
	# 		}''')



	# def hidePopup(self):
	# 	self.setStyleSheet('''
	# 		}''')



	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.refreshContents()

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
