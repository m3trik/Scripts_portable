from __future__ import print_function
from tk_ import Tk
from PySide2.QtWidgets import QApplication


app = QApplication.instance() #get the qApp instance if it exists.
if not app:
	app = QApplication(sys.argv)





class Tk_maya(Tk):
	'''
	Tk class overridden for use with Autodesk Maya.
	args:
		parent = main application top level window object.
	'''
	def __init__(self, parent=None):

		if not parent:
			try:
				global app
				parent = [x for x in app.topLevelWidgets() if x.objectName() is 'MayaWindow'][0]
			except:
				print('# Error: "MayaWindow" object not found in app.topLevelWidgets() #')

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






if __name__ == "__main__":
	import sys
	global app

	#create a parent object to run the code outside of maya.
	from PySide2.QtWidgets import QWidget
	p = QWidget()
	p.setObjectName('MayaWindow')

	Tk_maya(p).show()
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