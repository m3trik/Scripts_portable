# ||||||||||||||||||||||||||||||||||||||||||||||||||
# |||||||||     hotBox marking menu     ||||||||||||
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from PySide2 import QtCore, QtGui, QtWidgets
from ctypes import windll, Structure, c_long, byref

import sys, os.path

from tk_switchboard import Switchboard
import tk_styleSheet as styleSheet

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
# Custom HotBox Widget
# ------------------------------------------------
class HotBox(QtWidgets.QWidget):

	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self)
		
		self.setObjectName(self.__class__.__name__) #set object name to: 'HotBox'
		
		#set window style
		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.X11BypassWindowManagerHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		# self.setStyle(QtWidgets.QStyleFactory.create("plastique"))
		self.setStyleSheet(styleSheet.css)
		
		# self.setMouseTracking(True) #mouse tracking events during mouse button up state.
		
		
		self.sb = Switchboard()
		
		self.app = self.sb.setApp(parent)
		
		self.sb.setClass(self) #add hotBox instance to switchboard dict
		self.signal = self.sb.setClass('tk_signals.Signal')()



	def layoutStack(self, index):
		'''
		#args:
			index=int - index for ui in stacked layout
				*or string - name of ui in stacked layout
		'''
		# import timeit
		# t0=timeit.default_timer()

		if type(index)!=int: #get index using name
			index = self.sb.getUiIndex(index)

		if not self.layout(): #if layout doesnt exist; initialize stackedLayout.
			self.stackedLayout = QtWidgets.QStackedLayout()

			for name, ui in self.sb.uiList():
				# store size info for each ui
				self.sb.setUiSize(name, [ui.frameGeometry().width(), ui.frameGeometry().height()])
				# ui.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
				# add ui to layoutStack
				self.stackedLayout.addWidget(ui) #add each ui
			self.setLayout(self.stackedLayout)


		self.index = index
		self.name = self.sb.setUiName(self.index) #get/set current ui name from index
		self.ui = self.sb.getUi() #get the current dymanic ui

		#set ui from stackedLayout
		self.stackedLayout.setCurrentIndex(self.index)

		
		#get ui size for current ui and resize window
		self.width = self.sb.getUiSize(width=1)
		self.height = self.sb.getUiSize(height=1)
		# self.ui.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.resize(self.width, self.height) #window size
		
		self.point = QtCore.QPoint(self.sb.getUiSize(percentWidth=50), self.sb.getUiSize(percentHeight=50)) #set point to the middle of the layout
		#position window
		if not any([self.name=='init', self.name=='main', self.name=='viewport']): #set initial positon on showEvent, and reposition here on index change.
			self.moveWindow(self, -self.point.x(), -self.point.y()/2)
			

		if not self.sb.hasKey(self.name, 'connectionDict'):
			self.signal.buildConnectionDict() #construct the signals and slots for the ui


		if self.name=='init':
			self.sb.getClass('init')().info()
		else:
			#remove old and add new signals for current ui from connectionDict
			if self.name!=self.sb.previousName(allowDuplicates=1):
				if self.sb.previousName():
					self.signal.removeSignal(self.sb.previousName())
					self.signal.addSignal(self.name)
				else: #if no previous ui exists
					self.signal.addSignal(self.name)



		#close window when pin unchecked
		try: self.ui.pin.released.connect(self.hide_)
		except: pass

		# t1=timeit.default_timer()
		# print 'time:',t1-t0

		



# ------------------------------------------------
# Event overrides
# ------------------------------------------------
	def hoverEvent(self, event):
		'''
		args: [QEvent]
		'''
		print "hover"


	def keyPressEvent(self, event):
		'''
		args: [QEvent]
		'''
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat(): #Key_Meta or Key_Menu =windows key
			if all ([self.name!='init', self.name!='main', self.name!='viewport']):
				self.layoutStack('init') #reset layout back to init on keyPressEvent
			
			
	def keyReleaseEvent(self, event):
		'''
		args: [QEvent]
		'''
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat():
			self.hide_()


	def mousePressEvent(self, event):
		'''
		args: [QEvent]
		'''
		if any ([self.name=='main', self.name=='viewport', self.name=='init', self.name=='display']):
			if event.button()==QtCore.Qt.LeftButton:
				self.layoutStack('viewport')

			elif event.button()==QtCore.Qt.RightButton:
				self.layoutStack('main')

			elif event.button()==QtCore.Qt.MiddleButton:
				self.layoutStack('display')


	def mouseDoubleClickEvent(self, event):
		'''
		args: [QEvent]
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
			if any([self.name=='init', self.name=='main', self.name=='viewport']):
				try: #repeat last command
					self.repeatLastCommand()
				except Exception as error:
					print "# Warning: No recent commands in history. #"


	def mouseMoveEvent(self, event):
		'''
		args: [QEvent]
		'''
		if self.name=='main':
			self.setVisibility(event.pos(), 'r000-11')
			self.setDown_(event.pos(), 'i003-18, i020-24, v000-30')

		if self.name=='viewport':
			self.setVisibility(event.pos(), 'r000-7')
			self.setDown_(event.pos(), 'v000-23')
			self.showPopup_(event.pos(), 'cmb000-3')

		elif self.name!='init' and event.buttons()==QtCore.Qt.LeftButton:
			if (event.buttons() & QtCore.Qt.LeftButton): #drag window and pin
				self.moveWindow(self, -self.point.x(), -self.point.y()*.1) #set mouse position and move window with mouse down
				self.ui.pin.setChecked(True)


	def unpackNames(self, nameString):
		'''
		get a list of inidvidual names from a single name string.
		args:	 nameString=string consisting of widget names separated by commas. ie. 'v000, b004-6'
		returns: unpacked names. ie. ['v000','b004','b005','b006']
		'''
		packed_names = [n.strip() for n in nameString.split(',') if '-' in n] #build list of all widgets passed in containing '-'

		unpacked_names=[]
		for name in packed_names:
			name=name.split('-') #ex. split 'b000-8'
			prefix = name[0].strip('0123456789') #ex. split 'b' from 'b000'
			start = int(name[0].strip('abcdefghijklmnopqrstuvwxyz') or 0) #start range. #ex. '000' #converting int('000') returns None, if case; assign 0.
			stop = int(name[1])+1 #end range. #ex. '9' from 'b000-8' for range up to 9 but not including 9.
			unpacked_names.extend([str(prefix)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)]) #build list of name strings within given range

		names = [n.strip() for n in nameString.split(',') if '-' not in n] #all widgets passed in not containing '-'

		return names+unpacked_names


	def getUiObject(self, widgets):
		'''
		get ui objects from name strings.
		args:	 widgets='string' - ui object names
		returns: list of corresponding ui objects	
		'''
		objects=[]
		for name in self.unpackNames(widgets):
			try:
				w = getattr(self.ui, name)
				objects.append(w)
			except: pass
		return objects


	def setVisibility(self, mousePosition, widgets):
		'''
		show/hide widgets.
		args:	mousePosition=QPoint
				widgets=string consisting of widget names separated by commas. ie. 'r000, r001, v000-13, i020-23'
		'''
		for w in self.getUiObject(widgets):
			if w.geometry().contains(mousePosition):
				w.show()
			else:
				w.hide()


	def setDown_(self, mousePosition, widgets):
		'''
		set pushbutton down state.
		args:	mousePosition=QPoint
				widgets=string consisting of widget names separated by commas. ie. 'r000, r001, v000-13, i020-23'
		'''
		for w in self.getUiObject(widgets):
			if w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos())):
				w.setDown(True)
			else:
				w.setDown(False)


	def showPopup_(self, mousePosition, widgets):
		'''
		set combobox popup state.
		args:	mousePosition=QPoint
				widgets=string 
		'''
		for w in self.getUiObject(widgets):
			if w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos())):
				# w.showPopup()
				w.setStyleSheet('''
					QComboBox {
					background-color: rgba(82,133,166,200);
					color: white;
					}
					''')
			else:
				# w.hidePopup()
				w.setStyleSheet('''
					background-color: rgba(100,100,100,200);
					color: white;
					}
					''')


	def hide_(self):
		try: #if pin is unchecked: hide
			if not self.ui.pin.isChecked():
				self.hide()
		except: #if ui doesn't have pin: hide
			self.hide()


	def hideEvent(self, event):
		'''
		args: [QEvent]
		'''
		try: MaxPlus.CUI.EnableAccelerators()
		except: pass
		self.layoutStack('init')


	def showEvent(self, event):
		'''
		args: [QEvent]
		'''
		try: MaxPlus.CUI.DisableAccelerators()
		except: pass
		self.moveWindow(self, -self.point.x(), -self.point.y()) #move window to cursor position and offset from left corner to center


	def moveWindow(self, window, x, y):
		#args: [object], [int], [int]
		mPos = getMousePosition()
		x = mPos['x']+x
		y = mPos['y']+y
		window.move(x, y)


	def repeatLastCommand(self):
		self.sb.prevCommand()() #execute command object
		print self.sb.prevCommand(docString=1) #print command name string
		

	def repeatLastView(self):
		self.sb.previousView()() #execute method
		print self.sb.previousView(asList=1)










# ------------------------------------------------
# PaintEvent Overlay
# ------------------------------------------------
class Overlay(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(Overlay, self).__init__(parent)

		self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
		self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

		self.sb = Switchboard()

		self.point = QtCore.QPoint(self.sb.getUiSize(percentWidth=50), self.sb.getUiSize(percentHeight=50)) #set point to the middle of the layout
		self.start_line, self.end_line = self.point, QtCore.QPoint()



	def paintEvent(self, event):
		if any([self.sb.getUiName()=='main', self.sb.getUiName()=='viewport']):
			painter = QtGui.QPainter(self) #Initialize painter
			painter.fillRect(self.rect(), QtGui.QColor(127, 127, 127, 0))
			pen = QtGui.QPen(QtGui.QColor(115, 115, 115), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
			painter.setPen(pen)
			painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
			painter.setBrush(QtGui.QColor(115, 115, 115))
			painter.drawEllipse(self.point, 5, 5)
			if not self.end_line.isNull():
				painter.drawLine(self.start_line, self.end_line)
				painter.drawEllipse(self.end_line, 5, 5)


	def mousePressEvent(self, event):
		self.start_line = self.point
		self.end_line = event.pos()
		self.update()


	def mouseMoveEvent(self, event):
		self.end_line = event.pos()
		self.update()


	def mouseReleaseEvent(self, event):
		self.start_line = self.point
		self.end_line = QtCore.QPoint()



class OverlayFactoryFilter(QtCore.QObject):
	def __init__(self, parent=None):
		super(OverlayFactoryFilter, self).__init__(parent)
		
		self.m_overlay = None



	def setWidget(self, w):
		w.installEventFilter(self)
		if self.m_overlay is None:
			self.m_overlay = Overlay()
		self.m_overlay.setParent(w)


	def eventFilter(self, obj, event):
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
			# self.m_overlay.activateWindow()
		return super(OverlayFactoryFilter, self).eventFilter(obj, event)







# ------------------------------------------------
# Popup Window
# ------------------------------------------------
class Popup(QtWidgets.QWidget):
	def __init__(self, parent = None, ui=None):
		QtWidgets.QWidget.__init__(self, parent)

		layout = QtWidgets.QGridLayout(self)
		layout.addWidget(ui)

		layout.setContentsMargins(0, 0, 0, 0) #adjust the margins or you will get an invisible, unintended border

		self.setLayout(layout)
		self.adjustSize()

		self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint) #tag this widget as a popup
		
		# point = ui.rect().bottomRight() #calculate the botoom right point from the parents rectangle
		# global_point = ui.mapToGlobal(point) #map that point as a global position

		# self.move(global_point - QtCore.QPoint(self.width(), 0)) #widget will be placed from its top-left corner, move it to the left based on the widgets width








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
	
	hotBox = HotBox(parent=mainWindow)
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

# ------------------------------------------------
	# def mouseReleaseEvent(self, event):
	# 	# if event.button() == QtCore.Qt.LeftButton:
	# 	if self.mouseHover:
	# 		# self.buttonObject.click()
	# 		pass
	# 		# print "mouseReleaseEvent", self.mouseHover
			

	# def leaveEvent(self, event):
	# 	#args: [QEvent]
	# 	#can be temp set with; self.leaveEventOn = bool
	# 	pass

# ------------------------------------------------


