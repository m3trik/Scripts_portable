import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt



#~ -----------------------------------------------
#~ copy. if not valid object uncheck.
#~ lock xyz

#~ get translate

#~ ,move

#~ ,scale

#-------------------------------------------------

#~ sel = [s for s in rt.getCurrentSelection()]

#~ for obj in sel:
	#~ if obj.isFrozen == True:
		#~ obj.isFrozen = False
	#~ else:
		#~ obj.isFrozen = True
	
#~ for obj in sel:
	#~ if not obj.isHiddenInVpt:
		#~ obj.isHidden = True
		

viewport = rt.viewport.activeViewport
#~ print rt.viewport.isWire()
#~ if rt.viewport.isWire():
	#~ rt.actionMan.executeAction 0 "40212"
	#~ rt.actionMan.getmxsprop('Views.ShadeSelected', '40212')
	#~ actionMan.executeAction 0 "40212"
	
#~ 130 ID:40212 
#~ Desc:'Viewport Selection Shade Selected Objects Toggle' 
#~ Cat:'Views' 
#~ BtnTxt:'S&hade Selected' 
#~ MnuTxt:'S&hade Selected'
	
atbl = rt.actionMan.getActionTable(62)
print atbl
if atbl:
	aitm = atbl.getActionItem(130)
	print aitm.isChecked
	  
	