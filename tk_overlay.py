from PySide2 import QtCore, QtGui, QtWidgets

import os.path

from tk_switchboard import Switchboard








# ------------------------------------------------
# PaintEvent Overlay
# ------------------------------------------------
class Overlay(QtWidgets.QWidget):
	'''
	Handles paint events as an overlay on top of an existing widget.
	'''
	def __init__(self):
		super(Overlay, self).__init__()

		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_NoSystemBackground) #takes a single arg
		self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

		self.sb = Switchboard()
		self.point = QtCore.QPoint(self.sb.getUiSize(percentWidth=50), self.sb.getUiSize(percentHeight=50)) #set point to the middle of the layout

		self.start_line, self.end_line = self.point, QtCore.QPoint()



	def paintEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		uiName = self.sb.getUiName()
		if any([uiName=='main', uiName=='viewport', uiName=='editors']):

			greyPen = QtGui.QPen(QtGui.QColor(115, 115, 115), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
			blackPen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

			path = QtGui.QPainterPath()
			path.addEllipse(QtCore.QPointF(self.point), 7, 7)

			painter = QtGui.QPainter(self) #Initialize painter
			painter.fillRect(self.rect(), QtGui.QColor(127, 127, 127, 0)) #transparent overlay background.
			painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
			painter.setBrush(QtGui.QColor(115, 115, 115))
			painter.fillPath(path, QtGui.QColor(115, 115, 115))
			painter.setPen(blackPen)
			painter.drawPath(path) #stroke
			if not self.end_line.isNull():
				painter.setPen(greyPen)
				painter.drawLine(self.start_line, self.end_line)
				painter.drawEllipse(self.end_line, 5, 5)



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.start_line = self.point
		self.end_line = event.pos()
		self.update()



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.end_line = event.pos()
		self.update()



	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.start_line = self.point
		self.end_line = QtCore.QPoint()






class OverlayFactoryFilter(QtCore.QObject):
	'''
	Relay events from the parent widget to the overlay.
	'''
	def __init__(self, parent=None):
		super(OverlayFactoryFilter, self).__init__(parent)

		self.overlay = Overlay()
		self.overlay.setParent(parent)
		parent.installEventFilter(self)



	def eventFilter(self, widget, event):
		'''
		args:
			widget=<QWidget>
			event=<QEvent>
		'''
		if not widget.isWidgetType():
			return False

		if event.type()==QtCore.QEvent.MouseButtonPress:
			self.overlay.mousePressEvent(event)

		elif event.type()==QtCore.QEvent.MouseButtonRelease:
			self.overlay.mouseReleaseEvent(event)

		elif event.type()==QtCore.QEvent.MouseMove:
			self.overlay.mouseMoveEvent(event)

		elif event.type()==QtCore.QEvent.MouseButtonDblClick:
			self.overlay.mouseDoubleClickEvent(event)

		elif event.type()==QtCore.QEvent.Resize:
			if self.overlay and self.overlay.parentWidget()==widget:
				self.overlay.resize(widget.size())

		elif event.type()==QtCore.QEvent.Show:
			self.overlay.raise_()

		return super(OverlayFactoryFilter, self).eventFilter(widget, event)







#module name
print os.path.splitext(os.path.basename(__file__))[0]


# -----------------------------------------------
# Notes
# -----------------------------------------------