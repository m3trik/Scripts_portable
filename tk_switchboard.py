from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

from pydoc import locate

import sys, os.path






# ------------------------------------------------
#	Manage Ui elements
# ------------------------------------------------
class Switchboard(object):
	'''
	Get/set elements across modules from a single dictionary.
	
	ui name/corresponding class name - should always be the same. (case insensitive)
	ui files are looked for in a sub dir named 'ui'.

	widget name/corresponding method name - need to be the same.
	custom widget modules are looked for in a sub directory named 'widgets'. The module name and custom widget class name need to be identical.

	structure:
	_sbDict = {	
		'<ui name>' : {
					'ui' : <ui object>,
					'size' : [<width int>, <height int>],
					'class' : <Class>,
					'widgetDict' : {
								'<widget name>':{
											'widget':<widget>,
											'widgetWithSignal':<widget.signal>,
											'widgetType':'<widgetClassName>',
											'derivedType':'<derivedClassName>',
											'widgetClassInstance':<Class>,
											'method':<method>,
											'docString':'method docString'
								}
					}
		}
		'name' : [string list]} Tracks the order in which the uis are called. A new ui is placed at element[-1]. ie. ['previousName2', 'previousName1', 'currentName']
		'prevCommand' : [list of 2 element lists] ie. [history of commands, last used method at element[-1]]. [[method,'methodNameString']]  ie. [{b00, 'multi-cut tool'}]
		'mainAppWindow' : parent application. ie. <maya Window object>
		'gcProtect' : [items protected from garbage collection]
	}

	the widgetDict is built a'la carte for each class when addSignal (or any other dependant method) is called.
	'''

	app = QApplication.instance() #get the app instance if it exists (required by the QUiLoader)
	if not app:
		app = QApplication(sys.argv)


	global uiLoader, widgetPath, uiPath
	uiLoader = QUiLoader()

	#get path to the directory containing the custom widgets.
	widgetPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'widgets')
	#register any custom widgets
	widgetNames = [file_.replace('.py','',-1) for file_ in os.listdir(widgetPath) if file_.endswith('.py') and not file_.startswith('__')]
	[uiLoader.registerCustomWidget(locate('widgets.'+m+'.'+m)) for m in widgetNames]


	#set path to the directory containing the ui files.

	uiPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui') #get absolute path from dir of this module + relative path to directory
	#initialize _sbDict
	_sbDict = {file_.replace('.ui',''):{'ui':uiLoader.load(uiPath+'/'+file_)} for file_ in os.listdir(uiPath) if file_.endswith('.ui')}



	def __init__(self, parent=None):
		if parent: #check for parent, so that if another instance of switchboard is called without arguments, it doesn't overwrite setMainAppWindow to None.
			self.setMainAppWindow(parent)






	def buildWidgetDict(self, name):
		'''
		Add the signal/slot connections for each widget in a given ui.

		The signalType dict establishes what type widgets will be added to the widgetDict, and what associated signal to apply.
		Following that, the items in the ui are looped over, and the widgets' method resolution order is checked against the signalType keys
		to determine the correct derived class type (used in the case of a custom widget).
		args:
			name='string' - name of the ui to construct connections for.
		returns:
			dict - 'widgetName':{'widget':<widget>,'widgetWithSignal':<widgetWithSignal>,'method':<method>,'docString':'docString','widgetClassInstance':<class object>,'widgetClassName':'class name'}
		'''
		ui = self.getUi(name)
		pathToSlots = 'tk_slots_'+self.getMainAppWindow(objectName=True)+'_'+name+'.'+name[0].upper()+name[1:] #ie. tk_slots_maya_init.Init
		class_ = self.setClassInstance(pathToSlots)


		signalType = {'QMainWindow':'',
					'QWidget':'',
					'QProgressBar':'valueChanged',
					'QPushButton':'released',
					'QSpinBox':'valueChanged',
					'QDoubleSpinBox':'valueChanged',
					'QCheckBox':'released',
					'QComboBox':'currentIndexChanged',
					'QLineEdit':'returnPressed',
					'QTextEdit':'textChanged'}


		for widgetName, widget in ui.__dict__.items(): #for each object in the ui:
			for d in widget.__class__.__mro__:
				if d.__name__ in signalType:
					derivedType = d.__name__
					signal = signalType[derivedType]


					widgetWithSignal = getattr(widget, signal, None) #add signal to widget
					method = getattr(class_, widgetName, None) #use 'widgetName' (ie. b006) to get the corresponding method of the same name.
					docString = getattr(method, '__doc__', None)

					#add values to widgetDict
					self.widgetDict(name).update(
								{widgetName:{'widget':widget, 
											'widgetWithSignal':widgetWithSignal,
											'widgetType':widget.__class__.__name__,
											'derivedType':derivedType,
											'widgetClassInstance':widget.__class__(),
											'method':method,
											'docString':docString}})

					break #stop looping up the chain of mro types found in signalType once a type match is found.

		# print self.widgetDict(name)
		return self.widgetDict(name)



	def widgetDict(self, name):
		'''
		Dictionary holding widget information.
		Used primarily by 'buildWidgetDict' method to construct signal and slot connections that can later be connected and disconnected by the add/removeSignal methods. 
		args:
			name='string' name of ui/class. ie. 'polygons'
		returns:
			connection dict of given name with widget/method name string as key.
		ex.
		'widget':ui object.  ie. b001
		'widgetWithSignal':ui object with signal attached. ie. b001.connect
		'method':class method object for the corresponding ui widget. ie. main.b001
		'docString': string description of command from method docString.  ie. 'Multi-Cut Tool'}
		#ie. {'b001':{'widget':b001, 'widgetWithSignal':b001.onPressed, 'method':main.b001, 'docString':'Multi-Cut Tool'}},
		'''
		if not 'widgetDict' in self._sbDict[name]:
			self._sbDict[name]['widgetDict'] = {}
			self.buildWidgetDict(name) #construct the signals and slots for the ui

		return self._sbDict[name]['widgetDict']



	def addSignal(self, name):
		'''
		Connects signals/slots from the widgetDict for the given ui. Works with both single slots or multiple slots given as a list.
		args:
			name='string' - ui name
		'''
		for widgetName in self.widgetDict(name):
			signal = self.getSignal(name, widgetName)
			slot = self.getMethod(name, widgetName)
			# print 'addSignal: ', signal, slot
			try:
				signal.connect(slot) #add single slot (main and viewport)
			except:
				try:
					map(signal.connect, slot) #add multiple slots from a list.
				except Exception as error:
					if slot:
						print '# Error: addSignal '+name+' '+widgetName+str(signal)+str(slot)+' #' #, error



	def removeSignal(self, name):
		'''
		Disconnects signals/slots from the widgetDict for the given ui. Works with both single slots or multiple slots given as a list.
		args:
			name='string' - ui name
		'''
		for widgetName in self.widgetDict(name):
			signal = self.getSignal(name, widgetName)
			slot = self.getMethod(name, widgetName)
			# print 'removeSignal: ', signal, slot
			try:
				signal.disconnect(slot) #add single slot (main and viewport)
			except: 
				try:
					map(signal.disconnect, slot) #add multiple slots from a list.
				except Exception as error:
					if slot:
						print '# Error: removeSignal '+name+' '+widgetName+str(signal)+str(slot)+' #' #, error



	def uiList(self, name=False, ui=False):
		'''
		Get a list of either all ui names, all ui object's, or both as key/value pairs in a dict.
		args:
			name=bool 	return string ui list
			ui=bool 	return dynamic ui list
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
			name='string' name of class. ie. 'polygons' (by default getUi returns the current ui)
		returns:
			if name: corresponding dynamic ui object of given name from the key 'uiList'.
			else: current dynamic ui object
		'''
		if not name:
			name = self.getUiName()

		return self.uiList(ui=True)[self.getUiIndex(name)]



	def setUiName(self, index):
		'''
		The 'name' list is used for various things such as; maintaining a history of ui's that have been called previously.
		args:
			index='string' - name
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
			ui=<ui object> - (optional) use ui object to get its corresponding name. (the default behavior is to return the current ui name)
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
			name='string' name of class. ie. 'polygons'
		returns:
			if name: index of given name from the key 'uiList'.
			else: index of current ui
		'''
		if name:
			return self.uiList(name=True).index(name)
		else:
			return self.uiList(name=True).index(self.getUiName())



	def getNameFrom(self, obj):
		'''
		Get the ui(class) name from any object existing in widgetDict.
		args:
			obj=<object> - 
		returns:
			 'string' - the corresponding method name from the given object.
			 ie. 'polygons' from <widget>
		'''
		for key, v in self._sbDict.iteritems():
			if type(v)==dict:
				for k, v in v.iteritems():
					if type(v)==dict:
						for k, v in v.iteritems():
							if type(v)==dict:
								for k, v in v.iteritems():
									if v==obj:
										return key



	def setMainAppWindow(self, app):
		'''
		Set parent application.
		args:
			app=app object.
		returns:
			string name of app
		'''
		self._sbDict['mainAppWindow'] = app

		return self._sbDict['mainAppWindow']



	def getMainAppWindow(self, objectName=False):
		'''
		Get parent application if any.
		args:
			objectName=bool - get string name of app. (by default getMainAppWindow returns app object)
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
				return app.objectName().rstrip('Window').lower()
		else:
			return app



	def setUiSize(self, name=None, size=None): #store ui size.
		'''
		Set UI size. If no size is given, the minimum ui size needed to frame its
		contents will be used. If no name is given, the current ui will be used.
		args:
			name='string' - optional ui name
			size=[int, int] - optional width and height as an integer list. [width, height]
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



	def getUiSize(self, width=None, percentWidth=None, height=None, percentHeight=None): #get current ui size info.
		'''
		args:
			width=int 	returns width of current ui
			height=int 	returns hight of current ui
			percentWidth=int returns a percentage of the width
			percentHeight=int returns a percentage of the height
		returns:
			if width: returns width as int
			if height: returns height as int
			if percentWidth: returns the percentage of the width as an int
			if percentHeight: returns the percentage of the height as an int
			else: ui size info as integer values in a list. [width, hight]
		'''
		if width:
			return self._sbDict[self.getUiName()]['size'][0]
		elif height:
			return self._sbDict[self.getUiName()]['size'][1]
		elif percentWidth:
			return self._sbDict[self.getUiName()]['size'][0] *percentWidth /100
		elif percentHeight:
			return self._sbDict[self.getUiName()]['size'][1] *percentHeight /100
		else:
			return self._sbDict[self.getUiName()]['size']



	def setClassInstance(self, class_):
		'''
		Case insensitive. Class string keys are stored lowercase regardless of how they are recieved.
		args:
			class_='string' *or <class object> - module name.class to import and store class. 
					ie.  ie. 'polygons', 'tk_slots_max_polygons.Polygons', or <tk_slots_max_polygons.Polygons>
		returns:
			class object.
		'''
		if type(class_)==str or type(class_)==unicode: #if arg given as string or unicode:
			name = class_.split('_')[-1].split('.')[-1].lower(); #get key from class_ string ie. 'class' from 'module.Class'
			class_ = locate(class_)

		else: #if arg as <object>:
			name = class_.__class__.__name__.lower();

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
			class_='string' name of class *or <class object>
				ie. 'polygons', 'tk_slots_max_polygons.Polygons', or <tk_slots_max_polygons.Polygons>
		returns:
			class object.
		'''
		if type(class_)==str or type(class_)==unicode: #if arg given as string or unicode:
			name = class_.lower()
		else: #if arg as <object>:
			if not callable(class_):
				return None
			name = class_.__class__.__name__.lower();

		if not 'class' in self._sbDict[name]:
			return self.setClassInstance(name) #construct the signals and slots for the ui

		return self._sbDict[name]['class']



	def getWidget(self, name, widgetName=None):
		'''
		Case insensitive. Get the widget object from its name.
		args:	
			name='string' - name of ui. ie. 'polygons'. If no name is given, the current ui will be used.
			widgetName='string' - optional name of widget. ie. 'b000'
		returns:
			if widgetName: widget object with the given name.
			else: all widgets from the given ui.
		'''
		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui

		if widgetName:
			return self._sbDict[name]['widgetDict'][widgetName]['widget']
		else: #return all widgets:
			return [self._sbDict[name]['widgetDict'][widgetName]['widget'] for widgetName in self._sbDict[name]['widgetDict']]



	def getWidgetClassInstance(self, widget, name=None):
		'''
		ie. returns <type 'PySide2.QtWidgets.QPushButton'> or, <class 'widgets.QComboBox_Popup.QComboBox_Popup'>
		args:
			widget='string'  - name of widget
					*or <object> - widget
			name='string' - name of dynamic ui (else use current ui)
		returns:
			<class object> - the corresponding widget class
		'''
		if not type(widget)==str:
			widget = widget.objectName()

		if not name:
			name = self.getUiName()

		try:
			if not 'widgetDict' in self._sbDict[name]:
				self.widgetDict(name) #construct the signals and slots for the ui
		except Exception as error:
			if not type(error)==KeyError:
				raise error
			return widget.__class__()

		return self._sbDict[name]['widgetDict'][widget]['widgetClassInstance']



	def getWidgetType(self, widget, name=None):
		'''
		Get widget type class name as a string.
		ie. 'QPushButton' from pushbutton type widget.
		args:
			widget='string'  - name of widget/widget
				*or <object> -widget
			name='string' - name of dynamic ui (else use current ui)
		returns:
			'string' - the corresponding widget class name
		'''
		if not type(widget)==str:
			widget = widget.objectName() #use the objectName to get a string key for 'widget'

		if not name:
			name = self.getUiName()

		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui

		return self._sbDict[name]['widgetDict'][widget]['widgetType']



	def getDerivedType(self, widget, name=None):
		'''
		Get widget derived type class name as a string.
		ie. 'QPushButton' from a custom subclassed pushbutton.
		args:
			widget='string'  - name of widget/widget
				*or <object> -widget
			name='string' - name of dynamic ui (else use current ui)
		returns:
			'string' - the corresponding widget derived class name
		'''
		if not type(widget)==str:
			widget = widget.objectName() #use the objectName to get a string key for 'widget'

		if not name:
			name = self.getUiName()

		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui

		return self._sbDict[name]['widgetDict'][widget]['derivedType']



	def getMethod(self, name, methodName=None):
		'''
		args:
			name='string' name of class. ie. 'polygons'
			methodName='string' optional name of method. ie. 'b001'
		returns:
			if methodName: corresponding method object to given method name string.
			else: all of the methods associated with the given name as a list.
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



	def getSignal(self, name, widgetName=None):
		'''
		args:
			name='string' name of ui. ie. 'polygons'
			widgetName='string' optional widget name. ie. 'b001'
		returns:
			if widgetName: the corresponding widget object with attached signal (ie. b001.onPressed) of the given widget name.
			else: all of the signals associated with the given name as a list.
		'''
		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui

		if widgetName:
			return self._sbDict[name]['widgetDict'][widgetName]['widgetWithSignal']
		else:
			return [self._sbDict[name]['widgetDict'][widgetName]['widgetWithSignal'] for widgetName in self._sbDict[name]['widgetDict']]



	def getDocString(self, name, methodName, full=False):
		'''
		args:
			name='string' optional name of class. ie. 'polygons'. else, use current name.
			methodName='string' name of method. ie. 'b001'
			full=bool return full unedited docString
		returns:
			if full: full stored docString
			else: edited docString; name of method
		'''
		if not 'widgetDict' in self._sbDict[name]:
			self.widgetDict(name) #construct the signals and slots for the ui

		docString = self._sbDict[name]['widgetDict'][methodName]['docString']
		if docString and not full:
			docString.strip('\n\t') #return formatted docString
		else:
			return docString #return entire unformatted docString. In some cases 'None'.



	def previousName(self, previousIndex=False, allowDuplicates=False, allowInit=False, as_list=False):
		'''
		Get the previously called ui name string, or a list of ui name strings ordered by use. ie. ['previousName2', 'previousName1', 'currentName']
		args:
			previousIndex=bool - return the index of the last valid previously opened ui name.
			allowDuplicates=bool - applicable when returning as_list. Returns the list allowing for duplicate names.
			allowInit=bool - keep instances of init. Default is Off.
			as_list=bool - returns the full list of previously called names. By default duplicates are removed.
		returns:
			with no arguments given - string name of previously opened layout.
			if previousIndex: int - index of previously opened ui
			if as_list: returns [list of string names]
		'''
		if not 'name' in self._sbDict:
			self._sbDict['name'] = []

		self._sbDict['name'] = self._sbDict['name'][-50:] #keep original list length restricted to last fifty elements

		if allowInit:
			list_ = [i for i in self._sbDict['name']] #work on a copy of the list, keeping the original intact
		else:	
			list_ = [i for i in self._sbDict['name'] if 'init' not in i] #work on a copy of the list, removing any instances of 'init', keeping the original intact
		
		if not allowDuplicates:
			[list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous duplicates if they exist; keeping the last added element.

		if previousIndex:
			validPrevious = [i for i in list_ if all(['viewport' not in i, 'main' not in i])]
			return self.getUiIndex(validPrevious[-2])

		elif as_list:
			return list_

		else:
			try:
				return list_[-2]
			except:
				return ''



	def prevCommand(self, docString=False, method=False, as_list=False):
		'''
		args:
			docString=bool 		return docString of last command
			methodList=bool 	return method of last command
		returns:
			if docString: 'string' description (derived from the last used command method's docString)
			if docString AND as_list: [string list] all docStrings, in order of use, as a list
			if method: method of last used command.
			if method AND as_list: [<method object> list} all methods, in order of use, as a list
			if as_list: list of lists with <method object> as first element and <docString> as second. 'prevCommand':[[b001, 'multi-cut tool']] }
			else : <method object> of the last used command
		'''
		if not 'prevCommand' in self._sbDict: self._sbDict['prevCommand'] = [] #initialize list

		self._sbDict['prevCommand'] = self._sbDict['prevCommand'][-20:] #keep original list length restricted to last 20 elements

		list_ = self._sbDict['prevCommand']
		[list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous duplicates if they exist; keeping the last added element.

		if docString and as_list:
			try:
				return [i[1] for i in list_]
			except:
				return None

		elif docString:
			try:
				return list_[-1][1]
			except:
				return ''

		elif method and as_list:
			try:
				return [i[0] for i in list_]
			except:
				return ['# No commands in history. #']

		elif method:
			try:
				return list_[-1][0]
			except:
				return ''
		
		elif as_list:
			return list_

		else:
			try:
				return list_[-1][0]
			except:
				return None



	def previousView(self, previousIndex=False, allowDuplicates=False, as_list=False):
		'''
		args:
			previousIndex=bool 	return the index of the last valid previously opened ui name.
		returns:
			if previousIndex: int index of previously opened ui
			else: string name of previously opened layout.
		'''
		if not 'name' in self._sbDict:
			self._sbDict['name'] = []

		self._sbDict['name'] = self._sbDict['name'][-10:] #keep original list length restricted to last ten elements

		list_ = [i for i in self._sbDict['name'] if 'init' not in i] #work on a copy of the list, removing any instances of 'init', keeping the original intact
		if not allowDuplicates:
			[list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous duplicates if they exist; keeping the last added element.

		if previousIndex:
			validPrevious = [i for i in list_ if all(['viewport' not in i, 'main' not in i])]
			return self.getUiIndex(validPrevious[-2])

		elif as_list:
			return list_

		else:
			try:
				return list_[-2]
			except:
				return ''



	def gcProtect(self, obj):
		'''
		Protect given object from garbage collection.
		args:
			obj=<object>
		'''
		if not 'gcProtect' in self._sbDict:
			self._sbDict['gcProtect']=[]
		self._sbDict['gcProtect'].append(obj)



	def dict_(self):
		'''
		returns:
			full switchboard dict
		'''
		return self._sbDict



	def hasKey(self, *args): #check if key exists in switchboard dict.
		'''
		ie. hasKey('polygons', 'widgetDict', 'widgetName')
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



	@staticmethod
	def qApp_getWindow(name=None):
		'''
		Get Qt window/s
		args:
			name='string' - optional name of window (widget.objectName)
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
			name='string' - optional name of widget (widget.objectName)
		returns:
			if name: corresponding <widget object>
			else: return a dictionary of all widgets {widgetName:widget}
		'''
		widgets = {w.objectName():w for w in QApplication.allWidgets()}
		if name:
			return widgets[name]
		else:
			return widgets









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

'''
test example:
_sbDict={
	'polygons':{'class': '<Polygons>',
				'ui': '<polygons ui object>', 
				'size': [295, 234],
				'widgetDict': {'b001':{'widget':'<b001>', 'widgetWithSignal':'<b001.connect>', 'method':'<main.b001>', 'docString':'Multi-Cut Tool', 'widgetClassInstance':'<QPushButton>', 'widgetType':'QPushButton'}}},
	'mainAppWindow': None,
	'name': ['polygons'],
	'prevCommand': [['b000', 'multi-cut tool']],
	'gcProtect': ['<protected object>']}
'''