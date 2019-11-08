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
		classes = [locate('tk_slots_'+self.tk.app+'_'+name+'.'+name.capitalize())(self.tk) for name in self.tk.uiList]
		for class_ in classes:
			print str(class_), class_




test=Test001()
# test.method()


# obj = 'pPyramid1'
# vtx = pm.ls(obj+'.vtx[*]', flatten=True)

# print vtx

# # slice tool

# duplicate
# move
# loft w/ output polygon
# boolean




# def getObject(class_, objectNames, showError_=True, print_=False):
# 	#args: 	class_=class object
# 	#			 	objectNames='string' - names separated by ','. ie. 's000,b004-7'. b004-7 specifies buttons b004-b007.  
# 	#		 	 	showError_=bool - show attribute error if item doesnt exist
# 	#				print_=bool - print unpacked objectNames to console.
# 	#returns: list of corresponding objects
# 	#ex. getObject(self.tk.ui, 's000,b002,cmb011-15') #get objects for s000,b002, and cmb011-cmb015

# 	unpacked_names=[]
# 	for name in [n.strip() for n in objectNames.split(',') if '-' in n]: #build list of all objectNames containing '-'
# 		name=name.split('-') #ex. split 'b000-8'

# 		prefix = name[0].strip('0123456789') #ex. split 'b' from 'b000'
# 		start = int(name[0].strip('abcdefghijklmnopqrstuvwxyz') or 0) #start range. #ex. '000' #converting int('000') returns None, if case; assign 0.
# 		stop = int(name[1])+1 #end range. #ex. '9' from 'b000-8' for range up to 9 but not including 9.

# 		unpacked_names.extend([str(prefix)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)]) #build list of name strings within given range

# 	names = [n.strip() for n in objectNames.split(',') if '-' not in n]

# 	if print_: print names+unpacked_names
# 	# objects=[] #corresponding objects
# 	# for name in names+unpacked_names:
# 	# 	try:
# 	# 		objects.append(getattr(class_, name)) #equivilent to:(self.tk.ui.m000)
# 	# 	except: 
# 	# 		if showError_:
# 	# 			print "# Error:"+str(class_)+" has no attribute "+str(name)+" #"
# 	# 		else: pass
# 	# return objects

# def getObject(class_, objectNames, showError_=True, print_=False):
# 	#args:	class_=class object
# 	#				objectNames='string' - names separated by ','. ie. 's000,b004-7'. b004-7 specifies buttons b004-b007.  
# 	#				showError=bool - show attribute error if item doesnt exist
# 	#				print_=bool - print unpacked objectNames to console.
# 	#returns: list of corresponding objects
# 	#ex. getObject(self.tk.ui, 's000,b002,cmb011-15') #get objects for s000,b002, and cmb011-cmb015
# 	packed_names = [n.strip() for n in objectNames.split(',') if '-' in n] #build list of all objectNames passed in containing '-'

# 	unpacked_names=[]
# 	for name in packed_names:
# 		name=name.split('-') #ex. split 'b000-8'
# 		prefix = name[0].strip('0123456789') #ex. split 'b' from 'b000'
# 		start = int(name[0].strip('abcdefghijklmnopqrstuvwxyz') or 0) #start range. #ex. '000' #converting int('000') returns None, if case; assign 0.
# 		stop = int(name[1])+1 #end range. #ex. '9' from 'b000-8' for range up to 9 but not including 9.
# 		unpacked_names.extend([str(prefix)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)]) #build list of name strings within given range

# 	names = [n.strip() for n in objectNames.split(',') if '-' not in n] #all objectNames passed in not containing '-'
# 	if print_: print names+unpacked_names



# # print getObject('c', 's100-121, s002-3, s022-23', print_=True)
# print getObject('self.tk.ui', 'i003-25', print_=True)








	# #returns a list of objects from a supplied range, or string list.
	# @staticmethod
	# def getObject(class_, objectNames, range_=None, showError_=True):
	# 	#args: class_=class object
	# 	#			 objectNames='string' - single name when used with range arg. ie. 's'  else; names separated by ','. ie. ['s000,s001,s002'] 
	# 	#			 range_=[int list] - integers representing start, end of range. used with single string type objectName.  ie. [2,10]
	# 	#		 	 showError=bool - show attribute error if item doesnt exist
	# 	#returns: list of corresponding objects
	# 	#ex. getObject(self.tk.ui, 's', [0,10])  or  getObject(self.tk.ui, ['s000,s002,s011'])
	# 	if range_: #if range is given; generate list within given range_
	# 		start, stop = range_[0], range_[1] #add a numberical suffix to the object name within the given range.
	# 		names = [str(objectNames)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)] #build list of name strings within given range
	# 	else: #use the list of names passed in as objectName
	# 		names = objectNames.split(',')
	# 	objects=[]
	# 	for name in names:
	# 		# if hasattr(class_, name):
	# 		try:
	# 			objects.append(getattr(class_, name)) #equivilent to:(self.tk.ui.m000)
	# 		# elif showError_:
	# 		except: 
	# 			if showError_:
	# 				print "# Error:"+str(class_)+" has no attribute "+str(name)+" #"
	# 			else: pass
	# 	return objects


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

# import os

# path = os.path.expandvars(r'%CLOUD%/____Graphics/Maya/Scripts/_Python/_Python_startup/tk_maya_ui')#"%CLOUD%/____Graphics/Maya/Scripts/_Python/_Python_startup/tk_maya_ui"

# #to add a new layout, simply add name to uiList, then create a corresponding class in tk_maya(or max)_functions (make sure super is renamed properly if using copy/paste) and make sure corresponding ui buttons are named accordingly.
# uiList=[f.replace('tk_','').replace('.ui','') for f in os.listdir(path) if f.endswith('.ui')] #gets uiList but doesnt maintain the order needed to sync with the layout stack index
# print uiList

# indexDict = {name:'i000'[:-len(str(num))]+str(num) for num,name in enumerate(uiList)}
# print indexDict