try: import timeit, maya.mel as mel, pymel.core as pm; from tk_slots_maya_init import Init as func
except ImportError as error: print error
try: tk_scrollFieldReporter = pm.melGlobals['tk_scrollFieldReporter']; pm.scrollFieldReporter (tk_scrollFieldReporter, edit=1, clear=1)
except: pass

''' Start Code '''

objectName = 'pCube1'
name = objectName+"_dup"

pm.instance (objectName, name=name)
pm.duplicate (objectName, returnRootsOnly=1, name=name)







# #straighten circle
# import math

# degree = 360/float(numPoints)
# radian = math.radians(degree) #or math.pi*degree/180 (pi * degrees / 180)

# vertexPoints = []

# for _ in range(numPoints):
# 	# print "deg:", degree,"\n", "cos:",math.cos(radian),"\n", "sin:",math.sin(radian),"\n", "rad:",radian
# 	if axis =="x":
# 		x = center[2] + (math.cos(radian) *radius)
# 		y = center[1] + (math.sin(radian) *radius)
# 		vertexPoints.append([0,x,y])
# 	if axis =="y":
# 		x = center[2] + (math.cos(radian) *radius)
# 		y = center[0] + (math.sin(radian) *radius)
# 		vertexPoints.append([y,0,x])
# 	else: # z axis
# 		x = center[0] + (math.cos(radian) *radius)
# 		y = center[1] + (math.sin(radian) *radius)
# 		# vertexPoints.append([x,y,0]) #not working.
# 		vertexPoints.append([0,x,y]) #create on x axis and rotate below
# 	radian = radian+math.radians(degree) #increment by original radian value that was converted from degrees
# 	#print x,y,"\n"




# vertices = pm.ls (selection=True, flatten=True)

# print vertices

# for vertex in vertices:
# 	point = pm.xform(vertex, query=True, translation=True, objectSpace=True)
# 	x = round (point[0], 2)
# 	y = round (point[1], 2)
# 	z = round (point[2], 2)
# 	print x,y,z


# import tk_main
# if 'tk_hotBox_init' not in locals() or 'tk_hotBox_init' not in globals():
# 	tk_hotBox_init = tk_main.createInstance()
# # tk_hotBox_init.hbShow()
# tk_hotBox_init.hbHide()


# lambda: self.overlay.setVisible(False) if self.overlay.isVisible() else self.overlay.setVisible(True)

# def convertMelToPy(melScript): #convert mel to python
# 	from pymel.tools import mel2py
# 	# convert to single line
# 	translation = [mel2py.mel2pyStr(e+';') for e in melScript.split(';')]
# 	pythonScript = [s.lstrip('from pymel.all import *') for s in translation]
# 	print " ".join(pythonScript)
# 	return pythonScript
# 	#print to outputscrollField
# 	# outputscrollField (python_script, "mel2py", 1.0, 1.0) #text, window_title, width, height

# # string = 'global string $tk_matID [];'

