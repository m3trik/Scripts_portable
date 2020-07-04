from __future__ import print_function
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

from pydoc import locate

import sys, os.path






# ------------------------------------------------
#	Manage Ui element information.
# ------------------------------------------------
class Switchboard(QtCore.QObject):
	'''
	Get/set elements across modules using convenience methods.
	
	Ui name/and it's corresponding slot class name should always be the same. (case insensitive) ie. 'polygons' (ui name) will look to build connections to 'Polygons' (class name). 
	Widget ovjectName/corresponding class method name need to be the same. ie. 'b000' (widget objectName) will try to connect to <b000> class method.

	Ui files are looked for in a sub dir named 'ui'. naming convention is: <ui name>.ui ie. polygons.ui
	Custom widget modules are looked for in a sub directory named 'widgets'. naming convention: <name capital first char> widget class inside <name lowercase first char>.py module. ie. QLabel_ class inside qLabel_.py module.

	nested dictionary structure:
	_sbDict = {	
		'<ui name>' : {
					'ui' : <ui object>,
					'uiLevel' : int,
					'class' : <Class>,
					'size' : [int, int]
					'widgets' : {
								'<widget>':{
											'widgetName':'objectName',
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

	A widgets dict is built as needed for each class when connectSlots (or any other dependant) is called.
	'''

	def __init__(self, parent):
		'''
		Initialize the main dict (_sbDict).
		'''
		self.parent = parent

		uiLoader = QUiLoader()

		# register any custom widgets.
		widgetPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'widgets') #get the path to the widget directory.
		moduleNames = [file_.replace('.py','',-1) for file_ in os.listdir(widgetPath) if file_.startswith('q') and file_.endswith('.py')] #format names using the files in path.
		for m in moduleNames: #register any custom widgets using the module names.
			className = m[:1].capitalize()+m[1:] #capitalize first letter of module name to convert to class name
			path = 'widgets.{0}.{1}'.format(m, className)
			class_ = locate(path)
			if class_:
				uiLoader.registerCustomWidget(class_)
			else:
				raise ImportError, path

		# get the path to the directory containing the ui files.
		uiPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui') #get absolute path from dir of this module + relative path to directory

		# initialize _sbDict by setting keys for the ui files.
		for dirpath, dirnames, filenames in os.walk(uiPath):
			for filename in (f for f in filenames if f.endswith(".ui")):
				path = os.path.join(dirpath, filename)
				name = filename.replace('.ui','')
				d = dirpath[dirpath.rfind('ui\\'):] #slice the absolute path from 'ui\' ie. ui\base_menus_1\sub_menus_2\main_menus_3 from fullpath\ui\base_menus_1\sub_menus_2\main_menus_3
				self.sbDict[filename.replace('.ui','')] = {'ui':uiLoader.load(path), 'uiLevel':len(d.split('\\'))-1} #ie. {'polygons':{'ui':<ui obj>, uiLevel:<int>}} (the ui level is it's hierarchy)


	@property
	def sbDict(self):
		'''
		Get the full switchboard dict or one of it's values from a given key.
		'''
		if not hasattr(self, '_sbDict'):
			self._sbDict={}

		return self._sbDict


	def addWidgets(self, name, widgets=None, **kwargs):
		'''
		Extends the fuctionality of the 'addWidget' method to support adding multiple widgets.
		If widgets is None; the method will attempt to add all widgets from the ui of the given name.

		args:
			name (str) = name of the parent ui to construct connections for.
			widgets (list) = widget objects to be added. If none are given all objects from the ui will be added.
		'''
		if widgets is None:
			ui = self.getUi(name)
			widgets = ui.__dict__.values() #each object in the ui:

		for widget in widgets:
			self.addWidget(name, widget, **kwargs)


	def addWidget(self, name, widget, **kwargs):
		'''
		Adds a widget to the widgets dict under the given (ui) name.

		args:
			name (str) = name of the parent ui to construct connections for.
			widget (obj) = widget to be added.
			objectName (str) = widget's name.

		returns:
			<widget object>
		'''
		name = str(name) #prevent unicode

		self.setAttributes(kwargs) #set any passed in keyword args for the widget.

		objectName = str(widget.objectName())

		#add the widget as an attribute of the ui if it is not already.
		ui = self.getUi(name)
		if not hasattr(ui, objectName):
			setattr(ui, objectName, widget)

		class_ = self.getClassFromUiName(name) #get the corresponding slot class from the ui name.
		derivedType = self._getDerivedType(widget) #the base class of any custom widgets.  ie. 'QPushButton' from 'QPushButton_'
		signalType = self.getDefaultSignalType(derivedType) #get the default signal type for the widget as a string. ie. 'released' from 'QPushButton'
		signalInstance = getattr(widget, signalType, None) #add signal to widget. ie. <widget.valueChanged>
		method = getattr(class_, objectName, None) #use 'objectName' to get the corresponding method of the same name. ie. get method <b006> from widget 'b006' else None
		docString = getattr(method, '__doc__', None)
		prefix = self.prefix(objectName) #returns an string alphanumberic prefix if objectName startswith a series of alphanumberic chars, and is followed by three integers. ie. 'cmb' from 'cmb015'

		#add values to widgets
		self.widgets(name).update(
					{widget:{
						'widgetName':objectName, 
						'signalInstance':signalInstance,
						'widgetType':widget.__class__.__name__,
						'derivedType':derivedType,
						'method': method,
						'prefix':prefix,
						'docString':docString}})

		# print(self.sbDict[name]['widgets'][widget])
		return self.sbDict[name]['widgets'][widget] #return the stored widget.


	def removeWidgets(self, widgets, name=None):
		'''
		Remove widget keys from the widgets dict.

		args:
			widgets (obj)(list) = single or list of QWidgets.
			name (str) = ui name.
		'''
		if not name:
			name = self.getUiName()

		widgets = self.list(widgets) #if 'widgets' isn't a list, convert it to one.
		for widget in widgets:
			w = self.sbDict[name]['widgets'].pop(widget, None)
			self.gcProtect(w)

			try: #remove the widget attribute from the ui if it exists.
				delattr(ui, w.objectName())
			except: pass


	def widgets(self, name):
		'''
		Dictionary holding widget information.

		args:
			name (str) = name of ui/class. ie. 'polygons'

		returns:
			connection dict of given name with widget/method name string as key.
		ex. {'widgets' : {
						'<widget>':{
									'widgetName':'objectName',
									'signalInstance':<widget.signal>,
									'widgetType':'<widgetClassName>',
									'derivedType':'<derivedClassName>',
									'method':<method>,
									'prefix':'alphanumeric prefix',
									'docString':'method docString'
						}
			}
		'''
		if not 'widgets' in self.sbDict[name]:
			self.sbDict[name]['widgets'] = {}
			self.addWidgets(name) #construct the signals and slots for the ui

		return self.sbDict[name]['widgets']


	def setAttributes(self, attributes=None, order=['globalPos', 'setVisible'], **kwargs):
		'''
		Works with attributes passed in as a dict or kwargs.
		If attributes are passed in as a dict, kwargs are ignored.
		args:
			attributes (dict) = keyword attributes and their corresponding values.
			#order (list) = list of string keywords. ie. ['move', 'show']. attributes in this list will be set last, in order of the list. an example would be setting move positions after setting resize arguments.
		kwargs:
			set any keyword arguments.
		'''
		if not attributes:
			attributes = kwargs

		for k in order:
			v = attributes.pop(k, None)
			if v:
				from collections import OrderedDict
				attributes = OrderedDict(attributes)
				attributes[k] = v

		for attr, value in attributes.items():
			try:
				getattr(self, attr)(value)

			except Exception as error:
				if type(error)==AttributeError:
					self.setCustomAttribute(attr, value)
				else:
					raise error


	def setCustomAttribute(self, attr, value):
		'''
		Handle custom keyword arguments.
		args:
			attr (str) = custom keyword attribute.
			value (str) = the value corresponding to the given attr.
		kwargs:
			copy (obj) = widget to copy certain attributes from.
			globalPos (QPoint) = move to given global location and center.
		'''
		if attr=='copy':
			self.setObjectName(value.objectName())
			self.resize(value.size())
			self.setText(value.text())
			self.setWhatsThis(value.whatsThis())

		if attr=='globalPos':
			self.move(self.mapFromGlobal(value - self.rect().center())) #move and center


	def getClassFromUiName(self, name):
		'''
		Get the slot class corresponding to the given ui name.  ie. <Polygons> from 'polygons'
		If the name is a submenu, the parent class will be returned. ie. <Polygons> from 'polygons_submenu'		

		args:
			name (str) = ui name. ie. 'polygons'

		returns:
			(obj) class obj
		'''
		n = name.split('_')[0] #get ie. 'polygons' from 'polygons_submenu' in cases where a submenu shares the same slot class of it's parent menu.
		ui = self.getUi(name)
		# path = 'slots.{0}'.format(n[0].upper()+n[1:]) #ie. slots.Init
		mainAppWindowName = self.getMainAppWindow(objectName=True)
		className = n[0].upper()+n[1:] #capitalize the first char of name to get the class name.
		path = 'tk_slots_{0}_{1}.{2}'.format(mainAppWindowName, n, className) #ie. 'tk_slots_maya_init.Init'
		class_ = self.getClassInstance(path, ui=ui, sb=self, tk=self.parent) #get the class instance while passing in any keyword arguments into **kwargs.

		return class_


	def getDefaultSignalType(self, widgetType):
		'''
		Get the default signal type for a given widget type.

		args:
			widgetType (str) = Widget class name. ie. 'QPushButton'

		returns:
			(str) signal ie. 'released'
		'''
		signals = { #the default signal to be associated with each widget type.
			'QAction':'triggered',
			'QLabel':'released',
			'QPushButton':'released',
			'QToolButton':'released',
			'QListWidget':'itemClicked',
			'QTreeWidget':'itemClicked',
			'QComboBox':'currentIndexChanged',
			'QSpinBox':'valueChanged',
			'QDoubleSpinBox':'valueChanged',
			'QCheckBox':'released',
			'QRadioButton':'released',
			'QLineEdit':'returnPressed',
			'QTextEdit':'textChanged',
			'QProgressBar':'valueChanged',
		}

		try: #if the widget type has a default signal assigned in the signals dict; get the signal.
			signal = signals[widgetType]
		except KeyError:
			signal = ''

		return signal


	def getSignal(self, name, widget=None):
		'''
		Get the widget object with attached signal (ie. b001.onPressed) from the given widget name.

		args:
			name (str) = name of ui. ie. 'polygons'
			objectName (str) = optional widget name. ie. 'b001'

		returns:
			if objectName: (obj) widget object with attached signal (ie. b001.onPressed) of the given widget name.
			else: (list) all of the signals associated with the given name as a list.
		'''
		if not 'widgets' in self.sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		if widget:
			if not widget in self.sbDict[name]['widgets']:
				self.addWidget(name, widget)
			return self.sbDict[name]['widgets'][widget]['signalInstance']
		else:
			return [w['signalInstance'] for w in self.sbDict[name]['widgets'].values()]


	def setConnections(self, name):
		'''
		Replace any signal connections of a previous ui with the set for the ui of the given name.
		'''
		previousName = self.previousName(allowDuplicates=True)
		if previousName:
			self.disconnectSlots(previousName) #remove signals from the previous ui.
		self.connectSlots(name)


	def connectSlots(self, name, widgets=None):
		'''
		Connects signals/slots from the widgets for the given ui.
		Works with both single slots or multiple slots given as a list.

		args:
			name (str) = ui name
			widgets (obj)(list) = QWidget
		'''
		if widgets is None:
			widgets = self.widgets(name)
		else:
			widgets = self.list(widgets) #convert 'widgets' to a list if it is not one already.

		for widget in widgets:
			signal = self.getSignal(name, widget)
			slot = self.getMethod(name, widget)
			# print('connectSlots: ', name, widget.objectName(), signal, slot)
			if slot and signal:
				try:
					if isinstance(slot, (list, set, tuple)):
						map(signal.connect, slot) #connect to multiple slots from a list.
					else:
						signal.connect(slot) #connect single slot (main and cameras ui)

				except Exception as error:
					print('Error: {0} {1} connectSlots: {2} {3}'.format(name, widget.objectName(), signal, slot), '\n', error)


	def disconnectSlots(self, name, widgets=None):
		'''
		Disconnects signals/slots from the widgets for the given ui.
		Works with both single slots or multiple slots given as a list.

		args:
			name (str) = ui name
			widgets (obj)(list) = QWidget
		'''
		if widgets is None:
			widgets = self.widgets(name)
		else:
			widgets = self.list(widgets) #convert 'widgets' to a list if it is not one already.

		for widget in widgets:
			signal = self.getSignal(name, widget)
			slot = self.getMethod(name, widget)
			# print('disconnectSlots: ', name, widget.objectName(), signal, slot)
			if slot and signal:
				try:
					if isinstance(slot, (list, set, tuple)):
						signal.disconnect() #disconnect all #map(signal.disconnect, slot) #disconnect multiple slots from a list.
					else:
						signal.disconnect(slot) #disconnect single slot (main and cameras ui)

				except Exception as error:
					print('Error: {0} {1} disconnectSlots: {2} {3} #'.format(name, widget.objectName(), signal, slot), '\n', error)


	def uiList(self, names=False, ui=False):
		'''
		Get a list of either all ui names, all ui object's, or both as key/value pairs in a dict.

		args:
			names (bool) = return string ui list
			ui (bool) =	return dynamic ui list

		returns:
			if name: return list of ui names
			if ui: return list of dynamic ui objects
			else: dict of ui names strings as keys, and corresponding ui objects as values. ie. {'ui name':<ui object>}
			'''
		if names:
			return [k for k,v in self.sbDict.items() if type(v)==dict and 'ui' in v]
		elif ui:
			return [v['ui'] for k,v in self.sbDict.items() if type(v)==dict and 'ui' in v]
		else:
			return {k:v['ui'] for k,v in self.sbDict.items() if type(v)==dict and 'ui' in v}

	#Property
	def getUi(self, name=None, setAsCurrent=False, level=None):
		'''
		Get the dynamic ui using its string name, or if no argument is given, return the current ui.

		args:
			name (str) = Name of class. ie. 'polygons' (by default getUi returns the current ui)
			setAsCurrent (bool) = Set the ui name as the currently active ui. (default: False)
			level (int) = Get the ui of the given level. (2:submenu, 3:main_menu)

		returns:
			if name: corresponding dynamic ui object of given name from the key 'uiList'.
			else: current dynamic ui object
		'''
		if name is None:
			name = self.getUiName(camelCase=True)
			if name is None:
				return None

		if level==2: #submenu
			if 'submenu' not in name:
				name = name+'_submenu'

		if level==3: #main menu
			name = name.split('_')[0] #'polygons' from 'polygons_component_submenu'

		if setAsCurrent:
			self.name = name #set the property for the current ui name.
			self.setConnections(name) #connect signal/slot connections for the current ui, while disconnecting any previous.

		try:
			return self.sbDict[name]['ui']
		except (ValueError, KeyError):
			try:
				name = name[0].lower()+name[1:] #if the ui key doesn't exist, try lowercasing the first letter in name.
				return self.sbDict[name]['ui']
			except (ValueError, KeyError):
				return None


	def getUiFromWidget(self, widget):
		'''
		Get the ui for the given widget.

		args:
			widget (obj) = QWidget

		returns:
			 (obj) ui. ie. <polygons> from <somewidget>
		'''
		return next((self.getUi(k) for k,v in self.sbDict.items() if type(v) is dict and 'widgets' in v and widget in v['widgets']), None)

	#Property
	def setUiName(self, index):
		'''
		The 'name' list is used for various things such as; maintaining a history of ui's that have been called.

		args:
			index (int)(str) = index or name of the ui.

		returns:
			(str) corresponding ui name.
		'''
		if not 'name' in self.sbDict:
			self.sbDict['name']=[]

		if not type(index)==int:
			index = self.getUiIndex(index) #get index using name

		self.sbDict['name'].append(self.uiList(names=True)[index])

		return self.sbDict['name'][-1]

	#Property
	def getUiName(self, ui=None, camelCase=False, pascalCase=False, level=None):
		'''
		Get the ui name as a string.
		If no argument is given, the name for the current ui will be returned.

		args:
			ui (obj) = Use ui object to get its corresponding name. (the default behavior is to return the current ui name)
			camelCase (bool) = Return name with first letter lowercase. (default: False)
			pascalCase (bool) = Return name with first letter capitalized. (default: False)
			level (int) = Get the ui of the given level. (2:submenu, 3:main_menu)

		returns:
			(str) - ui name.
		'''
		if not 'name' in self.sbDict:
			self.sbDict['name']=[]

		if ui is None:
			try:
				name = self.sbDict['name'][-1]
			except IndexError: #if index out of range (no value exists): return None
				return None
		else: #get the ui name string key from the ui value in uiList.
			name = next(k for k, v in self.uiList().items() if v==ui)

		if level==2: #submenu
			if 'submenu' not in name:
				name = name+'_submenu'

		if level==3: #main menu
			name = name.split('_')[0] #polygons from polygons_component_submenu

		if pascalCase:
			name = name[:1].capitalize()+name[1:] #capitalize the first letter
		if camelCase:
			name = name[0].lower()+name[1:] #lowercase the first letter

		return name


	def getUiNameFromWidget(self, widget):
		'''
		Get the ui name from the given widget.

		args:
			widget (obj) = QWidget

		returns:
			 (str) ui name. ie. 'polygons' from <somewidget>
		'''
		return next((k for k,v in self.sbDict.items() if type(v) is dict and 'widgets' in v and widget in v['widgets']), None)


	def getUiNameFromMethod(self, method):
		'''
		Get the ui name from the given method.

		args:
			widget (obj) = QWidget

		returns:
			 (str) ui name. ie. 'polygons' from <somewidget>
		'''
		for name, value in self.sbDict.items():
			if type(value)==dict:
				try:
					if next((v for v in value['widgets'].values() if v['method'] is method), None):
						return name
				except KeyError:
					pass

	#Generator
	def getUiNameFromKey(self, nestedKey, _uiName=None, _nested_dict=None):
		'''
		Get the ui name from a given nested key.

		args:
			nestedKey (key) = The key of a nested dict to get the ui of.
			_uiName (key) = internal use. The key from the top-level dict. (ie. 'polygons') which is later returned as the uiName if a key match is found in a directly nested dict.
			_nested_dict (dict) = internal use. Recursive call.

		ex. next(self.getUiNameFromKey(<widget>), None) #returns the first ui name with a nested dict containing the given key if found; else None.
		'''
		if _nested_dict is None:
			_nested_dict = self.sbDict

		for k,v in _nested_dict.items():
			if type(v) is dict:
				if nestedKey in v.keys():
					if not self.sbDict.get(k): #if the key is not top level:
						k = _uiName #re-assign and keep passing the top level key so that it can eventually be returned.
					yield _uiName
				else:
					n = next(self.getUiNameFromKey(nestedKey, k, v), None)
					if n:
						yield n


	def getUiNamesFromValue(self, nestedValue):
		'''
		Get the ui name from a given nested Value.

			args:
				nestedValue (value) = The value of a nested dict to get the ui of.

			returns:
				(list) of uiNames that contain the given nestedValue.

			ex. self.getUiNameFromValue('cmb002') #returns the names of all ui with a dict containing value 'cmb002'.
		'''
		_uiNames=[]
		for uiName, value in self.sbDict.items():
			if type(value)==dict: #for each top-level dict in sbDict:
				if self.getParentKeys(nestedValue, value): #if a nested dict contains the nested value: (getParentKeys returns a list containing the hierarchical key path of the nestedValue)
					_uiNames.append(uiName)
		return _uiNames

	#Property
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
			return self.uiList(names=True).index(name)
		else:
			return self.uiList(names=True).index(self.getUiName())


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

		self.sbDict[name]['size'] = size
		return self.sbDict[name]['size']

	#Property
	def setUiSizeX(self, width, name=None):
		'''
		Set the X (width) value for the current ui.

		args:
			name (str) = the name of the ui to set the width for.
			width (int) = X size as an int
		'''
		height = self.getUiSize(name=name, height=True) #get the hight value.
		self.setUiSize(name=name, width=width, height=height)

	#Property
	def setUiSizeY(self, height, name=None):
		'''
		Set the Y (height) value for the current ui.

		args:
			name (str) = the name of the ui to set the height for.
			height (int) = Y size as an int
		'''
		width = self.getUiSize(name=name, width=True) #get the width value.
		self.setUiSize(name=name, height=height, width=width)

	#Property
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

		if not 'size' in self.sbDict[name]:
			self.setUiSize(name)

		if width:
			return self.sbDict[name]['size'][0]
		elif height:
			return self.sbDict[name]['size'][1]
		elif percentWidth:
			return self.sbDict[name]['size'][0] *percentWidth /100
		elif percentHeight:
			return self.sbDict[name]['size'][1] *percentHeight /100
		else:
			return self.sbDict[name]['size']

	#Property
	def getUiSizeX(self, name=None):
		'''
		Get the X (width) value for the current ui.

		args:
			name (str) = ui name to get size from.

		returns:
			returns width as int
		'''
		return self.getUiSize(name=name, width=True)

	#Property
	def getUiSizeY(self, name=None):
		'''
		Get the Y (height) value for the current ui.

		args:
			name (str) = ui name to get size from.

		returns:
			returns width as int
		'''
		return self.getUiSize(name=name, height=True)

	#Property
	def setMainAppWindow(self, app):
		'''
		Set parent application.

		args:
			app = app object.

		returns:
			string name of app
		'''
		self.sbDict['mainAppWindow'] = app

		return self.sbDict['mainAppWindow']

	#Property
	def getMainAppWindow(self, objectName=False):
		'''
		Get parent application if any.

		args:
			objectName (bool) = get string name of app. (by default getMainAppWindow returns app object)

		returns:
			app object or string name
		'''
		if not 'mainAppWindow' in self.sbDict:
			self.sbDict['mainAppWindow'] = None
		
		app = self.sbDict['mainAppWindow']

		if objectName:
			if not app: #if app is None, return an empty string value.
				return ''
			else: #remove 'Window' from objectName ie. 'Maya' from 'MayaWindow' and set lowercase.
				name = app.objectName().rstrip('Window')
				return name[0].lower()+name[1:] #lowercase the first letter.
		else:
			return app

	#Property
	def setClassInstance(self, class_, name=None, **kwargs):
		'''
		Case insensitive. Class string keys are stored lowercase regardless of how they are recieved.

		args:
			class_ (str)(obj) = module name.class to import and store class. 
					ie.  ie. 'polygons', 'tk_slots_max_polygons.Polygons', or <tk_slots_max_polygons.Polygons>
			name (str) = optional name key to store the class under (else the class name will be used).

		returns:
			class object.
		'''
		if isinstance(class_, (str, unicode)): #if arg given as string or unicode:
			name = class_.split('_')[-1].split('.')[-1] #get key from the class_ string ie. 'class' from 'module.Class'
			class_ = locate(class_)
		elif not name:
			name = class_.__class__.__name__ #if arg as <object>:

		name = name[0].lower()+name[1:] #lowercase the first letter.

		if not name in self.sbDict:
			self.sbDict[name] = {}

		if callable(class_):
			self.sbDict[name]['class'] = class_(**kwargs)
		else:
			self.sbDict[name]['class'] = class_


		return self.sbDict[name]['class']

	#Property
	def getClassInstance(self, class_, **kwargs):
		'''
		Case insensitive. (Class string keys are lowercase and any given string will be converted automatically)
		If class is not in self.sbDict, getClassInstance will attempt to use setClassInstance() to first store the class.

		args:
			class_ (str)(obj) = module name.class to import and store class.
				ie. 'polygons', 'tk_slots_max_polygons.Polygons', or <tk_slots_max_polygons.Polygons>

		returns:
			class object.
		'''
		if isinstance(class_, (str, unicode)): #if arg given as string or unicode:
			name = class_.split('_')[-1].split('.')[-1] #get key from class_ string ie. 'class' from 'module.Class'#class_.lower()
		else: #if arg as <object>:
			if not callable(class_):
				return None
			name = class_.__class__.__name__

		name = name[0].lower()+name[1:] #lowercase the first letter.

		try:
			if not 'class' in self.sbDict[name]:
				return self.setClassInstance(class_, **kwargs) #construct the signals and slots for the ui

			return self.sbDict[name]['class']

		except KeyError as error:
			print(error)
			return None

	#Property
	def getWidget(self, objectName=None, name=None):
		'''
		Case insensitive. Get the widget object/s from the given ui and objectName.

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

		if not 'widgets' in self.sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		if objectName:
			return next((w for w in self.sbDict[name]['widgets'].values() if w['widgetName']==objectName), None)
		else:
			return [w for w in self.sbDict[name]['widgets'].keys()]

	#Property
	def getWidgetName(self, widget=None, name=None):
		'''
		Get the widget's stored string objectName.

		args:
			widget (obj) = QWidget
			name (str) = name of ui. ie. 'polygons'. If no name is given, the current ui will be used.

		returns:
			if widget: (str) the stored objectName for the given widget.
			if not widget: (list) all names.
			if name: stored objectNames for the given ui name.
			if not name: stored objectName from the current ui.
			else: all stored objectNames.
		'''
		if not name:
			name = self.getUiName()

		if not 'widgets' in self.sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		if widget:
			if not widget in self.sbDict[name]['widgets']:
				self.addWidget(name, widget)
			return self.sbDict[name]['widgets'][widget]['widgetName']

		if name and not widget: #return all objectNames from ui name.
			return [w['widgetName'] for w in self.sbDict[name]['widgets'].values()]
		else: #return all objectNames:
			return [w['widgetName'] for k,w in self.sbDict.items() if k=='widgets']


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
		if isinstance(widget, (str, unicode)):
			objectName = self.sbDict[name]['widgets'][widget] #use the stored objectName as a more reliable key.
			widget = self.getWidget(objectName, name) #use the objectName to get a string key for 'widget'

		if not name:
			name = self.getUiName()

		if not 'widgets' in self.sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui
		# print(name, widget)
		try:
			if not widget in self.sbDict[name]['widgets']:
				self.addWidget(name, widget)
			return self.sbDict[name]['widgets'][widget]['widgetType']

		except KeyError:
			return None


	def _getDerivedType(self, widget):
		'''
		Internal use. Get the base class of a custom widget.
		If the type is a standard widget, the derived type will be that widget's type.

		args:
			widget (obj) = QWidget. ie. widget with class name: 'QPushButton_'

		returns:
			(string) base class name. ie. 'QPushButton'
		'''
		# print(widget.__class__.__mro__)
		for c in widget.__class__.__mro__:
			if c.__module__=='PySide2.QtWidgets': #check for the first built-in class.
				derivedType = c.__name__ #Then use it as the derived class.
				return derivedType


	def getDerivedType(self, widget, name=None):
		'''
		Get the base class of a custom widget.
		If the type is a standard widget, the derived type will be that widget's type.

		args:
			widget (str)(obj) = QWidget or it's objectName.
			name (str) = ui name.

		returns:
			(string) base class name. ie. 'QPushButton' from a custom widget with class name: 'QPushButton_'
		'''
		if isinstance(widget, (str, unicode)):
			objectName = self.sbDict[name]['widgets'][widget] #use the stored objectName as a more reliable key.
			widget = self.getWidget(objectName, name) #use the objectName to get a string key for 'widget'

		if not name:
			name = self.getUiName()

		if not 'widgets' in self.sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		try:
			if not widget in self.sbDict[name]['widgets']:
				self.addWidget(name, widget)
			return self.sbDict[name]['widgets'][widget]['derivedType']

		except KeyError:
			return None


	def getMethod(self, name, widget=None):
		'''
		Get the method(s) associated with the given ui / widget.

		args:
			name (str) = name of class. ie. 'polygons'
			widget (str)(obj) = widget, widget's objectName, or method name.

		returns:
			if widget: corresponding method object to given widget.
			else: all of the methods associated to the given ui name as a list.

		ex. sb.getMethod('polygons', <b022>)() #call method <b022> of the 'polygons' class
		'''
		if not 'widgets' in self.sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		if widget:
			try:
				if type(widget) is str:
					return next(w['method'][0] for w in self.sbDict[name]['widgets'].values() if w['widgetName']==widget) #if there are event filters attached (as a list), just get the method (at index 0).
				
				if not widget in self.sbDict[name]['widgets']:
					self.addWidget(name, widget)
				return self.sbDict[name]['widgets'][widget]['method'][0] #if there are event filters attached (as a list), just get the method (at index 0).

			except:
				if type(widget) is str:
					return next((w['method'] for w in self.sbDict[name]['widgets'].values() if w['widgetName']==widget), None)
				
				if not widget in self.sbDict[name]['widgets']:
					self.addWidget(name, widget)
				return self.sbDict[name]['widgets'][widget]['method']
		else:
			return [w['method'] for w in self.sbDict[name]['widgets'].values()]


	def getDocString(self, name, widgetName, first_line_only=True, unformatted=False):
		'''
		args:
			name (str) = optional name of class. ie. 'polygons'. else, use current name.
			widgetName (str) = name of method. ie. 'b001'
			unformatted = bool return entire unedited docString

		returns:
			if unformatted: the entire stored docString
			else: edited docString; name of method
		'''
		if not 'widgets' in self.sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		docString = next(w['docString'] for w in self.sbDict[name]['widgets'].values() if w['widgetName']==widgetName)

		if docString is None:
			return None

		lines = docString.split('\n')
		if first_line_only:
			i=0
			while not docString:
				try:
					docString = lines[i]
					i+=1
				except IndexError:
					break

		if docString and not unformatted:
			return docString.strip('\n\t') #return formatted docString
		else:
			return docString #return entire unformatted docString, or 'None' is docString==None.

	#Property
	def previousName(self, previousIndex=False, allowDuplicates=False, allowCurrent=False, omitLevel=[], as_list=False):
		'''
		Get the previously called ui name string, or a list of ui name strings ordered by use.
		It does so by pulling from the 'name' list which keeps a list of the ui names as they are called. ie. ['previousName2', 'previousName1', 'currentName']

		args:
			previousIndex (bool) = Return the index of the last valid previously opened ui name.
			allowDuplicates (bool) = Applicable when returning as_list. Allows for duplicate names in the returned list.
			omitLevel (int)(list) = Remove instances of the given ui level(s) from the results. Default is [] which omits nothing.
			allowCurrent (bool) = Allow the currentName. Default is off.
			as_list (bool) = Returns the full list of previously called names. By default duplicates are removed.

		returns:
			with no arguments given - string name of previously opened ui.
			if previousIndex: int - index of previously opened ui
			if as_list: returns [list of string names]
		'''
		if not 'name' in self.sbDict:
			self.sbDict['name'] = []

		self.sbDict['name'] = self.sbDict['name'][-200:] #keep original list length restricted to last 200 elements

		list_ = self.sbDict['name'] #work on a copy of the list, keeping the original intact

		if not allowCurrent:
			list_ = list_[:-1] #remove the last index. (currentName)

		omitLevel = self.list(omitLevel) #if omitLevel is not a list, convert it to one.
		list_ = [i for i in list_ if not self.getUiLevel(i) in omitLevel] #remove any items having a uiLevel of those in the omitLevel list.

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
		if not 'prevCommand' in self.sbDict:
			self.sbDict['prevCommand'] = [] #initialize list

		self.sbDict['prevCommand'] = self.sbDict['prevCommand'][-20:] #keep original list length restricted to last 20 elements

		list_ = self.sbDict['prevCommand']
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
		if not 'prevCamera' in self.sbDict:
			self.sbDict['prevCamera'] = [] #initialize list

		self.sbDict['prevCamera'] = self.sbDict['prevCamera'][-20:] #keep original list length restricted to last 20 elements

		list_ = self.sbDict['prevCamera']
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


	def gcProtect(self, obj=None, clear=False):
		'''
		Protect given object from garbage collection.

		args:
			obj (obj) = obj to add to the protected list.

		returns:
			(list) of protected objects.
		'''
		if not 'gcProtect' in self.sbDict:
			self.sbDict['gcProtect']=[]

		if clear:
			return self.sbDict['gcProtect'][:]

		if obj and obj not in self.sbDict['gcProtect']:
			self.sbDict['gcProtect'].append(obj)

		return self.sbDict['gcProtect']


	def get(self, obj, type_='value', _nested_dict=None, _nested_list=[]):
		'''
		Get objects from any nested object in _nested_dict using a given key or value.

		args:
			obj (key)(value) = Key or Value. The object to get the 'type_' of return value from.
			type_ (str) = Desired return type. valid values are: 'value', 'valuesFromKey', 'keysFromValue', 'namesFromValue'
			_nested_dict (dict) = internal use. default is sbDict
			_nested_list (list) = internal use.

		returns:
			(list) depending on the specified type.

		ex. call:
		self.get('cmb002', 'nameFromValue') #returns a list of all ui names containing 'cmb002' values.
		'''
		if _nested_dict is None:
			_nested_dict = self.sbDict

		for k,v in _nested_dict.items():
			if type_ is 'valuesFromKey': 
				if k==obj: #found key
					_nested_list.append(v)

			elif type_ is 'keysFromValue':
				if v==obj: #found value
					_nested_list.append(k)

			elif type_ is 'namesFromValue':
				if v==obj: #found value
					_nested_list.append(self.getParentKeys(v)[0])

			if type(v) is dict: #found dict
				p = self.get(obj, type_, v, _nested_list) #recursive call
				if p:
					return p
		return _nested_list


	def getParentKeys(self, value, _nested_dict=None):
		'''
		Get all parent keys from a nested value.

		args:
			value (value) = The nested value to get keys for.
			_nested_dict (dict) = internal use.

		returns:
			(list) parent keys

		ex. call:
		getParentKeys('cmb002') returns all parent keys of the given value. ex. ['polygons', 'widgets', '<widgets.QComboBox_.QComboBox_ object at 0x0000016B6C078908>', 'widgetName'] ...
		'''
		if _nested_dict is None:
			_nested_dict = self.sbDict

		for k,v in _nested_dict.items():
			if type(v) is dict:
				p = self.getParentKeys(value, v)
				if p:
					return [k]+p
			elif v==value:
				return [k]

	#Property
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
			return self.sbDict[name]['uiLevel']
		except ValueError:
			return None


	def prefix(self, widget, prefix=None):
		'''
		Get or Query the widgets prefix.
		A valid prefix is returned when the given widget's objectName startswith an alphanumeric char, followed by at least three integers. ex. i000 (alphanum,int,int,int)

		ex. prefix('b023') returns 'b'
		if the second 'prefix' arg is given, then the method checks if the given objectName has the prefix, and the return value is bool.

		args:
			widget (str)(obj) = widget or it's objectName.
			prefix (str)(list) = optional; check if the given objectName startwith this prefix.

		returns:
			if prefix arg given:
				(bool) - True if correct format else; False.
			else:
				(str) alphanumeric 'string' 

		ex call: sb.prefix(widget, ['b', 'chk', '_'])
		'''
		if prefix is not None: #check the actual prefix against the given prefix and return bool.
			prefix = self.list(prefix) #if 'widgets' isn't a list, convert it to one.

			name = self.getUiName()
			for p in prefix:
				try:
					if isinstance(widget, (str, unicode)): #get the prefix using the widget's objectName.
						prefix_ = next(w['prefix'] for w in self.sbDict[name]['widgets'].values() if w['widgetName']==widget)
					else:
						prefix_ = self.sbDict[name]['widgets'][widget]['prefix']
					if prefix_==p:
						return True

				except:
					if not isinstance(widget, (str, unicode)):
						widget = widget.objectName()
					if widget.startswith(p):
						i = len(p)
						integers = [c for c in widget[i:i+3] if c.isdigit()]
						if len(integers)>2 or len(widget)==i:
							return True
			return False

		else: #return prefix.
			prefix=''
			if not isinstance(widget, (str, unicode)):
				widget = widget.objectName()
			for char in widget:
				if not char.isdigit():
					prefix = prefix+char
				else:
					break

			i = len(prefix)
			integers = [c for c in widget[i:i+3] if c.isdigit()]
			if len(integers)>2 or len(widget)==i:
				return prefix


	@staticmethod
	def list(x):
		'''
		Convert a given obj to a list if it isn't a list, set, or tuple already.

		args:
			x () = unknown object type.

		returns:
			(list)
		'''
		if not isinstance(x, (list,set,tuple)):
			x = [x]
		return x


	@staticmethod
	def getParentWidgets(widget, objectNames=False):
		'''
		Get the parent widget at the top of the hierarchy for the given widget.

		args:
			widget (obj) = QWidget
			index (int) = (optional) index. Last index is top level.

		returns:
			(list)
		'''
		parentWidgets=[]
		w = widget
		while w:
			parentWidgets.append(w)
			w = w.parentWidget()
		if objectNames:
			return [str(w.objectName()) for w in parentWidgets]
		return parentWidgets


	@staticmethod
	def getTopLevelParent(widget, index=-1):
		'''
		Get the parent widget at the top of the hierarchy for the given widget.

		args:
			widget (obj) = QWidget
			index (int) = (optional) index. Last index is top level.

		returns:
			(QWidget)
		'''
		return self.getParentWidgets[index]


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


	#assign properties
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
	getWidgetNames = property(getWidgetName)









if __name__=='__main__':
	#initialize and create a Switchboard instance
	app = QApplication.instance() #get the app instance if it exists (required by the QUiLoader)
	if not app:
		app = QApplication(sys.argv)






#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

'''
test example:
sbDict={
	'polygons':{'class': '<Polygons>',
				'ui': '<polygons ui object>',
				'uiLevel': 3,
				'size': [210, 480],
				'widgets': {'<widgets.QComboBox_.QComboBox_ object at 0x0000016B6C078908>': {
									'widgetName': 'cmb002', 
									'widgetType': 'QComboBox_', 
									'derivedType': 'QComboBox', 
									'signalInstance': '<PySide2.QtCore.SignalInstance object at 0x0000016B62BC5780>',
									'prefix':'cmb', 
									'docString': '\n\t\tSelect All Of Type\n\t\t',
									'method': '<bound method Polygons.cmb002 of <tk_slots_max_polygons.Polygons object at 0x0000016B6BC26470>>'}, }},
	'mainAppWindow': None,
	'name': ['polygons'],
	'prevCommand': [['b000', 'multi-cut tool']],
	'prevCamera:': [['v000', 'Viewport: Persp']],
	'gcProtect': ['<protected object>']}


#real world example:
sbDict = {
'materials': {
	'widgets': {
		'<PySide2.QtWidgets.QVBoxLayout object at 0x0000000003D07208>': {'widgetType': 'QVBoxLayout', 'widgetName': 'verticalLayout_2', 'derivedType': 'QVBoxLayout', 'signalInstance': None, 'docString': None, 'prefix': None, 'method': None}, 
		'<widgets.qToolButton_.QToolButton_ object at 0x0000000003D04E08>': {'widgetType': 'QToolButton_', 'widgetName': 'tb002', 'derivedType': 'QToolButton', 'signalInstance': '<PySide2.QtCore.SignalInstance object at 0x0000000002A463D8>', 'docString': None, 'prefix': 'tb', 'method': '<bound method Materials.wrapper of <tk_slots_max_materials.Materials object at 0x0000000003D547C8>>'}, 
		'<PySide2.QtWidgets.QGroupBox object at 0x0000000003D07248>': {'widgetType': 'QGroupBox', 'widgetName': 'group000', 'derivedType': 'QGroupBox', 'signalInstance': None, 'docString': None, 'prefix': 'group', 'method': None}, 
		'<PySide2.QtWidgets.QPushButton object at 0x0000000003D07288>': {'widgetType': 'QPushButton', 'widgetName': 'b002', 'derivedType': 'QPushButton', 'signalInstance': '<PySide2.QtCore.SignalInstance object at 0x0000000002A46390>', 'docString': None, 'prefix': 'b', 'method': '<bound method Materials.wrapper of <tk_slots_max_materials.Materials object at 0x0000000003D547C8>>'}, 
		'<widgets.qToolButton_.QToolButton_ object at 0x0000000003D04FC8>': {'widgetType': 'QToolButton_', 'widgetName': 'tb001', 'derivedType': 'QToolButton', 'signalInstance': '<PySide2.QtCore.SignalInstance object at 0x0000000002A46408>', 'docString': '\n\t\tStored Material Options\n\t\t', 'prefix': 'tb', 'method': '<bound method Materials.tb001 of <tk_slots_max_materials.Materials object at 0x0000000003D547C8>>'}, 
		'<PySide2.QtWidgets.QWidget object at 0x0000000003D070C8>': {'widgetType': 'QWidget', 'widgetName': 'mainWindow', 'derivedType': 'QWidget', 'signalInstance': None, 'docString': None, 'prefix': 'mainWindow', 'method': None}, 
		'<widgets.qProgressBar_.QProgressBar_ object at 0x0000000003D07088>': {'widgetType': 'QProgressBar_', 'widgetName': 'progressBar', 'derivedType': 'QProgressBar', 'signalInstance': '<PySide2.QtCore.SignalInstance object at 0x0000000002A463F0>', 'docString': None, 'prefix': 'progressBar', 'method': None}, 
		'<widgets.qComboBox_.QComboBox_ object at 0x0000000003D04F08>': {'widgetType': 'QComboBox_', 'widgetName': 'cmb002', 'derivedType': 'QComboBox', 'signalInstance': '<PySide2.QtCore.SignalInstance object at 0x0000000002A46378>', 'docString': '\n\t\tMaterial list\n\n\t\targs:\n\t\t\tindex (int) = parameter on activated, currentIndexChanged, and highlighted signals.\n\t\t', 'prefix': 'cmb', 'method': '<bound method Materials.cmb002 of <tk_slots_max_materials.Materials object at 0x0000000003D547C8>>'}, 
		'<widgets.qPushButton_Draggable.QPushButton_Draggable object at 0x0000000003D04D88>': {'widgetType': 'QPushButton_Draggable', 'widgetName': 'pin', 'derivedType': 'QPushButton', 'signalInstance': '<PySide2.QtCore.SignalInstance object at 0x0000000002A463A8>', 'docString': '\n\t\tContext menu\n\t\t', 'prefix': 'pin', 'method': '<bound method Materials.pin of <tk_slots_max_materials.Materials object at 0x0000000003D547C8>>'}, 
		'<PySide2.QtWidgets.QGridLayout object at 0x0000000003D07148>': {'widgetType': 'QGridLayout', 'widgetName': 'gridLayout_2', 'derivedType': 'QGridLayout', 'signalInstance': None, 'docString': None, 'prefix': None, 'method': None}, 
		'<PySide2.QtWidgets.QHBoxLayout object at 0x0000000003D07188>': {'widgetType': 'QHBoxLayout', 'widgetName': 'horizontalLayout', 'derivedType': 'QHBoxLayout', 'signalInstance': None, 'docString': None, 'prefix': 'horizontalLayout', 'method': None}, 
		'<PySide2.QtWidgets.QVBoxLayout object at 0x0000000003D071C8>': {'widgetType': 'QVBoxLayout', 'widgetName': 'verticalLayout', 'derivedType': 'QVBoxLayout', 'signalInstance': None, 'docString': None, 'prefix': 'verticalLayout', 'method': None}, 
		'<widgets.qToolButton_.QToolButton_ object at 0x0000000003D04E88>': {'widgetType': 'QToolButton_', 'widgetName': 'tb000', 'derivedType': 'QToolButton', 'signalInstance': '<PySide2.QtCore.SignalInstance object at 0x0000000002A46420>', 'docString': None, 'prefix': 'tb', 'method': '<bound method Materials.wrapper of <tk_slots_max_materials.Materials object at 0x0000000003D547C8>>'}, 
		'<PySide2.QtWidgets.QWidget object at 0x0000000003D07108>': {'widgetType': 'QWidget', 'widgetName': 'layoutWidget_2', 'derivedType': 'QWidget', 'signalInstance': None, 'docString': None, 'prefix': None, 'method': None}
		}, 
	'size': [256, 182], 
	'ui': '<PySide2.QtWidgets.QMainWindow object at 0x0000000003D04D48>', 
	'class': '<tk_slots_max_materials.Materials object at 0x0000000003D547C8>', 
	'uiLevel': 3
	}
}
'''




# deprecated: -----------------------------------




	



# def hasKey(self, *args): #check if key exists in switchboard dict.
# 	'''
# 	Check if a nested key exists .

# 	args:
# 		(str) dict keys in order of hierarchy.  ie. 'polygons', 'widgets', 'b001', 'method'

# 	returns:
# 		(bool)
# 	'''
# 	if len(args)==1:
# 		if args[0] in self.sbDict:
# 			return True

# 	elif len(args)==2:
# 		if args[1] in self.sbDict[args[0]]:
# 			return True

# 	elif len(args)==3:
# 		if args[2] in self.sbDict[args[0]][args[1]]:
# 			return True

# 	elif len(args)==4:
# 		if args[3] in self.sbDict[args[0]][args[1]][args[2]]:
# 			return True
# 	else:
# 		return False

	# def getSubmenu(self, ui=None):
	# 	'''
	# 	Get the submenu object of the given ui using it's name string, or the parent ui object.

	# 	args:
	# 		ui (str) = ui name.
	# 			<ui object> - dynamic ui.
	# 	'''
	# 	if not isinstance(ui, (str, unicode)):
	# 		name = self.getUiName(ui) #get name using ui object, or get current ui name if ui=None.

	# 	if 'submenu' not in name:
	# 		name = name+'_submenu'

	# 	return self.getUi(name)



	# def getWidgets(self, name=None):
	# 	'''
	# 	Get all widgets for a ui.

	# 	args:
	# 		name (str) = name of ui. ie. 'polygons'. If no name is given, the current ui will be used.
	# 	returns:
	# 		all widgets for the given ui.
	# 	'''
	# 	return self.getWidget(name=name)


	
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

# def getNameFrom(obj):
# 	'''
# 	Get the ui name from any object existing in 'widgets'.

# 	args:
# 		obj = <object> - 
# 	returns:
# 		 'string' - the corresponding method name from the given object.
# 		 ex. 'polygons' from <widget>
# 	'''
# 	for name, v in self.sbDict.items():
# 		if type(v)==dict:
# 			for k, v in v.items():
# 				if type(v)==dict:
# 					for k, v in v.items():
# 						if type(v)==dict:
# 							for k, v in v.items():
# 								if v==obj:
# 									return name