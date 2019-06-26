import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt




infoDict={}
selection = rt.selection

level = rt.subObjectLevel
print level

if not level: #object level
	selCount = len(selection) #number of selected objects
	selectedObjects={}; [selectedObjects.setdefault(str(rt.classOf(s.baseObject)),[]).append(str(s.name)) for s in selection] #for any selected objects, set object type as key and append object names as value. if key doesn't exist, use setdefault to initialize an empty list and append. ie. {'joint': ['joint_root_0', 'joint_lower_L8', 'joint_lower_L3']}
	infoDict.update({'Objects: ':selectedObjects}) #currently selected objects



print infoDict



def createWidget(ui, type, offset, axis):
	pass





