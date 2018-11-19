from PySide2 import QtCore

import os.path








class Signal(QtCore.QObject):
	def __init__(self, hotBox):
		QtCore.QObject.__init__(self)


		self.hotBox = hotBox
		self.connectionDict={} #<key=ui name string identifier>:<value=dict{button object:method object}> ie."main : b001:main.b001"
		self.prevCommand=[] #history of commands. last used command method at element[-1]


	def buildConnectionDict(self, name):
		currentIndex = self.hotBox.uiList.index(name)
		ui = self.hotBox.stackedLayout.widget(currentIndex)

		buttonType = {'b':'clicked','v':'clicked','s':'valueChanged','chk':'released','cmb':'currentIndexChanged','t':'returnPressed'}
		if name=='main' or name=='viewport': buttonType = {'i':'clicked','v':'clicked'}

		self.connectionDict[name] = {} #initialize the key before attempting to add any values, so that a placeholder key will be generated even if no values are present.
		for prefix,signal in buttonType.iteritems(): #button/method's that start with ie. 'b'
			size = 200
			for num in xrange(size):
				numString = '000'[:-len(str(num))]+str(num) #remove zeros from the prefix string corresponding to the length of num
				buttonString = prefix+numString
				# if hasattr(ui, buttonString):
				try: #get the button from the dynamic ui
					buttonObject = getattr(ui, buttonString)  #equivilent to: self.ui.b000
					size-=1 #decrease search length on each successful match

					#add signal
					buttonWithSignal = getattr(buttonObject, signal)

					#add eventfilter
					if prefix=='i' or prefix=='v': #layoutStack index and viewport signals
						buttonObject.installEventFilter(self.hotBox) #ie. ui.i000.installEventFilter(self)

					#get the corresponding method
					if prefix=='i': #add slot to change index
						index = self.hotBox.uiList.index(buttonObject.whatsThis().lower()) #use the button's 'whatsThis' to get the index from uiList
						method = lambda i=index: self.hotBox.layoutStack(i) #lambda function to call index. ie. hotBox.layoutStack(6)
					else: #add class method
						# if hasattr(self.hotBox.class_(self.hotBox), buttonString):
						method = getattr(self.hotBox.class_(self.hotBox), buttonString) #use 'buttonString' (ie. b006) to get method of the same name in current class_.
						if prefix!='v':	#add onPressedEvent
							method = [method, lambda m=method: self.onPressedEvent(m)]
						#add signal/slot dict value to connectionDict[name] key
					self.connectionDict[name].update ({buttonWithSignal:method})
				except Exception as err: print err
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



#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------