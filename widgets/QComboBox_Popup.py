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



class ListView(QtWidgets.QListView):
	'''
	
	'''
	def __init__(self, parent=None):
		super(ListView, self).__init__()

		form = QtWidgets.QFormLayout(self)
		form.addRow(QtWidgets.QLabel('message'))
		form.addRow(self)
		model = QtGui.QStandardItemModel(self)

		# for item in items:
		# # 	# create an item with a caption
		# 	standardItem = QtGui.QStandardItem(item)
		# 	standardItem.setCheckable(True)
		# 	model.appendRow(standardItem)
		self.setModel(model)

		# buttonBox = QtGui.QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
		# form.addRow(buttonBox)
		# buttonBox.accepted.connect(self.accept)
		# buttonBox.rejected.connect(self.reject)



class QComboBox_Popup(QtWidgets.QComboBox):
	'''
	Under construction.
	'''
	def __init__(self, parent=None):
		super(QComboBox_Popup, self).__init__(parent)
	
		# self.listView = ListView()
		# self.setView(self.listView)



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
	# 	self.widget.setStyleSheet('''

	# 		}''')


	# def hidePopup(self):
	# 	self.widget.setStyleSheet('''
			
	# 		}''')



	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__showEvent'
		self.refreshContents()
		# # self.model()
		# self.listView

		# model = self.listView.model()

		# # items = [self.itemText(i) for i in range(self.count())]
		# items = ['1','2','3','4']
		# [model.item(i) for i in items]

		# model.item(0)
		# model.item(0).checkState()
		# model.item(0).text()

		return QtWidgets.QComboBox.showEvent(self, event)



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print '__mouseMoveEvent_1'
		# if not self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
			# self.hidePopup()

		return QtWidgets.QComboBox.mouseMoveEvent(self, event)



	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		print '__mouseReleaseEvent_1'
		self.showPopup()

		return QtWidgets.QComboBox.mouseReleaseEvent(self, event)



	def enterEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		print '__enterEvent'
		# self.showPopup()
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
		print '__leaveEvent'
		# self.hidePopup()
		self.setStyleSheet('''
			QComboBox {
				background-color: rgba(100,100,100,200);
				color: white;
			}''')

		return QtWidgets.QComboBox.leaveEvent(self, event)






if __name__ == "__main__":
	qApp = QtWidgets.QApplication(sys.argv)

	w = QComboBox_Popup()
	w.show()
	sys.exit(qApp.exec_())