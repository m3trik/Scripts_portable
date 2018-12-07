import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt


sel = [s for s in rt.getCurrentSelection()]

objects = sel[:-1]
target = sel[-1]

[obj.center = target.center for obj in objects]
