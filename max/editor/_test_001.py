try: from pymxs import runtime as rt; import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript;from tk_switchboard import Switchboard; sb = Switchboard();from tk_slots_max_init import Init as func;
except: pass



def getTrailingIntegers(string, increment=0):
	'''
	args: increment=int - optional step amount

	Returns 'string' - any integers from the end of the given string.
	'''
	num='' #get trailing integers
	for char in reversed(str(string)):
		if str.isdigit(char):
			num = num+char
		else: #when a non-integer char is found return any integers as a string.
			num = int(num[::-1])+increment #re-reverse the string and increment.
			return '000'[:-len(str(num))]+str(num) #prefix '000' removing zeros according to num length ie. 009 becomes 010


find = '*Box*|Box*'
to = 'Box001'

for o in rt.objects:
	for f in find.split('|'):
		if rt.matchPattern(o.name, pattern=f, ignoreCase=0):
			print o
			break


lists = [[o for o in rt.objects if rt.matchPattern(o.name, pattern=f, ignoreCase=0)] for f in find.split('|')]
objects = set([i for sublist in lists for i in sublist])

# print objects

newName = to.replace('*', '')


while [o for o in rt.objects if o.name==newName]:
	num = getTrailingIntegers(newName, increment=1)
	newName = newName.rstrip('0123456789')+num



for obj in objects:
	print newName
	obj.name = newName #Rename the object with the new name

#~ creaseAmount = 1



#~ obj = rt.selection[0]

#~ obj.EditablePoly.makeHardEdges(1) #1=flag bit 1 : 'is selected'
#~ obj.EditablePoly.setEdgeData(1, creaseAmount)

# def bitArrayIndex(bitArray):
# 	return [i for i, bit in enumerate(bitArray) if bit==1]


# creaseAmount = 5*0.1

# for obj in rt.selection:
# 	obj.EditablePoly.setEdgeData(1, creaseAmount)
	
# 	edges = bitArrayIndex(rt.polyop.getEdgeSelection(obj))
# 	print edges
# 	for edge in edges:
# 		print edge
# 		edgeVerts = rt.polyop.getEdgeVerts(obj, edge)
# 		normal = rt.averageSelVertNormal(obj)
# 		for vertex in edgeVerts:
# 			rt.setNormal(obj, vertex, normal)

#~ print bitIndex([0,0,1,1])




#~ for obj in rt.selection:
	#~ vertices = [i.index for i in obj.selectedVerts]

	#~ target = rt.polyOp.getVert(obj, vertices[-1])
	#~ for v in vertices[1:]:
		#~ rt.polyop.weldVerts (obj, vertices[0], v, target)



# print func.tk('classInfo')



# @staticmethod
# def toggleSmoothPreview():
# 	toggle = func.cycle([0,1], 'toggleSmoothPreview') #toggle 0/1

# 	geometry = rt.selection #if there is a selection; perform operation on those object/s
# 	if not len(geometry): #else: perform operation on all scene geometry.
# 		geometry = rt.geometry



# 	for obj in geometry:
# 		if toggle==0: #preview off
# 			level = tkDict['previousSmoothPreviewLevel']
# 			func.setSubObjectLevel(level) #restore previous subObjectLevel
# 			obj.modifiers['TurboSmooth'].iterations = 0 #set subdivision levels to 0.
# 			func.displayWireframeOnMesh(True)

# 		else: #preview on
# 			tkDict['previousSmoothPreviewLevel'] = rt.subObjectLevel #store previous subObjectLevel
# 			func.setSubObjectLevel(0)
# 			renderIters = obj.modifiers['TurboSmooth'].renderIterations #get renderIter value.
# 			obj.modifiers['TurboSmooth'].iterations = renderIters #apply to iterations value.
# 			func.displayWireframeOnMesh(False)

# toggleSmoothPreview()
