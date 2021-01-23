from __future__ import print_function
from builtins import super
import sys

from PySide2 import QtWidgets, QtGui, QtCore


class TkWidget_GifPlayer(QtWidgets.QWidget):
	def __init__(self, parent=None, gif='loading_indicator.gif'): 
		super().__init__(parent)
		'''
		'''
		self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		self.setFocusPolicy(QtCore.Qt.NoFocus)

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setAttribute(QtCore.Qt.WA_SetStyle) #Indicates that the widget has a style of its own.

		self.label = QtWidgets.QLabel() #set up the player on a label.
		# expand and center the label
		self.label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		self.label.setAlignment(QtCore.Qt.AlignCenter)     

		# positin the widgets
		main_layout = QtWidgets.QVBoxLayout() 
		main_layout.addWidget(self.label)
		self.setLayout(main_layout)

		self.movie = QtGui.QMovie(gif, QtCore.QByteArray(), self) 
		self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
		self.movie.setSpeed(100) 
		self.label.setMovie(self.movie)

		# self.movie.start(); self.movie.stop() # display first frame
		self.label.resize(50, 50)
		self.move(QtGui.QCursor.pos() - self.rect().center())


	def start(self):
		'''start animnation
		'''
		self.show()
		self.movie.start()

		
	def stop(self):
		'''stop the animation
		'''
		self.hide()
		self.movie.stop()


if __name__=='__main__':
	# you can replace [] with sys.argv commandline arg 
	app = QtWidgets.QApplication([]) 
	player = TkWidget_GifPlayer() 

	player.start()
	app.exec_()