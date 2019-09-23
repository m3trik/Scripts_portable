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






	def init(self, name):
		'''
		Initialize widget states.
		args:
			name='string' - ui name.
		'''
		for widget in self.sb.getWidget(name): #get all widgets for the given ui name.
			widgetName = widget.objectName()
			widgetType = self.sb.getWidgetType(widget)

			widget.setStyleSheet(getattr(StyleSheet, widgetType, '')) #add StyleSheet
			widget.installEventFilter(self)

			# Set initial widget states.
			if widgetName=='pin':
				widget.setStyleSheet(StyleSheet.QPushButton_pin)
				widget.setDisabled(True)

			elif widgetName=='cmb':
				widget.setStyleSheet(StyleSheet.QComboBox_cmb)

			elif widgetType=='QProgressBar':
				widget.setVisible(False)

			elif name=='init' and widgetName=='info':
				widget.viewport().setAutoFillBackground(False)
				widget.setTextBackgroundColor(QtGui.QColor(50, 50, 50))

			elif name=='main' or name=='viewport':
				if widgetName.startswith('r'):
					widget.setVisible(False)

			elif name=='create':
				if widgetName.startswith('s'):
					widget.setVisible(False)



	def mouseTracking(self, name):
		'''
		Get widget/s currently under cursor. Grab mouse, and send events.
		args:
			name='string' - ui name.
		'''
		for widget in self.sb.getWidget(name): #get all widgets from the current ui.
			widgetName = widget.objectName()

			if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
				if not widget in self.__mouseOver: #if widget is already in the mouseOver list, no need to re-process the events.
					QtWidgets.QApplication.sendEvent(widget, self.enterEvent_)
					self.__mouseOver.append(widget)

					if widgetName.startswith('i') or widgetName.startswith('v'):
						widget.grabMouse() #set widget to receive mouse events.
						self.__mouseGrabber = widget

			else:
				if widget in self.__mouseOver: #if widget is in the mouseOver list, but the mouse is no longer over the widget:
					QtWidgets.QApplication.sendEvent(widget, self.leaveEvent_)
					self.__mouseOver.remove(widget)



	def eventFilter(self, widget, event):
		'''
		args:
			widget=<QWidget>
			event=<QEvent>
		'''
		if not widget.isWidgetType():
			return False

		self.name = self.sb.getNameFrom(widget) #get the ui name corresponding to the given widget.
		# if not self.name==self.sb.getUiName(): #if the widget belongs to former ui, don't process the event.
		# 	return False

		# e = str(event.type()).split('.')[-1]
		# if e!='Paint':
		# 	print widget.objectName(), e

		self.widget = widget
		self.widgetName = self.widget.objectName()
		self.widgetType = self.sb.getWidgetType(self.widget)


		if event.type()==QtCore.QEvent.MouseButtonPress:
			self.mousePressEvent(event)

		elif event.type()==QtCore.QEvent.MouseButtonRelease:
			self.mouseReleaseEvent(event)

		elif event.type()==QtCore.QEvent.MouseMove:
			self.mouseMoveEvent(event)

		elif event.type()==QtCore.QEvent.Enter: #HoverEnter
			self.enterEvent(event)

		elif event.type()==QtCore.QEvent.Leave: #HoverLeave
			self.leaveEvent(event)

		return super(EventFactoryFilter, self).eventFilter(widget, event)



	# ------------------------------------------------
	# Events
	# ------------------------------------------------
	def enterEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print self.name,'enterEvent',self.widgetType,self.widgetName
		self.__mouseHover.emit(True)

		if self.widgetName.startswith('r'):
			self.widget.setVisible(True) #set visibility



	def leaveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print self.name,'leaveEvent',self.widgetType,self.widgetName
		self.__mouseHover.emit(False)

		if self.widget==self.__mouseGrabber: #self.widget.mouseGrabber():
			mainWindow = self.sb.getWidget(self.name, 'mainWindow')
			mainWindow.grabMouse()
			self.__mouseGrabber = mainWindow

		if self.widgetName.startswith('r'):
			self.widget.setVisible(False) #set visibility



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print self.name,'mousePressEvent',self.widgetType,self.widgetName
		self.__mousePressPos = event.globalPos() #mouse positon at press
		self.__mouseMovePos = event.globalPos() #mouse move position from last press



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print self.name,'mouseMoveEvent',self.widgetType,self.widgetName
		if self.widgetType=='QPushButton':
			if self.widgetName=='pin': #move window
				hotBox = self.sb.getClassInstance('hotBox')
				curPos = hotBox.mapToGlobal(hotBox.pos())
				globalPos = event.globalPos()
				diff = globalPos -self.__mouseMovePos
				hotBox.move(hotBox.mapFromGlobal(curPos + diff))
				self.__mouseMovePos = globalPos

		elif self.widgetType=='QComboBox':
			if self.widget.rect().contains(self.widget.mapFromGlobal(QtGui.QCursor.pos())):
				self.widget.setStyleSheet(StyleSheet.QComboBox_alt)
				index = self.widget.currentIndex()
				self.widget.blockSignals(True)
				self.widget.setCurrentIndex(-1) #switch the index before opening to initialize the contents of the comboBox
				self.widget.blockSignals(False)
				self.widget.setCurrentIndex(index) #change index back to refresh contents
			else:
				self.widget.setStyleSheet(StyleSheet.QComboBox)



	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print self.name,'mouseReleaseEvent',self.widgetType,self.widgetName
		if self.widgetType=='QPushButton':
			# if self.widget in self.__mouseOver:
				if self.widgetName.startswith('i'): #set the stacked widget.
					self.sb.getClassInstance('hotBox').setWidget(self.widget.whatsThis()) #switch the stacked layout to the given ui.
					self.__mouseGrabber.releaseMouse()
					self.__mouseGrabber = None
					# self.sb.getUi().activateWindow()
					self.sb.getClassInstance('hotBox').activateWindow()

				elif self.widgetName.startswith('v'): #ie. 'v012'
					self.sb.previousView(as_list=1).append(self.sb.getMethod(self.name, self.widgetName)) #store the camera view
					self.widget.click()

				elif self.widgetName.startswith('b'): #ie. 'b012'
					self.sb.prevCommand(as_list=1).append([self.sb.getMethod(self.name, self.widgetName), self.sb.getDocString(self.name, self.widgetName)]) #store the command method object and it's docString (ie. 'Multi-cut tool')

				elif self.widgetName=='pin': #Override pushbutton to move the main window on left mouse drag event. When checked, prevents hide event on main window.
					moveAmount = event.globalPos() -self.__mousePressPos
					if moveAmount.manhattanLength() >5: #if widget moved:
						self.widget.setChecked(True) #setChecked to prevent window from closing.
					else:
						self.widget.setChecked(not self.widget.isChecked()) #toggle check state
						self.sb.getClassInstance('hotBox').hide_()

		elif self.widgetType=='QComboBox':
			if self.widget.rect().contains(self.widget.mapFromGlobal(QtGui.QCursor.pos())):
				self.widget.setStyleSheet(StyleSheet.QComboBox_popup)
				self.widget.showPopup()







#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------