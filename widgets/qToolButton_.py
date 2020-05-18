from PySide2 import QtCore, QtGui, QtWidgets

import sys

from widgets.qMenu_ import QMenu_

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



class QToolButton_(QtWidgets.QToolButton):
	'''
	'''
	def __init__(self, parent=None, showMenuOnMouseOver=False):
		super(QToolButton_, self).__init__(parent)

		menu = QMenu_(self)
		self.setMenu(menu)

		self.showMenuOnMouseOver=showMenuOnMouseOver
 
 		self.setArrowType(QtCore.Qt.RightArrow) #DownArrow,LeftArrow,NoArrow,RightArrow,UpArrow
		self.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly) #ToolButtonIconOnly,ToolButtonTextBesideIcon,ToolButtonTextOnly,ToolButtonTextUnderIcon
		self.setPopupMode(self.MenuButtonPopup) #DelayedPopup (default), MenuButtonPopup, InstantPopup


	def add(self, w, **kwargs):
		'''
		Add items to the toolbutton's menu.

		args:
			widget (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel
		kwargs:
			show (bool) = show the menu.
			insertSeparator (QAction) = insert separator in front of the given action.
		returns:
 			the added widget.

		ex.call:
		tb.add('QCheckBox', setText='Component Ring', setObjectName='chk000', setToolTip='Select component ring.')
		'''
		try:
			w = getattr(QtWidgets, w)() #ex. QtWidgets.QAction(self) object from string.
		except:
			if callable(w):
				w = widget() #ex. QtWidgets.QAction(self) object.

		w.setMinimumHeight(self.minimumSizeHint().height()+1) #set child widget height to that of the toolbutton

		w = self.menu().add(w, **kwargs)
		setattr(self, w.objectName(), w)
		return w


	def childWidgets(self, index=None):
		'''
		Get the widget at the given index.
		If no arg is given all widgets will be returned.

		args:
			index (int) = widget location.
		returns:
			(QWidget) or (list)
		'''
		return self.menu().childWidgets(index)


	def enterEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.showMenuOnMouseOver:
			self.menu().show()

		return QtWidgets.QToolButton.enterEvent(self, event)


	def leaveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.showMenuOnMouseOver:
			self.menu().hide()

		return QtWidgets.QToolButton.leaveEvent(self, event)


	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if not __name__=='__main__' and not hasattr(self, 'parentUiName'):
			self.parentUiName = self.window().sb.getUiName()
			self.childEvents = self.window().sb.getClassInstance('EventFactoryFilter')

			self.classMethod = self.window().sb.getMethod(self.parentUiName, self)
			if callable(self.classMethod):
				self.classMethod('setMenu')

		return QtWidgets.QToolButton.showEvent(self, event)









if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	b = QToolButton_()

	b.menu().add('QAction', setText='Action', insertSeparator=True)
	b.menu().add('QPushButton', setText='Button', insertSeparator=True)
	b.menu().add('QLabel', setText='Label', insertSeparator=True)

	b.show()
	# b.showMenu()
	sys.exit(app.exec_())






# deprecated ---------------------------------------------------

	# def mouseMoveEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QToolButton.mouseMoveEvent(self, event)


	# def mouseClickEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''
	# 	if event.button()==QtCore.Qt.LeftButton:
	# 		pass
	# 	elif event.button()==QtCore.Qt.MiddleButton:
	# 		pass
	# 	elif event.button()==QtCore.Qt.RightButton:
	# 		self.menu().show()

	# 	return QtWidgets.QToolButton.mouseClickEvent(self, event)