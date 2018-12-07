import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt


sel = [s for s in rt.getCurrentSelection()]
print sel
# getModContextTM <node> <modifier>
# getModContextBBoxMin <node> <modifier>
#~ print sel.typeInPos, sel.height



for obj in sel:
	obj.pivot = [obj.center.x, obj.center.y, obj.center.z] #center, min, max

	transform = [obj.transform.pos.x, obj.transform.pos.y, obj.transform.pos.z]
	scale = [obj.scale.x, obj.scale.y, obj.scale.z]
	rotate = [obj.rotate.x, obj.rotate.y, obj.rotate.z]
	
	print transform, scale, rotate

