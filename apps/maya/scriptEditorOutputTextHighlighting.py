from PySide2 import QtWidgets, QtGui, QtGui, QtCore

from shiboken2 import wrapInstance
from maya.OpenMayaUI import MQtUtil 





# dependancies: scriptEditorOutput.mel
class SyntaxHighlighter(QtGui.QSyntaxHighlighter):
	'''
	:Parameters:
		parent=parent's widget
	'''
	def __init__(self, parent):
		QtGui.QSyntaxHighlighter.__init__(self, parent) #inherit



	def highlightBlock(self, text):
		'''apply color-syntaxing to text
		:Parameters:
			text=text input
		'''
		rules = [(QtGui.QColor( 90,  90,  90), r"^(//|#).+$"),         #grey 90, 90, 90
				 (QtGui.QColor(205, 200, 120), r"^(//|#) Warning.+$"), #yellow 205, 200, 120
				 (QtGui.QColor(165,  75,  75), r"^(//|#).+Error.+$"),  #red 165, 75, 75
				 (QtGui.QColor(115, 215, 150), r"^(//|#).+Result.+$")] #green 115, 215, 150
		# loop through rules
		for color, pattern in rules:
			keyword = QtGui.QTextCharFormat()
			keyword.setForeground(color)
			# get regexp pattern
			expression = QtCore.QRegExp(pattern)
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
			se_edit = wrapInstance(long(MQtUtil.findControl('cmdScrollFieldReporter%i' %i)), QtWidgets.QTextEdit)
			break
		except TypeError:
			i+=1
	syntax_highlighter = SyntaxHighlighter(se_edit)

	#untested.  send to $cmdScrollFieldReporter explicitly. used in place of above code.
	# cmdScrollFieldReporter = "$cmdScrollFieldReporter"
	# se_edit = wrapInstance(long(MQtUtil.findControl(cmdScrollFieldReporter)), QtWidgets.QTextEdit)
	# syntax_highlighter = SyntaxHighlighter(se_edit)
  


	#unused from original script
	# # try:
	# #     syntax_highlighter.deleteLater()
	# # except:
	# #     pass