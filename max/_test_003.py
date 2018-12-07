import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

# from PySide2 import QtCore, QtGui

# from tk_slots_max_init import Init as func



sel = [s for s in rt.getCurrentSelection()]

objects = sel[:-1]
target = sel[-1]

for obj in objects: 
	print obj
	obj.center = target.center