# ||||||||||||||||||||||||||||||||||||||||||||||||||
# |||||||||     hotBox marking menu     ||||||||||||
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
path = os.path.join(os.path.dirname(__file__), 'tk_ui') #get absolute path from dir of this module + relative path to directory


# ------------------------------------------------
# Ui List
# ------------------------------------------------
#create a list of the names of the files in the ui folder, removing the extension.
def uiList():
	return [file_.replace('.ui','') for file_ in os.listdir(path) if file_.endswith('.ui')] #gets uiList from directory contents




# ------------------------------------------------
# Generate individual ui file paths
# ------------------------------------------------
#set path to ui files
def getQtui(name):
	'''
	arg:	 string
	returns: dynamic ui object
	'''
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
#	Manage Ui elements
# ------------------------------------------------
class Switchboard(object):
	def __init__(self):

		self.uiList_ = uiList()
		self.sbDict = {name:{} for name in self.uiList_} #initialize sbDict using the class names from uiList. ie. { 'edit':{}, 'create':{}, 'animation':{}, 'cameras':{}, 'display':{} }

		'''
		# key:values
		# 'class name' : 'string name of class'
				'class' : 'class object' 
				'size' : list containing width int, height int. ie. [295, 234]
				'connectionDict' : {'b001':{'buttonObject':b001, 'buttonObjectWithSignal':b001.connect, 'methodObject':main.b001, 'methodName':'Multi-Cut Tool'}},
		# uiList : formatted string list of all ui filenames in the ui folder.
		# prevName #when a new ui is called its name is last and the previous ui is at element[-2]. ie. [previousNameString, previousNameString, currentNameString]
		# prevCommand #history of commands. last used command method at element[-1].  list of 2 element lists. [[methodObject,'methodNameString']]  ie. [{b00, 'multi-cut tool'}]
		ex.
		sbDict={
		'polygons':{ 
		'class':Polygons, 
		'size':[295, 234], 
		'connectionDict':{'b001':{'buttonObject':b001, 'buttonObjectWithSignal':b001.connect, 'methodObject':main.b001, 'methodName':'Multi-Cut Tool'}},
		}
		'uiList':['animation', 'cameras', 'create', 'display', 'edit'],
		'prevName':['previousName', 'previousName', 'currentName'], 
		'prevCommand':[{b00, 'multi-cut tool'}] }
		
		'''

	def uiList(self): #ie. ['animation', 'cameras', 'create', 'display', 'edit']
		if not 'uiList' in self.sbDict: self.sbDict['uiList'] = self.uiList_
		return self.sbDict['uiList']

	def getUiName(self, index):
		return self.sbDict['uiList'][index]

	def getUiIndex(self, name):
		return self.sbDict['uiList'].index(name)

	def setUiSize(self, name, size): #set ui size
		self.sbDict[name]['size'] = size
		return self.sbDict[name]['size']

	def getUiSize(self, name): #get ui size
		return self.sbDict[name]['size']

	def setClassObject(self, name, fileName):
		if not name in self.sbDict: self.sbDict[name] = {}
		self.sbDict[name]['class'] = locate(fileName)
		return self.sbDict[name]['class']

	def getClassObject(self, name):
		return self.sbDict[name]['class']

	def prevName(self):
		if not 'prevName' in self.sbDict: self.sbDict['prevName'] = []
		return self.sbDict['prevName']

	def prevCommand(self):
		if not 'prevCommand' in self.sbDict: self.sbDict['prevCommand'] = []
		return self.sbDict['prevCommand']

	def connectionDict(self, name):
		if not 'connectionDict' in self.sbDict[name]: self.sbDict[name]['connectionDict'] = {}
		return self.sbDict[name]['connectionDict']

	def getSignal(self, name, buttonName):
		return self.sbDict[name]['connectionDict'][buttonName]['buttonObjectWithSignal']

	def getSlot(self, name, buttonName):
		return self.sbDict[name]['connectionDict'][buttonName]['methodObject']

	def setMethodName(self, name, methodString, methodName):
		self.sbDict[name]['connectionDict'][methodString]['methodName'] = methodName
		return self.sbDict[name]['connectionDict'][methodString]['methodName']

	def getMethodName(self, name, methodString):
		return self.sbDict[name]['connectionDict'][methodString]['methodName']
		
	def getMethod(self, name, methodString):
		return self.sbDict[name]['connectionDict'][methodString]['methodObject']

	def dict(self):
		return self.sbDict

	def hasKey(self, *args):
		if len(args)==1:
			if args[0] in self.sbDict: return True
			else: return False
		if len(args)==2:
			if args[1] in self.sbDict[args[0]]: return True
			else: return False
		if len(args)==3:
			if args[2] in self.sbDict[args[0]][args[1]]: return True
			else: return False



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

		self.sb = Switchboard()
		
		self.app = parent.objectName().rstrip('Window').lower() #remove 'Window' from objectName ie. 'Maya' from 'MayaWindow' and set lowercase.
		self.signal = self.sb.setClassObject('signal', 'tk_signals.Signal')(self)
		for name in self.sb.uiList(): self.sb.setClassObject(name, 'tk_slots_'+self.app+'_'+name+'.'+name.capitalize()) #append each corresponding class object of the uiList to switchboardDict

		self.layoutStack()
		self.overlay = Overlay(self)

		

	def layoutStack(self, index=None):
		#args:	[int] #layout index
		if not self.layout(): #if layout doesnt exist; init stackedLayout.
			self.stackedLayout = QtWidgets.QStackedLayout()

			for name in self.sb.uiList():
				ui = getQtui(name) #get the dynamic ui
				# build dictionary to store size info for each ui
				self.sb.setUiSize(name, [ui.frameGeometry().width(), ui.frameGeometry().height()])
				# add ui to layoutStack
				self.stackedLayout.addWidget(ui) #add each ui
			self.setLayout(self.stackedLayout)
			index = self.sb.getUiIndex('init') #Initialize layout index to 'init'

		self.index = index
		self.name = self.sb.getUiName(self.index) #use index to get name

		#set ui from stackedLayout
		self.stackedLayout.setCurrentIndex(self.index)
		#get ui from stackedLayout
		self.ui = self.stackedLayout.widget(self.index)
		
		#get ui size from uiSideDict and resize window
		self.width = self.sb.getUiSize(self.name)[0]
		self.height = self.sb.getUiSize(self.name)[1]
		self.resize(self.width, self.height) #window size
		
		self.point = QtCore.QPoint(self.width/2, self.height/2) #set point to the middle of the layout
		
		# self.init = locate('tk_slots_'+self.app+'_init.Init')(self) #equivalent to: import tk_slots_maya_init.Init
		self.init = self.sb.getClassObject('init')(self)
		if self.name=='init':
			self.init.info()
		else:
			if not self.sb.hasKey(self.name, 'connectionDict'):
				self.signal.buildConnectionDict() #construct the signals and slots for the ui 

			#remove old and add new signals for current ui from connectionDict
			if len(self.sb.prevName())>1:
				if self.name!=self.sb.prevName()[-2]:
					self.signal.removeSignal(self.sb.prevName()[-2])
					self.signal.addSignal(self.name)
			else: #if no previous ui exists
				self.signal.addSignal(self.name)

			#build array that stores prevName string for removeSignal and open last used window command
			self.sb.prevName().append(self.name)
			if len(self.sb.prevName())>20:
				del self.sb.prevName()[0] #a long list provides the ability to skip past irrellivent windows that may have populated since the window that we are actually looking for.

			#close window when pin unchecked
			# if hasattr (self.ui, 'chkpin'):
			try: self.ui.chkpin.released.connect(self.hide_)
			except: pass


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
		#args:	[source object]
		#		[QEvent]
		if event.type()==QtCore.QEvent.Type.Enter: #enter event
			self.mouseHover.emit(True)
			# print button.__class__.__name__
			if button.__class__.__name__ == 'QComboBox':
				button.setCurrentIndex(99)
				button.setCurrentIndex(0)
				button.showPopup()
			else:
				button.click()

		if event.type()==QtCore.QEvent.Type.HoverLeave:
			self.mouseHover.emit(False)

		return QtWidgets.QWidget.eventFilter(self, button, event)


# ------------------------------------------------


	def hoverEvent(self, event):
		#args: [QEvent]
		print "hover"


	def keyPressEvent(self, event):
		#args: [QEvent]
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat(): #Key_Meta or Key_Menu =windows key
			if all ([self.name!="init", self.name!="main", self.name!="viewport"]):
				self.layoutStack(self.sb.getUiIndex('init')) #reset layout back to init on keyPressEvent
			
			
	def keyReleaseEvent(self, event):
		#args: [QEvent]
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat():
			self.hide_()


	def mousePressEvent(self, event):
		#args: [QEvent]
		if self.mousePressOn:
			if any ([self.name=="main", self.name=="viewport", self.name=="init"]):
				if event.button()==QtCore.Qt.LeftButton:
					self.layoutStack(self.sb.getUiIndex('viewport'))
				if event.button()==QtCore.Qt.RightButton:
					self.layoutStack(self.sb.getUiIndex('main'))
				if event.button()==QtCore.Qt.MiddleButton:
					self.layoutStack(self.sb.getUiIndex('display'))


	def mouseDoubleClickEvent(self, event):
		#args: [QEvent]
		#show last used submenu on double mouseclick 
		if event.button()==QtCore.Qt.RightButton:
			if len(self.sb.prevName())>0:
				if all ([self.sb.prevName()[-2]!="init", self.sb.prevName()[-2]!="main", self.sb.prevName()[-2]!="viewport"]):
					self.layoutStack(self.sb.getUiIndex(self.sb.prevName()[-2]))
				else: #search prevName for valid previously used submenu 
					if len(self.sb.prevName())>2:
						i = -3
						for element in range (len(self.sb.prevName()) -2):
							if all ([self.sb.prevName()[i]!="init", self.sb.prevName()[i]!="main", self.sb.prevName()[i]!="viewport"]): 
								index = self.sb.getUiIndex(self.sb.prevName()[i])
								if index is not None:
									self.layoutStack(index)
							else:
								i-=1
		if event.button()==QtCore.Qt.LeftButton:
			try:
				self.repeatLastCommand()
			except Exception as error: 
				if not self.sb.prevCommand():
					print "# Warning: No recent commands in history. #"
				else:
					print error


	def mouseMoveEvent(self, event):
		#args: [QEvent]
		if (event.buttons()==QtCore.Qt.LeftButton) or (event.buttons()==QtCore.Qt.RightButton):
			if (self.name=="main") or (self.name=="viewport"):
				self.mousePosition = event.pos()
				self.update()
			elif (self.name!="init"):
				if (event.buttons() & QtCore.Qt.LeftButton): #drag window and pin
					moveWindow(self, -self.point.x(), -self.point.y()*.1) #set mouse position and move window with mouse down
					self.ui.chkpin.setChecked(True)
					# self.popup = Popup(self, self.ui)
					# self.popup.show()


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
				pass
			else:
				self.hide()
		except Exception as error:
			if error!=RuntimeWarning: print error

	def hideEvent(self, event):
		try: MaxPlus.CUI.EnableAccelerators()
		except: pass
		self.layoutStack(self.sb.getUiIndex('init'))


	def repeatLastCommand(self):
		self.sb.prevCommand()[-1][0]() #execute command object
		print self.sb.prevCommand()[-1][1] #print command name string
		






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
# Popup Window
# ------------------------------------------------
		# self.stackedLayout = QtWidgets.QStackedLayout()

		# 	for name in self.sb.uiList():
		# 		ui = getQtui(name) #get the dynamic ui
		# 		# build dictionary to store size info for each ui
		# 		self.uiSizeDict [name] = [ui.frameGeometry().width(), ui.frameGeometry().height()]
		# 		# add ui to layoutStack
		# 		self.stackedLayout.addWidget(ui) #add each ui
		# 	self.setLayout(self.stackedLayout)
		# 	index = self.sb.getUiIndex('init') #Initialize layout index to 'init'

		# #set ui from stackedLayout
		# self.stackedLayout.setCurrentIndex(index)
		# #get ui from stackedLayout
		# self.ui = self.stackedLayout.widget(index)


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

# ------------------------------------------------