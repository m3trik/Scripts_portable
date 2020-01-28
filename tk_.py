from PySide2 import QtCore, QtGui, QtWidgets

import sys, os.path

from tk_switchboard import Switchboard
from tk_overlay import OverlayFactoryFilter
from tk_childEvents import EventFactoryFilter






# ------------------------------------------------
# 	Construct the Widget Stack
# ------------------------------------------------
class Tk(QtWidgets.QStackedWidget):
	'''
	Marking menu-style modal window based on a stacked widget.
	Gets and sets signal connections (through the switchboard module).
	Initializes events for child widgets using the childEvents module.
	Plots points for paint events in the overlay module.

	The various ui's are set by calling 'setUi' with the intended ui name string. ex. Tk().setUi('polygons')
	args:
		parent = main application top level window object.
	'''
	def __init__(self, parent=None):
		super(Tk, self).__init__(parent)

		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		self.sb = Switchboard(self, parent)
		self.sb.setClassInstance(self, 'tk')
		self.childEvents = EventFactoryFilter(self)
		self.overlay = OverlayFactoryFilter(self) #Paint events are handled by the overlay module.

		self.key_show = QtCore.Qt.Key_F12
		self.preventHide = False



	def setUi(self, name='init'):
		'''
		Set the stacked Widget's index.
		args:
			name = 'string' - name of ui.
		'''
		if not name in self.sb.previousName(allowLevel0=1, as_list=1): #if ui(name) hasn't been set before, init the ui for the given name.
			self.sb.setUiSize(name) #Set the size info for each ui (allows for resizing a stacked widget where ordinarily resizing is constrained by the largest widget in the stack)
			self.addWidget(self.sb.getUi(name)) #add each ui to the stackedLayout.
			self.childEvents.init(name)

		self.name = self.sb.setUiName(name) #set ui name.
		self.ui = self.sb.getUi(self.name) #get the dymanic ui of the given name.
		self.uiLevel = self.sb.getUiLevel(self.name) #get the hierarchical level of the ui.

		self.sb.setSignals(self.name) #connect new signals while disconnecting any previous.

		self.resize(self.sb.getUiSize(width=1), self.sb.getUiSize(height=1)) #get ui size for current ui and resize window

		self.setCurrentWidget(self.ui) #set the stacked widget to the given ui.



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
			widget = <QWidget> - the widget that called this method.
			name = 'string' - name of ui.
		'''
		p1 = widget.mapToGlobal(widget.rect().center()) #widget position before submenu change.

		try: #open a submenu on mouse enter (if it exists).
			self.setUi(name) #switch the stacked widget to the given submenu.
		except Exception as error:
			if type(error)==ValueError: #if no submenu exists: ignore and return.
				return None
			else:
				raise error

		w = getattr(self.currentWidget(), widget.objectName()) #get the widget of the same name in the new ui.
		#maintain the correct contents of the widgetPath and drawPath lists by removing elements when moving back up levels in the ui.
		if len(self.sb.previousName(as_list=1, allowDuplicates=1))>2:
			if name in self.sb.previousName(as_list=1, allowDuplicates=1)[:-1]: #if index is that of the previous ui, remove the information associated with that ui from the list.
				widgets = [i[2] for i in self.widgetPath] #get the names associated with the widgets in widgetPath. ie. 'edit_submenu'
				if name in widgets:
					index = widgets[::-1].index(name) #reverse the list and get the index of the last occurrence of name.
					del self.drawPath[-index-1:]
					del self.widgetPath[-2:]

		self.widgetPath.append([widget, p1, name]) #add the widget (and its position) from the old ui to the widgetPath list so that it can be re-created in the new ui (in the same position).
		self.drawPath.append(QtGui.QCursor.pos()) #add the global cursor position to the drawPath list so that paint events can draw the path tangents.

		p2 = w.mapToGlobal(w.rect().center()) #widget position after submenu change.
		currentPos = self.mapToGlobal(self.pos())
		self.move(self.mapFromGlobal(currentPos +(p1 - p2))) #currentPos + difference


		#recreate any relevant buttons from the previous ui on first show.
		if name not in self.sb.previousName(as_list=1, allowDuplicates=1)[:-1]: #if submenu ui called for the first time, construct widgets from the previous ui that fall along the plotted path.
			w0 = self.childEvents.createPushButton(name=name, objectName='<', size=[45, 45], location=self.drawPath[0], show=False) #create an invisible return button at the start point.

			if '_submenu' in self.sb.previousName(): #recreate widget/s from the previous ui that are in the current path.
				for index in range(2, len(self.widgetPath)+1): #index starting at 2:
					prevWidget = self.widgetPath[-index][0] #give index neg value.
					w1 = self.childEvents.createPushButton(name=name, objectName=prevWidget.objectName(), size=prevWidget.size(), location=self.widgetPath[-index][1], text=prevWidget.text(), whatsThis=prevWidget.whatsThis())
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



	def keyReleaseEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if event.key()==self.key_show and not event.isAutoRepeat():
			self.hide()



	def mousePressEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.uiLevel<3:
			self.move(QtGui.QCursor.pos() - self.rect().center()) #move window to cursor position and offset from left corner to center

			self.widgetPath=[] #maintain a list of widgets and their location, as a path is plotted along the ui hierarchy. ie. [[<QPushButton object1>, QPoint(665, 396)], [<QPushButton object2>, QPoint(585, 356)]]
			self.drawPath=[] #initiate the drawPath list that will contain points as the user moves along a hierarchical path.
			self.drawPath.append(self.mapToGlobal(self.rect().center()))

			if event.button()==QtCore.Qt.LeftButton:
				self.setUi('viewport')

			elif event.button()==QtCore.Qt.MiddleButton:
				self.setUi('editors')

			elif event.button()==QtCore.Qt.RightButton:
				self.setUi('main')



	def mouseMoveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.uiLevel<3:
			self.childEvents.mouseTracking(self.name)



	def mouseReleaseEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.uiLevel>0 and self.uiLevel<3:
			self.setUi('init')



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



	def hide(self, force=False):
		'''
		Prevents hide event under certain circumstances.

		args:
			force = bool - override preventHide.
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



	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self.setUi('init')
		#run once on launch. update the info textEdit.
		method = self.sb.getMethod(self.name, 'info')
		if callable(method):
			self.ui.info.insertText(method())

		self.move(QtGui.QCursor.pos() - self.rect().center()) #move window to cursor position and offset from left corner to center
		self.activateWindow()



	def repeatLastCommand(self):
		'''
		Repeat the last used command.
		'''
		try:
			self.sb.prevCommand()()
		except:
			print "# Warning: No recent commands in history. #"



	def repeatLastCameraView(self):
		'''
		Show the previous camera view.
		'''
		try:
			self.sb.prevCamera()()
			cam = self.sb.prevCamera(allowCurrent=True, as_list=1)[-2]
			self.sb.prevCamera(allowCurrent=True, as_list=1).append(cam) #store the camera view
		except:
			print "# Warning: No recent camera views in history. #"



	def repeatLastUi(self):
		'''
		Open the last used level 3 menu.
		'''
		previousName = self.sb.previousName(allowLevel1=False, allowLevel2=False)
		if previousName:
			self.setUi(previousName)
			self.move(self.drawPath[0] - self.rect().center())
		else:
			print "# Warning: No recent menus in history. #"









if __name__ == '__main__':
	app = QtWidgets.QApplication.instance() #get the qApp instance if it exists.
	if not app:
		app = QtWidgets.QApplication(sys.argv)

	Tk().show()

	sys.exit(app.exec_())






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