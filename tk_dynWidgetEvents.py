from PySide2 import QtCore, QtGui, QtWidgets

import os.path

from tk_switchboard import Switchboard
from tk_styleSheet import StyleSheet





class Events(QtWidgets.QWidget):
	'''
	Event filter for dynamic ui widgets.
	'''
	__mouseHover = QtCore.Signal(bool)

	def __init__(self, widget):
		super(Events, self).__init__()
		'''
		Set initial widget states. 
		'''
		self.sb = Switchboard()
		self.name = self.sb.getUiName()
		print 'Events:',self.name,widget.objectName()

		self.widget = widget
		self.widgetName = widget.objectName()
		self.widgetType = widget.__class__.__name__ # self.sb.getWidgetType(self.widget)



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print 'mousePressEvent'
		self.__mousePressPos = event.globalPos()



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		# print 'mouseMoveEvent',self.widgetName
		if self.widgetType=='QPushButton':
			if self.widgetName.startswith('i') or self.widgetName.startswith('v'): #set down
				self.widget.setDown(self.widget.rect().contains(self.widget.mapFromGlobal(QtGui.QCursor.pos())))

			elif self.widgetName=='pin': #move window on left mouse drag.
				self.moveToMousePosition(self, -self.point.x(), -self.point.y()*.1)

		elif self.widgetType=='QWidget':
			if self.widgetName.startswith('r'): #set visibility
				self.widget.setVisible(self.widget.geometry().contains(event.pos()))

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
		print 'mouseReleaseEvent',self.widgetName
		if self.widgetType=='QPushButton':
			if self.widget.rect().contains(self.widget.mapFromGlobal(QtGui.QCursor.pos())):
				if self.widgetName.startswith('i'): #connect to layoutStack and pass in an index as int or string 'name'.
					index = self.widget.whatsThis()
					print 'layout:',self.widget.layout()
					# self.layoutStack(index) #switch the stacked layout to the given ui.

				elif self.widgetName.startswith('v'): #ie. 'v012'
					self.sb.previousView(as_list=1).append(self.sb.getMethod(self.name, self.widgetName)) #store the camera view
					self.widget.click()

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
		print 'enterEvent',self.widgetName
		self.__mouseHover.emit(True)



	def dragEnterEvent(self, event):
		event.accept()
		print 'dragEnterEvent'

	

	def dragMoveEvent(self, event):
		event.accept()



	def leaveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.__mouseHover.emit(False)



	def dragLeaveEvent(self, event):
		event.accept()
		print 'dragLeaveEvent'



	def dropEvent(self, event):
		event.accept()
		print 'dropEvent'






class EventFactoryFilter(QtCore.QObject):
	'''
	args:
		name='string' - ui name.
		parent=<parent>
	'''
	def __init__(self, name, parent=None):
		super(EventFactoryFilter, self).__init__(parent)

		self.sb = Switchboard()

		for widget in self.sb.getWidget(name): #get all widgets for the given ui name.

			widget.setStyleSheet(StyleSheet.css) #add StyleSheet
			widget.installEventFilter(self)
			# widget.setMouseTracking(True)
			# widget.setAcceptDrops(True)
			# widget.mousePressEvent = Events(widget).mousePressEvent
			# widget.mouseReleaseEvent = Events(widget).mouseReleaseEvent

			if name=='init' and widget.objectName()=='t000':
				widget.viewport().setAutoFillBackground(False)
				widget.setTextBackgroundColor(QtGui.QColor(50, 50, 50))

			if name=='main' or name=='viewport':
				if widget.objectName().startswith('r'):
					widget.setVisible(False)

			if name=='create':
				if widget.objectName().startswith('s'):
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

		elif event.type()==QtCore.QEvent.Type.DragEnter:
			Events(widget).dragEnterEvent(event)

		elif event.type()==QtCore.QEvent.Type.DragLeave:
			Events(widget).dragLeaveEvent(event)

		elif event.type()==QtCore.QEvent.Type.DragMove:
			Events(widget).dragMoveEvent(event)

		elif event.type()==QtCore.QEvent.Type.Drop:
			Events(widget).dropEvent(event)


		return super(EventFactoryFilter, self).eventFilter(widget, event)