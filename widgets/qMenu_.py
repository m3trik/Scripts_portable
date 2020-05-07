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
		widget (obj) = Setting a widget to this property allows the menu to be positioned in relation to the widget. If nothing is given, the parent widget 
		position (str) = Desired menu position relative to it's parent.
	'''
	def __init__(self, parent=None, widget=None, position='topRight', **kwargs):
		super(QMenu_, self).__init__(parent)

		self.widget=widget
		self.position=position

		self.setAttributes(kwargs)
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


	def setAttributes(self, attributes=None, action=None, order=['show'], **kwargs):
		'''
		Works with attributes passed in as a dict or kwargs.
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
					self.setCustomAttribute(action, attr, value)
				else:
					raise error


	def setCustomAttribute(self, action, attr, value):
		'''
		Custom attributes can be set using a trailing underscore convention to differentiate them from standard attributes. ie. insertSeparator_=True

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
			self.setAttributes({'setLayoutDirection':getattr(QtCore.Qt, value)}, action)

		elif attr=='setAlignment_':
			self.setAttributes({'setAlignment':getattr(QtCore.Qt, value)}, action)

		elif attr=='setButtonSymbols_':
			self.setAttributes({'setButtonSymbols':getattr(QtWidgets.QAbstractSpinBox, value)}, action)

		#presets
		elif attr=='preset_':
			#integer
			if value=='1-100 step1':
				self.setAttributes({'setMinimum':1, 'setMaximum':100, 'setSingleStep':1, 'setButtonSymbols_':'NoButtons'}, action)
			elif value=='1-180 step1':
				self.setAttributes({'setMinimum':1, 'setMaximum':180, 'setSingleStep':1, 'setButtonSymbols_':'NoButtons'}, action)
			elif value=='1-360 step1':
				self.setAttributes({'setMinimum':1, 'setMaximum':360, 'setSingleStep':1, 'setButtonSymbols_':'NoButtons'}, action)
			if value=='0-10000 step1':
				self.setAttributes({'setMinimum':0, 'setMaximum':10000, 'setSingleStep':1, 'setButtonSymbols_':'NoButtons'}, action)
			#float
			elif value=='0.0-10 step.1':
				self.setAttributes({'setMinimum':0.0, 'setMaximum':100.0, 'setSingleStep':0.1, 'setDecimals':1, 'setButtonSymbols_':'NoButtons'}, action)
			elif value=='0.00-1 step.01':
				self.setAttributes({'setMinimum':0.0, 'setMaximum':1.0, 'setSingleStep':0.01, 'setDecimals':2, 'setButtonSymbols_':'NoButtons'}, action)
			elif value=='0.00-10 step.05':
				self.setAttributes({'setMinimum':0.0, 'setMaximum':10.0, 'setSingleStep':0.05, 'setDecimals':2, 'setButtonSymbols_':'NoButtons'}, action)
			elif value=='0.00-100 step.01':
				self.setAttributes({'setMinimum':0.0, 'setMaximum':100.0, 'setSingleStep':0.01, 'setDecimals':2, 'setButtonSymbols_':'NoButtons'}, action)
			elif value=='0.00-100 step1':
				self.setAttributes({'setMinimum':0.0, 'setMaximum':100.0, 'setSingleStep':1, 'setDecimals':2, 'setButtonSymbols_':'NoButtons'}, action)
			elif value=='0.000-10 step.001':
				self.setAttributes({'setMinimum':0.0, 'setMaximum':10.0, 'setSingleStep':0.001, 'setDecimals':3, 'setButtonSymbols_':'NoButtons'}, action)
		else:
			print('# Error: {} has no attribute {}'.format(action, attr))


	def add(self, w, **kwargs):
		'''
		Add items to the QMenu.

		args:
			widget (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel
		kwargs:
			show (bool) = show the menu.
			insertSeparator (QAction) = insert separator in front of the given action.
		returns:
 			the added widget.

		ex.call:
		menu.add('QCheckBox', setText='Component Ring', setObjectName='chk000', setToolTip='Select component ring.')
		'''
		#set widget
		try:
			w = getattr(QtWidgets, w)() #ex. QtWidgets.QAction(self) object from string.
		except:
			if callable(w):
				w = widget() #ex. QtWidgets.QAction(self) object.

		type_ = w.__class__.__name__

		if type_=='QAction':
			self.addAction(w)
		elif w is not self:
			wAction = QtWidgets.QWidgetAction(self)
			# w = wAction.createWidget(a)
			wAction.setDefaultWidget(w)
			self.addAction(wAction)

		self.setAttributes(kwargs, w) #set any additional given keyword args for the widget.

		return w


	def addMenus(self, menus):
		'''
		Add multiple menus at once.

		args:
			menus (list) = list of menus.
		returns:
			list. the menuAction() for each menu
		'''
		return [self.addMenu(m) for m in menus]


	def childWidgets(self, index=None):
		'''
		Get the widget at the given index.
		If no arg is given all widgets will be returned.

		args:
			index (int) = widget location.
		returns:
			(QWidget) or (list)
		'''
		children = [i for i in self.children() if not i.__class__.__name__ in ['QAction', 'QWidgetAction']]
		if index is not None:
			return children[index]
		return children


	def leaveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self.hide()

		return QtWidgets.QMenu.leaveEvent(self, event)


	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if not __name__=='__main__' and not hasattr(self, 'sb'):
			from tk_switchboard import sb
			self.sb = sb

			self.parentUiName = self.sb.getUiName()
			self.childEvents = self.sb.getClassInstance('EventFactoryFilter')

			self.childEvents.addWidgets(self.parentUiName, self.children()+[self])


		if self.widget: #if a widget is specified:
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

