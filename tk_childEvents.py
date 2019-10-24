from PySide2 import QtCore, QtGui, QtWidgets

import os.path

from tk_switchboard import Switchboard
from tk_styleSheet import StyleSheet






class EventFactoryFilter(QtCore.QObject):
	'''
	Event filter for dynamic ui widgets.
	args:
		parent=<parent>
	'''
	__mouseOver = [] #list of widgets currently under the mouse cursor.
	__mouseGrabber = None
	__mouseHover = QtCore.Signal(bool)
	__mousePressPos = QtCore.QPoint()

	enterEvent_ = QtCore.QEvent(QtCore.QEvent.Enter)
	leaveEvent_ = QtCore.QEvent(QtCore.QEvent.Leave)


	def __init__(self, parent=None):
		super(EventFactoryFilter, self).__init__(parent)

		self.sb = Switchboard()
		self.hotBox = self.sb.getClassInstance('hotBox')

		self.prevWidget=[]



	def init(self, name):
		'''
		Set Initial widget states.
		args:
			name='string' - ui name.
		'''
		for widget in self.sb.getWidget(name=name): #get all widgets for the given ui name.
			widgetName = widget.objectName()
			widgetType = self.sb.getWidgetType(widget, name) #get the class type as string.
			derivedType = self.sb.getDerivedType(widget, name) #get the derived class type as string.

			widget.setStyleSheet(getattr(StyleSheet, derivedType, '')) #add StyleSheet
			widget.installEventFilter(self)


			if widgetName=='info':
				widget.viewport().setAutoFillBackground(False)
				widget.setTextBackgroundColor(QtGui.QColor(50, 50, 50))

			elif widgetType=='QProgressBar':
				widget.setVisible(False)

			elif any([name=='main', name=='viewport']):
				if widgetName.startswith('r'):
					widget.setVisible(False)

			elif name=='create':
				if widgetName.startswith('s'):
					widget.setVisible(False)



	def mouseTracking(self, name):
		'''
		Get widget/s currently under cursor. Grab mouse, and send events accordingly.
		args:
			name='string' - ui name.
		'''
		for widget in self.sb.getWidget(name=name): #get all widgets from the current ui.
			widgetName = widget.objectName()

			if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
				if not widget in self.__mouseOver: #if widget is already in the mouseOver list, no need to re-process the events.
					QtWidgets.QApplication.sendEvent(widget, self.enterEvent_)
					self.__mouseOver.append(widget)

					if not widgetName=='mainWindow':
						widget.grabMouse() #set widget to receive mouse events.
						self.__mouseGrabber = widget

			else:
				if widget in self.__mouseOver: #if widget is in the mouseOver list, but the mouse is no longer over the widget:
					QtWidgets.QApplication.sendEvent(widget, self.leaveEvent_)
					self.__mouseOver.remove(widget)



	@staticmethod
	def createEventName(event):
		'''
		Get an event method name string from a given event.
		ie. 'enterEvent' from QtCore.QEvent.Type.Enter,
		ie. 'mousePressEvent' from QtCore.QEvent.Type.MouseButtonPress
		args:
			event=<QEvent>
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
			widget=<QWidget>
			event=<QEvent>
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
			# print event.__class__.__name__
			return False
		# print event.__class__.__name__


		self.name = self.sb.getNameFrom(widget) #get the ui name corresponding to the given widget.

		self.widget = widget
		self.widgetName = self.widget.objectName()
		self.widgetType = self.sb.getWidgetType(self.widget, self.name)
		self.derivedType = self.sb.getDerivedType(self.widget, self.name)
		self.widgetClass = self.sb.getWidgetClassInstance(self.widget, self.name)

		eventName = EventFactoryFilter.createEventName(event) #get 'mousePressEvent' from <QEvent>
		# print self.name, eventName, self.widgetType, self.widgetName


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
			event=<QEvent>
		'''
		pass



	def hideEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		pass



	def enterEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.__mouseHover.emit(True)

		if self.widgetType=='QWidget':
			if self.widgetName.startswith('r'):
				self.widget.setVisible(True) #set visibility

		elif self.widgetType=='QPushButton':
			if self.widgetName.startswith('i'): #set the stacked widget.
				try: #open a submenu on mouse enter (if it exists).
					p1 = self.widget.mapToGlobal(self.widget.rect().center()) #widget position before submenu change.

					submenu = self.widget.whatsThis()+'_submenu'
					if not self.name==submenu: #do not reopen submenu on enter event if it is already open.
						w = self.widget #store widget before changing the stacked widget ui.
						name = self.hotBox.setWidget(submenu) #switch the stacked widget to the given submenu.
						widget = getattr(self.hotBox.currentWidget(), w.objectName()) #get the widget of the same name in the new ui.
						#maintain the correct contents of the prevWidget and drawPath lists by removing elements when moving back up levels in the ui.
						if len(self.sb.previousName(as_list=1, allowDuplicates=1))>2:
							if name==self.sb.previousName(as_list=1, allowDuplicates=1)[-3]: #if index is that of the previous ui, remove the information associated with that ui from the lists so that any new list will draw with the correct contents.
								del self.prevWidget[-2:]
								if len(self.hotBox.drawPath)>2: #temp solution for removing drawPath points. works only when there are two levels of submenus to draw paths for.
									del self.hotBox.drawPath[-2:]

						self.prevWidget.append([w, p1]) #add the widget that was initially entered to the prevWidget list so that it can be re-created in the new ui (in the same position).
						self.hotBox.drawPath.append(QtGui.QCursor.pos()) #add the global cursor position to the drawPath list so that paint events can draw the path tangents.

						p2 = widget.mapToGlobal(widget.rect().center()) #widget position after submenu change.
						currentPos = self.hotBox.mapToGlobal(self.hotBox.pos())
						self.hotBox.move(self.hotBox.mapFromGlobal(currentPos +(p1 - p2))) #currentPos + difference


						if name not in self.sb.previousName(as_list=1, allowDuplicates=1)[:-1]: #if submenu ui called for the first time, construct widgets from the previous ui that fall along the plotted path.
							w0 = QtWidgets.QPushButton('<', self.sb.getUi(name))
							w0 = self.sb.addWidget(name, w0, '<')
							w0.resize(30, 30)
							w0.move(w0.mapFromGlobal(self.hotBox.drawPath[0] - w0.rect().center())) #move and center
							w0.show()

							if '_submenu' in self.sb.previousName(): #recreate widget/s from the previous ui that are in the current path.
								for index in range(2, len(self.prevWidget)+1): #index starting at 2:
									prevWidget = self.prevWidget[-index][0] #give index neg value.
									prevWidgetLocation = self.prevWidget[-index][1]

									w1 = QtWidgets.QPushButton(prevWidget.text(), self.sb.getUi(name))
									w1 = self.sb.addWidget(name, w1, prevWidget.objectName())
									w1.setWhatsThis(prevWidget.whatsThis())
									w1.resize(prevWidget.size())
									w1.move(w1.mapFromGlobal(prevWidgetLocation - w1.rect().center())) #move and center
									w1.show()
									index+=1

							self.init(name) #re-initialize the widgets under this ui name to set things like the event filter and stylesheet for the newly added widgets. 

				except Exception as error:
					if not type(error)==ValueError: #if no submenu exists: ignore.
						raise error

			elif self.widgetName=='<':
				previous = [i for i in self.sb.previousName(as_list=1) if '_submenu' not in i][-1]
				self.name = self.hotBox.setWidget(previous) #return the stacked widget to it's previous ui.
				del self.hotBox.drawPath[1:] #clear the draw path, while leaving the starting point.
				del self.prevWidget[:] #clear the list of previous widgets.
				self.hotBox.move(self.hotBox.drawPath[0] - self.hotBox.rect().center())



	def leaveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.__mouseHover.emit(False)

		if self.widget==self.__mouseGrabber: #self.widget.mouseGrabber():
			mainWindow = self.sb.getWidget('mainWindow', self.name)
			if mainWindow.isVisible():
				mainWindow.grabMouse()
				self.__mouseGrabber = mainWindow

		if self.widgetType=='QWidget':
			if self.widgetName.startswith('r'):
				self.widget.setVisible(False) #set visibility



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.__mousePressPos = event.globalPos() #mouse positon at press
		self.__mouseMovePos = event.globalPos() #mouse move position from last press



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		globalPos = event.globalPos()
		diff = globalPos -self.__mouseMovePos
		self.__mouseMovePos = globalPos



	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if self.widgetType=='QPushButton':
			if self.widgetName.startswith('i'): #set the stacked widget.
				self.name = self.hotBox.setWidget(self.widget.whatsThis()) #switch the stacked layout to the given ui.
				self.__mouseGrabber.releaseMouse()
				self.__mouseGrabber = None
				self.hotBox.activateWindow()

			elif self.widgetName.startswith('v'): #ie. 'v012'
				self.sb.previousView(as_list=1).append(self.sb.getMethod(self.name, self.widgetName)) #store the camera view
				self.widget.click()

			elif self.widgetName.startswith('b'): #ie. 'b012'
				self.sb.prevCommand(as_list=1).append([self.sb.getMethod(self.name, self.widgetName), self.sb.getDocString(self.name, self.widgetName)]) #store the command method object and it's docString (ie. 'Multi-cut tool')






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

# p1 = self.widget.mapToGlobal(self.widget.rect().center())

# 					submenu = self.widget.whatsThis()+'_submenu'
# 					n = self.widgetName
# 					if not self.name==submenu: #do not reopen submenu on enter event if it is already open.
# 						self.name = self.hotBox.setWidget(submenu) #switch the stacked layout to the given submenu.
# 						self.widget = getattr(self.hotBox.currentWidget(), n) #get the widget with the same name in the new ui.


# 						p3 = self.hotBox.mapToGlobal(self.hotBox.pos())
# 						p2 = self.widget.mapToGlobal(self.widget.rect().center())
# 						self.hotBox.move(self.hotBox.mapFromGlobal(p3 +(p1 - p2)))



# print name, self.sb.previousName(as_list=1)[-3]
					# if name==self.sb.previousName(as_list=1, allowDuplicates=1)[-3]: #if index is changed to the previous ui, remove the last widget.
						# del self.prevWidget[-1:]