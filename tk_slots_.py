from PySide2 import QtGui, QtCore, QtWidgets

import os.path

from tk_switchboard import Switchboard
import tk_styleSheet as styleSheet





class Slot(object):
	def __init__(self):

		self.sb = Switchboard()
		self.hotBox = self.sb.getClass('hotbox')
		self.ui = self.sb.getUi()


		#init styleSheet
		self.initStyleSheet()
		#init widgets
		self.initWidgets()





	#returns a list of objects from a string list.
	def getObject(self, class_, objectNames, showError_=False, print_=False):
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
		if print_: print names+unpacked_names

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
	def setButtons(self, ui, checked=None, unchecked=None, enable=None, disable=None, visible=None, invisible=None):
		'''
		args:	 setButtons=dynamic ui object
				 checked/unchecked/enable/disable/visible/invisible=string - the names of buttons to modify separated by ','. ie. 'b000,b001,b022'
		ex.	setButtons(self.ui, disable='b000', unchecked='b009-12', invisible='b015')
		'''
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
		'''
		args:	 ui=<dynamic ui>
				 spinboxNames='string' - spinbox string object names (used in place of the range argument). ie. 's001-4, s007'.  
							  default value will try to add values to spinboxes starting at s000 and add values in order skipping any spinboxes not found in the ui.
				 values=int or [(tuple) list] - tuple representing a string prefix label and value, and/or just a value. [(string prefix,int value)] ie. [("size",5), 20, ("width",8)]
		
		returns: list of values without prefix
		ex. self.setSpinboxes (self.ui, values=[("width",1),("length ratio",1),("patches U",1),("patches V",1)]) #range. dict 'value's will be added to corresponding spinbox starting at s000 through s003.
		ex. self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',5)]) #explicit;  set single s000 with a label 'size' and value of 5. multiple spinboxes can be set this way. specify a range of spinboxes using 's010-18'.
		'''
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



	
	


	# ------------------------------------------------
	#' Set widget state and style overrides'
	# ------------------------------------------------



	#init signals, button states etc. for a stacked widget class
	def initWidgets(self):
		for comboBox in self.getObject(self, 'cmb000-50', False):
			try: comboBox()
			except: pass




	def initStyleSheet(self):
		#general case style sheet
		buttons = self.getObject(self.ui, 'i000-50, v000-50, b000-100, t000-50, s000-50, chk000-50, cmb000-50', showError_=False)
		# buttons.append (self.getObject(self.ui, 'chkpin'))
		for button in buttons:
			button.setStyleSheet(styleSheet.css)

		#specific case StyleSheet overrides:
		if self.hotBox.name=='main':
			#setStyleSheet for transparent buttons
			buttons = self.getObject(self.ui, 'v000-13, i020-23, cmb000-25', showError_=False)
			for button in buttons:
				button.setStyleSheet('''
					QPushButton {border: 1px solid transparent;}
					QComboBox::drop-down {border-width: 0px;}
					QComboBox::down-arrow {image: url(:/none); border-width: 0px;}
					''')
					

		if self.hotBox.name=='viewport':
			#setStyleSheet for transparent buttons
			buttons = self.getObject(self.ui, 'v008-15, cmb000-25', showError_=False)
			for button in buttons:
				button.setStyleSheet('''
					QPushButton {border: 1px solid transparent;}
					QComboBox {background-color: transparent; color: grey;}
					QComboBox::drop-down {border-width: 0px;}
					QComboBox::down-arrow {image: url(:/none); border-width: 0px;}
					''')
				

		if self.hotBox.name=='create':
			self.setButtons(self.ui, invisible='s000-11, t000')


		if self.hotBox.name=='init':
			self.ui.t000.viewport().setAutoFillBackground(False)
			self.ui.t000.setTextBackgroundColor(QtGui.QColor(50, 50, 50))











#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------