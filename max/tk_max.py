from __future__ import print_function
from tk_ import Tk

try:
	import MaxPlus
except ImportError as error:
	print(error)



class Tk_max(Tk):
	'''
	Tk class overridden for use with Autodesk 3ds max.

	args:
		parent = main application top level window object.
	'''
	def __init__(self, parent=None):

		if not parent:
			try:
				parent = MaxPlus.GetQMaxMainWindow()
				parent.setObjectName('MaxWindow')

			except Exception as error:
				print(self.__class__.__name__, error)

		super(Tk_max, self).__init__(parent)


	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		try:
			MaxPlus.CUI.DisableAccelerators()

		except Exception as error:
			print(error)

		return Tk.showEvent(self, event) #super(Tk_max, self).showEvent(event)


	def hideEvent(self, event):
		'''
		args:
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


class Instance():
	'''
	Manage multiple instances of Tk_max.
	'''
	instances={}

	def __init__(self, parent=None):
		'''
		'''
		self.parent = parent
		self.activeWindow_ = None


	def _getInstance(self):
		'''
		Internal use. Returns a new instance if one is running and currently visible.
		Removes any old non-visible instances outside of the current 'activeWindow_'.
		'''
		self.instances = {k:v for k,v in self.instances.items() if not any([v.isVisible(), v==self.activeWindow_])}

		if self.activeWindow_ is None or self.activeWindow_.isVisible():
			name = 'tk'+str(len(self.instances))
			setattr(self, name, Tk_max(self.parent))
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

	Instance(dummyParent).show_() #Tk_max(p).show()
	sys.exit(app.exec_())



# -----------------------------------------------
# Notes
# -----------------------------------------------