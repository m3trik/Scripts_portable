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
		


	
#~ 130 ID:40212 
#~ Desc:'Viewport Selection Shade Selected Objects Toggle' 
#~ Cat:'Views' 
#~ BtnTxt:'S&hade Selected'
#~ MnuTxt:'S&hade Selected'

def maxUiSetChecked(id, table, item, state=True):
	atbl = rt.actionMan.getActionTable(table)
	if atbl:
		aitm = atbl.getActionItem(item)
		print aitm.isChecked
		if state:
			if not aitm.isChecked:
				rt.actionMan.executeAction(0, id)
				print aitm.isChecked
		else:
			if aitm.isChecked:
				rt.actionMan.executeAction(0, id)
				print aitm.isChecked



sel = [s for s in rt.getCurrentSelection()]
geometry = [g for g in rt.geometry]

for g in geometry:
	if g not in sel:
		g.xray = True


