import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Viewport(Init):
	def __init__(self, *args, **kwargs):
		super(Viewport, self).__init__(*args, **kwargs)

	

	def v000(self): #viewport: back view
		maxEval("max vpt back")

	def v001(self): #viewport: top view
		maxEval("max vpt top")

	def v002(self): #viewport: right view
		maxEval("max vpt right")

	def v003(self): #viewport: left view
		maxEval("max vpt left")

	def v004(self): #viewport: perspective view
		maxEval("max vpt persp user")

	def v005(self): #viewport: front view
		maxEval("max vpt front")

	def v006(self): #viewport: bottom view
		maxEval("max vpt bottom")

	def v007(self): #viewport: align view
		maxEval('''
		max vpt iso user
		max align camera
		''')

	def v008(self): #component mode:vertex
		pm.selectMode (component=True)
		pm.selectType (subdivMeshPoint=1, polymeshVertex=True)
		self.viewPortMessage("<hl>vertex</hl> mask.")

	def v009(self): #component mode:edge
		pm.selectMode (component=True)
		pm.selectType (subdivMeshEdge=1, polymeshEdge=True)
		self.viewPortMessage("<hl>edge</hl> mask.")

	def v010(self): #component mode:facet
		pm.selectMode (component=True)
		pm.selectType (subdivMeshFace=1, polymeshFace=True)
		self.viewPortMessage("<hl>facet</hl> mask.")

	def v011(self): #object mode
		pm.selectMode (object=True)
		self.viewPortMessage("<hl>object</hl> mode.")

	def v012(self): #component mode:uv
		pm.selectMode (component=True)
		pm.selectType (subdivMeshUV=True, polymeshUV=True)
		self.viewPortMessage("<hl>UV</hl> mask.")

	def v013(self): #
		pass

	def v014(self): #
		pass

	def v015(self): #
		pass


#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------