from __future__ import print_function
from PySide2 import QtWidgets, QtGui, QtCore

from multiprocessing import Pool



# class Form(QtWidgets.QDialog):

# 	def __init__(self, parent=None):
# 		super(Form, self).__init__(parent)
# 		self.browser = QtWidgets.QTextBrowser()

class TkSplashScreen(QtWidgets.QSplashScreen):
	''''''
	def __init__(self, animation='loading_indicator', flags=QtCore.Qt.WindowStaysOnTopHint):
		'''Run event dispatching in another thread.
		'''
		QtWidgets.QSplashScreen.__init__(self, QtGui.QPixmap(), flags)

		self.movie = QtGui.QMovie(animation)
		self.movie.frameChanged.connect(self.onNextFrame)
		self.movie.start()


	def onNextFrame(self):
		''''''
		pixmap = self.movie.currentPixmap()
		self.setPixmap(pixmap)
		self.setMask(pixmap.mask())




def longInitialization(arg):
	'''Put your initialization code here.
	'''
	time.sleep(arg)
	return 0



if __name__ == "__main__":
	import sys, time

	app = QtWidgets.QApplication(sys.argv)

	# Create and display the splash screen
	# splash_pix = QtGui.QPixmap('qWidget_imagePlayer.gif')
	splash = TkSplashScreen()
#   splash.setMask(splash_pix.mask())
	#splash.raise_()
	splash.show()
	app.processEvents()

	# this event loop is needed for dispatching of Qt events
	initLoop = QtCore.QEventLoop()
	pool = Pool(processes=1)
	pool.apply_async(longInitialization, [2], callback=lambda exitCode: initLoop.exit(exitCode))
	initLoop.exec_()

	# form = Form()
	# form.show()
	# splash.finish(form)
	app.exec_()