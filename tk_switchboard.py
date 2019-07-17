from pydoc import locate
from PySide2.QtUiTools import QUiLoader

import os.path








#set path to the directory containing the ui files.
path = os.path.join(os.path.dirname(__file__), 'ui') #get absolute path from dir of this module + relative path to directory

#build uiList
uiList = [[file_.replace('.ui',''), QUiLoader().load(path+'/'+file_)] for file_ in os.listdir(path) if file_.endswith('.ui')] #constructs uiList from directory contents. ie. [['polygons', <polygons dynamic ui object>]]

#initialize sbDict using the class names from uiList.
global sbDict
sbDict = {name[0]:{} for name in uiList} # ie. { 'edit':{}, 'create':{}, 'animation':{}, 'cameras':{}, 'display':{} }

#add uiList to sbDict
if 'uiList' not in sbDict: sbDict['uiList'] = uiList

#add name list to sbDict
if 'name' not in sbDict: sbDict['name'] = ['init']


# ------------------------------------------------
#	Manage Ui elements
# ------------------------------------------------
class Switchboard(object): #get/set elements across modules from a single dictionary.
	
	def __init__(self):
		'''
		# -- keys/values ---------- #
			'string name of class'{
				'class' : class object
				'size' : list containing width int, height int. ie. [295, 234]
				'connectionDict' : {'b001':{'buttonObject':b001, 'buttonObjectWithSignal':b001.connect, 'methodObject':main.b001, 'docString':'Multi-Cut Tool', 'widgetClass':QPushButton, widgetClassName':'QPushButton'}},
				}
			'uiList' : list of two element lists containing all ui filenames in the ui folder and their corresponding dynamic ui object. ie. [['polygons', <polygons dynamic ui object>]]
			'app' : string name of parent application. ie. 'maya' or 'max'
			'name' #string list. when a new ui is called its name is at element[-1] and the previous ui is at element[-2]. ie. ['previousName', 'previousName', 'currentName']
			'prevCommand' #history of commands. last used command method at element[-1].  list of 2 element lists. [[methodObject,'methodNameString']]  ie. [{b00, 'multi-cut tool'}]
		ex.
		sbDict={
		'polygons':{ 
		'class':Polygons, 
		'size':[295, 234], 
		'connectionDict':{'b001':{'buttonObject':b001, 'buttonObjectWithSignal':b001.connect, 'methodObject':main.b001, 'docString':'Multi-Cut Tool', 'widgetClass':QPushButton, widgetClassName':'QPushButton'}},
		}
		'uiList':[['animation', <animation dynamic ui object>], ['cameras', <cameras dynamic ui object>], ['create', <create dynamic ui object>], ['display', <display dynamic ui object>]],
		'app':'maya'
		'name':['polygons', 'edit', 'cameras'], 
		'prevCommand':[[b00, 'multi-cut tool']],
		
		'''




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
			return [i[0] for i in sbDict['uiList']]
		elif ui:
			return [i[1] for i in sbDict['uiList']]
		else:
			return sbDict['uiList']



	def getUi(self, name=None):
		'''
		args:
				name='string' name of class. ie. 'polygons'
		returns:
				if name: corresponding dynamic ui object of given name from the key 'uiList'.
				else: current dynamic ui object
		'''
		if name:
			return self.uiList(ui=1)[self.getUiIndex(name)]
		else:
			return self.uiList(ui=1)[self.getUiIndex(self.getUiName())]



	def setUiName(self, index):
		'''
		args:
				index=int
		returns:
				corresponding ui name as string
		'''
		sbDict['name'].append(self.uiList(name=1)[index])
		return sbDict['name'][-1]



	def getUiName(self):
		'''
		returns:
				current ui name as string
		'''
		return sbDict['name'][-1]



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



	def setApp(self, parent):
		'''
		args:
				parent=parent app object.
		returns:
				string name of parent app
		'''
		sbDict['app'] = parent.objectName().rstrip('Window').lower() #remove 'Window' from objectName ie. 'Maya' from 'MayaWindow' and set lowercase.
		return sbDict['app']



	def getApp(self):
		'''
		args:
				parent=parent app object.
		'''
		if not 'app' in sbDict: sbDict['app'] = '' #initialize list

		return sbDict['app']



	def setUiSize(self, name, size): #store ui size.
		'''
		args:
				size=[int, int]
		returns:
				ui size info as integer values in a list. [width, hight]
		'''
		sbDict[name]['size'] = size
		return sbDict[name]['size']



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
			return sbDict[self.getUiName()]['size'][0]
		elif height:
			return sbDict[self.getUiName()]['size'][1]
		elif percentWidth:
			return sbDict[self.getUiName()]['size'][0] *percentWidth /100
		elif percentHeight:
			return sbDict[self.getUiName()]['size'][1] *percentHeight /100
		else:
			return sbDict[self.getUiName()]['size']



	def setClass(self, class_):
		'''
		args:
				class_='string' module name and class to import and store class instance. 
					ie. 'tk_slots_max_polygons.Polygons'
					*or <class object>. to store class instance
		returns:
				class object corresponding to key: class_.
		'''
		if type(class_)==str or type(class_)==unicode: #arg as string
			name = class_.split('_')[-1].split('.')[-1].lower(); #get key from class_ string ie. 'class' from 'tk_slots_max_polygons.Class'
			if not name in sbDict:
				sbDict[name] = {}

			sbDict[name]['class'] = locate(class_)

		else: #if class_ arg as <object>:
			name = class_.__class__.__name__.lower();
			if not name in sbDict:
				sbDict[name] = {}
			
			sbDict[name]['class'] = class_

		if not sbDict[name]['class']:
			return '# Error: '+class_+' not found. #'
		else:
			return sbDict[name]['class']


	def getClass(self, name):
		'''
		If class is not in sbDict, use setClass() instead.
		args:
				name='string' name of class. ie. 'polygons' (lowercase)
		returns:
				class object from given class name.
		'''
		return sbDict[name]['class']



	def getMethod(self, name, methodString):
		'''
		args:
				name='string' name of class. ie. 'polygons' (lowercase)
				methodString='string' name of method. ie. 'b001'
		returns:
				corresponding method object to given method name string.
		'''
		try: return sbDict[name]['connectionDict'][methodString]['methodObject'][0] #if there are event filters attached, just get the method.
		except: return  sbDict[name]['connectionDict'][methodString]['methodObject']



	def getSignal(self, name, buttonName=None):
		'''
		args:
				name='string' name of class. ie. 'polygons'
				buttonName='string'  ie. 'b001'
		returns:
				if buttonName: the corresponding button object with attached signal (ie. b001.onPressed) of the given button name.
				else: all of the signals associated with the given name as a list
		'''
		if buttonName:
			return sbDict[name]['connectionDict'][buttonName]['buttonObjectWithSignal']
		else:
			return [sbDict[name]['connectionDict'][buttonName]['buttonObjectWithSignal'] for buttonName in sbDict[name]['connectionDict']]



	def getSlot(self, name, buttonName=None):
		'''
		args:
				name='string' name of class. ie. 'polygons'
				buttonName='string'  ie. 'b001'
		returns:
				if buttonName: the corresponding method object (ie. Polygons.b001) of the given button name.
				else: all of the slots associated with the given name as a list
		'''
		if buttonName:
			return sbDict[name]['connectionDict'][buttonName]['methodObject']
		else:
			return [sbDict[name]['connectionDict'][buttonName]['methodObject'] for buttonName in sbDict[name]['connectionDict']]



	def getDocString(self, name, methodString, full=False):
		'''
		args:
				name='string' name of class. ie. 'polygons'
				methodString='string' name of method. ie. 'b001'
				full=bool return full unedited docString
		returns:
				if full: full stored docString
				else: edited docString; name of method
		'''
		if full: #entire unformatted docString
			return sbDict[name]['connectionDict'][methodString]['docString']
		else: #formatted docString
			return sbDict[name]['connectionDict'][methodString]['docString'].strip('\n\t')


	def getWidgetClass(self, button, name=None):
		'''
		args:
				button='string'  - name of button/widget
					*or <object> -widget
				name='string' - name of dynamic ui (else use current ui)
		returns:
				<class object> - the corresponding widget class
		'''
		if not type(button)==str:
			try:
				return button.__class__
			except:
				button = button.objectName()

		if not name:
			name = self.getUiName()

		return sbDict[name]['connectionDict'][button]['widgetClass']


	def getWidgetType(self, button, name=None):
		'''
		args:
				button='string'  - name of button/widget
					*or <object> -widget
				name='string' - name of dynamic ui (else use current ui)
		returns:
				'string' - the corresponding widget class name
		'''
		if not type(button)==str:
			try:
				return button.__class__.__name__
			except:
				button = button.objectName()

		if not name:
			name = self.getUiName()

		return sbDict[name]['connectionDict'][button]['widgetClassName']


	def previousName(self, previousIndex=False, allowDuplicates=False, as_list=False):
		'''
		args:
				previousIndex=bool 	return the index of the last valid previously opened ui name.
		returns:
				if previousIndex: int index of previously opened ui
				else: string name of previously opened layout.
		'''
		sbDict['name'] = sbDict['name'][-10:] #keep original list length restricted to last ten elements

		list_ = [i for i in sbDict['name'] if 'init' not in i] #work on a copy of the list, removing any instances of 'init', keeping the original intact
		if not allowDuplicates:
			[list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous duplicates if they exist; keeping the last added element.

		if previousIndex:
			validPrevious = [i for i in list_ if all(['viewport' not in i, 'main' not in i])]
			return self.getUiIndex(validPrevious[-2])

		elif as_list:
			return list_

		else:
			try: return list_[-2]
			except: return ''



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
		if not 'prevCommand' in sbDict: sbDict['prevCommand'] = [] #initialize list

		sbDict['prevCommand'] = sbDict['prevCommand'][-20:] #keep original list length restricted to last 20 elements

		list_ = sbDict['prevCommand']
		[list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous duplicates if they exist; keeping the last added element.

		if docString and as_list:
			try: return [i[1] for i in list_]
			except: return None

		elif docString:
			try: return list_[-1][1]
			except: return ''

		elif method and as_list:
			try:return [i[0] for i in list_]
			except: return ['# No commands in history. #']

		elif method:
			try: return list_[-1][0]
			except: return ''
		
		elif as_list:
			return list_

		else:
			try: return list_[-1][0]
			except: return None



	def previousView(self, previousIndex=False, allowDuplicates=False, as_list=False):
		'''
		args:
				previousIndex=bool 	return the index of the last valid previously opened ui name.
		returns:
				if previousIndex: int index of previously opened ui
				else: string name of previously opened layout.
		'''
		sbDict['name'] = sbDict['name'][-10:] #keep original list length restricted to last ten elements

		list_ = [i for i in sbDict['name'] if 'init' not in i] #work on a copy of the list, removing any instances of 'init', keeping the original intact
		if not allowDuplicates:
			[list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous duplicates if they exist; keeping the last added element.

		if previousIndex:
			validPrevious = [i for i in list_ if all(['viewport' not in i, 'main' not in i])]
			return self.getUiIndex(validPrevious[-2])

		elif as_list:
			return list_

		else:
			try: return list_[-2]
			except: return ''



	def connectionDict(self, name):
		'''
		args:
				name='string' name of class. ie. 'polygons'
		returns:
				connection dict of given name with button/corresponding method string as key.
		ex.
		'buttonObject':button ui object.  ie. b001
		'buttonObjectWithSignal':button ui object with signal attached. ie. b001.connect
		'methodObject':class method object for the corresponding ui button. ie. main.b001
		'docString': string description of command from method docString.  ie. 'Multi-Cut Tool'}
		#ie. {'b001':{'buttonObject':b001, 'buttonObjectWithSignal':b001.onPressed, 'methodObject':main.b001, 'docString':'Multi-Cut Tool'}},
		'''
		if not 'connectionDict' in sbDict[name]: sbDict[name]['connectionDict'] = {}

		return sbDict[name]['connectionDict']




	def dict(self):
		'''
		returns:
				full switchboard dict
		'''
		return sbDict



	def hasKey(self, *args): #check if key exists in switchboard dict.
		'''
		args:
				'string' dict keys in order of hierarchy.  ie. 'polygons', 'connectionDict', 'b001', 'methodObject'
		returns:
				bool
		'''
		if len(args)==1:
			if args[0] in sbDict: return True
			else: return False
		if len(args)==2:
			if args[1] in sbDict[args[0]]: return True
			else: return False
		if len(args)==3:
			if args[2] in sbDict[args[0]][args[1]]: return True
			else: return False
		if len(args)==4:
			if args[3] in sbDict[args[0]][args[1]][args[2]]: return True
			else: return False







#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------