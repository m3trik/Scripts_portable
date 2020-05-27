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



class QComboBox_(QtWidgets.QComboBox):
	'''
	
	'''
	def __init__(self, parent=None, popupStyle='modelView', **kwargs):
		super(QComboBox_, self).__init__(parent)
		'''
		args:
			popupStyle (str) = specify the type of popup menu. default is the standard 'modelView'.
		'''
		self.initialized=False
		self.popupStyle = popupStyle
		self.menu = QMenu_(self, position='bottomLeft')
		self.menu.visible=False #built-in method isVisible() not working.

		self.setAttributes(kwargs)


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


	def addToContext(self, w, title=None, **kwargs):
		'''
		Same as 'add', but instead adds items to the context menu.
		'''
		_menu=self.contextMenu()
		return self.add(w, title, _menu, **kwargs)


	def add(self, w, title=None, _menu=None, **kwargs):
		'''
		Add items to the comboboxes's custom menu (or it's standard modelView).

		args:
			w (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel
			title (str) = optional - header string at top when using standard model/view.
			_menu (obj) = menu to add to. typically internal use only.
		kwargs:
			show (bool) = show the menu.
			insertSeparator (QAction) = insert separator in front of the given action.
		returns:
 			the added widget.

		ex.call:
		tb.add('QCheckBox', setText='Component Ring', setObjectName='chk000', setToolTip='Select component ring.')
		'''
		if self.popupStyle=='modelView' and _menu is None:
			items = self.addItems_(w, title)
			return items

		try:
			w = getattr(QtWidgets, w)() #ex. QtWidgets.QAction(self) object from string.
		except:
			if callable(w):
				w = widget() #ex. QtWidgets.QAction(self) object.

		w.setMinimumHeight(self.minimumSizeHint().height()+1) #set child widget height to that of the toolbutton

		if _menu is None:
			_menu = self.menu
		w = _menu.add(w, **kwargs)
		setattr(self, w.objectName(), w)
		return w


	def addItems_(self, items, title=None):
		'''
		Add items to the combobox's standard modelView without triggering any signals.

		args:
			items (list) = list of strings to fill the comboBox with
			title (str) = optional value for the first index of the comboBox's list

		returns:
			comboBox's current item list minus any title.

		ex call: comboBox.addItems_(["Import file", "Import Options"], "Import")
		'''
		self.blockSignals(True) #to keep clear from triggering currentIndexChanged
		index = self.currentIndex() #get current index before refreshing list
		self.clear()

		items_ = [str(i) for i in [title]+items if i]
		self.addItems(items_) 

		self.setCurrentIndex(index)
		self.blockSignals(False)

		return items_


	def setCurrent_(self, i):
		'''
		Sets the current item from the given item text or index without triggering any signals.

		args:
			item (str)(int) = item text or item index
		'''
		self.blockSignals(True) #to keep clear from triggering currentIndexChanged

		if isinstance(i, int): #set by item index:
			self.setCurrentIndex(i)
		else: #set by item text string:
			self.setCurrentText(i)

		self.blockSignals(False)


	def menuItems(self):
		'''

		'''
		return [i for i in self.menu.children() if i.__class__.__name__ not in ['QAction', 'QWidgetAction']]


	def contextMenu(self):
		'''
		Get the context menu.
		'''
		if not hasattr(self, '_menu'):
			self._menu = QMenu_(self, position='cursorPos')
		return self._menu


	def childWidgets(self, index=None, contextMenu=False):
		'''
		Get the widget at the given index.
		If no arg is given all widgets will be returned.

		args:
			index (int) = widget location.
		returns:
			(QWidget) or (list)
		'''
		menuWidgets = self.menu.childWidgets(index)
		contextMenuWidgets = self.contextMenu().childWidgets(index)

		if contextMenu:
			return contextMenuWidgets
		if index is None:
			return menuWidgets + contextMenuWidgets
		else:
			return menuWidgets


	def showPopup(self):
		'''
		Show the popup menu.
		'''
		if not self.popupStyle=='modelView':
			if not self.menu.visible:
				self.menu.show()
				self.menu.visible=True
			else:
				self.menu.hide()
				self.menu.visible=False
		else:
			width = self.minimumSizeHint().width()
			self.view().setMinimumWidth(width)

			super(QComboBox_, self).showPopup()


	def hidePopup(self):
		if not self.popupStyle=='modelView':
			self.menu.hide()
			self.menu.visible=False
		else:
			super(QComboBox_, self).hidePopup()


	def enterEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''

		return QtWidgets.QComboBox.enterEvent(self, event)


	def leaveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# self.hidePopup()

		return QtWidgets.QComboBox.leaveEvent(self, event)


	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if event.button()==QtCore.Qt.RightButton:
			self.contextMenu().show()

		return QtWidgets.QComboBox.mousePressEvent(self, event)


	# def mouseDoubleClickEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''
	# 	if self.isEditable():
	# 		self.setEditable(False)
	# 	else:
	# 		self.setEditable(True)
	# 		print('mouseDoubleClickEvent')
	# 		self.lineEdit().installEventFilter(self)

	# 	return QtWidgets.QComboBox.mouseDoubleClickEvent(self, event)


	# def eventFilter(self, widget, event):
	# 	'''
	# 	Event filter for the lineEdit.
	# 	'''
	# 	if event.type()==QtCore.QEvent.MouseButtonDblClick:
	# 		pass
	# 	# print (event.type)
	# 	if event.type()==QtCore.QEvent.KeyPress:
	# 		print (widget, event, event.key())
	# 		if event.key()==QtCore.Qt.Key_Enter:
	# 			self.setEditable(False)

	# 	return super(QComboBox_, self).eventFilter(widget, event)


	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		try:
			if not __name__=='__main__':
				if callable(self.classMethod):
					self.classMethod()
		except:
			p = self.parent()
			while not hasattr(p.window(), 'sb'):
				p = p.parent()

			self.sb = p.window().sb
			self.parentUiName = self.sb.getUiName()
			self.classMethod = self.sb.getMethod(self.parentUiName, str(self.objectName()))

			if callable(self.classMethod):
				self.classMethod()
				self.initialized=True

		return QtWidgets.QComboBox.showEvent(self, event)









if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	w=QComboBox_(popupStyle='qmenu')
	w.show()
	sys.exit(app.exec_())



# -----------------------------------------------
# Notes
# -----------------------------------------------


	# def mouseMoveEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''
	# 	# print '__mouseMoveEvent_1'
	# 	if not self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
	# 		self.hidePopup()

	# 	return QtWidgets.QComboBox.mouseMoveEvent(self, event)



	# def mouseReleaseEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''
	# 	# print '__mouseReleaseEvent_1'
	# 	if self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
	# 		self.showPopup()

	# 	return QtWidgets.QComboBox.mouseReleaseEvent(self, event)
