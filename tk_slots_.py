from PySide2 import QtGui, QtCore, QtWidgets

import os.path








class Slot(object):
	def __init__(self, hotBox):

		self.hotBox = hotBox

		#init styleSheet
		self.initStyleSheet()
		#init widgets
		self.initWidgets()




	def chk000(self): #pin open a separate instance of the ui in a new window
		if self.hotBox.ui.chk000.isChecked():
			print 'chk000'
			self.hotBox.pin(self.hotBox.ui)
		else:
			self.hotBox.pin.hide()




		#returns a list of objects from a supplied range, or string list.
	def getObject(self, class_, objectNames, range_=None, showError_=True):
		#args: class_=class object
		#			 objectNames='string' - single name when used with range arg. ie. 's'  else; names separated by ','. ie. ['s000,s001,s002'] 
		#			 range_=[int list] - integers representing start, end of range. used with single string type objectName.  ie. [2,10]
		#		 	 showError=bool - show attribute error if item doesnt exist
		#returns: list of corresponding objects
		#ex. getObject(self.hotBox.ui, 's', [0,10])  or  getObject(self.hotBox.ui, ['s000,s002,s011'])
		if range_: #if range is given; generate list within given range_
			start, stop = range_[0], range_[1] #add a numberical suffix to the object name within the given range.
			names = [str(objectNames)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)] #build list of name strings within given range
		else: #use the list of names passed in as objectName
			names = objectNames.split(',')
		objects=[]
		for name in names:
			# if hasattr(class_, name):
			try:
				objects.append(getattr(class_, name)) #equivilent to:(self.hotBox.ui.m000)
			# elif showError_:
			except: 
				if showError_:
					print "# Error:"+str(class_)+" has no attribute "+str(name)+" #"
				else: pass
		return objects


	#init signals, button states etc. for a stacked widget class
	def initWidgets(self):
		if self.hotBox.name == 'init':
			# self.hotBox.ui.t000.clearFocus()
			self.hotBox.ui.t000.viewport().setAutoFillBackground(False)

		if self.hotBox.name != 'create':
			#ex. initWidgets(self)
			for comboBox in self.getObject(self.hotBox, 'cmb', [0,50], False):
				# combobox.currentIndexChanged.connect(self.combobox.objectName())
				comboBox()

		if self.hotBox.name == 'create':
			self.setButtons(self.hotBox.ui, invisible='s000,s010,s011,t000')
			#temp fix for function below calling setAttributes with only last arg
			self.hotBox.ui.s000.valueChanged.connect (lambda: self.hotBox.setAttributes(0))
			self.hotBox.ui.s001.valueChanged.connect (lambda: self.hotBox.setAttributes(1))
			self.hotBox.ui.s002.valueChanged.connect (lambda: self.hotBox.setAttributes(2))
			self.hotBox.ui.s003.valueChanged.connect (lambda: self.hotBox.setAttributes(3))
			self.hotBox.ui.s004.valueChanged.connect (lambda: self.hotBox.setAttributes(4))
			self.hotBox.ui.s005.valueChanged.connect (lambda: self.hotBox.setAttributes(5))
			self.hotBox.ui.s006.valueChanged.connect (lambda: self.hotBox.setAttributes(6))
			self.hotBox.ui.s007.valueChanged.connect (lambda: self.hotBox.setAttributes(7))
			self.hotBox.ui.s008.valueChanged.connect (lambda: self.hotBox.setAttributes(8))
			self.hotBox.ui.s009.valueChanged.connect (lambda: self.hotBox.setAttributes(9))
			self.hotBox.ui.s010.valueChanged.connect (lambda: self.hotBox.setAttributes(10))
			self.hotBox.ui.s011.valueChanged.connect (lambda: self.hotBox.setAttributes(11))
			spinboxes = self.getObject(self.hotBox.ui, 's', [0,12], False)
			for index, spinbox in enumerate(spinboxes):
				# spinbox.valueChanged.connect (lambda i=index: self.hotBox.setAttributes(i)) #use lambda to call method with argument: index of spinbox
				spinbox.setVisible(False)


	def comboBox(self, comboBox, items, title=None):
		#args: comboBox=QComboBox object - list of items to fill the comboBox with
		#			title='string' - optional value for the first index of the comboboxs list
		#returns: combobox's current item list
		#ex. comboBox (self.hotBox.ui.cmb003, ["Import file", "Import Options"], "Import")
		comboBox.blockSignals(True) #to keep clear from triggering currentIndexChanged
		comboBox.clear()
		items = items+['refresh'] #refresh string is a temp work around. until we override to call comboBox on open insead of index change.
		if title:
			comboBox.addItem(title)
		comboBox.addItems(items)
		comboBox.blockSignals(False)
		if title:
			return [title]+items
		else:
			return items


	class CheckableComboBox(QtWidgets.QComboBox):
		# once there is a checkState set, it is rendered
		# here we assume default Unchecked
		def addItem(self, item):
			super(CheckableComboBox, self).addItem(item)
			item = self.model().item(self.count()-1,0)
			item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
			item.setCheckState(QtCore.Qt.Unchecked)

		def checkIndex(self, index):
			item = self.model().item(index,0)
			return item.checkState() == QtCore.Qt.Checked



	#ex. set various states for multiple buttons at once  
	def setButtons(self, ui, checked=None, unchecked=None, enable=None, disable=None, visible=None, invisible=None):
		#args: setButtons=dynamic ui object
		#			checked/unchecked/enable/disable/visible/invisible=string - the names of buttons to modify separated by ','. ie. 'b000,b001,b022'
		#ex. setButtons(self.hotBox.ui, disable=['b000'], unchecked=['b009,b010,b012'])
		if checked:
			checked = self.getObject(ui,checked)
			[button.setChecked(True) for button in checked]
			
		if unchecked:
			unchecked = self.getObject(ui,unchecked)
			[button.setChecked(False) for button in unchecked]
				
		if enable:
			enable = self.getObject(ui,enable)
			[button.setEnabled(True) for button in enable]
				
		if disable:
			disable = self.getObject(ui,disable)
			[button.setDisabled(True) for button in disable]
				
		if visible:
			visible = self.getObject(ui,visible)
			[button.setVisible(True) for button in visible]
				
		if invisible:
			invisible = self.getObject(ui,invisible)
			[button.setVisible(False) for button in invisible]
				


	def setSpinboxes(self, ui, values, range_=[0,9], spinboxNames=None):
		#args: spinboxNames=[string list] - spinbox string object names (used in place of the range argument). ie. ['s000,s001,s002']
		#			 range_=[int list] - [int start, int end] of spinbox range. ie. spinboxes 2-10.  ie. [2,10]
		#			 values=int or [tuple list] - tuple representing a string prefix and value, and/or just a value. [(string prefix,int value)] ie. [("size",5), 20, ("width",8)]
		#returns: list of values without prefix
		#ex. setSpinboxes (self.hotBox.ui, values=[("width",1),("length ratio",1),("patches U",1),("patches V",1)])
		if spinboxNames: #get spinbox objects
			spinboxes = self.getObject(ui, spinboxNames)
		else:
			spinboxes = self.getObject(ui, 's', range_)

		#clear previous values
		for spinbox in spinboxes:
			spinbox.blockSignals(True) #block signals to keep from calling method on valueChanged
			spinbox.setPrefix('')
			spinbox.setValue(0)
			spinbox.setDisabled(True)
			spinbox.setVisible(False)

		values_=[] #list of values to return.
		#set new values
		for i, value in enumerate(values):
			spinboxes[i].setVisible(True)
			spinboxes[i].setEnabled(True)
			if type(value) == tuple:
				spinboxes[i].setPrefix(value[0]+':  ')
				spinboxes[i].setValue(value[1])
				values_.append(value[1])
			else:
				spinboxes[i].setValue(value)
				values_.append(value)
			spinboxes[i].blockSignals(False)

		return values_


	cycleDict={}
	#used for maintaining toggling sequences for multiple objects simultaniously
	def cycle(self, id_sequence, query=False): #toggle between numbers in a given sequence
		#args: id_sequence=string or int list - id_numberical sequence ie. 'name_123' or [1,2,3].
		#			takes the string argument and splits it at '_'
		#			converting the second numberical half to integers and putting them in a list.
		#			each time this function is called, it returns the next number in that list
		#			using the original string as a unique id.
		#ex. cycle('componentID_01234')
		try:
			if query:
				return int(cycleDict[id_sequence][-1]) #get the current value ie. 0
			value = cycleDict[id_sequence] #check if key exists. if so return the value. ie. value = [1,2,3]
		except KeyError: #else create sequence list for the given key
			id_ = id_sequence.split('_')[0] #ie. name
			sequence = id_sequence.split('_')[1] #ie. 123
			cycleDict[id_sequence] = [i for i in list(sequence)] #ie. {name_123:[1,2,3]}
		value = cycleDict[id_sequence][0] #get the next value ie. 1
		cycleDict[id_sequence] = cycleDict[id_sequence][1:]+[value] #move the value to the end of the list ie. {name_123:[2,3,1]}
		return int(value) #return an integer from string value


	def try_(self, expressions, exceptions='pass', showError_=True):
		#args: expressions='string' - expression separated by ';'
		#			exceptions='string' - separated by ';'
		#			showError_=bool - hide or show any errors
		#returns: True if no errors occured, else: False
		#ex. try_('pm.ls(selection=1, objectsOnly=1)[0]', 'print "# Warning: Nothing selected #"')
		pass_=True
		for expression in expressions.split(';'): #split string arg at ';'
			try:
				print expression
			except Exception as err:
				pass_=False #if any errors occur return False
				if showError_:
					print "# Error: "+str(err)+" #"
				exec (exceptions)
			return pass_



	# ------------------------------------------------
	#' LayoutStack StyleSheet'
	# ------------------------------------------------


	def initStyleSheet(self):
		#specific case StyleSheet
		if self.hotBox.name=='main':
			buttons = self.getObject(self.hotBox.ui, 'i', [3,25], False)
			for button in buttons:
				button.setStyleSheet('''QPushButton:hover {   
					border: 1px solid black;
					border-radius: 5px;
					background-color:#66c0ff;
					}''')
			#setStyleSheet for transparent buttons
			buttons = self.getObject(self.hotBox.ui, 'v', [0,8])+self.getObject(self.hotBox.ui, 'i', [20,24])
			for button in buttons:
				button.setStyleSheet("border: 1px solid transparent;")

		if self.hotBox.name=='viewport':
			buttons = self.getObject(self.hotBox.ui, 'v', [0,8])
			for button in buttons:
				button.setStyleSheet('''QPushButton:hover {   
					border: 1px solid black;
					border-radius: 5px;   
					background-color:#66c0ff;
					}''')
			#setStyleSheet for transparent buttons
			buttons = self.getObject(self.hotBox.ui, 'v', [8,16])
			for button in buttons:
				button.setStyleSheet("border: 1px solid transparent;")

		if self.hotBox.name == 'init':
			self.hotBox.ui.t000.setTextBackgroundColor(QtGui.QColor(50, 50, 50))


		#general case style sheet
		buttons = self.getObject(self.hotBox.ui, 'chk', [0,50], False)
		# buttons.append (self.getObject(self.hotBox.ui, ['chkpin']))
		for button in buttons:
			button.setStyleSheet('''QPushButton:checked{
			background-color: rgb(170, 70, 255);
			}''')

		buttons = self.getObject(self.hotBox.ui, 'b', [0,100], False)
		for button in buttons:
			button.setStyleSheet('''QPushButton:hover {   
				border: 1px solid black;
				border-radius: 5px;
				background-color:#66c0ff;
				}''')


#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------