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



class View(QtWidgets.QListView):
	'''
	Provides a list or icon view onto a model.
	'''
	__popupPreventHide = False

	def __init__(self, parent=None):
		super(View, self).__init__(parent)

		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)

		# self.setMouseTracking(True)
		# print self.isSelectionRectVisible()
		# self.setSelectionRectVisible(True)
		# self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus) #don't allow focusing of the view of the popup
		# self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
		# QtWidgets.QStyle.styleHint(QtWidgets.QStyle.SH_ComboBox_Popup, self)

		self.parent = parent
		if self.parent.parentWidget():
			self.parent.parentWidget().installEventFilter(self)


	def showPopup(self, pos=None):
		'''
		args:
			pos=<QPoint> - Move to position.
		'''
		# self.setStyleSheet('''

		# 	}''')
		self.resize(115, self.minimumSizeHint().height()+5)

		if pos:
			self.move(pos)

		self.show()
		self.setFocus()


	def hidePopup(self):
		'''
		'''
		# self.setStyleSheet('''
			
		# 	}''')
		if not self.__popupPreventHide:
			self.hide()


	def mouseMoveEvent(self, event):
		print event


	def mouseReleaseEvent(self, event):
		print event


	def eventFilter(self, widget, event):
		'''
		Handles mainWindow (top level parent) events relating to the view.
		args:
			widget=<event reciever>
			event=QEvent
		'''
		# print event.__class__.__name__, widget
		if event.__class__==QtGui.QMouseEvent:
			# self.view.rect().setLeft(0)
			if self.isVisible() and self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())):# and not self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())):
				# print 'active'
				self.__popupPreventHide = True
				# self.activateWindow()
				# self.raise_()
				self.__mouseGrabber = self.mouseGrabber()
				# print self.mouseGrabber().objectName()
				# self.grabMouse()
				# print self.mouseGrabber().objectName()
				# self.setFocus()
				self.event(event)
			else:
				self.__popupPreventHide = False
				# print 'not rect'
				# self.__mouseGrabber.grabMouse()

		return super(View, self).eventFilter(widget, event)



class QComboBox_Popup(QtWidgets.QComboBox):
	'''
	Under construction.
	'''
	def __init__(self, parent=None):
		super(QComboBox_Popup, self).__init__(parent)

		self.model = self.model()

		self.view = View(self)
		self.view.setModel(self.model)

		# frame = self.findChild(QtWidgets.QFrame) #get frame from the comboBox (after calling showPopup the comboBox instance becomes a QFrame.)
		# frame.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
		# frame.setAttribute(QtCore.Qt.WA_NoMousePropagation)
		# self.setAttribute(QtCore.Qt.WA_NoMouseReplay)#QtCore.Qt.WA_MouseNoMask)


	def refreshContents(self):
		'''
		Change index to refresh contents.
		'''
		index = self.currentIndex()
		self.blockSignals(True)
		self.setCurrentIndex(-1) #switch the index before opening to initialize the contents of the comboBox
		self.blockSignals(False)
		self.setCurrentIndex(index) #change index back to refresh contents


	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__showEvent'
		self.refreshContents()

		return QtWidgets.QComboBox.showEvent(self, event)


	def hideEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__hideEvent'
		# self.view.hidePopup()

		return QtWidgets.QComboBox.hideEvent(self, event)


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

		pos = self.mapToGlobal(self.rect().topRight())
		self.view.showPopup(pos)

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

		self.view.hidePopup()

		return QtWidgets.QComboBox.leaveEvent(self, event)


	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__mouseMoveEvent'
		# if not self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())):
		# 	# self.view.hidePopup()
		# 	print 'not rect'

		return QtWidgets.QComboBox.mouseMoveEvent(self, event)



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	w = QComboBox_Popup()
	w.show()
	sys.exit(app.exec_())



# class Model(QtGui.QStandardItemModel):
# 	'''
# 	Provides a generic model for storing custom data.
# 	'''
# 	def __init__(self, parent=None):
# 		super(Model, self).__init__(parent)

# 		self.nodes = ['node0', 'node1', 'node2']


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



# class View(QtWidgets.QListView):
# 	'''
# 	Provides a list or icon view onto a model.
# 	'''
# 	__popupPreventHide = False

# 	def __init__(self, parent=None):
# 		super(View, self).__init__(parent)

# 		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)

# 		self.setMouseTracking(True)
# 		# self.setSelectionRectVisible(True)
# 		# self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus) #don't allow focusing of the view of the popup
# 		# self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)

# 		if parent.parentWidget():
# 			parent.parentWidget().installEventFilter(self)


# 	def showPopup(self, pos=None):
# 		'''
# 		args:
# 			pos=<QPoint> - Move to position.
# 		'''
# 		# self.setStyleSheet('''

# 		# 	}''')
# 		self.resize(115, self.minimumSizeHint().height()+5)

# 		if pos:
# 			self.move(pos)

# 		self.show()


# 	def hidePopup(self):
# 		'''
# 		'''
# 		# self.setStyleSheet('''
			
# 		# 	}''')
# 		if not self.__popupPreventHide:
# 			self.hide()


# 	def mouseMoveEvent(self, event):
# 		print event


# 	def mouseReleaseEvent(self, event):
# 		print event


# 	def eventFilter(self, widget, event):
# 		'''
# 		Handles mainWindow (top level parent) events relating to the view.
# 		args:
# 			widget=<event reciever>
# 			event=QEvent
# 		'''
# 		# print event.__class__.__name__, widget
# 		if event.__class__==QtGui.QMouseEvent:
# 			# self.view.rect().setLeft(0)
# 			if self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())):# and not self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())):
# 				print 'active'
# 				self.__popupPreventHide = True
# 				self.activateWindow()
# 				self.setFocus()
# 			else:
# 				print 'not view rect'
# 				self.__popupPreventHide = False
# 				# self.hidePopup()

# 		return super(View, self).eventFilter(widget, event)