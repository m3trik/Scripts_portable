from __future__ import print_function
from PySide2 import QtCore
import os.path, sys






class Slots(QtCore.QObject):
	'''
	Parent class for all slot type classes.

	If you need to create a invokable method that returns some value, declare it as a slot, e.g.:
	@Slot(result=int, float)
	def getFloatReturnInt(self, f):
		return int(f)
	'''
	def __init__(self, parent=None, *args, **kwargs):
		super(Slots, self).__init__(parent)
		'''
		'''
		for k,v in kwargs.items():
			setattr(self, k, v)


	@property
	def currentUi(self):
		'''
		Get the current Ui.
		'''
		# print ('ui', self.sb.getUiName(self.ui)) #same as current ui
		# print ('currentUi:', self.sb.getUiName(self.sb.getUi()))
		return self.sb.getUi() #current

	@property
	def parentUi(self):
		'''
		Get the calling module's top level Ui.
		'''
		# print ('parentUi:', self.sb.getUiName(self.sb.getUi(level=3)))
		caller = sys._getframe(1)  # Obtain calling frame
		callingModule = caller.f_globals['__name__']
		name = callingModule.split('_')[-1] #get name from the module name.
		return self.sb.getUi(name, level=3) #main_menu

	@property
	def childUi(self):
		'''
		Get the calling module's submenu.
		'''
		# print ('submenu:', self.sb.getUiName(self.sb.getUi(level=2)))
		caller = sys._getframe(1)  # Obtain calling frame
		callingModule = caller.f_globals['__name__']
		name = callingModule.split('_')[-1] #get name from the module name.
		return self.sb.getUi(name, level=2) #submenu


	# @classmethod
	# def progress(cls, fn):
	# 	'''
	# 	Decorator that populates a messageBox with the string returned by the given function.
	# 	'''
	# 	def wrapper(self, *args, **kwargs):
	# 		self.progressBar(fn(self, *args, **kwargs))
	# 	return wrapper


	def progressBar(self):
		'''
		'''
		if not hasattr(self, '_progressBar'):
			from widgets.qProgressBar_ import QProgressBar_
			self._progressBar = QProgressBar_(self.tk)

		try:
			self.currentUi.progressBar.step1
		except AttributeError:
			pass

		# self._progressBar

		return self._progressBar


	@classmethod
	def message(cls, fn):
		'''
		Decorator that populates a messageBox with the string returned by the given function.
		'''
		def wrapper(self, *args, **kwargs):
			self.messageBox(fn(self, *args, **kwargs))
		return wrapper


	def messageBox(self, string, location='topMiddle', timeout=1):
		'''
		Spawns a message box with the given text.
		Prints a formatted version of the given string, stripped of html tags, to the console.

		args:
			location (str)(point) = move the messagebox to the specified location. Can be given as a qpoint or string value. default is: 'topMiddle'
			timeout (int) = time in seconds before the messagebox auto closes.
		'''
		if not hasattr(self, '_messageBox'):
			from widgets.qMessageBox_ import QMessageBox_
			self._messageBox = QMessageBox_(self.tk.parent())

		self._messageBox.location = location
		self._messageBox.timeout = timeout

		if isinstance(string, (str, unicode)):
			from re import sub
			print(''+sub('<.*?>', '', string)+'') #strip everything between '<' and '>' (html tags)

			self._messageBox.setText(string)
			self._messageBox.exec_()


	def getObjects(self, class_, objectNames, showError_=False):
		'''
		Get a list of corresponding objects from a single string.
		ie. 's000,b002,cmb011-15' would return object list: [<s000>, <b002>, <cmb011>, <cmb012>, <cmb013>, <cmb014>, <cmb015>]

		args:
			class_ (obj) = Class object
			objectNames (str) = Names separated by ','. ie. 's000,b004-7'. b004-7 specifies buttons b004-b007.  
			showError (bool) = Show attribute error if item doesnt exist

		returns:
			(list) of corresponding objects

		#ex call: getObjects(self.ui, 's000,b002,cmb011-15')
		'''
		objects=[]
		for name in Slots.unpackNames(objectNames):
			try:
				objects.append(getattr(class_, name)) #equivilent to:(self.ui.m000)
			except Exception as error: 
				if showError_:
					print(error)
				else: pass
		return objects


	def callMethod(self, name, method, *args, **kwargs):
		'''
		Call a method from a class outside of the current ui.
		Momentarily switches to the ui of the given method for the call, before returning to the previous ui.

		args:
			name (str) = ui name.
			method (str) = method name.
		'''
		ui = self.sb.getUi()
		temp = self.tk.setUi(name)
		method = self.sb.getMethod(name, method)

		try:
			method(*args, **kwargs)
		except Exception as error:
			print(error)

		self.tk.setUi(ui)


	def connect_(self, widgets, signals, slots, class_=None):
		'''
		Connect multiple signals to multiple slots at once.

		args:
			widgets (str)(obj)(list) = ie. 'chk000-2' or [tb.chk000, tb.chk001]
			signals (str)(list) = ie. 'toggled' or [toggled]
			slots (obj)(list) = ie. self.cmb002 or [self.cmb002]
			class_ (obj)(list) = if the widgets arg is given as a string, then the class_ it belongs to can be explicitly given. else, the current ui will be used.

		ex call: self.connect_('chk000-2', 'toggled', self.cmb002, tb) *or self.connect_([tb.chk000, tb.chk001], 'toggled', self.cmb002)
		'''
		if isinstance(widgets, (str,unicode)):
			try:
				widgets = self.getObjects(class_, widgets, showError_=True) #getObjects returns a widget list from a string of objectNames.
			except:
				widgets = self.getObjects(self.sb.getUi(), widgets, showError_=True)

		#if the variables are not of a list type; convert them.
		widgets = self.sb.list_(widgets)
		signals = self.sb.list_(signals)
		slots = self.sb.list_(slots)

		for widget in widgets:
			for signal in signals:
				signal = getattr(widget, signal)
				for slot in slots:
					signal.connect(slot)


	def toggleWidgets(self, *args, **kwargs):
		'''
		Set multiple boolean properties, for multiple widgets, on multiple ui's at once.
		If the ui has a submenu with the same widget, then the value will be set there as well. It can be set on additional ui's by passing them in explicitly in *args.
		args:
			*args = dynamic ui object/s
			*kwargs = keyword: - the property to modify. ex. setChecked, setUnChecked, setEnabled, setDisabled, setVisible, setHidden
								Optionally appending '_False' or '_True' to the attribute name, will set the attribute accordingly. (The default state is True)
					argument: string of objectNames - objectNames separated by ',' ie. 'b000-12,b022'

		ex.	self.toggleWidgets(self.ui1, self.ui2, setDisabled='b000', setUnChecked='chk009-12', setVisible='b015,b017')
		'''
		for ui in args:
			for property_ in kwargs: #ie. property_ could be setUnChecked
				widgets = self.getObjects(ui, kwargs[property_]) #getObjects returns a widget list from a string of objectNames.

				state = True
				if 'Un' in property_: #set state to False if '_False' is appended to the keyword.
					property_ = property_.replace('Un', '')
					state = False

				[getattr(w, property_)(state) for w in widgets] #set the property state for each widget in the list.


	def setAxisForCheckBoxes(self, checkboxes, axis, ui=None):
		'''
		Set the given checkbox's check states to reflect the specified axis.

		args:
			checkboxes (str)(list) = 3 or 4 (or six with explicit negative values) checkboxes.
			axis (str) = Axis to set. Valid text: '-','X','Y','Z','-X','-Y','-Z' ('-' indicates a negative axis in a four checkbox setup)

		ex call: self.setAxisForCheckBoxes('chk000-3', '-X') #optional ui arg for the checkboxes
		'''
		if isinstance(checkboxes, (str, unicode)):
			if ui is None:
				ui = self.currentUi
			checkboxes = self.getObjects(ui, checkboxes)

		prefix = '-' if '-' in axis else '' #separate the prefix and axis
		coord = axis.strip('-')

		for chk in checkboxes:
			if any([chk.text()==prefix, chk.text()==coord, chk.text()==prefix+coord]):
				chk.setChecked(True)


	def getAxisFromCheckBoxes(self, checkboxes, ui=None):
		'''
		Get the intended axis value as a string from the given checkbox's check states.

		args:
			checkboxes (str)(list) = 3 or 4 (or six with explicit negative values) checkboxes. Valid text: '-','X','Y','Z','-X','-Y','-Z' ('-' indicates a negative axis in a four checkbox setup)

		ex call: self.getAxisFromCheckBoxes('chk000-3')
		'''
		if isinstance(checkboxes, (str, unicode)):
			if ui is None:
				ui = self.currentUi
			checkboxes = self.getObjects(ui, checkboxes, showError_=1)

		prefix=axis=''
		for chk in checkboxes:
			if chk.isChecked():
				if chk.text()=='-':
					prefix = '-'
				else:
					axis = chk.text()

		return prefix+axis #ie. '-X'


	def setSpinboxes(self, ui, spinboxes, attributes={}):
		'''
		Set multiple spinbox values.
		args:
			ui = <dynamic ui>
			spinboxes (str)(list) = Packed spinbox names or object list. ie. 's001-4, s007' or [<s001>, <s002>, <s003>, <s004>, <s007>]
			attributes = {'string key':value}

		ex. self.setSpinboxes (self.ui, spinboxNames='s000-15', attributes={'width':1, 'length ratio':1, 'patches U':1, 'patches V':1})
		ex. self.setSpinboxes (self.ui, spinboxNames='s000', attributes={'size':5} #explicit;  set single s000 with a label 'size' and value of 5
		'''
		if isinstance(spinboxes, (str, unicode)):
			spinboxes = self.getObjects(ui, spinboxes) #get spinbox objects

		#clear previous values
		for spinbox in spinboxes:
			spinbox.blockSignals(True)
			# spinbox.setEnabled(False)

		#set values
		for index, (key, value) in enumerate(attributes.items()):
			if isinstance(value, float):
				if value<0: spinboxes[index].setMinimum(-100)
				decimals = str(value)[::-1].find('.') #get decimal places
				spinboxes[index].setDecimals(decimals)
				spinboxes[index].setPrefix(key+': ')
				spinboxes[index].setValue(value)
				spinboxes[index].setSuffix('')

			elif isinstance(value, int):
				if value<0: spinboxes[index].setMinimum(-100)
				spinboxes[index].setDecimals(0)
				spinboxes[index].setPrefix(key+': ')
				spinboxes[index].setValue(value)
				spinboxes[index].setSuffix('')

			elif isinstance(value, bool):
				value = int(value)
				spinboxes[index].setMinimum(0)
				spinboxes[index].setMaximum(1)
				spinboxes[index].setSuffix('<bool>')

			# spinboxes[index].setEnabled(True)
			spinboxes[index].blockSignals(False)


	@staticmethod
	def getAttributes(node, exclude=None):
		'''
		Get existing node attributes.
		args:
			node = object
			exclude = 'string list' - attributes to exclude from returned dictionay

		returns:
			dictionary {'string attribute': value}
		'''
		return {attr:getattr(node, attr) for attr in dir(node) if attr not in exclude}


	@staticmethod
	def setAttributes(node, attributes):
		'''
		Set node attributes.
		args:
			node = object
			attributes = dictionary {'string attribute': value} - attributes and their correponding value to set
		'''
		[setattr(node, attr, value) for attr, value in attributes.iteritems() if attr and value]


	global cycleDict
	cycleDict={}
	@staticmethod
	def cycle(sequence, name=None, query=False):
		'''
		Toggle between numbers in a given sequence.
		Used for maintaining toggling sequences for multiple objects simultaniously.
		Each time this function is called, it returns the next number in the sequence
		using the name string as an identifier key.
		
		args:
			sequence (list) = sequence to cycle through. ie. [1,2,3].
			name (str) = identifier. used as a key to get the sequence value from the dict.
			
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
	def unpackNames(nameString):
		'''
		Get a list of individual names from a single name string.
		If you are looking to get multiple objects from a name string, call 'getObjects' directly instead.

		args:
			nameString = string consisting of widget names separated by commas. ie. 'v000, b004-6'

		returns:
			unpacked names. ie. ['v000','b004','b005','b006']
		'''
		packed_names = [n.strip() for n in nameString.split(',') if '-' in n] #build list of all widgets passed in containing '-'
		otherNames = [n.strip() for n in nameString.split(',') if '-' not in n] #all widgets passed in not containing '-'

		unpacked_names=[] #unpack the packed names:
		for name in packed_names:
			name = name.split('-') #ex. split 'b000-8'
			prefix = name[0].strip('0123456789') #ex. split 'b' from 'b000'
			start = int(name[0].strip('abcdefghijklmnopqrstuvwxyz') or 0) #start range. #ex. '000' #converting int('000') returns None, if case; assign 0.
			stop = int(name[1])+1 #end range. #ex. '8' from 'b000-8' becomes 9, for range up to 9 but not including 9.
			unpacked_names.extend([str(prefix)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)]) #build list of name strings within given range

		return otherNames+unpacked_names


	@staticmethod
	def collapseList(list_, limit=None):
		'''
		Convert a list of integers to a collapsed sequential string format.
		ie. [19,22,23,24,25,26] to ['19', '22..26']

		args:
			list_ (list) = of integers

		returns:
			(list)
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

		if limit and len(collapsedList)>limit:
			l = collapsedList[:limit]
			l.append('...')
			return l
		else:
			return collapsedList









#module name
print (os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------


#depricated:

	# @staticmethod
	# def msg(string, prefix='', inView=False):
	# 	'''
	# 	args:
	# 		string (str) = message string.
	# 	returns:
	# 		(str) formatted string.
	# 	'''
	# 	if prefix:
	# 		prefix = prefix+':'
	# 	return '{}{}{}{}'.format('',prefix, string, '')


	# def getUiObject(self, widgets):
	# 	'''
	# 	Get ui objects from name strings.
	# 	args:
	# 		widgets (str) = ui object names
	# 	returns:
	# 		list of corresponding ui objects	
	# 	'''
	# 	objects=[]
	# 	for name in self.unpackNames(widgets):
	# 		try:
	# 			w = getattr(self.ui, name)
	# 			objects.append(w)
	# 		except: pass
	# 	return objects





	# def setButtons(self, ui, checked=None, unchecked=None, enable=None, disable=None, visible=None, invisible=None):
	# 	'''
	# 	Set various states for multiple buttons at once.
	# 	args:
	# 		setButtons = dynamic ui object
	# 		checked/unchecked/enable/disable/visible/invisible (str) = the names of buttons to modify separated by ','. ie. 'b000,b001,b022'

	# 	ex.	setButtons(self.ui, disable='b000', unchecked='chk009-12', invisible='b015')
	# 	'''
	# 	if checked:
	# 		checked = self.getObjects(ui, checked)
	# 		[button.setChecked(True) for button in checked]
			
	# 	if unchecked:
	# 		unchecked = self.getObjects(ui, unchecked)
	# 		[button.setChecked(False) for button in unchecked]
			
	# 	if enable:
	# 		enable = self.getObjects(ui, enable)
	# 		[button.setEnabled(True) for button in enable]
			
	# 	if disable:
	# 		disable = self.getObjects(ui, disable)
	# 		[button.setDisabled(True) for button in disable]
			
	# 	if visible:
	# 		visible = self.getObjects(ui, visible)
	# 		[button.setVisible(True) for button in visible]
			
	# 	if invisible:
	# 		invisible = self.getObjects(ui, invisible)
	# 		[button.setVisible(False) for button in invisible]




# def setSpinboxes(ui, spinboxNames='s000-15', values=[]):
# 	'''
# 	args:	 ui=<dynamic ui>
# 			 spinboxNames (str) = spinbox string object names (used in place of the range argument). ie. 's001-4, s007'.  
# 						  default value will try to add values to spinboxes starting at s000 and add values in order skipping any spinboxes not found in the ui.
# 			 values=int or [(tuple) list] - tuple representing a string prefix label and value, and/or just a value. [(string prefix,int value)] ie. [("size",5), 20, ("width",8)]
	
# 	returns: list of values without prefix
# 	ex. self.setSpinboxes (self.ui, values=[("width",1),("length ratio",1),("patches U",1),("patches V",1)]) #range. dict 'value's will be added to corresponding spinbox starting at s000 through s003.
# 	ex. self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',5)]) #explicit;  set single s000 with a label 'size' and value of 5. multiple spinboxes can be set this way. specify a range of spinboxes using 's010-18'.
# 	'''
# 	spinboxes = self.getObjects(ui, spinboxNames) #get spinbox objects

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
# 			spinboxes[i].setPrefix(value[0]+': ')
# 			spinboxes[i].setValue(value[1])
# 			values_.append(value[1])
# 		else:
# 			spinboxes[i].setValue(value)
# 			values_.append(value)
# 		spinboxes[i].blockSignals(False)

# 	return values_


# packed_names = [n.strip() for n in objectNames.split(',') if '-' in n] #build list of all objectNames passed in containing '-'

# 		unpacked_names=[]
# 		for name in packed_names:
# 			name=name.split('-') #ex. split 'b000-8'
# 			prefix = name[0].strip('0123456789') #ex. split 'b' from 'b000'
# 			start = int(name[0].strip('abcdefghijklmnopqrstuvwxyz') or 0) #start range. #ex. '000' #converting int('000') returns None, if case; assign 0.
# 			stop = int(name[1])+1 #end range. #ex. '9' from 'b000-8' for range up to 9 but not including 9.
# 			unpacked_names.extend([str(prefix)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)]) #build list of name strings within given range

# 		names = [n.strip() for n in objectNames.split(',') if '-' not in n] #all objectNames passed in not containing '-'
# 		if print_: print names+unpacked_names #used for debugging





	# @staticmethod
	# def comboBox(comboBox, items, title=None):
	# 	'''
	# 	Set comboBox items.
	# 	args:
	# 		comboBox = QComboBox object - list of items to fill the comboBox with
	# 		title (str) = optional value for the first index of the comboBox's list

	# 	returns:
	# 		comboBox's current item list minus any title.
	# 	ex. comboBox (self.ui.cmb003, ["Import file", "Import Options"], "Import")
	# 	'''
	# 	comboBox.blockSignals(True) #to keep clear from triggering currentIndexChanged
	# 	index = comboBox.currentIndex() #get current index before refreshing list
	# 	comboBox.clear()
		
	# 	items_ = [str(i) for i in [title]+items if i]
	# 	comboBox.addItems(items_) 

	# 	comboBox.setCurrentIndex(index)
	# 	comboBox.blockSignals(False)

	# 	return items_