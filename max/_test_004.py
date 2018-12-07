import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt


#~ sel = rt.getCurrentSelection()
#~ print sel

#~ source = sel[0]
#~ target = sel[1]

#~ source.center = target.center

sel = [s for s in rt.getCurrentSelection()]

objects = sel[:-1]
target = sel[-1]

[obj.center = target.center for obj in objects]
