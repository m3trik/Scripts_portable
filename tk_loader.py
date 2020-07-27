from __future__ import print_function
from PySide2 import QtWidgets, QtGui, QtCore



class ImagePlayer(QtWidgets.QWidget):
	'''
	'''

	def __init__(self, filename, title, parent=None):
		'''
		'''
		QtWidgets.QWidget.__init__(self, parent)

		# Load the file into a QMovie
		self.movie = QtGui.QMovie(filename, QtCore.QByteArray(), self)

		size = self.movie.scaledSize()
		self.setGeometry(200, 200, size.width(), size.height())
		self.setWindowTitle(title)

		self.movie_screen = QtWidgets.QLabel()
		# Make label fit the gif
		self.movie_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)

		# Create the layout
		main_layout = QtWidgets.QVBoxLayout()
		main_layout.addWidget(self.movie_screen)

		self.setLayout(main_layout)

		# Add the QMovie object to the label
		self.movie.setCacheMode(QtGui.QMovie.CacheAll)
		self.movie.setSpeed(100)
		self.movie_screen.setMovie(self.movie)
		self.movie.start()



def run():
	import sys
	app = QtWidgets.QApplication.instance() #get the qApp instance if it exists.
	if not app:
		app = QtWidgets.QApplication(sys.argv)

	global w
	try:
		w.close()
		w.deleteLater()
	except:
		pass

	w = ImagePlayer(r'loader.gif', "...")
	w.show()

run()