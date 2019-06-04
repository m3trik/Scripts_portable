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
		self.hotBox = self.sb.getClass('hotbox')
		self.app = self.sb.getApp()
		



	def buildConnectionDict(self, name=None):

		if name: #build connections for the specified name
			self.name = name
		else: #get current name
			self.name = self.sb.getUiName()
		self.ui = self.sb.getUi(self.name)

		class_ = self.sb.setClass('tk_slots_'+self.app+'_'+self.name+'.'+self.name.capitalize())() #append class object to switchboardDict



		buttonType = {'i':'clicked','b':'clicked','v':'clicked','s':'valueChanged','chk':'released','cmb':'currentIndexChanged','t':'returnPressed'}

		for prefix,signal in buttonType.iteritems(): #button/method's that start with ie. 'b'
			size = 200
			for num in xrange(size):
				numString = '000'[:-len(str(num))]+str(num) #remove zeros from the prefix string corresponding to the length of num
				buttonString = prefix+numString
				# docString = ''
				# if hasattr(self.ui, buttonString):
				try: 
					#get the button from the dynamic ui
					buttonObject = getattr(self.ui, buttonString)  #equivilent to: self.ui.b000
					size-=1 #decrease search length on each successful match
					
					#add stylesheet
					buttonObject.setStyleSheet(styleSheet.css)

					#add eventfilter
					buttonObject.installEventFilter(self) #ie. self.ui.i000.installEventFilter(self)

					#add signal to buttonObject
					buttonObjectWithSignal = getattr(buttonObject, signal)

					#set the corresponding method
					if prefix=='i': #connect to layoutStack and pass in an index as int or string name.
						index = buttonObject.whatsThis().lower() #buttonObject.text().lower()
						method = lambda i=index: self.hotBox.layoutStack(i) #lambda function to call index. ie. hotBox.layoutStack(6) or hotBox.layoutStack('polygons')
					else:
						m = getattr(class_, buttonString) #use signal 'buttonString' (ie. b006) to get method/slot of the same name in current class.
						method = [m, lambda method=m: self.onPressedEvent(method)] #add onPressedEvent. pass multiple slots as list.
					
					#add docString info
					try:
						docString = m.__doc__
					except:
						docString = None

					#add values to connectionDict
					self.sb.connectionDict(self.name).update(
						{buttonString:{
							'buttonObject':buttonObject, 
							'buttonObjectWithSignal':buttonObjectWithSignal, 
							'methodObject':method, 
							'docString':docString,
							'widgetClass':buttonObject.__class__,
							'widgetClassName':buttonObject.__class__.__name__,
							}})

				except Exception as error:
					if error==AttributeError:
						print 'Exception:',error
		# print self.sb.connectionDict(self.name)
		return self.sb.connectionDict(self.name)



	def addSignal(self, name):
		#args: [string]
		for buttonString in self.sb.connectionDict(name):
			signal = self.sb.getSignal(name, buttonString)
			slot = self.sb.getSlot(name, buttonString)
			# print 'addSignal: ', signal, slot
			try: map(signal.connect, slot) #add multiple slots
			except:
				try: signal.connect(slot) #add single slot (main and viewport)
				except Exception as error: print '# Error: '+str(type(slot))+str(slot)+' #' #, error



	def removeSignal(self, name):
		#args: [string]
		for buttonString in self.sb.connectionDict(name):
			signal = self.sb.getSignal(name, buttonString)
			slot = self.sb.getSlot(name, buttonString)
			# print 'removeSignal: ', signal, slot
			try: map(signal.disconnect, slot) #add multiple slots
			except: 
				try: signal.disconnect(slot) #add single slot (main and viewport)
				except Exception as error: print '# Error: '+str(type(slot))+str(slot)+' #' #, error



	def eventFilter(self, button, event):
		#args:	[source object]
		#		[QEvent]
		if event.type()==QtCore.QEvent.Type.Enter: #enter event
			self.mouseHover.emit(True)
			if self.sb.getWidgetType(button)=='QComboBox':
				#switch the index before opening to initialize the contents of the combobox
				index = button.currentIndex()
				button.blockSignals(True); button.setCurrentIndex(99); button.blockSignals(False)
				button.setCurrentIndex(index) #change index back to refresh contents
				
			if self.hotBox.name=='main' or self.hotBox.name=='viewport': #layoutStack index and viewport signals
				# print button.__class__.__name__
				if self.sb.getWidgetType(button)=='QComboBox':
					button.showPopup()
				else:
					button.click()

		if event.type()==QtCore.QEvent.Type.HoverLeave:
			self.mouseHover.emit(False)

		return QtWidgets.QWidget.eventFilter(self, button, event)



	def onPressedEvent(self, method):
		#args: [method object]
		#add method and docstring to prevCommand list
		if type(method)!=int and method.__name__.startswith('b'): #ie. 'b012'
			try:
				docString = self.sb.getDocString(self.name, method.__name__) #get the 'docString'. ie. 'Multi-Cut Tool'
				# print docString, method.__name__, self.sb.prevCommand(as_list=1)
				self.sb.prevCommand(as_list=1).append([method, docString]) #build array that stores the command method object and the corresponding docString (ie. 'Multi-cut tool')
			except Exception as error:
				print 'tk_signals:147:', error
		#add previous view to preView list
		if type(method)!=int and method.__name__.startswith('v'): #ie. 'v012'
			self.sb.previousView(as_list=1).append(method)








#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

