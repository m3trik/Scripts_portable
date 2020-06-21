from PySide2 import QtCore, QtGui, QtWidgets

import sys



'''
Promoting a widget in designer to use a custom class:
>	In Qt Designer, select all the widgets you want to replace, 
		then right-click them and select 'Promote to...'. 

>	In the dialog:
		Base Class:		Class from which you inherit. ie. QWidget
		Promoted Class:	Name of the class. ie. "MyWidget"
		Header File:	Path of the file (changing the extension .py to .h)  ie. myfolder.mymodule.mywidget.h

>	Then click "Add", "Promote", 
		and you will see the class change from "QWidget" to "MyWidget" in the Object Inspector pane.
'''



class QProgressBar_(QtWidgets.QProgressBar):
	'''
	ex. for n, i in enumerate(list_):
			if not self.ui.progressBar.step(n, len(list_)): #register progress while checking for cancellation:
				break
	'''
	def __init__(self, parent=None):
		super(QProgressBar_, self).__init__(parent)

		self.setVisible(False)

		self.isCanceled = False
		# self.connect(QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self), self.cancel())


	def cancel(self):
		'''
		cancel the procedure.
		'''
		self.isCanceled = True


	def step(self, progress, length=100):
		'''
		args:
			progress (int) = current value
			length (int) = total value

		returns:
			current percentage
		ie.
		self.progressBar(init=1) #initialize the progress bar
		for obj in selection:
			self.progressBar(len(selection)) #register progress
		'''
		if self.isCanceled:
			return False

		if not self.isVisible():
			self.setVisible(True)

		value = 100*progress/length
		self.setValue(value)
		# QtGui.qApp.processEvents() #ensure that any pending events are processed sufficiently often for the GUI to remain responsive
		if value>=100:
			self.setVisible(False)

		print value
		return True


	def showEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.isCanceled = False
		self.setValue(0)

		return QtWidgets.QProgressBar.showEvent(self, event)


	def hideEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''

		return QtWidgets.QProgressBar.hideEvent(self, event)






if __name__ == "__main__":
	qApp = QtWidgets.QApplication(sys.argv)
		
	w = QProgressBar_()
	w.show()
	sys.exit(qApp.exec_())



# -----------------------------------------------
# Notes
# -----------------------------------------------

# if pm.progressBar ("tk_progressBar", query=1, isCancelled=1):
	# break
