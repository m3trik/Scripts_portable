import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path


from tk_slots_max_init import Init




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
			self.hotBox.signal.buildConnectionDict(name) #construct the signals and slots for the ui 

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
		
		# self.hotBox.sb.method('edit','b032')
		for obj in rt.selection:
			obj.EditablePoly.Remove()
		print '# Result: '+text+' #'

	def v005(self):
		'''
		Delete Loop

		'''
		for edge in rt.selection:
			edge.SelectEdgeLoop()
			edge.EditablePoly.Remove()

	def v006(self):
		'''
		Toggle Mode

		'''
		self.cycle([0,1,2,3,4], 'shortCutMode')

	def v007(self):
		'''
		Minimize Main Application

		'''
		obj = rt.createOLEObject('Shell.Application')
		obj.minimizeAll()
		#obj.undoMinimizeAll()
		rt.releaseOLEObject(obj)
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




# component mode:vertex
# 		pm.selectMode (component=True)
# 		pm.selectType (subdivMeshPoint=1, polymeshVertex=True)
# 		self.viewPortMessage("<hl>vertex</hl> mask.")

# component mode:edge
# 		pm.selectMode (component=True)
# 		pm.selectType (subdivMeshEdge=1, polymeshEdge=True)
# 		self.viewPortMessage("<hl>edge</hl> mask.")

# component mode:facet
# 		pm.selectMode (component=True)
# 		pm.selectType (subdivMeshFace=1, polymeshFace=True)
# 		self.viewPortMessage("<hl>facet</hl> mask.")

# object mode
# 		pm.selectMode (object=True)
# 		self.viewPortMessage("<hl>object</hl> mode.")

# component mode:uv
# 		pm.selectMode (component=True)
# 		pm.selectType (subdivMeshUV=True, polymeshUV=True)
# 		self.viewPortMessage("<hl>UV</hl> mask.")