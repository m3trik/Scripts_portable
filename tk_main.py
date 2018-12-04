#	|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#	||||||||||||||||||||||||||||||||     hotBox marking menu     ||||||||||||||||||||||||||||||||
#	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from PySide2 import QtCore, QtGui, QtWidgets
from ctypes import windll, Structure, c_long, byref

import sys, os.path
from PySide2.QtUiTools import QUiLoader

from pydoc import locate
import tk_styleSheet as styleSheet

try: import MaxPlus
except: pass




# ------------------------------------------------
# Get relative path to ui files
# ------------------------------------------------

#set path to the directory containing the ui files.
script_dir = os.path.dirname(__file__) #dir of this module
rel_path = "tk_ui" #relative path to directory
path = os.path.join(script_dir, rel_path) #absolute path


# ------------------------------------------------
# Ui List
# ------------------------------------------------

#create a list of the names of the files in the ui folder, removing the prefix and extension.
def uiList():
	return [file_.replace('.ui','') for file_ in os.listdir(path) if file_.endswith('.ui')] #gets uiList from directory contents


# ------------------------------------------------
# Generate individual ui file paths
# ------------------------------------------------

#set path to ui files
def getQtui(name):
	#arg: string
	#returns: dynamic ui object
	qtui = QUiLoader().load(path+'/'+name+'.ui')
	return qtui


# ------------------------------------------------
#	Mouse Tracking
# ------------------------------------------------
class Point(Structure):
	_fields_ = [("x", c_long), ("y", c_long)]

def getMousePosition():
	pt = Point()
	windll.user32.GetCursorPos(byref(pt))
	return { "x": pt.x, "y": pt.y}

def moveWindow(window, x, y):
	#args: [object], [int], [int]
	mPos = getMousePosition()
	x = mPos['x']+x
	y = mPos['y']+y
	window.move(x, y)


# ------------------------------------------------
# Custom HotBox Widget
# ------------------------------------------------
class HotBox(QtWidgets.QWidget):

	mouseHover = QtCore.Signal(bool)

	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self)

		self.setObjectName(self.__class__.__name__) #set object name to: 'HotBox'

		#set window style
		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.X11BypassWindowManagerHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setStyle(QtWidgets.QStyleFactory.create("plastique"))
		self.setStyleSheet(styleSheet.css)
		
		self.mousePosition = None
		self.mousePressOn = True

		self.uiList = uiList() #ie. ['animation', 'cameras', 'create', 'display', 'edit']
		self.uiSizeDict={} #key is the ui name string identifier. value is a list containing width int, height int. ie. {'selection': [295, 234], 'scene': [203, 254], 'rendering': [195, 177]}
		self.prevName=[] #when a new ui is called its name is last and the previous ui is at element[-2]. ie. [previousNameString, previousNameString, currentNameString]
		
		self.app = parent.objectName().rstrip('Window').lower() #remove 'Window' from objectName ie. 'Maya' from 'MayaWindow' and set lowercase.
		
		self.signal = locate('tk_signals.Signal')(self)
		self.layoutStack()
		self.overlay = Overlay(self)
		# self.pin = Pin()
		
		

	def layoutStack(self, index=None):
		#args: [int]
		if not self.layout(): #if layout doesnt exist; init stackedLayout.
			self.stackedLayout = QtWidgets.QStackedLayout()

			for uiName in self.uiList:
				ui = getQtui(uiName) #get the dynamic ui
				# build dictionary to store size info for each ui
				self.uiSizeDict [uiName] = [ui.frameGeometry().width(), ui.frameGeometry().height()]
				# add ui to layoutStack
				self.stackedLayout.addWidget(ui) #add each ui
			self.setLayout(self.stackedLayout)
			index = self.uiList.index('init') #Initialize layout index to 'init'

		#set ui from stackedLayout
		self.stackedLayout.setCurrentIndex(index)
		#get ui from stackedLayout
		self.ui = self.stackedLayout.widget(index)

		self.index = index
		self.name = self.uiList[self.index] #use index to get name
		
		#get ui size from uiSideDict and resize window
		self.width = self.uiSizeDict[self.name][0]
		self.height = self.uiSizeDict[self.name][1]
		self.resize(self.width, self.height) #window size
		
		self.point = QtCore.QPoint(self.width/2, self.height/2) #set point to the middle of the layout
		
		self.init = locate('tk_slots_'+self.app+'_init.Init')(self) #equivalent to: import tk_slots_maya_init.Init
		
		if self.name=='init':
			self.init.info()
		else:
			if self.name not in self.signal.connectionDict: #construct the signals and slots for the ui 
				self.signal.buildConnectionDict()

			#remove old and add new signals for current ui from connectionDict
			if len(self.prevName)>1:
				if self.name!=self.prevName[-2]:
					self.signal.removeSignal(self.prevName[-2])
					self.signal.addSignal(self.name)
			else: #if no previous ui exists
				self.signal.addSignal(self.name)

			#build array that stores prevName string for removeSignal and open last used window command
			self.prevName.append(self.name)
			if len(self.prevName)>20:
				del self.prevName[0] #a long list provides the ability to skip past irrellivent windows that may have populated since the window that we are actually looking for.

			#close window when pin unchecked
			# if hasattr (self.ui, 'chkpin'):
			try: self.ui.chkpin.released.connect(self.hide_)
			except: pass


			#instead try entering main and viewport the same way submenus are entered as this produces the desired state.
			# self.mousePressOn = False
			# # import time
			# if self.name=='main':
			# 	windll.user32.mouse_event(0x10, 0, 0, 0,0) #right up
			# 	# time.sleep(.5)
			# 	# windll.user32.mouse_event(0x8, 0, 0, 0,0) #right down
				
			# if self.name=='viewport':
			# 	windll.user32.mouse_event(0x4, 0, 0, 0,0) #left up
			# 	# time.sleep(.5)
			# 	# windll.user32.mouse_event(0x2, 0, 0, 0,0) #left down
			# self.mousePressOn = True




# ------------------------------------------------
# overrides
# ------------------------------------------------


	def eventFilter(self, button, event):
		#args: [source object]
		#			 [QEvent]
		if event.type()==QtCore.QEvent.Type.Enter:
			self.mouseHover.emit(True)
			button.click()
			# if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
				# button.release()
			return True
		if event.type()==QtCore.QEvent.Type.HoverLeave:
			self.mouseHover.emit(False)
			return False
		return QtWidgets.QWidget.eventFilter(self, button, event)

# ------------------------------------------------


	def keyPressEvent(self, event):
		#args: [QEvent]
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat(): #Key_Meta or Key_Menu =windows key
			if all ([self.name!="init", self.name!="main", self.name!="viewport"]):
				self.layoutStack(self.uiList.index('init')) #reset layout back to init on keyPressEvent
		else:
			return super(HotBox, self).eventFilter(self, event) #returns the event that occurred
			
	def keyReleaseEvent(self, event):
		#args: [QEvent]
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat():
			self.hide_()
		else:
			return super(HotBox, self).eventFilter(self, event)


	def mousePressEvent(self, event):
		#args: [QEvent]
		if self.mousePressOn:
			if any ([self.name=="main", self.name=="viewport", self.name=="init"]):
				if event.button()==QtCore.Qt.LeftButton:
					self.layoutStack(self.uiList.index('viewport'))
				if event.button()==QtCore.Qt.RightButton:
					self.layoutStack(self.uiList.index('main'))
		else:
			return super(HotBox, self).eventFilter(self, event)

	def mouseDoubleClickEvent(self, event):
		#args: [QEvent]
		#show last used submenu on double mouseclick 
		if event.button()==QtCore.Qt.RightButton:
			if len(self.prevName)>0:
				if all ([self.prevName[-2]!="init", self.prevName[-2]!="main", self.prevName[-2]!="viewport"]):
					self.layoutStack(self.uiList.index(self.prevName[-2]))
				else: #search prevName for valid previously used submenu 
					if len(self.prevName)>2:
						i = -3
						for element in range (len(self.prevName) -2):
							if all ([self.prevName[i]!="init", self.prevName[i]!="main", self.prevName[i]!="viewport"]): 
								index = self.uiList.index(self.prevName[i])
								if index is not None:
									self.layoutStack(index)
							else:
								i-=1
		if event.button()==QtCore.Qt.LeftButton:
			try:
				buttons.repeatLastCommand()
			except: print "# Warning: No recent commands in history. #"
		else:
			return super(HotBox, self).eventFilter(self, event)

	def mouseMoveEvent(self, event):
		#args: [QEvent]
		if (event.buttons()==QtCore.Qt.LeftButton) or (event.buttons()==QtCore.Qt.RightButton):
			if (self.name=="main") or (self.name=="viewport"):
				self.mousePosition = event.pos()
				self.update()
			elif (self.name!="init"):
				if (event.buttons() & QtCore.Qt.LeftButton): #MiddleButton
					moveWindow(self, -self.point.x(), -self.point.y()*.1) #set mouse position and move window with mouse down
					self.ui.chkpin.setChecked(True)
					# Pin(self).show()
		else:
			return super(HotBox, self).eventFilter(self, event)

	def showEvent(self, event):
		try: MaxPlus.CUI.DisableAccelerators()
		except: pass
		#move window to cursor position and offset from left corner to center
		if any([self.name=="init", self.name=="main", self.name=="viewport"]):
			moveWindow(self, -self.point.x(), -self.point.y())
		else:
			moveWindow(self, -self.point.x(), -self.point.y()/2)
		self.activateWindow()
		self.raise_()
		self.setFocus()

	def hide_(self):
		try:
			if hasattr (self.ui, 'chkpin') and self.ui.chkpin.isChecked():
				return False
			else:
				self.hide()
				return True
		except Exception as exc:
			if not exc==RuntimeWarning: print exc

	def hideEvent(self, event):
		try: MaxPlus.CUI.EnableAccelerators()
		except: pass
		return self.layoutStack(self.uiList.index('init'))


# ------------------------------------------------
# PaintEvent Overlay
# ------------------------------------------------
# class Overlay(QtWidgets.QWidget):
# 	def __init__(self, parent=None):
# 		super(Overlay, self).__init__(parent)
# 		self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
# 		self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

# 		self.hotBox = parent
# 		self.resize(self.hotBox.width, self.hotBox.height)
# 		self.start_line, self.end_line = self.hotBox.point, QtCore.QPoint()


# 	def paintEvent(self, event):
# 		# Initialize painter
# 		painter = QtGui.QPainter(self)
# 		pen = QtGui.QPen(QtGui.QColor(115, 115, 115), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
# 		painter.setPen(pen)
# 		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
# 		painter.setBrush(QtGui.QColor(115, 115, 115))
# 		painter.drawEllipse(self.hotBox.point, 5, 5)
# 		if not self.end_line.isNull():
# 			painter.drawLine(self.start_line, self.end_line)

# 	def mousePressEvent(self, event):
# 		self.end_line = event.pos()
# 		self.update()

# 	def mouseMoveEvent(self, event):
# 		self.end_line = event.pos()
# 		self.update()

# 	def mouseReleaseEvent(self, event):
# 		self.end_line = QtCore.QPoint()



# class OverlayFactoryFilter(QtCore.QObject):
# 	def __init__(self, parent=None):
# 		super(OverlayFactoryFilter, self).__init__(parent)
# 		self.m_overlay = None

# 	def setWidget(self, w):
# 		w.installEventFilter(self)
# 		if self.m_overlay is None:
# 			self.m_overlay = Overlay()
# 		self.m_overlay.setParent(w)

# 	def eventFilter(self, obj, event):
# 		if not obj.isWidgetType():
# 			return False

# 		if event.type() == QtCore.QEvent.MouseButtonPress:
# 			self.m_overlay.mousePressEvent(event)
# 		elif event.type() == QtCore.QEvent.MouseButtonRelease:
# 			self.m_overlay.mouseReleaseEvent(event)
# 		elif event.type() == QtCore.QEvent.MouseMove:
# 			self.m_overlay.mouseMoveEvent(event)
# 		elif event.type() == QtCore.QEvent.MouseButtonDblClick:
# 			self.m_overlay.mouseDoubleClickEvent(event)

# 		elif event.type() == QtCore.QEvent.Resize:
# 			if self.m_overlay and self.m_overlay.parentWidget() == obj:
# 				self.m_overlay.resize(obj.size())
# 		elif event.type() == QtCore.QEvent.Show:
# 			self.m_overlay.raise_()
# 		return super(OverlayFactoryFilter, self).eventFilter(obj, event)


class Overlay(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(Overlay, self).__init__(parent)
		
		self.hotBox = parent
		self.resize(self.hotBox.width, self.hotBox.height)
		

	def paintEvent(self, event):
		#args: [QEvent]
		if any ([self.hotBox.name=="main", self.hotBox.name=="viewport"]):
			# self.raise_()
			# self.setWindowFlags(QtCore.Qt.WA_TransparentForMouseEvents)

			#Initialize painter
			painter = QtGui.QPainter(self)
			pen = QtGui.QPen(QtGui.QColor(115, 115, 115), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
			painter.setPen(pen)
			painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
			painter.setBrush(QtGui.QColor(115, 115, 115))
			painter.drawEllipse(self.hotBox.point, 5, 5)

			#perform paint
			if self.hotBox.mousePosition:
				mouseX = self.hotBox.mousePosition.x()
				mouseY = self.hotBox.mousePosition.y()
				line = QtCore.QLine(mouseX, mouseY, self.hotBox.point.x(), self.hotBox.point.y())
				painter.drawLine(line)
				painter.drawEllipse(mouseX-5, mouseY-5, 10, 10)


# ------------------------------------------------
# Pin Window
# ------------------------------------------------
class Pin(QtWidgets.QWidget): #keep the layout open using a new instance.
	def __init__(self, parent=None):
		super(Pin, self).__init__(parent)

		self.hotBox = parent
		self.resize(self.hotBox.width, self.hotBox.height)

		self.hotBox.ui.chkpin.setChecked(True)

		#set layout
		# self.layout = QtWidgets.QVBoxLayout()
		# print self.hotBox.index
		# self.layout.addWidget(self.hotBox.ui)
		# self.setLayout(self.layout)




# ------------------------------------------------
# Garbage-collection-management
# ------------------------------------------------
class _GCProtector(object):
	widgets = []


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




# -------------------------------------------------

