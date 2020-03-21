from tk_slots_maya_init import Init

import os.path



class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('main')



	def v000(self):
		'''
		
		'''
		
		

	def v001(self):
		'''
		
		'''
		


	def v002(self):
		'''
		
		'''
		


	def v003(self):
		'''
		
		'''
		


	def v004(self):
		'''
		
		'''
		


	def v005(self):
		'''
		
		'''
		


	def v006(self):
		'''
		
		'''
		


	def v007(self):
		'''
		
		'''
		


	def v008(self):
		'''
		
		'''
		


	def v009(self):
		'''
		
		'''
		


	def v010(self):
		'''
		
		'''
		


	def v011(self):
		'''
		
		'''
		


	def v012(self):
		'''
		
		'''
		pass


	def v013(self):
		'''
		Minimize Main Application

		'''
		self.sb.getMethod('file', 'b005')()


	def v022(self):
		'''
		
		'''
		


	def v023(self):
		'''
		
		'''
		


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