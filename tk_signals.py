from PySide2 import QtCore

import os.path





# ------------------------------------------------
#	Manage signal connections
# ------------------------------------------------
class Signal(QtCore.QObject):
	def __init__(self, hotBox):
		QtCore.QObject.__init__(self)


		self.hotBox = hotBox

		




	def buildConnectionDict(self):
		class_ = self.hotBox.sb.getClassObject(self.hotBox.name)(self.hotBox)

		buttonType = {'i':'clicked','b':'clicked','v':'clicked','s':'valueChanged','chk':'released','cmb':'currentIndexChanged','t':'returnPressed'}

		for prefix,signal in buttonType.iteritems(): #button/method's that start with ie. 'b'
			size = 200
			for num in xrange(size):
				numString = '000'[:-len(str(num))]+str(num) #remove zeros from the prefix string corresponding to the length of num
				buttonString = prefix+numString
				# if hasattr(self.hotBox.ui, buttonString):
				try: #get the button from the dynamic ui
					buttonObject = getattr(self.hotBox.ui, buttonString)  #equivilent to: self.hotBox.ui.b000
					size-=1 #decrease search length on each successful match

					#add signal to buttonObject
					buttonWithSignal = getattr(buttonObject, signal)

					#add eventfilter
					if prefix=='i' or prefix=='v' or prefix=='cmb' and self.hotBox.name=='main' or  self.hotBox.name=='viewport': #layoutStack index and viewport signals
						buttonObject.installEventFilter(self.hotBox) #ie. self.hotBox.ui.i000.installEventFilter(self)

					#set the corresponding method
					if prefix=='i': #connect to layoutStack and pass in an index.
						index = self.hotBox.sb.getUiIndex(buttonObject.whatsThis().lower()) #use the button's 'whatsThis' to get the index from uiList
						method = lambda index=index: self.hotBox.layoutStack(index) #lambda function to call index. ie. hotBox.layoutStack(6)
					else: #add class method
						#set the spinboxes for the create menu to connect to the setAttributes method, and pass in the index of the spinbox to set attributes for.
						if prefix=='s' and self.hotBox.name=='create' and num<=11:
							# method = lambda index=num: getattr(class_, 'setAttributes')(index)
							pass #moved to class until this is fixed. oddly the above slot calls setAttributes with spinbox value as argument.
						else:
							method = getattr(class_, buttonString) #use signal 'buttonString' (ie. b006) to get method/slot of the same name in current class.
							if prefix!='v':
								method = [method, lambda m=method: self.onPressedEvent(m)] #add onPressedEvent. pass multiple slots as list.
						#add values to connectionDict
					self.hotBox.sb.connectionDict(self.hotBox.name).update({buttonString:{'buttonObject':buttonObject, 'buttonObjectWithSignal':buttonWithSignal, 'methodObject':method}})
				except Exception as error:
					if error==AttributeError:
						print 'Exception:',error
		self.buildCommandNameDict()
		# print self.hotBox.sb.connectionDict(self.hotBox.name)
		return self.hotBox.sb.connectionDict(self.hotBox.name)


	def addSignal(self, name):
		#args: [string]
		for buttonString in self.hotBox.sb.connectionDict(name):
			signal = self.hotBox.sb.getSignal(name, buttonString)
			slot = self.hotBox.sb.getSlot(name, buttonString)
			try: map(signal.connect, slot) #add multiple slots
			except: signal.connect(slot) #add single slot (main and viewport)


	def removeSignal(self, name):
		#args: [string]
		for buttonString in self.hotBox.sb.connectionDict(name):
			signal = self.hotBox.sb.getSignal(name, buttonString)
			slot = self.hotBox.sb.getSlot(name, buttonString)
			try: map(signal.disconnect, slot) #add multiple slots
			except: signal.disconnect(slot) #add single slot (main and viewport)


	def onPressedEvent(self, method):
		#args: [method object]
		if type(method)==str and method.__name__.startswith('b'): #ie. 'b012'
			commandName = self.hotBox.sb.connectionDict(self.hotBox.name, method.__name__) #get the 'command name' value from the 'methodName' key.
			self.hotBox.prevCommand.append([method, commandName]) #build array that stores the command method object and the corresponding command name string (ie. 'Multi-cut tool') for repeatLastCommand
			# if len(self.hotBox.prevCommand)>20: #keep a list of the last 20 used commands.
			# 	del self.hotBox.prevCommand[0]



	def buildCommandNameDict(self): #dictionary of user friendly command names derived from the comment in the declaration line of button command methods.
		#'class':{connectionDict':{'methodString':{'methodName':'commentString'}} ie. 'polygons':{connectionDict':{'b000':{'methodName':'Multi_Cut Tool'}},
		path = os.path.join(os.path.dirname(__file__), self.hotBox.app+'/tk_slots_'+self.hotBox.app) #get absolute path from dir of this module + relative path to directory
		file = path+'/'+'tk_slots_'+self.hotBox.app+'_'+self.hotBox.name+'.py'

		with open(file) as f:
			for line in f.readlines():
				if 'def b' in line and '#' in line:
					methodString = line.split('#')[0].strip().lstrip('def ').rstrip('(self):')
					commentString = line.split('#')[1]
					try:
						self.hotBox.sb.setMethodName(self.hotBox.name, methodString, commentString)
					except Exception as error:
						if error==KeyError:
							print "#Exception: ", error



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------