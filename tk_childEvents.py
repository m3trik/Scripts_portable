from __future__ import print_function
from PySide2 import QtCore, QtGui, QtWidgets
try:
	import shiboken2
except:
	from PySide2 import shiboken2

import os.path

from tk_styleSheet import StyleSheet



class EventFactoryFilter(QtCore.QObject):
	'''
	Event filter for dynamic ui objects.

	args:
		parent (obj) = parent widget.
	'''
	_mouseOver=[] #list of widgets currently under the mouse cursor.
	_mouseGrabber=None
	_mouseHover = QtCore.Signal(bool)
	_mousePressPos = QtCore.QPoint()

	enterEvent_ = QtCore.QEvent(QtCore.QEvent.Enter)
	leaveEvent_ = QtCore.QEvent(QtCore.QEvent.Leave)


	def __init__(self, parent):
		super(EventFactoryFilter, self).__init__(parent)

		self.tk = parent
		self.sb = self.tk.sb
		self.sb.setClassInstance(self)


	def initWidgets(self, name, widgets=None):
		'''
		Set Initial widget states.

		args:
			name (str) = ui name.
			widgets (str)(list) = <QWidgets> if no arg is given, the operation will be performed on all widgets of the given ui name.
		'''
		if widgets is None:
			widgets = self.sb.getWidget(name=name) #get all widgets for the given ui name.
		widgets = self.sb.list(widgets) #if 'widgets' isn't a list, convert it to one.

		for widget in widgets: #get all widgets for the given ui name.
			widgetName = self.sb.getWidgetName(widget, name)
			widgetType = self.sb.getWidgetType(widget, name) #get the class type as string.
			derivedType = self.sb.getDerivedType(widget, name) #get the derived class type as string.
			uiLevel = self.sb.getUiLevel(name)
			classMethod = self.sb.getMethod(name, widgetName)

			self.setStyleSheet_(name, widget)

			widgetTypes = [ #install an event filter on the given types.
				'QWidget', 
				'QAction', 
				'QLabel', 
				'QPushButton', 
				'QToolButton', 
				'QListWidget', 
				'QTreeWidget', 
				'QComboBox', 
				'QSpinBox',
				'QDoubleSpinBox',
				'QCheckBox',
				'QRadioButton',
				'QLineEdit',
				'QTextEdit',
				'QProgressBar',
				]

			if derivedType in widgetTypes:
				widget.installEventFilter(self)
				# print (widgetName if widgetName else widget)

				#type specific:
				if widgetType in ['QToolButton_', 'QPushButton_Draggable', 'QComboBox_', 'QTreeWidget_ExpandableList']:
					if callable(classMethod):
						classMethod('setMenu')

				if derivedType in ['QPushButton', 'QToolButton', 'QLabel']:
					if uiLevel<3:
						self.resizeAndCenterWidget(widget)

				elif derivedType=='QWidget':
					if self.sb.prefix(widget, 'w') and uiLevel==1: #prefix returns True if widgetName startswith the given prefix, and is followed by three integers.
						widget.setVisible(False)

			#finally, add any of the widget's children.
			exclude = ['QTreeWidget_ExpandableList'] #, 'QObject', 'QBoxLayout', 'QFrame', 'QAbstractItemView', 'QHeaderView', 'QItemSelectionModel', 'QItemDelegate', 'QScrollBar', 'QScrollArea', 'QValidator', 'QStyledItemDelegate', 'QPropertyAnimation'] #, 'QAction', 'QWidgetAction'
			[self.addWidgets(name, w) for w in widget.children() if w not in widgets and not widgetType in exclude]
			# print(name, [w.objectName() for w in widget.children() if w not in widgets and not widgetType in exclude])


	def addWidgets(self, name, widgets):
		'''
		Convenience method for adding additional widgets to the switchboard dict,
		and initializing them by setting connections, event filters, and stylesheets.

		args:
			name (str) = name of the parent ui.
			widgets (obj)(list) = widget or list of widgets.
		'''
		widgets = self.sb.list(widgets) #if 'widgets' isn't a list, convert it to one.

		self.sb.addWidgets(name, widgets)
		self.sb.connectSlots(name, widgets)
		self.initWidgets(name, widgets) #initialize the widget to set things like the event filter and styleSheet.


	def setStyleSheet_(self, name, widgets):
		'''
		Set the style sheet for the given widgets.

		args:
			name (str) = name of the parent ui.
			widgets (obj)(list) = widget or list of widgets.
		'''
		uiLevel = self.sb.getUiLevel(name)
		for widget in self.sb.list(widgets):
			derivedType = self.sb.getDerivedType(widget, name) #get the derived class type as string.
			if hasattr(widget, 'styleSheet'):
				s = getattr(StyleSheet, derivedType, '')
				if widget.size().width()<20:
					s = s+'{} {{padding: 0px 0px 0px 0px;}}'.format(derivedType) #remove padding on small sized widgets.
				if uiLevel==2 and not self.sb.prefix(widget, 'i'): #if submenu and objectName doesn't start with 'i':
					s = s+getattr(StyleSheet, 'dark') #override with the dark version on uiLevel 2 (submenus).
				if widget.styleSheet(): #if the widget has an existing style sheet, append.
					s = s+widget.styleSheet()
				widget.setStyleSheet(s)


	def resizeAndCenterWidget(self, widget, paddingX=30, paddingY=6):
		'''
		Adjust the given widget's size to fit contents and re-center.

		args:
			widget = <widget object> - widget to resize.
			paddingX (int) = additional width to be applied.
			paddingY (int) = additional height to be applied.
		'''
		p1 = widget.rect().center()
		widget.resize(widget.sizeHint().width()+paddingX, widget.sizeHint().height()+paddingY)
		p2 = widget.rect().center()
		diff = p1-p2
		widget.move(widget.pos()+diff)


	def mouseTracking(self, name):
		'''
		Get widget/s currently under cursor. Grab mouse, and send events accordingly.
		Send Enter event and grab mouse. (used to trigger widgets entered while in the mouse button down state)

		args:
			name (str) = ui name.
		'''
		# print([i.objectName() for i in self.sb.getWidget(name=name) if name=='cameras']), '---'
		ui = self.sb.getUi(name)
		widgetsUnderMouse=[] #list of widgets currently under the mouse cursor and their parents. in hierarchical order. ie. [[<widgets.qPushButton_.QPushButton_ object at 0x00000000045F6948>, <PySide2.QtWidgets.QMainWindow object at 0x00000000045AA8C8>, <__main__.Tk_max object at 0x000000000361F508>, <PySide2.QtWidgets.QWidget object at 0x00000000036317C8>]]
		for widget in self.sb.getWidget(name=name): #all widgets from the current ui.
			if not shiboken2.isValid(widget):
				self.sb.removeWidgets(widget) #remove any widgets from the main dict if the c++ object no longer exists.

			elif not hasattr(widget, 'rect'): #ignore any widgets not having the 'rect' attribute.
				pass

			else:
				try:
					widgetName = self.sb.getWidgetName(widget, name)
				except:
					self.addWidgets(name, widget) #initialize the widget to set things like the event filter and styleSheet.
					widgetName = self.sb.getWidgetName(widget, name)

				if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
					# print (widget.objectName(), 'mouseTracking')
					if not widget in self._mouseOver: #if widget is already in the mouseOver list, no need to re-process the events.
						QtWidgets.QApplication.sendEvent(widget, self.enterEvent_)
						self._mouseOver.append(widget)

						if not widgetName=='mainWindow':
							if widget.underMouse() and widget.isEnabled():
								parentWidgets = self.sb.getParentWidgets(widget)
								widgetsUnderMouse.append(parentWidgets)
				else:
					if widget in self._mouseOver: #if widget is in the mouseOver list, but the mouse is no longer over the widget:
						QtWidgets.QApplication.sendEvent(widget, self.leaveEvent_)
						self._mouseOver.remove(widget)
						if ui.mainWindow.isVisible():
							ui.mainWindow.grabMouse()
							self._mouseGrabber = ui.mainWindow
				

		widgetsUnderMouse.sort(key=len) #sort 'widgetsUnderMouse' by ascending length so that lowest level child widgets get grabMouse last.
		if widgetsUnderMouse:
			for widgetList in widgetsUnderMouse:
				widget = widgetList[0]
				widget.grabMouse() #set widget to receive mouse events.
				# print (widget.objectName())
				# print('grab:', widget.mouseGrabber().objectName(), '(tk_childEvents)')
				self._mouseGrabber = widget


	@staticmethod
	def createEventName(event):
		'''
		Get an event method name string from a given event.
		ie. 'enterEvent' from QtCore.QEvent.Type.Enter,
		ie. 'mousePressEvent' from QtCore.QEvent.Type.MouseButtonPress

		args:
			event = <QEvent>
		returns:
			'string' - formatted method name
		'''
		e = str(event.type()).split('.')[-1] #get the event name ie. 'Enter' from QtCore.QEvent.Type.Enter
		e = e[0].lower() + e[1:] #lowercase the first letter.
		e = e.replace('Button', '') #remove 'Button' if it exists.
		return e + 'Event' #add trailing 'Event'


	def eventFilter(self, widget, event):
		'''
		Forward widget events to event handlers.
		For any event type, the eventfilter will try to connect to a corresponding method derived
		from the event type string.  ie. self.enterEvent(event) from 'QtCore.QEvent.Type.Enter'
		This allows for forwarding of all events without each having to be explicity stated.

		args:
			widget = <QWidget>
			event = <QEvent>
		'''
		if not shiboken2.isValid(widget) or event.type()==QtCore.QEvent.Destroy:
			return False

		eventTypes = [ #types of events to be handled:
			'QEvent',
			'QChildEvent',
			'QResizeEvent',
			'QShowEvent',
			'QHideEvent',
			'QEnterEvent',
			'QLeaveEvent',
			'QKeyEvent',
			'QMouseEvent',
			'QMoveEvent',
			'QHoverEvent',
			'QContextMenuEvent',
			'QDragEvent',
			'QDropEvent',
		]

		if not any([event.__class__.__name__==e for e in eventTypes]): #do not process the event if it is not one of the types listed in 'eventTypes'
			# print(event.__class__.__name__)
			return False #;print(event.__class__.__name__)

		self.widget = widget
		self.name = self.sb.getUiNameFromWidget(self.widget) #get the name of the ui containing the given widget.
		# if not self.name: print('Error: tk_childEvents.eventFilter: getNameFrom(widget): {0} Failed on Event: {1} #'.format(self.widget.objectName(), str(event.type()).split('.')[-1]))
		self.widgetName = self.sb.getWidgetName(self.widget, self.name) #get the stored objectName string (pyside objectName() returns unicode).
		self.widgetType = self.sb.getWidgetType(self.widget, self.name)
		self.derivedType = self.sb.getDerivedType(self.widget, self.name)
		self.ui = self.sb.getUi(self.name)
		self.uiLevel = self.sb.getUiLevel(self.name)
		self.classMethod = self.sb.getMethod(self.name, self.widgetName)

		eventName = EventFactoryFilter.createEventName(event) #get 'mousePressEvent' from <QEvent>
		# print(self.name, eventName, self.widgetType, self.widgetName)


		if hasattr(self, eventName):
			getattr(self, eventName)(event) #handle the event locally. #ie. self.enterEvent(event)
			return super(EventFactoryFilter, self).eventFilter(widget, event)
		else:
			return False


	# ------------------------------------------------
	# Events
	# ------------------------------------------------
	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.widgetName=='mainWindow':
			self.widget.activateWindow()

		elif self.widgetName=='info':
			self.resizeAndCenterWidget(self.widget)

		if self.widgetType in ['QComboBox', 'QTreeWidget_ExpandableList']:
			try:
				self.classMethod()
			except (AttributeError, NameError, TypeError) as error:
				print(self.name, self.widgetName, error)

			if self.widgetType=='QTreeWidget_ExpandableList':
				self.addWidgets(self.name, self.widget.newWidgets) #removeWidgets=self.widget._gcWidgets.keys()


	def hideEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.widgetName=='mainWindow':
			if self._mouseGrabber:
				self._mouseGrabber.releaseMouse()
				self._mouseGrabber = None


	def enterEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self._mouseHover.emit(True)

		if self.widgetType=='QWidget':
			if self.sb.prefix(self.widget, 'w'):
				self.widget.setVisible(True) #set visibility

		elif self.derivedType=='QPushButton':
			if self.sb.prefix(self.widget, 'i'): #set the stacked widget.
				submenu = self.widget.whatsThis()+'_submenu'
				if not self.name==submenu: #do not reopen the submenu if it is already open.
					self.name = self.tk.setSubUi(self.widget, submenu)

			elif self.widgetName=='return_':
				self.tk.setPrevUi()

			elif self.sb.prefix(self.widget, 'chk'):
				if self.sb.getUiLevel(self.name)==2: #if submenu:
					self.widget.click()


	def leaveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self._mouseHover.emit(False)

		if self.widgetType=='QWidget':
			if self.sb.prefix(self.widget, 'w'):
				self.widget.setVisible(False) #set visibility


	def mousePressEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self._mousePressPos = event.globalPos() #mouse positon at press
		self.__mouseMovePos = event.globalPos() #mouse move position from last press


	def mouseMoveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if hasattr(self, '__mouseMovePos'):
			globalPos = event.globalPos()
			diff = globalPos -self.__mouseMovePos
			self.__mouseMovePos = globalPos


	def mouseReleaseEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.widget.underMouse(): #if self.widget.rect().contains(event.pos()): #if mouse over widget:
			if self.derivedType=='QPushButton' or self.derivedType=='QToolButton':
				if self.sb.prefix(self.widget, 'i'): #ie. 'i012'
					ui = self.tk.setUi(self.widget.whatsThis()) #switch the stacked layout to the given ui.
					self.tk.move(QtGui.QCursor.pos() - ui.rect().center()) #self.tk.ui.rect().center()) #move window to cursor position and offset from left corner to center

				elif self.sb.prefix(self.widget, 'v'):
					#add the buttons command info to the prevCamera list.
					method = self.sb.getMethod(self.name, self.widgetName)
					docString = self.sb.getDocString(self.name, self.widgetName)
					self.sb.prevCamera(allowCurrent=True, as_list=1).append([method, docString]) #store the camera view
					#send click signal on mouseRelease.
					self.widget.click()

				elif self.sb.prefix(self.widget, ['b','tb']):
					if self.sb.getUiLevel(self.name)==2: #if submenu:
						self.widget.click()
					#add the buttons command info to the prevCommand list.
					method = self.sb.getMethod(self.name, self.widgetName)
					docString = self.sb.getDocString(self.name, self.widgetName)
					self.sb.prevCommand(as_list=1).append([method, docString]) #store the command method object and it's docString (ie. 'Multi-cut tool')









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

# p1 = self.widget.mapToGlobal(self.widget.rect().center())

# 					submenu = self.widget.whatsThis()+'_submenu'
# 					n = self.widgetName
# 					if not self.name==submenu: #do not reopen submenu on enter event if it is already open.
# 						self.name = self.tk.setUi(submenu) #switch the stacked layout to the given submenu.
# 						self.widget = getattr(self.tk.currentWidget(), n) #get the widget with the same name in the new ui.


# 						p3 = self.tk.mapToGlobal(self.tk.pos())
# 						p2 = self.widget.mapToGlobal(self.widget.rect().center())
# 						self.tk.move(self.tk.mapFromGlobal(p3 +(p1 - p2)))



# print(name, self.sb.previousName(omitLevel=0, as_list=1)[-3])
					# if name==self.sb.previousName(omitLevel=0, as_list=1, allowDuplicates=1)[-3]: #if index is changed to the previous ui, remove the last widget.
						# del self.prevWidget[-1:]


#show button for any previous commands.
		# if self.sb.prefix(self.widget, 'v') and self.name=='main': #'v024-29'
		# 	self.widget.setText(self.sb.prevCommand(docString=1, as_list=1)[-num]) #prevCommand docString
		#  	#self.resizeAndCenterWidget(self.widget)
		# 	self.widget.show()