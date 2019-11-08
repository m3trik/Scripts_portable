from PySide2 import QtCore, QtGui, QtWidgets

import os.path

from tk_switchboard import Switchboard
from tk_childEvents import EventFactoryFilter







# ------------------------------------------------
# PaintEvent Overlay
# ------------------------------------------------
class Overlay(QtWidgets.QWidget):
	'''
	Handles paint events as an overlay on top of an existing widget.
	'''
	greyPen = QtGui.QPen(QtGui.QColor(115, 115, 115), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
	blackPen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)


	def __init__(self):
		super(Overlay, self).__init__()

		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_NoSystemBackground) #takes a single arg
		self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

		self.sb = Switchboard()
		self.tk = self.sb.getClassInstance('tk')



	def paintEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		uiName = self.sb.getUiName()
		if any([uiName=='main', uiName=='viewport', uiName=='editors', 'submenu' in uiName]):

			painter = QtGui.QPainter(self) #Initialize painter

			for i, start_point in enumerate(self.tk.drawPath): #plot and draw the points in the drawPath list.
				try:
					end_point = self.mapFromGlobal(self.tk.drawPath[i+1])
				except:
					end_point = self.mouseEventPos #after the list points are drawn, plot the current end_point, controlled by the mouse move event.

				self.drawTangent(painter, self.mapFromGlobal(start_point), end_point)



	def drawTangent(self, painter, start_point, end_point):
		'''
		draw a segment between two points with the given painter.
		'''
		path = QtGui.QPainterPath()
		path.addEllipse(QtCore.QPointF(start_point), 7, 7)

		painter.fillRect(self.rect(), QtGui.QColor(127, 127, 127, 0)) #transparent overlay background.
		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
		painter.setBrush(QtGui.QColor(115, 115, 115))
		painter.fillPath(path, QtGui.QColor(115, 115, 115))
		painter.setPen(self.blackPen)
		painter.drawPath(path) #stroke
		if not end_point.isNull():
			painter.setPen(self.greyPen)
			painter.drawLine(start_point, end_point)
			# painter.drawEllipse(end_point, 5, 5)



	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.mouseEventPos = event.pos()
		self.update()



	def mouseMoveEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		self.mouseEventPos = event.pos()
		self.update()






class OverlayFactoryFilter(QtCore.QObject):
	'''
	Relay events from the parent widget to the overlay.
	'''
	def __init__(self, parent=None):
		super(OverlayFactoryFilter, self).__init__(parent)

		self.overlay = Overlay()
		self.overlay.setParent(parent)

		if parent:
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
			if widget==self.overlay.parentWidget():
				self.overlay.resize(widget.size())

		elif event.type()==QtCore.QEvent.Show:
			self.overlay.raise_()

		return super(OverlayFactoryFilter, self).eventFilter(widget, event)






#module name
print os.path.splitext(os.path.basename(__file__))[0]


# -----------------------------------------------
# Notes
# -----------------------------------------------

		# self.tk.currentChanged.connect(self.currentChanged)


	# def mousePressEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''
	# 	self.drawPath.append(self.rect().center()) #append as startPoint
	# 	self.mouseEventPos = event.pos()
	# 	self.update()



	# def mouseMoveEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''
	# 	# switch/case
	# 	if self.flag==2 or self.flag==3:
	# 		w = self.sb.getWidget('tk')

	# 		if self.flag==2:
	# 			print '2'
	# 			p = w.mapFromGlobal(self.globalCenter)
	# 			w.move(p.x() - w.width()/2, p.y() - w.height()/2) #move and center

	# 		startPoint = w.mapToGlobal(w.rect().center())
	# 		self.drawPath[0] = self.mapFromGlobal(startPoint) #replace the startPoint
	# 		self.drawPath.append(self.mapFromGlobal(QtGui.QCursor.pos()))
	# 		self.flag = None #run once

	# 	elif self.flag==1:
	# 		self.globalCenter = self.mapToGlobal(self.rect().center())
	# 		del self.drawPath[:]
	# 		self.drawPath.append(self.rect().center())
	# 		self.flag = None #run once

	# 	self.mouseEventPos = event.pos()
	# 	self.update()



	# def mouseReleaseEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''
	# 	del self.drawPath[:]
	# 	self.update()



	# def currentChanged(self):
	# 	'''
	# 	On stackedWidget index change, set flag value to allow the overlay to plot points accordingly.

	# 	1 = Main menu
	# 	2 = Submenu called for the first time.
	# 	3 = Submenu called.
	# 	'''
	# 	name = self.sb.getUiName()

	# 	if name:
	# 		if '_submenu' in name:
	# 			if name not in self.sb.previousName(as_list=1, allowDuplicates=1)[:-1]:
	# 				self.flag = 2
	# 			else:
	# 				self.flag = 3
	# 		else:
	# 			self.flag = 1



	# def currentChanged(self):
	# 	'''
	# 	On stackedWidget index change, set flag value to allow the overlay to plot points accordingly.
	# 	'''
	# 	name = self.sb.getUiName()

	# 	if name:
	# 		if '_submenu' in name: #Submenu
	# 			w = self.sb.getWidget('tk')

	# 			if name not in self.sb.previousName(as_list=1, allowDuplicates=1)[:-1]: #if Submenu called for the first time:
	# 				p = w.mapFromGlobal(self.globalCenter)
	# 				w.move(p.x() - w.width()/2, p.y() - w.height()/2) #move and center

	# 			# if '_submenu' in self.sb.previousName():
	# 			# 	q = QtWidgets.QPushButton(self.q, self.sb.getUi(name))
	# 			# 	p = q.mapFromGlobal(self.globalCenter)
	# 			# 	q.move(p.x() - q.width()/2, p.y() - q.height()/2) #move and center

	# 			# for widget in self.sb.getWidget(name=self.sb.getUiName()): #get all widgets from the current ui.
	# 			# 	if widget.objectName().startswith('i') and widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
	# 			# 		self.q = widget.objectName()

	# 			startPoint = w.mapToGlobal(w.rect().center())
	# 			self.drawPath[0] = self.mapFromGlobal(startPoint) #replace the startPoint
	# 			self.drawPath.append(self.mapFromGlobal(QtGui.QCursor.pos()))
	# 			# print self.drawPath

	# 		else: #Main menu
	# 			self.globalCenter = self.mapToGlobal(self.rect().center())

	# 			del self.drawPath[:]
	# 			self.drawPath.append(self.rect().center())


	# def currentChanged(self):
	# 	'''
	# 	On stackedWidget index change, set a point for .
	# 	'''
	# 	name = self.sb.getUiName()

	# 	if name and '_submenu' in name: #Submenu
	# 		self.drawPath.append(QtGui.QCursor.pos()) #global cursor position

	# 	else: #Main menu
	# 		if not self.globalCenter:
	# 			self.drawPath=[]
	# 			self.globalCenter = self.mapToGlobal(self.rect().center())
	# 			self.drawPath.append(self.globalCenter)
	# 		else:
	# 			del self.drawPath[1:] #clear the draw path


			# for widget in self.sb.getWidget(name=self.sb.getUiName()): #get all widgets from the current ui.
			# 	if widget.objectName().startswith('i') and widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
			# 		self.q = widget.objectName()



	# def currentChanged(self):
	# 	'''
	# 	On stackedWidget index change, set flag value to allow the overlay to plot points accordingly.
	# 	'''
	# 	name = self.sb.getUiName()

	# 	if name:
	# 		if '_submenu' in name: #Submenu
	# 			w = self.sb.getWidget('tk')

	# 			if name not in self.sb.previousName(as_list=1, allowDuplicates=1)[:-1]: #if Submenu called for the first time:
	# 				p = w.mapFromGlobal(self.globalCenter)
	# 				w.move(p.x() - w.width()/2, p.y() - w.height()/2) #move and center

	# 			# if '_submenu' in self.sb.previousName():
	# 			# 	q = QtWidgets.QPushButton(self.q, self.sb.getUi(name))
	# 			# 	p = q.mapFromGlobal(self.globalCenter)
	# 			# 	q.move(p.x() - q.width()/2, p.y() - q.height()/2) #move and center

	# 			# for widget in self.sb.getWidget(name=self.sb.getUiName()): #get all widgets from the current ui.
	# 			# 	if widget.objectName().startswith('i') and widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
	# 			# 		self.q = widget.objectName()

	# 			startPoint = w.mapToGlobal(w.rect().center())
	# 			self.drawPath[0] = self.mapFromGlobal(startPoint) #replace the startPoint
	# 			self.drawPath.append(self.mapFromGlobal(QtGui.QCursor.pos()))
	# 			# print self.drawPath

	# 		else: #Main menu
	# 			self.globalCenter = self.mapToGlobal(self.rect().center())

	# 			del self.drawPath[:]
	# 			self.drawPath.append(self.rect().center())