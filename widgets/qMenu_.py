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
			
	returns:

	'''
	def __init__(self, parent=None, **kwargs):
		super(QMenu_, self).__init__(parent)

		self.setAttributes(kwargs)
		# self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating) #Show the widget without making it active.

		self.items=[]


	def setAttributes(self, attributes=None, action=None, w=None, order=['show'], **kwargs):
		'''
		Works with attributes passed in as a dict or kwargs.
		If attributes are passed in as a dict, kwargs are ignored.

		args:
			attributes (dict) = keyword attributes and their corresponding values.
			action (obj) = the child action or widgetAction to set attributes for. (default=None)
			w (str) = the string action or widgetAction type. ie. 'QAction' or 'QPushButton' (default=None)
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
					self.setCustomAttribute(action, w, attr, value)
				else:
					raise error


	def setCustomAttribute(self, action, w, attr, value):
		'''
		args:
			action (obj) = action (obj) = the child action or widgetAction to set attributes for.
			w (str) = the string action or widgetAction type. ie. 'QAction' or 'QPushButton'
			attr (str) = custom keyword attribute.
			value (str) = the value corresponding to the given attr.
		'''
		if attr=='show':
			# self.popup()
			# self.exec_()
			self.show()

		if attr=='insertSeparator':
			try:
				self.insertSeparator(action)
			except: pass


	def add(self, w, **kwargs):
		'''
		Add items to the menu.

		args:
			w (str)(obj) = widget. ie. 'QAction' or QtWidgets.QAction
		kwargs:
			show (bool) = show the menu.
			insertSeparator (QAction) = insert separator in front of the given action.

		ex.call: menu().add('QAction', setText='', insertSeparator=True)
		'''
		try:
			action = getattr(QtWidgets, w)(self) #ex. QtWidgets.QAction(self) object from string. parented to self.
		except:
			action = w(self) #ex. QtWidgets.QAction(self) object. parented to self.


		if w=='QAction':
			self.addAction(action)
		elif w is not self:
			wAction = QtWidgets.QWidgetAction(self)
			# action = wAction.createWidget(a)
			wAction.setDefaultWidget(action)
			self.addAction(wAction)


		#set any built-in attributes.
		self.setAttributes(kwargs, action, w)

		self.items.append(action)


		return action


	def addMenus(self, menus):
		'''
		Add multiple menus at once.

		args:
			menus (list) = list of menus.
		returns:
			list. the menuAction() for each menu
		'''
		return [self.addMenu(m) for m in menus]



	def clear(self):
		'''
		Clear the Menu and the items list.
		'''
		self.clear()
		self.items=[]

		return QtWidgets.QMenu.clear(self)


	def temp(self):
		print __name__




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

	# def showEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QMenu.showEvent(self, event)


	# def hide(self):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QMenu.hide(self)


	# def enterEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QMenu.enterEvent(self, event)


	# def leaveEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QMenu.leaveEvent(self, event)


	# def mouseMoveEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QMenu.mouseMoveEvent(self, event)


# class QMenu_(QtWidgets.QMenu):
# 	'''
# 	'''	
# 	def __init__(self, parent=None):
# 		super(QMenu_, self).__init__(parent)


# 		a1 = QtWidgets.QAction('Import mail', self) 
# 		self.addAction(a1)
		
# 		submenu = self.addMenu('menu')
# 		a2 = QtWidgets.QAction('submenu', self)
# 		submenu.addAction(a2)

# 		self.setGeometry(300, 300, 300, 200)
# 		self.setWindowTitle('Submenu')    






# if __name__ == '__main__':
# 	app = QtWidgets.QApplication(sys.argv)
# 	w = QMenu_('Import')
# 	w.show()

# 	sys.exit(app.exec_())

# we have two menu items; one is located in the File menu and the other one in the File's Import submenu.
# self = QMenu('Import', self)
# New menu is created with QMenu.

# action = QAction('Import mail', self) 
# self.addAction(action)
# An action is added to the submenu with addAction().




# OLD

# '''
# Promoting a widget in designer to use a custom class:
# >	In Qt Designer, select all the widgets you want to replace, 
# 		then right-click them and select 'Promote to...'. 

# >	In the dialog:
# 		Base Class:		Class from which you inherit. ie. QWidget
# 		Promoted Class:	Name of the class. ie. "MyWidget"
# 		Header File:	Path of the file (changing the extension .py to .h)  ie. myfolder.mymodule.mywidget.h

# >	Then click "Add", "Promote", 
# 		and you will see the class change from "QWidget" to "MyWidget" in the Object Inspector pane.
# '''



# class QMenu_(QtWidgets.QMenu):
# 	'''
# 	args:
			
# 	returns:

# 	'''
# 	def __init__(self, parent=None, **kwargs):
# 		super(QMenu_, self).__init__(parent)

# 		self.setAttributes(kwargs)

# 		self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating) #Show the widget without making it active.



# 	def setAttributes(self, attributes=None, action=None, type_=None, order=['show'], **kwargs):
# 		'''
# 		Works with attributes passed in as a dict or kwargs.
# 		If attributes are passed in as a dict, kwargs are ignored.

# 		args:
# 			attributes (dict) = keyword attributes and their corresponding values.
# 			action (obj) = the child action or widgetAction to set attributes for. (default=None)
# 			type_ (str) = the string action or widgetAction type. ie. 'QAction' or 'QPushButton' (default=None)
# 			#order (list) = list of string keywords. ie. ['move', 'show']. attributes in this list will be set last, by list order. an example would be setting move positions after setting resize arguments, or showing the widget only after other attributes have been set.
# 		kwargs:
# 			set any keyword arguments.
# 		'''
# 		if not attributes:
# 			attributes = kwargs

# 		for k in order:
# 			v = attributes.pop(k, None)
# 			if v:
# 				from collections import OrderedDict
# 				attributes = OrderedDict(attributes)
# 				attributes[k] = v

# 		for attr, value in attributes.items():
# 			try:
# 				getattr(action, attr)(value)

# 			except Exception as error:
# 				if type(error)==AttributeError:
# 					self.setCustomAttribute(action, type_, attr, value)
# 				else:
# 					raise error


# 	def setCustomAttribute(self, action, type_, attr, value):
# 		'''
# 		args:
# 			action (obj) = action (obj) = the child action or widgetAction to set attributes for.
# 			type_ (str) = the string action or widgetAction type. ie. 'QAction' or 'QPushButton'
# 			attr (str) = custom keyword attribute.
# 			value (str) = the value corresponding to the given attr.
# 		'''
# 		if attr=='show':
# 			self.show()

# 		if attr=='insertSeparator':
# 			try:
# 				self.insertSeparator(action)
# 			except: pass


# 	def add(self, **kwargs):
# 		'''
# 		Add items to the menu.

# 		kwargs:
# 			show (bool) = show the menu.
# 			insertSeparator (QAction) = insert separator in front of the given action.

# 		ex.call: menu().add(type_='QAction', setText='', insertSeparator=True)
# 		'''
# 		type_ = kwargs.pop('type_')

# 		try:
# 			action = getattr(QtWidgets, type_)(self) #ex. QtWidgets.QAction(self) object from string. parented to self.
# 		except:
# 			if callable(type_):
# 				action = type_(self) #ex. QtWidgets.QAction(self) object. parented to self.
# 			else:
# 				action = type_ #ex. self object. not parented.
		
# 		if type_=='QAction':
# 			self.addAction(action)
# 		elif type_ is not self:
# 			wAction = QtWidgets.QWidgetAction(self)
# 			# action = wAction.createWidget(a)
# 			wAction.setDefaultWidget(action)
# 			self.addAction(wAction)


# 		#set any built-in attributes.
# 		self.setAttributes(kwargs, action, type_)


# 			#a.colorSelected.connect(self.clicked_color)
# 			#button.action.trigger()
# 			#button.triggered.connect(self.close)



# 	def showEvent(self, event):
# 		'''
# 		args:
# 			event = <QEvent>
# 		'''

# 		return QtWidgets.QMenu.showEvent(self, event)


# 	def hide(self):
# 		'''
# 		args:
# 			event = <QEvent>
# 		'''
# 		if self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())): #if not mouse over widget:
# 			return

# 		return QtWidgets.QMenu.hide(self)


# 	def enterEvent(self, event):
# 		'''
# 		args:
# 			event = <QEvent>
# 		'''
# 		print 'enterEvent'

# 		return QtWidgets.QMenu.enterEvent(self, event)


# 	def leaveEvent(self, event):
# 		'''
# 		args:
# 			event = <QEvent>
# 		'''
# 		self.hide()

# 		return QtWidgets.QMenu.leaveEvent(self, event)


# 	def mouseMoveEvent(self, event):
# 		'''
# 		args:
# 			event = <QEvent>
# 		'''
# 		if not self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())): #if not mouse over self:
# 			print self.mouseGrabber(), '0'
# 			self.parent().grabMouse()
# 			# self.parent().window().grabMouse()
# 			# self.releaseMouse()
# 			# self.parent().window().activateWindow()
# 		else:
# 			print self.mouseGrabber(),'1'
# 			self.grabMouse()
# 			# self.activateWindow()

# 		return QtWidgets.QMenu.mouseMoveEvent(self, event)






# if __name__ == "__main__":
# 	import sys
# 	app = QtWidgets.QApplication(sys.argv)
# 	m = QMenu_(show=True)

# 	m.add(type_='QAction', setText='Action', insertSeparator=True)
# 	m.add(type_='QPushButton', setText='Button', insertSeparator=True)
# 	m.add(type_='QLabel', setText='Label', insertSeparator=True)
# 	sys.exit(app.exec_())