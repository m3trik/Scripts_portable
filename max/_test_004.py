import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

#-------------------------------------------------------------------------------

sel = [s for s in rt.getCurrentSelection()]
print sel

#~ for obj in sel:
	#~ obj.pivot = [obj.center.x, obj.center.y, obj.center.z] #center, min, max

	#~ transform = [obj.transform.pos.x, obj.transform.pos.y, obj.transform.pos.z]
	#~ scale = [obj.scale.x, obj.scale.y, obj.scale.z]
	#~ rotation = [obj.rotation.x, obj.rotation.y, obj.rotation.z]
	
	#~ print transform, scale, rotation
#-------------------------------------------------------------------------------

oldActiveView = viewport.activeViewport
	viewport.activeViewport = source_index
	type = viewport.getType()
	tm = viewport.getTM()
	fov = viewport.getFOV()
	viewport.activeViewport = target_index
	viewport.setType type
	viewport.setTM tm
	viewport.setFOV fov
	viewport.activeViewport = oldActiveView
	
	
#-------------------------------------------------------------------------------

#visibility track:
animate on

(

at time 0 $foo.visibility = on

at time 35 $foo.visibility = off

at time 57 $foo.visibility = on

)

The controller for this property is stored in the 1st subAnim of the node.
You can access this controller as:

<node>[1].controller -- the visibility controller

------------------------------- other post:
at time 0 (obj1.visibility = 0 )

Afterwards its possible to add keys:

(addNewKey obj1.visibility.controller 30).value = 0


#------------------------------------------------------------------------------

#max ui 

ViewportButtonMgr.EnableButtons=true|false

trackbar.visible=false

