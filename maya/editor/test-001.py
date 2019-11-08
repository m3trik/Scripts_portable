try: import timeit, maya.mel as mel, pymel.core as pm;
except ImportError as error: print error
try: tk_scrollFieldReporter = pm.melGlobals['tk_scrollFieldReporter']; pm.scrollFieldReporter (tk_scrollFieldReporter, edit=1, clear=1)
except: pass

from pydoc import locate
from tk_slots_maya_init import Init as func #inherits from Slot
import tk_switchboard as sb




panel =  [p for p in pm.getPanel(type='modelPanel')]
panel = pm.getPanel(withFocus=1)
import inspect

print inspect.getmembers(pm.modelEditor(panel, edit=1, pluginObjects=['gpuCache', True]) )



class Test001(func):
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
		classes = [locate('tk_slots_'+self.tk.app+'_'+name+'.'+name.capitalize())(self.tk) for name in self.tk.uiList]
		for class_ in classes:
			print str(class_), class_




# test=Test001()
# test.method()


import maya.OpenMayaUI as omUI
from PySide2 import QtWidgets, QtCore
import shiboken2


def mayaWidgets(widgetList):
	return {widget:self.getMayaWidget(widget) for widget in widgetList}



class embedWidget(QtWidgets.QMainWindow):
	'''

	'''
	def __init__(self, parent=func.getMayaMainWindow()):
		super(embedWidget, self).__init__(parent)


		keyword1 = 'outliner'
		keyword2 = ''
		widgets = {w.objectName():w for w in QtWidgets.QApplication.allWidgets() if keyword1 in w.objectName() and keyword2 in w.objectName() or keyword1.title() in w.objectName() and keyword2 in w.objectName()}
		# for widget in widgets:
		# 	print widget


		widget = func.getMayaWidget('ToggledOutlinerLayout') #DisplayLayerTab
		layout = widget.layout()
		# print widget, layout
		self.setLayout(layout)
		self.setCentralWidget(widget)
		# self.setCentralWidget(func.convertToWidget(widget))


# w = embedWidget()
# w.show()
# w.resize(w.sizeHint())


# # We create a simple window with a QWidget
# window = QtWidgets.QWidget()
# window.resize(500,500)
# # We have our Qt Layout where we want to insert, say, a Maya viewport
# qtLayout = QtWidgets.QVBoxLayout(window)

# # We set a qt object name for this layout.
# qtLayout.setObjectName('viewportLayout') 

# # We set the given layout as parent and create the paneLayout under it.
# pm.setParent('viewportLayout')
# paneLayoutName = pm.paneLayout()
    
# # Create the model panel. I use # to generate a new panel with no conflicting name
# modelPanelName = pm.modelPanel("embeddedModelPanel#", cam='persp')

# # Find a pointer to the paneLayout that we just created using Maya API
# ptr = omUI.MQtUtil.findControl(paneLayoutName)
    
# # Wrap the pointer into a python QObject. Note that with PyQt QObject is needed. In Shiboken we use QWidget.
# paneLayoutQt = shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)

# # Now that we have a QtWidget, we add it to our Qt layout
# qtLayout.addWidget(paneLayoutQt)

# window.show()



