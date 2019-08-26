# ||||||||||||||||||||||||||||||||||||||||||||||||||
# |||||||||     hotBox marking menu     ||||||||||||
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from PySide2 import QtCore, QtGui, QtWidgets
from ctypes import windll, Structure, c_long, byref

import sys, os.path

from tk_switchboard import Switchboard
from tk_styleSheet import StyleSheet

try: import MaxPlus
except: pass







# ------------------------------------------------
# Mouse Tracking
# ------------------------------------------------
class Point(Structure):
	_fields_ = [("x", c_long), ("y", c_long)]


def getMousePosition():
	pt = Point()
	windll.user32.GetCursorPos(byref(pt))
	return {"x": pt.x, "y": pt.y}






# ------------------------------------------------
# hotBox 
# ------------------------------------------------
class HotBox(QtWidgets.QWidget):
	'''
	HotBox marking menu-style modal window.
	Getting and setting of signal connections are handled by the switchboard module.
	args:
		parent=main application window object.
	'''
	mouseHover = QtCore.Signal(bool)

	def __init__(self, parent):
		super(HotBox, self).__init__(parent)

		#set window style
		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.X11BypassWindowManagerHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		# self.setStyle(QtWidgets.QStyleFactory.create("plastique"))

		self.sb = Switchboard(parent)

		self.stackedLayout = None



	def layoutStack(self, index):
		'''
		Set the stacked layout.
		args:
			index=int - index of ui in stacked layout.
				*or 'string' - name of ui in stacked layout.
		'''
		if type(index)!=int: #get index using name
			index = self.sb.getUiIndex(index)

		self.index = index
		self.name = self.sb.setUiName(self.index) #set current ui name from index
		self.ui = self.sb.getUi() #get the current dymanic ui


		if not self.stackedLayout: #add the stacked layout.
			self.stackedLayout = QtWidgets.QStackedLayout(self)

			for name, ui in self.sb.uiList():
				self.sb.setUiSize(name) #store size info for each ui
				self.stackedLayout.addWidget(ui) #add each ui to the stackedLayout.

		self.stackedLayout.setCurrentIndex(self.index) #set the index in the stackedLayout for the given ui.


		self.point = QtCore.QPoint(self.sb.getUiSize(percentWidth=50), self.sb.getUiSize(percentHeight=50)) #set point to the middle of the layout
		self.moveToMousePosition(self, -self.point.x(), -self.point.y()) #set initial positon on showEvent, and reposition here on index change.
		self.resize(self.sb.getUiSize(width=1), self.sb.getUiSize(height=1)) #get ui size for current ui and resize window


		if not self.sb.hasKey(self.name, 'connectionDict'): #build the connectionDict containing the widgets and their connections.
			for widget in self.sb.getWidget(self.name, allWidgets=1): #constructs and returns all widgets for the given ui name.
				widget.setStyleSheet(StyleSheet.css) #add StyleSheet
				widget.installEventFilter(self) #add eventfilter
				# widget.setMouseTracking(True)
				self.sb.addSignal(self.name)



	# ------------------------------------------------
	# Event overrides
	# ------------------------------------------------
	def eventFilter(self, widget, event):
		'''
		Event filter for dynamic ui objects.
		args:
			widget=<object> - the widget for which the event occurred.
			event=<QEvent>
		'''
		widgetName = widget.objectName()
		widgetType = widget.__class__.__name__ # self.sb.getWidgetType(widget)


		#___MouseButtonPress Event_____________________
		if event.type()==QtCore.QEvent.MouseButtonPress:
			if widgetName=='pin':
				self.__mousePressPos = event.globalPos()


		#___MouseMove Event_____________________
		if event.type()==QtCore.QEvent.MouseMove:
			if widgetName=='pin':
				self.moveToMousePosition(self, -self.point.x(), -self.point.y()*.1) #move window on left mouse drag.

			if any([self.name=='main', self.name=='editors', self.name=='viewport']):
				print 'MouseMove:',self.name,widgetName,widgetType
				if widgetName.startswith('r'):
					print '- -'
					if widget.geometry().contains(event.pos()):
						print '- - -'
						widget.setVisible(True)
					else:
						widget.setVisible(False)

				if widgetName.startswith('i') or widgetName.startswith('v'):
					if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
						widget.setDown(True)
					else:
						widget.setDown(False)

				if widgetName.startswith('cmb'):
					if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
						widget.setStyleSheet(StyleSheet.comboBox_alt)
					else:
						widget.setStyleSheet(StyleSheet.comboBox_popup)


		#___MouseButtonRelease Event_____________________
		if event.type()==QtCore.QEvent.MouseButtonRelease:
			print 'MouseButtonRelease:',self.name,widgetName,widgetType
			if widgetName=='pin': #Override pushbutton to move the main window on left mouse drag event. When checked, prevents hide event on main window.
				moveAmount = event.globalPos() - self.__mousePressPos
				if moveAmount.manhattanLength() > 5: #if widget moved:
					widget.setChecked(True) #setChecked to prevent window from closing.
					event.ignore()
				else:
					widget.setChecked(not widget.isChecked()) #toggle check state
					self.hide_()

			if widgetName.startswith('i'): #connect to layoutStack and pass in an index as int or string 'name'.
				index = widget.whatsThis()
				self.layoutStack(index) #switch the stacked layout to the given ui.

			if widgetName.startswith('v'): #ie. 'v012'
				self.sb.previousView(as_list=1).append(self.sb.getMethod(widgetName)) #store the camera view

			if widgetName.startswith('b'): #ie. 'b012'
				self.sb.prevCommand(as_list=1).append([self.sb.getMethod(widgetName), self.sb.getDocString(widgetName)]) #store the command method object and it's docString (ie. 'Multi-cut tool')


		#___Enter Event__________________________
		if event.type()==QtCore.QEvent.Type.Enter:
			self.mouseHover.emit(True)
			if widgetType=='QComboBox':
				#switch the index before opening to initialize the contents of the comboBox
				index = widget.currentIndex()
				widget.blockSignals(True); widget.setCurrentIndex(-1); widget.blockSignals(False)
				widget.setCurrentIndex(index) #change index back to refresh contents
				widget.setStyleSheet(StyleSheet.comboBox_popup)

			if any([self.name=='main', self.name=='editors', self.name=='viewport']): #layoutStack index and viewport signals
				if widgetType=='QComboBox':
					widget.showPopup()
				elif widgetType=='QPushButton':
					widget.click()

			if self.name=='init' and widgetType=='QTextEdit':
				# self.sb.getMethod('t000')()
				pass


		#___HoverLeave Event__________________________
		if event.type()==QtCore.QEvent.Type.HoverLeave:
			self.mouseHover.emit(False)
			if widgetType=='QComboBox':
				widget.setStyleSheet(StyleSheet.comboBox)
	


		return QtWidgets.QWidget.eventFilter(self, widget, event)



	def keyPressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat(): #Key_Meta or Key_Menu =windows key
			# if all([self.name!='init', self.name!='main', self.name!='viewport']):
			# 	self.layoutStack('init') #reset layout back to init on keyPressEvent
			if self.name=='init':
				print '!n!t'
				self.ui.t000.setFocus()



	def keyReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat():
			self.hide_()



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if any ([self.name=='init', self.name=='main', self.name=='viewport', self.name=='editors']):
			if event.button()==QtCore.Qt.LeftButton:
				self.layoutStack('viewport')

			elif event.button()==QtCore.Qt.MiddleButton:
				self.layoutStack('editors')

			elif event.button()==QtCore.Qt.RightButton:
				self.layoutStack('main')



	def mouseDoubleClickEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if event.button()==QtCore.Qt.RightButton:
			if any([self.name=='init', self.name=='main']):
				try: #show last used submenu on double mouseclick
					self.layoutStack(self.sb.previousName(previousIndex=True))
				except Exception as error: 
					print "# Warning: No recent submenus in history. #"

		if event.button()==QtCore.Qt.LeftButton:
			if any([self.name=='init', self.name=='viewport']):
				try: #show last view
					self.repeatLastView()
				except Exception as error: 
					print "# Warning: No recent views in history. #"

		if event.button()==QtCore.Qt.MiddleButton:
			if any([self.name=='init', self.name=='editors']):
				try: #repeat last command
					self.repeatLastCommand()
				except Exception as error:
					print "# Warning: No recent commands in history. #"



	def hide_(self):
		'''
		Prevent hide event under certain circumstances.
		'''
		try: #if pin is unchecked: hide
			if not self.ui.pin.isChecked():
				self.hide()
		except: #if ui doesn't have pin: hide
			self.hide()



	def hideEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		try: MaxPlus.CUI.EnableAccelerators()
		except: pass

		self.layoutStack('init')



	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		try: MaxPlus.CUI.DisableAccelerators()
		except: pass

		self.moveToMousePosition(self, -self.point.x(), -self.point.y()) #move window to cursor position and offset from left corner to center



	def moveToMousePosition(self, window, xOffset=None, yOffset=None):
		'''
		Move window from it's current position to the mouse position.
		args:
			window=widget
			xOffset=int - optional x coordinate offset amount
			yOffset=int - optional y coordinate offset amount
		'''
		mPos = getMousePosition()
		x = mPos['x']+xOffset
		y = mPos['y']+yOffset
		window.move(x, y)



	def repeatLastCommand(self):
		'''
		Repeat the last used command.
		'''
		self.sb.prevCommand()()
		print self.sb.prevCommand(docString=1) #print command name string
		


	def repeatLastView(self):
		'''
		Show the previous view.
		'''
		self.sb.previousView()()
		print self.sb.previousView(asList=1)








# ------------------------------------------------
# PaintEvent Overlay
# ------------------------------------------------
class Overlay(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(Overlay, self).__init__(parent)

		self.setAttribute(QtCore.Qt.WA_NoSystemBackground) #takes a single arg
		self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

		self.sb = Switchboard()
		self.point = QtCore.QPoint(self.sb.getUiSize(percentWidth=50), self.sb.getUiSize(percentHeight=50)) #set point to the middle of the layout

		self.start_line, self.end_line = self.point, QtCore.QPoint()



	def paintEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		uiName = self.sb.getUiName()
		if any([uiName=='main', uiName=='viewport', uiName=='editors']):

			greyPen = QtGui.QPen(QtGui.QColor(115, 115, 115), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
			blackPen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

			path = QtGui.QPainterPath()
			path.addEllipse(QtCore.QPointF(self.point), 7, 7)

			painter = QtGui.QPainter(self) #Initialize painter
			painter.fillRect(self.rect(), QtGui.QColor(127, 127, 127, 0)) #transparent overlay background.
			painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
			painter.setBrush(QtGui.QColor(115, 115, 115))
			painter.fillPath(path, QtGui.QColor(115, 115, 115))
			painter.setPen(blackPen)
			painter.drawPath(path) #stroke
			if not self.end_line.isNull():
				painter.setPen(greyPen)
				painter.drawLine(self.start_line, self.end_line)
				painter.drawEllipse(self.end_line, 5, 5)



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.start_line = self.point
		self.end_line = event.pos()
		self.update()



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.end_line = event.pos()
		self.update()



	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.start_line = self.point
		self.end_line = QtCore.QPoint()



class OverlayFactoryFilter(QtCore.QObject):
	def __init__(self, parent=None):
		super(OverlayFactoryFilter, self).__init__(parent)
		
		self.m_overlay = None



	def setWidget(self, w):
		'''
		args:
			w=<QWidget>
		'''
		w.installEventFilter(self)
		if self.m_overlay is None:
			self.m_overlay = Overlay()
		self.m_overlay.setParent(w)



	def eventFilter(self, obj, event):
		'''
		args:
			event=<QEvent>
		'''
		if not obj.isWidgetType():
			return False

		if event.type() == QtCore.QEvent.MouseButtonPress:
			self.m_overlay.mousePressEvent(event)

		elif event.type() == QtCore.QEvent.MouseButtonRelease:
			self.m_overlay.mouseReleaseEvent(event)

		elif event.type() == QtCore.QEvent.MouseMove:
			self.m_overlay.mouseMoveEvent(event)

		elif event.type() == QtCore.QEvent.MouseButtonDblClick:
			self.m_overlay.mouseDoubleClickEvent(event)

		elif event.type() == QtCore.QEvent.Resize:
			if self.m_overlay and self.m_overlay.parentWidget() == obj:
				self.m_overlay.resize(obj.size())

		elif event.type() == QtCore.QEvent.Show:
			self.m_overlay.raise_()
			#self.m_overlay.activateWindow()

		return super(OverlayFactoryFilter, self).eventFilter(obj, event)









# ------------------------------------------------
# Garbage-collection-management
# ------------------------------------------------
class _GCProtector(object):
	widgets=[]




# ------------------------------------------------
# Initialize
# ------------------------------------------------
def createInstance():

	app = QtWidgets.QApplication.instance()
	if not app:
		app = QtWidgets.QApplication([])

	try: mainWindow = MaxPlus.GetQMaxMainWindow(); mainWindow.setObjectName('MaxWindow')
	except: mainWindow = [x for x in app.topLevelWidgets() if x.objectName() == 'MayaWindow'][0]
	
	hotBox = HotBox(mainWindow)
	hotBox.layoutStack('init') #initialize layout
	hotBox.overlay = OverlayFactoryFilter()
	hotBox.overlay.setWidget(hotBox)


	_GCProtector.widgets.append(hotBox)

	return hotBox










#module name
print os.path.splitext(os.path.basename(__file__))[0]


# -----------------------------------------------
# Notes
# -----------------------------------------------

# deprecated

		# # if not self.name=='init': #remove old and add new signals for current ui from connectionDict
		# if self.name!=self.sb.previousName(allowDuplicates=1):
		# 	if self.sb.previousName():
		# 		self.sb.removeSignal(self.sb.previousName())
		# 		self.sb.addSignal(self.name)
		# 	else: #if no previous ui exists
		# 		self.sb.addSignal(self.name)


	# def mouseMoveEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''
	# 	if self.name=='main':
	# 		self.setVisibilityOnHover(event.pos(), 'r000-9')
	# 		self.setDown_(event.pos(), 'i003-32, v000-37')
	# 		self.showPopup_(event.pos(), 'cmb000-2')

	# 	if self.name=='editors':
	# 		self.setVisibilityOnHover(event.pos(), 'r000-9')
	# 		self.setDown_(event.pos(), 'v000-4')
	# 		# self.showPopup_(event.pos(), 'cmb000-2')

	# 	elif self.name=='viewport':
	# 		self.setVisibilityOnHover(event.pos(), 'r000-8')
	# 		self.setDown_(event.pos(), 'v000-29')
	# 		self.showPopup_(event.pos(), 'cmb000-3')



	# def unpackNames(self, nameString):
	# 	'''
	# 	Get a list of individual names from a single name string.
	# 	args:
	# 		nameString=string consisting of widget names separated by commas. ie. 'v000, b004-6'
	# 	returns:
	# 		unpacked names. ie. ['v000','b004','b005','b006']
	# 	'''
	# 	packed_names = [n.strip() for n in nameString.split(',') if '-' in n] #build list of all widgets passed in containing '-'

	# 	unpacked_names=[]
	# 	for name in packed_names:
	# 		name=name.split('-') #ex. split 'b000-8'
	# 		prefix = name[0].strip('0123456789') #ex. split 'b' from 'b000'
	# 		start = int(name[0].strip('abcdefghijklmnopqrstuvwxyz') or 0) #start range. #ex. '000' #converting int('000') returns None, if case; assign 0.
	# 		stop = int(name[1])+1 #end range. #ex. '9' from 'b000-8' for range up to 9 but not including 9.
	# 		unpacked_names.extend([str(prefix)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)]) #build list of name strings within given range

	# 	names = [n.strip() for n in nameString.split(',') if '-' not in n] #all widgets passed in not containing '-'

	# 	return names+unpacked_names



	# def getUiObject(self, widgets):
	# 	'''
	# 	Get ui objects from name strings.
	# 	args:
	# 		widgets='string' - ui object names
	# 	returns:
	# 		list of corresponding ui objects	
	# 	'''
	# 	objects=[]
	# 	for name in self.unpackNames(widgets):
	# 		try:
	# 			w = getattr(self.ui, name)
	# 			objects.append(w)
	# 		except: pass
	# 	return objects



	# def setVisibilityOnHover(self, mousePosition, widgets):
	# 	'''
	# 	Show/hide widgets on mouseover event.
	# 	args:
	# 		mousePosition=QPoint
	# 		widgets=string consisting of widget names separated by commas. ie. 'r000, r001, v000-13, i020-23'
	# 	'''
	# 	for w in self.getUiObject(widgets):
	# 		if w.geometry().contains(mousePosition):
	# 			w.show()
	# 		else:
	# 			w.hide()



	# def setDown_(self, mousePosition, widgets):
	# 	'''
	# 	Set pushbutton down state.
	# 	args:
	# 		mousePosition=QPoint
	# 		widgets=string consisting of widget names separated by commas. ie. 'r000, r001, v000-13, i020-23'
	# 	'''
	# 	for w in self.getUiObject(widgets):
	# 		if w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos())):
	# 			w.setDown(True)
	# 		else:
	# 			w.setDown(False)



	# def showPopup_(self, mousePosition, widgets):
	# 	'''
	# 	Set comboBox popup state.
	# 	args:
	# 		mousePosition=QPoint
	# 		widgets=string 
	# 	'''
	# 	for w in self.getUiObject(widgets):
	# 		if w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos())):
	# 			# w.showPopup()
	# 			w.setStyleSheet('''
	# 				QComboBox {
	# 				background-color: rgba(82,133,166,200);
	# 				color: white;
	# 				}
	# 				''')
	# 		else:
	# 			# w.hidePopup()
	# 			w.setStyleSheet('''
	# 				background-color: rgba(100,100,100,200);
	# 				color: white;
	# 				}
	# 				''')



# def hoverEvent(self, event):
# 		'''
# 		args:
# 			event=<QEvent>
# 		'''
# 		print "hover"


# def onSignalEvent(self, widgetName):
# 	'''
# 	Called on any ui widget before it's signal is triggered.
# 	args:
# 		widgetName='string' - objectName of button
# 	'''
# 	widget = self.getWidget(widgetName)

# 	if widgetName.startswith('i'): #connect to layoutStack and pass in an index as int or string 'name'.
# 		index = widget.whatsThis() #widget.text()
# 		self.layoutStack(index) #switch the stacked layout to the given ui.

# 	if widgetName.startswith('b'): #ie. 'b012'
# 		self.sb.prevCommand(as_list=1).append([self.sb.getMethod(widgetName), self.sb.getDocString(widgetName)]) #store the command method object and it's docString (ie. 'Multi-cut tool')

# 	if widgetName.startswith('v'): #ie. 'v012'
# 		self.sb.previousView(as_list=1).append(self.sb.getMethod(widgetName)) #store the camera view



# # ------------------------------------------------
# # Popup Window
# # ------------------------------------------------
# class Popup(QtWidgets.QWidget):
# 	def __init__(self, ui, parent=None):
# 		QtWidgets.QWidget.__init__(self, parent)

# 		layout = QtWidgets.QGridLayout(self)
# 		layout.addWidget(ui)
# 		layout.setContentsMargins(0,0,0,0) #adjust the margins or you will get an invisible, unintended border

# 		self.setLayout(layout)
# 		self.adjustSize()

# 		self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint) #tag this widget as a popup



# # ------------------------------------------------
# # Grid
# # ------------------------------------------------
# class Grid(QtWidgets.QWidget):
# 	def __init__(self, hotBox, parent=None):
# 		super(Grid, self).__init__(parent)


# 		# layout = QtWidgets.QHBoxLayout(self)
# 		# layout.setSpacing(0)
# 		# layout.setContentsMargins(0,0,0,0)

# 		# self.pin = Pin(hotBox)
# 		# layout.addWidget(self.pin)

# 		# self.cmb = QtWidgets.QComboBox()
# 		# self.cmb.setMaximumSize(18,18)
# 		# layout.addWidget(self.cmb)

# 		self.hotBox = hotBox

# 		self.hotBox.signal.buildConnectionDict('grid') #construct the signals and slots for the ui
# 		self.ui = self.hotBox.sb.getUi('grid')

# 		self.ui.pin.installEventFilter(self)



# 	def eventFilter(self, obj, event):
# 		# if event.buttons()==QtCore.Qt.LeftButton:
# 		if event.type()==QtCore.QEvent.MouseButtonPress:
# 			self.__mousePressPos = event.globalPos()
# 			return True

# 		if event.type()==QtCore.QEvent.MouseMove:
# 			self.hotBox.moveToMousePosition(self.hotBox, -self.hotBox.point.x(), -self.hotBox.point.y()*.1) #move window on left mouse drag.
# 			return True

# 		if event.type()==QtCore.QEvent.MouseButtonRelease:
# 			moveAmount = event.globalPos() - self.__mousePressPos
# 			if moveAmount.manhattanLength() > 5: #if button moved:
# 				self.setChecked(True) #setChecked to prevent window from closing.
# 				event.ignore()
# 			else:
# 				self.setChecked(not self.isChecked()) #toggle check state
# 				self.hotBox.hide_()
# 			return True
# 		return False #return False for other event types




# class Pin(QtWidgets.QPushButton):
# 	'''
# 	Pushbutton overridden to move the main window on left mouse drag event.
# 	When checked, prevents hide event on main window.
# 	'''
# 	def __init__(self, hotBox, parent=None):
# 		super(Pin, self).__init__(parent)

# 		self.hotBox = hotBox
# 		self.setCheckable(True)


# 	def mousePressEvent(self, event):
# 		'''
# 		args:
# 			event=<QEvent>
# 		'''
# 		if event.button()==QtCore.Qt.LeftButton:
# 			self.__mousePressPos = event.globalPos()


# 	def mouseMoveEvent(self, event):
# 		'''
# 		args:
# 			event=<QEvent>
# 		'''
# 		if event.buttons()==QtCore.Qt.LeftButton:
# 			self.hotBox.moveToMousePosition(self.hotBox, -self.hotBox.point.x(), -self.hotBox.point.y()*.1) #move window on left mouse drag.


# 	def mouseReleaseEvent(self, event):
# 		'''
# 		args:
# 			event=<QEvent>
# 		'''
# 		if event.button()==QtCore.Qt.LeftButton:
# 			moveAmount = event.globalPos() - self.__mousePressPos
# 			if moveAmount.manhattanLength() > 5: #if button moved:
# 				self.setChecked(True) #setChecked to prevent window from closing.
# 				event.ignore()
# 			else:
# 				self.setChecked(not self.isChecked()) #toggle check state
# 				self.hotBox.hide_()