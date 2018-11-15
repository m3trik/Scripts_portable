try:
	import maya.mel as mel, pymel.core as pm, tk_maya_shared_functions as func, timeit
	import maya.OpenMayaUI as omui
except ImportError as err:
	print err
try:
    tk_scrollFieldReporter = pm.melGlobals['tk_scrollFieldReporter']
    pm.scrollFieldReporter (tk_scrollFieldReporter, edit=1, clear=1)
except:
   pass

''' Start Code '''


# #rotate camera
# import maya.OpenMaya as OpenMaya
# import maya.OpenMayaUI as OpenMayaUI

# view = OpenMayaUI.M3dView.active3dView()
# cam = OpenMaya.MDagPath()
# view.getCamera(cam)
# camPath = cam.fullPathName()

# print pm.camera (camPath, q=1, rotation=1)
# camAngle = pm.camera (camPath, q=1, rotation=1)
# #rotation = [camAngle[0], camAngle[1], camAngle[2]+180] #round to 15 and flip neg neg/pos and vice versa
# rotation = [-82, 8, -179]
# print rotation

# pm.camera (camPath, rotation=rotation)
# component = pm.ls(selection=1)[0]
# print component
# pm.normalConstraint (str(component), 'pPlane1',
# 	# aimVector=[0,1,0],
# 	# upVector=normal,
# 	worldUpVector=[1,0,0],
# 	worldUpType="vector", # "scene","object","objectrotation","vector","none"
# 	weight=10
# 	)

# normal: (0.38268289803626016, 0.0, -0.9238797538373538)
# normal: (0.0, 1.0, 0.0)

# import maya.api.OpenMaya as om

# dest_ = om.MVector (0.38268289803626016, 0.0, -0.9238797538373538)
# obj_  = om.MVector (0.0, 1.0, 0.0)
# print dest_, obj_
# print type(dest_)
# quaternion = om.MQuaternion (dest_, obj_, factor=1.0)
# print type(quaternion)
# # pm.xform ("pPlane1", rotation=quaternion)



# pm.selectType (locatorUV=1)
# pm.selectType (subdivMeshUV=1)
# pm.selectType (surfaceUV=1)


# TypeError: Invalid flag 'centerPivot'
# # line 2287, in b014
# # turn off objects only if in component selection mode
# print [pm.xform (s, centerPivot=1) for s in pm.ls (sl=1, objectsOnly=0, flatten=1)]
# #pm.xform (s, centerPivot=1)

# import os

# path = r"O:\Cloud\____Graphics\Maya\Scripts\_Python\_Python_startup\tk_maya_ui"

# files = [f.replace('tk_','').replace('.ui','') for f in os.listdir(path) if f.endswith('.ui')]


# print files

import os

path = os.path.expandvars(r'%CLOUD%/____Graphics/Maya/Scripts/_Python/_Python_startup/tk_maya_ui')#"%CLOUD%/____Graphics/Maya/Scripts/_Python/_Python_startup/tk_maya_ui"

#to add a new layout, simply add name to uiList, then create a corresponding class in tk_maya(or max)_functions (make sure super is renamed properly if using copy/paste) and make sure corresponding ui buttons are named accordingly.
uiList=[f.replace('tk_','').replace('.ui','') for f in os.listdir(path) if f.endswith('.ui')] #gets uiList but doesnt maintain the order needed to sync with the layout stack index
print uiList

indexDict = {name:'i000'[:-len(str(num))]+str(num) for num,name in enumerate(uiList)}
print indexDict