try: import timeit, maya.mel as mel, pymel.core as pm; from tk_slots_maya_init import Init as func
except ImportError as error: print error
try: tk_scrollFieldReporter = pm.melGlobals['tk_scrollFieldReporter']; pm.scrollFieldReporter (tk_scrollFieldReporter, edit=1, clear=1)
except: pass

from pydoc import locate
# from tk_slots_maya_init import Init as func
from tk_slots_ import Slot
import tk_switchboard as sb









class Test001(Slot):
	def __init__(self, *args, **kwargs):
		super(Test001, self).__init__(*args, **kwargs)
		'''
		Start Code
		'''
		if pm.selectType(query=1, vertex=1): #get vertex selection info
			selectedVerts = [v.split('[')[-1].rstrip(']') for v in pm.filterExpand(selectionMask=31)] #pm.polyEvaluate(vertexComponent=1);
			collapsedList = self.collapseList(selectedVerts)
			numVerts = pm.polyEvaluate (selection[0], vertex=1)
			infoDict.update({'Selected '+str(len(selectedVerts))+'/'+str(numVerts)+" Vertices: ":collapsedList}) #selected verts





	def method(self):
		classes = [locate('tk_slots_'+self.hotBox.app+'_'+name+'.'+name.capitalize())(self.hotBox) for name in self.hotBox.uiList]
		for class_ in classes:
			print str(class_), class_




# test=Test001()
# test.method()






# def getBorderEdgeFromFace(faces=None):
# 	'''
# 	args:
# 		faces='string'/unicode or list of faces. ie. 'poly.f[696]' or 'polyShape.f[696]'
# 	returns:
# 		list of border edges.
# 	ie. getBorderEdgeFromFace(['poly.f[696]', 'poly.f[705:708]'])
# 	'''
# 	if not faces: #if no faces passed in as arg, get current face selection
# 		faces = [str(f) for f in pm.filterExpand(selectionMask=34)]

# 	edges = [str(i).replace('Shape.', '.', -1).split('|')[-1] for i in pm.ls(pm.polyListComponentConversion(faces, ff=1, te=1), flatten=1)] #get edges from the faces

# 	borderEdges=[]
# 	for edge in edges:
# 		edgeFaces = [str(i).replace('Shape.', '.', -1).split('|')[-1] for i in pm.ls(pm.polyListComponentConversion(edge, fe=1, tf=1), flatten=1)] #get faces that share the edge.

# 		if len(edgeFaces)<2: #if the edge has only one shared face, it is a border edge.
# 			borderEdges.append(edge)
# 		else:
# 			for f in edgeFaces:
# 				if f not in faces: #else if the edge's shared face is not part of the selected faces, it is a border edge.
# 					borderEdges.append(edge)
# 					break

# 	return borderEdges




# pm.select(getBorderEdgeFromFace())





# def getIntegers(string):
# 	num='' #get trailing integers
# 	for char in reversed(str(string)):
# 		if str.isdigit(char):
# 			num = num+char
# 		else:
# 			return num[::-1] #reverse the string


# find = '*1|*2'#str(self.ui.t000.text()) #asterisk denotes startswith*, *endswith, *contains* 
# to = '1'#str(self.ui.t001.text())

# if pm.ls(selection=1): #if selection; operate on only the selected objects.
# 	lists = [pm.ls(f, sl=1) for f in find.split('|')] #objects in current selection that match criteria
# else:
# 	lists = [pm.ls(f) for f in find.split('|')] # objects = pm.ls(find) #Stores a list of all objects containing 'find'
# objects = set([i for sublist in lists for i in sublist]) #flatten and remove any duplicates.

# for obj in objects:
# 	for f in  [f for f in find.split('|') if f.strip('*') in obj]: #get the objects that contain the chars in find.split('|')
# 		relatives = pm.listRelatives(obj, parent=1) #Get a list of it's direct parent
# 		if 'group*' in relatives: #If that parent starts with group, it came in root level and is pasted in a group, so ungroup it
# 			relatives[0].ungroup()

# 		#find modifiers
# 		if to.startswith('*') and to.endswith('*'): #replace chars
# 			newName = obj.name.replace(f, to)

# 		elif to.startswith('*'): #replace suffix
# 			newName = obj.name+to

# 		elif to.endswith('*'): #replace prefix
# 			newName = obj.name.replace(f, to, 1) #1=replace only the first occurance

# 		elif to.startswith('**'): #replace suffix and move any trailing integers
# 			num = self.getTrailingIntegers(obj.name)
# 			stripped = obj.name.rstrip('0123456789').rstrip(f)
# 			newName = stripped+num+to

# 		else: #replace whole name
# 			newName = to

# 		newName = newName.replace('*', '')
# 		while pm.objExists(newName):
# 			newName = moveIntegers(newName+str(1))
# 		name = pm.rename(obj, newName) #Rename the object with the new name
#		break



# x=1
# y=0
# z=0
# neg=1


# mergeThreshold=0.005
		
# cutMesh = 1 #cut
# instance = 0

# if x and neg: #'-x'
# 	direction = 0 #negative axis
# 	axis = 0 #0=x 1=y, 2=z
# 	x=1; y=1; z=1 #used to negaively scale instanced object
# else: #'x'
# 	direction = 1 #positive axis
# 	axis = 0
# 	x=-1; y=1; z=1
	
# if y and neg: #'-y'
# 	direction = 0
# 	axis = 1
# 	x=1; y=1; z=1
# else: #'y'
# 	direction = 1
# 	axis = 1
# 	x=1; y=-1; z=1
		
# if z and neg: #'-z'
# 	direction = 0
# 	axis = 2
# 	x=1; y=1; z=1
# else: #'z'
# 	direction = 1
# 	axis = 2
# 	x=1; y=1; z=-1


# if not instance:
# 	pm.polyMirrorFace(cutMesh=cutMesh, axis=axis, axisDirection=direction, mergeMode=1, mergeThresholdType=1, mergeThreshold=mergeThreshold, mirrorAxis=1, mirrorPosition=0, smoothingAngle=30, flipUVs=0, ch=0)
# else:
# 	pm.undoInfo(openChunk=1)
# 	if cutMesh:
# 		self.b032()
# 	instance = pm.instance() # bt_convertToMirrorInstanceMesh(0); #x=0, y=1, z=2, -x=3, -y=4, -z=5
# 	pm.scale (z,x,y, pivot=(0,0,0), relative=1) #zxy
# 	pm.undoInfo(closeChunk=1)
























# # pm.hyperShade(shaderNetworksSelectMaterialNodes=1) #selects the material node
# node = pm.ls(selection=1, type='VRayMultiSubTex')[0] #now add the selected node to a variable

# if pm.nodeType(node)=='VRayMultiSubTex':
# 	print node



# uiList = ['animation', 'cameras', 'create', 'display', 'edit', 'init']

# sbDict = {k:{} for k in uiList}

# sbDict={
# 		'polygons':{ 
# 		'class':'Polygons', 
# 		'size':[295, 234], 
# 		'connectionDict':{'b001':{'buttonObject':'b001', 'buttonObjectWithSignal':'b000.clicked', 'methodObject':'main.b001', 'methodName':'Multi-Cut Tool'}}, 
# 		'uiList':['animation', 'cameras', 'create', 'display', 'edit'],
# 		'prevName':['prevNameString', 'prevNameString', 'currentNameString'], 
# 		'prevCommand':[{'b00', 'multi-cut tool'}] }
# }

# def hasKey(*args):
# 	if len(args)==1:
# 		if args[0] in sbDict: return True
# 		else: return False
# 	if len(args)==2:
# 		if args[1] in sbDict[args[0]]: return True
# 		else: return False
# 	if len(args)==3:
# 		if args[2] in sbDict[args[0]][args[1]]: return True
# 		else: return False



# print hasKey('polygons', 'connectionDict', 'b000')


# {'i007': {
# 'buttonObject': <PySide2.QtWidgets.QPushButton object at 0x0000020D6D0EA888>, 
# 'methodObject': <function <lambda> at 0x0000020D6D0E5908>, 
# 'buttonObjectWithSignal': <PySide2.QtCore.SignalInstance object at 0x0000020D6175A3A8>
# }, 

# 'i006': {
# 'buttonObject': <PySide2.QtWidgets.QPushButton object at 0x0000020D6D0EA9C8>, 
# 'methodObject': <function <lambda> at 0x0000020D6D0E5898>, 
# 'buttonObjectWithSignal': <PySide2.QtCore.SignalInstance object at 0x0000020D6175A378>
# }, 







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

