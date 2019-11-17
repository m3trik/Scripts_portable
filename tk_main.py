# ||||||||||||||||||||||||||||||||||||||||||||||||
# |||||			tookit marking menu			||||||

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

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		self.sb = Switchboard(self, parent)

		self.childEvents = EventFactoryFilter(self)

		self.widgetPath=[] #maintain a list of widgets and their location, as a path is plotted along the ui hierarchy. ie. [[<QPushButton object1>, QPoint(665, 396)], [<QPushButton object2>, QPoint(585, 356)]]



	def setUi(self, name='init'):
		'''
		Set the stacked Widget's index.
		args:
			name = 'string' - name of ui.
		'''
		if not name in self.sb.previousName(allowInit=1, as_list=1): #if ui(name) hasn't been set before, init the ui for the given name.
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
		Return the stacked widget to it's previous ui.
		'''
		previous = [i for i in self.sb.previousName(as_list=1) if '_submenu' not in i][-1]
		self.setUi(previous) #return the stacked widget to it's previous ui.

		del self.drawPath[1:] #clear the draw path, while leaving the starting point.
		del self.widgetPath[:] #clear the list of previous widgets.

		self.move(self.drawPath[0] - self.rect().center())



	def setSubUi(self, widget, name):
		'''
		Uses the meta info of the given widget to switch the ui to the associated submenu.
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
			if not type(error)==ValueError: #if no submenu exists: ignore.
				raise error
				return None

		w = getattr(self.currentWidget(), widget.objectName()) #get the widget of the same name in the new ui.
		#maintain the correct contents of the widgetPath and drawPath lists by removing elements when moving back up levels in the ui.
		if len(self.sb.previousName(as_list=1, allowDuplicates=1))>2:
			if name==self.sb.previousName(as_list=1, allowDuplicates=1)[-3]: #if index is that of the previous ui, remove the information associated with that ui from the lists so that any new list will draw with the correct contents.
				del self.widgetPath[-2:]
				if len(self.drawPath)>2: #temp solution for removing drawPath points. works only when there are two levels of submenus to draw paths for.
					del self.drawPath[-2:]

		self.widgetPath.append([widget, p1]) #add the widget that was initially entered to the widgetPath list so that it can be re-created in the new ui (in the same position).
		self.drawPath.append(QtGui.QCursor.pos()) #add the global cursor position to the drawPath list so that paint events can draw the path tangents.

		p2 = w.mapToGlobal(w.rect().center()) #widget position after submenu change.
		currentPos = self.mapToGlobal(self.pos())
		self.move(self.mapFromGlobal(currentPos +(p1 - p2))) #currentPos + difference


		if name not in self.sb.previousName(as_list=1, allowDuplicates=1)[:-1]: #if submenu ui called for the first time, construct widgets from the previous ui that fall along the plotted path.
			w0 = QtWidgets.QPushButton('<', self.sb.getUi(name))
			w0 = self.sb.addWidget(name, w0, '<')
			self.childEvents.init(name, [w0]) #initialize the widget to set things like the event filter and stylesheet.
			w0.resize(45, 45)
			w0.move(w0.mapFromGlobal(self.drawPath[0] - w0.rect().center())) #move and center
			w0.show()

			if '_submenu' in self.sb.previousName(): #recreate widget/s from the previous ui that are in the current path.
				for index in range(2, len(self.widgetPath)+1): #index starting at 2:
					prevWidget = self.widgetPath[-index][0] #give index neg value.
					prevWidgetLocation = self.widgetPath[-index][1]

					w1 = QtWidgets.QPushButton(prevWidget.text(), self.sb.getUi(name))
					w1 = self.sb.addWidget(name, w1, prevWidget.objectName())
					self.childEvents.init(name, [w1]) #initialize the widget to set things like the event filter and stylesheet.
					w1.setWhatsThis(prevWidget.whatsThis())
					w1.resize(prevWidget.size())
					w1.move(w1.mapFromGlobal(prevWidgetLocation - w1.rect().center())) #move and center
					w1.show()
					index+=1



	# ------------------------------------------------
	# 	Event overrides
	# ------------------------------------------------
	def keyPressEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat():
			#run once on launch. update the info textEdit.
			if self.name=='init': #self.uiLevel==0:
				textEdit = self.sb.getUi('init').info
				info = self.sb.getMethod('init', 'info')
				if callable(info):
					infoDict = info()
					textEdit.addcontents(infoDict)



	def keyReleaseEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat():
			self.hide_()



	def mousePressEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self.move(QtGui.QCursor.pos() - self.rect().center()) #move window to cursor position and offset from left corner to center

		if self.uiLevel<2:
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
		if self.uiLevel>0 and self.uiLevel<2:
			self.setUi('init')



	def mouseDoubleClickEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if event.button()==QtCore.Qt.RightButton:
			if any([self.name=='init', self.name=='main']):
				self.repeatLastCameraView()

		elif event.button()==QtCore.Qt.LeftButton:
			if any([self.name=='init', self.name=='viewport']):
				self.repeatLastUi()

		elif event.button()==QtCore.Qt.MiddleButton:
			if any([self.name=='init', self.name=='editors']):
				self.repeatLastCommand()



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
			event = <QEvent>
		'''
		try: import MaxPlus; MaxPlus.CUI.EnableAccelerators()
		except: pass

		self.setUi('init') #reset layout back to init

		if __name__ == "__main__":
			sys.exit() #assure that the sys processes are terminated.



	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		try: import MaxPlus; MaxPlus.CUI.DisableAccelerators()
		except: pass

		self.move(QtGui.QCursor.pos() - self.rect().center()) #move window to cursor position and offset from left corner to center
		self.activateWindow()



	def repeatLastCommand(self):
		'''
		Repeat the last used command.
		'''
		try:
			print self.sb.prevCommand(), self.sb.prevCommand(docString=1) #print command name string
			self.sb.prevCommand()()
		except:
			print "# Warning: No recent commands in history. #"



	def repeatLastCameraView(self):
		'''
		Show the previous orthographic view.
		'''
		try:
			pass
		except:
			print "# Warning: No recent camera views in history. #"



	def repeatLastUi(self):
		'''
		Open the last used valid menu.
		'''
		try:
			print self.sb.previousUi()
			self.sb.previousUi()()
		except: 
			print "# Warning: No recent menus in history. #"
		






# ------------------------------------------------
# 	Initialize
# ------------------------------------------------
def createInstance(mainWindow=None):
	tk = Tk(mainWindow)
	tk.overlay = OverlayFactoryFilter(tk) #Paint events are handled by the overlay module.
	tk.setUi() #initialize layout

	return tk



if __name__ == "__main__":
	app = QtWidgets.QApplication.instance() #get the qApp instance if it exists.
	if not app:
		app = QtWidgets.QApplication(sys.argv)

	createInstance().show()

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