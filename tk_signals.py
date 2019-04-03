from PySide2 import QtCore, QtWidgets

import os.path

from tk_switchboard import Switchboard



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
		



	def buildConnectionDict(self):

		self.name = self.sb.getUiName()
		self.ui = self.sb.getUi()

		class_ = self.sb.setClass('tk_slots_'+self.app+'_'+self.name+'.'+self.name.capitalize())() #append class object to switchboardDict



		buttonType = {'i':'clicked','b':'clicked','v':'clicked','s':'valueChanged','chk':'released','cmb':'currentIndexChanged','t':'returnPressed'}

		for prefix,signal in buttonType.iteritems(): #button/method's that start with ie. 'b'
			size = 200
			for num in xrange(size):
				numString = '000'[:-len(str(num))]+str(num) #remove zeros from the prefix string corresponding to the length of num
				buttonString = prefix+numString
				docString = ''
				# if hasattr(self.ui, buttonString):
				try: #get the button from the dynamic ui
					buttonObject = getattr(self.ui, buttonString)  #equivilent to: self.ui.b000
					size-=1 #decrease search length on each successful match

					#add eventfilter
					buttonObject.installEventFilter(self) #ie. self.ui.i000.installEventFilter(self)

					#add signal to buttonObject
					buttonObjectWithSignal = getattr(buttonObject, signal)

					#set the corresponding method
					if prefix=='i': #connect to layoutStack and pass in an index.
						index = self.sb.getUiIndex(buttonObject.whatsThis().lower())
						method = lambda i=index: self.hotBox.layoutStack(i) #lambda function to call index. ie. hotBox.layoutStack(6)
					else:
						method = getattr(class_, buttonString) #use signal 'buttonString' (ie. b006) to get method/slot of the same name in current class.
						docString = method.__doc__
						if prefix!='v':
							method = [method, lambda m=method: self.onPressedEvent(m)] #add onPressedEvent. pass multiple slots as list.
						#add values to connectionDict
					self.sb.connectionDict(self.name).update({buttonString:{'buttonObject':buttonObject, 'buttonObjectWithSignal':buttonObjectWithSignal, 'methodObject':method, 'docString':docString}})
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
		if self.hotBox.name=='main' or self.hotBox.name=='viewport': #layoutStack index and viewport signals
			if event.type()==QtCore.QEvent.Type.Enter: #enter event
				self.mouseHover.emit(True)
				# print button.__class__.__name__
				if button.__class__.__name__ == 'QComboBox':
					#switch the index before opening to initialize the contents of the combobox
					button.blockSignals(True)#block signals and change from index 0
					button.setCurrentIndex(99)
					button.blockSignals(False)
					button.setCurrentIndex(0) 
					button.showPopup()
				else:
					button.click()

			if event.type()==QtCore.QEvent.Type.HoverLeave:
				self.mouseHover.emit(False)

		return QtWidgets.QWidget.eventFilter(self, button, event)


	def onPressedEvent(self, method):
		#args: [method object]
		if type(method)!=int and method.__name__.startswith('b'): #ie. 'b012'
			docString = self.sb.getDocString(self.name, method.__name__) #get the 'docString'. ie. 'Multi-Cut Tool'
			# print docString, method.__name__, self.sb.prevCommand(as_list=1)
			self.sb.prevCommand(as_list=1).append([method, docString]) #build array that stores the command method object and the corresponding docString (ie. 'Multi-cut tool')






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

# if prefix=='i' or prefix=='v' or prefix=='cmb' and self.name=='main' or  self.name=='viewport': #layoutStack index and viewport signals

# #set the spinboxes for the create menu to connect to the setAttributes method, and pass in the index of the spinbox to set attributes for.
# if prefix=='s' and self.name=='create' and num<=11:
# 	# method = lambda index=num: getattr(class_, 'setAttributes')(index)
# 	pass #moved to class until this is fixed. oddly the above slot calls setAttributes with spinbox value as argument.