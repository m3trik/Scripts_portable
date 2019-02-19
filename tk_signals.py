from PySide2 import QtCore

import os.path

from pydoc import locate






class Signal(QtCore.QObject):
	def __init__(self, hotBox):
		QtCore.QObject.__init__(self)


		self.hotBox = hotBox
		self.connectionDict={} #<key=ui name string identifier>:<value=dict{button object:method object}> ie."main : b001:main.b001"
		self.prevCommand=[] #history of commands. last used command method at element[-1]

		

	def buildConnectionDict(self):
		class_ = self.hotBox.classDict[self.hotBox.name](self.hotBox)

		buttonType = {'i':'clicked','b':'clicked','v':'clicked','s':'valueChanged','chk':'released','cmb':'currentIndexChanged','t':'returnPressed'}

		self.connectionDict[self.hotBox.name] = {} #initialize the key before attempting to add any values, so that a placeholder key will be generated even if no values are present.
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
					if prefix=='i' or prefix=='v': #layoutStack index and viewport signals
						buttonObject.installEventFilter(self.hotBox) #ie. self.hotBox.ui.i000.installEventFilter(self)

					#set the corresponding method
					if prefix=='i': #connect to layoutStack and pass in an index.
						index = self.hotBox.uiList.index(buttonObject.whatsThis().lower()) #use the button's 'whatsThis' to get the index from uiList
						method = lambda index=index: self.hotBox.layoutStack(index) #lambda function to call index. ie. hotBox.layoutStack(6)
					else: #add class method
						#set the spinboxes for the create menu to connect to the setAttributes method, and pass in the index of the spinbox to set attributes for.
						if prefix=='s' and self.hotBox.name=='create' and num<=11:
							# method = lambda index=num: getattr(class_, 'setAttributes')(index)
							pass #moved to class until this is fixed. oddly the above slot calls setAttributes with spinbox value as argument.
						else:
							method = getattr(class_, buttonString) #use signal 'buttonString' (ie. b006) to get method/slot of the same name in current class.
							if prefix!='v':
								method = [method, lambda m=method: self.onPressedEvent(m)] #add onPressedEvent

						#add signal/slot dict value to connectionDict[self.hotBox.name] key
					self.connectionDict[self.hotBox.name].update ({buttonWithSignal:method})
				except Exception as err:
					if err==AttributeError:
						print 'Exception:',err
		# print self.connectionDict
		return self.connectionDict


	def addSignal(self, name):
		#args: [string]
		for buttonObject,method in self.connectionDict[name].iteritems():
			try: map(buttonObject.connect, method) #add multiple slots
			except: buttonObject.connect(method) #add single slot (main and viewport)


	def removeSignal(self, name):
		#args: [string]
		for buttonObject,method in self.connectionDict[name].iteritems():
			try: map(buttonObject.disconnect, method) #remove multiple slots
			except: buttonObject.disconnect(method) #remove single slot (main and viewport)


	def repeatLastCommand(self):
		self.prevCommand[-1]()


	def onPressedEvent(self, method):
		#args: [method object]
		#build array that stores prevCommand string for repeatLastCommand
		self.prevCommand.append(method)
		if len(self.prevCommand)>20: #keep a list of the last 20 used commands.
			del self.prevCommand[0]
		self.hotBox.hide_()



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------