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
			except:
				print('# Error: "MaxWindow" object not found by MaxPlus.GetQMaxMainWindow() #')

		super(Tk_max, self).__init__(parent)
		self.setUi()


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






if __name__ == "__main__":
	import sys
	from PySide2.QtWidgets import QApplication

	app = QApplication.instance() #get the qApp instance if it exists.
	if not app:
		app = QApplication(sys.argv)

	#create a parent object to run the code outside of maya.
	from PySide2.QtWidgets import QWidget
	p=QWidget() #dummy parent
	p.setObjectName('MaxWindow')

	Tk_max(p).show()
	sys.exit(app.exec_())



# -----------------------------------------------
# Notes
# -----------------------------------------------