from __future__ import print_function
from PySide2 import QtCore, QtGui, QtWidgets


import sys




class QTreeWidget_ExpandableList(QtWidgets.QTreeWidget):
	'''
	Additional columns are shown as they are triggered by parent widgets.
	'''
	enterEvent_	= QtCore.QEvent(QtCore.QEvent.Enter)
	leaveEvent_	= QtCore.QEvent(QtCore.QEvent.Leave)
	hoverEnter_ = QtCore.QEvent(QtCore.QEvent.HoverEnter)
	hoverMove_ = QtCore.QEvent(QtCore.QEvent.HoverMove)
	hoverLeave_ = QtCore.QEvent(QtCore.QEvent.HoverLeave)

	def __init__(self, parent=None, stepColumns=False):
		super (QTreeWidget_ExpandableList, self).__init__(parent)

		self.setHeaderHidden(True)
		self.setIndentation(0)

		self.widgets={}
		self.stepColumns=stepColumns
		self._mouseGrabber=None


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


	def add(self, widget, header='root', parent_=None, **kwargs):
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

		ex. widgets dict
				#QWidget object				#header	  #col #row #parent
				widgets = {
					<Custom Camera>:	['Create',	1, 0, None],
					'<Cameras>':		['root', 	0, 1, 'Cameras'], 
					<Set Custom Camera>:['Create',	1, 1, None], 
					<Cam1>:				['Cameras', 2, 1, None],
					<Cam2>:				['Cameras', 2, 2, None],
					<opt2>:				['Options', 3, 4, None], 
					<Create>:			['root', 	0, 0, 'Create'], 
					<Camera From View>:	['Create', 	1, 2, None], 
					<Options>:			['Cameras', 2, 3, 'Options'], 
					<opt1>:				['Options', 3, 3, None]
				}
		'''
		try:
			widget = getattr(QtWidgets, widget)(self) #ex. QtWidgets.QAction(self) object from string. parented to self.
		except:
			if callable(widget):
				widget = widget(self) #ex. QtWidgets.QAction(self) object. parented to self.

		self.setAttributes(widget, kwargs) #set any built-in attributes.


		header = self.getHeaderFromWidget(widget, header)
		column = self.getColumnFromHeader(header)
		row = self.getStartingRowFromHeader(header)

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
		if not widget.isVisible():
			return super(QTreeWidget_ExpandableList, self).eventFilter(widget, event)

		if event.type()==QtCore.QEvent.HoverEnter:
			print(widget.text(), 'HoverEnter')
			if self.isParent(widget):
				childColumns = self.getChildColumnsFromWidget(widget)
				columns = [0]+childColumns
				self.__setEnabledState(childColumns, widget) #set widgets enabled/disabled
				self._showColumns(columns)
				self._resize(columns)
			else:
				column = self.getColumnFromWidget(widget)
				parentColumns = self.getParentColumnsFromWidget(widget)
				self.__setEnabledState(column, widget) #set widgets enabled/disabled
				self._showColumns([column]+parentColumns)
				self._resize([column]+parentColumns)

		if event.type()==QtCore.QEvent.HoverMove:
			try:
				w = next(w for w in self.widgets.keys() if w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos())) and w.isVisible())
				if not w is self._mouseGrabber:
					if self._mouseGrabber is not None:
						QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.hoverLeave_)
						QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.leaveEvent_)
					if not w is self.mouseGrabber():
						w.grabMouse()
						print('grab:', self.mouseGrabber().objectName())
					self._mouseGrabber = w
					QtWidgets.QApplication.sendEvent(w, self.hoverEnter_)
					QtWidgets.QApplication.sendEvent(w, self.enterEvent_)

			except StopIteration:
				QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.hoverLeave_)

		if event.type()==QtCore.QEvent.HoverLeave:
			print(widget.text(), 'HoverLeave')
			if not __name__=='__main__':
				self.window().grabMouse()
				print('grab:', self.mouseGrabber().objectName(), 'window()')

		if event.type()==QtCore.QEvent.MouseButtonRelease:
			print(widget.text(), 'MouseButtonRelease')
			if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
				wItem = self.getWItemFromWidget(widget)
				row = self.getRowFromWidget(widget)
				column = self.getColumnFromWidget(widget)
				print(widget.text(), wItem, row, column, 8*'*')
				self.itemClicked.emit(wItem, column)
				self.window().hide()

		return super(QTreeWidget_ExpandableList, self).eventFilter(widget, event)


	def EnterEvent(self, event):
		'''
		'''
		print ('EnterEvent')
		self.__setEnabledState(0) #set widgets enabled/disabled
		self._resize(0)
		self._showColumns(0)
		QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.hoverMove_)
		return QtWidgets.QTreeWidget.EnterEvent(self, event)


	def leaveEvent(self, event):
		'''
		'''
		self._resize(0)
		self._showColumns(0)
		return QtWidgets.QTreeWidget.leaveEvent(self, event)


	def _resize(self, columns, buffer_=25, resizeFirstColumn=False, collapseOtherColumns=False):
		'''
		Resize the treeWidget to fit it's current visible wItems.

		args:
			columns (int)(list) = column index or list of column indices.
			buffer (int) = Amount to additionally resize. (default is 25)
		'''
		if type(columns) is int:
			columns = [columns]

		columnWidths=[]
		for column in set(columns):
			if not resizeFirstColumn and column is 0:
				if not hasattr(self, '_columnWidth0'):
					self._columnWidth0 = self.columnWidth(column)
				columnWidth = self._columnWidth0
			else:
				columnWidth = self.sizeHintForColumn(column)+buffer_
			self.setColumnWidth(column, columnWidth)
			columnWidths.append(columnWidth)
		totalWidth = sum(columnWidths) #totalWidth = sum([self.columnWidth(c) for c in columns])
		self.resize(totalWidth, self.sizeHint().height()) #resize main widget to fit column.

		if collapseOtherColumns:
			[self.setColumnWidth(c, 0) for c in self.getColumns() if c not in columns] #set all other column widths to 0


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


	def __setEnabledState(self, columns, widget=None):
		'''
		Disables/Enables widgets along the tree hierarchy.

		args:
			widget (obj) = QWidget. current widget
			columns (list) = column indices.
		'''
		if widget:
			if self.getColumnFromWidget(widget)==(0):
				columns = [0]+columns
			parentWidgets = self.getParentWidgetsFromWidget(widget)
		else:
			parentWidgets = []
		self.setWidgets(widgets=self.getWidgets(columns=columns, inverse=True), setDisabled=True)
		self.setWidgets(widgets=self.getWidgets(columns=columns)+parentWidgets, setEnabled=True)


	def setWidgets(self, widgets, **kwargs):
		'''
		'''
		for w in widgets:
			for k, v in kwargs.items():
				if hasattr(w, k):
					getattr(w, k)(v)


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


	def getParentFromHeader(self, header, returnWidget=False):
		'''
		Get the Headers parent from the header name.

		args:
			header (str) = header name. ie. 'Options'
		'''
		try:
			return next(i[3] for i in self.widgets.values() if i[3]==header)
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
		try:
			return next(c for c in self.getColumns() for i in self.getTopLevelItems() if self.itemWidget(i, c)==widget)
		except:
			return None


	def getChildColumnFromWidget(self, widget):
		'''
		Get the child column of the given widget.

		args:
			widget (obj) = QWidget
		returns:
			(int) child column, or None.
		'''
		header = self.widgets[widget][3]
		try:
			return next(i[1] for i in self.widgets.values() if i[0]==header)
		except:
			return None


	def getParentColumnsFromWidget(self, widget):
		'''
		'''
		header = self.widgets[widget][0]
		columns=[]
		while header is not 'root':
			for i in self.widgets.values():
				if i[3]==header:
					columns.append(i[1])
					header = i[0]
					break
		return columns


	def getParentWidgetsFromWidget(self, widget):
		'''
		'''
		header = self.widgets[widget][0]
		widgets=[]
		while header is not 'root':
			for w, i in self.widgets.items():
				if i[3]==header:
					widgets.append(w)
					header = i[0]
					break
		return widgets


	def getChildColumnsFromWidget(self, widget):
		'''
		Get the child column of the given widget.

		args:
			widget (obj) = QWidget
		returns:
			(list) all child columns (int), or None.
		'''
		header = self.widgets[widget][3]
		try:
			return list(set([i[1] for i in self.widgets.values() if header in i and not i[0] is 'root']))
		except:
			return []


	def getColumnFromHeader(self, header):
		'''
		Get the stored column index.

		args:
			header (str) = header name.
		returns:
			(int) = the column corresponding to the given header.
		'''
		try:
			return next(i[1] for i in self.widgets.values() if i[0]==header)
		except StopIteration: #else assign a new column to the header.
			if not hasattr(self, '_c'):
				self._c = 0 #columns start at 0
				return self._c
			self._c+=1 #and each new column is incremented by 1.
			return self._c


	def getStartingRowFromHeader(self, header):
		'''
		Get the starting row index for a given header's column.
		When the 'stepColumns' flag is True, the starting row corresponds to the parents row index. Else, the starting row is always 0.

		args:
			header (str) = the header of the column to get the starting row of.
		returns:
			(int) = starting row index.
		'''
		if not hasattr(self, '_r'):
			self._r = 0
			return self._r
		if self.stepColumns:
			try:
				return next(i[2] for i in self.widgets.values() if i[3]==header) #return starting row for an existing column.
			except StopIteration:
				self._r+=1
		return self._r


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


	def _showColumns(self, columns):
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


	def getWidgets(self, wItem=None, columns=None, removeNoneValues=False, inverse=False):
		'''
		Get the widgets from the given widgetItem, or all widgets if no specific widgetItem is given.

		args:
			wItem (obj) = QWidgetItem.
			columns (int)(list) = column(s) where widgets are located. single column or a list of columns.
			removeNoneValues (bool) = Remove any 'None' values from the returned list.
			inverse (bool) = get the widgets not associated with the given argument. ie. not in 'columns' or not in 'wItem'. inverse has no effect when returning all widgets.
		returns:
			widgets (list)
		'''
		if wItem:  #get widgets contained in the given widgetItem.
			if columns:
				list_ = [self.itemWidget(wItem, c) for c in columns]
			else:
				list_ = [self.itemWidget(wItem, c) for c in self.getColumns()]

		elif columns:  #get widgets in the given columns.
			if type(columns)==int:
				list_ = [w for w, i in self.widgets.items() if i[1]==columns]
			else:
				list_ = [w for w, i in self.widgets.items() for c in columns if i[1]==c]

		else: #get all widgets
			list_ = [self.itemWidget(i, c) for c in self.getColumns() for i in self.getTopLevelItems()]

		if inverse:
			list_ = [i for i in self.getWidgets() if i not in list_]

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

		return QtWidgets.QTreeWidget.showEvent(self, event)






if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)

	tree=QTreeWidget_ExpandableList(stepColumns=1)

	create = tree.add('QPushButton', parent_='Create', setText='Create')
	tree.add('QPushButton', create, row=1, setText='Custom Camera')
	tree.add('QPushButton', create, row=1, setText='Set Custom Camera')
	tree.add('QPushButton', create, row=1, setText='Camera From View')

	cameras = tree.add('QPushButton', parent_='Cameras', setText='Cameras')
	tree.add('QPushButton', cameras, setText='Cam1')
	tree.add('QPushButton', cameras, setText='Cam2')

	options = tree.add('QPushButton', cameras, parent_='Options', setText='Options')
	tree.add('QPushButton', options, setText='Opt1')
	tree.add('QPushButton', options, setText='Opt2')


	tree.show()

	sys.exit(app.exec_())






# depricated: ---------------------------------------------------------------------------

# #test dict --------------------------------------------
# 	#widget					#header	  #col #row #parent
# widgets = {
# 	'<Custom Camera>':		['Create',	1, 0, None],
# 	'<Cameras>':			['root', 	0, 1, 'Cameras'], 
# 	'<Set Custom Camera>':	['Create',	1, 1, None], 
# 	'<Cam1>':				['Cameras', 2, 1, None],
# 	'<Cam2>':				['Cameras', 2, 2, None],
# 	'<opt2>':				['Options', 3, 4, None], 
# 	'<Create>':				['root', 	0, 0, 'Create'], 
# 	'<Camera From View>':	['Create', 	1, 2, None], 
# 	'<Options>':			['Cameras', 2, 3, 'Options'], 
# 	'<opt1>':				['Options', 3, 3, None]
# }
# # -----------------------------------------------------




# def _resize(self, columns, buffer_=25, resizeFirstColumn=False):
	# 	'''
	# 	Resize the treeWidget to fit it's current visible wItems.

	# 	args:
	# 		columns (int)(list) = column index or list of column indices.
	# 		buffer (int) = Amount to additionally resize. (default is 25)
	# 	'''
	# 	if type(columns) is int:
	# 		columns = [columns]
	# 	for column in set(columns):
	# 		if not resizeFirstColumn and column is 0:
	# 			columnWidth = self.columnWidth(column)
	# 		else:
	# 			columnWidth = self.sizeHintForColumn(column)+buffer_
	# 			self.resizeColumnToContents(column)
	# 		# self.setColumnWidth(column, columnWidth)
	# 		# self.header().resizeSection(column, columnWidth)

	# 	# totalWidth = sum([self.columnWidth(c) for c in columns])
	# 	# self.resize(totalWidth, self.sizeHint().height()) #resize main widget to fit column.


	