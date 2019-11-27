from tk_ import Tk
from PySide2 import QtWidgets






class Tk_maya(Tk):
	'''
	Tk class overridden for use with Autodesk Maya.
	args:
		parent = main application top level window object.
	'''
	def __init__(self, parent=None):
		super(Tk_maya, self).__init__(parent)

		self.setUi()



	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''


		# super(Tk_maya, self).showEvent(event)
		return Tk.showEvent(self, event)


	def hideEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''


		# super(Tk_maya, self).hideEvent(event)
		return Tk.hideEvent(self, event)



def createInstance():
	'''
	Return an instance parented to the app mainWindow.
	'''
	app = QtWidgets.QApplication.instance() #get the qApp instance if it exists.
	if not app:
		app = QtWidgets.QApplication(sys.argv)

	mainWindow = [x for x in app.topLevelWidgets() if x.objectName()=='MayaWindow']

	if mainWindow:
		return Tk_maya(mainWindow[0])
	else:
		print '# Error: "MayaWindow" object not found in app.topLevelWidgets() #'
		return Tk_maya()



# if not pm.runTimeCommand('Hk_tk', exists=1):
# 	pm.runTimeCommand(
# 		'Hk_tk'
# 		annotation='',
# 		catagory='',
# 		commandLanguage='python',
# 		command=if 'tk' not in locals() or 'tk' not in globals(): tk = tk_maya.createInstance(); tk.hide(); tk.show(),
# 		hotkeyCtx='',
# 	)



if __name__=='__main__':
	createInstance().show()