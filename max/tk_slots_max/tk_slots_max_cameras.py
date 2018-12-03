import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Cameras(Init):
	def __init__(self, *args, **kwargs):
		super(Cameras, self).__init__(*args, **kwargs)




	def chk000(self): #pin open a separate instance of the ui in a new window
		if self.hotBox.ui.chk000.isChecked():
			print 'chk000'
			self.hotBox.pin(self.hotBox.ui)
		else:
			self.hotBox.pin.hide()

	def b000(self): #
			pass

	def b001(self): #Custom camera
		maxEval('cameraView -edit -camera persp -setCamera $homeName;')

	def b002(self): #Set custom camera
		maxEval('string $homeName = `cameraView -camera persp`;')

	def b003(self): #Camera from view
		maxEval('')

	def b004(self): #Group cameras
		maxEval('''
		if (`objExists cameras`)
		{
		  print "Group 'cameras' already exists";
		}
		else
		{
		  group -world -name cameras side front top persp;
		  hide cameras;
		  // Now add non-default cameras to group
		  if (`objExists back`)
		  {
		  	parent back cameras;
		  }
		  if (`objExists bottom`)
		  {
		  	parent bottom cameras;
		  }
		  if (`objExists left`)
		  {
		  	parent left cameras;
		  }
		  if (`objExists alignToPoly`)
		  {
		  	parent alignToPoly cameras;
		  }
		}
		''')

	def b005(self): #Camera sequencer
		maxEval('SequenceEditor;')

	def b006(self): #Camera set editor
		maxEval('cameraSetEditor;')

	def b007(self): #
		maxEval('')

	def b008(self): #
		mel.eval("")

	def b009(self): #
		maxEval('')


#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------