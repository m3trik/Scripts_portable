from tk_ import Tk
import MaxPlus






class Tk_max(Tk):
	'''
	Tk class overridden for use with Autodesk 3ds max.
	args:
		parent = main application top level window object.
	'''
	def __init__(self, parent=None):
		super(Tk_max, self).__init__(parent)

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



def createInstance():
	'''
	Return an instance parented to the app mainWindow.
	'''
	mainWindow = MaxPlus.GetQMaxMainWindow()
	mainWindow.setObjectName('MaxWindow')

	if mainWindow:
		return Tk_max(mainWindow)
	else:
		print '# Error: "MaxWindow" object not found in MaxPlus.GetQMaxMainWindow() #'
		return Tk_max()