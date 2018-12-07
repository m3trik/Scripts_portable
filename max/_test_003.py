import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

# from PySide2 import QtCore, QtGui

# from tk_slots_max_init import Init as func



source = rt.getNodeByName('Point001')
target = rt.getNodeByName('Box001')

source.center = target.center