# !/usr/bin/python
# coding=utf-8
from PySide2 import QtWidgets, QtCore, QtGui



class QWidget_MultiWidget(QtWidgets.QWidget):
	'''
	'''
	enterEvent_	= QtCore.QEvent(QtCore.QEvent.Enter)
	leaveEvent_	= QtCore.QEvent(QtCore.QEvent.Leave)
	hoverEnter_ = QtCore.QEvent(QtCore.QEvent.HoverEnter)
	hoverMove_ = QtCore.QEvent(QtCore.QEvent.HoverMove)
	hoverLeave_ = QtCore.QEvent(QtCore.QEvent.HoverLeave)

	def __init__(self, widgets, parent=None):
		super(QWidget_MultiWidget, self).__init__(parent)

		self._mouseGrabber=None

		self.row = QtWidgets.QHBoxLayout(self)
		self.row.setSpacing(0)
		# self.row.addStretch(0)
		self.row.setContentsMargins(0,0,0,0) #self.row.setMargin(0)

		for widget in widgets:
			try:
				widget = getattr(QtWidgets, widget)(self) #ex. QtWidgets.QAction(self) object from string. parented to self.
			except:
				if callable(widget):
					widget = widget(self) #ex. QtWidgets.QAction(self) object. parented to self.

			self.row.addWidget(widget)

			# widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
			widget.installEventFilter(self)


	def eventFilter(self, widget, event):
		'''
		'''
		# if not (str(event.type()).split('.')[-1]) in ['QPaintEvent', 'UpdateLater', 'PolishRequest', 'Paint']: print(str(event.type())) #debugging
		# if event.type()==QtCore.QEvent.HoverEnter:
		# 	print ('hoverEnter_')

		if event.type()==QtCore.QEvent.HoverMove:
			try:
				w = next(w for w in self.childWidgets() if w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos())) and w.isVisible())
			except StopIteration:
				return QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.hoverLeave_)

			if not w is self._mouseGrabber:
				if self._mouseGrabber is not None:
					QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.hoverLeave_)
					QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.leaveEvent_)
				if not w is self.mouseGrabber():
					w.grabMouse()
				self._mouseGrabber = w
				QtWidgets.QApplication.sendEvent(w, self.hoverEnter_)
				QtWidgets.QApplication.sendEvent(w, self.enterEvent_)

		if event.type()==QtCore.QEvent.HoverLeave:
			if not __name__=='__main__':
				if self.window().isVisible():
					self.window().grabMouse()

		if event.type()==QtCore.QEvent.MouseButtonRelease:
			if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
				next(w.hide() for w in QtWidgets.QApplication.topLevelWindows() if w.isVisible() and not 'QMenu' in w.objectName()) #hide all windowshttps://www.commondreams.org/news/2020/04/21/warnings-suspension-democracy-new-york-state-officials-weigh-removing-sanders

		return super(QWidget_MultiWidget, self).eventFilter(widget, event)


	def enterEvent(self, event):
		'''
		'''
		self._mouseGrabber = self.mouseGrabber()
		
		return QtWidgets.QWidget.enterEvent(self, event)


	def mouseMoveEvent(self, event):
		'''
		'''
		for w in self.childWidgets():
			if w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos())) and w.isVisible():
				w.grabMouse()

		return QtWidgets.QWidget.mouseMoveEvent(self, event)


	def leaveEvent(self, event):
		'''
		'''
		QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.hoverLeave_)
		if self._mouseGrabber is not self:
			QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.leaveEvent_)
		
		return QtWidgets.QWidget.leaveEvent(self, event)


	def childWidgets(self, index=None):
		'''
		Get the widget at the given index.
		If no arg is given all widgets will be returned.

		args:
			index (int) = widget location.
		returns:
			(QWidget) or (list)
		'''
		children = [i for i in self.children() if not i.__class__.__name__=='QHBoxLayout']
		if index is not None:
			return children[index]
		return children


	def setAsOptionBox(self, widget):
		'''
		Set a pushbutton type widget to an option box style.
		'''
		widget.setFixedWidth(widget.sizeHint().height()*1.5)
		widget.setFixedHeight(widget.sizeHint().height()*1.6)
		widget.setText('□')
		font = widget.font()
		font.setPointSize(font.pointSize()*1.5)
		widget.setFont(font)
		widget.setContentsMargins(0,0,0,0) # widget.setStyleSheet('margin: 0px 0px 5px 0px;')
		widget.setStyleSheet('''
			QLabel {
			padding: 0px 0px 5px 0px;
			}''')


	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if not __name__=='__main__' and not hasattr(self, 'sb'):
			from tk_switchboard import sb
			self.sb = sb

			self.parentUiName = self.sb.getUiName()
			self.childEvents = self.sb.getClassInstance('EventFactoryFilter')

			self.childEvents.addWidgets(self.parentUiName, self.childWidgets())

		self.resize(self.sizeHint().width(), self.sizeHint().height())

		return QtWidgets.QWidget.showEvent(self, event)






if __name__ == "__main__":
	import sys
	qApp = QtWidgets.QApplication(sys.argv)

	m = QWidget_MultiWidget([QtWidgets.QPushButton('Cameras'), 'QPushButton'])
	m.setAsOptionBox(m.childWidgets(1))
	print(m.childWidgets(0).text())

	m.show()
	sys.exit(qApp.exec_())



# adding a Multi-Widget row to a custom tree widget:
# m = MultiWidget(['QPushButton', 'QPushButton'])
# m.childWidgets(0).setText('ButtonText')
# m.setAsOptionBox(m.childWidgets(1)) #set button 2 to be an option box style
# tree.add(m, 'Cameras') #add the widgets to the tree under the parent header 'Cameras'

