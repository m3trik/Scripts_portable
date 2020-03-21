from tk_slots_max_init import Init
maxEval = Init.maxEval

import os.path



class Preferences(Init):
	def __init__(self, *args, **kwargs):
		super(Preferences, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('preferences')

		self.ui.b010.setText('3dsMax Preferences')

		self.cmb001(init=1) #init cmb001
		self.cmb002(init=1) #init cmb002



	# def cmb000(self, index=None):
	# 	'''
	# 	Custom Menu Set
	# 	'''
	# 	cmb = self.ui.cmb000
		
	# 	list_ = ['Modeling', 'Normals', 'Materials', 'UV'] #combobox list menu corresponding to the button text sets.
	# 	contents = cmb.addItems_(list_, 'Menu Sets')

	# 	if not index:
			# index = cmb.currentIndex()
	# 	buttons = self.getObject(self.sb.getUi('main'), 'v000-11') #the ui in which the changes are to be made.
	# 	for i, button in enumerate(buttons):
	# 		if index==1: #set the text for each button.
	# 			button.setText(['','','','','','','','','','','',''][i])

	# 		if index==2:
	# 			button.setText(['','','','','','','','','','','',''][i])


	def cmb000(self, index=None, init=False):
		'''
		Preferences:Ui - Set main ui style using QStyleFactory
		'''
		cmb = self.ui.cmb000

		from PySide2 import QtGui, QtCore
		list_ = QtGui.QStyleFactory.keys() #get styles from QStyleFactory
		contents = cmb.addItems_(list_)

		if init: #temp.  move main function to shared Slots class
			index = self.styleComboBox.findText(QtGui.qApp.style().objectName(), QtCore.Qt.MatchFixedString)
			cmb.setCurrentIndex(index)
		else:
			index = self.styleComboBox.findText(QtGui.qApp.style().objectName(), QtCore.Qt.MatchFixedString)
			cmb.setCurrentIndex(index)

			QtGui.qApp.setStyle(style)


	def cmb001(self, index=None, init=False):
		'''
		Preferences:App - Set Working Units: Linear
		'''
		cmb = self.ui.cmb001

		list_ = ['millimeter','centimeter','meter','kilometer','inch','foot','yard','mile']
		contents = cmb.addItems_(list_)

		# if init:
		# 	index = contents.index(pm.currentUnit(query=1, fullName=1, linear=1)) #get/set current linear value
		# 	cmb.setCurrentIndex(index)
		# else:
		# 	pm.currentUnit(linear=contents[index]) #millimeter | centimeter | meter | kilometer | inch | foot | yard | mile


	def cmb002(self, index=None, init=False):
		'''
		Preferences:App - Set Working Units: Time
		'''
		cmb = self.ui.cmb002

		#store a corresponding value for each item in the comboBox list_.
		l = [('15 fps: ','game'),('24 fps: ','film'),('25 fps: ','pal'),('30 fps: ','ntsc'),('48 fps: ','show'),('50 fps: ','palf'),('60 fps: ','ntscf')]
		list_ = [i[0]+i[1] for i in l] #ie. ['15 fps: game','24 fps: film', ..etc]
		values = [i[1] for i in l] #ie. ['game','film', ..etc]

		contents = cmb.addItems_(list_)

		# if init:
		# 	index = values.index(pm.currentUnit(query=1, fullName=1, time=1)) #get/set current time value
		# 	cmb.setCurrentIndex(index)
		# else:
		# 	pm.currentUnit(time=values[index]) #game | film | pal | ntsc | show | palf | ntscf


	def cmb003(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb003

		files = ['']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Init Tk_Main
		'''
		print "init: tk_main"
		reload(tk_main)


	def b001(self):
		'''
		Color Settings
		'''
		maxEval('colorPrefWnd;')

	
	def b002(self):
		'''
		
		'''
		pass


	def b003(self):
		'''
		
		'''
		pass


	def b004(self):
		'''
		
		'''
		pass


	def b005(self):
		'''
		
		'''
		pass


	def b006(self):
		'''
		
		'''
		pass


	def b007(self):
		'''
		
		'''
		pass


	def b008(self):
		'''
		Hotkeys
		'''
		mel.eval("HotkeyPreferencesWindow;")


	def b009(self):
		'''
		Plug-In Manager
		'''
		maxEval('PluginManager;')


	def b010(self):
		'''
		Settings/Preferences
		'''
		mel.eval("PreferencesWindow;")






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------