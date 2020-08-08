from __future__ import print_function
from tk_ import Tk
from PySide2.QtWidgets import QApplication

from widgets.qWidget_ProgressIndicator import QWidget_ProgressIndicator

import sys
global app
app = QApplication.instance() #get the qApp instance if it exists.
if not app:
	app = QApplication(sys.argv)



class Tk_maya(Tk):
	'''
	Tk class overridden for use with Autodesk Maya.

	args:
		parent = Application top level window instance.
	'''
	def __init__(self, parent=None):

		if not parent:
			try:
				parent = next(w for w in app.topLevelWidgets() if w.objectName()=='MayaWindow')

			except Exception as error:
				print(self.__class__.__name__, error)

		# progressIndicator = QWidget_ProgressIndicator()
		# progressIndicator.start()

		super(Tk_maya, self).__init__(parent)

		# progressIndicator.stop()


	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''

		return Tk.showEvent(self, event) #super(Tk_maya, self).showEvent(event)


	def hideEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if __name__ == "__main__":
			QApplication.instance().quit()
			sys.exit() #assure that the sys processes are terminated.

		return Tk.hideEvent(self, event) #super(Tk_maya, self).hideEvent(event)


class Instance():
	'''
	Manage multiple instances of Tk_maya.
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
			setattr(self, name, Tk_maya(self.parent))
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