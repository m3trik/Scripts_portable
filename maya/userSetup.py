import os, sys
import pymel.core as pm
import maya.mel as mel

#get maya version
from pymel import versions
version = versions.current()




#maya python path----------------------------------------------------
#get %MAYA_SCRIPT_PATH% directories
dir_ = [s for s in os.environ['MAYA_SCRIPT_PATH'].split(';') if '__portable/_scripts/' in s][0]
dir_ = dir_.rstrip('/maya')

#if path not found, print error and current paths set in maya.env
if not dir_:
	print "# Error: in userSetup.py. dir not found in MAYA_SCRIPT_PATH #"
	print "# MAYA_SCRIPT_PATH:"+ str([s for s in os.environ['MAYA_SCRIPT_PATH'].split(';')]) +" #"

#append to system path:
paths = [
	dir_,
	dir_+"/ui",
	dir_+"/maya",
	dir_+"/maya/slots"
	]

for path in paths:
	sys.path.append(path)



#script editor in/output---------------------------------------------
import commandPort #commandPort.py -opens ports 7001/7002 for external script editor


mel.eval ('source "scriptEditorOutput.mel";')
mel.eval ('evalDeferred -lowPriority ("tk_initScriptEditorOutputWin");')


if 'scriptEditorOutputTextHighlighting' not in sys.modules:
	import scriptEditorOutputTextHighlighting #syntax highlighting for script editor output window
else:
	print "reload: scriptEditorOutputTextHighlighting"
	reload(scriptEditorOutputTextHighlighting)

pm.evalDeferred ("scriptEditorOutputTextHighlighting.wrap()", lowestPriority=1)



#--------------------------------------------------------------------

#Set the initial state of the tool settings.
pm.workspaceControl ("ToolSettings", edit=1, minimumWidth=False)
#Set the initial state of the attribute editor.
pm.workspaceControl ("AttributeEditor", edit=1, minimumWidth=False)




# ------------------------------------------------
#tk_main------------------------------------------
# if 'tk_main' not in sys.modules:
# 	import tk_main #tk_maya_main.py -qt hotbox menus and controls
# else:
# 	print "reload: tk_main"
# 	reload(tk_main)


# ------------------------------------------------
# Get the main Maya window as a QtGui.QMainWindow instance.
# ------------------------------------------------

#not currently used
# import maya.OpenMayaUI as omui
# Main_Window_ptr = omui.MQtUtil.mainWindow()
# if Main_Window_ptr is not None:
# 	mainWindow = wrapInstance (long(Main_Window_ptr), QtWidgets.QWidget)

# ------------------------------------------------






#---------------------------------------------------------------------
