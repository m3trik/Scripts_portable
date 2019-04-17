import maya.mel as mel
import pymel.core as pm

import os.path


from tk_slots_maya_init import Init




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

		

	def v001(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b005')()


	def v002(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b012')()
			self.hotBox.hide_()


	def v003(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b004')()


	def v004(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('edit','b032')()


	def v005(self):
		'''
		
		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b009')()


	def v006(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b047')()


	def v007(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('selection','b008')()


	def v008(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b044')()


	def v009(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b022')()


	def v010(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b007')()


	def v011(self):
		'''
		

		'''
		text = self.menuSet.currentText()
		
		if text=='Modeling':
			self.method('polygons','b043')()


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