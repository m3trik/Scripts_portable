# |||||||||||||||||||||||||||||||||||||||||||||||||
# ||||||   	 	tookit marking menu			|||||||
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
	Initializes events for child widgets in the childEvents module.
	Plots points for paint events in the overlay module.
	The various ui's are set by calling 'setUi' with the intended ui name string. ex. Tk().setUi('polygons')
	args:
		parent = main application window object.
	'''
	def __init__(self, parent=None):
		super(Tk, self).__init__(parent)

		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		self.sb = Switchboard(parent)
		self.sb.setClassInstance(self) #store this class instance.

		self.childEvents = EventFactoryFilter()

		self.setUi('init') #initialize layout
		self.prevWidget=[]



	def setUi(self, name):
		'''
		Set the stacked Widget's index.
		args:
			name = 'string' - name of ui.
		returns:
			'string' - name of ui. ex. 'polygons'
		'''
		if not name in self.sb.previousName(allowInit=1, as_list=1): #if ui(name) hasn't been set before, init the ui for the given name.
			self.sb.setUiSize(name) #Set the size info for each ui (allows for resizing a stacked widget where ordinarily resizing is constrained by the largest widget in the stack)
			self.addWidget(self.sb.getUi(name)) #add each ui to the stackedLayout.
			self.childEvents.init(name)

		self.name = self.sb.setUiName(name) #set ui name.
		self.ui = self.sb.getUi(name) #get the dymanic ui of the given name.
		self.uiLevel = self.sb.getUiLevel(name) #get the hierarchical level of the ui.

		self.sb.setSignals(name) #connect new signals while disconnecting any previous.

		self.resize(self.sb.getUiSize(width=1), self.sb.getUiSize(height=1)) #get ui size for current ui and resize window

		self.setCurrentWidget(self.ui) #set the stacked widget to the given ui.

		return self.name #return name. useful in cases where switching ui in the middle of an event the name can be immediately updated. ie. self.name = self.tk.setUi('main')



	def setPrevUi(self):
		'''
		Return the stacked widget to it's previous ui.
		'''
		previous = [i for i in self.sb.previousName(as_list=1) if '_submenu' not in i][-1]
		name = self.setUi(previous) #return the stacked widget to it's previous ui.
		del self.drawPath[1:] #clear the draw path, while leaving the starting point.
		del self.prevWidget[:] #clear the list of previous widgets.
		self.move(self.drawPath[0] - self.rect().center())
		return name



	def setSubUi(self, widget, submenu):
		'''
		Uses the meta info of the given widget to switch the ui to the associated submenu.
		Moves the new ui to line up with the previous ui's children.
		Re-constructs the relevant buttons from the previous ui for the new ui, and positions them.
		Initializes the new buttons to recieve events through the childEvents filter.
		args:
			widget = <QWidget> - the widget that called this method.
			submenu = 'string' - name of ui.
		returns:
			'string' - name of ui. ex. 'polygons_submenu'
		'''
		p1 = widget.mapToGlobal(widget.rect().center()) #widget position before submenu change.

		# w = widget #store widget before changing the stacked widget ui.
		
		# try: #open a submenu on mouse enter (if it exists).
		name = self.setUi(submenu) #switch the stacked widget to the given submenu.
		# except Exception as error:
		# 	if not type(error)==ValueError: #if no submenu exists: ignore.
		# 		raise error
		# 		return None

		w = getattr(self.currentWidget(), widget.objectName()) #get the widget of the same name in the new ui.
		#maintain the correct contents of the prevWidget and drawPath lists by removing elements when moving back up levels in the ui.
		if len(self.sb.previousName(as_list=1, allowDuplicates=1))>2:
			if name==self.sb.previousName(as_list=1, allowDuplicates=1)[-3]: #if index is that of the previous ui, remove the information associated with that ui from the lists so that any new list will draw with the correct contents.
				del self.prevWidget[-2:]
				if len(self.drawPath)>2: #temp solution for removing drawPath points. works only when there are two levels of submenus to draw paths for.
					del self.drawPath[-2:]

		self.prevWidget.append([widget, p1]) #add the widget that was initially entered to the prevWidget list so that it can be re-created in the new ui (in the same position).
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
				for index in range(2, len(self.prevWidget)+1): #index starting at 2:
					prevWidget = self.prevWidget[-index][0] #give index neg value.
					prevWidgetLocation = self.prevWidget[-index][1]

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
			print 'keyPressEvent', self.name
			if self.name=='init': #self.uiLevel==0:
				textEdit = self.sb.getUi('init').info
				info = self.sb.getMethod('init', 'info')
				print info
				if callable(info):
					infoDict = info()

					#populate the textedit with any values
					for key, value in infoDict.items():
						if value:
							highlight = QtGui.QColor(255, 255, 0)
							baseColor = QtGui.QColor(185, 185, 185)

							textEdit.setTextColor(baseColor)
							textEdit.append(key) #textEdit.append(key+str(value))
							textEdit.setTextColor(highlight)
							textEdit.insertPlainText(str(value))



	def keyReleaseEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat():
			#clear the info textEdit on hide.
			textEdit = self.sb.getUi('init').info
			textEdit.clear()

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
		if self.uiLevel>0 and self.uiLevel<3:
			self.childEvents.mouseTracking(self.name)



	def mouseReleaseEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.uiLevel>0 and self.uiLevel<2:
			if any([event.button()==QtCore.Qt.LeftButton,event.button()==QtCore.Qt.MiddleButton,event.button()==QtCore.Qt.RightButton]):
				self.setUi('init')



	def mouseDoubleClickEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if event.button()==QtCore.Qt.RightButton:
			if any([self.name=='init', self.name=='main']):
				try: #show last used submenu on double mouseclick
					self.setUi(self.sb.previousName(previousIndex=True))
				except:
					print "# Warning: No recent submenus in history. #"

		elif event.button()==QtCore.Qt.LeftButton:
			if any([self.name=='init', self.name=='viewport']):
				try: #show last view
					self.repeatLastView()
				except: 
					print "# Warning: No recent views in history. #"

		elif event.button()==QtCore.Qt.MiddleButton:
			if any([self.name=='init', self.name=='editors']):
				try: #repeat last command
					self.repeatLastCommand()
				except:
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
			event = <QEvent>
		'''
		try: import MaxPlus; MaxPlus.CUI.EnableAccelerators()
		except: pass

		self.setUi('init') #reset layout back to init on keyPressEvent

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
		print self.sb.prevCommand()
		self.sb.prevCommand()()
		print self.sb.prevCommand(docString=1) #print command name string
		


	def repeatLastView(self):
		'''
		Show the previous view.
		'''
		print self.sb.previousView()
		self.sb.previousView()()
		print self.sb.previousView(asList=1)






# ------------------------------------------------
# 	Initialize
# ------------------------------------------------
def createInstance(mainWindow=None):
	tk = Tk(mainWindow)
	tk.overlay = OverlayFactoryFilter(tk) #Paint events are handled by the overlay module.

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