

from PySide2 import QtCore, QtGui


class Window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		# add a few widgets for testing
		widget = QtGui.QWidget(self)
		edit = QtGui.QTextEdit(widget)
		button = QtGui.QPushButton('Button', widget)
		layout = QtGui.QVBoxLayout(widget)
		layout.addWidget(edit)
		layout.addWidget(button)
		self.setCentralWidget(widget)
		menu = self.menuBar().addMenu('&File')
		menu.addAction('&Quit', self.close)
		menu = self.menuBar().addMenu('&Edit')
		menu.addAction('&Clear', edit.clear)
#------------------------------------------------
		QtGui.qApp.installEventFilter(self)
		# make sure initial window size includes menubar
		QtCore.QTimer.singleShot(0, self.menuBar().hide)


def eventFilter(self, source, event):
	# do not hide menubar when menu shown
	if QtGui.qApp.activePopupWidget() is None:
		if event.type() == QtCore.QEvent.MouseMove:
			if self.menuBar().isHidden():
				rect = self.geometry()
				# set mouse-sensitive zone
				rect.setHeight(25)
				if rect.contains(event.globalPos()):
					self.menuBar().show()
			else:
				rect = QtCore.QRect(
				self.menuBar().mapToGlobal(QtCore.QPoint(0, 0)),
				self.menuBar().size())
				if not rect.contains(event.globalPos()):
					self.menuBar().hide()
		elif event.type() == QtCore.QEvent.Leave and source is self:
			self.menuBar().hide()
	return QtGui.QMainWindow.eventFilter(self, source, event)


if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	window = Window()
	window.setGeometry(500, 300, 300, 100)
	window.show()
	sys.exit(app.exec_())