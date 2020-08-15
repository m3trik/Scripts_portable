from __future__ import print_function
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

from pydoc import locate

import sys, os.path



# ------------------------------------------------
#	Load Dynamic Ui files
# ------------------------------------------------
class UiLoader(QtCore.QObject):
	'''
	Load and maintain a dict of loaded dynamic ui files and related info.

	Ui files are searched for in the directory of this module.
	Custom widget modules are searched for in a sub directory named 'widgets'. naming convention: <name capital first char> widget class inside <name lowercase first char>.py module. ie. QLabel_ class inside qLabel_.py module.

	uiDict = {
		'<uiName>':{'ui':<ui obj>, 'level':<int>}
	}
	'''

	def __init__(self):
		'''
		Load the ui files and any custom widgets.
		'''
		self._uiDict={}
		self.loader = QUiLoader()

		uiPath = os.path.dirname(os.path.abspath(__file__)) #get absolute path from dir of this module
		# register any custom widgets.
		widgetPath = os.path.join(os.path.dirname(uiPath), 'ui\\widgets') #get the path to the widget directory.
		moduleNames = [file_.replace('.py','',-1) for file_ in os.listdir(widgetPath) if file_.startswith('q') and file_.endswith('.py')] #format names using the files in path.
		self.registerWidgets(moduleNames)

		# initialize _sbDict by setting keys for the ui files.
		for dirPath, dirNames, filenames in os.walk(uiPath):
			uiFiles = (f for f in filenames if f.endswith('.ui'))
			self.addUi(dirPath, uiFiles)


	@property
	def uiDict(self):
		return self._uiDict


	def registerWidgets(self, moduleNames):
		'''
		Register any custom widgets using the module names.
		'''
		for m in moduleNames:
			className = m[:1].capitalize()+m[1:] #capitalize first letter of module name to convert to class name
			path = 'widgets.{0}.{1}'.format(m, className)
			class_ = locate(path)
			if class_:
				self.loader.registerCustomWidget(class_)
			else:
				raise ImportError, path


	def addUi(self, dirPath, uiFiles):
		'''
		Load ui files and add them to the uiDict.

		args:
			dirPath (str) = The absolute directory path to the uiFiles.
			uiFiles (list) = A list of dynamic ui files.

		ie. {'polygons':{'ui':<ui obj>, 'level':<int>}} (the ui level is it's hierarchy based on the ui file's dir location)
		'''
		for filename in uiFiles:
			uiName = filename.replace('.ui','') #get the name from fileName by removing the '.ui' extension.

			#load the dynamic ui file.
			path = os.path.join(dirPath, filename)
			ui = self.loader.load(path)

			#get the ui level from it's directory location.
			d = dirPath[dirPath.rfind('ui\\'):] #slice the absolute path from 'ui\' ie. ui\base_menus_1\sub_menus_2\main_menus_3 from fullpath\ui\base_menus_1\sub_menus_2\main_menus_3
			uiLevel = len(d.split('\\'))-1

			self._uiDict[uiName] = {'ui':ui, 'level':uiLevel}


app = QApplication(sys.argv)
ui = UiLoader(); #print (ui.uiDict)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------