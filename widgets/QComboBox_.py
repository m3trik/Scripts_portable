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
	def __init__(self, parent=None):
		super(QComboBox_, self).__init__(parent)



	def showPopup(self):
		# self.setMaximumSize(999,999)

		width = self.minimumSizeHint().width()
		self.view().setMinimumWidth(width)

		super(QComboBox_, self).showPopup()


	def hidePopup(self):
		# self.setMaximumSize(self.minimumSize())

		super(QComboBox_, self).hidePopup()


	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''

		return QtWidgets.QComboBox.showEvent(self, event)


	def enterEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''

		return QtWidgets.QComboBox.enterEvent(self, event)


	def leaveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# self.hidePopup()

		return QtWidgets.QComboBox.leaveEvent(self, event)


	def addItems_(self, items, title=None):
		'''
		Set items.
		args:
			items (list) = list of strings to fill the comboBox with
			title (str) = optional value for the first index of the comboBox's list

		returns:
			comboBox's current item list minus any title.
		ex. comboBox.addItems_(["Import file", "Import Options"], "Import")
		'''
		self.blockSignals(True) #to keep clear from triggering currentIndexChanged
		index = self.currentIndex() #get current index before refreshing list
		self.clear()
		
		items_ = [str(i) for i in [title]+items if i]
		self.addItems(items_) 

		self.setCurrentIndex(index)
		self.blockSignals(False)

		return items_





if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	w=QComboBox_()
	w.show()
	sys.exit(app.exec_())



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
