from PySide2 import QtCore, QtGui, QtWidgets

from shared import Attributes



class QMenu_(QtWidgets.QMenu, Attributes):
	'''
	args:
		position (str)(obj) = Desired menu position relative to it's parent. 
						valid values are: 'cursorPos', 'center', 'top', 'bottom', 'right', 'left', 
						'topLeft', 'topRight', 'bottomRight', 'bottomLeft', or <QWidget>. Setting a widget to this property, positions the menu in relation to the given widget.
	'''
	def __init__(self, parent=None, position='bottomLeft', **kwargs):
		super(QMenu_, self).__init__(parent)

		self.position=position

		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		self.setStyleSheet('''
			QMenu {
				background-color: rgba(127,127,127,175);
				border: 1px solid white;
				padding: 10px 10px 10px 10px;
				margin: 5px;
			}

			QMenu::item {
				background-color: transparent;
				spacing: 0px;
				border: 1px solid transparent;
				margin: 0px;
			}''')

		self.setAttributes(kwargs)


	@property
	def containsMenuItems(self):
		'''
		Query whether a menu has been constructed.
		'''
		if not self.children_():
			return False
		return True


	def add(self, w, **kwargs):
		'''
		Add items to the QMenu.

		args:
			widget (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel

		kwargs:
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
			w = getattr(QtWidgets, w)(self) #ie. QtWidgets.QAction(self) object from string.
		except:
			if callable(w):
				w = w(self) #ie. QtWidgets.QAction(self) object.

		self.setAttributes(kwargs, w) #set any additional given keyword args for the widget.

		type_ = w.__class__.__name__

		if type_=='QAction': #
			a = self.addAction(w)

		else: #
			wAction = QtWidgets.QWidgetAction(self)
			wAction.setDefaultWidget(w)
			self.addAction(wAction)

			w.setMinimumSize(w.sizeHint().width(), 20) #self.parent().minimumSizeHint().height()+1) #set child widget height to that of the toolbutton]

			setattr(self, w.objectName(), w) #add the widget's objectName as a QMenu attribute.

			#connect to 'setLastActiveChild' when signal activated.
			if hasattr(w, 'released'):
				w.released.connect(lambda widget=w: self.setLastActiveChild(widget))
			elif hasattr(w, 'valueChanged'):
				w.valueChanged.connect(lambda value, widget=w: self.setLastActiveChild(value, widget))

		return w


	def children_(self, index=None, include=[], exclude=['QAction', 'QWidgetAction', 'QHBoxLayout', 'QVBoxLayout']):
		'''
		Get a list of the menu's child objects, excluding those types listed in 'exclude'.

		args:
			index (int) = return the child widget at the given index.
			exclude (list) = Widget types to exclude from the returned results.
			include (list) = Widget types to include in the returned results. All others will be omitted. Exclude takes dominance over include. Meaning, if a widget is both in the exclude and include lists, it will be excluded.

		returns:
			(obj)(list) child widgets or child widget at given index.
		'''
		children = [i for i in self.children() 
				if i.__class__.__name__ not in exclude 
				and (i.__class__.__name__ in include if include else i.__class__.__name__ not in include)]

		if index is not None:
			try:
				children = children[index]
			except IndexError:
				children = None
		return children


	def setLastActiveChild(self, widget, *args, **kwargs):
		'''
		Set the given widget as the last active.
		Maintains a list of the last 10 active child widgets.

		args:
			widget = Widget to set as last active. The widget can later be returned by calling the 'lastActiveChild' method.
			*args **kwargs = Any additional arguments passed in by the wiget's signal during a connect call.

		returns:
			(obj) widget.
		'''
		# widget = args[-1]

		if not hasattr(self, '_lastActiveChild'):
			self._lastActiveChild = []

		del self._lastActiveChild[11:] #keep the list length at 10 elements.

		self._lastActiveChild.append(widget)
		# print(args, kwargs, widget.objectName() if hasattr(widget, 'objectName') else None)
		return self._lastActiveChild[-1]


	def lastActiveChild(self, name=False, as_list=False):
		'''
		Get the given widget set as last active.
		Contains a list of the last 10 active child widgets.

		args:
			name (bool) = Return the last active widgets name as a string.

		returns:
			(obj) widget or (str) widget name.

		ex. slot connection to the last active child widget:
			cmb.returnPressed.connect(lambda m=cmb.contextMenu.lastActiveChild: getattr(self, m(name=1))()) #connect to the last pressed child widget's corresponding method after return pressed. ie. self.lbl000 if cmb.lbl000 was clicked last.
		'''
		if not hasattr(self, '_lastActiveChild'):
			return None

		if name:
			lastActive = str(self._lastActiveChild[-1].objectName())
		elif name and as_list:
			lastActive = [str(w.objectName()) for w in self._lastActiveChild]
		elif as_list:
			lastActive = [w for w in self._lastActiveChild]
		else:
			lastActive = self._lastActiveChild[-1]

		return lastActive


	def contextMenuToolTip(self):
		'''
		Creates an html formatted toolTip combining the toolTips of any context menu items.

		returns:
			(str) formatted toolTip.
		'''
		if not hasattr(self, '_contextMenuToolTip'):
			self._contextMenuToolTip=''
			menuItems = self.children_()
			if menuItems:
				self._contextMenuToolTip = '<br><br><u>Context menu items:</u>'
				for menuItem in menuItems:
					try:
						self._contextMenuToolTip = '{0}<br>  <b>{1}</b> - {2}'.format(self._contextMenuToolTip, menuItem.text(), menuItem.toolTip())
					except AttributeError:
						pass

		return self._contextMenuToolTip


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
			self.move(pos.x()-self.width()/4-10, pos.y()-20) #move to cursor position and offset slightly.

		elif not isinstance(self.position, (type(None), str, unicode)): #if self.position is a widget:
			pos = getattr(self.positionRelativeTo.rect(), self.position)
			self.move(self.positionRelativeTo.mapToGlobal(pos()))

		elif self.parent(): #if parent: map to parent in the given position. default is 'bottomLeft'
			pos = getattr(self.parent().rect(), self.position)
			pos = self.parent().mapToGlobal(pos())
			self.move(pos.x()-16, pos.y()-2)

		#resize the menu
		width = self.sizeHint().width()
		if self.parent():
			parentWidth = self.parent().size().width()
			if parentWidth>width:
				width = parentWidth

		self.setMinimumSize(width, self.sizeHint().height()+5)

		return QtWidgets.QToolButton.showEvent(self, event)









if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)

	# create parent menu containing two submenus:
	m = QMenu_(position='cursorPos', setVisible=True)
	m1 = QMenu_('Create', addMenu_=m)
	m1.add('QAction', setText='Action', insertSeparator_=True)
	m1.add('QAction', setText='Action', insertSeparator_=True)
	m1.add('QPushButton', setText='Button')

	m2 = QMenu_('Cameras', addMenu_=m)
	m2.add('QAction', setText='Action', insertSeparator_=True)
	m2.add('QAction', setText='Action', insertSeparator_=True)
	m2.add('QPushButton', setText='Button')

	# m.exec_(parent=None)
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

# depricated ------------------------------------------------------------------------


	# def addMenus(self, menus):
	# 	'''
	# 	Add multiple menus at once.

	# 	args:
	# 		menus (list) = list of menus.

	# 	returns:
	# 		(list) the menuAction() for each menu

	# 	ex. usage: 
	# 	m = QMenu_(position='cursorPos', setVisible=True)
	# 	m1 = QMenu_('Create', addMenu=m)
	# 	m2 = QMenu_('Cameras', addMenu=m)
	# 	m.addMenus([m1,m2])
	# 	'''
	# 	return [self.addMenu(m) for m in menus]


# @property
# 	def containsContextMenuItems(self):
# 		'''
# 		Query whether a menu has been constructed.
# 		'''
# 		if not self.children_(contextMenu=True):
# 			return False
# 		return True


	# def addToContext(self, w, **kwargs):
	# 	'''
	# 	Add items to the pushbutton's context menu.

	# 	args:
	# 		w (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel
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

	# 	w.setMinimumHeight(self.minimumSizeHint().height()+1) #set child widget height to that of the button

	# 	w = self.contextMenu.add(w, **kwargs)
	# 	setattr(self, w.objectName(), w)
	# 	return w



	# def setAttributes(self, attributes=None, action=None, order=['globalPos', 'setVisible'], **kwargs):
	# 	'''
	# 	Internal use. Works with attributes passed in as a dict or kwargs.
	# 	If attributes are passed in as a dict, kwargs are ignored.

	# 	args:
	# 		attributes (dict) = keyword attributes and their corresponding values.
	# 		action (obj) = the child action or widgetAction to set attributes for. (default=None)
	# 		#order (list) = list of string keywords. ie. ['move_', 'setVisible']. attributes in this list will be set last, by list order. an example would be setting move positions after setting resize arguments, or showing the widget only after other attributes have been set.

	# 	kwargs:
	# 		set any keyword arguments.
	# 	'''
	# 	if not attributes:
	# 		attributes = kwargs

	# 	if action is None:
	# 		action = self

	# 	for k in order:
	# 		v = attributes.pop(k, None)
	# 		if v:
	# 			from collections import OrderedDict
	# 			attributes = OrderedDict(attributes)
	# 			attributes[k] = v

	# 	for attr, value in attributes.items():
	# 		try:
	# 			getattr(action, attr)(value)

	# 		except AttributeError:
	# 			self.setCustomAttribute(action, attr, value)


	# def setCustomAttribute(self, action, attr, value):
	# 	'''
	# 	Internal use. Custom attributes can be set using a trailing underscore convention to differentiate them from standard attributes.

	# 	args:
	# 		action (obj) = action (obj) = the child action or widgetAction to set attributes for.
	# 		attr (str) = custom keyword attribute.
	# 		value (str) = the value corresponding to the given attr.

	# 	attributes:
	# 		copy (obj) = widget to copy certain attributes from.
	# 		globalPos (QPoint) = move to given global location and center.
	# 		insertSeparator_ (bool) = insert a line separater before the new widget.
	# 		setLayoutDirection_ (str) = set the layout direction using a string value. ie. 'LeftToRight'
	# 		setAlignment_ (str) = set the alignment using a string value. ie. 'AlignVCenter'
	# 		setButtonSymbols_ (str) = set button symbols using a string value. ex. ie. 'PlusMinus'
	# 		minMax_ (str) = set the min, max, and step value using a string value. ex. '.01-10 step.1'
	# 	'''
	# 	if attr=='copy':
	# 		self.setObjectName(value.objectName())
	# 		self.resize(value.size())
	# 		self.setText(value.text())
	# 		self.setWhatsThis(value.whatsThis())

	# 	elif attr=='globalPos':
	# 		self.move(self.mapFromGlobal(value - self.rect().center())) #move and center

	# 	elif attr=='insertSeparator_':
	# 		if action.__class__.__name__=='QAction':
	# 			self.insertSeparator(action)

	# 	elif attr=='setLayoutDirection_':
	# 		self.setAttributes({'setLayoutDirection':getattr(QtCore.Qt, value)}, action)

	# 	elif attr=='setAlignment_':
	# 		self.setAttributes({'setAlignment':getattr(QtCore.Qt, value)}, action)

	# 	elif attr=='setButtonSymbols_':
	# 		self.setAttributes({'setButtonSymbols':getattr(QtWidgets.QAbstractSpinBox, value)}, action)

	# 	#presets
	# 	elif attr=='minMax_':
	# 		self.setMinMax(action, value)

	# 	elif attr=='setSpinBoxByValue_':
	# 		self.setByValue(action, value[0], value[1])

	# 	else:
	# 		print('Error: {} has no attribute {}'.format(action, attr))


	# def setMinMax(self, spinbox, value):
	# 	'''
	# 	Set the minimum, maximum, and step values for a spinbox using a shorthand string value.

	# 	args:
	# 		spinbox (obj) = spinbox widget.
	# 		value (str) = value as shorthand string. ie. '0.00-100 step1'
	# 	'''
	# 	minimum = float(value.split('-')[0])
	# 	maximum = float(value.split('-')[1].split(' ')[0])
	# 	step = float(value.split(' ')[1].strip('step'))

	# 	self.setAttributes({
	# 		'setMinimum':minimum, 
	# 		'setMaximum':maximum, 
	# 		'setSingleStep':step, 
	# 		'setButtonSymbols_':'NoButtons',
	# 	}, spinbox)


	# def setByValue(self, spinbox, attribute, value):
	# 	'''
		
	# 	args:
	# 		spinbox (obj) = spinbox widget.
	# 		attribute (str) = object attribute.
	# 		value (multi) = attribute value.
	# 	'''
	# 	prefix = attribute+': '
	# 	suffix = spinbox.suffix()
	# 	minimum = spinbox.minimum()
	# 	maximum = spinbox.maximum()
	# 	step = spinbox.singleStep()
	# 	decimals = spinbox.decimals()

	# 	if isinstance(value, float):
	# 		decimals = str(value)[::-1].find('.') #get decimal places

	# 	elif isinstance(value, int):
	# 		decimals = 0

	# 	elif isinstance(value, bool):
	# 		value = int(value)
	# 		minimum = 0
	# 		maximum = 1

	# 	self.setAttributes({
	# 		'setValue':value,
	# 		'setPrefix':prefix,
	# 		'setSuffix':suffix,
	# 		'setMinimum':minimum, 
	# 		'setMaximum':maximum, 
	# 		'setSingleStep':step, 
	# 		'setDecimals':decimals,
	# 		'setButtonSymbols_':'NoButtons',
	# 	}, spinbox)


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

# 	self.setAttributes({'setMinimum':0.0, 'setMaximum':10.0, 'setSingleStep':0.001, 'setDecimals':3, 'setButtonSymbols_':'NoButtons'}, action)