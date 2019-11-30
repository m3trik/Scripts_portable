from tk_ import Tk
import MaxPlus






class Tk_max(Tk):
	'''
	Tk class overridden for use with Autodesk 3ds max.
	args:
		parent = main application top level window object.
	'''
	def __init__(self, parent=None):

		if not parent:
			parent = MaxPlus.GetQMaxMainWindow()
			if parent:
				parent.setObjectName('MaxWindow')
				super(Tk_max, self).__init__(parent)
			else:
				super(Tk_max, self).__init__(None)
				print '# Error: "MaxWindow" object not found by MaxPlus.GetQMaxMainWindow() #'

		self.setUi()


	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		MaxPlus.CUI.DisableAccelerators()

		# super(Tk_max, self).showEvent(event)
		return Tk.showEvent(self, event)


	def hideEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		MaxPlus.CUI.EnableAccelerators()

		# super(Tk_max, self).hideEvent(event)
		return Tk.hideEvent(self, event)





if __name__ == "__main__":
	import sys
	from PySide2.QtWidgets import QApplication

	app = QApplication.instance() #get the qApp instance if it exists.
	if not app:
		app = QApplication(sys.argv)

	Tk_max().show()

	sys.exit(app.exec_())



# -----------------------------------------------
# Notes
# -----------------------------------------------