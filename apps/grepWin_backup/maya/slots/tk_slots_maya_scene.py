from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Scene(Init):
	def __init__(self, *args, **kwargs):
		super(Scene, self).__init__(*args, **kwargs)

		self.scene.t000.returnPressed.connect(self.t001) #preform rename on returnPressed


	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.scene.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb000', setToolTip='Maya Scene Editors')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.scene.cmb000

		if index is 'setMenu':
			items = ['Node Editor', 'Outlinder', 'Content Browser', 'Optimize Scene Size', 'Prefix Hierarchy Names', 'Search and Replace Names']
			cmb.addItems_(items, 'Maya Scene Editors')
			return

		if index>0:
			if index==cmb.items.index('Node Editor'):
				mel.eval('NodeEditorWindow;') #
			elif index==cmb.items.index('Outlinder'):
				mel.eval('OutlinerWindow;') #
			elif index==cmb.items.index('Content Browser'):
				mel.eval('ContentBrowserWindow;') #
			elif index==cmb.items.index('Optimize Scene Size'):
				mel.eval('cleanUpScene 2;')
			elif index==cmb.items.index('Prefix Hierarchy Names'):
				mel.eval('prefixHierarchy;') #Add a prefix to all hierarchy names.
			elif index==cmb.items.index('Search and Replace Names'):
				mel.eval('SearchAndReplaceNames;') #performSearchReplaceNames 1; #Rename objects in the scene.
			cmb.setCurrentIndex(0)


	def t000(self, state=None):
		'''Find
		'''
		t000 = self.scene.t000

		if state is 'setMenu':
			t000.contextMenu.add('QCheckBox', setText='Ignore Case', setObjectName='chk000', setToolTip='Search case insensitive.')
			t000.contextMenu.add('QCheckBox', setText='Regular Expression', setObjectName='chk001', setToolTip='When checked, regular expression syntax is used instead of the default \'*\' and \'|\' wildcards.')
			return


	def t001(self, state=None):
		'''Replace
		'''
		t001 = self.scene.t001

		if state is 'setMenu':
			return

		find = self.scene.t000.text() #an asterisk denotes startswith*, *endswith, *contains* 
		to = self.scene.t001.text()
		regEx = self.scene.t000.contextMenu.chk001.isChecked()
		ignoreCase = self.scene.t000.contextMenu.chk000.isChecked()

		Scene.rename(find, to, regEx=regEx, ignoreCase=ignoreCase)


	@staticmethod
	def rename(frm, to, regEx=False, ignoreCase=False):
		'''Rename scene objects.

		:Parameters:
			frm (str) = Current name. An asterisk denotes startswith*, *endswith, *contains*, and multiple search strings can be separated by pipe ('|') chars.
				frm - Search exact.
				*frm* - Search contains chars.
				*frm - Search endswith chars.
				frm* - Search startswith chars.
				frm|frm - Search any of.  can be used in conjuction with other modifiers.
			to (str) = Desired name: An optional asterisk modifier can be used for formatting
				to - replace all.
				*to* - replace only.
				*to - replace suffix.
				**to - append suffix.
				to* - replace prefix.
				to** - append prefix.
			regEx (bool) = If True, regular expression syntax is used instead of the default '*' and '|' modifiers.
			ignoreCase (bool) = Ignore case when searching. Applies only to the 'frm' parameter's search.

		ex. rename(r'Cube', '*001', regEx=True) #replace chars after frm on any object with a name that contains 'Cube'. ie. 'polyCube001' from 'polyCube'
		ex. rename(r'Cube', '**001', regEx=True) #append chars on any object with a name that contains 'Cube'. ie. 'polyCube1001' from 'polyCube1'
		'''
		pm.undoInfo (openChunk=1)
		names = Init.findStrAndFormat(frm, to, [obj.name() for obj in pm.ls()], regEx=regEx, ignoreCase=ignoreCase)
		print ('# Rename: Found {} matches. #'.format(len(names)))

		for oldName, newName in names:
			try:
				if pm.objExists(oldName):
					n = pm.rename(oldName, newName) #Rename the object with the new name
					if not n==newName:
						print ('# Warning: Attempt to rename "{}" to "{}" failed. Renamed instead to "{}". #'.format(oldName, newName, n))
					else:
						print ('# Result: Successfully renamed "{}" to "{}". #'.format(oldName, newName))

			except Exception as e:
				print ('# Error: Attempt to rename "{}" to "{}" failed. {} #'.format(oldName, newName, str(e).rstrip()))
		pm.undoInfo (closeChunk=1)









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------