import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path


from tk_slots_max_init import Init




class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('main')
		
		# self.getMethod('preferences', 'cmb000')() #init menuSet combobox
		# self.getObject(self.sb.setClass('tk_slots_max_preferences.Preferences'), 'cmb000')[0]()



	def v000(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons', 'b006')()


	def v001(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons','b005')()


	def v002(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons','b012')()


	def v003(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons','b004')()


	def v004(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('edit','b032')()


	def v005(self):
		'''
		
		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons','b009')()


	def v006(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons','b047')()


	def v007(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('selection','b008')()


	def v008(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons','b044')()
		

	def v009(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons','b022')()


	def v010(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons','b007')()


	def v011(self):
		'''
		

		'''
		index = self.sb.getUi('preferences').cmb000.currentIndex()
		
		if index==0: #modeling
			self.getMethod('polygons','b043')()


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

		self.getMethod('scene','b005')()







#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------