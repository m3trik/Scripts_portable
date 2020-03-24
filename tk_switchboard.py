from __future__ import print_function
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

from pydoc import locate

import sys, os.path






# ------------------------------------------------
#	Manage Ui elements
# ------------------------------------------------
class __Switchboard(object):
	'''
	Get/set elements across modules using convenience methods.
	
	ui name/corresponding class name - should always be the same. (case insensitive)
	ui files are looked for in a sub dir named 'ui'.

	widget name/corresponding method name - need to be the same.
	custom widget modules are looked for in a sub directory named 'widgets'. The module name and custom widget class name need to be identical.

	structure:
	_sbDict = {	
		'<ui name>' : {
					'ui' : <ui object>,
					'uiLevel' : int,
					'class' : <Class>,
					'size' : [int, int]
					'widgetDict' : {
								'<widget name>':{
											'widget':<widget>,
											'signalInstance':<widget.signal>,
											'widgetType':'<widgetClassName>',
											'derivedType':'<derivedClassName>',
											'method':<method>,
											'prefix':'alphanumeric prefix',
											'docString':'method docString'
								}
					}
		}
		'name' : [string list]} Ui history. Tracks the order in which the uis are called. A new ui is placed at element[-1]. ie. ['previousName2', 'previousName1', 'currentName']
		'prevCommand' : [list of 2 element lists] - Command history. ie. [[<b000>, 'multi-cut tool']]
		'prevCamera'  : [list of 2 element lists] - Camera history. ie. [[<v000>, 'camera: persp']]
		'mainAppWindow' : parent application. ie. <maya Window object>
		'gcProtect' : [items protected from garbage collection]
	}

	The widgetDict is built as needed for each class when __addSignal (or any other dependant method) is called.
	'''
	def __init__(self, sbDict):
		'''
		args:
			sbDict = main dictionary object.
		'''
		self._sbDict = sbDict



	def buildWidgetDict(self, name):
		'''
		Add the signal/slot connections for each widget in a given ui.

		The signals dict establishes what type widgets will be added to the widgetDict, and what associated signal to apply.
		Following that, the items in the ui are looped over, and the widgets' method resolution order is checked against the signals keys
		to determine the correct derived class type (used in the case of a custom widget).

		args:
			name (str) = name of the ui to construct connections for.
		returns:
			dict - 'objectName':{'widget':<widget>,'signalInstance':<signalInstance>,'method':<method>,'docString':'docString','widgetClassInstance':<class object>,'widgetClassName':'class name'}
		'''
		ui = self.getUi(name)

		for objectName, widget in ui.__dict__.items(): #for each object in the ui:
			self.addWidget(name, widget, objectName)

		# print(self.widgetDict(name))
		return self.widgetDict(name)



	def addWidgets(self, name, widgets, objectNames=[]):
		'''
		Extends the fuctionality of the 'addWidget' method to allow a list (of widgets) to be passed in.
		
		args:
			name (str) = name of the parent ui to construct connections for.
			widgets (list) = widget objects to be added.
			objectName (list) = widget string names.
		'''
		if objectNames and not len(widgets)==len(objectNames):
			raise Exception('# Error: The list of objectNames must be of equal length to that of the given widgets. #')

		for i, widget in enumerate(widgets):
			try:
				self.addWidget(name, widget, objectNames[i])
			except:
				self.addWidget(name, widget)



	def addWidget(self, name, widget, objectName=None):
		'''
		Adds a widget to the widgetDict under the given (ui) name.
		Decoupling this from 'buildWidgetDict' allows additional widgets to be added at any time.
		The signals dictionary provides both a way to set a default signal for a widget type.

		args:
			name (str) = name of the parent ui to construct connections for.
			widget (obj) = widget to be added.
			objectName (str) = widget's name.
		returns:
			<widget object>
		'''
		name = str(name) #prevent unicode

		if objectName:
			widget.setObjectName(objectName) #assure the widget has an object name.
		else:
			objectName = widget.objectName()


		n = name.split('_')[0] #get ie. 'polygons' from 'polygons_submenu' in cases where a submenu shares the same slot class of it's parent menu.
		# path = 'slots.{0}'.format(n[0].upper()+n[1:]) #ie. slots.Init
		path = 'tk_slots_{0}_{1}.{2}'.format(self.getMainAppWindow(objectName=True), n, n[0].upper()+n[1:]) #ie. tk_slots_maya_init.Init
		class_ = self.getClassInstance(path)



		signals = { #the default signal to be associated with each widget type.
			'QProgressBar':'valueChanged',
			'QPushButton':'released',
			'QToolButton':'triggered',
			'QListWidget':'itemClicked',
			'QTreeWidget':'itemClicked',
			'QAction':'triggered',
			'QSpinBox':'valueChanged',
			'QDoubleSpinBox':'valueChanged',
			'QCheckBox':'released',
			'QRadioButton':'released',
			'QComboBox':'currentIndexChanged',
			'QLineEdit':'returnPressed',
			'QTextEdit':'textChanged',
		}
		# print(widget.__class__.__mro__)
		for d in widget.__class__.__mro__: #get the directly derived class if a custom widget.
			if d.__module__=='PySide2.QtWidgets': #check for the first built-in class. Then use it as the derived class.
				derivedType = d.__name__
				break

		try: #if the widget type has a default signal assigned in the signals dict; get the signal.
			signal = signals[derivedType]
		except:
			signal = ''

		signalInstance = getattr(widget, signal, None) #add signal to widget. ie. signalInstance = widget.valueChanged
		method = getattr(class_, objectName, None) #use 'objectName' to get the corresponding method of the same name. ie. get method <b006> from widget 'b006' else None
		docString = getattr(method, '__doc__', None)
		prefix = self.prefix(objectName) #returns an string alphanumberic prefix if objectName startswith a series of alphanumberic chars, and is followed by three integers. ie. 'cmb' from 'cmb015'

		#add values to widgetDict
		self.widgetDict(name).update(
					{objectName:{'widget':widget, 
								'signalInstance':signalInstance,
								'widgetType':widget.__class__.__name__,
								'derivedType':derivedType,
								'method':method,
								'prefix':prefix,
								'docString':docString}})

		# print(self._sbDict[name]['widgetDict'][objectName]['widget'].objectName())
		return self._sbDict[name]['widgetDict'][objectName]['widget'] #return the stored widget.



	def widgetDict(self, name):
		'''
		Dictionary holding widget information.
		Used primarily by 'buildWidgetDict' method to construct signal and slot connections that can later be connected and disconnected by the add/__removeSignal methods.

		args:
			name (str) = name of ui/class. ie. 'polygons'
		returns:
			connection dict of given name with widget/method name string as key.
		ex.
		'widget':ui object.  ie. b001
		'signalInstance':ui object with signal attached. ie. b001.connect
		'method':class method object for the corresponding ui widget. ie. main.b001
		'docString': string description of command from method docString.  ie. 'Multi-Cut Tool'}
		#ie. {'b001':{'widget':b001, 'signalInstance':b001.onPressed, 'method':main.b001, 'docString':'Multi-Cut Tool'}},
		'''
		if not 'widgetDict' in self._sbDict[name]:
			self._sbDict[name]['widgetDict'] = {}
			self.buildWidgetDict(name) #construct the signals and slots for the ui

		return self._sbDict[name]['widgetDict']



	def setSignals(self, name):
		'''
		Replace any old signals with the set for the given name.
		'''
		# if not name in self.previousName(allowLevel0=True, allowDuplicates=1): #ie. 'polygons' not in 'polygons_submenu' (as they both share the same connections).
		# print('not ',name,' in ',self.previousName(allowLevel0=True, allowDuplicates=1))
		# print('setSignals:', self.previousName(allowLevel0=True, allowDuplicates=1, as_list=1))
		previousName = self.previousName(allowLevel0=True, allowDuplicates=1)
		if previousName:
			self.__removeSignal(previousName) #remove signals from the previous ui.
		self.__addSignal(name)



	def __addSignal(self, name):
		'''
		Connects signals/slots from the widgetDict for the given ui. Works with both single slots or multiple slots given as a list.

		args:
			name (str) = ui name
		'''
		for objectName in self.widgetDict(name):
			signal = self.getSignal(name, objectName)
			slot = self.getMethod(name, objectName)
			# print('__addSignal: ', name, objectName, signal, slot)
			if slot and signal:
				try:
					signal.connect(slot) #connect single slot (main and cameras)
				except:
					try:
						map(signal.connect, slot) #connect multiple slots from a list.

					except Exception as error:
						print('# Error: __addSignal:', name, objectName, error, signal, slot,'#') #, error



	def __removeSignal(self, name):
		'''
		Disconnects signals/slots from the widgetDict for the given ui. Works with both single slots or multiple slots given as a list.

		args:
			name (str) = ui name
		'''
		for objectName in self.widgetDict(name):
			signal = self.getSignal(name, objectName)
			slot = self.getMethod(name, objectName)
			# print('__removeSignal: ', name, objectName, signal, slot)
			if slot and signal:
				try:
					signal.disconnect(slot) #disconnect single slot (main and cameras)
				except:
					try:
						signal.disconnect() #disconnect all
						# map(signal.disconnect, slot) #disconnect multiple slots from a list.

					except Exception as error:
						print('# Error: __removeSignal:', name, objectName, error, signal, slot,'#') #, error



	def uiList(self, name=False, ui=False):
		'''
		Get a list of either all ui names, all ui object's, or both as key/value pairs in a dict.

		args:
			name (bool) = return string ui list
			ui (bool) =	return dynamic ui list
		returns:
			if name: return list of ui names
			if ui: return list of dynamic ui objects
			else: dict of ui names strings as keys, and corresponding ui objects as values. ie. {'ui name':<ui object>}
			'''
		if name:
			return [k for k,v in self._sbDict.items() if type(v)==dict and 'ui' in v]
		elif ui:
			return [v['ui'] for k,v in self._sbDict.items() if type(v)==dict and 'ui' in v]
		else:
			return {k:v['ui'] for k,v in self._sbDict.items() if type(v)==dict and 'ui' in v}



	def getUi(self, name=False):
		'''
		Get the dynamic ui using its string name, or if no argument is given, return the current ui.

		args:
			name (str) = name of class. ie. 'polygons' (by default getUi returns the current ui)
		returns:
			if name: corresponding dynamic ui object of given name from the key 'uiList'.
			else: current dynamic ui object
		'''
		if not name:
			n = self.getUiName()
			name = n[0].lower()+n[1:] #lowercase the first letter of name.

		try:
			return self._sbDict[name]['ui'] #self.uiList(ui=True)[self.getUiIndex(name)]
		except ValueError:
			return None



	def setUiName(self, index):
		'''
		The 'name' list is used for various things such as; maintaining a history of ui's that have been called previously.

		args:
			index (str) = name
				*or int - index of ui name
		returns:
			corresponding ui name as string
		'''
		if not 'name' in self._sbDict:
			self._sbDict['name'] = []

		if not type(index)==int:
			index = self.getUiIndex(index) #get index using name

		self._sbDict['name'].append(self.uiList(name=True)[index])

		return self._sbDict['name'][-1]



	def getUiName(self, ui=None):
		'''
		Get the ui name as a string.
		If no argument is given, the name for the current ui will be returned.

		args:
			ui = <ui object> - (optional) use ui object to get its corresponding name. (the default behavior is to return the current ui name)
		returns:
			'string' - ui name.
		'''
		if not 'name' in self._sbDict:
			self._sbDict['name'] = []

		if ui:
			return next(k for k, value in self.uiList().items() if value==ui)

		try:
			return self._sbDict['name'][-1]
		except: #if index out of range (no value exists): return None
			return None



	def getUiIndex(self, name=False):
		'''
		Get the index of the given ui name in the uiList.

		args:
			name (str) = name of class. ie. 'polygons'
		returns:
			if name: index of given name from the key 'uiList'.
			else: index of current ui
		'''
		
		if name:
			return self.uiList(name=True).index(name)
		else:
			return self.uiList(name=True).index(self.getUiName())



	def setUiSize(self, name=None, size=None): #store ui size.
		'''
		Set UI size.
		If no size is given, the minimum ui size needed to frame its
		contents will be used. If no name is given, the current ui will be used.

		args:
			name (str) = optional ui name
			size = [int, int] - optional width and height as an integer list. [width, height]
		returns:
			ui size info as integer values in a list. [width, hight]
		'''
		if not name:
			name = self.getUiName()

		if not size:
			ui = self.getUi(name)
			size = [ui.frameGeometry().width(), ui.frameGeometry().height()]

		self._sbDict[name]['size'] = size
		return self._sbDict[name]['size']



	def setUiSizeX(self, width, name=None):
		'''
		Set the X (width) value for the current ui.

		args:
			name (str) = the name of the ui to set the width for.
			width (int) = X size as an int
		'''
		height = self.getUiSize(name=name, height=True) #get the hight value.
		setUiSize(name=name, width=width, height=height)



	def setUiSizeY(self, height, name=None):
		'''
		Set the Y (height) value for the current ui.

		args:
			name (str) = the name of the ui to set the height for.
			height (int) = Y size as an int
		'''
		width = self.getUiSize(name=name, width=True) #get the width value.
		setUiSize(name=name, height=height, width=width)



	def getUiSize(self, name=None, width=None, percentWidth=None, height=None, percentHeight=None): #get current ui size info.
		'''
		Get the size info for each ui (allows for resizing a stacked widget where ordinarily resizing is constrained by the largest widget in the stack)

		args:
			name (str) = ui name to get size from.
			width (int) = returns width of current ui
			height (int) = returns hight of current ui
			percentWidth (int) = returns a percentage of the width
			percentHeight = int returns a percentage of the height
		returns:
			if width: returns width as int
			if height: returns height as int
			if percentWidth: returns the percentage of the width as an int
			if percentHeight: returns the percentage of the height as an int
			else: ui size info as integer values in a list. [width, hight]
		'''
		if not name:
			name = self.getUiName()

		if not 'size' in self._sbDict[name]:
			self.setUiSize(name)

		if width:
			return self._sbDict[name]['size'][0]
		elif height:
			return self._sbDict[name]['size'][1]
		elif percentWidth:
			return self._sbDict[name]['size'][0] *percentWidth /100
		elif percentHeight:
			return self._sbDict[name]['size'][1] *percentHeight /100
		else:
			return self._sbDict[name]['size']



	def getUiSizeX(self, name=None):
		'''
		Get the X (width) value for the current ui.

		args:
			name (str) = ui name to get size from.
		returns:
			returns width as int
		'''
		return self.getUiSize(name=name, width=True)



	def getUiSizeY(self, name=None):
		'''
		Get the Y (height) value for the current ui.

		args:
			name (str) = ui name to get size from.
		returns:
			returns width as int
		'''
		return self.getUiSize(name=name, height=True)



	def getNameFrom(self, obj):
		'''
		Get the ui name from any object existing in widgetDict.

		args:
			obj = <object> - 
		returns:
			 'string' - the corresponding method name from the given object.
			 ex. 'polygons' from <widget>
		'''
		for name, v in self._sbDict.iteritems():
			if type(v)==dict:
				for k, v in v.iteritems():
					if type(v)==dict:
						for k, v in v.iteritems():
							if type(v)==dict:
								for k, v in v.iteritems():
									if v==obj:
										return name



	def setMainAppWindow(self, app):
		'''
		Set parent application.

		args:
			app = app object.
		returns:
			string name of app
		'''
		self._sbDict['mainAppWindow'] = app

		return self._sbDict['mainAppWindow']



	def getMainAppWindow(self, objectName=False):
		'''
		Get parent application if any.

		args:
			objectName (bool) = get string name of app. (by default getMainAppWindow returns app object)
		returns:
			app object or string name
		'''
		if not 'mainAppWindow' in self._sbDict:
			self._sbDict['mainAppWindow'] = None
		
		app = self._sbDict['mainAppWindow']

		if objectName:
			if not app: #if app is None, return an empty string value.
				return ''
			else: #remove 'Window' from objectName ie. 'Maya' from 'MayaWindow' and set lowercase.
				name = app.objectName().rstrip('Window')
				return name[0].lower()+name[1:] #lowercase the first letter.
		else:
			return app



	def setClassInstance(self, class_, name=None):
		'''
		Case insensitive. Class string keys are stored lowercase regardless of how they are recieved.

		args:
			class_ (str)(obj) = module name.class to import and store class. 
					ie.  ie. 'polygons', 'tk_slots_max_polygons.Polygons', or <tk_slots_max_polygons.Polygons>
			name (str) = optional name key to store the class under (else the class name will be used).
		returns:
			class object.
		'''
		if type(class_)==str or type(class_)==unicode: #if arg given as string or unicode:
			name = class_.split('_')[-1].split('.')[-1] #get key from the class_ string ie. 'class' from 'module.Class'
			class_ = locate(class_)
		elif not name:
			name = class_.__class__.__name__ #if arg as <object>:

		name = name[0].lower()+name[1:] #lowercase the first letter.

		if not name in self._sbDict:
			self._sbDict[name] = {}

		if callable(class_):
			self._sbDict[name]['class'] = class_()
		else:
			self._sbDict[name]['class'] = class_


		return self._sbDict[name]['class']



	def getClassInstance(self, class_):
		'''
		Case insensitive. (Class string keys are lowercase and any given string will be converted automatically)
		If class is not in self._sbDict, getClassInstance will attempt to use setClassInstance() to first store the class.

		args:
			class_ (str)(obj) = module name.class to import and store class.
				ie. 'polygons', 'tk_slots_max_polygons.Polygons', or <tk_slots_max_polygons.Polygons>
		returns:
			class object.
		'''
		if type(class_)==str or type(class_)==unicode: #if arg given as string or unicode:
			name = class_.split('_')[-1].split('.')[-1] #get key from class_ string ie. 'class' from 'module.Class'#class_.lower()
		else: #if arg as <object>:
			if not callable(class_):
				return None
			name = class_.__class__.__name__

		name = name[0].lower()+name[1:] #lowercase the first letter.

		if not 'class' in self._sbDict[name]:
			return self.setClassInstance(class_) #construct the signals and slots for the ui

		return self._sbDict[name]['class']



	def getWidget(self, objectName=None, name=None):
		'''
		Case insensitive. Get the widget object/s from the given ui or widget name.

		args:
			name (str) = name of ui. ie. 'polygons'. If no name is given, the current ui will be used.
			objectName (str) = optional name of widget. ie. 'b000'
		returns:
			if objectName:  widget object with the given name from the current ui.
			if name and objectName: widget object with the given name from the given ui name.
			if name: all widgets for the given ui.
		'''
		if not name:
			name = self.getUiName()

		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui

		if objectName:
			return self._sbDict[name]['widgetDict'][objectName]['widget']
		else: #return all widgets:
			return [self._sbDict[name]['widgetDict'][objectName]['widget'] for objectName in self._sbDict[name]['widgetDict']]



	def getWidgets(self, name=None):
		'''
		Get all widgets for a ui.

		args:
			name (str) = name of ui. ie. 'polygons'. If no name is given, the current ui will be used.
		'''
		self.getWidget(name=name)



	def getWidgetType(self, widget, name=None):
		'''
		Get widget type class name as a string.
		ie. 'QPushButton' from pushbutton type widget.

		args:
			widget = 'string'  - name of widget/widget
				*or <object> -widget
			name (str) = name of dynamic ui (else use current ui)
		returns:
			'string' - the corresponding widget class name
		'''
		if not type(widget)==str:
			widget = widget.objectName() #use the objectName to get a string key for 'widget'

		if not name:
			name = self.getUiName()

		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui
		# print(name, widget)
		try:
			return self._sbDict[name]['widgetDict'][widget]['widgetType']
		except KeyError:
			return None



	def getDerivedType(self, widget, name=None):
		'''
		Get widget derived type class name as a string.
		ie. 'QPushButton' from a custom subclassed pushbutton.

		args:
			widget = 'string'  - name of widget/widget
				*or <object> - widget
			name (str) = name of dynamic ui (else use current ui)
		returns:
			'string' - the corresponding widget derived class name
		'''
		if not type(widget)==str:
			w = widget.objectName() #use the objectName to get a string key for 'widget'
			if not w:
				raise Exception('# Error: No object name found for '+str(widget)+' #')
			else:
				widget = w

		if not name:
			name = self.getUiName()

		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui

		return self._sbDict[name]['widgetDict'][widget]['derivedType']



	def getMethod(self, name, methodName=None):
		'''
		args:
			name (str) = name of class. ie. 'polygons'
			methodName (str) = optional name of method. ie. 'b001'
		returns:
			if methodName: corresponding method object to given method name string.
			else: all of the methods associated with the given name as a list.
		ex. sb.getMethod('polygons', 'b022')() #call method 'b022' of the 'polygons' class
		'''
		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui
		
		if methodName:
			try:
				return self._sbDict[name]['widgetDict'][methodName]['method'][0] #if there are event filters attached (ie. a list), just get the method.
			except:
				return  self._sbDict[name]['widgetDict'][methodName]['method']
		else:
			return [self._sbDict[name]['widgetDict'][methodName]['method'] for methodName in self._sbDict[name]['widgetDict']]



	def getSignal(self, name, objectName=None):
		'''
		args:
			name (str) = name of ui. ie. 'polygons'
			objectName (str) = optional widget name. ie. 'b001'
		returns:
			if objectName: the corresponding widget object with attached signal (ie. b001.onPressed) of the given widget name.
			else: all of the signals associated with the given name as a list.
		'''
		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui

		if objectName:
			return self._sbDict[name]['widgetDict'][objectName]['signalInstance']
		else:
			return [self._sbDict[name]['widgetDict'][objectName]['signalInstance'] for objectName in self._sbDict[name]['widgetDict']]



	def getDocString(self, name, methodName, all_=False):
		'''
		args:
			name (str) = optional name of class. ie. 'polygons'. else, use current name.
			methodName (str) = name of method. ie. 'b001'
			all_ = bool return entire unedited docString
		returns:
			if all_: the entire stored docString
			else: edited docString; name of method
		'''
		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui

		docString = self._sbDict[name]['widgetDict'][methodName]['docString']
		if docString and not all_:
			return docString.strip('\n\t') #return formatted docString
		else:
			return docString #return entire unformatted docString, or 'None' is docString==None.



	def previousName(self, previousIndex=False, allowDuplicates=False, allowLevel0=False, allowLevel1=True, allowLevel2=True, allowCurrent=False, as_list=False):
		'''
		Get the previously called ui name string, or a list of ui name strings ordered by use.
		It does so by pulling from the 'name' list which keeps a list of the ui names as they are called. ie. ['previousName2', 'previousName1', 'currentName']

		args:
			previousIndex (bool) = return the index of the last valid previously opened ui name.
			allowDuplicates (bool) = applicable when returning as_list. Returns the list allowing for duplicate names.
			allowLevel0 (bool) = allow instances of init menu in the results. Default is Off.
			allowLevel1 (bool) = allow instances of base level menus in the results. Default is On.
			allowLevel2 (bool) = allow instances of submenu's in the results. Default is On.
			allowCurrent (bool) = allow the currentName. Default is off.
			as_list (bool) = returns the full list of previously called names. By default duplicates are removed.
		returns:
			with no arguments given - string name of previously opened ui.
			if previousIndex: int - index of previously opened ui
			if as_list: returns [list of string names]
		'''
		if not 'name' in self._sbDict:
			self._sbDict['name'] = []

		self._sbDict['name'] = self._sbDict['name'][-200:] #keep original list length restricted to last 200 elements

		list_ = self._sbDict['name'] #work on a copy of the list, keeping the original intact

		if not allowCurrent:
			list_ = list_[:-1] #remove the last index. (currentName)

		if not allowLevel0:
			list_ = [i for i in list_ if not self.getUiLevel(i)==0] #remove 'init' menu.

		if not allowLevel1:
			list_ = [i for i in list_ if not self.getUiLevel(i)==1] #remove base level menus.

		if not allowLevel2:
			list_ = [i for i in list_ if not self.getUiLevel(i)==2] #remove any submenus.

		if not allowDuplicates:
			[list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous duplicates if they exist; keeping the last added element.

		if previousIndex:
			validPrevious = [i for i in list_ if all(['cameras' not in i, 'main' not in i])]
			return self.getUiIndex(validPrevious[-2])

		elif as_list:
			return list_ #return entire list after being modified by any flags such as 'allowDuplicates'.

		else:
			try:
				return list_[-1] #return the previous ui name if one exists.
			except:
				return ''



	def prevCommand(self, docString=False, method=False, as_list=False):
		'''
		args:
			docString (bool) = return the docString of last command. Default is off.
			method (bool) = return the method of last command. Default is off.
		returns:
			if docString: 'string' description (derived from the last used command method's docString) (as_list: [string list] all docStrings, in order of use)
			if method: method of last used command. (as_list: [<method object> list} all methods, in order of use)
			if as_list: list of lists with <method object> as first element and <docString> as second. ie. [[b001, 'multi-cut tool']]
			else : <method object> of the last used command
		'''
		if not 'prevCommand' in self._sbDict:
			self._sbDict['prevCommand'] = [] #initialize list

		self._sbDict['prevCommand'] = self._sbDict['prevCommand'][-20:] #keep original list length restricted to last 20 elements

		list_ = self._sbDict['prevCommand']
		[list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous duplicates if they exist; keeping the last added element.

		if as_list:
			if docString and not method:
				try:
					return [i[1] for i in list_]
				except:
					return None
			elif method and not docString:
				try:
					return [i[0] for i in list_]
				except:
					return ['# No commands in history. #']
			else:
				return list_

		elif docString:
			try:
				return list_[-1][1]
			except:
				return ''

		else:
			try:
				return list_[-1][0]
			except:
				return None



	def prevCamera(self, docString=False, method=False, allowCurrent=False, as_list=False):
		'''
		args:
			docString (bool) = return the docString of last camera command. Default is off.
			method (bool) = return the method of last camera command. Default is off.
			allowCurrent (bool) = allow the current camera. Default is off.
		returns:
			if docString: 'string' description (derived from the last used camera command's docString) (as_list: [string list] all docStrings, in order of use)
			if method: method of last used camera command. (as_list: [<method object> list} all methods, in order of use)
			if as_list: list of lists with <method object> as first element and <docString> as second. ie. [[<v001>, 'camera: persp']]
			else : <method object> of the last used command
		'''
		if not 'prevCamera' in self._sbDict:
			self._sbDict['prevCamera'] = [] #initialize list

		self._sbDict['prevCamera'] = self._sbDict['prevCamera'][-20:] #keep original list length restricted to last 20 elements

		list_ = self._sbDict['prevCamera']
		[list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous duplicates if they exist; keeping the last added element.

		if not allowCurrent:
			list_ = list_[:-1] #remove the last index. (currentName)

		if as_list:
			if docString and not method:
				try:
					return [i[1] for i in list_]
				except:
					return None
			elif method and not docString:
				try:
					return [i[0] for i in list_]
				except:
					return ['# No commands in history. #']
			else:
				return list_

		elif docString:
			try:
				return list_[-1][1]
			except:
				return ''

		else:
			try:
				return list_[-1][0]
			except:
				return None



	def gcProtect(self, obj=None):
		'''
		Protect given object from garbage collection.

		args:
			obj = <object>
		returns:
			list of protected objects.
		'''
		if not 'gcProtect' in self._sbDict:
			self._sbDict['gcProtect']=[]

		if obj and obj not in self._sbDict['gcProtect']:
				self._sbDict['gcProtect'].append(obj)

		return self._sbDict['gcProtect']



	def dict_(self):
		'''
		returns:
			full switchboard dict
		'''
		return self._sbDict



	def hasKey(self, *args): #check if key exists in switchboard dict.
		'''
		ie. hasKey('polygons', 'widgetDict', 'objectName')

		args:
			'string' dict keys in order of hierarchy.  ie. 'polygons', 'widgetDict', 'b001', 'method'
		returns:
			bool
		'''
		if len(args)==1:
			if args[0] in self._sbDict:
				return True

		elif len(args)==2:
			if args[1] in self._sbDict[args[0]]:
				return True

		elif len(args)==3:
			if args[2] in self._sbDict[args[0]][args[1]]:
				return True

		elif len(args)==4:
			if args[3] in self._sbDict[args[0]][args[1]][args[2]]:
				return True
		else:
			return False



	def getSubmenu(self, ui):
		'''
		Get the submenu object of the given ui using it's name string, or the parent ui object.

		args:
			ui (str) = ui name.
				<ui object> - dynamic ui.
		'''
		if type(ui)==str: #get name using string.
			name = ui+'_submenu'
		else: #get name using ui object.
			name = self.getUiName(ui)+'_submenu'

		return self.getUi(name)



	def getUiLevel(self, name=False):
		'''
		Get the hierarcical level of a ui from its string name.
		If no argument is given, the level of current ui will be returned.

		level 0: init (root) (parent class)
		level 1: base_menus
		level 2: sub_menus
		level 3: main_menus

		args:
			name (str) = ui name to get level of. ie. 'polygons'
		returns:
			ui level as an integer.
		'''
		if not name:
			name = self.getUiName()
			name = name[0].lower()+name[1:] #lowercase the first letter of name.

		try:
			return self._sbDict[name]['uiLevel']
		except ValueError:
			return None



	def prefix(self, objectName, prefix=None):
		'''
		Checks if the given objectName startswith an alphanumeric prefix, followed by three integers. ex. i000 (alphanum,int,int,int)
		and if so, returns the alphanumberic prefix.
		ex. prefix('i023') returns 'i'
		if second prefix arg is given, then the method checks if the given objectName has the prefix, and the return value is bool.

		args:
			objectName (str) = string to check against.
			prefix (str) = optional; check if the given objectName startwith this prefix.
		returns:
			if prefix arg given:
				bool - True if correct format else, False.
			else:
				alphanumeric 'string' 
		'''
		if prefix: #check the actual prefix against the given prefix and return bool.
			name = self.getUiName()
			try:
				prefix1 = self._sbDict[name]['widgetDict'][objectName]['prefix']
				if prefix1==prefix:
					return True

			except KeyError:
				if objectName.startswith(prefix):
					i = len(prefix)
					integers = [c for c in objectName[i:i+3] if c.isdigit()]
					if len(integers)>2 or len(objectName)==i:
						return True

			return False

		else: #return prefix.
			prefix=''
			for char in objectName:
				if not char.isdigit():
					prefix = prefix+char
				else:
					break

			i = len(prefix)
			integers = [c for c in objectName[i:i+3] if c.isdigit()]
			if len(integers)>2 or len(objectName)==i:
				return prefix



	@staticmethod
	def qApp_getWindow(name=None):
		'''
		Get Qt window/s

		args:
			name (str) = optional name of window (widget.objectName)
		returns:
			if name: corresponding <window object>
			else: return a dictionary of all windows {windowName:window}
		'''
		windows = {w.objectName():w for w in QApplication.allWindows()}
		if name:
			return windows[name]
		else:
			return windows



	@staticmethod
	def qApp_getWidget(name=None):
		'''
		Get Qt widget/s

		args:
			name (str) = optional name of widget (widget.objectName)
		returns:
			if name: corresponding <widget object>
			else: return a dictionary of all widgets {objectName:widget}
		'''
		widgets = {w.objectName():w for w in QApplication.allWidgets()}
		if name:
			return widgets[name]
		else:
			return widgets



	#set properties
	name = property(getUiName, setUiName)
	prevName = property(previousName)
	ui = property(getUi)
	uiIndex = property(getUiIndex)
	uiLevel = property(getUiLevel)
	size = property(getUiSize, setUiSize)
	sizeX = property(getUiSizeX, setUiSizeX)
	sizeY = property(getUiSizeY, setUiSizeY)
	class_ = property(getClassInstance, setClassInstance)
	mainAppWindow = property(getMainAppWindow, setMainAppWindow)
	getWidgets = property(getWidget)





# ------------------------------------------------------------------------------------------


#initialize and create a __Switchboard instance
app = QApplication.instance() #get the app instance if it exists (required by the QUiLoader)
if not app:
	app = QApplication(sys.argv)


global uiLoader, widgetPath, uiPath
uiLoader = QUiLoader()

# register any custom widgets.
# get path to the widget directory.
widgetPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'widgets')
# format names using the files in path.
moduleNames = [file_.replace('.py','',-1) for file_ in os.listdir(widgetPath) if file_.startswith('q') and file_.endswith('.py')]
# register any custom widgets using the module names.
for m in moduleNames:
	className = m[:1].capitalize()+m[1:] #capitalize first letter of module name to convert to class name
	path = 'widgets.{0}.{1}'.format(m, className)
	class_ = locate(path)
	if class_:
		uiLoader.registerCustomWidget(class_)
	else:
		raise ImportError, path


# set path to the directory containing the ui files.
uiPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui') #get absolute path from dir of this module + relative path to directory
# initialize _sbDict by loading and setting keys for the ui files.
_sbDict={}
for dirpath, dirnames, filenames in os.walk(uiPath):
	for filename in (f for f in filenames if f.endswith(".ui")):
		path = os.path.join(dirpath, filename)
		name = filename.replace('.ui','')
		d = dirpath[dirpath.rfind('ui\\'):] #slice the absolute path from 'ui\' ie. ui\base_menus_1\sub_menus_2\main_menus_3 from fullpath\ui\base_menus_1\sub_menus_2\main_menus_3
		_sbDict[filename.replace('.ui','')] = {'ui':uiLoader.load(path), 'uiLevel':len(d.split('\\'))-1} #ie. {'polygons':{'ui':<ui obj>, uiLevel:<int>}} (the ui level is it's hierarchy)


sb = __Switchboard(_sbDict)







#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

'''
test example:
_sbDict={
	'polygons':{'class': '<Polygons>',
				'ui': '<polygons ui object>',
				'uiLevel': 3,
				'size': [210, 480],
				'widgetDict': {'cmb002': {'widget': '<widgets.QComboBox_.QComboBox_ object at 0x0000016B6C078908>', 
									'widgetType': 'QComboBox_', 
									'derivedType': 'QComboBox', 
									'signalInstance': '<PySide2.QtCore.SignalInstance object at 0x0000016B62BC5780>',
									'prefix':'cmb', 
									'docString': '\n\t\tSelect All Of Type\n\t\t',
									'method': '<bound method Selection.cmb002 of <tk_slots_max_selection.Selection object at 0x0000016B6BC26470>>'}, }},
	'mainAppWindow': None,
	'name': ['polygons'],
	'prevCommand': [['b000', 'multi-cut tool']],
	'prevCamera:': [['v000', 'Viewport: Persp']],
	'gcProtect': ['<protected object>']}
'''




# deprecated: -----------------------------------

	
	# def getPrevNameList_wDuplicates(self):
	# 	'''
	# 	Get previous names as a list (containing duplicates).

	# 	returns:
	# 		list
	# 	'''
	# 	return self.previousName(as_list=True, allowDuplicates=True)



	# def getPrevNameList_woDuplicates(self):
	# 	'''
	# 	Get previous names as a list (duplicates removed).

	# 	returns:
	# 		list
	# 	'''
	# 	return self.previousName(allowLevel0=1, as_list=1)