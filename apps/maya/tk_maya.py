from __future__ import print_function
import sys

from PySide2 import QtWidgets, QtCore
try: import shiboken2
except: from PySide2 import shiboken2
global app
app = QtWidgets.QApplication.instance() #get the qApp instance if it exists.
if not app:
	app = QtWidgets.QApplication(sys.argv)

# import maya.OpenMayaUI as omui

from tk_ import Tk
from ui import widgets



class Tk_maya(Tk):
	'''Tk class overridden for use with Autodesk Maya.

	:Parameters:
		parent = Application top level window instance.
	'''
	def __init__(self, parent=None, preventHide=False, key_show=QtCore.Qt.Key_F12):
		'''
		'''
		if not parent:
			try:
				parent = self.getMainWindow()

			except Exception as error:
				print(self.__class__.__name__, error)

		# progressIndicator = widgets.TkWidget_ProgressIndicator()
		# progressIndicator.start()

		super(Tk_maya, self).__init__(parent)

		# progressIndicator.stop()


	def getMainWindow(self):
		'''Get maya's main window object.

		:Return:
			(QWidget)
		'''
		# ptr = OpenMayaUI.MQtUtil.mainWindow()
		# main_window = shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)

		main_window = next(w for w in app.topLevelWidgets() if w.objectName()=='MayaWindow')

		return main_window


	def keyPressEvent(self, event):
		'''
		:Parameters:
			event = <QEvent>
		'''
		if not event.isAutoRepeat():
			modifiers = QtWidgets.QApplication.keyboardModifiers()

			if event.key()==self.key_undo and modifiers==QtCore.Qt.ControlModifier:
				import Pymel.Core as pm
				pm.undo()

		return QtWidgets.QStackedWidget.keyPressEvent(self, event)


	def showEvent(self, event):
		'''
		:Parameters:
			event = <QEvent>
		'''

		return Tk.showEvent(self, event) #super(Tk_maya, self).showEvent(event)


	def hideEvent(self, event):
		'''
		:Parameters:
			event = <QEvent>
		'''
		if __name__ == "__main__":
			QtWidgets.QApplication.instance().quit()
			sys.exit() #assure that the sys processes are terminated.

		return Tk.hideEvent(self, event) #super(Tk_maya, self).hideEvent(event)



class Instance():
	'''Manage multiple instances of Tk_maya.
	'''
	instances={}

	def __init__(self, parent=None, preventHide=False, key_show=QtCore.Qt.Key_F12):
		'''
		'''
		self.parent = parent
		self.activeWindow_ = None
		self.preventHide = preventHide
		self.key_show = key_show


	def _getInstance(self):
		'''Internal use. Returns a new instance if one is running and currently visible.
		Removes any old non-visible instances outside of the current 'activeWindow_'.
		'''
		self.instances = {k:v for k,v in self.instances.items() if not any([v.isVisible(), v==self.activeWindow_])}

		if self.activeWindow_ is None or self.activeWindow_.isVisible():
			name = 'tk'+str(len(self.instances))
			setattr(self, name, Tk_maya(self.parent, self.preventHide, self.key_show))
			self.activeWindow_ = getattr(self, name)
			self.instances[name] = self.activeWindow_

		return self.activeWindow_


	def show_(self):
		'''
		'''
		instance = self._getInstance()
		instance.show()









if __name__ == "__main__":
	import sys

	#create a generic parent object to run the code outside of maya.
	from PySide2.QtWidgets import QWidget
	dummyParent = QWidget()
	dummyParent.setObjectName('MayaWindow')

	# import cProfile
	# cProfile.run('Instance(dummyParent).show_()')
	Instance(dummyParent).show_() #Tk_maya(dummyParent).show()
	sys.exit(app.exec_())



# -----------------------------------------------
# Notes
# -----------------------------------------------


# if not pm.runTimeCommand('Hk_tk', exists=1):
# 	pm.runTimeCommand(
# 		'Hk_tk'
# 		annotation='',
# 		catagory='',
# 		commandLanguage='python',
# 		command=if 'tk' not in locals() or 'tk' not in globals(): tk = tk_maya.createInstance(); tk.hide(); tk.show(),
# 		hotkeyCtx='',
# 	)