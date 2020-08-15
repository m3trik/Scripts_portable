# !/usr/bin/python
# coding=utf-8
from builtins import super
from PySide2 import QtCore, QtGui, QtWidgets



class Menu(object):
	'''
	Get Menu instances.
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



class RichText(object):
	'''
	Rich text support for widgets.
	Text with rich text formatting will be set as rich text, otherwise it will be handled as usual.

	args:
		parent (obj) = parent widget.
		alignment (str) = text alignment. valid values are: 'AlignLeft', 'AlignCenter', 'AlignRight'
	'''
	def __init__(self, parent=None, alignment='AlignLeft', **kwargs):
		'''
		'''
		self.alignment = getattr(QtCore.Qt, alignment)

		self.setText = self.setRichText
		self.text = self.richText
		self.sizeHint = self.richTextSizeHint


	@property
	def hasRichText(self):
		'''
		Query whether the widget contains rich text.

		returns:
			(bool)
		'''
		if not hasattr(self, '_hasRichText'):
			self._hasRichText=False

		return self._hasRichText


	@property
	def richTextLabel(self):
		'''
		Return a QLabel and inside a QHBoxLayout.
		'''
		if not hasattr(self, '_richTextLabel'):

			self.__layout = QtWidgets.QHBoxLayout(self)
			self.__layout.setContentsMargins(0, 0, 0, 0)
			# self.__layout.setSpacing(0)

			self._richTextLabel = QtWidgets.QLabel(self)
			self._richTextLabel.setAttribute(QtCore.Qt.WA_TranslucentBackground)
			self._richTextLabel.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
			# self._richTextLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
			self._richTextLabel.setAlignment(self.alignment)

			self.__layout.addWidget(self._richTextLabel)

			self.setRichTextStyle()

		return self._richTextLabel


	def setRichTextStyle(self, textColor='white'):
		self._richTextLabel.setStyleSheet('''
			QLabel {{
				color: {0};
				margin: 3px 0px 0px 0px; /* top, right, bottom, left */
				padding: 0px 5px 0px 5px; /* top, right, bottom, left */
			}}
		'''.format(textColor))


	def setRichText(self, text):
		'''
		If the text string contains rich text formatting:
			Set the rich text label text.
			Add whitespace to the actual widget text until it matches the sizeHint of what it would containing the richTextLabel's text.

		args:
			text (str) = The desired widget's display text.
		'''
		if text and all(i in text for i in ('<','>')): #check the text string for rich text formatting.
			self.richTextLabel.setTextFormat(QtCore.Qt.RichText)
			self.richTextLabel.setText(text)
			self.updateGeometry()

			self.__class__.__base__.setText(self, text) #temporarily set the text to get the sizeHint value.
			self.__richTextSizeHint = self.__class__.__base__.sizeHint(self)

			self.__class__.__base__.setText(self, None) #clear the text, and add whitespaces until the sizeHint is the correct size.
			whiteSpace=' '
			while self.__richTextSizeHint.width()>self.__class__.__base__.sizeHint(self).width():
				self.__class__.__base__.setText(self, whiteSpace)
				whiteSpace += ' '

			self._hasRichText=True

		else:
			self.__class__.__base__.setText(self, text) #set standard widget text


	def richText(self):
		'''
		returns:
			(str) the widget's or the richTextLabel's text.
		'''
		if self.hasRichText:
			text = self.richTextLabel.text()
			return text

		else:
			return self.__class__.__base__.text(self) #return standard widget text


	def richTextSizeHint(self):
		'''
		The richTextSizeHint is the sizeHint of the actual widget if it were containing the text.

		returns:
			(str) the widget's or the richTextLabel's sizeHint.
		'''
		if self.hasRichText:
			return self.__richTextSizeHint

		else:
			return self.__class__.__base__.sizeHint(self) #return standard widget sizeHint



class Attributes(object):
	'''
	Methods for managing object Attributes.
	'''
	def __init__(self):
		'''
		'''

	def setAttributes(self, attributes=None, obj=None, order=['setPosition_', 'setVisible'], **kwargs):
		'''
		Works with attributes passed in as a dict or kwargs.
		If attributes are passed in as a dict, kwargs are ignored.

		args:
			attributes (dict) = keyword attributes and their corresponding values.
			obj (obj) = the child obj or widgetAction to set attributes for. (default=None)
			#order (list) = list of string keywords. ie. ['setPosition_', 'setVisible']. attributes in this list will be set last, by list order. an example would be setting move positions after setting resize arguments, or showing the widget only after other attributes have been set.

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
			setSize_ (list) = size as an x and y value. ie. (40, 80)
			setPosition_ (QPoint)(str) = move to given global position and center. valid string values include: 'cursor', 
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

		elif attr=='setSize_':
			x, y = value
			obj.resize(QtCore.QSize(x, y))

		elif attr=='setPosition_':
			if value is 'cursor':
				value = QtGui.QCursor.pos()
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

		elif attr=='setSpinBoxByValue_':
			self.setSpinBoxByValue(obj, value[0], value[1])

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


	def setSpinBoxByValue(self, spinbox, attribute, value):
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

		if isinstance(value, bool):
			value = int(value)
			minimum = 0
			maximum = 1

		elif isinstance(value, float):
			decimals = str(value)[::-1].find('.') #get decimal places
			step = Attributes.moveDecimalPoint(1, -decimals)

		elif isinstance(value, int):
			decimals = 0

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
