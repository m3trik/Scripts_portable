from __future__ import print_function
from PySide2 import QtCore, QtGui, QtWidgets


import sys




class QTreeWidget_ExpandableList(QtWidgets.QTreeWidget):
	'''
	Additional columns are shown as they are triggered by the widgets in column 0.
	ie.  in column 0 index (row) 0 unhides column 1. index 1 (row 1) unhides column 2.
	
	Uses the widgetItem as a dictionary key to store the row, column, and group (derived from the parent items text).
	_wItems (dict) = wItem(key) : [row, column, group](value as list)
	'''
	hoverLeave_ = QtCore.QEvent(QtCore.QEvent.HoverLeave)

	def __init__(self, parent=None):
		super (QTreeWidget_ExpandableList, self).__init__(parent)

		self.setHeaderHidden(True)
		self.setIndentation(0)

		self._wItems={}

		self.setStyleSheet('''
			QTreeWidget {
				background-color: transparent;
				border:none;
			} 

			QTreeWidget::item {
				height: 20px;
			}

			QTreeView::item:hover {
				background: transparent;
				color: none;
			}

			QTreeView::item:selected {
			    background-color: none;
			}''')



	def setAttributes(self, item=None, attributes=None, order=['moveGlobal'], **kwargs):
		'''
		Works with attributes passed in as a dict or kwargs.
		If attributes are passed in as a dict, kwargs are ignored.

		args:
			attributes (dict) = keyword attributes and their corresponding values.
			order (list) = list of string keywords. ie. ['move', 'show']. attributes in this list will be set last, in order of the list. an example would be setting move positions after setting resize arguments.
		kwargs:
			set any additional keyword arguments.
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
			moveGlobal (QPoint) = move to given global location and center.
		'''
		if attr=='moveGlobal':
			self.move(self.mapFromGlobal(value - self.rect().center())) #move and center


	def add(self, w, g=None, **kwargs):
		'''
		Add items to the treeWidget.

		kwargs:
			w (str)(obj) = widget. ie. w='QLabel' or w=QtWidgets.QLabel
			g (str) = group.
		returns:
			the group name as a string.

		ex.call: create = w.add('QPushButton', setText='Create')
				 cameras = w.add('QPushButton', setText='Cameras')
				 w.add('QPushButton', create, setText='Custom Camera')
		'''
		try:
			item = getattr(QtWidgets, w)(self) #ex. QtWidgets.QAction(self) object from string. parented to self.
		except:
			if callable(w):
				item = w(self) #ex. QtWidgets.QAction(self) object. parented to self.
			else:
				item = w

		self.setAttributes(item, kwargs) #set any built-in attributes.

		column = self.getColumnFromGroup(g)

		wItem = self.getWItemFromRow(0) #get the top widgetItem.
		while self.itemWidget(wItem, column): #while there is a widget in this column:
			wItem = self.itemBelow(wItem) #get the wItem below
		if not wItem:
			wItem = self.__createNewWItem(item)


		self.setItemWidget(wItem, column, item)
		self.setColumnCount(len(self.getColumns()))

		item.setObjectName(self.__createObjectName(wItem, column)) #set an dynamically generated objectName.
		item.installEventFilter(self)

		return g



	def eventFilter(self, widget, event):
		'''
		'''
		# if not (str(event.type()).split('.')[-1]) in ['QPaintEvent', 'UpdateLater', 'PolishRequest', 'Paint']: print(str(event.type())) #debugging
		if event.type()==QtCore.QEvent.Enter:
			group = self.getGroupFromWidget(widget)
			parent = self.getGroupParent(group)
			if widget is parent:
				column = self.getColumnFromGroup(group)
				self.__showColumns(column)
				self.__resize(column)

		if event.type()==QtCore.QEvent.HoverMove:
			if not widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
				QtWidgets.QApplication.sendEvent(widget, self.hoverLeave_)

		if event.type()==QtCore.QEvent.HoverLeave:
			if not __name__=='__main__':
				self.window().grabMouse()

		if event.type()==QtCore.QEvent.MouseButtonRelease:
			wItem = self.getWItemFromWidget(widget)
			row = self.getRowFromWidget(widget)
			print(widget.text())
			column = self.getColumnFromWidget(widget)
			self.itemClicked.emit(wItem, column)
			self.window().hide()


		return super(QTreeWidget_ExpandableList, self).eventFilter(widget, event)


	def getGroupParent(self, group):
		'''
		Get the groups parent from the group name.

		args:
			group (str) = group name. ie. 'Options'
		'''
		for w in self.getWidgets():
			if w.text()==group:
				return w


	def leaveEvent(self, event):
		'''
		'''
		self.__resize(0)
		self.__showColumns(0)
		return QtWidgets.QTreeWidget.leaveEvent(self, event)


	def __resize(self, column, buffer_=25):
		'''
		Resize the treeWidget to fit it's current visible wItems.

		args:
			column (int) = column index.
			buffer (int) = Amount to additionally resize. (default is 25)
		'''
		if column is 0:
			return self.resize(self.columnWidth(0), self.sizeHint().height())

		columnWidth = self.sizeHintForColumn(column)+buffer_
		self.setColumnWidth(column, columnWidth)

		totalWidth = self.columnWidth(0)+columnWidth
		self.resize(totalWidth, self.sizeHint().height()) #resize main widget to fit column.


	def __createNewWItem(self, item):
		'''
		Create a new widgetItem containing the given widget type.

		args:
			item (obj) = QWidget.
		'''
		try:
			g = item.text()
		except:
			g = item.value()
		wItem = QtWidgets.QTreeWidgetItem(self)
		row = self.getRow(wItem)
		self._wItems[wItem] = [row, row+1, g] #use the widgetItem as a dictionary key to store the row, column, and group (derived from the parent items text).
		return wItem


	def __createObjectName(self, wItem, column):
		'''
		Create an objectName for an itemWidget consisting of its group, row index, and column index.

		args:
			wItem (obj) = QWidgetItem.
			column (int) = The index of the column.
		'''
		group = self.getGroup(wItem)
		row = self.getRow(wItem)
		return 'b0{0}{1}|{2}|{3}'.format(row, column, group, self.objectName()) #ie. 'b000|Options|tree002'


	def getWItemFromRow(self, row):
		'''
		Get the widgetItem contained in a given row.

		args:
			row (int) = Row index.
		'''
		try:
			return next(k for k, v in self._wItems.items() if v[0]==row)
		except:
			None


	def getGroup(self, wItem):
		'''
		Get the stored Group.

		args:
			wItem (obj) = QWidgetItem.
		'''
		try:
			return self._wItems[wItem][2]
		except:
			return None


	def getGroupFromWidget(self, widget):
		'''
		Get the group that the widget belongs to.

		args:
			widget (obj) = A widget contained in one of the tree's wItems.
		'''
		try:
			for wItem, v in self._wItems.items():
				for w in self.getWidgets(wItem):
					if w==widget:
						return v[2]
		except:
			return None


	def getRow(self, wItem):
		'''
		Get the stored row index.
		
		args:
			wItem (obj) = QWidgetItem.
		'''
		try:
			return self._wItems[wItem][0]
		except:
			return self.indexFromItem(wItem).row()


	def getRowFromWidget(self, widget):
		'''
		'''
		return next(self.getRow(i) for c in self.getColumns() for i in self.getItems() if self.itemWidget(i, c)==widget)


	def getColumn(self, wItem):
		'''
		Get the stored column index.
		
		args:
			wItem (obj) = QWidgetItem.
		'''
		try:
			if self.itemWidget(wItem, 0):
				return self._wItems[wItem][1]
			else: #
				return 0
		except:
			return self.indexFromItem(wItem).column()


	def getColumnFromWidget(self, widget):
		'''
		'''
		return next(c for c in self.getColumns() for i in self.getItems() if self.itemWidget(i, c)==widget)


	def getColumnFromGroup(self, group):
		'''
		Get the stored column index.

		args:
			group (str) = Group name.
		'''
		if not group:
			return 0
		try:
			return next(v[1] for v in self._wItems.values() if v[2]==group)
		except:
			None


	def getColumns(self):
		'''
		Get all of the columns currently used.

		returns:
			set of ints 
		'''
		try:
			return set([0]+[v[1] for v in self._wItems.values()])
		except:
			0


	def __showColumns(self, columns):
		'''
		Unhide the given column, while hiding all others. Column 0 is always left visible.

		args:
			columns (list) = list of indices of the columns to show.
		'''
		if type(columns)==int:
			columns = [columns]
		for c in [i[1] for i in self._wItems.values()]:
			if c in columns:
				self.setColumnHidden(c, False)
			else:
				self.setColumnHidden(c, True)


	def getItems(self):
		'''
		Get all QTreeWidgetItems in the given QTreeWidget.
		
		returns:
			QTreeWidgetItems (list)
		'''
		return [self.topLevelItem(i) for i in xrange(self.topLevelItemCount())]


	def getWItemFromWidget(self, widget):
		'''
		'''
		return next(i for c in self.getColumns() for i in self.getItems() if self.itemWidget(i, c)==widget)


	def getWidgets(self, wItem=None, removeNoneValues=False):
		'''
		Get the widgets from the given widgetItem, or all widgets if no specific widgetItem is given.

		args:
			wItem (obj) = QWidgetItem.
			removeNoneValues (bool) = Remove any 'None' values from the returned list.
		returns:
			widgets (list)
		'''
		if wItem:
			list_ = [self.itemWidget(wItem, c) for c in self.getColumns()]
		else: 
			list_ = [self.itemWidget(i, c) for c in self.getColumns() for i in self.getItems()]
		if removeNoneValues:
			list_ = [i for i in list_ if not i==None]

		return list_


	def getWidget(self, wItem, column):
		'''
		Get the widget from the widgetItem at the given column (if it exists).

		args:
			wItem (obj) = The widgetItem containing the widget.
			column (int) = The column location on the widget.
		returns:
			(obj) QWidget
		'''
		try:
			return next(w for w in self.getWidgets(wItem) if self.getColumnFromWidget(w)==column)
		except:
			return None


	def getWidgetText(self, wItem, column):
		'''
		Get the widget text from the widgetItem at the given column (if it exists).

		args:
			wItem (obj) = The widgetItem containing the widget.
			column (int) = The column location on the widget.
		returns:
			(str) QWidget's text
		'''
		try:
			return next(w.text() for w in self.getWidgets(wItem) if self.getColumnFromWidget(w)==column)
		except:
			return None


	def convert(self, items, w):
		'''
		Convert itemsWidgets to a given type.

		args:
			w (str) = widget type. ie. 'QPushButton'
			items (list) = QTreeWidgetItems
		'''
		try:
			wItems = [i.text(0) for i in items] #get a string list containing each widgetItem's text string.
		except:
			wItems = [i.value(0) for i in items]
		[self.takeTopLevelItem(self.indexOfTopLevelItem(i)) for i in items] #delete each widgetItem
		for t in wItems:
			self.add(w, setText=t)


	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		try:
			if __name__=='__main__':return
			self.sb
		except:
			from tk_switchboard import sb
			self.sb = sb
			childEvents = self.sb.getClassInstance('EventFactoryFilter')
			childEvents.initWidgetItems(self.getWidgets(removeNoneValues=1), self.sb.getUiName())



if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)

	tree=QTreeWidget_ExpandableList()

	create = tree.add('QPushButton', setText='Create')
	tree.add('QPushButton', create, setText='Custom Camera')
	tree.add('QPushButton', create, setText='Set Custom Camera')
	tree.add('QPushButton', create, setText='Camera From View')

	cameras = tree.add('QPushButton', setText='Cameras')
	tree.add('QPushButton', cameras, setText='Cam1')
	tree.add('QPushButton', cameras, setText='Cam2')

	tree.show()

	sys.exit(app.exec_())






# depricated: ---------------------------------------------------------------------------


	# self.itemClicked.connect(self.test)
	# def test(self, item, column):
	# 	'''
	# 	'''
	# 	print(item, column)