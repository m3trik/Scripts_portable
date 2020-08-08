from PySide2 import QtCore, QtGui, QtWidgets

from shared import Menu, Attributes, RichText



class QPushButton_Draggable(QtWidgets.QPushButton, Menu, Attributes, RichText):
	'''
	Draggable/Checkable pushbutton.
	'''

	__mousePressPos = QtCore.QPoint()

	def __init__(self, parent=None, **kwargs):
		super(QPushButton_Draggable, self).__init__(parent)

		self.setCheckable(True)

		self.setStyleSheet('''
			QPushButton {
				border: 1px solid transparent;
				background-color: rgba(127,127,127,2);
			}

			QPushButton::hover {
				background-color: rgba(127,127,127,2);
			}

			QPushButton:checked::hover {
				background-color: rgba(127,127,127,2);
			}''')

		self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

		self.setAttributes(kwargs)


	def setText(self, text):
		'''
		Override setText to support rich text formatting.

		args:
			text (str) = The desired widget text.
		'''
		self.setRichText(text)


	def text(self):
		'''
		Override text to support rich text formatting.

		returns:
			(str)
		'''
		return self.richText()


	def sizeHint(self):
		'''
		Override sizeHint to support rich text formatting.

		returns:
			(QSize)
		'''
		return self.richTextSizeHint()


	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if event.button()==QtCore.Qt.LeftButton:
			self.__mousePressPos = event.globalPos() #mouse positon at press.
			self.__mouseMovePos = event.globalPos() #mouse move position from last press. (updated on move event) 

			self.setChecked(True) #setChecked to prevent window from closing.
			self.window().preventHide = True

		if event.button()==QtCore.Qt.RightButton:
			self.contextMenu.show()

		return QtWidgets.QPushButton.mousePressEvent(self, event)


	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

		#move window:
		curPos = self.window().mapToGlobal(self.window().pos())
		globalPos = event.globalPos()
		diff = globalPos - self.__mouseMovePos

		self.window().move(self.window().mapFromGlobal(curPos + diff))
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
			self.window().preventHide = True
		else:
			self.setChecked(not self.isChecked()) #toggle check state

		self.window().preventHide = self.isChecked()
		self.window().hide()

		return QtWidgets.QPushButton.mouseReleaseEvent(self, event)









if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
		
	QPushButton_Draggable().show()
	sys.exit(app.exec_())



# --------------------------------
# Notes
# --------------------------------

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


# Deprecated ---------------------------------------------------------------


	# def showEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''

	# 	return QtWidgets.QPushButton.showEvent(self, event)


	# def add(self, w, **kwargs):
	# 	'''
	# 	Add items to the toolbutton's menu.

	# 	args:
	# 		widget (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel
	# 	kwargs:
	# 		show (bool) = show the menu.
	# 		insertSeparator (QAction) = insert separator in front of the given action.
	# 	returns:
 # 			the added widget.

	# 	ex.call:
	# 	tb.menu_.add('QCheckBox', setText='Component Ring', setObjectName='chk000', setToolTip='Select component ring.')
	# 	'''
	# 	try:
	# 		w = getattr(QtWidgets, w)() #ex. QtWidgets.QAction(self) object from string.
	# 	except:
	# 		if callable(w):
	# 			w = w() #ex. QtWidgets.QAction(self) object.

	# 	w.setMinimumHeight(self.minimumSizeHint().height()+1) #set child widget height to that of the toolbutton

	# 	w = self.contextMenu.add(w, **kwargs)
	# 	setattr(self, w.objectName(), w)
	# 	return w


	# def children_(self, index=None):
	# 	'''
	# 	Get the widget at the given index.
	# 	If no arg is given all widgets will be returned.

	# 	args:
	# 		index (int) = widget location.
	# 	returns:
	# 		(QWidget) or (list)
	# 	'''
	# 	return self.contextMenu.children_(index)


	# @property
	# def containsContextMenuItems(self):
	# 	'''
	# 	Query whether a menu has been constructed.
	# 	'''
	# 	if not self.children_():
	# 		return False
	# 	return True





		# if not __name__=='__main__' and not hasattr(self, 'parentUiName'):
		# 	p = self.parent()
		# 	while not hasattr(p.window(), 'sb'):
		# 		p = p.parent()

		# 	self.sb = p.window().sb
		# 	self.parentUiName = self.sb.getUiName()
		# 	self.childEvents = self.sb.getClassInstance('EventFactoryFilter')

		# 	self.classMethod = self.sb.getMethod(self.parentUiName, self)
		# 	if callable(self.classMethod):
		# 		if self.contextMenu:
		# 			self.classMethod('setMenu')