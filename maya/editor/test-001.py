try: import timeit, maya.mel as mel, pymel.core as pm;
except ImportError as error: print error
try: tk_scrollFieldReporter = pm.melGlobals['tk_scrollFieldReporter']; pm.scrollFieldReporter (tk_scrollFieldReporter, edit=1, clear=1)
except: pass

from pydoc import locate
# from tk_slots_maya_init import Init as func
from tk_slots_ import Slot
import tk_switchboard as sb









class Test001(Slot):
	def __init__(self, *args, **kwargs):
		super(Test001, self).__init__(*args, **kwargs)


		''' Start Code '''
		selection = pm.ls(selection=1)

		if selection:
			print pm.selectType(query=1, vertex=1)
			if pm.selectType(query=1, vertex=1): #get vertex selection info
				# selectedVerts = [v.split('[')[-1].rstrip(']') for v in pm.filterExpand(selectionMask=31)] #pm.polyEvaluate(vertexComponent=1);
				# collapsedList = self.collapseList(selectedVerts)
				numVerts = pm.polyEvaluate (selection[0], vertex=1)
				infoDict.update({'Selected '+str(len(selectedVerts))+'/'+str(numVerts)+" Vertices: ":collapsedList}) #selected verts





	def method(self):
		classes = [locate('tk_slots_'+self.hotBox.app+'_'+name+'.'+name.capitalize())(self.hotBox) for name in self.hotBox.uiList]
		for class_ in classes:
			print str(class_), class_




# test=Test001()
# test.method()




import maya.OpenMayaUI as omUI
from PySide2 import QtWidgets, QtCore
import shiboken2


def getMayaWindow():
	'''
	Get the main Maya window as a QtGui.QMainWindow instance
	@return: QtGui.QMainWindow instance of the top level Maya windows
	'''
	ptr = apiUI.MQtUtil.mainWindow()
	if ptr:
		return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)


def toQtObject(mayaName):
	'''
	Given the name of a Maya UI element of any type,
	return the corresponding QWidget or QAction.
	If the object does not exist, returns None
	'''
	ptr = omUI.MQtUtil.findControl(mayaName)
	if ptr is None:
		ptr = omUI.MQtUtil.findLayout(mayaName)
	if ptr is None:
		ptr = omUI.MQtUtil.findMenuItem(mayaName)
	if ptr is not None:
		return sip.wrapinstance(long(ptr), QtCore.QObject)


class MayaSubWindow(QtWidgets.QMainWindow):
	'''

	'''
	def __init__(self, parent=getMayaWindow()):
		super(MayaSubWindow, self).__init__(parent)
		self.executer = pm.cmdScrollFieldExecuter(sourceType='python')
		qtObj = toQtObject(self.executer)
		#Fill the window, could use qtObj.setParent
		#and then add it to a layout.
		self.setCentralWidget(qtObj)

w = MayaSubWindow()
w.show()


