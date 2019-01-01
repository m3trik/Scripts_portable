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
				self.layoutStack(self.uiList.index('init')) #reset layout back to init on keyPressEvent
			
			
	def keyReleaseEvent(self, event):
		#args: [QEvent]
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat():
			self.hide_()


	def mousePressEvent(self, event):
		#args: [QEvent]
		if self.mousePressOn:
			if any ([self.name=="main", self.name=="viewport", self.name=="init"]):
				if event.button()==QtCore.Qt.LeftButton:
					self.layoutStack(self.uiList.index('viewport'))
				if event.button()==QtCore.Qt.RightButton:
					self.layoutStack(self.uiList.index('main'))


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
		except Exception as exc:
			if not exc==RuntimeWarning: print exc

	def hideEvent(self, event):
		try: MaxPlus.CUI.EnableAccelerators()
		except: pass
		self.layoutStack(self.uiList.index('init'))


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

		# 	for uiName in self.uiList:
		# 		ui = getQtui(uiName) #get the dynamic ui
		# 		# build dictionary to store size info for each ui
		# 		self.uiSizeDict [uiName] = [ui.frameGeometry().width(), ui.frameGeometry().height()]
		# 		# add ui to layoutStack
		# 		self.stackedLayout.addWidget(ui) #add each ui
		# 	self.setLayout(self.stackedLayout)
		# 	index = self.uiList.index('init') #Initialize layout index to 'init'

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


'''
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



# -----------------------------------------------
# structure:
# -----------------------------------------------

tk_main:
	get dynamic ui files
	construct stacked layout with ui files
	set window flags and attributes
	set event filters
	construct paint event overlay



tk_signals:
	build connection dict for each class with corresponding signals and slots
	add/remove signals using the connection dict each time the stacked layouts index is changed
	add each relavent method call to a recent command list	



tk_slots:
	class that holds the corresponding slot methods for each layout in the stack




tk_shared_functions:
	functions shared across all Slot class modules








# -----------------------------------------------
# basic use:
# -----------------------------------------------

#pressed hotkey shows instance. release hides.
#mouse not pressed; general scene heads up info
#right mouse down shows main window.
#left mouse down shows viewport navigation.
#releasing the mouse over any of the buttons in those windows takes you to the corresponding submenu.
#double left mouseclick produces last used window.
#double right mouseclick repeats last command.
#dragging on an empty are of the widget moves the window and pins it open in a separate instance.
#holding ctrl while using Spinboxes increments/decrements by an extra decimal place.
#mouse over buttons while window pinned to get an explanation of its function.


# -----------------------------------------------
# to install:
# -----------------------------------------------

#set path to the directory containing the ui files.
ie. path = os.path.expandvars(r'%CLOUD%/____Graphics/Maya/Scripts/_Python/_path/tk_maya_ui')
#have tk_maya(or max)_functions and tk_maya(or max)_buttons in your python path

#understand that this was developed for personal use, and is an ongoing project, so I tend to debug as I run across something, rather than put a ton of checks in place initially.
#a lot of ui polishing is on my list, and is lots of fun, but not the highest priority


#to add additional layouts, simply add a ui file with the same naming convention in the ui path, then create a corresponding class of the same name. finally, tag the ui button's whatsThis with the ui name.




# -----------------------------------------------
# Notes
# -----------------------------------------------

#comment ascii font=Nancyj
#shelf item scripts can be found: C:\Users\m3\Documents\maya\2016\prefs\shelves


# Re-load Ui:
# import sys
# import os.path as os

# path = os.expandvars("%CLOUD%/____Graphics/Maya/scripts/_Python/_Python_startup")
# sys.path.append(path)

# reload(tk_main)




# -----------------------------------------------
# THINGS TO DO NOW:
# -----------------------------------------------

#read ui folder file list to populate uiList


#create; creating a primitive doesnt align to set axis
#spinboxes visible on set point
#wrap setattributes call in an undoinfo chunk

#duplicate w/transform spinboxes; convert to being interactive.
#add center pivot option

#bug: transform negative '-' sets spinbox value to 0.  

#line 1640, in b010
#     parent = pm.listRelatives(instances[0], parent=True)[0]
# UnboundLocalError: local variable 'instances' referenced before assignment

#build convert menu with a pair of comboboxes to select to/from

#create; angled pipe.  creates a basic pipe section and allows to interactively add angles/fittings/ etc.
#create; stairs.  step, rise, amount
#create; railing
#create; saved asset. store points to building block items etc ascii


#move ui path variable to a config file

#scene: set unreal/unity project. GamePipeline -sp "Unreal";
#scene: re-export last

#display; build a layer editor

#fix recent autosave;  %userprofile%/AppData/Local/Temp  get dir file list,  sort by date modified

#add try/except to delete history function

#fix in-view message alpha transparency

#use grow/shrink selection buttons to scroll through 'select by name' results.
#commands change the textfielchrome-extension://mpognobbkildjkofajifpdfhcoklimli/components/startpage/startpage.htmld text and call t001 function to select that node.
#possibly use the toggle function to keep tabs on list place
#prevent focus initially.  when focused chkpin down



#edit; delete (component) not working
# Traceback (most recent call last):
#   File "O:\Cloud/____Graphics/Maya/scripts/_Python/_Python_startup\tk_maya_buttons.py", line 1420, in b032
#     faces = func.getAllFacesOnAxis (axis)
#   File "O:\Cloud/____Graphics/Maya/scripts/_Python/_Python_startup\tk_maya_functions.py", line 45, in getAllFacesOnAxis
#     if pm.exactWorldBoundingBox (attr)[index] < -0.00001:
#   File "C:\Program Files\Autodesk\Maya2018\Python\lib\site-packages\pymel\internal\pmcmds.py", line 140, in exactWorldBoundingBox_wrapped
#     raise pymel.core.general._objectError(obj)
# pymel.core.general.MayaAttributeError: Maya Attribute does not exist (or is not unique):: u'|brake_disc|brake_disc|brake_discShape.e[261:262].f[0]'


#better clean up menu. with checkboxes for options

#better center pivot; check component or object mode and apply interactive transforms accordingly.
#possibly merge with main transform menu. and add separate spinboxes for x, y, and z. with the option to chain values to each other. 


#save; could not delete: elise_mid.009 find a way to delete file regardless of extension. possibly for filename in filenames: if filename.startswith('elise_mid.009'): remove file. maybe best to just get project root and search recursively.
#change default iterations to 5; save iteration amount to settings text file.


#undo queue combobox (command start with capital letters and functions start with lower case).
#scripting; recent commands combobox
 
add maya uv workflow to uv notes https://www.youtube.com/watch?v=cy1vqLw-agk


#consolidate all in edit> transfer.  batch transfer is missing. batch translate is being called instead.

#start a store settings text file

#in the functions module build a list and function that can track selection order
#later use it to create a tool instance

#align pivot; face normal

#create menu creates object on combobox index changed. adjusting settings edits the created objects inputs
#pm.plane = polyPlane[]   plane[0] points to pPlane1 (transform node), and plane[1] points to polyPlane1 (history node).

#tooltip for polygons>split vertex

#display> wireframe inactive; set to query current mode and if wireframe: set to shaded then apply.  otherwise doesn't work

#create function for populating new window/message window

#add custom keyboard shortcuts via python script instead of manually

#pinned windows re-open as separate instance

#radial array 
# ['VRayLightRect1', 'VRayLightRect1_ins1', 'VRayLightRect1_ins2', 'VRayLightRect1_ins3', 'VRayLightRect1_ins4', 'VRayLightRect1_ins5', 'VRayLightRect1_ins6', 'VRayLightRect1_ins7', 'VRayLightRect1_ins8', 'VRayLightRect1_ins9', 'VRayLightRect1_ins10', 'VRayLightRect1_ins11', 'VRayLightRect1_ins12', 'VRayLightRect1_ins13', 'VRayLightRect1_ins14', 'VRayLightRect1_ins15', 'VRayLightRect1_ins16', 'VRayLightRect1_ins17', 'VRayLightRect1_ins18', 'VRayLightRect1_ins19', 'VRayLightRect1_ins19', 'VRayLightRect1_ins19_ins1', 'VRayLightRect1_ins19_ins2', 'VRayLightRect1_ins19_ins3', 'VRayLightRect1_ins19_ins4', 'VRayLightRect1_ins19_ins5', 'VRayLightRect1_ins19_ins6', 'VRayLightRect1_ins19_ins7', 'VRayLightRect1_ins19_ins8', 'VRayLightRect1_ins19_ins9', 'VRayLightRect1_ins19_ins10', 'VRayLightRect1_ins19_ins11', 'VRayLightRect1_ins19_ins12', 'VRayLightRect1_ins19_ins13', 'VRayLightRect1_ins19_ins14', 'VRayLightRect1_ins19_ins15', 'VRayLightRect1_ins19_ins16', 'VRayLightRect1_ins19_ins17', 'VRayLightRect1_ins19_ins18', 'VRayLightRect1_ins19_ins19', 'VRayLightRect1', 'VRayLightRect1_dup1', 'VRayLightRect1_dup2', 'VRayLightRect1_dup3', 'VRayLightRect1_dup4', 'VRayLightRect1_dup5', 'VRayLightRect1_dup6', 'VRayLightRect1_dup7', 'VRayLightRect1_dup8', 'VRayLightRect1_dup9', 'VRayLightRect1_dup10', 'VRayLightRect1_dup11', 'VRayLightRect1_dup12', 'VRayLightRect1_dup13', 'VRayLightRect1_dup14', 'VRayLightRect1_dup15', 'VRayLightRect1_dup16', 'VRayLightRect1_dup17', 'VRayLightRect1_dup18', 'VRayLightRect1_dup19', 'VRayLightRect1_dup19', 'VRayLightRect1_dup19_dup1', 'VRayLightRect1_dup19_dup2', 'VRayLightRect1_dup19_dup3', 'VRayLightRect1_dup19_dup4', 'VRayLightRect1_dup19_dup5', 'VRayLightRect1_dup19_dup6', 'VRayLightRect1_dup19_dup7', 'VRayLightRect1_dup19_dup8', 'VRayLightRect1_dup19_dup9', 'VRayLightRect1_dup19_dup10', 'VRayLightRect1_dup19_dup11', 'VRayLightRect1_dup19_dup12', 'VRayLightRect1_dup19_dup13', 'VRayLightRect1_dup19_dup14', 'VRayLightRect1_dup19_dup15', 'VRayLightRect1_dup19_dup16', 'VRayLightRect1_dup19_dup17', 'VRayLightRect1_dup19_dup18', 'VRayLightRect1_dup19_dup19', 'VRayLightRect1', 'VRayLightRect1_ins1', 'VRayLightRect1_ins2', 'VRayLightRect1_ins3', 'VRayLightRect1_ins4', 'VRayLightRect1_ins5', 'VRayLightRect1_ins6', 'VRayLightRect1_ins7', 'VRayLightRect1_ins8', 'VRayLightRect1_ins9', 'VRayLightRect1_ins10', 'VRayLightRect1_ins11', 'VRayLightRect1_ins12', 'VRayLightRect1_ins13', 'VRayLightRect1_ins14', 'VRayLightRect1_ins15', 'VRayLightRect1_ins16', 'VRayLightRect1_ins17', 'VRayLightRect1_ins18', 'VRayLightRect1_ins19'] #
# Traceback (most recent call last):
#   File "O:\Cloud/____Graphics/Maya/scripts/_Python/_Python_startup\tk_maya_func.py", line 1836, in b038
#     self.b001(create=True)
#   File "O:\Cloud/____Graphics/Maya/scripts/_Python/_Python_startup\tk_maya_func.py", line 1554, in b001
#     pm.polyUnite (radialArrayObjList, name=objectName)
#   File "C:\Program Files\Autodesk\Maya2018\Python\lib\site-packages\pymel\internal\factories.py", line 957, in newFuncWithReturnFunc
#     res = beforeReturnFunc(*args, **kwargs)
#   File "C:\Program Files\Autodesk\Maya2018\Python\lib\site-packages\pymel\internal\pmcmds.py", line 140, in polyUnite_wrapped
#     raise pymel.core.general._objectError(obj)
# pymel.core.general.MayaNodeError: Maya Node does not exist (or is not unique):: u'VRayLightRect1_ins1'

#add all relevant options for smooth preview located in poly display properties.

#image plane setup; get size of selected image and construct plane at camera
#look at maya/workflow notes for proper workflow to automate
#lock; aspect ratio on plane.  backface culling.

#default xyz values for transform move and rotate. 
	#add rotate (scale, move) 'by camera' option to transform
	#center pivot (object seems to work best) option (on by default)
transform:
	add tweak mode checkbox. strsTweakMode true; click and drag mode for adjusting components
	add step snap relative. manipMoveSetSnapMode 1; toggle off 0 checkable transform an object or component in incriments
	add step snap absolute. manipMoveSetSnapMode 2; toggle off 0 checkable ""
	for both; textfield defalt float 1.00. manipMoveContext -edit -snapValue value Move;

#add button for soften/ harden edge procedure. I think it is in a tab here or in python startup.
#in normals: create procedure for: if creased; edge harden else; soften. crease transfer algorithm my have useful parts.
fix crease transfer algorithm 
	#note future features such as bevel all creased edge by crease value
	#explore idea of working with hard/soft edges and transforming them to creased edges

#create> text
import maya.app.type.typeToolSetup
maya.app.type.typeToolSetup.createTypeTool()

create init button.  rehash functions module

Cannot find procedure "bt_snapAlignObjectToComponentOptions".
	Start of trace: (command window: line 1).

add toggle polyVertex Face to display menu. or look into face draw size option. doMenuComponentSelection("elise_bodyShell_mid_001", "pvf");
	$mode = `selectMode -query -component`;
	if ($mode==0)
	changeSelectMode -component;
	$maskVertex = `selectType -query -vertex`;
	
#add grease pencil window to grease pencil tool as option
GreasePencilTool;
createGreasePencilWindow();

#add clipping planes to display
#could query current camera and getAttr and change perspShape to "current camera"+Shape
# or just have a camera settings button that shows the settings in the attribute editor. 
pm.setAttr ("perspShape.nearClipPlane", 0.001)
pm.setAttr ("perspShape.farClipPlane", 10000)

# dR_selConstraintAngle; #alternate command syntax. use regex
dR_DoCmd("selConstraintAngle"); #takes an angle value
dR_DoCmd("selConstraintBorder");
dR_DoCmd("selConstraintElement");
dR_DoCmd("selConstraintOff");



EXTEND FUNCTIONALITY:

modify'frame selected' to query symmetry state (because when more than 1 vertex is selected, they are generally far apart) edit: $state = `symmetricModelling -query -symmetry`;



UI FUNCTIONALITY:

transparent shortcut buttons reveal text name when moused over
transparent shortcut groups can be changed in preferences. ie. modeling shortcuts, rendering shortcuts

#tk_maya init; ui in sub-folder with tk_main instead of path (just copy code from test.py)
#importing tk_maya_buttons as buttons instead of * would be pointless if splitting up the button module later 

#outputwindow text color for help messages

#push text from a helpline to a textfield

#finish ui stylesheet
#simply the way signals and slots are built based on the way the stylesheet builds styles
#move all 

#spinboxes increment an extra decimal place while holding shift key (pyside key modifiers)






MORE INVOLVED:

#add framework for interactive tools (use radial array as a model)

build layer editor.

build a selection function that returns different the current selection
	filter by type:
	as string:
		main object from component
	as object
	converted to:
		vertices
		faces
		edges
	various ls flags:
	all objects

radial symmetry

straighten circle tool.
average curve tool.


script command popup elf window commands like mel2py won't accept multiple lines of code. tried to fix and now completely broken. possibly have a look and see if its not better to just convert it and 'scene options' elf windows into qt ui and add them to layout stack.


play with contrain edge options to build useful selection constraints

#better insert edge tool
polySplitRing -constructionHistory off -smoothingAngle 30 -weight 0.9 -fixQuads 1;

collapse edge/
	pm.selectPref (preSelectClosest=True) #definitely want this setting off when not used
	selectPref -preSelectSize 15; #this sets the preselect area tolerance (i think)
	closestVert = pm.ls (selection=True)
	print closestVert
stitch tool
	selectPref(trackSelectionOrder=True)

build heads up display:
	symmetry state
	any active selection constraits
	polycount
	pm.helpLine(width=20, height=8)
	progress bar

select island doesnt work with symmetry also needs the abiltiy for multiple selections







OLD:

functionality to add:

quick rotate menu set. rotate by textedit amount + or - (default 45).

marking menu normals 'set to face' add command average normals before calling
add button edit> Optimize Scene mel; OptimizeScene;
modify Un crease edge so that it works both in object mode for all edges and component mode on just selected edges
add crease 'sets' button; python code: from maya.app.general import creaseSetEditor creaseSetEditor.showCreaseSetEditor()
add toggle crease edge visibility mel; polyOptions -displayCreaseEdge true; polyOptions -displayCreaseEdge false; modify to iterate through and toggle crease display for all objects in the scene. this is a good candidate for a checkbox
modify script; if nothing selected export visible geometry
understand symmetry and getting the align edge loop tool to work with it
functionality for hotkey g repeat last to be used on custom tools
add button toggle script editor output window size
fix sets in toolkit. add buttons from create> sets; set partition, quick select set and options
add buttons; edit mesh> vertex> average vertices, chamfer vertices, reorder vertices
uv tool popup mel window
add button 'Transfer Maps' (no options) mel: performSurfaceSampling 1; 
hotkey hide other objects f2; check for how many objects visible before executing if <2 inView error message
query poly clean up to get current flag state
building on top of existing straighten edgeloop script:use selection order to build an array and iterate through multiple edgeloops
check box support
create instance toggle for all duplicate actions
mod toolkit selection contraints; create drop down menu to select contraint and user input for contraint angle
change minimum size for tool settings, channel/layers
UV display put current display settings in array and toggle off/on 
heads up display for current selection count
toggle (black) silhouette of geometry  (to see low poly curvature ect)





#batch export FBX and OBJ
proc batchExport (string $fileType)
	{
	$selection = createArrayFromSelection();
	$exportPath = sourceDirectory($fileType);

	for ($node in $selection)
		{
		$finalExportPath = ($exportPath+"/"+$node);

		if ($fileType == "obj")
			{
			// select -replace $node;
			file -force
						-exportSelected
						-preserveReferences 
						-type "OBJexport"
						-options "-groups 0 \
											-ptgroups 0 \
											-materials 0 \
											-smoothing 1 \
											-normals 1"
						// ($node+".obj");
						($finalExportPath+".obj");
						print ($finalExportPath+".obj"+"\n");
			}

		if ($fileType == "fbx")
			{
			// // Uncomment for export options
			// // Geometry
			// FBXExportSmoothingGroups -v true;
			// FBXExportHardEdges -v false;
			// FBXExportTangents -v false;
			// FBXExportSmoothMesh -v true;
			// FBXExportInstances -v false;
			// FBXExportReferencedContainersContent -v false;
			// // Animation
			// FBXExportBakeComplexAnimation -v false;
			// // FBXExportBakeComplexStart -v "";
			// // FBXExportBakeComplexEnd -v "";
			// FBXExportBakeComplexStep -v 1;
			// // FBXExportBakeResampleAll -v true;
			// FBXExportUseSceneName -v false;
			// // FBXExportQuaternion -v euler;
			// FBXExportShapes -v true;
			// FBXExportSkins -v true;
			// // Constraints
			// FBXExportConstraints -v false;
			// // Cameras
			// FBXExportCameras -v false;
			// // Lights
			// FBXExportLights -v false;
			// // Embed Media
			// FBXExportEmbeddedTextures -v false;
			// // Connections
			// FBXExportInputConnections -v false;
			// // Axis Conversion
			// FBXExportUpAxis y;

			// print ($finalExportPath+"\n");
			FBXExport -selected -file ($finalExportPath+".fbx");
			print ($finalExportPath+".fbx"+"\n");
			}
		}
	}







- da_intPlay: this script add the interactive play button directly to Time Slider
- da_curveToPoly: this script make possible the conversion of curves in polygons
- da_interactiveBooleans: this script make the Polygonal Boolean process more interactive
- da_BooleanFullIntersect: this script make a full intersect, so this execute a mesh subtraction but maintain subtracted part as separate object
- da_PlaneCutter: this script cut a mesh by using a flat mesh, this can be useful for simulate surface cracks
- da_AutoBevel: this script analyse the angle between faces and try to add a Bevel node only on needed edges
- da_ClothAsDeformer: this script set up the current mesh to be deformed by nCloth solver, this can be useful for simulate character selfcollision skin or muscle dynamics
- da_nParticleConverter: this script add the ability to convert particle to a specific type after their creation
- da_perspToggle: this script convert the current persp view to the closest ortho, and vice versa
- da_shell: this script emulates Shell deformer of Autodesk 3D Studio Max, by adding a thickness to flat polygons
- da_ConvertToMetaballs: this script convert particles to polygonal Metaballs
- da_MashVoxelizer: this script use MASH to voxelize an arbitrary mesh inside of another mesh
- da_RivetMash: this script constraint the pivot of a polygon to a component of another polygon
- da_CurveDistributionMash: this script scatter and constrain a polygonal object along a curve
- da_EdgeToLoopToCurve: this script convert edge selection to loop and then make a batch conversion to curves, this is useful for converting polygonal hair to curve hair 
- da_SurfaceScatterMash: this script scatter and constrain a polygonal object on a mesh
- da_CurveLength: this script returns the length of a curve in Maya unit
- da_MouseTrack: this script tracks the mouse movement and create an animation
- da_FacesFollicles: this script creates a follicle in the centre of selected faces
- da_Compass: this script converts Euler angle into a XYZ vector, for drive wind direction in Nucleus and Air Filed
- da_CombineCurves: this script combines curves in a single transform
- da_SepareCurves: this script separate combined curves
- da_MapFacesUV: this script maps any single faces of a mesh as separate planar UV shell
- da_KeyKeyedOnly: this script creates animation keys only on already animated channels
- Control Constraint: this set of scripts constraint a controller to a single or multiple controlled object(s)





'''
















'''