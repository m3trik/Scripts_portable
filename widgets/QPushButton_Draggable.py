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



class QPushButton_Draggable(QtWidgets.QPushButton):
	'''
	Draggable/Checkable pushbutton.
	'''

	__mousePressPos = QtCore.QPoint()
	__sb = None

	def __init__(self, parent=None):
		super(QPushButton_Draggable, self).__init__(parent)

		self.setStyleSheet('''
			QPushButton {
				border: none;
			}

			QPushButton::checked {
				border: none;
			}''')

		self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.__mousePressPos = event.globalPos() #mouse positon at press.
		self.__mouseMovePos = event.globalPos() #mouse move position from last press. (updated on move event) 

		self.setChecked(True) #setChecked to prevent window from closing.

		return QtWidgets.QPushButton.mousePressEvent(self, event)



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

		#move window:
		curPos = self.tk.mapToGlobal(self.tk.pos())
		globalPos = event.globalPos()
		diff = globalPos -self.__mouseMovePos
		self.tk.move(self.tk.mapFromGlobal(curPos + diff))
		self.__mouseMovePos = globalPos

		return QtWidgets.QPushButton.mouseMoveEvent(self, event)



	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

		moveAmount = event.globalPos() -self.__mousePressPos

		if moveAmount.manhattanLength() >5: #if widget moved:
			self.setChecked(True) #setChecked to prevent window from closing.
		else:
			self.setChecked(not self.isChecked()) #toggle check state
			self.tk.hide_()

		return QtWidgets.QPushButton.mouseReleaseEvent(self, event)



	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if not self.__sb:
			try:
				from tk_switchboard import Switchboard
				self.__sb = Switchboard()
				self.tk = self.__sb.getClassInstance('tk')
			except Exception as error:
				print error

		return QtWidgets.QPushButton.showEvent(self, event)






if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
		
	w = QPushButton_Draggable()
	w.show()
	sys.exit(app.exec_())