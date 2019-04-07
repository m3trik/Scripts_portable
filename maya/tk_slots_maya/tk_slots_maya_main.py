import maya.mel as mel
import pymel.core as pm

import os.path


from tk_slots_maya_init import Init




class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)





	def method(self, name, method):
		'''
		#args:
			name='string' class name (lowercase)
			method='string' method name
		#returns:
		 	method object
		'''
		if not self.sb.hasKey(name, 'connectionDict'):
			self.hotBox.signal.buildConnectionDict() #construct the signals and slots for the ui 

		return self.sb.getMethod(name, method)




	def v000(self):
		'''
		Extrude

		'''
		text = 'Extrude'
		self.hotBox.ui.v000.setText(text)

		self.method('polygons', 'b006')()

		
		print '# Result: '+text+' #'

	def v001(self):
		'''
		Bridge

		'''
		text = 'Bridge'
		self.hotBox.ui.v001.setText(text)

		self.method('polygons','b005')()


		print '# Result: '+text+' #'

	def v002(self):
		'''
		Multi-Cut Tool

		'''
		text = 'Multi-Cut'
		self.hotBox.ui.v002.setText(text)

		self.method('polygons','b012')()
		print '# Result: '+text+' #'

	def v003(self):
		'''
		Delete History

		'''
		text = 'Delete History'
		self.hotBox.ui.v003.setText(text)

		self.method('edit','b016')()
		print '# Result: '+text+' #'

	def v004(self):
		'''
		Delete

		'''
		text = 'Delete'
		self.hotBox.ui.v004.setText(text)
		
		pm.delete()
		# self.hotBox.sb.getMethod('edit','b032')
		print "# Result: delete #"

	def v005(self):
		'''
		

		'''
		pass

	def v006(self):
		'''
		Toggle Mode

		'''
		self.cycle([0,1,2,3,4], 'shortCutMode')

	def v007(self):
		'''
		Minimize Main Application

		'''
		mel.eval("minimizeApp;")
		self.hotBox.hbHide()

	def v008(self):
		'''
		

		'''
		pass

	def v009(self):
		'''
		

		'''
		pass

	def v010(self):
		'''
		

		'''
		pass

	def v011(self):
		'''
		

		'''
		pass

	def v012(self):
		'''
		Chamfer

		'''
		text = 'Chamfer'
		self.hotBox.ui.v003.setText(text)

		self.method('polygons','b007')()
		print '# Result: '+text+' #'

	def v013(self):
		'''
		Target Weld

		'''
		text = 'Target Weld'
		self.hotBox.ui.v003.setText(text)

		self.method('polygons','b043')()
		print '# Result: '+text+' #'



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------