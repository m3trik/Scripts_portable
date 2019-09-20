# |||||||||||||||||||||||||||||||||||||||||||||||||
# ||||||   	 	hotBox marking menu			|||||||
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from PySide2 import QtCore, QtGui, QtWidgets

import sys, os.path

from tk_switchboard import Switchboard
from tk_styleSheet import StyleSheet
from tk_overlay import OverlayFactoryFilter
from tk_childEvents import EventFactoryFilter

try: import MaxPlus
except: pass






# ------------------------------------------------
# Widget Stack
# ------------------------------------------------
class HotBox(QtWidgets.QStackedWidget):
	'''
	Marking menu-style modal window.
	Gets and sets signal connections through the switchboard module.
	Paint events are handled by the overlay module.
	args:
		parent=main application window object.
	'''
	def __init__(self, parent=None):
		super(HotBox, self).__init__(parent)

		#set window style
		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint) #QtCore.Qt.X11BypassWindowManagerHint|QtCore.Qt.WindowStaysOnTopHint
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setStyleSheet(StyleSheet.css)
		# self.setStyle(QtWidgets.QStyleFactory.create('plastique'))

		self.sb = Switchboard(parent)
		self.sb.setClass(self) #store this class instance.

		for name, ui in self.sb.uiList():
			self.sb.setUiSize(name) #store size info for each ui
			self.addWidget(ui) #add each ui to the stackedLayout.

		self.childEvents = EventFactoryFilter()



	def setWidget(self, name):
		'''
		Set the stacked Widgets index.
		args:
			index=int - 'string' - name of ui in stacked layout.
		'''
		self.name = self.sb.setUiName(name) #set ui name
		self.ui = self.sb.getUi() #get the current dymanic ui

		self.setCurrentWidget(self.ui) #set the stacked widget to the given ui.

		self.point = QtCore.QPoint(self.sb.getUiSize(percentWidth=50), self.sb.getUiSize(percentHeight=50)) #set point to the middle of the layout
		self.moveToMousePosition(self, -self.point.x(), -self.point.y()) #set initial positon on showEvent, and reposition here on index change.
		self.resize(self.sb.getUiSize(width=1), self.sb.getUiSize(height=1)) #get ui size for current ui and resize window


		if not self.sb.hasKey(self.name, 'connectionDict'): #build the connectionDict containing the widgets and their connections.
			self.childEvents.init(self.name)


		if not any([self.name=='init', self.name==self.sb.previousName(allowDuplicates=1)]):
			if self.sb.previousName(): #if previous ui signals exist:
				self.sb.removeSignal(self.sb.previousName()) #remove signals from the previous ui.
			self.sb.addSignal(self.name)



	# ------------------------------------------------
	# Event overrides
	# ------------------------------------------------
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
		if any([self.name=='init', self.name=='main', self.name=='viewport', self.name=='editors']):
			if event.button()==QtCore.Qt.LeftButton:
				self.setWidget('viewport')

			elif event.button()==QtCore.Qt.MiddleButton:
				self.setWidget('editors')

			elif event.button()==QtCore.Qt.RightButton:
				self.setWidget('main')



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if any([self.name=='main', self.name=='viewport', self.name=='editors']):
			self.childEvents.mouseTracking(self.name)



	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if any([self.name=='main', self.name=='viewport', self.name=='editors']):
			if any([event.button()==QtCore.Qt.LeftButton,event.button()==QtCore.Qt.MiddleButton,event.button()==QtCore.Qt.RightButton]):
				self.setWidget('init')



	def mouseDoubleClickEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if event.button()==QtCore.Qt.RightButton:
			if any([self.name=='init', self.name=='main']):
				try: #show last used submenu on double mouseclick
					self.setWidget(self.sb.previousName(previousIndex=True))
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
		Prevents hide event under certain circumstances.
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

		self.setWidget('init') #reset layout back to init on keyPressEvent



	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		try: MaxPlus.CUI.DisableAccelerators()
		except: pass

		self.moveToMousePosition(self, -self.point.x(), -self.point.y()) #move window to cursor position and offset from left corner to center
		self.activateWindow()



	def moveToMousePosition(self, window, xOffset=None, yOffset=None):
		'''
		Move window from it's current position to the mouse position.
		args:
			window=widget
			xOffset=int - optional x coordinate offset amount
			yOffset=int - optional y coordinate offset amount
		'''
		mousePosition = QtGui.QCursor.pos()
		x = mousePosition.x()+xOffset
		y = mousePosition.y()+yOffset
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
# Initialize
# ------------------------------------------------
def createInstance():
	try: mainWindow = [x for x in app.topLevelWidgets() if x.objectName()=='MayaWindow'][0]
	except:
		try: mainWindow = MaxPlus.GetQMaxMainWindow(); mainWindow.setObjectName('MaxWindow')
		except: mainWindow = None

	hotBox = HotBox(mainWindow)
	hotBox.setWidget('init') #initialize layout
	hotBox.overlay = OverlayFactoryFilter(hotBox)

	return hotBox



if __name__ == "__main__":
	createInstance().show()
	sys.exit(qApp.exec_())










#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

		# if any([self.name=='main', self.name=='viewport', self.name=='editors']):
		# 	drag = QtGui.QDrag(self)
		# 	drag.setMimeData(QtCore.QMimeData())
		# 	# drag.setHotSpot(event.pos())
		# 	# drag.setDragCursor(QtGui.QCursor(QtCore.Qt.CrossCursor).pixmap(), QtCore.Qt.MoveAction) #QtCore.Qt.CursorShape(2) #QtCore.Qt.DropAction
		# 	drag.start(QtCore.Qt.MoveAction) #drag.exec_(QtCore.Qt.MoveAction)
		# 	print drag.target() #the widget where the drag object was dropped.