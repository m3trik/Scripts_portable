from PySide2 import QtGui, QtCore, QtWidgets
import pymel.core as pm #used when expressions passed into the try_ method

import os.path







class Slot(object):
	def __init__(self, hotBox):

		self.hotBox = hotBox

		#init styleSheet
		self.initStyleSheet()
		#init widgets
		self.initWidgets()




	def chk000(self): #pin open a separate instance of the ui in a new window
		pass
		# if self.hotBox.ui.chk000.isChecked():
		# 	print 'chk000'
		# 	self.hotBox.pin(self.hotBox.ui)
		# else:
		# 	self.hotBox.pin.hide()



	#returns a list of objects from a string list.
	@staticmethod
	def getObject(class_, objectNames, showError_=False, print_=False):
		#args:	class_=class object
		#				objectNames='string' - names separated by ','. ie. 's000,b004-7'. b004-7 specifies buttons b004-b007.  
		#				showError=bool - show attribute error if item doesnt exist
		#				print_=bool - print unpacked objectNames to console.
		#returns: list of corresponding objects
		#ex. getObject(self.hotBox.ui, 's000,b002,cmb011-15') #get objects for s000,b002, and cmb011-cmb015
		packed_names = [n.strip() for n in objectNames.split(',') if '-' in n] #build list of all objectNames passed in containing '-'

		unpacked_names=[]
		for name in packed_names:
			name=name.split('-') #ex. split 'b000-8'
			prefix = name[0].strip('0123456789') #ex. split 'b' from 'b000'
			start = int(name[0].strip('abcdefghijklmnopqrstuvwxyz') or 0) #start range. #ex. '000' #converting int('000') returns None, if case; assign 0.
			stop = int(name[1])+1 #end range. #ex. '9' from 'b000-8' for range up to 9 but not including 9.
			unpacked_names.extend([str(prefix)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)]) #build list of name strings within given range

		names = [n.strip() for n in objectNames.split(',') if '-' not in n] #all objectNames passed in not containing '-'
		if print_: print names+unpacked_names

		objects=[]
		for name in names+unpacked_names:
			try:
				objects.append(getattr(class_, name)) #equivilent to:(self.hotBox.ui.m000)
			except: 
				if showError_:
					print "# Error in getObject():"+str(class_)+" has no attribute "+str(name)+" #"
				else: pass
		return objects



	#init signals, button states etc. for a stacked widget class
	def initWidgets(self):
		for comboBox in self.getObject(self, 'cmb000-50', False):
			comboBox()


		if self.hotBox.name == 'create':
			self.setButtons(self.hotBox.ui, invisible='s000-11, t000')


		if self.hotBox.name == 'init':
			self.hotBox.ui.t000.viewport().setAutoFillBackground(False)




	@staticmethod
	def comboBox(comboBox, items, title=None):
		#args: comboBox=QComboBox object - list of items to fill the comboBox with
		#			title='string' - optional value for the first index of the comboboxs list
		#returns: combobox's current item list
		#ex. comboBox (self.hotBox.ui.cmb003, ["Import file", "Import Options"], "Import")
		comboBox.blockSignals(True) #to keep clear from triggering currentIndexChanged
		comboBox.clear()
		# items = items+['refresh'] #refresh string is a temp work around until comboBox is called on open insead of index change.
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
		#ex. setButtons(self.hotBox.ui, disable='b000', unchecked='b009-12', invisible='b015')
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
			


	#set spinbox values explicitly or for each in range
	def setSpinboxes(self, ui, spinboxNames='s000-15', values=[]):
		#args:	ui=<dynamic ui>
		#				spinboxNames='string' - spinbox string object names (used in place of the range argument). ie. 's001-4, s007'.  
		#											default value will try to add values to spinboxes starting at s000 and add values in order skipping any spinboxes not found in the ui.
		#			 	values=int or [(tuple) list] - tuple representing a string prefix label and value, and/or just a value. [(string prefix,int value)] ie. [("size",5), 20, ("width",8)]
		#returns: list of values without prefix
		#ex. self.setSpinboxes (self.hotBox.ui, values=[("width",1),("length ratio",1),("patches U",1),("patches V",1)]) #range. dict 'value's will be added to corresponding spinbox starting at s000 through s003.
		#ex. self.setSpinboxes (self.hotBox.ui, spinboxNames='s000', values=[('size',5)]) #explicit;  set single s000 with a label 'size' and value of 5. multiple spinboxes can be set this way. specify a range of spinboxes using 's010-18'.
		spinboxes = self.getObject(ui, spinboxNames) #get spinbox objects

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
	@staticmethod
	#used for maintaining toggling sequences for multiple objects simultaniously
	def cycle(id_sequence, query=False): #toggle between numbers in a given sequence
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



	@staticmethod
	def try_(expressions, exceptions='pass', showError_=True, print_=False, **kwargs):
		#args: expressions='string' - expression separated by ';'
		#			exceptions='string' - separated by ';'
		#			showError_=bool - hide or show any errors
		#			printCommand=bool - print expression/s to console
		#			*kwargs=any additional arguments used by expressions.
		#returns: True if no errors occured, else: False
		#ex. self.try_('pm.delete(arg1)', arg1=radialArrayObjList) #pass in radialArrayObjList as a **kwarg.
		#ex. self.try_('pm.ls(selection=1, objectsOnly=1)[0]; <additional command>, exceptions=" ERROR: Nothing selected."')
		didCodeExecWithoutError=True

		for key,value in kwargs.iteritems():
			locals()[key]=value #create variables for any kwargs passed in

		for expression in expressions.split(';'): #split string arg at ';'
			try:
				expression = expression.lstrip(" ") #strip any leading whitespace
				if print_: print expression
				exec (expression)
			except Exception as err:
				didCodeExecWithoutError=False #if any errors occur return False
				if showError_:
					print "# Error in try_(): "+str(err)+" #"
				exec (exceptions)
		return didCodeExecWithoutError



	# ------------------------------------------------
	#' LayoutStack StyleSheet'
	# ------------------------------------------------



	def initStyleSheet(self):
		#specific case StyleSheet
		if self.hotBox.name=='main':
			buttons = self.getObject(self.hotBox.ui, 'i003-24', showError_=False)
			for button in buttons:
				button.setStyleSheet('''QPushButton:hover {   
					border: 1px solid black;
					border-radius: 5px;
					background-color:#66c0ff;
					}''')
			#setStyleSheet for transparent buttons
			buttons = self.getObject(self.hotBox.ui, 'v000-8, i020-23', showError_=False)
			for button in buttons:
				button.setStyleSheet("border: 1px solid transparent;")

		if self.hotBox.name=='viewport':
			buttons = self.getObject(self.hotBox.ui, 'v000-8')
			for button in buttons:
				button.setStyleSheet('''QPushButton:hover {   
					border: 1px solid black;
					border-radius: 5px;   
					background-color:#66c0ff;
					}''')
			#setStyleSheet for transparent buttons
			buttons = self.getObject(self.hotBox.ui, 'v008-15', showError_=False)
			for button in buttons:
				button.setStyleSheet("border: 1px solid transparent;")

		if self.hotBox.name == 'init':
			self.hotBox.ui.t000.setTextBackgroundColor(QtGui.QColor(50, 50, 50))


		#general case style sheet
		buttons = self.getObject(self.hotBox.ui, 'chk000-50', showError_=False)
		# buttons.append (self.getObject(self.hotBox.ui, 'chkpin'))
		for button in buttons:
			button.setStyleSheet('''QPushButton:checked{
			background-color: rgb(170, 70, 255);
			}''')

		buttons = self.getObject(self.hotBox.ui, 'b000-100', showError_=False)
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