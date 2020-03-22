from __future__ import print_function
from PySide2 import QtCore, QtGui, QtWidgets

import os.path

from tk_switchboard import sb
from tk_styleSheet import StyleSheet





class EventFactoryFilter(QtCore.QObject):
	'''
	Event filter for dynamic ui objects.

	args:
		parent=<parent>
	'''
	_mouseOver = [] #list of widgets currently under the mouse cursor.
	_mouseGrabber = None
	_mouseHover = QtCore.Signal(bool)
	_mousePressPos = QtCore.QPoint()

	enterEvent_ = QtCore.QEvent(QtCore.QEvent.Enter)
	leaveEvent_ = QtCore.QEvent(QtCore.QEvent.Leave)


	def __init__(self, parent=None):
		super(EventFactoryFilter, self).__init__(parent)

		sb.setClassInstance(self)

		if parent:
			self.parent = parent



	def initWidget(self, name, widgets=None):
		'''
		Set Initial widget states.

		args:
			name (str) = ui name.
			widgets (str)(list) = <QWidgets> if no arg is given, the operation will be performed on all widgets of the given ui name.
		'''
		if not widgets:
			widgets = sb.getWidget(name=name)
		elif not type(widgets)==list:
			widgets = [widgets]

		for widget in widgets: #get all widgets for the given ui name.
			widgetName = widget.objectName()
			widgetType = sb.getWidgetType(widget, name) #get the class type as string.
			derivedType = sb.getDerivedType(widget, name) #get the derived class type as string.

			uiLevel = sb.getUiLevel(name)

			if hasattr(widget,'styleSheet') and not widget.styleSheet(): #if the widget can be assigned a stylesheet, and doesn't already have one:
				if uiLevel==2 and not sb.prefix(widgetName, 'i'): #if submenu and objectName doesn't start with 'i':
					widget.setStyleSheet(getattr(StyleSheet, 'submenu', ''))
				else:
					widget.setStyleSheet(getattr(StyleSheet, derivedType, ''))			

			widget.installEventFilter(self)


			if widgetType=='QPushButton' and uiLevel<3:
				if not '|' in widgetName:
					self.resizeAndCenterWidget(widget)

			elif widgetType=='QWidget':
				if sb.prefix(widgetName, 'r'): #prefix returns True if widgetName startswith the given prefix, and is followed by three integers.
					widget.setVisible(False)

			elif widgetType=='QDoubleSpinBox':
				if name=='create':
					if sb.prefix(widgetName, 's'):
						widget.setVisible(False)



	def initWidgetItems(self, items, name):
		'''
		Store widget items in the switchboard dict for referencing.
		Set Event filters, stylesheets, and connections for the items.

		args:
			name (str) = name of the parent ui.
			items (list) = widget objects.
		'''
		try:
			sb.addWidgets(name, items)
			self.initWidget(name, items) #initialize the widget to set things like the event filter and styleSheet.
		except Exception as error:
			print(error)



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
		# print([i.objectName() for i in sb.getWidget(name=name) if name=='cameras']), '---'
		for widget in sb.getWidget(name=name): #get all widgets from the current ui.
			widgetName = widget.objectName()

			if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
				if not widget in self._mouseOver: #if widget is already in the mouseOver list, no need to re-process the events.
					QtWidgets.QApplication.sendEvent(widget, self.enterEvent_)
					self._mouseOver.append(widget)

					if not widgetName=='mainWindow':
						# if '|' not in widgetName:
						widget.grabMouse() #set widget to receive mouse events.
						self._mouseGrabber = widget

			else:
				if widget in self._mouseOver: #if widget is in the mouseOver list, but the mouse is no longer over the widget:
					QtWidgets.QApplication.sendEvent(widget, self.leaveEvent_)
					self._mouseOver.remove(widget)
					if self.ui.mainWindow.isVisible():
						self.ui.mainWindow.grabMouse()
						self._mouseGrabber = self.ui.mainWindow



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
			return False
		# print(event.__class__.__name__)


		self.widget = widget
		self.name = sb.getNameFrom(self.widget) #get the name of the ui containing the given widget.
		if not self.name:
			print('# Error: tk_childEvents.eventFilter: getNameFrom(widget): {0} Failed on Event: {1} #'.format(self.widget.objectName(), str(event.type()).split('.')[-1]))
			return False
		self.widgetName = self.widget.objectName()
		self.widgetType = sb.getWidgetType(self.widget, self.name)
		self.derivedType = sb.getDerivedType(self.widget, self.name)
		self.ui = sb.getUi(self.name)
		self.uiLevel = sb.getUiLevel(self.name)

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

		if self.widgetName=='info':
			self.resizeAndCenterWidget(self.widget)

		if self.derivedType=='QComboBox':
			method = sb.getMethod(self.name, self.widgetName)
			if callable(method):
				method()



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
			if sb.prefix(self.widgetName, 'r'):
				self.widget.setVisible(True) #set visibility

		elif self.derivedType=='QPushButton':
			if sb.prefix(self.widgetName, 'i'): #set the stacked widget.
				submenu = self.widget.whatsThis()+'_submenu'
				if not self.name==submenu: #do not reopen the submenu if it is already open.
					self.name = self.parent.setSubUi(self.widget, submenu)

			elif self.widgetName=='<':
				self.parent.setPrevUi()

			elif sb.prefix(self.widgetName, 'chk'):
				if sb.getUiLevel(self.name)==2: #if submenu:
					self.widget.click()



	def leaveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self._mouseHover.emit(False)

		if self.widgetType=='QWidget':
			if sb.prefix(self.widgetName, 'r'):
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
			if self.derivedType=='QPushButton':
				if sb.prefix(self.widgetName, 'i'): #ie. 'i012'
					self.parent.setUi(self.widget.whatsThis()) #switch the stacked layout to the given ui.
					self.parent.move(QtGui.QCursor.pos() - self.parent.ui.rect().center()) #move window to cursor position and offset from left corner to center

				elif sb.prefix(self.widgetName, 'v'):
					#add the buttons command info to the prevCamera list.
					method = sb.getMethod(self.name, self.widgetName)
					docString = sb.getDocString(self.name, self.widgetName)
					sb.prevCamera(allowCurrent=True, as_list=1).append([method, docString]) #store the camera view
					#send click signal on mouseRelease.
					self.widget.click()

				elif sb.prefix(self.widgetName, 'b'):
					if '_submenu' in self.name:
						self.widget.click()
					#add the buttons command info to the prevCommand list.
					method = sb.getMethod(self.name, self.widgetName)
					docString = sb.getDocString(self.name, self.widgetName)
					sb.prevCommand(as_list=1).append([method, docString]) #store the command method object and it's docString (ie. 'Multi-cut tool')






#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

# p1 = self.widget.mapToGlobal(self.widget.rect().center())

# 					submenu = self.widget.whatsThis()+'_submenu'
# 					n = self.widgetName
# 					if not self.name==submenu: #do not reopen submenu on enter event if it is already open.
# 						self.name = self.parent.setUi(submenu) #switch the stacked layout to the given submenu.
# 						self.widget = getattr(self.parent.currentWidget(), n) #get the widget with the same name in the new ui.


# 						p3 = self.parent.mapToGlobal(self.parent.pos())
# 						p2 = self.widget.mapToGlobal(self.widget.rect().center())
# 						self.parent.move(self.parent.mapFromGlobal(p3 +(p1 - p2)))



# print(name, sb.previousName(as_list=1)[-3])
					# if name==sb.previousName(as_list=1, allowDuplicates=1)[-3]: #if index is changed to the previous ui, remove the last widget.
						# del self.prevWidget[-1:]


#show button for any previous commands.
		# if sb.prefix(self.widgetName, 'v') and self.name=='main': #'v024-29'
		# 	self.widget.setText(sb.prevCommand(docString=1, as_list=1)[-num]) #prevCommand docString
		#  	#self.resizeAndCenterWidget(self.widget)
		# 	self.widget.show()