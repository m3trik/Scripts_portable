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



class QTextEdit_(QtWidgets.QTextEdit):
	'''
	
	'''
	def __init__(self, parent=None):
		super(QTextEdit_, self).__init__(parent)

		self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

		self.setStyleSheet('''
			QTextEdit {
				background-color: transparent';
				color: white;
				selection-background-color: grey;
				selection-color: white;
				background-attachment: fixed; /* fixed, scroll */
		}''')
		
		self.viewport().setAutoFillBackground(False)
		self.setTextBackgroundColor(QtGui.QColor(50, 50, 50))



	def insertText(self, dict_):
		'''
		args:
			dict_ = {dict} - contents to add.  for each key if there is a value, the key and value pair will be added.
		'''
		highlight = QtGui.QColor(255, 255, 0)
		baseColor = QtGui.QColor(185, 185, 185)

		#populate the textedit with any values
		for key, value in dict_.items():
			if value:
				self.setTextColor(baseColor)
				self.append(key) #textEdit.append(key+str(value))
				self.setTextColor(highlight)
				self.insertPlainText(str(value))


	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''

		return QtWidgets.QTextEdit.showEvent(self, event)


	def hideEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.clear()

		return QtWidgets.QTextEdit.hideEvent(self, event)






if __name__ == "__main__":
	qApp = QtWidgets.QApplication(sys.argv)
		
	w = QTextEdit_()
	w.show()
	sys.exit(qApp.exec_())



# -----------------------------------------------
# Notes
# -----------------------------------------------

# if pm.progressBar ("tk_progressBar", query=1, isCancelled=1):
	# break
