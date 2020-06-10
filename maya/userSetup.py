from __future__ import print_function
import os, sys

import pymel.core as pm
import maya.mel as mel

#get maya version
from pymel import versions
version = versions.current()



#maya python path----------------------------------------------------
#get %MAYA_SCRIPT_PATH% directories
dir_ = next((s for s in os.environ['MAYA_SCRIPT_PATH'].split(';') if '__portable/_scripts/' in s), None)

if dir_:
	dir_ = dir_.rstrip('/maya')
else: #if path not found, print error and current paths set in maya.env
	print('Error: dir not found in MAYA_SCRIPT_PATH. '+os.path.splitext(os.path.basename(__file__))[0]) #print error and module name.
	print('MAYA_SCRIPT_PATH: '+ str([s for s in os.environ['MAYA_SCRIPT_PATH'].split(';')]))

#append to system path:
paths = [
	dir_,
	dir_+'/ui',
	dir_+'/maya',
	dir_+'/maya/slots',
	]

for path in paths:
	sys.path.append(path)



#macros--------------------------------------------------------------
from macros import Macros
Macros().setMacros()



#script editor in/output---------------------------------------------
import commandPort #opens ports 7001/7002 for external script editor
import scriptEditorOutputTextHighlighting #syntax highlighting

mel.eval('source "scriptEditorOutput.mel";')
mel.eval('evalDeferred -lowPriority ("initScriptEditorOutputWin");')

pm.evalDeferred("scriptEditorOutputTextHighlighting.wrap()", lowestPriority=1)



#--------------------------------------------------------------------

#Set the initial state of the tool settings.
pm.workspaceControl("ToolSettings", edit=1, minimumWidth=False)
#Set the initial state of the attribute editor.
pm.workspaceControl("AttributeEditor", edit=1, minimumWidth=False)



#--------------------------------------------------------------------

#GoZ
mel.eval("source \"C:/Users/Public/Pixologic/GoZApps/Maya/GoZScript.mel\"");





# ------------------------------------------------
# Get the main Maya window as a QtGui.QMainWindow instance.
# ------------------------------------------------

# import maya.OpenMayaUI as omui
# Main_Window_ptr = omui.MQtUtil.mainWindow()
# if Main_Window_ptr is not None:
# 	mainWindow = wrapInstance (long(Main_Window_ptr), QtWidgets.QWidget)

# ------------------------------------------------






#---------------------------------------------------------------------
