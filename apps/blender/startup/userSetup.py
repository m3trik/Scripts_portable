import os, sys

import bpy



#blender python path----------------------------------------------------
#get %MAYA_SCRIPT_PATH% directories
MAYA_SCRIPT_PATH = os.environ['MAYA_SCRIPT_PATH'].split(';')
dir_ = next((s for s in MAYA_SCRIPT_PATH if '__portable/_scripts/' in s), None)

if dir_:
	dir_root = dir_.replace('/apps/maya', '')
else: #if path not found, print error and current paths set in maya.env
	module_name = os.path.splitext(os.path.basename(__file__))[0]
	print('Error: {}: dir not found in MAYA_SCRIPT_PATH.'.format(module_name)) #print error and module name.
	print('MAYA_SCRIPT_PATH: {}'.format(MAYA_SCRIPT_PATH))

ui_dir = dir_root+"/ui"
scripts_dir	= dir_root+"/apps/blender"
slots_dir = scripts_dir+"/slots"
startup_dir = scripts_dir+"/startup"

#append to system path:
paths = [dir_root, ui_dir, scripts_dir, slots_dir, startup_dir]

for path in paths:
	sys.path.append(path)



#macros--------------------------------------------------------------
from macros import Macros
Macros().setMacros()






#--------------------------------------------------------------------





#--------------------------------------------------------------------
# Notes:
#--------------------------------------------------------------------

