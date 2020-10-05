from __future__ import print_function
from builtins import super
from tk_slots_maya_init import *

import os.path



class Editors(Init):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.dynLayout = self.sb.getUi('dynLayout')
		self.stackedWidget = self.dynLayout.stackedWidget


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.editors.pin

		if state is 'setMenu':
			pin.contextMenu.add(QComboBox_, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.editors.cmb000
		
		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		if index>0:
			if index==cmb.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def getEditorWidget(self, name):
		'''
		Get a maya widget from a given name.

		args:
			name (str) = name of widget
		'''
		_name = '_'+name
		if not hasattr(self, _name):
			w = self.convertToWidget(name)
			self.stackedWidget.addWidget(w)
			setattr(self, _name, w)

		return getattr(self, _name)


	def showEditor(self, name, width=640, height=480):
		'''
		Show, resize, and center the given editor.

		args:
			name (str) = The name of the editor.
			width (int) = The editor's desired width.
			height (int) = The editor's desired height.

		returns:
			(obj) The editor as a QWidget.
		'''
		w = self.getEditorWidget(name)

		self.tk.setUi('dynLayout')
		self.stackedWidget.setCurrentWidget(w)
		self.tk.resize(width, height)
		self.tk.move(QtGui.QCursor.pos() - self.tk.rect().center()) #move window to cursor position and offset from left corner to center

		return w


	def v000(self):
		'''
		Attributes
		'''
		# e = mel.eval('$tmp=$gAttributeEditorForm')
		# self.showEditor(e, 640, 480)
		pm.mel.AttributeEditor()


	def v001(self):
		'''
		Outliner
		'''
		e = mel.eval('$tmp=$gOutlinerForm')

		# if not hasattr(self, 'outlinerEditor_'):
		# 	panel = pm.outlinerPanel()
		# 	self.outliner_ = pm.outlinerPanel(panel, query=True, outlinerEditor=True)
		# 	pm.outlinerEditor(self.outliner_, edit=True, mainListConnection='worldList', selectionConnection='modelList', showShapes=False, showReferenceNodes=False, showReferenceMembers=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showNamespace=True, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, setFilter='defaultSetFilter', ignoreHiddenAttribute=False)

		# e = pm.outlinerEditor(self.outliner_, edit=True, showSelected=True) #expand to the current selection in the outliner.
		w = self.showEditor(e, 260, 740)


	def v002(self):
		'''
		Tool
		'''
		# e = mel.eval('$tmp=$gToolSettingsForm')
		# self.showEditor(e, 461, 480)
		print(pm.toolPropertyWindow())


	def v003(self):
		'''
		Layers
		'''
		e = mel.eval('$tmp=$gLayerEditorForm')
		self.showEditor(e, 320, 480)


	def v004(self):
		'''
		Channels
		'''
		e = mel.eval('$tmp=$gChannelsForm')
		self.showEditor(e, 320, 640)


	def v005(self):
		'''
		Script
		'''
		#e = mel.eval('$tmp=$gScriptEditorPanel')
		# self.showEditor(e, 640, 480)
		pm.mel.ScriptEditor()


	def v006(self):
		'''
		Dependancy Graph

		$editorName = ($panelName+"HyperGraphEd");
		hyperGraph -e 
			-graphLayoutStyle "hierarchicalLayout" 
			-orientation "horiz" 
			-mergeConnections 0
			-zoom 1
			-animateTransition 0
			-showRelationships 1
			-showShapes 0
			-showDeformers 0
			-showExpressions 0
			-showConstraints 0
			-showConnectionFromSelected 0
			-showConnectionToSelected 0
			-showConstraintLabels 0
			-showUnderworld 0
			-showInvisible 0
			-transitionFrames 1
			-opaqueContainers 0
			-freeform 0
			-imagePosition 0 0 
			-imageScale 1
			-imageEnabled 0
			-graphType "DAG" 
			-heatMapDisplay 0
			-updateSelection 1
			-updateNodeAdded 1
			-useDrawOverrideColor 0
			-limitGraphTraversal -1
			-range 0 0 
			-iconSize "smallIcons" 
			-showCachedConnections 0
			$editorName // 
		'''
		#e = mel.eval('$tmp=$gHyperGraphPanel')
		# self.showEditor(e, 640, 480)
		pm.mel.HypergraphHierarchyWindow()









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

# deprecated: -----------------------------------
