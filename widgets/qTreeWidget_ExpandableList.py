from __future__ import print_function
from PySide2 import QtCore, QtGui, QtWidgets
try:
	import shiboken2
except:
	from PySide2 import shiboken2

import sys






class QTreeWidget_ExpandableList(QtWidgets.QTreeWidget):
	'''
	Additional column lists are shown as they are triggered by their parent widgets.

	args:
		parent (obj) = Parent Object.
		stepColumns (bool) = Start child columns at row of its parent widget. Else, always at row 0.
		expandOnHover (bool) = Expand columns on mouse hover.

	ex. widgets dict
		#QWidget object			#header	#col #row #parentHeader
		widgets = {
			<Custom Camera>:	['Create',	1, 0, None],
			<Cameras>:			['root', 	0, 1, 'Cameras'], 
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
	enterEvent_	= QtCore.QEvent(QtCore.QEvent.Enter)
	leaveEvent_	= QtCore.QEvent(QtCore.QEvent.Leave)
	hoverEnter_ = QtCore.QEvent(QtCore.QEvent.HoverEnter)
	hoverMove_ = QtCore.QEvent(QtCore.QEvent.HoverMove)
	hoverLeave_ = QtCore.QEvent(QtCore.QEvent.HoverLeave)


	def __init__(self, parent=None, stepColumns=True, expandOnHover=False):
		super (QTreeWidget_ExpandableList, self).__init__(parent)

		self.refresh=False
		self._mouseGrabber=None
		self.widgets={}
		self._gcWidgets={}

		self.stepColumns=stepColumns
		self.expandOnHover=expandOnHover

		self.setHeaderHidden(True)
		self.setIndentation(0)
		self.setStyleSheet('''
			QTreeWidget {
				background-color: transparent;
				border: none;
			} 

			QTreeWidget::item {
				height: 20px;
				margin-left: 0px;
			}

			QTreeView::item:hover {
				background: transparent;
				color: none;
			}

			QTreeView::item:selected {
			    background-color: none;
			}''')


	def setAttributes(self, item=None, attributes=None, order=['globalPos'], **kwargs):
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
					if item:
						self.setCustomAttribute(attr, value, item)
					else:
						self.setCustomAttribute(attr, value)
				else:
					raise error


	def setCustomAttribute(self, attr, value, item=None):
		'''
		Handle custom keyword arguments.

		args:
			attr (str) = custom keyword attribute.
			value (str) = the value corresponding to the given attr.
		kwargs:
			refresh (bool) = set the header's column to be refreshed on showEvent.
			globalPos (QPoint) = move to given global location and center.
		'''
		if attr=='globalPos':
			self.move(self.mapFromGlobal(value - self.rect().center())) #move and center

		else:
			if item:
				print('Error: {} has no attribute {}'.format(item, attr))
			else:
				print('Error: {} has no attribute {}'.format(self, attr))


	def add(self, widget, header='root', parentHeader=None, refresh=False, **kwargs):
		'''
		Add items to the treeWidget.
		Using custom kwarg refresh=True will flag the header's column contents to be refreshed each time the widget is shown.

		args:
			widget (str)(obj) = widget. ie. 'QLabel' or QtWidgets.QLabel
			header (str) = header.
			parentHeader (str) = parent header.
		returns:
 			the parent header string.

		ex.call:
			create = tree.add('QPushButton', parentHeader='Create', setText='Create')
			tree.add('QPushButton', create, setText='Custom Camera')
			#sublist:
			options = tree.add('QPushButton', create, parentHeader='Options', setText='Options')
			tree.add('QPushButton', options, setText='Opt1')
		'''
		#if header doesn't contain the refresh column flag: return the parent header.
		if self.refresh and self.isRefreshedHeader(header)==False:
			return self.getParentHeaderFromHeader(header)

		#set widget
		try:
			widget = getattr(QtWidgets, widget)(self) #ex. QtWidgets.QAction(self) object from string. parented to self.
		except:
			if callable(widget):
				widget = widget(self) #ex. QtWidgets.QAction(self) object. parented to self.

		#set widgetItem
		header = self.getHeaderFromWidget(widget, header)
		column = self.getColumnFromHeader(header, self.refresh)
		row = self.getStartingRowFromHeader(header)
		parentHeader = self.getParentHeaderFromWidget(widget, parentHeader)

		wItem = self.getWItemFromRow(row) #get the top widgetItem.
		while self.itemWidget(wItem, column): #while there is a widget in this column:
			wItem = self.itemBelow(wItem) #get the wItem below
			row+=1
		if not wItem:
			wItem = QtWidgets.QTreeWidgetItem(self)

		self.widgets[widget] = [header, column, row, parentHeader, refresh] #store the widget and it's column/row/header information.

		self.setItemWidget(wItem, column, widget)
		self.setColumnCount(len(self.getColumns()))

		widget.setObjectName(self._createObjectName(wItem, column)) #set an dynamically generated objectName.
		widget.installEventFilter(self)

		self.setAttributes(widget, kwargs) #set any additional given keyword args for the widget.

		return parentHeader


	def eventFilter(self, widget, event):
		'''
		'''
		# if not (str(event.type()).split('.')[-1]) in ['QPaintEvent', 'UpdateLater', 'PolishRequest', 'Paint']: print(str(event.type())) #debugging
		if widget not in self.widgets or not shiboken2.isValid(widget):
			return False

		if event.type()==QtCore.QEvent.HoverEnter:
			if self.expandOnHover:
				self.resizeAndShowColumns(widget)

		if event.type()==QtCore.QEvent.HoverMove:
			try:
				w = next(w for w in self.widgets.keys() if w.rect().contains(w.mapFromGlobal(QtGui.QCursor.pos())) and w.isVisible())
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
			if self.expandOnHover:
				self.resizeAndShowColumns(widget, reset=True)
			if not __name__=='__main__':
				self.window().grabMouse()

		if event.type()==QtCore.QEvent.MouseButtonRelease:
			if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())):
				wItem = self.getWItemFromWidget(widget)
				row = self.getRowFromWidget(widget)
				column = self.getColumnFromWidget(widget)
				self.itemClicked.emit(wItem, column)
				self.window().hide()

		return super(QTreeWidget_ExpandableList, self).eventFilter(widget, event)


	def leaveEvent(self, event):
		'''
		'''
		self.resizeAndShowColumns(reset=True)
		self._mouseGrabber = self
		
		return QtWidgets.QTreeWidget.leaveEvent(self, event)


	def resizeAndShowColumns(self, widget=None, reset=False):
		'''
		Set size, widget states, and visible columns for a given widget.

		args:
			widget (obj) = QWidget. Required when not doing a reset.
			reset (bool) = set tree to original state.
		'''
		if reset:
			self._showColumns(0)
			self._resize(0)
			self._setEnabledState(0, widget) #set widgets enabled/disabled

		elif self.isParent(widget):
			childColumns = self.getChildColumnsFromWidget(widget)
			columns = [0]+childColumns
			self._setEnabledState(childColumns, widget) #set widgets enabled/disabled
			self._showColumns(columns)
			self._resize(columns)
		else:
			column = self.getColumnFromWidget(widget)
			parentColumns = self.getParentColumnsFromWidget(widget)
			self._setEnabledState(column, widget) #set widgets enabled/disabled
			self._showColumns([column]+parentColumns)
			self._resize([column]+parentColumns)


	def _resize(self, columns, resizeFirstColumn=False, collapseOtherColumns=False):
		'''
		Resize the treeWidget to fit it's current visible wItems.

		args:
			columns (int)(list) = column index or list of column indices.
			resizeFirstColumn (bool) = allow resize of column 0.
			collapseOtherColumns (bool) = set all columns not given in the argument to 0 width.
		'''
		if type(columns) is int:
			columns = [columns]

		columnWidths=[]
		for column in set(columns):
			if column is 0 and not resizeFirstColumn:
				if not hasattr(self, '_columnWidth0'):
					self._columnWidth0 = self.columnWidth(column)
				columnWidth = self._columnWidth0
			else:
				columnWidth = self.sizeHintForColumn(column) #else get the size hint
			self.setColumnWidth(column, columnWidth)
			columnWidths.append(columnWidth)
		totalWidth = sum(columnWidths) #totalWidth = sum([self.columnWidth(c) for c in columns])
		self.resize(totalWidth, self.sizeHint().height()) #resize main widget to fit column.

		if collapseOtherColumns:
			[self.setColumnWidth(c, 0) for c in self.getColumns() if c not in columns] #set all other column widths to 0


	def _setEnabledState(self, columns, widget=None):
		'''
		Disables/Enables widgets along the tree hierarchy.

		args:
			widget (obj) = QWidget. current widget
			columns (int)(list) = column indices.
		'''
		if type(columns) is int:
			columns = [columns]
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


	def _createObjectName(self, wItem, column):
		'''
		Create an objectName for an itemWidget consisting of the parent treeWidget's object name, header, column, and parentHeader.

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


	def _setHeader(self, header, column=None):
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
			__header (str) = internal use. header assignment.
		returns:
			(str) header
		'''
		if __header is not None:
			return __header
		try:
			return self.widgets[widget][0]
		except:
			return None


	def getParentHeaderFromWidget(self, widget, __parentHeader=None):
		'''
		Get the header that the widget belongs to.

		args:
			widget (obj) = A widget contained in one of the tree's wItems.
			__parentHeader (str) = internal use. parentHeader assignment.
		returns:
			(str) parent header
		'''
		if __parentHeader is not None:
			return __parentHeader
		try:
			return self.widgets[widget][3]
		except:
			return None


	def getParentHeaderFromHeader(self, header):
		'''
		Get the parentHeader from the header name.

		args:
			header (str) = header name. ie. 'Options'
		returns:
			(str) the parent's header.
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


	def getColumnFromHeader(self, header, refreshedColumn=False):
		'''
		Get the stored column index.

		args:
			header (str) = header name.
		returns:
			(int) = the column corresponding to the given header.
		'''
		try:
			if refreshedColumn:
				return next(i[1] for i in self._gcWidgets.values() if i and i[0]==header)
			else:
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


	def getColumnFromParentHeader(self, parentHeader):
		'''
		Get the stored column index.

		args:
			parentHeader (str) = parentHeader text.
		'''
		try:
			return next(i[1] for i in self.widgets.values() if i[3]==parentHeader)
		except:
			return None


	def getColumns(self, refreshedColumns=False):
		'''
		Get all of the columns currently used.

		args:
			refreshedColumns (bool) = get only columns flagged as refreshed. Default is False.
		returns:
			(set) set of ints representing column indices. 
		'''
		try:
			if refreshedColumns:
				columns = set([i[1] for i in self.widgets.values() if i[4]])
				# columns = set([i[1] for i in self.widgets.values() if self.isRefreshedHeader(i[0])])
			else:
				columns = set([i[1] for i in self.widgets.values()])
				if not columns: #when not getting refreshed columns, and columns have yet to be stored in the widgets dict, try an alt method.
					raise Exception
		except Exception:
			columns = set([i for i in range(self.columnCount())])
		return columns


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


	def getWidgets(self, wItem=None, columns=None, removeNoneValues=False, refreshedWidgets=False, inverse=False):
		'''
		Get the widgets from the given widgetItem, or all widgets if no specific widgetItem is given.

		args:
			wItem (obj) = QWidgetItem.
			columns (int)(list) = column(s) where widgets are located. single column or a list of columns.
			removeNoneValues (bool) = Remove any 'None' values from the returned list.
			refreshedWidgets (bool) = Return only widgets from a column that is flagged to refresh. ie. it's column header starts with '*'. None values are removed when this argument is set.
			inverse (bool)(iter) = get the widgets not associated with the given argument. ie. not in 'columns' or not in 'wItem'. An iterative can be passed in instead of a bool value. inverse has no effect when returning all widgets.
		returns:
			widgets (list)
		'''
		if wItem:  #get widgets contained in the given widgetItem.
			if columns:
				list_ = [self.itemWidget(wItem, c) for c in columns]
			else:
				list_ = [self.itemWidget(wItem, c) for c in self.getColumns()]

		elif columns is not None:  #get widgets in the given columns.
			if type(columns)==int:
				list_ = [w for w, i in self.widgets.items() if i[1]==columns]
			else:
				list_ = [w for w, i in self.widgets.items() for c in columns if i[1]==c]

		else: #get all widgets
			list_ = [self.itemWidget(i, c) for c in self.getColumns() for i in self.getTopLevelItems()]

		if refreshedWidgets:
			list_ = [w for w in list_ if w is not None and self.isRefreshedHeader(self.getHeaderFromWidget(w))]

		if inverse:
			if isinstance(inverse, (list, tuple, set)):
				list_ = inverse
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


	def isRefreshedHeader(self, header):
		'''
		'''
		try:
			return next(i[4] for i in self.widgets.values() if i[0]==header)
		except StopIteration:
			return None


	def convert(self, items, w, columns=None):
		'''
		Convert itemWidgets to a given type.
		Can be used with Qt Designer to convert columns and their headers to widgets.

		args:
			w (str) = widget type. ie. 'QPushButton'
			items (list) = QTreeWidgetItems

		ex. call
		tree.convert(tree.getTopLevelItems(), 'QLabel')
		'''
		[self.takeTopLevelItem(self.indexOfTopLevelItem(i)) for i in items] #delete each widgetItem

		if columns is None:
			columns = self.getColumns()
		if type(columns)==int:
			columns = [columns]
		for c in columns:
			list_ = [str(i.text(c)) for i in items] #get each widgetItem's text string.

			if c is 0:
				[self.add(w, parentHeader=i, setText=i) for i in list_ if i]
			else:
				header = str(self.headerItem().text(c))
				[self.add(w, header=header, setText=i) for i in list_ if i]


	def clear_(self, columns):
		'''
		'''
		self._gcWidgets={}
		for column in columns:
			for wItem in self.getTopLevelItems():
				widget = self.itemWidget(wItem, column)
				self.removeItemWidget(wItem, column)
				list_ = self.widgets.pop(widget, None) #remove the widget from the widgets dict.
				self._gcWidgets[widget] = list_
				# if widget:
				# 	shiboken2.delete(widget)


	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		try:
			if not __name__=='__main__':
				self.classMethod()

		except:
			p = self.parent()
			while not hasattr(p.window(), 'sb'):
				p = p.parent()

			self.sb = p.window().sb
			self.parentUiName = self.sb.getUiName()
			self.childEvents = self.sb.getClassInstance('EventFactoryFilter')
			self.classMethod = self.sb.getMethod(self.parentUiName, self)
			self.classMethod()

		if self.refresh:
			widgets = self.getWidgets(refreshedWidgets=1) #get only any newly created widgets on each refresh.
		else:
			widgets = self.getWidgets(removeNoneValues=1) #get all widgets on first show.
		self.childEvents.addWidgets(self.parentUiName, widgets) #removeWidgets=self._gcWidgets.keys()

		return QtWidgets.QTreeWidget.showEvent(self, event)


	def hideEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self.refresh = True #init flag stays False after first hide
		refreshedColumns = self.getColumns(refreshedColumns=True)
		if refreshedColumns:
			self.clear_(refreshedColumns)

		return QtWidgets.QTreeWidget.hideEvent(self, event)






if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)

	tree=QTreeWidget_ExpandableList(stepColumns=1)

	create = tree.add('QPushButton', parentHeader='Create', setText='Create')
	tree.add('QLabel', create, setText='Custom Camera')
	tree.add('QLabel', create, setText='Set Custom Camera')
	tree.add('QLabel', create, setText='Camera From View')

	cameras = tree.add('QPushButton', parentHeader='Cameras', setText='Cameras')
	tree.add('QLabel', cameras, setText='Cam1')
	tree.add('QLabel', cameras, setText='Cam2')

	options = tree.add('QPushButton', cameras, parentHeader='Options', setText='Options')
	tree.add('QLabel', options, setText='Opt1')
	tree.add('QLabel', options, setText='Opt2')

	tree.show()
	sys.exit(app.exec_())



# #alternate call example: ------------------------------
# l = ['Create', 'Cameras', 'Editors', 'Options']
# [tree.add('QLabel', parentHeader=t, setText=t) for t in l]

# l = ['Custom Camera','Set Custom Camera','Camera From View']
# [tree.add('QLabel', 'Create', setText=t) for t in l]

# l = ['camera '+str(i) for i in range(6)] #debug: dummy list
# [tree.add('QLabel', '*Cameras', setText=t, refresh=True) for t in l]

# l = ['Group Cameras']
# [tree.add('QLabel', 'Options', setText=t) for t in l]


# #using Qt Designer: ----------------------------------
# tree.convert(tree.getTopLevelItems(), 'QLabel')


# #test dict --------------------------------------------
# 	#widget					#header	  #col #row #parentHeader
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


# depricated: ---------------------------------------------------------------------------



	# def isExistingWidget(self, widget, column, row):
	# 	'''
	# 	'''
	# 	wItem = self.getWItemFromRow(row) #get the top widgetItem.
	# 	if self.itemWidget(wItem, column).text()==widget.text():
	# 		print (widget.text())
	# 		return True



	# def EnterEvent(self, event):
	# 	'''
	# 	'''
	# 	print ('EnterEvent')
	# 	self._setEnabledState(0) #set widgets enabled/disabled
	# 	self._resize(0)
	# 	self._showColumns(0)
	# 	QtWidgets.QApplication.sendEvent(self._mouseGrabber, self.hoverMove_)
		
	# 	return QtWidgets.QTreeWidget.EnterEvent(self, event)

	# def clear_(self):
	# 	'''
	# 	'''
	# 	self.widgets.clear()
	# 	self.clear()
	# 	# for column in self.getColumns():
	# 	# 	if column is not 0:
	# 	# 		for wItem in self.getTopLevelItems():
	# 	# 			widget = self.itemWidget(wItem, column)
	# 	# 			# self.removeItemWidget(wItem, column)
	# 	# 			self.removeChild(wItem, column)
	# 	# 			self.widgets.pop(widget, None) #remove the widget from the widgets dict.
	# 	# 			if widget:
	# 	# 				shiboken2.delete(widget)

	# 	# 		if widget:
	# 	# 			print (widget)
	# 	# 			shiboken2.delete(widget)
	# 	# gc = [w for w in self.widgets if self.getColumnFromWidget(w) is not 0]
	# 	# for widget in gc:
	# 	# 	self.widgets.pop(widget, None) #remove the widget from the widgets dict.
	# 	# 	# if widget:
	# 	# 	# 	shiboken2.delete(widget)


			# className = self.window().sb.getUiName(pascalCase=True)
			# class_ = self.window().sb.getClassInstance(className)
			# self.classMethod = getattr(class_, str(self.objectName()))

	# className = self.window().sb.getUiName(pascalCase=True)
	# class_ = self.window().sb.getClassInstance(className)
	# try:
		# self.classMethod = getattr(class_, str(self.objectName()))
	# except AttributeError as error:
	# 	print('Error:', self.__class__.__name__, 'in getattr:', error, '')