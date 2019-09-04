from pydoc import locate
from PySide2 import QtCore, QtWidgets
from PySide2.QtUiTools import QUiLoader

import os.path






# ------------------------------------------------
#	Manage Ui elements
# ------------------------------------------------
class Switchboard():
	'''
	Get/set elements across modules from a single dictionary.
	__sbDict -- key/value structure -
		'string name of class'{
			'class' : <class obj>
			'size' : [list containing width int, height int]. ie. [295, 234]
			'connectionDict' : {'widgetName':{'widget':<obj>, 'widgetWithSignal':<obj.connect>, 'method':<obj>, 'docString':'', 'widgetClass':<QPushButton>, widgetType':'QPushButton'}},}
		'uiList' : [list of two element lists containing all ui filenames in the ui folder and their corresponding dynamic ui object]. ie. [['polygons', <polygons dynamic ui object>]]
		'app' : 'string name of the parent application'. ie. 'maya' or 'max'
		'name' : [string list]. when a new ui is called it's name is at element[-1] and the previous ui is at element[-2]. ie. ['previousName', 'previousName', 'currentName']
		'prevCommand' : list of 2 element lists. [history of commands, last used method at element[-1]]. [[method,'methodNameString']]  ie. [{b00, 'multi-cut tool'}]
	ex.
	__sbDict={
		'polygons':{ 
			'class':Polygons, 
			'size':[295, 234], 
			'connectionDict':{'b001':{'widget':b001, 'widgetWithSignal':b001.connect, 'method':main.b001, 'docString':'Multi-Cut Tool', 'widgetClass':QPushButton, widgetType':'QPushButton'}}}
		'uiList':[['animation', <animation dynamic ui object>], ['cameras', <cameras dynamic ui object>], ['create', <create dynamic ui object>], ['display', <display dynamic ui object>]],
		'app':'maya'
		'name':['polygons', 'edit', 'cameras'], 
		'prevCommand':[[b00, 'multi-cut tool']],
	'''
	#initialize the main dict.
	__sbDict = {'name':[]}

	#set path to the directory containing the ui files.
	path = os.path.join(os.path.dirname(__file__), 'ui') #get absolute path from dir of this module + relative path to directory

	#construct the uiList from directory contents. ie. [['polygons', <polygons dynamic ui object>]]
	__sbDict['uiList'] = [[file_.replace('.ui',''), QUiLoader().load(path+'/'+file_)] for file_ in os.listdir(path) if file_.endswith('.ui')]
	 #use the uiList to initialize the main dict. ie. { 'edit':{}, 'create':{}, 'animation':{}, 'cameras':{}, 'display':{} }
	[__sbDict.update({ui[0]:{}}) for ui in __sbDict['uiList']]


	def __init__(self, app=None):
		if app:
			self.setApp(app)





	def buildConnectionDict(self, name):
		'''
		Add the signal/slot connections for each widget in a given ui.
		args:
			name='string' - name of the ui to construct connections for.
		returns:
			dict - 'widgetName':{'widget':<widget>,'widgetWithSignal':<widgetWithSignal>,'method':<method>,'docString':'docString','widgetClass':<class object>,'widgetClassName':'class name'}
		'''
		ui = self.getUi(name)
		class_ = self.setClass('tk_slots_'+self.getApp()+'_'+name+'.'+name[0].upper()+name[1:])() #ie. tk_slots_maya_init.Init


		signalType = {'QMainWindow':'',
					'QWidget':'',
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
		if not 'connectionDict' in self.__sbDict[name]:
			self.__sbDict[name]['connectionDict'] = {}
			self.buildConnectionDict(name) #construct the signals and slots for the ui

		return self.__sbDict[name]['connectionDict']



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
			return [i[0] for i in self.__sbDict['uiList']]
		elif ui:
			return [i[1] for i in self.__sbDict['uiList']]
		else:
			return self.__sbDict['uiList']



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

		return self.uiList(ui=1)[self.getUiIndex(name)]



	def setUiName(self, index):
		'''
		args:
				index=int
		returns:
				corresponding ui name as string
		'''
		self.__sbDict['name'].append(self.uiList(name=1)[index])
		return self.__sbDict['name'][-1]



	def getUiName(self):
		'''
		returns:
				current ui name as string
		'''
		return self.__sbDict['name'][-1]



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



	def setApp(self, app):
		'''
		args:
				app=app object.
		returns:
				string name of app
		'''
		self.__sbDict['app'] = app.objectName().rstrip('Window').lower() #remove 'Window' from objectName ie. 'Maya' from 'MayaWindow' and set lowercase.
		return self.__sbDict['app']



	def getApp(self):
		'''
		returns:
				string name of app
		'''
		if not 'app' in self.__sbDict:
			self.__sbDict['app'] = None #initialize list

		return self.__sbDict['app']



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

		self.__sbDict[name]['size'] = size
		return self.__sbDict[name]['size']



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
			return self.__sbDict[self.getUiName()]['size'][0]
		elif height:
			return self.__sbDict[self.getUiName()]['size'][1]
		elif percentWidth:
			return self.__sbDict[self.getUiName()]['size'][0] *percentWidth /100
		elif percentHeight:
			return self.__sbDict[self.getUiName()]['size'][1] *percentHeight /100
		else:
			return self.__sbDict[self.getUiName()]['size']



	def setClass(self, class_):
		'''
		Case insensitive. class string keys are stored lowercase regardless of how they are recieved.
		args:
				class_='string' *or <class object> - module name and class to import and store class. 
						ie. 'tk_slots_max_polygons.Polygons'
		returns:
				class object.
		'''
		if type(class_)==str or type(class_)==unicode: #arg given as string or unicode:
			name = class_.split('_')[-1].split('.')[-1].lower(); #get key from class_ string ie. 'class' from 'tk_slots_max_polygons.Class'
			if not name in self.__sbDict:
				self.__sbDict[name] = {}
			self.__sbDict[name]['class'] = locate(class_)

		else: #if class_ arg as <object>:
			name = class_.__class__.__name__.lower();
			if not name in self.__sbDict:
				self.__sbDict[name] = {}
			
			self.__sbDict[name]['class'] = class_

		if not self.__sbDict[name]['class']:
			return '# Error: '+class_+' not found. #'
		else:
			return self.__sbDict[name]['class']



	def getClass(self, name):
		'''
		If class is not in self.__sbDict, use setClass() to first store the class.
		Case insensitive. class string keys are lowercase and any given string will be converted automatically.
		args:
				name='string' name of class. ie. 'polygons'
		returns:
				class object.
		'''
		name = name.lower()

		if not 'class' in self.__sbDict[name]:
			return self.setClass(name) #construct the signals and slots for the ui

		return self.__sbDict[name]['class']



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
		if not 'connectionDict' in self.__sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui

		if widgetName:
			return self.__sbDict[name]['connectionDict'][widgetName]['widget']
		else: #return all widgets:
			return [self.__sbDict[name]['connectionDict'][widgetName]['widget'] for widgetName in self.__sbDict[name]['connectionDict']]



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

		if not 'connectionDict' in self.__sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui

		return self.__sbDict[name]['connectionDict'][widget]['widgetClass']



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

		if not 'connectionDict' in self.__sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui

		return self.__sbDict[name]['connectionDict'][widget]['widgetType']



	def getMethod(self, name, methodName=None):
		'''
		args:
				name='string' name of class. ie. 'polygons'
				methodName='string' optional name of method. ie. 'b001'
		returns:
				if methodName: corresponding method object to given method name string.
				else: all of the methods associated with the given name as a list.
		'''
		if not 'connectionDict' in self.__sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui
		
		if methodName:
			try:
				return self.__sbDict[name]['connectionDict'][methodName]['method'][0] #if there are event filters attached (ie. a list), just get the method.
			except:
				return  self.__sbDict[name]['connectionDict'][methodName]['method']
		else:
			return [self.__sbDict[name]['connectionDict'][methodName]['method'] for methodName in self.__sbDict[name]['connectionDict']]



	def getSignal(self, name, widgetName=None):
		'''
		args:
				name='string' name of ui. ie. 'polygons'
				widgetName='string' optional widget name. ie. 'b001'
		returns:
				if widgetName: the corresponding widget object with attached signal (ie. b001.onPressed) of the given widget name.
				else: all of the signals associated with the given name as a list.
		'''
		if not 'connectionDict' in self.__sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui

		if widgetName:
			return self.__sbDict[name]['connectionDict'][widgetName]['widgetWithSignal']
		else:
			return [self.__sbDict[name]['connectionDict'][widgetName]['widgetWithSignal'] for widgetName in self.__sbDict[name]['connectionDict']]



	def getDocString(self, methodName, name=None, full=False):
		'''
		args:
				name='string' optional name of class. ie. 'polygons'. else; use current name.
				methodName='string' name of method. ie. 'b001'
				full=bool return full unedited docString
		returns:
				if full: full stored docString
				else: edited docString; name of method
		'''
		if not name:
			name = self.getUiName()

		if not 'connectionDict' in self.__sbDict[name]:
			self.getConnectionDict(name) #construct the signals and slots for the ui
			
		if full: #entire unformatted docString
			return self.__sbDict[name]['connectionDict'][methodName]['docString']
		else: #formatted docString
			return self.__sbDict[name]['connectionDict'][methodName]['docString'].strip('\n\t')



	def previousName(self, previousIndex=False, allowDuplicates=False, as_list=False):
		'''
		args:
				previousIndex=bool 	return the index of the last valid previously opened ui name.
		returns:
				if previousIndex: int index of previously opened ui
				else: string name of previously opened layout.
		'''
		self.__sbDict['name'] = self.__sbDict['name'][-10:] #keep original list length restricted to last ten elements

		list_ = [i for i in self.__sbDict['name'] if 'init' not in i] #work on a copy of the list, removing any instances of 'init', keeping the original intact
		
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
		if not 'prevCommand' in self.__sbDict: self.__sbDict['prevCommand'] = [] #initialize list

		self.__sbDict['prevCommand'] = self.__sbDict['prevCommand'][-20:] #keep original list length restricted to last 20 elements

		list_ = self.__sbDict['prevCommand']
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
		self.__sbDict['name'] = self.__sbDict['name'][-10:] #keep original list length restricted to last ten elements

		list_ = [i for i in self.__sbDict['name'] if 'init' not in i] #work on a copy of the list, removing any instances of 'init', keeping the original intact
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



	def dict(self):
		'''
		returns:
				full switchboard dict
		'''
		return self.__sbDict



	def hasKey(self, *args): #check if key exists in switchboard dict.
		'''
		args:
				'string' dict keys in order of hierarchy.  ie. 'polygons', 'connectionDict', 'b001', 'method'
		returns:
				bool
		'''
		if len(args)==1:
			if args[0] in self.__sbDict:
				return True

		elif len(args)==2:
			if args[1] in self.__sbDict[args[0]]:
				return True

		elif len(args)==3:
			if args[2] in self.__sbDict[args[0]][args[1]]:
				return True

		elif len(args)==4:
			if args[3] in self.__sbDict[args[0]][args[1]][args[2]]:
				return True
		else:
			return False







#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------