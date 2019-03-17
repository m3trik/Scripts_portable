import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

# from PySide2 import QtCore, QtGui

# from tk_slots_max_init import Init as func


angle=10
maxEval('$.selectByAngle = on')
maxEval('$.selectAngle='+str(angle))


# maxEval('$.selectByAngle = off')


# def cmb000(self): #list scene cameras
# 		index = self.hotBox.ui.cmb000.currentIndex() #get current index before refreshing list
# 		cameras = [cam.name for cam in rt.cameras if 'Target' not in cam.name]
# 		items = self.comboBox (self.hotBox.ui.cmb000, cameras, "Cameras:")
		
# 		if index!=0:
# 			rt.select (rt.getNodeByName(items[index]))
# 			self.hotBox.ui.cmb000.setCurrentIndex(0)

# def b005(self): #move to
# 	sel = [s for s in rt.getCurrentSelection()] #rebuild selection array in python.

# 	objects = sel[:-1]
# 	target = sel[-1]
# 	#move object(s) to center of the last selected items bounding box
# 	for obj in objects: 
# 		obj.center = target.center