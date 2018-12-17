import os, sys
import pymel.core as pm
import maya.mel as mel

#get maya version
from pymel import versions
version = versions.current()





#maya python path----------------------------------------------------
#Append directory to system path
paths = [
'%CLOUD%/____Graphics/__general/_portable/_scripts/__path',
'%CLOUD%/____Graphics/__general/_portable/_scripts/__path/tk_ui',
'%CLOUD%/____Graphics/__general/_portable/_scripts/__path/maya',
'%CLOUD%/____Graphics/__general/_portable/_scripts/__path/maya/tk_slots_maya',

'%USERPROFILE%/Documents/_portable/__scripts/__path',
'%USERPROFILE%/Documents/_portable/__scripts/__path/tk_ui',
'%USERPROFILE%/Documents/_portable/__scripts/__path/maya',
'%USERPROFILE%/Documents/_portable/__scripts/__path/maya/tk_slots_maya'
]

for path in paths.split(';'):
	try: sys.path.append(os.path.expandvars(path))
	except: pass




#script editor in/output---------------------------------------------
import commandPort #commandPort.py -opens ports 7001/7002 for external script editor


mel.eval ('source "tk_scriptEditorOutput.mel";')
mel.eval ('evalDeferred -lowPriority ("tk_initScriptEditorOutputWin");')


if 'scriptEditorOutputTextHighlighting' not in sys.modules:
	import scriptEditorOutputTextHighlighting #syntax highlighting for script editor output window
else:
	print "reload: scriptEditorOutputTextHighlighting"
	reload(scriptEditorOutputTextHighlighting)

pm.evalDeferred ("scriptEditorOutputTextHighlighting.wrap()", lowestPriority=1)



#tk_main-------------------------------------------------------------
import tk_main
# if 'tk_main' not in sys.modules:
# 	import tk_main #tk_maya_main.py -qt hotbox menus and controls
# else:
# 	print "reload: tk_main"
# 	reload(tk_main)


#---------------------------------------------------------------------


# ------------------------------------------------
# Get the main Maya window as a QtGui.QMainWindow instance.
# ------------------------------------------------

#not currently used
# import maya.OpenMayaUI as omui
# Main_Window_ptr = omui.MQtUtil.mainWindow()
# if Main_Window_ptr is not None:
# 	mainWindow = wrapInstance (long(Main_Window_ptr), QtWidgets.QWidget)

# ------------------------------------------------


# ------------------------------------------------



#---------------------------------------------------------------------
