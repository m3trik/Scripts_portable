import sys, os.path

import MaxPlus




# ------------------------------------------------
# Get the main Max window as a QtGui.QMainWindow instance.
# ------------------------------------------------

# mainWindow = MaxPlus.GetQMaxMainWindow()


# ------------------------------------------------
# MaxPlus.FileManager.Reset(True)





#Append directory to system path -----------------
#paths = r'%CLOUD%/____Graphics/3ds Max/Scripts/__path;%CLOUD%/____Graphics/3ds Max/scripts/__path/tk_slots;%CLOUD%/_Programming/Qt/__path;%CLOUD%/_Programming/Qt/__path/tk_ui'
paths = r'%USERPROFILE%/Documents/_portable/Scripts_portable/__path;%USERPROFILE%/Documents/_portable/Scripts_portable/__path/tk_ui;%USERPROFILE%/Documents/_portable/Scripts_portable/__path/max;%USERPROFILE%/Documents/_portable/Scripts_portable/__path/max/tk_slots'
for path in paths.split(';'):
	sys.path.append(os.path.expandvars(path))


#load tk_main ------------------------------------
import tk_main

# if 'tk_main' not in sys.modules:
# 	import tk_main #tk_maya_main.py -qt hotbox menus and controls
# else:
# 	print "reload: tk_main"
# 	reload(tk_main)



#------------------------------------------------------------------------------