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

	The widgets is built as needed for each class when addSignals (or any other dependant method) is called.
	'''
	def __init__(self, sbDict):
		'''
		args:
			sbDict = main dictionary object.
		'''
		self._sbDict = sbDict


	def buildwidgets(self, name):
		'''
		Add the signal/slot connections for each widget in a given ui.

		The signals dict establishes what type widgets will be added to the widgets, and what associated signal to apply.
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

		# print(self.widgets(name))
		return self.widgets(name)


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
		Adds a widget to the widgets under the given (ui) name.
		Decoupling this from 'buildwidgets' allows additional widgets to be added at any time.
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
			objectName = str(widget.objectName())


		n = name.split('_')[0] #get ie. 'polygons' from 'polygons_submenu' in cases where a submenu shares the same slot class of it's parent menu.
		# path = 'slots.{0}'.format(n[0].upper()+n[1:]) #ie. slots.Init
		path = 'tk_slots_{0}_{1}.{2}'.format(self.getMainAppWindow(objectName=True), n, n[0].upper()+n[1:]) #ie. tk_slots_maya_init.Init
		class_ = self.getClassInstance(path)


		signals = { #the default signal to be associated with each widget type.
			'QProgressBar':'valueChanged',
			'QPushButton':'released',
			'QToolButton':'released',
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

		signalInstance = getattr(widget, signal, None) #add signal to widget. ie. signalInstance == widget.valueChanged
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
						'method':method,
						'prefix':prefix,
						'docString':docString}})

		#add the widget as an attribute of the ui if it is not already.
		ui = self.getUi(name)
		if not hasattr(ui, objectName):
			setattr(ui, objectName, widget)


		# print(self._sbDict[name]['widgets'][widget])
		return self._sbDict[name]['widgets'][widget] #return the stored widget.


	def widgets(self, name):
		'''
		Dictionary holding widget information.
		Used primarily by 'buildwidgets' method to construct signal and slot connections that can later be connected and disconnected by the add/removeSignals methods.

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
		if not 'widgets' in self._sbDict[name]:
			self._sbDict[name]['widgets'] = {}
			self.buildwidgets(name) #construct the signals and slots for the ui

		return self._sbDict[name]['widgets']


	def removeWidgets(self, widgets, name=None):
		'''
		Remove widget keys from the 'widgets'.

		args:
			widgets (obj)(list) = single or list of QWidgets.
			name (str) = ui name.
		'''
		if not name:
			name = self.getUiName()

		widgets = self.list_(widgets) #if 'widgets' isn't a list, convert it to one.
		for widget in widgets:
			w = self._sbDict[name]['widgets'].pop(widget, None)
			self.gcProtect(w)

			try: #remove the widget attribute from the ui if it exists.
				delattr(ui, w.objectName())
			except: pass


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
		if not 'widgets' in self._sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		if widget:
			return self._sbDict[name]['widgets'][widget]['signalInstance']
		else:
			return [w['signalInstance'] for w in self._sbDict[name]['widgets'].values()]


	def setSignals(self, name):
		'''
		Replace any signals of a previous ui with the set for the ui of the given name.
		'''
		previousName = self.previousName(allowLevel0=True, allowDuplicates=1)
		if previousName:
			self.removeSignals(previousName) #remove signals from the previous ui.
		self.addSignals(name)



	def addSignals(self, name, widgets=None):
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
			widgets = self.list_(widgets) #convert 'widgets' to a list if it is not one already.

		for widget in widgets:
			signal = self.getSignal(name, widget)
			slot = self.getMethod(name, widget)
			# print('addSignals: ', name, widget.objectName(), signal, slot)
			if slot and signal:
				try:
					if isinstance(slot, (list, set, tuple)):
						map(signal.connect, slot) #connect multiple slots from a list.
					else:
						signal.connect(slot) #connect single slot (main and cameras ui)

				except Exception as error:
					print('# Error: {0} {1} addSignals: {2} {3} #'.format(name, widget.objectName(), signal, slot), '\n', error)


	def removeSignals(self, name, widgets=None):
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
			# print('removeSignals: ', name, widget.objectName(), signal, slot)
			if slot and signal:
				try:
					if isinstance(slot, (list, set, tuple)):
						signal.disconnect() #disconnect all #map(signal.disconnect, slot) #disconnect multiple slots from a list.
					else:
						signal.disconnect(slot) #disconnect single slot (main and cameras ui)

				except Exception as error:
					print('# Error: {0} {1} removeSignals: {2} {3} #'.format(name, widget.objectName(), signal, slot), '\n', error)


	def uiList(self, name=None, ui=None):
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


	def getUi(self, name=None):
		'''
		Property.
		Get the dynamic ui using its string name, or if no argument is given, return the current ui.

		args:
			name (str) = name of class. ie. 'polygons' (by default getUi returns the current ui)
		returns:
			if name: corresponding dynamic ui object of given name from the key 'uiList'.
			else: current dynamic ui object
		'''
		if name is None:
			name = self.getUiName(camelCase=True)
		try:
			return self._sbDict[name]['ui'] #self.uiList(ui=True)[self.getUiIndex(name)]
		except ValueError:
			return None


	def setUiName(self, index):
		'''
		The 'name' list is used for various things such as; maintaining a history of ui's that have been called previously.

		args:
			index (str) = name
				*or (int) - index of ui name
		returns:
			(str) corresponding ui name.
		'''
		if not 'name' in self._sbDict:
			self._sbDict['name'] = []

		if not type(index)==int:
			index = self.getUiIndex(index) #get index using name

		self._sbDict['name'].append(self.uiList(name=True)[index])

		return self._sbDict['name'][-1]


	def getUiName(self, ui=None, camelCase=False, pascalCase=False):
		'''
		Property.
		Get the ui name as a string.
		If no argument is given, the name for the current ui will be returned.

		args:
			ui (obj) = (optional) use ui object to get its corresponding name. (the default behavior is to return the current ui name)
			camelCase (bool) = (optional) return name with first letter lowercase. (default: False)
			pascalCase (bool) = (optional) return name with first letter capitalized. (default: False)
		returns:
			(str) - ui name.
		'''
		if not 'name' in self._sbDict:
			self._sbDict['name']=[]

		if ui:
			return next(k for k, value in self.uiList().items() if value==ui)

		try:
			name = self._sbDict['name'][-1]
			if pascalCase:
				name = name[:1].capitalize()+name[1:] #capitalize the first letter
			if camelCase:
				name = name[0].lower()+name[1:] #lowercase the first letter
			return name
		except: #if index out of range (no value exists): return None
			return None


	def getUiIndex(self, name=False):
		'''
		Property.
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
		Property.
		Set the X (width) value for the current ui.

		args:
			name (str) = the name of the ui to set the width for.
			width (int) = X size as an int
		'''
		height = self.getUiSize(name=name, height=True) #get the hight value.
		self.setUiSize(name=name, width=width, height=height)


	def setUiSizeY(self, height, name=None):
		'''
		Property.
		Set the Y (height) value for the current ui.

		args:
			name (str) = the name of the ui to set the height for.
			height (int) = Y size as an int
		'''
		width = self.getUiSize(name=name, width=True) #get the width value.
		self.setUiSize(name=name, height=height, width=width)


	def getUiSize(self, name=None, width=None, percentWidth=None, height=None, percentHeight=None): #get current ui size info.
		'''
		Property.
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
		Property.
		Get the X (width) value for the current ui.

		args:
			name (str) = ui name to get size from.
		returns:
			returns width as int
		'''
		return self.getUiSize(name=name, width=True)


	def getUiSizeY(self, name=None):
		'''
		Property.
		Get the Y (height) value for the current ui.

		args:
			name (str) = ui name to get size from.
		returns:
			returns width as int
		'''
		return self.getUiSize(name=name, height=True)


	def getNameFromWidget(self, widget):
		'''
		Get the ui name from the given widget.

		args:
			widget (obj) = QWidget
		returns:
			 (str) ui name. ie. 'polygons' from <somewidget>
		'''
		return next((k for k,v in _sbDict.items() if type(v) is dict and 'widgets' in v and widget in v['widgets']), None)


	def setMainAppWindow(self, app):
		'''
		Property.
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
		Property.
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
		Property.
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

		if not name in self._sbDict:
			self._sbDict[name] = {}

		if callable(class_):
			self._sbDict[name]['class'] = class_()
		else:
			self._sbDict[name]['class'] = class_


		return self._sbDict[name]['class']


	def getClassInstance(self, class_):
		'''
		Property.
		Case insensitive. (Class string keys are lowercase and any given string will be converted automatically)
		If class is not in self._sbDict, getClassInstance will attempt to use setClassInstance() to first store the class.

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

		if not 'class' in self._sbDict[name]:
			return self.setClassInstance(class_) #construct the signals and slots for the ui

		return self._sbDict[name]['class']


	def getWidget(self, objectName=None, name=None):
		'''
		Property.
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

		if not 'widgets' in self._sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		if objectName:
			return next((w for w in self._sbDict[name]['widgets'].values() if w['widgetName']==objectName), None)
		else:
			return [w for w in self._sbDict[name]['widgets'].keys()]


	def getWidgetName(self, widget=None, name=None):
		'''
		Property.
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

		if not 'widgets' in self._sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		if widget:
			return self._sbDict[name]['widgets'][widget]['widgetName']

		if name and not widget: #return all objectNames from ui name.
			return [w['widgetName'] for w in self._sbDict[name]['widgets'].values()]
		else: #return all objectNames:
			return [w['widgetName'] for k,w in self._sbDict.items() if k=='widgets']


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
			objectName = self._sbDict[name]['widgets'][widget] #use the stored objectName as a more reliable key.
			widget = self.getWidget(objectName, name) #use the objectName to get a string key for 'widget'

		if not name:
			name = self.getUiName()

		if not 'widgets' in self._sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui
		# print(name, widget)
		try:
			return self._sbDict[name]['widgets'][widget]['widgetType']
		except KeyError:
			return None


	def getDerivedType(self, widget, name=None):
		'''
		Get widget derived type class name as a string.
		ie. 'QPushButton' from a custom subclassed pushbutton.

		args:
			widget (str)(obj) = widget or objectName.
			name (str) = ui name.
		returns:
			'string' - the corresponding widget derived class name
		'''
		if isinstance(widget, (str, unicode)):
			objectName = self._sbDict[name]['widgets'][widget] #use the stored objectName as a more reliable key.
			widget = self.getWidget(objectName, name) #use the objectName to get a string key for 'widget'

		if not name:
			name = self.getUiName()

		if not 'widgets' in self._sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		return self._sbDict[name]['widgets'][widget]['derivedType']


	def getMethod(self, name, widget=None):
		'''
		args:
			name (str) = name of class. ie. 'polygons'
			widget (str)(obj) = widget, widget's objectName, or method name.
		returns:
			if widget: corresponding method object to given widget.
			else: all of the methods associated to the given ui name as a list.
		ex. sb.getMethod('polygons', <b022>)() #call method <b022> of the 'polygons' class
		'''
		if not 'widgets' in self._sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		if widget:
			try:
				if type(widget) is str:
					return next(w['method'][0] for w in self._sbDict[name]['widgets'].values() if w['widgetName']==widget) #if there are event filters attached (as a list), just get the method (at index 0).
				return self._sbDict[name]['widgets'][widget]['method'][0] #if there are event filters attached (as a list), just get the method (at index 0).
			except:
				if type(widget) is str:
					return next((w['method'] for w in self._sbDict[name]['widgets'].values() if w['widgetName']==widget), None)
				return self._sbDict[name]['widgets'][widget]['method']
		else:
			return [w['method'] for w in self._sbDict[name]['widgets'].values()]


	def getDocString(self, name, widgetName, all_=False):
		'''
		args:
			name (str) = optional name of class. ie. 'polygons'. else, use current name.
			widgetName (str) = name of method. ie. 'b001'
			all_ = bool return entire unedited docString
		returns:
			if all_: the entire stored docString
			else: edited docString; name of method
		'''
		if not 'widgets' in self._sbDict[name]:
			self.widgets(name) #construct the signals and slots for the ui

		docString = next(w['docString'] for w in self._sbDict[name]['widgets'].values() if w['widgetName']==widgetName)
		if docString and not all_:
			return docString.strip('\n\t') #return formatted docString
		else:
			return docString #return entire unformatted docString, or 'None' is docString==None.


	def previousName(self, previousIndex=False, allowDuplicates=False, allowLevel0=False, allowLevel1=True, allowLevel2=True, allowCurrent=False, as_list=False):
		'''
		Property.
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


	def gcProtect(self, obj=None, clear=False):
		'''
		Protect given object from garbage collection.

		args:
			obj (obj) = obj to add to the protected list.
		returns:
			(list) of protected objects.
		'''
		if not 'gcProtect' in self._sbDict:
			self._sbDict['gcProtect']=[]

		if clear:
			return self._sbDict['gcProtect'][:]

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
		ie. hasKey('polygons', 'widgets', 'objectName')

		args:
			'string' dict keys in order of hierarchy.  ie. 'polygons', 'widgets', 'b001', 'method'
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


	def getParentKeys(self, nested_dict, value):
		'''
		Get all parent keys from a nested value.

		args:
			nested_dict (dict) = 
			value (value) = 
		returns:
			(list) parent keys

		ex. call:
		getParentKeys(_sbDict, 'cmb002') returns all parent keys of the given value. ex. ['polygons', 'widgets', '<widgets.QComboBox_.QComboBox_ object at 0x0000016B6C078908>', 'widgetName'] ...
		'''
		for k,v in nested_dict.items():
			if type(v) is dict:
				p = self.getParentKeys(v, value)
				if p:
					return [k]+p
			elif v==value:
				return [k]


	def get(self, nested_dict, obj, type_='value', nested_list=[]):
		'''
		Get objects from any nested dict in _sbDict using a given key or value.

		args:
			nested_dict (dict) = 
			obj (key)(value) = 
			type_ (str) = 
			nested_list (list) = 
		returns:
			(list) keys or values.

		ex. call:
		self.get(self._sbDict, 'cmb002', 'nameFromValue') #returns a list of all ui names containing 'cmb002' values.
		'''
		for k,v in nested_dict.items():
			if type_ is 'valuesFromKey': 
				if k==obj: #found key
					nested_list.append(v)

			elif type_ is 'keysFromValue':
				if v==obj: #found value
					nested_list.append(k)

			elif type_ is 'namesFromValue':
				if v==obj: #found value
					nested_list.append(self.getParentKeys(self._sbDict, v)[0])

			if type(v) is dict: #found dict
				p = get(v, obj, type_, nested_list) #recursive call
				if p:
					return p
		return nested_list


	def getSubmenu(self, ui):
		'''
		Get the submenu object of the given ui using it's name string, or the parent ui object.

		args:
			ui (str) = ui name.
				<ui object> - dynamic ui.
		'''
		if not isinstance(ui, (str, unicode)):
			name = self.getUiName(ui) #get name using ui object.
		if 'submenu' not in name:
			name = name+'_submenu'

		return self.getUi(name)


	def getUiLevel(self, name=False):
		'''
		Property.
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


	def prefix(self, widget, prefix=None):
		'''
		Get or Query the widgets prefix.
		A valid prefix is returned when the given widget's objectName startswith an alphanumeric char, followed by at least three integers. ex. i000 (alphanum,int,int,int)

		ex. prefix('i023') returns 'i'
		if the second 'prefix' arg is given, then the method checks if the given objectName has the prefix, and the return value is bool.

		args:
			widget (str)(obj) = widget or it's objectName.
			prefix (str)(list) = optional; check if the given objectName startwith this prefix.
		returns:
			if prefix arg given:
				(bool) - True if correct format else; False.
			else:
				(str) alphanumeric 'string' 

		ex call: sb.prefix(widget, ['b', 'v', 'i'])
		'''
		if prefix is not None: #check the actual prefix against the given prefix and return bool.
			prefix = sb.list_(prefix) #if 'widgets' isn't a list, convert it to one.

			name = self.getUiName()
			for p in prefix:
				try:
					if isinstance(widget, (str, unicode)): #get the prefix using the widget's objectName.
						prefix_ = next(w['prefix'] for w in self._sbDict[name]['widgets'].values() if w['widgetName']==widget)
					else:
						prefix_ = self._sbDict[name]['widgets'][widget]['prefix']
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
	def list_(x):
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
	getWidgetNames = property(getWidgetName)





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
				'widgets': {'<widgets.QComboBox_.QComboBox_ object at 0x0000016B6C078908>': {
									'widgetName': 'cmb002', 
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

	# def getWidgets(self, name=None):
	# 	'''
	# 	Get Property.
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
# 	for name, v in self._sbDict.items():
# 		if type(v)==dict:
# 			for k, v in v.items():
# 				if type(v)==dict:
# 					for k, v in v.items():
# 						if type(v)==dict:
# 							for k, v in v.items():
# 								if v==obj:
# 									return name