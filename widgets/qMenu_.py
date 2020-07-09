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



class QMenu_(QtWidgets.QMenu):
	'''
	args:
		widget (obj) = Setting a widget to this property allows the menu to be positioned in relation to a widget. If nothing is given, the parent widget is used.
		position (str) = Desired menu position relative to it's parent. 'cursorPos', 'topRight' etc.
	'''
	def __init__(self, parent=None, widget=None, position='topRight', **kwargs):
		super(QMenu_, self).__init__(parent)

		self.widget=widget
		self.position=position

		self._setAttributes(kwargs)
		# self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setStyleSheet('''
			QMenu {
				background-color: transparent;
				margin: 0px;
			}

			QMenu::item {
				padding: 0px 0px 0px 0px;
				border: 0px solid transparent;
			}''')


	@property
	def containsMenuItems(self):
		'''
		Query whether a menu has been constructed.
		'''
		if not self.children_():
			return False
		return True


	def _setAttributes(self, attributes=None, action=None, order=['show'], **kwargs):
		'''
		Internal use. Works with attributes passed in as a dict or kwargs.
		If attributes are passed in as a dict, kwargs are ignored.

		args:
			attributes (dict) = keyword attributes and their corresponding values.
			action (obj) = the child action or widgetAction to set attributes for. (default=None)
			#order (list) = list of string keywords. ie. ['move', 'show']. attributes in this list will be set last, by list order. an example would be setting move positions after setting resize arguments, or showing the widget only after other attributes have been set.
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
				getattr(action, attr)(value)

			except Exception as error:
				if type(error)==AttributeError:
					self._setCustomAttribute(action, attr, value)
				else:
					raise error


	def _setCustomAttribute(self, action, attr, value):
		'''
		Internal use. Custom attributes can be set using a trailing underscore convention to differentiate them from standard attributes.

		args:
			action (obj) = action (obj) = the child action or widgetAction to set attributes for.
			attr (str) = custom keyword attribute.
			value (str) = the value corresponding to the given attr.
		'''
		if attr=='show_': #show the menu immediately.
			self.show() # self.exec_() # self.popup()

		elif attr=='insertSeparator_':
			self.insertSeparator(action)

		elif attr=='setLayoutDirection_':
			self._setAttributes({'setLayoutDirection':getattr(QtCore.Qt, value)}, action)

		elif attr=='setAlignment_':
			self._setAttributes({'setAlignment':getattr(QtCore.Qt, value)}, action)

		elif attr=='setButtonSymbols_':
			self._setAttributes({'setButtonSymbols':getattr(QtWidgets.QAbstractSpinBox, value)}, action)

		#presets
		elif attr=='minMax_':
			minimum = float(value.split('-')[0])
			maximum = float(value.split('-')[1].split(' ')[0])
			step = float(value.split(' ')[1].strip('step'))

			self._setAttributes({'setMinimum':minimum, 'setMaximum':maximum, 'setSingleStep':step, 'setButtonSymbols_':'NoButtons'}, action)

		else:
			print('Error: {} has no attribute {}'.format(action, attr))


	def add(self, w, **kwargs):
		'''
		Add items to the QMenu.

		args:
			widget (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel
		kwargs:
			show_ (bool) = show the menu immediately.
			insertSeparator_ (bool) = insert a separator before the widget.
			setLayoutDirection_ (str) = ie. 'LeftToRight'
			setAlignment_ (str) = ie. 'AlignVCenter'
			setButtonSymbols_ (str) = ie. 'PlusMinus'
			minMax_ (str) = Set the min, max, and step values with a string. ie. '1-100 step.1'
		returns:
 			the added widget.

		ex.call:
		menu.add('QCheckBox', setText='Component Ring', setObjectName='chk000', setToolTip='Select component ring.')
		'''
		#get the widget
		try:
			w = getattr(QtWidgets, w)(self) #ex. QtWidgets.QAction(self) object from string.
		except:
			if callable(w):
				w = w() #ex. QtWidgets.QAction(self) object.

		type_ = w.__class__.__name__

		if type_=='QAction':
			a = self.addAction(w)
		elif w is not self:
			wAction = QtWidgets.QWidgetAction(self)
			# w = wAction.createWidget(a)
			wAction.setDefaultWidget(w)
			self.addAction(wAction)

		self._setAttributes(kwargs, w) #set any additional given keyword args for the widget.
		setattr(self, w.objectName(), w) #add the widget's objectName as a QMenu attribute.

		return w


	def addMenus(self, menus):
		'''
		Add multiple menus at once.

		args:
			menus (list) = list of menus.
		returns:
			(list) the menuAction() for each menu
		'''
		return [self.addMenu(m) for m in menus]


	def children_(self, index=None, exclude=['QAction', 'QWidgetAction'], include=[]):
		'''
		Get the widget at the given index.
		If no arg is given all widgets will be returned.

		args:
			index (int) = widget location.
		returns:
			(QWidget) or (list)
		'''
		children = [i for i in self.children() if not i.__class__.__name__ in exclude and i.__class__.__name__ in include if include]
		if index is not None:
			return children[index]
		return children


	def mouseMoveEvent(self, event):
		'''

		'''
		# if not self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
		# 	self.hide()

		return QtWidgets.QMenu.mouseMoveEvent(self, event)


	def leaveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self.hide()

		return QtWidgets.QMenu.leaveEvent(self, event)


	def hide(self, force=False):
		'''
		Hide the menu.
		'''
		if not force:
			for child in self.children():
				try:
					if child.view().isVisible():
						return
				except AttributeError:
					pass

		return super(QMenu_, self).hide()


	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		#set menu position
		if self.position is 'cursorPos':
			pos = QtGui.QCursor.pos() #global position
			self.move(pos.x()-self.width()/4, pos.y()-10) #move to cursor position and offset slightly.

		elif self.widget: #if a widget is specified:
			pos = getattr(self.widget.rect(), self.position)
			self.move(self.widget.mapToGlobal(pos()))

		elif self.parent(): #else; try to get the parent.
			pos = getattr(self.parent().rect(), self.position)
			self.move(self.parent().mapToGlobal(pos()))


		self.resize(self.sizeHint().width(), self.sizeHint().height())

		return QtWidgets.QToolButton.showEvent(self, event)









if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)

	m = QMenu_()
	m1 = QMenu_('Create')
	m1.add('QAction', setText='Action', insertSeparator=True)
	m1.add('QAction', setText='Action', insertSeparator=True)
	m1.add('QPushButton', setText='Button', insertSeparator=True)

	m2 = QMenu_('Cameras')
	m2.add('QAction', setText='Action', insertSeparator=True)
	m2.add('QAction', setText='Action', insertSeparator=True)
	m2.add('QPushButton', setText='Button', insertSeparator=True)
	m.addMenus([m1,m2])
	
	m.exec_(parent=None)

	sys.exit(app.exec_())





# depricated ------------------------------------------------------------------------


# if not __name__=='__main__' and not hasattr(self, 'parentUiName'):
# 	p = self.parent()
# 	try:
# 		while not hasattr(p.window(), 'sb'):
# 			p = p.parent()

# 		self.sb = p.window().sb
# 		self.parentUiName = self.sb.getUiName()
# 		self.childEvents = self.sb.getClassInstance('EventFactoryFilter')

# 		self.childEvents.addWidgets(self.parentUiName, self.children()+[self])
# 	except AttributeError:
# 		pass



			# integer
			# if value=='1-10 step1':
			# 	self._setAttributes({'setMinimum':1, 'setMaximum':10, 'setSingleStep':1, 'setButtonSymbols_':'NoButtons'}, action)
			# if value=='1-100 step1':
			# 	self._setAttributes({'setMinimum':1, 'setMaximum':100, 'setSingleStep':1, 'setButtonSymbols_':'NoButtons'}, action)
			# elif value=='1-180 step1':
			# 	self._setAttributes({'setMinimum':1, 'setMaximum':180, 'setSingleStep':1, 'setButtonSymbols_':'NoButtons'}, action)
			# elif value=='1-360 step1':
			# 	self._setAttributes({'setMinimum':1, 'setMaximum':360, 'setSingleStep':1, 'setButtonSymbols_':'NoButtons'}, action)
			# if value=='0-10000 step1':
			# 	self._setAttributes({'setMinimum':0, 'setMaximum':10000, 'setSingleStep':1, 'setButtonSymbols_':'NoButtons'}, action)
			# #float
			# elif value=='0.0-10 step.1':
			# 	self._setAttributes({'setMinimum':0.0, 'setMaximum':100.0, 'setSingleStep':0.1, 'setDecimals':1, 'setButtonSymbols_':'NoButtons'}, action)
			# elif value=='0.00-1 step.01':
			# 	self._setAttributes({'setMinimum':0.0, 'setMaximum':1.0, 'setSingleStep':0.01, 'setDecimals':2, 'setButtonSymbols_':'NoButtons'}, action)
			# elif value=='0.00-10 step.05':
			# 	self._setAttributes({'setMinimum':0.0, 'setMaximum':10.0, 'setSingleStep':0.05, 'setDecimals':2, 'setButtonSymbols_':'NoButtons'}, action)
			# elif value=='0.00-100 step.01':
			# 	self._setAttributes({'setMinimum':0.0, 'setMaximum':100.0, 'setSingleStep':0.01, 'setDecimals':2, 'setButtonSymbols_':'NoButtons'}, action)
			# elif value=='0.00-100 step1':
			# 	self._setAttributes({'setMinimum':0.0, 'setMaximum':100.0, 'setSingleStep':1, 'setDecimals':2, 'setButtonSymbols_':'NoButtons'}, action)
			# elif value=='0.000-10 step.001':
			# 	self._setAttributes({'setMinimum':0.0, 'setMaximum':10.0, 'setSingleStep':0.001, 'setDecimals':3, 'setButtonSymbols_':'NoButtons'}, action)