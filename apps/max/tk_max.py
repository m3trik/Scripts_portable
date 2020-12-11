from __future__ import print_function

from PySide2 import QtCore, QtWidgets

try:
	import MaxPlus
except ImportError as error:
	print(error)

from tk_ import Tk
from ui import widgets



class Tk_max(Tk):
	'''
	Tk class overridden for use with Autodesk 3ds max.

	:Parameters:
		parent = main application top level window object.
	'''
	def __init__(self, parent=None, preventHide=False, key_show=QtCore.Qt.Key_F12):

		if not parent:
			try:
				parent = self.getMainWindow()
				parent.setObjectName('MaxWindow')

			except Exception as error:
				print(self.__class__.__name__, error)

		super(Tk_max, self).__init__(parent)


	def getMainWindow(self):
		'''
		Get maya's main window object.

		:Return:
			(QWidget)
		'''
		main_window = MaxPlus.GetQMaxMainWindow()

		return main_window


	def keyPressEvent(self, event):
		'''
		:Parameters:
			event = <QEvent>
		'''
		if not event.isAutoRepeat():
			modifiers = QtWidgets.QApplication.keyboardModifiers()

			if event.key()==self.key_undo and modifiers==QtCore.Qt.ControlModifier:
				import pymxs
				pymxs.undo(True)

		return QtWidgets.QStackedWidget.keyPressEvent(self, event)


	def showEvent(self, event):
		'''
		:Parameters:
			event = <QEvent>
		'''
		try:
			MaxPlus.CUI.DisableAccelerators()

		except Exception as error:
			print(error)

		return Tk.showEvent(self, event) #super(Tk_max, self).showEvent(event)


	def hideEvent(self, event):
		'''
		:Parameters:
			event = <QEvent>
		'''
		try:
			MaxPlus.CUI.EnableAccelerators()

		except Exception as error:
			print(error)

		if __name__ == "__main__":
			QApplication.instance().quit()
			sys.exit() #assure that the sys processes are terminated.

		return Tk.hideEvent(self, event) #super(Tk_max, self).hideEvent(event)


	# import contextlib
	# @contextlib.contextmanager
	# def performAppUndo(self, enabled=True, message=''):
	# 	'''
	# 	Uses pymxs's undo mechanism, but doesn't silence exceptions raised
	# 	in it.

	# 	:Parameter:
	# 		enabled (bool) = Turns undo functionality on.
	# 		message (str) = Label for the undo item in the undo menu.
	# 	'''
	# 	print('undo')
	# 	import pymxs
	# 	import traceback
	# 	e = None
	# 	with pymxs.undo(enabled, message):
	# 		try:
	# 			yield
	# 		except Exception as e:
	# 			# print error, raise error then run undo 
	# 			print(traceback.print_exc())
	# 			raise(e)
	# 			pymxs.run_undo()


class Instance():
	'''
	Manage multiple instances of Tk_max.
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
		'''
		Internal use. Returns a new instance if one is running and currently visible.
		Removes any old non-visible instances outside of the current 'activeWindow_'.
		'''
		self.instances = {k:v for k,v in self.instances.items() if not any([v.isVisible(), v==self.activeWindow_])}

		if self.activeWindow_ is None or self.activeWindow_.isVisible():
			name = 'tk'+str(len(self.instances))
			setattr(self, name, Tk_max(self.parent, self.preventHide, self.key_show))
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
	from PySide2.QtWidgets import QApplication

	app = QApplication.instance() #get the qApp instance if it exists.
	if not app:
		app = QApplication(sys.argv)

	#create a parent object to run the code outside of max.
	from PySide2.QtWidgets import QWidget
	dummyParent = QWidget()
	dummyParent.setObjectName('MaxWindow')

	import cProfile
	cProfile.run('Instance(dummyParent).show_()')
	# Instance(dummyParent).show_() #Tk_max(p).show()
	sys.exit(app.exec_())



# -----------------------------------------------
# Notes
# -----------------------------------------------