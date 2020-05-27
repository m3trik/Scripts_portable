from __future__ import print_function
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



class QListWidget_(QtWidgets.QListWidget):
	'''
	'''
	def __init__(self, parent=None, **kwargs):
		super(QListWidget_, self).__init__(parent) 

		self.setAttributes(kwargs)
		# self.setViewMode(QtWidgets.QListView.IconMode)

		self.itemList=[] #list of all current listWidget items.
		self.clear()



	def setAttributes(self, item=None, attributes=None, order=['globalPos'], **kwargs):
		'''
		Works with attributes passed in as a dict or kwargs.
		If attributes are passed in as a dict, kwargs are ignored.
		args:
			item (obj) = listWidget item.
			attributes (dict) = keyword attributes and their corresponding values.
			order (list) = list of string keywords. ie. ['move', 'show']. attributes in this list will be set last, in order of the list. an example would be setting move positions after setting resize arguments.
		kwargs:
			set any keyword arguments.
		'''
		if not attributes:
			attributes = kwargs

		for k in order: #re-order the attributes (with contents of 'order' list last).
			v = attributes.pop(k, None)
			if v:
				from collections import OrderedDict
				attributes = OrderedDict(attributes)
				attributes[k] = v

		for attr, value in attributes.items():
			try:
				if item:
					getattr(item, attr)(value)
				else:
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
			globalPos (QPoint) = move to given global location and center.
		'''
		if attr=='globalPos':
			self.move(self.mapFromGlobal(value - self.rect().center())) #move and center



	def add(self, w, **kwargs):
		'''
		Add items to the menu.

		kwargs:
			show (bool) = show the menu.
			insertSeparator (QAction) = insert separator in front of the given action.
		returns:
			the added item object.

		ex.call: menu().add(w='QAction', setText='', insertSeparator=True)
		'''
		try:
			item = getattr(QtWidgets, w)(self) #ex. QtWidgets.QAction(self) object from string. parented to self.
		except:
			if callable(w):
				item = w(self) #ex. QtWidgets.QAction(self) object. parented to self.
			else:
				item = w #ex. object instance.

		if w=='':
			self.addItem(item)
		if 'QAction' in str(w):
			self.addAction(item)
			# wItem = QtWidgets.QListWidgetItem(self)
			# self.setItemWidget(wItem, menu)
			# self.addItem(wItem)
		elif w is not self:
			wItem = QtWidgets.QListWidgetItem(self)
			self.setItemWidget(wItem, item)
			self.addItem(wItem)


		#set any built-in attributes.
		self.setAttributes(item, kwargs)

		#add to list of all current items.
		self.itemList.append(item)

		return item



	def items(self):
		'''

		'''
		print(self.itemList)
		return self.itemList



	def clear(self):
		'''

		'''
		self.itemList=[]

		return QtWidgets.QListWidget.clear(self)






if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)

	w = QListWidget_()

	w.add('QPushButton', setObjectName='b001', setText='Button1')
	w.add('QPushButton', setObjectName='b002', setText='Button2', setIcon=QtGui.QIcon())
	w.add('QLabel', setObjectName='lbl001', setText='Label1')

	w.show()
	sys.exit(app.exec_())



# --------------------------------


	# def mouseMoveEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QListWidget.mouseMoveEvent(self, event)



	# def showEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QListWidget.showEvent(self, event)



	# def enterEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QListWidget.enterEvent(self, event)



	# def leaveEvent(self, event):
	# 	'''
	# 	args:
	# 		event = <QEvent>
	# 	'''

	# 	return QtWidgets.QListWidget.leaveEvent(self, event)