from PySide2.QtWidgets  import QTextEdit
from PySide2.QtGui      import QSyntaxHighlighter, QColor, QTextCharFormat#, QFont
from PySide2.QtCore     import QRegExp

from shiboken2          import wrapInstance
from maya.OpenMayaUI    import MQtUtil 


# dependancies: scriptEditorOutput.mel

class SH(QSyntaxHighlighter):
	'''
	Syntax Highlight class, used by all SK_*_Codes SHs
	:param parent: parent's widget
	'''
	def __init__(self, parent):
		QSyntaxHighlighter.__init__(self, parent) #inherit
		self.parent = parent #define parent explicitly
		
	def highlightBlock(self, text):
		# Derived from Qt function, used to apply color-syntaxing to text
		# :param text: text input
		
		rules = [(QColor( 90,  90,  90), r"^(//|#).+$"),         #grey 90, 90, 90
				 (QColor(205, 200, 120), r"^(//|#) Warning.+$"), #yellow 205, 200, 120
				 (QColor(165,  75,  75), r"^(//|#).+Error.+$"),  #red 165, 75, 75
				 (QColor(115, 215, 150), r"^(//|#).+Result.+$")] #green 115, 215, 150
		# loop through rules
		for color, pattern in rules:
			keyword = QTextCharFormat()
			keyword.setForeground(color)
			# get regexp pattern
			expression = QRegExp(pattern)
			index = expression.indexIn(text)
			# loop until all matches are done
			while index >= 0:
				length = expression.matchedLength()
				# format text with current formatting
				self.setFormat(index, length, keyword)
				index = expression.indexIn(text, index + length)
		self.setCurrentBlockState(0)


def wrap():
	i=1
	while i:
		try:
			se_edit = wrapInstance(long(MQtUtil.findControl('cmdScrollFieldReporter%i' %i)), QTextEdit)
			break
		except TypeError:
			i+=1
	syntax_highlighter = SH(se_edit)

	#untested.  send to $tk_cmdScrollFieldReporter explicitly. used in place of above code.
	# cmdScrollFieldReporter = "$tk_cmdScrollFieldReporter"
	# se_edit = wrapInstance(long(MQtUtil.findControl(cmdScrollFieldReporter)), QTextEdit)
	# syntax_highlighter = SH(se_edit)
  


	#unused from original script
	# # try:
	# #     syntax_highlighter.deleteLater()
	# # except:
	# #     pass