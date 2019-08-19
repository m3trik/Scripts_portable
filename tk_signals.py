from PySide2 import QtCore, QtWidgets

import os.path

from tk_switchboard import Switchboard
import tk_styleSheet as styleSheet



# ------------------------------------------------
#	Manage signal connections
# ------------------------------------------------
class Signal(QtCore.QObject):

	mouseHover = QtCore.Signal(bool)
	
	def __init__(self):
		QtCore.QObject.__init__(self)


		self.sb = Switchboard()
		self.hotBox = self.sb.getClass('hotBox')
		self.app = self.sb.getApp()




	def buildConnectionDict(self, name=None):
		'''
		args:
			name='string' - name of the ui to construct connections for.
		returns:
			dict - 'buttonName':{'buttonObject':<buttonObject>,'buttonObjectWithSignal':<buttonObjectWithSignal>,'methodObject':<method>,'docString':'docString','widgetClass':<class object>,'widgetClassName':'class name'}
		'''
		if not name: #build connections for the given current ui name
			name = self.sb.getUiName()

		ui = self.sb.getUi(name)
		class_ = self.sb.setClass_tk_slots(name)()


		signalType = {
			'QPushButton':'clicked',
			'QSpinBox':'valueChanged',
			'QDoubleSpinBox':'valueChanged',
			'QCheckBox':'released',
			'QComboBox':'currentIndexChanged',
			'QLineEdit':'returnPressed'}

		for buttonName, buttonObject in ui.__dict__.iteritems(): #for each object in the ui:
			for buttonType, signal in signalType.iteritems():
				if buttonObject.__class__.__name__==buttonType: #if it is a type listed in the signalType dict, construct with the associated signal.

					buttonObjectWithSignal = getattr(buttonObject, signal) #add signal to buttonObject

					m = getattr(class_, buttonName, None) #use signal 'buttonName' (ie. b006) to get method/slot of the same name in current class.
					docString = getattr(m, '__doc__', None)
					method = list(filter(None, [m, lambda b=buttonName: self.onSignalEvent(b)])) #add onSignalEvent. passing multiple slots as list. filter any None values out.

					#add values to connectionDict
					self.sb.connectionDict(name).update(
						{buttonName:{
							'buttonObject':buttonObject, 
							'buttonObjectWithSignal':buttonObjectWithSignal, 
							'methodObject':method,
							'docString':docString,
							'buttonType':buttonType,
							'widgetClass':buttonObject.__class__}})

					
					buttonObject.setStyleSheet(styleSheet.css) #add stylesheet
					buttonObject.installEventFilter(self) #add eventfilter

		return self.sb.connectionDict(name)



	def addSignal(self, name):
		'''
		Connect signals/slots for the given ui.
		args:
			name='string' - name of ui
		'''
		for buttonName in self.sb.connectionDict(name):
			signal = self.sb.getSignal(buttonName, name)
			slot = self.sb.getSlot(buttonName, name)
			# print 'addSignal: ', signal, slot
			try: map(signal.connect, slot) #add multiple slots from list.
			except:
				try: signal.connect(slot) #add single slot (main and viewport)
				except Exception as error: print '# Error: '+buttonName+str(type(slot))+str(slot)+' #' #, error



	def removeSignal(self, name):
		'''
		Disconnect signals/slots for the given ui.
		args:
			name='string' - name of ui
		'''
		for buttonName in self.sb.connectionDict(name):
			signal = self.sb.getSignal(buttonName, name)
			slot = self.sb.getSlot(buttonName, name)
			# print 'removeSignal: ', signal, slot
			try: map(signal.disconnect, slot) #add multiple slots from list.
			except: 
				try: signal.disconnect(slot) #add single slot (main and viewport)
				except Exception as error: print '# Error: '+buttonName+str(type(slot))+str(slot)+' #' #, error



	def eventFilter(self, button, event):
		'''
		Event filter for dynamic ui objects.
		args:
			button=filtered object
			event=QEvent
		'''
		buttonName = button.objectName()
		buttonType = self.sb.getWidgetType(button)

		
		#Override pushbutton to move the main window on left mouse drag event.
		#When checked, prevents hide event on main window.
		if buttonName=='pin':
			if event.type()==QtCore.QEvent.MouseButtonPress:
				self.__mousePressPos = event.globalPos()
				return True

			if event.type()==QtCore.QEvent.MouseMove:
				self.hotBox.moveToMousePosition(self.hotBox, -self.hotBox.point.x(), -self.hotBox.point.y()*.1) #move window on left mouse drag.
				return True

			if event.type()==QtCore.QEvent.MouseButtonRelease:
				moveAmount = event.globalPos() - self.__mousePressPos
				if moveAmount.manhattanLength() > 5: #if button moved:
					button.setChecked(True) #setChecked to prevent window from closing.
					event.ignore()
				else:
					button.setChecked(not button.isChecked()) #toggle check state
					self.hotBox.hide_()
				return True


		if event.type()==QtCore.QEvent.Type.Enter: #hover enter event
			self.mouseHover.emit(True)
			if buttonType=='QComboBox':
				#switch the index before opening to initialize the contents of the combobox
				index = button.currentIndex()
				button.blockSignals(True); button.setCurrentIndex(-1); button.blockSignals(False)
				button.setCurrentIndex(index) #change index back to refresh contents
				button.setStyleSheet('''
					QComboBox {
					background-color: rgba(82,133,166,200);
					color: white;
					}''')
				
			if self.hotBox.name=='main' or self.hotBox.name=='viewport': #layoutStack index and viewport signals
				# print button.__class__.__name__
				if buttonType=='QComboBox':
					button.showPopup()
				else:
					button.click()


		if event.type()==QtCore.QEvent.Type.HoverLeave: #hover leave event
			self.mouseHover.emit(False)
			if buttonType=='QComboBox':
				button.setStyleSheet('''
					background-color: rgba(100,100,100,200);
					color: white;
					}''')

		return QtWidgets.QWidget.eventFilter(self, button, event)



	def onSignalEvent(self, buttonName):
		'''
		Called on any ui widget when it's signal is triggered.
		args:
			buttonName='string' - objectName of button
		'''
		buttonObject = self.sb.getWidget(buttonName)

		if buttonName.startswith('i'): #connect to layoutStack and pass in an index as int or string 'name'.
			index = buttonObject.whatsThis() #buttonObject.text()
			self.hotBox.layoutStack(index) #switch the stacked layout to the given ui.

		if buttonName.startswith('b'): #ie. 'b012'
			self.sb.prevCommand(as_list=1).append([self.sb.getMethod(buttonName), self.sb.getDocString(buttonName)]) #store the command method object and it's docString (ie. 'Multi-cut tool')

		if buttonName.startswith('v'): #ie. 'v012'
			self.sb.previousView(as_list=1).append(self.sb.getMethod(buttonName)) #store the camera view










#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

	# def onSignalEvent(self, method):
	# 	#args: [method object]
	# 	#add method and docString to prevCommand list
	# 	if callable(method) and method.__name__.startswith('b'): #ie. 'b012'
	# 		try:
	# 			docString = self.sb.getDocString(method.__name__, name) #get the 'docString'. ie. 'Multi-Cut Tool'
	# 			# print docString, method.__name__, self.sb.prevCommand(as_list=1)
	# 			self.sb.prevCommand(as_list=1).append([method, docString]) #build array that stores the command method object and the corresponding docString (ie. 'Multi-cut tool')
	# 		except Exception as error:
	# 			print 'tk_signals: onSignalEvent:', error
	# 	#add previousView to list
	# 	if callable(method) and method.__name__.startswith('v'): #ie. 'v012'
	# 		self.sb.previousView(as_list=1).append(method)