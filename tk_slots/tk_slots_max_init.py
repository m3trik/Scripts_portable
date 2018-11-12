import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots import Slot




class Init(Slot):
	def __init__(self, *args, **kwargs):
		super(Init, self).__init__(*args, **kwargs)

		#init widgets
		initWidgets(self)


		# self.ui.t000.clearFocus()
		self.ui.t000.viewport().setAutoFillBackground(False)
		self.ui.t000.setTextBackgroundColor(QtGui.QColor(50, 50, 50))


		# live surface #state and obj might need to be saved in external file
		# 'main' shorcut mode: ie. polygons, uv's, etc
		# pm.helpLine(width=20, height=8)
		# progress bar


	def info(self): #get current attributes. those with relavant values will be displayed.
		info={}
		# selection = pm.ls(selection=1)
		# objects = pm.ls(selection=1, objectsOnly=1)
		# value = len(objects); info.update({"selected objects: ":value}) #number of selected objects
		# currentSelection = [str(s) for s in pm.ls (selection=1)]; info.update({"Current Selection: ":currentSelection}) #currently selected objects
		
		# if selection: numQuads = pm.polyEvaluate (selection[0], face=1); info.update({"Num Quads: ":numQuads}) #number of faces

		# symmetry = pm.symmetricModelling(query=1, symmetry=1);
		# if symmetry==1: symmetry=True; info.update({"symmetry: ":symmetry}) #symmetry state
		# if symmetry: axis = pm.symmetricModelling(query=1, axis=1); info.update({"symmetry axis: ":axis}) #symmetry axis

		# xformConstraint = pm.xformConstraint(query=True, type=True)
		# if xformConstraint=='none': xformConstraint=None; info.update({"xform constrait: ":xformConstraint}) #transform constraits

		# value = pm.polyEvaluate(vertexComponent=1); info.update({"selected vertices: ":value}) #selected verts
		# value = pm.polyEvaluate(edgeComponent=1); info.update({"selected edges: ":value}) #selected edges
		# value = pm.polyEvaluate(faceComponent=1); info.update({"selected faces: ":value}) #selected faces
		# value = pm.polyEvaluate(uvComponent=1); info.update({"selected uv's: ":value}) #selected uv's

		#populate the textedit with any values
		for key, value in info.iteritems():
			if value:
				# self.ui.t000.setText(key+str(value)+'<br>') #<br> html break newline
				self.ui.t000.setHtml(key+str(value)+'<br>') #<br> html break newline








#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------