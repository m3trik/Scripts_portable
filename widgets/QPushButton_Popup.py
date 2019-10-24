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


class View(QtWidgets.QListWidget):
	'''
	Provides a list or icon view onto a model.
	'''
	def __init__(self, parent=None):
		super(View, self).__init__(parent)

		self.parent = parent
		print parent.size()
		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)

	def addItems(self, items):
		for text in items:
			widget = QtWidgets.QPushButton(text, parent=self)
			widget.setFixedSize(111, 19)
			item = QtWidgets.QListWidgetItem(self, 1)
			self.setItemWidget(item, widget)

		self.setFixedSize(111+5, self.minimumSizeHint().height())


class QPushButton_Popup(QtWidgets.QPushButton):
	'''
	Under construction.
	'''
	def __init__(self, parent=None):
		super(QPushButton_Popup, self).__init__(parent)

		self.view = View(self)

	# 	self.view.installEventFilter(self)


	# def eventFilter(self, widget, event):
	# 	'''
	# 	'''
	# 	print event.type
	# 	if event.__class__==QtGui.QShowEvent:
	# 		print event.type, widget
	# 		# widget.grabMouse()
	# 		return True
	# 	# if event.__class__==QtGui.QMoveEvent:
			
	# 	# 		return True
	# 	return False


	def showPopup(self):
		'''
		'''
		# self.setStyleSheet('''

		# 	}''')
		self.view.show()
		self.view.clear()
		self.view.addItems(['node0', 'node1', 'node2'])

		pos = self.mapToGlobal(self.rect().topRight())
		self.view.move(pos)


	def hidePopup(self):
		'''
		'''
		# self.setStyleSheet('''
			
		# 	}''')
		self.view.hide()


	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__showEvent'
		# self.refreshContents()

		return QtWidgets.QPushButton.showEvent(self, event)


	def hideEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__hideEvent'
		self.hidePopup()

		return QtWidgets.QPushButton.hideEvent(self, event)


	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__mouseMoveEvent'
		combinedRect = self.rect().united(self.view.rect())

		if not combinedRect.contains(self.mapFromGlobal(QtGui.QCursor.pos())):
			self.hidePopup()

		return QtWidgets.QPushButton.mouseMoveEvent(self, event)


	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__mouseReleaseEvent'

		return QtWidgets.QPushButton.mouseReleaseEvent(self, event)


	def enterEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__enterEvent'
		self.showPopup()

		self.view.rect().setLeft(0)

		# rect = self.rect().intersect(self.view.rect())
		# self.rect().unite(rect)

		# print rect.x(), rect.y(), rect.width(), rect.height() #(x, y, w, h)
		# rect.adjust(rect.x(), rect.y(), rect.width(), rect.height())

		# self.rect().setRect(rect.x(), rect.y(), rect.width(), rect.height())

		self.setStyleSheet('''
			QComboBox {
				background-color: rgba(82,133,166,200);
				color: white;
			}''')

		return QtWidgets.QPushButton.enterEvent(self, event)


	def leaveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__leaveEvent'
		if not self.view.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())):
			self.hidePopup()

		self.setStyleSheet('''
			QComboBox {
				background-color: rgba(100,100,100,200);
				color: white;
			}''')

		return QtWidgets.QPushButton.leaveEvent(self, event)



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	w = QPushButton_Popup()
	# w.view.addItems(['node0', 'node1', 'node2'])
	w.show()
	sys.exit(app.exec_())


		# def refreshContents(self):
	# 	'''
	# 	Change index to refresh contents.
	# 	'''
	# 	index = self.currentIndex()
	# 	self.blockSignals(True)
	# 	self.setCurrentIndex(-1) #switch the index before opening to initialize the contents of the comboBox
	# 	self.blockSignals(False)
	# 	self.setCurrentIndex(index) #change index back to refresh contents



# class Model(QtGui.QStandardItemModel):
# 	'''
# 	Provides a generic model for storing custom data.
# 	'''
# 	def __init__(self, parent=None):
# 		super(Model, self).__init__(parent)

# 		# self.nodes = ['node0', 'node1', 'node2']

# 	def index(self, row, column, parent):
# 		return self.createIndex(row, column, self.nodes[row])

# 	def parent(self, index):
# 		return QtCore.QModelIndex()

# 	def rowCount(self, index):
# 		if index.internalPointer() in self.nodes:
# 			return 0
# 		return len(self.nodes)

# 	def columnCount(self, index):
# 		return 1

# 	def data(self, index, role):
# 		if role == 0: 
# 			return index.internalPointer()
# 		else:
# 			return None