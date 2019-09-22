from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

from pydoc import locate

import sys, os.path





# ------------------------------------------------
#	Manage Ui elements
# ------------------------------------------------
class Switchboard():
	'''
	Get/set elements across modules from a single dictionary.
	
	ui name/corresponding class name - should always be the same. (case insensitive)
	widget name/corresponding method name - also need to be the same.

	structure:
	_sbDict = {	
		'(ui name)'{
			'class' : <Class>
			'size' : [(width) int, (height) int]
			'connectionDict' : {'(widget name)':{'widget':<widget>, 'widgetWithSignal':<widget.signal>, 'method':<method>, 'docString':'', 'widgetClass':<Class>, widgetType':'Class'}
			}
		'uiList' : [list of two element lists] containing all ui filenames in the ui folder and their corresponding dynamic ui object. ie. [['polygons', <polygons dynamic ui object>]]
		'name' : [string list]} Tracks the order in which the uis are called. A new ui is placed at element[-1]. ie. ['previousName2', 'previousName1', 'currentName']
		'prevCommand' : [list of 2 element lists] ie. [history of commands, last used method at element[-1]]. [[method,'methodNameString']]  ie. [{b00, 'multi-cut tool'}]
		'app' : 'string name' of the parent application. ie. 'maya' or 'max'
		'gcProtect' : [items protected from garbage collection]
	}

	dict structure at constructor:
	_sbDict={
	'name':[],
	'polygons':{},
	'uiList:[['polygons', '<polygons ui object>']],
	'app':'maya'
	}

	the connectionDict is built a'la carte for each class when addSignal (or any other dependant method) is called.
	'''

	_sbDict = {'name':[]}

	#set path to the directory containing the ui files.
	path = os.path.join(os.path.dirname(__file__), 'ui') #get absolute path from dir of this module + relative path to directory

	#construct the uiList from directory contents. ie. [['polygons', <polygons dynamic ui object>]]
	qApp = QApplication.instance() #get the qApp instance if it exists (for the QUiLoader)
	if not qApp:
		qApp = QApplication(sys.argv)

	_sbDict['uiList'] = [[file_.replace('.ui',''), QUiLoader().load(path+'/'+file_)] for file_ in os.listdir(path) if file_.endswith('.ui')]
	 #use the uiList to initialize the main dict keys. ie. { 'edit':{}, 'create':{}, 'animation':{}, 'cameras':{}, 'display':{} }
	[_sbDict.update({ui[0]:{}}) for ui in _sbDict['uiList']]


	def __init__(self, parent=None):
		if parent:
			self.setApp(parent)






	def buildConnectionDict(self, name):
		'''
		Add the signal/slot connections for each widget in a given ui.
		args:
			name='string' - name of the ui to construct connections for.
		returns:
			dict - 'widgetName':{'widget':<widget>,'widgetWithSignal':<widgetWithSignal>,'method':<method>,'docString':'docString','widgetClass':<class object>,'widgetClassName':'class name'}
		'''
		ui = self.getUi(name)
		class_ = self.setClassInstance('tk_slots_'+self.getApp()+'_'+name+'.'+name[0].upper()+name[1:]) #ie. tk_slots_maya_init.Init


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

		for widgetName, widget in ui.__dict__.iteritems(): #for each object in the ui:
			for widgetType, signal in signalType.iteritems():
				if widgetType==widget.__class__.__name__: #if it is a type listed in the signalType dict, construct with the associated signal.

					widgetWithSignal = getattr(widget, signal, None) #add signal to widget
					method = getattr(class_, widgetName, None) #use 'widgetName' (ie. b006) to get the corresponding method of the same name.
					docString = getattr(method, '__doc__', None)

					#add values to connectionDict
					self.getConnectionDict(name).update(
								{widgetName:{'widget':widget, 
											'widgetWithSignal':widgetWithSignal,
											'widgetType':widgetType,
											'widgetClass':widget.__class__,
											'method':method,
											'docString':docString}})

		# print self.getConnectionDict(name)
		return self.getConnectionDict(name)



	def getConnectionDict(self, name):
		'''
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
		if not 'connectionDict' in self._sbDict[name]:
			self._sbDict[name]['connectionDict'] = {}
			self.buildConnectionDict(name) #construct the signals and slots for the ui

		return self._sbDict[name]['connectionDict']



	def addSignal(self, name):
		'''
		Connects signals/slots from the connectionDict for the given ui. Works with both single slots or multiple slots given as a list.
		args:
			name='string' - ui name
		'''
		for widgetName in self.getConnectionDict(name):
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
		Disconnects signals/slots from the connectionDict for the given ui. Works with both single slots or multiple slots given as a list.
		args:
			name='string' - ui name
		'''
		for widgetName in self.getConnectionDict(name):
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
		args:
			name=bool 	return string ui list
			ui=bool 	return dynamic ui list
		returns:
			if name: return list of ordered ui names
			if ui: return list of ordered dynamic ui objects
			else: list of string names of classes(lowercase) from key 'uiList'. ie. ['animation', 'cameras', 'create', 'display', 'edit']
		'''
		if name:
			return [i[0] for i in self._sbDict['uiList']]
		elif ui:
			return [i[1] for i in self._sbDict['uiList']]
		else:
			return self._sbDict['uiList']



	def getUi(self, name=None):
		'''
		args:
			name='string' name of class. ie. 'polygons'
		returns:
			if name: corresponding dynamic ui object of given name from the key 'uiList'.
			else: current dynamic ui object
		'''
		if not name:
			name = self.getUiName()

		return self.uiList(ui=True)[self.getUiIndex(name)]



	def setUiName(self, index):
		'''
		args:
			index='string' - name
				*or int - index of ui name
		returns:
			corresponding ui name as string
		'''
		if not type(index)==int:
			index = self.getUiIndex(index) #get index using name

		self._sbDict['name'].append(self.uiList(name=True)[index])

		return self._sbDict['name'][-1]



	def getUiName(self, ui=None):
		'''
		Get the ui name as a string.
		If no argument is given, the name for the current ui will be returned.
		args:
			ui=<ui object> - use ui object to get its corresponding name.
		returns:
			'string' - ui name.
		'''
		if ui:
			for list_ in self._sbDict['uiList']:
				if list_[1]==ui:
					return list_[0] #return 'cameras' from ['cameras', '<cameras dynamic ui object>']
		try:
			return self._sbDict['name'][-1]
		except: #else if index out of range (no value exists):
			return None



	def getUiIndex(self, name=None):
		'''
		args:
			name='string' name of class. ie. 'polygons'
		returns:
			if name: index of given name from the key 'uiList'.
			else: index of current ui
		'''
		if name:
			return self.uiList(name=1).index(name)
		else:
			return self.uiList(name=1).index(self.getUiName())



	def getNameFrom(self, obj):
		'''
		Get the ui(class) name from any object existing in connectionDict.
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



	def setApp(self, app):
		'''
		args:
			app=app object.
		returns:
			string name of app
		'''
		self._sbDict['app'] = app.objectName().rstrip('Window').lower() #remove 'Window' from objectName ie. 'Maya' from 'MayaWindow' and set lowercase.
		return self._sbDict['app']



	def getApp(self):
		'''
		returns:
			string name of app
		'''
		if not 'app' in self._sbDict:
			self._sbDict['app'] = '' #initialize list

		return self._sbDict['app']



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
			class_='string' *or <class object> - module name and class to import and store class. 
					ie. 'tk_slots_max_polygons.Polygons'
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



	def getClassInstance(self, name):
		'''
		Case insensitive. (Class string keys are lowercase and any given string will be converted automatically)
		If class is not in self._sbDict, getClassInstance will attempt to use setClassInstance() to first store the class.
		args:
			name='string' name of class. ie. 'polygons'
		returns:
			class object.
		'''
		name = name.lower()

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
		if not 'connectionDict' in self._sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui

		if widgetName:
			return self._sbDict[name]['connectionDict'][widgetName]['widget']
		else: #return all widgets:
			return [self._sbDict[name]['connectionDict'][widgetName]['widget'] for widgetName in self._sbDict[name]['connectionDict']]



	def getWidgetClass(self, widget, name=None):
		'''
		args:
			widget='string'  - name of widget/widget
				*or <object> -widget
			name='string' - name of dynamic ui (else use current ui)
		returns:
			<class object> - the corresponding widget class
		'''
		if not type(widget)==str:
			try:
				return widget.__class__
			except:
				widget = widget.objectName()

		if not name:
			name = self.getUiName()

		if not 'connectionDict' in self._sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui

		return self._sbDict[name]['connectionDict'][widget]['widgetClass']



	def getWidgetType(self, widget, name=None):
		'''
		args:
			widget='string'  - name of widget/widget
				*or <object> -widget
			name='string' - name of dynamic ui (else use current ui)
		returns:
			'string' - the corresponding widget class name
		'''
		if not type(widget)==str:
			try:
				return widget.__class__.__name__
			except:
				widget = widget.objectName() #use the objectName to get a string key for 'widget'

		if not name:
			name = self.getUiName()

		if not 'connectionDict' in self._sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui

		return self._sbDict[name]['connectionDict'][widget]['widgetType']



	def getMethod(self, name, methodName=None):
		'''
		args:
			name='string' name of class. ie. 'polygons'
			methodName='string' optional name of method. ie. 'b001'
		returns:
			if methodName: corresponding method object to given method name string.
			else: all of the methods associated with the given name as a list.
		'''
		if not 'connectionDict' in self._sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui
		
		if methodName:
			try:
				return self._sbDict[name]['connectionDict'][methodName]['method'][0] #if there are event filters attached (ie. a list), just get the method.
			except:
				return  self._sbDict[name]['connectionDict'][methodName]['method']
		else:
			return [self._sbDict[name]['connectionDict'][methodName]['method'] for methodName in self._sbDict[name]['connectionDict']]



	def getSignal(self, name, widgetName=None):
		'''
		args:
			name='string' name of ui. ie. 'polygons'
			widgetName='string' optional widget name. ie. 'b001'
		returns:
			if widgetName: the corresponding widget object with attached signal (ie. b001.onPressed) of the given widget name.
			else: all of the signals associated with the given name as a list.
		'''
		if not 'connectionDict' in self._sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui

		if widgetName:
			return self._sbDict[name]['connectionDict'][widgetName]['widgetWithSignal']
		else:
			return [self._sbDict[name]['connectionDict'][widgetName]['widgetWithSignal'] for widgetName in self._sbDict[name]['connectionDict']]



	def getDocString(self, name, methodName, full=False):
		'''
		args:
			name='string' optional name of class. ie. 'polygons'. else; use current name.
			methodName='string' name of method. ie. 'b001'
			full=bool return full unedited docString
		returns:
			if full: full stored docString
			else: edited docString; name of method
		'''
		if not 'connectionDict' in self._sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui
			
		if full: #entire unformatted docString
			return self._sbDict[name]['connectionDict'][methodName]['docString']
		else: #formatted docString
			return self._sbDict[name]['connectionDict'][methodName]['docString'].strip('\n\t')



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
		args:
			'string' dict keys in order of hierarchy.  ie. 'polygons', 'connectionDict', 'b001', 'method'
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
		'app':'maya',
		'name':['polygons'],
		'uiList':[['polygons', '<polygons dynamic ui object>']],

		'polygons':{'class':'<Polygons>', 
					'size':[295, 234],
					'connectionDict':{'b001':{'widget':'<b001>', 'widgetWithSignal':'<b001.connect>', 'method':'<main.b001>', 'docString':'Multi-Cut Tool', 'widgetClass':'<QPushButton>', 'widgetType':'QPushButton'}}},

		'prevCommand':[['b000', 'multi-cut tool']],
		'gcProtect':['<protected object>']}
'''