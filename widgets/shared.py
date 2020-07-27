from PySide2 import QtCore, QtGui, QtWidgets



class Menu(object):
	'''
	Parent class for custom widgets.
	'''
	def __init__(self):
		'''
		'''

	@property
	def menu_(self):
		'''
		Get the menu.
		'''
		if not hasattr(self, '_menu'):
			from qMenu_ import QMenu_
			self._menu = QMenu_(self)

		return self._menu


	@property
	def contextMenu(self):
		'''
		Get the context menu.
		'''
		if not hasattr(self, '_contextMenu'):
			from qMenu_ import QMenu_
			self._contextMenu = QMenu_(self, position='cursorPos')

		return self._contextMenu



class Attributes(object):
	'''
	Parent class for custom widgets.
	'''
	def __init__(self):
		'''
		'''

	def setAttributes(self, attributes=None, obj=None, order=['moveGlobal_', 'setVisible'], **kwargs):
		'''
		Works with attributes passed in as a dict or kwargs.
		If attributes are passed in as a dict, kwargs are ignored.

		args:
			attributes (dict) = keyword attributes and their corresponding values.
			obj (obj) = the child obj or widgetAction to set attributes for. (default=None)
			#order (list) = list of string keywords. ie. ['moveGlobal_', 'setVisible']. attributes in this list will be set last, by list order. an example would be setting move positions after setting resize arguments, or showing the widget only after other attributes have been set.

		kwargs:
			set any keyword arguments.
		'''
		if not attributes:
			attributes = kwargs

		if obj is None:
			obj = self

		for k in order:
			v = attributes.pop(k, None)
			if v:
				from collections import OrderedDict
				attributes = OrderedDict(attributes)
				attributes[k] = v

		for attr, value in attributes.items():
			try:
				getattr(obj, attr)(value)

			except AttributeError:
				self.setCustomAttribute(obj, attr, value)


	def setCustomAttribute(self, obj, attr, value):
		'''
		Attributes that throw an AttributeError in 'setAttributes' are sent here, where they can be assigned a value.
		Custom attributes can be set using a trailing underscore convention to aid readability, and differentiate them from standard attributes.

		args:
			obj (obj) = obj (obj) = the child obj or widgetAction to set attributes for.
			attr (str) = custom keyword attribute.
			value (str) = the value corresponding to the given attr.

		attributes:
			copy_ (obj) = widget to copy attributes from.
			moveGlobal_ (QPoint) = move to given global location and center.
			addMenu_ (QMenu) = Used for adding additional menus to a parent menu. ex. parentMenu = QMenu_(); childMenu = QMenu_('Create', addMenu_=parentMenu)
			insertSeparator_ (bool) = insert a line separater before the new widget.
			setLayoutDirection_ (str) = set the layout direction using a string value. ie. 'LeftToRight'
			setAlignment_ (str) = set the alignment using a string value. ie. 'AlignVCenter'
			setButtonSymbols_ (str) = set button symbols using a string value. ex. ie. 'PlusMinus'
			minMax_ (str) = set the min, max, and step value using a string value. ex. '.01-10 step.1'
		'''
		if attr=='copy_':
			obj.setObjectName(value.objectName())
			obj.resize(value.size())
			obj.setText(value.text())
			obj.setWhatsThis(value.whatsThis())

		elif attr=='moveGlobal_':
			obj.move(obj.mapFromGlobal(value - obj.rect().center())) #move and center

		elif attr=='addMenu_':
			value.addMenu(obj)

		elif attr=='insertSeparator_':
			if obj.__class__.__name__=='QAction':
				self.insertSeparator(obj)

		elif attr=='setLayoutDirection_':
			self.setAttributes({'setLayoutDirection':getattr(QtCore.Qt, value)}, obj)

		elif attr=='setAlignment_':
			self.setAttributes({'setAlignment':getattr(QtCore.Qt, value)}, obj)

		elif attr=='setButtonSymbols_':
			self.setAttributes({'setButtonSymbols':getattr(QtWidgets.QAbstractSpinBox, value)}, obj)

		#presets
		elif attr=='minMax_':
			self.setMinMax(obj, value)

		elif attr=='set_by_value_':
			self.setByValue(obj, value[0], value[1])

		else:
			print('Error: {} has no attribute {}'.format(obj, attr))


	def setMinMax(self, spinbox, value):
		'''
		Set the minimum, maximum, and step values for a spinbox using a shorthand string value.

		args:
			spinbox (obj) = spinbox widget.
			value (str) = value as shorthand string. ie. '0.00-100 step1'
		'''
		minimum = float(value.split('-')[0])
		maximum = float(value.split('-')[1].split(' ')[0])
		step = float(value.split(' ')[1].strip('step'))

		self.setAttributes({
			'setMinimum':minimum, 
			'setMaximum':maximum, 
			'setSingleStep':step, 
			'setButtonSymbols_':'NoButtons',
		}, spinbox)


	def setByValue(self, spinbox, attribute, value):
		'''
		
		args:
			spinbox (obj) = spinbox widget.
			attribute (str) = object attribute.
			value (multi) = attribute value.
		'''
		prefix = attribute+': '
		suffix = spinbox.suffix()
		minimum = spinbox.minimum()
		maximum = spinbox.maximum()
		step = spinbox.singleStep()
		decimals = spinbox.decimals()

		if isinstance(value, float):
			decimals = str(value)[::-1].find('.') #get decimal places
			step = Attributes.moveDecimalPoint(1, -decimals)

		elif isinstance(value, int):
			decimals = 0

		elif isinstance(value, bool):
			value = int(value)
			minimum = 0
			maximum = 1

		self.setAttributes({
			'setValue':value,
			'setPrefix':prefix,
			'setSuffix':suffix,
			'setMinimum':minimum, 
			'setMaximum':maximum, 
			'setSingleStep':step, 
			'setDecimals':decimals,
			'setButtonSymbols_':'NoButtons',
		}, spinbox)


	@staticmethod
	def moveDecimalPoint(num, decimal_places):
		'''
		Move the decimal place in a given number.

		args:
			decimal_places (int) = decimal places to move. (works only with values 0 and below.)
		
		returns:
			(float) the given number with it's decimal place moved by the desired amount.
		
		ex. moveDecimalPoint(11.05, -2) returns: 0.1105
		'''
		for _ in range(abs(decimal_places)):

			if decimal_places>0:
				num *= 10; #shifts decimal place right
			else:
				num /= 10.; #shifts decimal place left

		return float(num)









if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)

	sys.exit(app.exec_())



# --------------------------------
# Notes
# --------------------------------

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

# depricated ------------------------------------------------------------------------
