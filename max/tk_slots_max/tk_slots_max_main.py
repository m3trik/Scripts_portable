import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path


from tk_slots_max_init import Init




class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('main')
		self.menuSet = self.sb.getUi('preferences').cmb000



	def method(self, name, method):
		'''
		#args:
			name='string' class name (lowercase)
			method='string' method name
		#returns:
		 	method object
		'''
		if not self.sb.hasKey(name, 'connectionDict'):
			self.hotBox.signal.buildConnectionDict(name) #construct the signals and slots for the ui 

			print self.sb.getDocString(name, method)
		return self.sb.getMethod(name, method)





	def v000(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons', 'b006')()

		self.hotBox.hide_()
		

	def v001(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b005')()

		self.hotBox.hide_()


	def v002(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b012')()
			self.hotBox.hide_()

		self.hotBox.hide_()

	def v003(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b004')()

		self.hotBox.hide_()

	def v004(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('edit','b032')()

		self.hotBox.hide_()

	def v005(self):
		'''
		
		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b009')()

		self.hotBox.hide_()

	def v006(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b047')()

		self.hotBox.hide_()

	def v007(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('selection','b008')()

		self.hotBox.hide_()

	def v008(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b044')()

		self.hotBox.hide_()

	def v009(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b022')()

		self.hotBox.hide_()

	def v010(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b007')()

		self.hotBox.hide_()

	def v011(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b043')()

		self.hotBox.hide_()

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

		self.method('scene','b005')()







#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------