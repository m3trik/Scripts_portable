from PySide2 import QtCore, QtGui, QtWidgets

import os.path

from tk_switchboard import Switchboard
from tk_styleSheet import StyleSheet





class Events(QtWidgets.QWidget):
	'''
	Event filter for dynamic ui widgets.
	'''
	__mouseHover = QtCore.Signal(bool)
	__mousePressPos = QtCore.QPoint()

	def __init__(self, widget):
		super(Events, self).__init__()
		'''
		Set initial widget states. 
		'''
		self.sb = Switchboard()

		self.widget = widget #self.sb.getWidget(self.name, 'mainWindow').mouseGrabber()
		self.widgetName = self.widget.objectName()
		self.widgetType = self.widget.__class__.__name__ # self.sb.getWidgetType(self.widget)

		self.name = self.sb.getNameFrom(self.widget)
		# print self.__mousePressPos



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		event.accept()
		print self.name,'mousePressEvent',self.widgetType,self.widgetName
		self.__mousePressPos = event.globalPos()



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# event.accept()
		print self.name,'mouseMoveEvent',self.widgetType,self.widgetName
		if self.widgetType=='QPushButton':
			if self.widgetName.startswith('i') or self.widgetName.startswith('v'):
				for w in self.sb.getWidget(self.name):
					if w.objectName().startswith('i') or w.objectName().startswith('v'):
						w.setDown(w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos()))) #set down on mouse hover.

			if self.widgetName=='pin':
				self.moveToMousePosition(self, -self.point.x(), -self.point.y()*.1) #move window on left mouse drag.


		elif self.widgetType=='QWidget':
			if self.widgetName.startswith('r'):
				for w in self.sb.getWidget(self.name):
					if w.objectName().startswith('r'):
						w.setVisible(w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos()))) #set visibility
					if w.objectName().startswith('i') or w.objectName().startswith('v'):
						w.setDown(w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos()))) #set down on mouse hover.


		elif self.widgetType=='QComboBox':
			if self.widget.rect().contains(self.widget.mapFromGlobal(QtGui.QCursor.pos())):
				#switch the index before opening to initialize the contents of the comboBox
				self.widget.setStyleSheet(StyleSheet.comboBox_alt)
				index = self.widget.currentIndex()
				self.widget.blockSignals(True)
				self.widget.setCurrentIndex(-1)
				self.widget.blockSignals(False)
				self.widget.setCurrentIndex(index) #change index back to refresh contents
			else:
				self.widget.setStyleSheet(StyleSheet.comboBox)



	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# event.accept()
		print self.name,'mouseReleaseEvent',self.widgetType,self.widgetName
		if self.widgetType=='QPushButton':
			if self.widget.rect().contains(self.widget.mapFromGlobal(QtGui.QCursor.pos())):
				if self.widgetName.startswith('i'): #connect to layoutStack and pass in an index as int or string 'name'.
					self.sb.getClass('hotBox').layoutStack(self.widget.whatsThis()) #switch the stacked layout to the given ui.

				if self.widgetName.startswith('v'): #ie. 'v012'
					self.sb.previousView(as_list=1).append(self.sb.getMethod(self.name, self.widgetName)) #store the camera view

				elif self.widgetName.startswith('b'): #ie. 'b012'
					self.sb.prevCommand(as_list=1).append([self.sb.getMethod(self.name, self.widgetName), self.sb.getDocString(self.widgetName)]) #store the command method object and it's docString (ie. 'Multi-cut tool')

				elif self.widgetName=='pin': #Override pushbutton to move the main window on left mouse drag event. When checked, prevents hide event on main window.
					print 'pin_mouseReleaseEvent', self.widgetName
					moveAmount = event.globalPos() - self.__mousePressPos
					if moveAmount.manhattanLength() > 5: #if widget moved:
						self.widget.setChecked(True) #setChecked to prevent window from closing.
						event.ignore()
					else:
						self.widget.setChecked(not self.widget.isChecked()) #toggle check state
						self.hide_()

		elif self.widgetType=='QComboBox':
			if self.widget.rect().contains(self.widget.mapFromGlobal(QtGui.QCursor.pos())):
				self.widget.setStyleSheet(StyleSheet.comboBox_popup)
				self.widget.showPopup()



	def enterEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		event.accept()
		print self.name,'enterEvent',self.widgetType,self.widgetName
		self.__mouseHover.emit(True)



	def leaveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		event.accept()
		print self.name,'leaveEvent',self.widgetType,self.widgetName
		self.__mouseHover.emit(False)






class EventFactoryFilter(QtCore.QObject):
	'''
	args:
		name='string' - ui name.
		parent=<parent>
	'''
	def __init__(self, name):
		super(EventFactoryFilter, self).__init__()

		self.sb = Switchboard()

		for widget in self.sb.getWidget(name): #get all widgets for the given ui name.
			widgetName = widget.objectName()

			widget.setStyleSheet(StyleSheet.css) #add StyleSheet
			if any([name=='init', name=='main', name=='viewport', name=='editors']):
				if not widgetName=='mainWindow':
					widget.installEventFilter(self)


			if name=='init' and widgetName=='t000':
				widget.viewport().setAutoFillBackground(False)
				widget.setTextBackgroundColor(QtGui.QColor(50, 50, 50))

			if name=='main' or name=='viewport':
				if widgetName.startswith('r'):
					widget.setVisible(False)

			if name=='create':
				if widgetName.startswith('s'):
					widget.setVisible(False)



	def eventFilter(self, widget, event):
		'''
		args:
			widget=<QWidget>
			event=<QEvent>
		'''
		if not widget.isWidgetType():
			return False

		if event.type()==QtCore.QEvent.MouseButtonPress:
			Events(widget).mousePressEvent(event)

		elif event.type()==QtCore.QEvent.MouseButtonRelease:
			Events(widget).mouseReleaseEvent(event)

		elif event.type()==QtCore.QEvent.MouseMove:
			Events(widget).mouseMoveEvent(event)

		elif event.type()==QtCore.QEvent.Type.Enter: #HoverEnter
			Events(widget).enterEvent(event)

		elif event.type()==QtCore.QEvent.Type.Leave: #HoverLeave
			Events(widget).leaveEvent(event)


		return super(EventFactoryFilter, self).eventFilter(widget, event)