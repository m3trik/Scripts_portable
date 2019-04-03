import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path


from tk_slots_max_init import Init




class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)


		




	def v000(self):
		'''
		Extrude

		'''
		text = 'Extrude'
		self.hotBox.ui.v000.setText(text)

		self.hotBox.sb.getMethod('polygons','b006')
		print "# Result: perform extrude #"

	def v001(self):
		'''
		Bridge

		'''
		text = 'Bridge'
		self.hotBox.ui.v001.setText(text)

		self.hotBox.sb.getMethod('polygons','b005')
		print "# Result: bridge #"

	def v002(self):
		'''
		Multi-Cut Tool

		'''
		text = 'Multi-Cut'
		self.hotBox.ui.v002.setText(text)

		self.hotBox.sb.getMethod('polygons','b012')
		print "# Result: multi-cut #"

	def v003(self):
		'''
		Delete History

		'''
		text = 'Delete History'
		self.hotBox.ui.v003.setText(text)

		self.hotBox.sb.getMethod('edit','b016')
		print "# Result: delete history #"

	def v004(self):
		'''
		Delete

		'''
		text = 'Delete'
		self.hotBox.ui.v004.setText(text)
		
		# self.hotBox.sb.getMethod('edit','b032')
		for obj in rt.selection:
			obj.EditablePoly.Remove()
		print "# Result: delete #"

	def v005(self):
		'''
		

		'''
		pass

	def v006(self):
		'''
		Toggle Mode

		'''
		self.cycle('shortCutMode_01234')

	def v007(self):
		'''
		Minimize Main Application

		'''
		mel.eval("minimizeApp;")
		self.hotBox.hbHide()







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