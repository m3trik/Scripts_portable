import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path


from tk_slots_max_init import Init




class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('main')

		




	def cmb000(self):
		'''
		Menu Set
		'''
		cmb = self.ui.cmb000
		
		list_ = ['Modeling', 'Normals', 'Materials', 'UV']
		contents = self.comboBox(cmb, list_)

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


	def cmb001(self):
		'''
		Convert To
		'''
		cmb = self.ui.cmb001
		
		files = ['']
		contents = self.comboBox(cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				mel.eval('')
			cmb.setCurrentIndex(0)


	def v000(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b006')()


	def v001(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b005')()


	def v002(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b012')()


	def v003(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b004')()


	def v004(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('edit', 'b032')()


	def v005(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b009')()


	def v006(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b047')()


	def v007(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('selection', 'b008')()


	def v008(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b044')()
		

	def v009(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b022')()


	def v010(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b007')()


	def v011(self):
		'''
		
		'''
		index = self.ui.cmb000.currentIndex()
		
		if index==0: #modeling
			self.sb.getMethod('polygons', 'b043')()


	def v012(self):
		'''
		
		'''
		pass


	def v013(self):
		'''
		Minimize Main Application

		'''
		# text = 'Minimize'
		# self.ui.v008.setText(text)

		self.sb.getMethod('file', 'b005')()


	def v024(self):
		'''
		Recent Command: 1
		'''
		self.sb.prevCommand(method=1, as_list=1)[-1]() #execute command at index


	def v025(self):
		'''
		Recent Command: 2
		'''
		self.sb.prevCommand(method=1, as_list=1)[-2]() #execute command at index
			

	def v026(self):
		'''
		Recent Command: 3
		'''
		self.sb.prevCommand(method=1, as_list=1)[-3]() #execute command at index


	def v027(self):
		'''
		Recent Command: 4
		'''
		self.sb.prevCommand(method=1, as_list=1)[-4]() #execute command at index


	def v028(self):
		'''
		Recent Command: 5
		'''
		self.sb.prevCommand(method=1, as_list=1)[-5]() #execute command at index


	def v029(self):
		'''
		Recent Command: 6
		'''
		self.sb.prevCommand(method=1, as_list=1)[-6]() #execute command at index







#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------