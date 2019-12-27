from PySide2 import QtCore, QtGui, QtWidgets


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


When loading the ui file:
	from myfolder.mymodule import MyWidget
	uiLoader = QUiLoader()
	uiLoader.registerCustomWidget(MyWidget)
	main_window = uiLoader.load(file)

'''






class QComboBox_Checkable(QtWidgets.QComboBox):
	'''

	'''
	def __init__(self, parent=None):
		super(QComboBox_Checkable, self).__init__(parent)
		self.view().pressed.connect(self.handleItemPressed)
		self._changed = False



	def handleItemPressed(self, index):
		'''

		'''
		item = self.model().itemFromIndex(index)
		if item.checkState() == QtCore.Qt.Checked:
			item.setCheckState(QtCore.Qt.Unchecked)
		else:
			item.setCheckState(QtCore.Qt.Checked)
		self._changed = True



	def hidePopup(self):
		'''

		'''
		if not self._changed:
			super(CheckableComboBox, self).hidePopup()
		self._changed = False



	def itemChecked(self, index):
		'''

		'''
		item = self.model().item(index, self.modelColumn())
		return item.checkState() == QtCore.Qt.Checked



	def setItemChecked(self, index, checked=True):
		'''

		'''
		item = self.model().item(index, self.modelColumn())
		if checked:
			item.setCheckState(QtCore.Qt.Checked)
		else:
			item.setCheckState(QtCore.Qt.Unchecked)






if __name__ == "__main__":
	import sys
	qApp = QtWidgets.QApplication(sys.argv)
		
	w = QComboBox_Checkable()
	w.show()
	sys.exit(qApp.exec_())