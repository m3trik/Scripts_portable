import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Preferences(Init):
	def __init__(self, *args, **kwargs):
		super(Preferences, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('preferences')

		self.ui.b010.setText(self.hotBox.app.capitalize()+' Preferences')


		self.cmb001(init=1) #init cmb001
		self.cmb002(init=1) #init cmb002


	def cmb000(self):
		'''
		Select Menu Set
		'''
		cmb = self.ui.cmb000

		list_ = ['Modeling', 'Normals', 'Materials', 'UV']
		contents = self.comboBox (cmb, list_)

		index = cmb.currentIndex()
		buttons = self.getObject(self.sb.getUi('main'), 'v000-11')
		for i, button in enumerate(buttons):
			if index==0:
				button.setText(['Extrude','Bridge','Cut','Slice','Delete','Collapse','Insert Loop','Select Loop','Detach','Attach','Chamfer','Target Weld'][i])

			if index==1:
				button.setText(['','','','','','','','','','','',''][i])

			if index==2:
				button.setText(['','','','','','','','','','','',''][i])

			if index==3:
				button.setText(['','','','','','','','','','','',''][i])


	def cmb001(self, init=False):
		'''
		Set Working Units: Linear
		'''
		cmb = self.ui.cmb001

		units = ['millimeter','centimeter','meter','kilometer','inch','foot','yard','mile']
		contents = self.comboBox (cmb, units)

		if init:
			index = self.ui.cmb001.findText(pm.currentUnit(query=1, fullName=1, linear=1)) #set current linear value
			self.ui.cmb001.setCurrentIndex(index)
		else:
			index = cmb.currentIndex()
			pm.currentUnit(linear=contents[index]) #millimeter | centimeter | meter | kilometer | inch | foot | yard | mile


	def cmb002(self, init=False):
		'''
		Set Working Units: Time
		'''
		cmb = self.ui.cmb002

		list_ = ['15 fps: game','24 fps: film','25 fps: pal','30 fps: ntsc','48 fps: show','50 fps: palf','60 fps: ntscf'] #combobox items
		time = ['game','film','pal','ntsc','show','palf','ntscf'] #corresponding command flags at same index
		contents = self.comboBox (cmb, list_)

		if init:
			index = time.index(pm.currentUnit(query=1, fullName=1, time=1)) #set current time value
			self.ui.cmb002.setCurrentIndex(index)
		else:
			index = cmb.currentIndex()
			pm.currentUnit(time=time[index]) #game | film | pal | ntsc | show | palf | ntscf


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