from PySide2 import QtWidgets, QtCore





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



class QLabel_(QtWidgets.QLabel):
	'''
	
	'''
	clicked = QtCore.Signal()
	released = QtCore.Signal()

	def __init__(self, parent=None, **kwargs):
		super(QLabel_, self).__init__(parent)

		self.setAttributes(kwargs)


	def setAttributes(self, attributes=None, order=['globalPos', 'setVisible'], **kwargs):
		'''
		Works with attributes passed in as a dict or kwargs.
		If attributes are passed in as a dict, kwargs are ignored.
		args:
			attributes (dict) = keyword attributes and their corresponding values.
			#order (list) = list of string keywords. ie. ['move', 'show']. attributes in this list will be set last, in order of the list. an example would be setting move positions after setting resize arguments.
		kwargs:
			set any keyword arguments.
		'''
		if not attributes:
			attributes = kwargs

		for k in order:
			v = attributes.pop(k, None)
			if v:
				from collections import OrderedDict
				attributes = OrderedDict(attributes)
				attributes[k] = v

		for attr, value in attributes.items():
			try:
				getattr(self, attr)(value)

			except Exception as error:
				if type(error)==AttributeError:
					self.setCustomAttribute(attr, value)
				else:
					raise error


	def setCustomAttribute(self, attr, value):
		'''
		Handle custom keyword arguments.
		args:
			attr (str) = custom keyword attribute.
			value (str) = the value corresponding to the given attr.
		kwargs:
			copy (obj) = widget to copy certain attributes from.
			globalPos (QPoint) = move to given global location and center.
		'''
		if attr=='copy':
			self.setObjectName(value.objectName())
			self.resize(value.size())
			self.setText(value.text())
			self.setWhatsThis(value.whatsThis())

		if attr=='globalPos':
			self.move(self.mapFromGlobal(value - self.rect().center())) #move and center


	def mousePressEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if event.button()==QtCore.Qt.LeftButton:
			self.clicked.emit()

		return QtWidgets.QLabel.mousePressEvent(self, event)


	def mouseReleaseEvent(self, event):
		'''
		args:
			event=<QEvent>
		'''
		if event.button()==QtCore.Qt.LeftButton:
			self.released.emit()

		return QtWidgets.QLabel.mouseReleaseEvent(self, event)


	# def showEvent(self, event):
	# 	'''
	# 	args:
	# 		event=<QEvent>
	# 	'''

	# 	return QtWidgets.QLabel.showEvent(self, event)










if __name__ == "__main__":
	import sys
	from PySide2.QtCore import QSize
	app = QtWidgets.QApplication(sys.argv)
	w = QLabel_(parent=None, setObjectName='lbl000', resize=QSize(45, 45), setText='QLabel_', setWhatsThis='', setVisible=True)
	w.show()
	sys.exit(app.exec_())



# Deprecated -----------------------------------------------


# if not __name__=='__main__' and not hasattr(self, 'parentUiName'):
# 	p = self.parent()
# 	while not hasattr(p.window(), 'sb'):
# 		p = p.parent()

# 	self.sb = p.window().sb
# 	self.parentUiName = self.sb.getUiName()
# 	self.classMethod = self.sb.getMethod(self.parentUiName, self)