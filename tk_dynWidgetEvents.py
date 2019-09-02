from PySide2 import QtCore, QtGui, QtWidgets

import os.path

from tk_switchboard import Switchboard
from tk_styleSheet import StyleSheet





class DynWidgetEvents(QtCore.QObject):
	'''
	
	'''
	__mouseHover = QtCore.Signal(bool)
	
	def __init__(self, name, parent=None):
		super(DynWidgetEvents, self).__init__(parent)
		'''
		Set initial states for dynamic ui widgets. 
		'''
		self.name = name

		self.sb = Switchboard()


		for widget in self.sb.getWidget(self.name): #constructs connections for, and returns, all widgets for the given ui name.
			widget.installEventFilter(self)
			# widget.setMouseTracking(True)

			widgetName = widget.objectName()
			widgetType = widget.__class__.__name__ # self.sb.getWidgetType(widget)

			widget.setStyleSheet(StyleSheet.css) #add StyleSheet

			if self.name=='init' and widgetName=='t000':
				widget.viewport().setAutoFillBackground(False)
				widget.setTextBackgroundColor(QtGui.QColor(50, 50, 50))

			if self.name=='main' or self.name=='viewport':
				if widgetName.startswith('r'):
					widget.setVisible(False)

			if self.name=='create':
				if widgetName.startswith('s'):
					widget.setVisible(False)



	def eventFilter(self, widget, event):
		'''
		Event filter for dynamic ui widgets.
		args:
			widget=<object> - the widget for which the event occurred.
			event=<QEvent>
		'''
		for widget in self.sb.getWidget(self.name): #constructs connections for, and returns, all widgets for the given ui name.

			widgetName = widget.objectName()
			widgetType = widget.__class__.__name__ # self.sb.getWidgetType(widget)


			#___MouseButtonPress Event
			if event.type()==QtCore.QEvent.MouseButtonPress:
				self.__mousePressPos = event.globalPos()


			#___MouseMove Event
			if event.type()==QtCore.QEvent.MouseMove:
				if widgetType=='QPushButton':
					if widgetName.startswith('i') or widgetName.startswith('v'): #set down
						widget.setDown(widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())))

					elif widgetName=='pin': #move window on left mouse drag.
						self.moveToMousePosition(self, -self.point.x(), -self.point.y()*.1)

				elif widgetType=='QWidget':
					if widgetName.startswith('r'): #set visibility
						widget.setVisible(widget.geometry().contains(event.pos()))

				elif widgetType=='QComboBox':
					if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
						#switch the index before opening to initialize the contents of the comboBox
						widget.setStyleSheet(StyleSheet.comboBox_alt)
						index = widget.currentIndex()
						widget.blockSignals(True)
						widget.setCurrentIndex(-1)
						widget.blockSignals(False)
						widget.setCurrentIndex(index) #change index back to refresh contents
					else:
						widget.setStyleSheet(StyleSheet.comboBox)


			#___MouseButtonRelease Event
			if event.type()==QtCore.QEvent.MouseButtonRelease:
				print widgetName
				if widgetType=='QPushButton':
					if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
						if widgetName.startswith('i'): #connect to layoutStack and pass in an index as int or string 'name'.
							index = widget.whatsThis()
							self.layoutStack(index) #switch the stacked layout to the given ui.

						elif widgetName.startswith('v'): #ie. 'v012'
							self.sb.previousView(as_list=1).append(self.sb.getMethod(self.name, widgetName)) #store the camera view
							widget.click()

						elif widgetName.startswith('b'): #ie. 'b012'
							self.sb.prevCommand(as_list=1).append([self.sb.getMethod(self.name, widgetName), self.sb.getDocString(widgetName)]) #store the command method object and it's docString (ie. 'Multi-cut tool')

						elif widgetName=='pin': #Override pushbutton to move the main window on left mouse drag event. When checked, prevents hide event on main window.
							print 'pin_mouseReleaseEvent', widgetName
							moveAmount = event.globalPos() - self.__mousePressPos
							if moveAmount.manhattanLength() > 5: #if widget moved:
								widget.setChecked(True) #setChecked to prevent window from closing.
								event.ignore()
							else:
								widget.setChecked(not widget.isChecked()) #toggle check state
								self.hide_()

				elif widgetType=='QComboBox':
					if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
						widget.setStyleSheet(StyleSheet.comboBox_popup)
						widget.showPopup()


			#___Enter Event
			if event.type()==QtCore.QEvent.Type.Enter:
				self.__mouseHover.emit(True)


			#___HoverLeave Event
			if event.type()==QtCore.QEvent.Type.HoverLeave:
				self.__mouseHover.emit(False)

		# return super(HotBox, self).eventFilter(widget, event)
		return QtWidgets.QWidget.eventFilter(self, widget, event)