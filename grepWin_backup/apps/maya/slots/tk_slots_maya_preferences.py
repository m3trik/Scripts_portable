from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Preferences(Init):
	def __init__(self, *args, **kwargs):
		super(Preferences, self).__init__(*args, **kwargs)

		self.preferences.b010.setText('Maya Preferences')


	def d000(self, state=None):
		'''Context menu
		'''
		d000 = self.preferences.d000

		if state is 'setMenu':
			d000.contextMenu.add(wgts.TkComboBox, setObjectName='cmb003', setToolTip='')
			return


	def cmb000(self, index=None):
		'''Ui Style: Set main ui style using QStyleFactory
		'''
		cmb = self.preferences.cmb000

		if index is 'setMenu':
			from PySide2 import QtWidgets, QtCore
			list_ = QtWidgets.QStyleFactory.keys() #get styles from QStyleFactory
			cmb.addItems_(list_)
			try:
				index = self.styleComboBox.findText(QtGui.qApp.style().objectName(), QtCore.Qt.MatchFixedString)
				cmb.setCurrentIndex(index)
			except:
				pass
			return

		if index is not None:
			QtGui.qApp.setStyle(cmb.items[index])


	def cmb001(self, index=None):
		'''Set Working Units: Linear
		'''
		cmb = self.preferences.cmb001

		if index is 'setMenu':
			list_ = ['millimeter','centimeter','meter','kilometer','inch','foot','yard','mile']
			cmb.addItems_(list_)
			try:
				index = cmb.items.index(pm.currentUnit(query=1, fullName=1, linear=1)) #get/set current linear value
				cmb.setCurrentIndex(index)
			except:
				pass
			return

		if index is not None:
			pm.currentUnit(linear=cmb.items[index]) #millimeter | centimeter | meter | kilometer | inch | foot | yard | mile


	def cmb002(self, index=None):
		'''Set Working Units: Time
		'''
		cmb = self.preferences.cmb002

		if index is 'setMenu':
			#store a corresponding value for each item in the comboBox list_.
			l = [('15 fps: ','game'),('24 fps: ','film'),('25 fps: ','pal'),('30 fps: ','ntsc'),('48 fps: ','show'),('50 fps: ','palf'),('60 fps: ','ntscf')]
			list_ = [i[0]+i[1] for i in l] #ie. ['15 fps: game','24 fps: film', ..etc]
			values = [i[1] for i in l] #ie. ['game','film', ..etc]
			cmb.addItems_(list_)
			try:
				index = cmb.items.index(pm.currentUnit(query=1, fullName=1, time=1)) #get/set current time value
				cmb.setCurrentIndex(index)
			except:
				pass
			return

		if index is not None:
			pm.currentUnit(time=cmb.items[index]) #game | film | pal | ntsc | show | palf | ntscf


	def cmb003(self, index=None):
		'''Editors
		'''
		cmb = self.preferences.cmb003

		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def b001(self):
		'''Color Settings

		'''
		mel.eval('colorPrefWnd;')


	def b008(self):
		'''Hotkeys

		'''
		mel.eval("HotkeyPreferencesWindow;")


	def b009(self):
		'''Plug-In Manager

		'''
		mel.eval('PluginManager;')


	def b010(self):
		'''Settings/Preferences

		'''
		mel.eval("PreferencesWindow;")









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------



#deprecated

# def cmb000(self):
# 	'''
# 	Custom Menu Set
# 	'''
# 	cmb = self.preferences.cmb000
	
# 	list_ = ['Modeling', 'Normals', 'Materials', 'UV'] #combobox list menu corresponding to the button text sets.
# 	contents = cmb.addItems_(list_, 'Menu Sets')

# 	if not index:
		# index = cmb.currentIndex()
# 	buttons = self.getObjects(sb.getUi('main'), 'v000-11') #the ui in which the changes are to be made.
# 	for i, button in enumerate(buttons):
# 		if index==1: #set the text for each button.
# 			button.setText(['','','','','','','','','','','',''][i])

# 		if index==2:
# 			button.setText(['','','','','','','','','','','',''][i])