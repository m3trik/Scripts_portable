from PySide2 import QtWidgets, QtCore

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



class QPushButton_(QtWidgets.QPushButton):
	'''
	
	'''
	def __init__(self, parent=None, **kwargs):
		super(QPushButton_, self).__init__(parent)

		self.setAttributes(kwargs)


	@property
	def containsContextMenuItems(self):
		'''
		Query whether a menu has been constructed.
		'''
		if not self.children_():
			return False
		return True


	def setAttributes(self, attributes=None, order=['globalPos', 'setVisible'], **kwargs):
		'''
		Works with attributes passed in as a dict or kwargs.
		If attributes are passed in as a dict, kwargs are ignored.
		args:
			attributes (dict) = keyword attributes and their corresponding values.
			#order (list) = list of string keywords. ie. ['move', 'show']. attributes in this list will be set last, in order of the list. an example would be setting move positions after setting resize arguments.
		kwargs:
			set any keyword arguments.
		'''
		if not attributes:
			attributes = kwargs

		for k in order:
			v = attributes.pop(k, None)
			if v:
				from collections import OrderedDict
				attributes = OrderedDict(attributes)
				attributes[k] = v

		for attr, value in attributes.items():
			try:
				getattr(self, attr)(value)

			except Exception as error:
				if type(error)==AttributeError:
					self.setCustomAttribute(attr, value)
				else:
					raise error


	def setCustomAttribute(self, attr, value):
		'''
		Handle custom keyword arguments.
		args:
			attr (str) = custom keyword attribute.
			value (str) = the value corresponding to the given attr.
		kwargs:
			copy (obj) = widget to copy certain attributes from.
			globalPos (QPoint) = move to given global location and center.
		'''
		if attr=='copy':
			self.setObjectName(value.objectName())
			self.resize(value.size())
			self.setText(value.text())
			self.setWhatsThis(value.whatsThis())

		if attr=='globalPos':
			self.move(self.mapFromGlobal(value - self.rect().center())) #move and center


	def contextMenu(self):
		'''
		Get the context menu.
		'''
		if not hasattr(self, '_menu'):
			self._menu = QMenu_(self, position='cursorPos')
		return self._menu


	def addToContext(self, w, **kwargs):
		'''
		Add items to the pushbutton's context menu.

		args:
			w (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel
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
				w = w() #ex. QtWidgets.QAction(self) object.

		w.setMinimumHeight(self.minimumSizeHint().height()+1) #set child widget height to that of the button

		w = self.contextMenu().add(w, **kwargs)
		setattr(self, w.objectName(), w)
		return w


	def children_(self, index=None):
		'''
		Get the widget at the given index.
		If no arg is given all widgets will be returned.

		args:
			index (int) = widget location.
		returns:
			(QWidget) or (list)
		'''
		return self.contextMenu().children_(index)


	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if event.button()==QtCore.Qt.RightButton:
			if self.contextMenu:
				self.contextMenu().show()

		return QtWidgets.QPushButton.mousePressEvent(self, event)


	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''

		return QtWidgets.QPushButton.showEvent(self, event)









if __name__ == "__main__":
	import sys
	from PySide2.QtCore import QSize
	app = QtWidgets.QApplication(sys.argv)
	w = QPushButton_(parent=None, setObjectName='b000', resize=QSize(45, 45), setText='QPushButton_', setWhatsThis='', setVisible=True)
	w.show()
	sys.exit(app.exec_())






# Deprecated ------------------------------------------------------

# if not __name__=='__main__' and not hasattr(self, 'parentUiName'):
# 	p = self.parent()
# 	while not hasattr(p.window(), 'sb'):
# 		p = p.parent()

# 	self.sb = p.window().sb
# 	self.parentUiName = self.sb.getUiName()
# 	self.classMethod = self.sb.getMethod(self.parentUiName, self)

# 	if callable(self.classMethod):
# 		if self.contextMenu:
# 			self.classMethod('setMenu')