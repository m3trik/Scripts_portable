from pydoc import locate







# ------------------------------------------------
#	Manage Ui elements
# ------------------------------------------------
class Switchboard(object): #get/set elements across modules from a single dictionary.
	def __init__(self, uiList=None):
		'''
		# key:values
		# 'class name' : 'string name of class'
				'class' : 'class object' 
				'size' : list containing width int, height int. ie. [295, 234]
				'connectionDict' : {'b001':{'buttonObject':b001, 'buttonObjectWithSignal':b001.connect, 'methodObject':main.b001, 'methodName':'Multi-Cut Tool'}},
		# uiList : formatted string list of all ui filenames in the ui folder.
		# prevName #when a new ui is called its name is last and the previous ui is at element[-2]. ie. [previousNameString, previousNameString, currentNameString]
		# prevCommand #history of commands. last used command method at element[-1].  list of 2 element lists. [[methodObject,'methodNameString']]  ie. [{b00, 'multi-cut tool'}]
		ex.
		sbDict={
		'polygons':{ 
		'class':Polygons, 
		'size':[295, 234], 
		'connectionDict':{'b001':{'buttonObject':b001, 'buttonObjectWithSignal':b001.connect, 'methodObject':main.b001, 'methodName':'Multi-Cut Tool'}},
		}
		'uiList':['animation', 'cameras', 'create', 'display', 'edit'],
		'prevName':['previousName', 'previousName', 'currentName'], 
		'prevCommand':[{b00, 'multi-cut tool'}] }
		
		'''

		self.uiList_ = uiList #get a string list of class names
		self.sbDict = {name:{} for name in self.uiList_} #initialize sbDict using the class names from uiList. ie. { 'edit':{}, 'create':{}, 'animation':{}, 'cameras':{}, 'display':{} }


	def uiList(self):
		'''
		#returns: list of string names of classes(lowercase) from key 'uiList'. ie. ['animation', 'cameras', 'create', 'display', 'edit']
		'''
		if not 'uiList' in self.sbDict: self.sbDict['uiList'] = self.uiList_
		return self.sbDict['uiList']

	def getUiName(self, index):
		'''
		#args:
		#	index=int
		#returns: string name of class(lowercase) at given index of key 'uiList'. ie. 'edit'
		'''
		return self.sbDict['uiList'][index]

	def getUiIndex(self, name):
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#returns: index of given name from the key 'uiList'.
		'''
		return self.sbDict['uiList'].index(name)

	def setUiSize(self, name, size): #store ui size.
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#	size=[int, int]
		#returns: ui size info as integer values in a list. [width, hight]
		'''
		self.sbDict[name]['size'] = size
		return self.sbDict[name]['size']

	def getUiSize(self, name): #get ui size info.
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#returns: ui size info as integer values in a list. [width, hight]
		'''
		return self.sbDict[name]['size']

	def setClassObject(self, class_name, module):
		'''
		#args:
		#	class_name='string' name of class(lowercase). ie. 'polygons'
		#	module='string'
		#returns: class object from given class name and module. 
		'''
		if not class_name in self.sbDict: self.sbDict[class_name] = {}
		self.sbDict[class_name]['class'] = locate(module)
		return self.sbDict[class_name]['class']

	def getClassObject(self, name):
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#returns: class object from given class name.
		'''
		return self.sbDict[name]['class']

	def prevName(self):
		'''
		#returns: string name of previously opened layout. ['previousName', 'previousName', 'currentName']
		'''
		if not 'prevName' in self.sbDict: self.sbDict['prevName'] = []
		return self.sbDict['prevName']

	def prevCommand(self):
		'''
		#returns: dict with method object as key and string description as value. 'prevCommand':{b001, 'multi-cut tool'} }
		'''
		if not 'prevCommand' in self.sbDict: self.sbDict['prevCommand'] = []
		return self.sbDict['prevCommand']

	def connectionDict(self, name):
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#returns: dict with button/corresponding method string as key
		#	'buttonObject':button ui object.  ie. b001
		#	'buttonObjectWithSignal':button ui object with signal attached. ie. b001.connect
		#	'methodObject':class method object for the corresponding ui button. ie. main.b001
		#	'methodName': string description of command from method docstring.  ie. 'Multi-Cut Tool'}
		#ie. {'b001':{'buttonObject':b001, 'buttonObjectWithSignal':b001.onPressed, 'methodObject':main.b001, 'methodName':'Multi-Cut Tool'}},
		'''
		if not 'connectionDict' in self.sbDict[name]: self.sbDict[name]['connectionDict'] = {}
		return self.sbDict[name]['connectionDict']

	def getSignal(self, name, buttonName):
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#	buttonName='string'  ie. 'b001'
		#returns: the corresponding button object with attached signal (ie. b001.onPressed) of the given button name.
		'''
		return self.sbDict[name]['connectionDict'][buttonName]['buttonObjectWithSignal']

	def getSlot(self, name, buttonName):
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#	buttonName='string'  ie. 'b001'
		#returns: the corresponding method object (ie. Polygons.b001) of the given button name.
		'''
		return self.sbDict[name]['connectionDict'][buttonName]['methodObject']

	def setMethodName(self, name, methodString, methodName):
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#	methodString='string' name of method. ie. 'b001'
		#	methodName='string' docstring name of method
		#returns: given docstring name of method
		'''
		self.sbDict[name]['connectionDict'][methodString]['methodName'] = methodName
		return self.sbDict[name]['connectionDict'][methodString]['methodName']

	def getMethodName(self, name, methodString):
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#	methodString='string' name of method. ie. 'b001'
		#returns: stored docstring name of method
		'''
		return self.sbDict[name]['connectionDict'][methodString]['methodName']
		
	def getMethod(self, name, methodString):
		'''
		#args:
		#	name='string' name of class. ie. 'polygons'
		#	methodString='string' name of method. ie. 'b001'
		#returns: corresponding method object to given method name string.
		'''
		return self.sbDict[name]['connectionDict'][methodString]['methodObject']

	def dict(self):
		'''
		#returns: full switchboard dict
		'''
		return self.sbDict

	def hasKey(self, *args): #check if key exists in switchboard dict.
		'''
		#args: 'string' dict keys in order of hierarchy.  ie. 'polygons', 'connectionDict', 'b001', 'methodObject'
		#returns: bool
		'''
		if len(args)==1:
			if args[0] in self.sbDict: return True
			else: return False
		if len(args)==2:
			if args[1] in self.sbDict[args[0]]: return True
			else: return False
		if len(args)==3:
			if args[2] in self.sbDict[args[0]][args[1]]: return True
			else: return False
		if len(args)==4:
			if args[3] in self.sbDict[args[0]][args[1]][args[2]]: return True
			else: return False
