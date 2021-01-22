from __future__ import print_function
import os, sys

import pymel.core as pm
import maya.mel as mel

#get maya version
from pymel import versions
version = versions.current()



#maya python path----------------------------------------------------
#get %MAYA_SCRIPT_PATH% directories
MAYA_SCRIPT_PATH = os.environ['MAYA_SCRIPT_PATH'].split(';')
dir_ = next((s for s in MAYA_SCRIPT_PATH if s.endswith('/apps/maya')), None)

if dir_:
	dir_root = dir_.replace('/apps/maya', '')
else: #if path not found, print error and current paths set in maya.env
	module_name = os.path.splitext(os.path.basename(__file__))[0]
	print('Error: {}: dir not found in MAYA_SCRIPT_PATH.'.format(module_name)) #print error and module name.
	print('MAYA_SCRIPT_PATH: {}'.format(MAYA_SCRIPT_PATH))


ui_dir = dir_root+"/ui"
scripts_dir	= dir_root+"/apps/maya"
slots_dir = scripts_dir+"/slots"


#append to system path:
paths = [dir_root, ui_dir, scripts_dir, slots_dir]

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


#MASH tools
import MASH_tools


# ------------------------------------------------
# Get the main Maya window as a QtGui.QMainWindow instance.
# ------------------------------------------------

# import maya.OpenMayaUI as omui
# Main_Window_ptr = omui.MQtUtil.mainWindow()
# if Main_Window_ptr is not None:
# 	mainWindow = wrapInstance (long(Main_Window_ptr), QtWidgets.QWidget)

# ------------------------------------------------






#---------------------------------------------------------------------
