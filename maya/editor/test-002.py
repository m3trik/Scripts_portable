try: import timeit, maya.mel as mel, pymel.core as pm; from tk_slots_maya_init import Init as func
except ImportError as error: print error
try: tk_scrollFieldReporter = pm.melGlobals['tk_scrollFieldReporter']; pm.scrollFieldReporter (tk_scrollFieldReporter, edit=1, clear=1)
except: pass

''' Start Code '''


uiList = ['animation', 'cameras', 'create', 'display', 'edit', 'init']

sbDict = {k:{} for k in uiList}

sbDict={
		'polygons':{ 
		'class':'Polygons', 
		'size':[295, 234], 
		'connectionDict':{'b001':{'buttonObject':'b001', 'buttonObjectWithSignal':'b000.clicked', 'methodObject':'main.b001', 'methodName':'Multi-Cut Tool'}}, 
		'uiList':['animation', 'cameras', 'create', 'display', 'edit'],
		'prevName':['prevNameString', 'prevNameString', 'currentNameString'], 
		'prevCommand':[{'b00', 'multi-cut tool'}] }
}

def hasKey(*args):
	if len(args)==1:
		if args[0] in sbDict: return True
		else: return False
	if len(args)==2:
		if args[1] in sbDict[args[0]]: return True
		else: return False
	if len(args)==3:
		if args[2] in sbDict[args[0]][args[1]]: return True
		else: return False



print hasKey('polygons', 'connectionDict', 'b000')


{'i007': {
'buttonObject': <PySide2.QtWidgets.QPushButton object at 0x0000020D6D0EA888>, 
'methodObject': <function <lambda> at 0x0000020D6D0E5908>, 
'buttonObjectWithSignal': <PySide2.QtCore.SignalInstance object at 0x0000020D6175A3A8>
}, 

'i006': {
'buttonObject': <PySide2.QtWidgets.QPushButton object at 0x0000020D6D0EA9C8>, 
'methodObject': <function <lambda> at 0x0000020D6D0E5898>, 
'buttonObjectWithSignal': <PySide2.QtCore.SignalInstance object at 0x0000020D6175A378>
}, 







# # cmb.itemText(index)
# prevCommand = [{'b000':'multi-cut tool'}, {'b001':'some other tool'}, {'b002':'yet another tool'}]

# # print [prevCommand[0] for c in prevCommand]

# print [dict_.values() for dict_ in prevCommand]


# for key in prevCommand[0]:
# 	print key




# angleLow = 85
# angleHigh = 95
# creaseAmount = 10

# mel.eval("PolySelectConvert 2;") #convert selection to edges
# contraint = pm.polySelectConstraint( m=3, t=0x8000, a=True, ab=(angleLow, angleHigh) ) # to get edges with angle between 45-89

# pm.polyCrease (value=creaseAmount, createHistory=True, operation=0) #PolyCreaseTool;

# pm.polySelectConstraint( angle=False ) # turn off angle constraint



# import os


# # path = os.path.join(os.path.dirname(__file__), 'maya/tk_slots_maya') #get absolute path from dir of this module + relative path to directory
# path = 'O:/Cloud/__portable/_scripts/maya/tk_slots_maya'


# # #create a list of the names of the files in the ui folder, removing the extension.
# # print [file_.replace('.ui','') for file_ in os.listdir(path) if file_.endswith('.ui')] #gets uiList from directory contents

# file = path+'/'+'tk_slots_maya_'+str('polygons')+'.py'

# with open(file) as f:
# 	for line in f.readlines():
# 		if 'def b' in line and '#' in line:
# 			methodString = line.split('#')[0].strip().strip('def ').strip('(self):')
# 			commentString = line.split('#')[1]







# objectName = 'pCube1'
# name = objectName+"_dup"

# pm.instance (objectName, name=name)
# pm.duplicate (objectName, returnRootsOnly=1, name=name)







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

