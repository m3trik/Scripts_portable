from __future__ import print_function
from PySide2 import QtCore, QtGui, QtWidgets


import sys




class QTreeWidget_ExpandableList(QtWidgets.QTreeWidget):
	'''
	Additional columns are shown as they are triggered by parent widgets.
	'''
	hoverLeave_ = QtCore.QEvent(QtCore.QEvent.HoverLeave)

	def __init__(self, parent=None):
		super (QTreeWidget_ExpandableList, self).__init__(parent)

		self.setHeaderHidden(True)
		self.setIndentation(0)

		self.widgets={}


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


	def add(self, widget, header=None, parent_=None, column=None, row=0, **kwargs):
		'''
		Add items to the treeWidget.

		kwargs:
			widget (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel
			header (str) = header
		returns:
 			the header name as a string.

		ex.call: create = w.add('QPushButton', setText='Create')
				 cameras = w.add('QPushButton', setText='Cameras')
				 w.add('QPushButton', create, setText='Custom Camera')
		'''
		try:
			widget = getattr(QtWidgets, widget)(self) #ex. QtWidgets.QAction(self) object from string. parented to self.
		except:
			if callable(widget):
				widget = widget(self) #ex. QtWidgets.QAction(self) object. parented to self.

		self.setAttributes(widget, kwargs) #set any built-in attributes.

		header = self.getHeaderFromWidget(widget, header)
		column = self.getColumnFromHeader(header, column)

		wItem = self.getWItemFromRow(row) #get the top widgetItem.
		while self.itemWidget(wItem, column): #while there is a widget in this column:
			wItem = self.itemBelow(wItem) #get the wItem below
			row+=1
		if not wItem:
			wItem = QtWidgets.QTreeWidgetItem(self)


		self.setItemWidget(wItem, column, widget)

		if parent_ is '':
			parent_ = widget.text()
		self.widgets[widget] = [header, column, row, parent_]

		self.setColumnCount(len(self.getColumns()))

		widget.setObjectName(self.__createObjectName(wItem, column)) #set an dynamically generated objectName.
		widget.installEventFilter(self)

		return parent_


	def eventFilter(self, widget, event):
		'''
		'''
		# if not (str(event.type()).split('.')[-1]) in ['QPaintEvent', 'UpdateLater', 'PolishRequest', 'Paint']: print(str(event.type())) #debugging
		if event.type()==QtCore.QEvent.Enter:
			if self.isParent(widget):
				column = self.getColumnFromWidget(widget)
				childColumns = self.getChildColumnsFromWidget(widget)
				if childColumns:
					self.__showColumns([column]+childColumns)
					self.__resize(childColumns)

		if event.type()==QtCore.QEvent.HoverMove:
			if not widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
				QtWidgets.QApplication.sendEvent(widget, self.hoverLeave_)

		if event.type()==QtCore.QEvent.HoverLeave:
			if not __name__=='__main__':
				self.window().grabMouse()
				# print(self.mouseGrabber().objectName(), 'grab --')

		if event.type()==QtCore.QEvent.MouseButtonRelease:
			if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
				wItem = self.getWItemFromWidget(widget)
				row = self.getRowFromWidget(widget)
				column = self.getColumnFromWidget(widget)
				print(widget.text(), wItem, row, column, 8*'*')
				self.itemClicked.emit(wItem, column)
				self.window().hide()

		return super(QTreeWidget_ExpandableList, self).eventFilter(widget, event)


	def leaveEvent(self, event):
		'''
		'''
		self.__resize(0)
		self.__showColumns(0)
		return QtWidgets.QTreeWidget.leaveEvent(self, event)


	def __resize(self, columns, buffer_=25):
		'''
		Resize the treeWidget to fit it's current visible wItems.

		args:
			columns (int)(list) = column index or list of column indices.
			buffer (int) = Amount to additionally resize. (default is 25)
		'''
		if type(columns) is int:
			if columns is 0:
				return self.resize(self.columnWidth(0), self.sizeHint().height())
			columns = [columns]

		for column in columns:
			columnWidth = self.sizeHintForColumn(column)+buffer_
			self.setColumnWidth(column, columnWidth)

		totalWidth = self.columnWidth(0) + sum([self.columnWidth(c) for c in columns])
		self.resize(totalWidth, self.sizeHint().height()) #resize main widget to fit column.


	def __createObjectName(self, wItem, column):
		'''
		Create an objectName for an itemWidget consisting of the parent treeWidget's object name, header, column, and row index.

		args:
			wItem (obj) = QWidgetItem.
			column (int) = The index of the column.
		returns:
			(str) name string.
		'''
		header = self.getHeaderFromColumn(column)
		row = self.getRow(wItem)
		return '{0}|{1}|{2}|{3}'.format(self.objectName(), header, column, row) #ie. 'tree002|Options|0|1'


	def getWItemFromRow(self, row):
		'''
		Get the widgetItem contained in a given row.

		args:
			row (int) = Row index.
		'''
		try:
			return next(wItem for wItem in self.getTopLevelItems() if self.indexOfTopLevelItem(wItem)==row)
		except:
			return None


	def __setHeader(self, header, column=None):
		'''
		Set new header and column or modify an existing.

		args:
			header (str) = header text.
			column (int) = column index.
		returns:
			(str) header text.
		'''
		if column:
			self.headerItem().setText(column, header)
		else: #set new header and column
			self.setHeaderLabel(header)
		return header


	def getHeaderFromWidget(self, widget, __header=None):
		'''
		Get the header that the widget belongs to.

		args:
			widget (obj) = A widget contained in one of the tree's wItems.
			__header (str) = internal use. header to assign as parent. Used when setting parent.
		returns:
			(str) header
		'''
		if __header is not None:
			return __header
		try:
			return self.widgets[widget][0]
		except:
			return None


	def getParentFromHeader(self, header):
		'''
		Get the Headers parent from the header name.

		args:
			header (str) = header name. ie. 'Options'
		'''
		try:
			return next(i[3] for i in self.widgets.values() if i[0]==header)
		except:
			None


	def getHeaderFromColumn(self, column):
		'''
		'''
		try:
			return next(i[0] for i in self.widgets.values() if i[1]==column)
		except:
			return None


	def getRow(self, wItem):
		'''
		Get the stored row index.
		
		args:
			wItem (obj) = QWidgetItem.
		'''
		return self.indexFromItem(wItem).row()


	def getRowFromWidget(self, widget):
		'''
		'''
		return next(self.getRow(i) for c in self.getColumns() for i in self.getTopLevelItems() if self.itemWidget(i, c)==widget)


	def getColumnFromWidget(self, widget):
		'''
		'''
		return next(c for c in self.getColumns() for i in self.getTopLevelItems() if self.itemWidget(i, c)==widget)


	def getChildColumnsFromWidget(self, widget):
		'''
		'''
		header = self.widgets[widget][3]
		try:
			return list(set([i[1] for i in self.widgets.values() if i[0]==header]))
		except:
			return []


	def getColumnFromHeader(self, header, __column=None):
		'''
		Get the stored column index.

		args:
			header (str) = header name.
			__column (int) = internal use.
		'''
		if __column is not None:
			return __column
		try:
			return next(i[1] for i in self.widgets.values() if i[0]==header)
		except: #else assign a new column to the header.
			if not hasattr(self, 'c'):
				self.c = max(self.getColumns()) #get the highest column and increment by one.
			self.c+=1
			return self.c


	def getColumnFromParent(self, parent):
		'''
		Get the stored column index.

		args:
			parent (str) = parent name.
		'''
		try:
			return next(i[1] for i in self.widgets.values() if i[3]==parent)
		except:
			return None


	def getColumns(self):
		'''
		Get all of the columns currently used.

		returns:
			set of ints 
		'''
		try:
			return set([i[1] for i in self.widgets.values()])
		except:
			0


	def __showColumns(self, columns):
		'''
		Unhide the given column, while hiding all others.

		args:
			columns (list) = list of indices of the columns to show.
		'''
		if type(columns)==int:
			columns = [columns]
		for c in self.getColumns():
			if c in columns:
				self.setColumnHidden(c, False)
			else:
				self.setColumnHidden(c, True)


	def getTopLevelItems(self):
		'''
		Get all top level QTreeWidgetItems in the given QTreeWidget.
		
		returns:
			(list) All Top level QTreeWidgetItems
		'''
		return [self.topLevelItem(i) for i in xrange(self.topLevelItemCount())]


	def getWItemFromWidget(self, widget):
		'''
		'''
		try:
			return next(i for c in self.getColumns() for i in self.getTopLevelItems() if self.itemWidget(i, c)==widget)
		except:
			return None


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
			list_ = [self.itemWidget(i, c) for c in self.getColumns() for i in self.getTopLevelItems()]
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


	def isParent(self, widget):
		'''
		'''
		if widget in self.widgets:
			if self.widgets[widget][3] is not None:
				return True
			return False
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
		[self.add(w, parent_='', column=0, setText=t) for t in wItems]


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

	create = tree.add('QPushButton', parent_='Create', column=0, setText='Create')
	tree.add('QPushButton', create, setText='Custom Camera')
	tree.add('QPushButton', create, setText='Set Custom Camera')
	tree.add('QPushButton', create, setText='Camera From View')

	cameras = tree.add('QPushButton', parent_='Cameras', column=0, setText='Cameras')
	tree.add('QPushButton', cameras, setText='Cam1')
	tree.add('QPushButton', cameras, setText='Cam2')

	options = tree.add('QPushButton', cameras, parent_='Options', setText='Options')
	tree.add('QPushButton', options, setText='Opt1')
	tree.add('QPushButton', options, setText='Opt2')


	tree.show()

	sys.exit(app.exec_())






# depricated: ---------------------------------------------------------------------------

