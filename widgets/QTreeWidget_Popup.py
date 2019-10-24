#!/bin/env python
from PySide2 import QtCore, QtGui, QtWidgets

import sys



class Header(QtWidgets.QHeaderView):
	'''
	'''
	def __init__(self, orientation, parent=None):
		super(Header, self).__init__(orientation, parent)

		button = QtWidgets.QPushButton('Header', self)
		button = QtWidgets.QPushButton('Header2', self)
		self.Stretch #.Fixed .ResizeToContents .minimumSectionSize()
		self.setSectionHidden(0, True) #If hide is true the section specified by logicalIndex is hidden; otherwise the section is shown.
		print self.count()


class QTreeWidget_Popup(QtWidgets.QTreeWidget):
	'''
	'''
	def __init__(self, parent=None):
		super (QTreeWidget_Popup, self).__init__(parent)

		self.setHeader(Header(QtCore.Qt.Horizontal, self))
		self.setColumnCount(2)


	def addItems(self, items):
		for text in items:
			widget = QtWidgets.QPushButton(text, self)
			item = QtWidgets.QTreeWidgetItem(self, 1)
			self.setItemWidget(item, 1, widget)


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
 
		self.centralwidget = QtWidgets.QWidget(self)
		self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

		self.treeWidget = QTreeWidget_Popup(self.centralwidget)
		self.treeWidget.addItems(['button1', 'button2', 'button3', 'button4'])

		self.verticalLayout.addWidget(self.treeWidget)
		self.setCentralWidget(self.centralwidget)



if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)

	w = MainWindow()
	w.show()
	sys.exit(app.exec_())



# class TreeItem(QtWidgets.QTreeWidgetItem):
# 	'''
# 	Custom QTreeWidgetItem with Widgets
# 	args:
# 		parent = <QTreeWidget> - Item's QTreeWidget parent.
# 	''' 
# 	def __init__(self, items, parent=None):
# 		super(TreeItem, self).__init__(parent)

# 		treeWidget = self.treeWidget()
# 		for text in items:
# 			widget = QtWidgets.QPushButton()
# 			widget.setText(text)
# 			# self.addTopLevelItem(text)
# 			treeWidget.setItemWidget(self, 0, widget)

	# @property
	# def name(self):
	# 	'''
	# 	Return name (1st column text)
	# 	'''
	# 	return self.text(0)
 
	# @property
	# def value(self):
	# 	'''
	# 	Return value (2nd column int)
	# 	'''
	# 	return self.spinBox.value() 
 
	# def buttonPressed(self):
	# 	'''
	# 	Triggered when Item's button pressed.
	# 	an example of using the Item's own values.
	# 	'''
	# 	print "This Item name:%s value:%i" %(self.name, self.value)