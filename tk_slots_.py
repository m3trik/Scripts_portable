from PySide2 import QtGui, QtCore, QtWidgets

import os.path

from tk_switchboard import Switchboard






class Slot(object):
	def __init__(self):

		self.sb = Switchboard()
		self.hotBox = self.sb.getClass('hotbox')
		self.signal = self.sb.getClass('signal')()
		
		
		self.styleSheetOverride()
		





	def getMethod(self, class_, method):
		'''
		#args:
			class_='string' class name (case insensitive)
			method='string' method name
		#returns:
		 	method object
		'''
		c = class_.lower()
		if not self.sb.hasKey(c, 'connectionDict'):
			self.hotBox.signal.buildConnectionDict(c) #construct the signals and slots for the ui 

			print self.sb.getDocString(c, method)
		return self.sb.getMethod(c, method)



	#returns a list of objects from a string list.
	@staticmethod
	def getObject(class_, objectNames, showError_=False, print_=False):
		'''
		args:	 class_=class object
				 objectNames='string' - names separated by ','. ie. 's000,b004-7'. b004-7 specifies buttons b004-b007.  
				 showError=bool - show attribute error if item doesnt exist
				 print_=bool - print unpacked objectNames to console.
		
		returns: list of corresponding objects
		#ex. getObject(self.ui, 's000,b002,cmb011-15') #get objects for s000,b002, and cmb011-cmb015
		'''
		packed_names = [n.strip() for n in objectNames.split(',') if '-' in n] #build list of all objectNames passed in containing '-'

		unpacked_names=[]
		for name in packed_names:
			name=name.split('-') #ex. split 'b000-8'
			prefix = name[0].strip('0123456789') #ex. split 'b' from 'b000'
			start = int(name[0].strip('abcdefghijklmnopqrstuvwxyz') or 0) #start range. #ex. '000' #converting int('000') returns None, if case; assign 0.
			stop = int(name[1])+1 #end range. #ex. '9' from 'b000-8' for range up to 9 but not including 9.
			unpacked_names.extend([str(prefix)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)]) #build list of name strings within given range

		names = [n.strip() for n in objectNames.split(',') if '-' not in n] #all objectNames passed in not containing '-'
		if print_: print names+unpacked_names #used for debugging

		objects=[]
		for name in names+unpacked_names:
			try:
				objects.append(getattr(class_, name)) #equivilent to:(self.ui.m000)
			except: 
				if showError_:
					print "# Error in getObject():"+str(class_)+" has no attribute "+str(name)+" #"
				else: pass
		return objects



	@staticmethod
	def comboBox(comboBox, items, title=None):
		'''
		args:	 comboBox=QComboBox object - list of items to fill the comboBox with
				 title='string' - optional value for the first index of the comboboxs list
		
		returns: combobox's current item list
		ex. comboBox (self.ui.cmb003, ["Import file", "Import Options"], "Import")
		'''
		comboBox.blockSignals(True) #to keep clear from triggering currentIndexChanged
		index = comboBox.currentIndex() #get current index before refreshing list
		comboBox.clear()
		
		if title:
			comboBox.addItem(title)
		comboBox.addItems(items)

		comboBox.setCurrentIndex(index)
		comboBox.blockSignals(False)

		if title:
			return [title]+items
		else:
			return items



	#ex. set various states for multiple buttons at once
	@staticmethod
	def setButtons(ui, checked=None, unchecked=None, enable=None, disable=None, visible=None, invisible=None):
		'''
		args:	 setButtons=dynamic ui object
				 checked/unchecked/enable/disable/visible/invisible=string - the names of buttons to modify separated by ','. ie. 'b000,b001,b022'
		ex.	setButtons(self.ui, disable='b000', unchecked='chk009-12', invisible='b015')
		'''
		if checked:
			checked = Slot.getObject(ui,checked)
			[button.setChecked(True) for button in checked]
			
		if unchecked:
			unchecked = Slot.getObject(ui,unchecked)
			[button.setChecked(False) for button in unchecked]
				
		if enable:
			enable = Slot.getObject(ui,enable)
			[button.setEnabled(True) for button in enable]
				
		if disable:
			disable = Slot.getObject(ui,disable)
			[button.setDisabled(True) for button in disable]
				
		if visible:
			visible = Slot.getObject(ui,visible)
			[button.setVisible(True) for button in visible]
				
		if invisible:
			invisible = Slot.getObject(ui,invisible)
			[button.setVisible(False) for button in invisible]
	


	@staticmethod
	def getAttributes(node, exclude=None):
		'''
		args:	node=object
				exclude='string list' - attributes to exclude from returned dictionay

		returns:	dictionary {'string attribute': value}
		'''
		return {attr:getattr(node, attr) for attr in dir(node) if attr not in exclude}



	@staticmethod
	def setAttributes(node, attributes):
		'''
		args:	node=object
				attributes=dictionary {'string attribute': value} - attributes and their correponding value to set
		'''
		[setattr(node, attr, value) for attr, value in attributes.iteritems() if attr and value]



	#set spinbox values explicitly or for each in range
	@staticmethod
	def setSpinboxes(ui, spinboxNames, attributes={}):
		'''
		args:	 ui=<dynamic ui>
				 spinboxNames='string' - spinbox string object names (used in place of the range argument). ie. 's001-4, s007'.
							  default value will try to add values to spinboxes starting at s000 and add values in order skipping any spinboxes not found in the ui.
				 attributes={'string key':value}

		ex. self.setSpinboxes (self.ui, spinboxNames='s000-15', attributes={'width':1, 'length ratio':1, 'patches U':1, 'patches V':1})
		ex. self.setSpinboxes (self.ui, spinboxNames='s000', attributes={'size':5} #explicit;  set single s000 with a label 'size' and value of 5
		'''
		spinboxes = Slot.getObject(ui, spinboxNames) #get spinbox objects

		#clear previous values
		for spinbox in spinboxes:
			spinbox.blockSignals(True)
			spinbox.setVisible(False)

		#set values
		for index, (key, value) in enumerate(attributes.items()):
			if any([type(value)==int, type(value)==float, type(value)==bool]):
				if value is bool:
					value = int(value)
					spinboxes[index].setMaximum(1)
					spinboxes[index].setSuffix(' <bool>')
				else:
					spinboxes[index].setMaximum(9999)
				spinboxes[index].setVisible(True)
				spinboxes[index].setPrefix(key+':  ')
				spinboxes[index].setValue(value)
				spinboxes[index].setSuffix('')
				spinboxes[index].blockSignals(False)



	progress=0
	def progressBar(self, length=100, init=False):
		'''
		args:
			ui=dynamic ui object
			length=int - total length of procedure

		returns: current percentage
		ie.
		self.progressBar(init=1) #initialize the progress bar
		for obj in selection:
			self.progressBar(len(selection)) #register progress
		'''
		ui=self.sb.getUi()
		global progress
		if init:
			progress=0
			ui.progressBar.show()
			return
		progress+=1
		value = 100*progress/length
		ui.progressBar.setValue(value)
		# QtGui.qApp.processEvents() #ensure that any pending events are processed sufficiently often for the GUI to remain responsive
		if progress>=100:
			ui.progressBar.hide()
			ui.progressBar.setValue(0)
		return value


	global cycleDict
	cycleDict={}
	@staticmethod
	#used for maintaining toggling sequences for multiple objects simultaniously
	def cycle(sequence, name=None, query=False): #toggle between numbers in a given sequence
		'''
		each time this function is called, it returns the next number in the sequence
		using the name string as an identifier key.
		
		args:
			sequence=[list] - sequence to cycle through. ie. [1,2,3].
			name='string' - identifier. used as a key to get the sequence value from the dict.
			
		ex. cycle([0,1,2,3,4], 'componentID')
		'''
		try:
			if query: #return the value without changing it.
				return cycleDict[name][-1] #get the current value ie. 0

			value = cycleDict[name] #check if key exists. if so return the value. ie. value = [1,2,3]
		
		except KeyError: #else create sequence list for the given key
			cycleDict[name] = [i for i in sequence] #ie. {name:[1,2,3]}

		value = cycleDict[name][0] #get the current value. ie. 1
		cycleDict[name] = cycleDict[name][1:]+[value] #move the current value to the end of the list. ie. [2,3,1]
		return value #return current value. ie. 1




	@staticmethod
	def try_(expressions, exceptions='pass', showError_=True, print_=False, **kwargs):
		'''
		args:	 expressions='string' - expression separated by ';'
				 exceptions='string' - separated by ';'
				 showError_=bool - hide or show any errors
				 printCommand=bool - print expression/s to console
				 *kwargs=any additional arguments used by expressions.
		
		returns: True if no errors occured, else: False
		ex. self.try_('pm.delete(arg1)', arg1=radialArrayObjList) #pass in radialArrayObjList as a **kwarg.
		ex. self.try_('pm.ls(selection=1, objectsOnly=1)[0]; <additional command>, exceptions=" ERROR: Nothing selected."')
		'''
		try: import pymel.core as pm; #used when expressions are passed into the try_ method
		except: pass

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



		
	@staticmethod
	def collapseList(list_):
		'''
		#args:
				list_=list - of integers
		#returns:
				list with sequencial integers collapsed in string format. ie. ['20', '22..28']
		'''
		list_ = [str(x) for x in list_] #make sure the list is made up of strings.
		
		ranges=[]
		for x in list_:
			if not ranges:
				ranges.append([x])
			elif int(x)-prev_x == 1:
				ranges[-1].append(x)
			else:
				ranges.append([x])
			prev_x = int(x)

		collapsedList = ["..".join([r[0], r[-1]] if len(r) > 1 else r) for r in ranges]
		return collapsedList
	
	


	# ------------------------------------------------
	#' Set widget state and style overrides'
	# ------------------------------------------------



	#init signals, button states etc. for a stacked widget class
	# def initWidgets(self):
	# 	for comboBox in Slot.getObject(self, 'cmb000-50', False):
	# 		try: comboBox()
	# 		except: pass




	def styleSheetOverride(self):
		ui = self.sb.getUi()
		if self.hotBox.name=='viewport':
			buttons = Slot.getObject(ui, 'cmb000-3', showError_=False)
			for button in buttons: #setStyleSheet for transparent buttons
				button.setStyleSheet('''
					QPushButton {border: 1px solid transparent;}
					QComboBox {background-color: transparent; color: white;}
					QComboBox::drop-down {border-width: 0px;}
					QComboBox::down-arrow {image: url(:/none); border-width: 0px;}
					''')
			

		if self.hotBox.name=='create':
			self.setButtons(ui, invisible='s000-13')


		if self.hotBox.name=='init':
			ui.t000.viewport().setAutoFillBackground(False)
			ui.t000.setTextBackgroundColor(QtGui.QColor(50, 50, 50))











#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------


#depricated:

# def setSpinboxes(ui, spinboxNames='s000-15', values=[]):
# 	'''
# 	args:	 ui=<dynamic ui>
# 			 spinboxNames='string' - spinbox string object names (used in place of the range argument). ie. 's001-4, s007'.  
# 						  default value will try to add values to spinboxes starting at s000 and add values in order skipping any spinboxes not found in the ui.
# 			 values=int or [(tuple) list] - tuple representing a string prefix label and value, and/or just a value. [(string prefix,int value)] ie. [("size",5), 20, ("width",8)]
	
# 	returns: list of values without prefix
# 	ex. self.setSpinboxes (self.ui, values=[("width",1),("length ratio",1),("patches U",1),("patches V",1)]) #range. dict 'value's will be added to corresponding spinbox starting at s000 through s003.
# 	ex. self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',5)]) #explicit;  set single s000 with a label 'size' and value of 5. multiple spinboxes can be set this way. specify a range of spinboxes using 's010-18'.
# 	'''
# 	spinboxes = Slot.getObject(ui, spinboxNames) #get spinbox objects

# 	#clear previous values
# 	for spinbox in spinboxes:
# 		spinbox.blockSignals(True) #block signals to keep from calling method on valueChanged
# 		spinbox.setPrefix('')
# 		spinbox.setValue(0)
# 		spinbox.setDisabled(True)
# 		spinbox.setVisible(False)

# 	values_=[] #list of values to return.
# 	#set new values
# 	for i, value in enumerate(values):
# 		spinboxes[i].setVisible(True)
# 		spinboxes[i].setEnabled(True)
# 		if type(value) == tuple:
# 			spinboxes[i].setPrefix(value[0]+':  ')
# 			spinboxes[i].setValue(value[1])
# 			values_.append(value[1])
# 		else:
# 			spinboxes[i].setValue(value)
# 			values_.append(value)
# 		spinboxes[i].blockSignals(False)

# 	return values_