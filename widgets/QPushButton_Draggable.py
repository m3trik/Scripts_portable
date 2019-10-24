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
				background: rgba(100,100,100,50);
			}
			QPushButton::checked {
				border: none;
				background-color: rgba(82,133,166,200);
			}''')

		self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.__mousePressPos = event.globalPos() #mouse positon at press.
		self.__mouseMovePos = event.globalPos() #mouse move position from last press. (updated at move event) 

		self.setChecked(True) #setChecked to prevent window from closing.

		return QtWidgets.QPushButton.mousePressEvent(self, event)



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

		#move window:
		curPos = self.hotBox.mapToGlobal(self.hotBox.pos())
		globalPos = event.globalPos()
		diff = globalPos -self.__mouseMovePos
		self.hotBox.move(self.hotBox.mapFromGlobal(curPos + diff))
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
			self.hotBox.hide_()

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
				self.hotBox = self.__sb.getClassInstance('hotBox')
			except Exception as error:
				print error

		return QtWidgets.QPushButton.showEvent(self, event)






if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
		
	w = QPushButton_Draggable()
	w.show()
	sys.exit(app.exec_())