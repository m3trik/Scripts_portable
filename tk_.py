from __future__ import print_function
from PySide2 import QtCore, QtGui, QtWidgets

import sys, os.path

from tk_switchboard import Switchboard
from tk_overlay import OverlayFactoryFilter
from tk_childEvents import EventFactoryFilter
from widgets.qPushButton_ import QPushButton_



# ------------------------------------------------
# 	Construct the Widget Stack
# ------------------------------------------------
class Tk(QtWidgets.QStackedWidget):
	'''
	Marking menu-style window based on a stacked widget.
	Gets and sets signal connections (through the switchboard module).
	Initializes events for child widgets using the childEvents module.
	Plots points for paint events in the overlay module.

	The various ui's are set by calling 'setUi' with the intended ui name string. ex. Tk().setUi('polygons')

	args:
		parent (obj) = the main application's top level window.
	'''
	def __init__(self, parent=None):
		super(Tk, self).__init__(parent)

		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setAttribute(QtCore.Qt.WA_SetStyle) #Indicates that the widget has a style of its own.

		self.key_show = QtCore.Qt.Key_F12
		self.preventHide = False

		self.sb = Switchboard(self)
		self.sb.setMainAppWindow(self.parent())
		self.sb.setClassInstance(self, 'tk')

		self.childEvents = EventFactoryFilter(self)
		self.overlay = OverlayFactoryFilter(self) #Paint events are handled by the overlay module.


	def setUi(self, name='init'):
		'''
		Set the stacked Widget's index.

		args:
			name (str) = name of ui.
		'''
		ui = self.sb.getUi(name, setAsCurrent=True) #Get the ui of the given name, and set it as the current ui.

		if not name in self.sb.previousName(allowLevel0=1, as_list=1): #if ui(name) hasn't been set before, init the ui for the given name.
		# self.sb.setUiSize(name) #Set the size info for each ui (allows for resizing a stacked widget where ordinarily resizing is constrained by the largest widget in the stack)
			self.addWidget(ui) #add each ui to the stackedLayout.
			self.childEvents.initWidget(name)

		self.sb.setSignals(name)#self.sb.setSignals = name #connect new signals while disconnecting any previous.

		self.resize(self.sb.sizeX, self.sb.sizeY)  #Set the size info for each ui (allows for resizing a stacked widget where ordinarily resizing is constrained by the largest widget in the stack)
		# if self.sb.uiLevel<3:
		# 	self.showFullScreen()
		# print('keyboardGrabber:', self.keyboardGrabber())

		self.setCurrentWidget(self.sb.ui) #set the stacked widget to the given ui.
		return ui


	def setPrevUi(self):
		'''
		Return the stacked widget to it's starting index.
		'''
		previous = self.sb.previousName(allowLevel2=False)
		self.setUi(previous) #return the stacked widget to it's previous ui.

		#Reset the lists that make up the draw and widget paths.
		del self.drawPath[1:] #clear the draw path, while leaving the starting point.
		del self.widgetPath[:] #clear the list of previous widgets.

		self.move(self.drawPath[0] - self.rect().center())



	def setSubUi(self, widget, name):
		'''
		Set the stacked widgets index to the submenu associated with the given widget.
		Moves the new ui to line up with the previous ui's children.
		Re-constructs the relevant buttons from the previous ui for the new ui, and positions them.
		Initializes the new buttons to receive events through the childEvents filter.

		args:
			widget (QWidget) = the widget that called this method.
			name (str) = name of ui.
		'''
		p1 = widget.mapToGlobal(widget.rect().center()) #widget position before submenu change.

		try: #open a submenu on mouse enter (if it exists).
			self.setUi(name) #switch the stacked widget to the given submenu.
		except ValueError: #if no submenu exists: ignore and return.
			return None

		w = getattr(self.currentWidget(), widget.objectName()) #get the widget of the same name in the new ui.
		#maintain the correct contents of the widgetPath and drawPath lists by removing elements when moving back up levels in the ui.
		if len(self.sb.previousName(as_list=1, allowDuplicates=1))>2:
			if name in self.sb.previousName(as_list=1, allowDuplicates=1)[:-1]: #if index is that of the previous ui, remove the information associated with that ui from the list.
				widgets = [i[2] for i in self.widgetPath] #get the names associated with the widgets in widgetPath. ie. 'edit_submenu'
				if name in widgets:
					i = widgets[::-1].index(name) #reverse the list and get the index of the last occurrence of name.
					del self.drawPath[-i-1:]
					del self.widgetPath[-2:]

		self.widgetPath.append([widget, p1, name]) #add the widget (and its position) from the old ui to the widgetPath list so that it can be re-created in the new ui (in the same position).
		self.drawPath.append(QtGui.QCursor.pos()) #add the global cursor position to the drawPath list so that paint events can draw the path tangents.

		p2 = w.mapToGlobal(w.rect().center()) #widget position after submenu change.
		currentPos = self.mapToGlobal(self.pos())
		self.move(self.mapFromGlobal(currentPos +(p1 - p2))) #currentPos + difference


		#recreate any relevant buttons from the previous ui on first show.
		if name not in self.sb.previousName(as_list=1, allowDuplicates=1)[:-1]: #if submenu ui called for the first time, construct widgets from the previous ui that fall along the plotted path.
			w0 = QPushButton_(parent=self.sb.getUi(name), setObjectName='return_', resize=QtCore.QSize(45, 45), globalPos=self.drawPath[0]) #create an invisible return button at the start point.
			self.childEvents.addWidgets(name, w0) #initialize the widget to set things like the event filter and styleSheet.

			if self.sb.getUiLevel(self.sb.previousName())==2: #if submenu: recreate widget/s from the previous ui that are in the current path.
				for i in range(2, len(self.widgetPath)+1): #index starting at 2:
					prevWidget = self.widgetPath[-i][0] #give index neg value.
					w1 = QPushButton_(parent=self.sb.getUi(name), copy=prevWidget, globalPos=self.widgetPath[-i][1], setVisible=True)
					self.childEvents.addWidgets(name, w1) #initialize the widget to set things like the event filter and styleSheet.
					# QtWidgets.QApplication.sendEvent(w1, self.childEvents.enterEvent_)
					self.childEvents._mouseOver.append(w1)
					w1.grabMouse() #set widget to receive mouse events.
					self.childEvents._mouseGrabber = w1


	# ------------------------------------------------
	# 	Event overrides
	# ------------------------------------------------
	def keyPressEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if event.key()==self.key_show and not event.isAutoRepeat():
			pass

		return QtWidgets.QStackedWidget.keyPressEvent(self, event)



	def keyReleaseEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if event.key()==self.key_show and not event.isAutoRepeat():
			self.hide()

		return QtWidgets.QStackedWidget.keyReleaseEvent(self, event)



	def mousePressEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.sb.uiLevel<3:
			self.move(QtGui.QCursor.pos() - self.rect().center()) #move window to cursor position and offset from left corner to center

			self.widgetPath=[] #maintain a list of widgets and their location, as a path is plotted along the ui hierarchy. ie. [[<QPushButton object1>, QPoint(665, 396)], [<QPushButton object2>, QPoint(585, 356)]]
			self.drawPath=[] #initiate the drawPath list that will contain points as the user moves along a hierarchical path.
			self.drawPath.append(self.mapToGlobal(self.rect().center()))

			if event.button()==QtCore.Qt.LeftButton:
				self.setUi('cameras')

			elif event.button()==QtCore.Qt.MiddleButton:
				self.setUi('editors')

			elif event.button()==QtCore.Qt.RightButton:
				self.setUi('main')

		return QtWidgets.QStackedWidget.mousePressEvent(self, event)



	def mouseMoveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.sb.uiLevel<3:
			self.childEvents.mouseTracking(self.sb.name)

		return QtWidgets.QStackedWidget.mouseMoveEvent(self, event)



	def mouseReleaseEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.sb.uiLevel>0 and self.sb.uiLevel<3:
			self.setUi('init')

		return QtWidgets.QStackedWidget.mouseReleaseEvent(self, event)



	def mouseDoubleClickEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if event.button()==QtCore.Qt.RightButton:
			self.repeatLastCameraView()

		elif event.button()==QtCore.Qt.LeftButton:
			self.repeatLastCommand()

		elif event.button()==QtCore.Qt.MiddleButton:
			self.repeatLastUi()

		return QtWidgets.QStackedWidget.mouseDoubleClickEvent(self, event)



	def hide(self, force=False):
		'''
		Prevents hide event under certain circumstances.

		args:
			force (bool) = override preventHide.
		'''
		if force or not self.preventHide:
			self.setUi('init')
			super(Tk, self).hide()



	def hideEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if __name__ == "__main__":
			sys.exit() #assure that the sys processes are terminated.

		return QtWidgets.QStackedWidget.hideEvent(self, event)



	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self.sb.gcProtect(clear=True) #clear any garbage protected items.

		self.setUi('init')
		#run once on launch. update the info textEdit.
		method = self.sb.getMethod(self.sb.name, 'info')
		if callable(method):
			self.sb.ui.info.insertText(method())

		self.move(QtGui.QCursor.pos() - self.rect().center()) #move window to cursor position and offset from left corner to center
		# self.sb.ui.staticWindow.move(self.sb.ui.staticWindow.pos()+QtGui.QCursor.pos())
		self.activateWindow()

		return QtWidgets.QStackedWidget.showEvent(self, event)



	def repeatLastCommand(self):
		'''
		Repeat the last stored command.
		'''
		method = self.sb.prevCommand()
		if callable(method):
			name = self.sb.getNameFromMethod(method)
			self.setUi(name)
			# print (self.sb.getUiName(), name, method)
			method()
		else:
			print(" Warning: No recent commands in history. ")



	def repeatLastCameraView(self):
		'''
		Show the previous camera view.
		'''
		camera = self.sb.prevCamera()
		if callable(camera):
			camera()

			cam = self.sb.prevCamera(allowCurrent=True, as_list=1)[-2]
			self.sb.prevCamera(allowCurrent=True, as_list=1).append(cam) #store the camera view
		else:
			print(" Warning: No recent camera views in history. ")



	def repeatLastUi(self):
		'''
		Open the last used level 3 menu.
		'''
		previousName = self.sb.previousName(allowLevel1=False, allowLevel2=False)
		if previousName:
			self.setUi(previousName)
			self.move(self.drawPath[0] - self.rect().center())
		else:
			print(" Warning: No recent menus in history. ")




			




if __name__ == '__main__':
	app = QtWidgets.QApplication.instance() #get the qApp instance if it exists.
	if not app:
		app = QtWidgets.QApplication(sys.argv)

	Tk().show()
	sys.exit(app.exec_())






#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

		# if any([self.sb.name=='main', self.sb.name=='cameras', self.sb.name=='editors']):
		# 	drag = QtGui.QDrag(self)
		# 	drag.setMimeData(QtCore.QMimeData())
		# 	# drag.setHotSpot(event.pos())
		# 	# drag.setDragCursor(QtGui.QCursor(QtCore.Qt.CrossCursor).pixmap(), QtCore.Qt.MoveAction) #QtCore.Qt.CursorShape(2) #QtCore.Qt.DropAction
		# 	drag.start(QtCore.Qt.MoveAction) #drag.exec_(QtCore.Qt.MoveAction)
		# 	print(drag.target() #the widget where the drag object was dropped.)

# @property
# 	def sb(self):
# 		if not hasattr(self, '_sb'):
# 			self._sb = Switchboard()
# 			self._sb.setMainAppWindow(self.parent)
# 			self._sb.setClassInstance(self, 'tk')
# 		return self._sb

# 	@property
# 	def childEvents(self):
# 		if not hasattr(self, '_childEvents'):
# 			self._childEvents = EventFactoryFilter(self)
# 		return self._childEvents

# 	@property
# 	def overlay(self):
# 		if not hasattr(self, '_overlay'):
# 			self._overlay = OverlayFactoryFilter(self) #Paint events are handled by the overlay module.
# 		return self._overlay