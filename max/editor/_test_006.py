try: from pymxs import runtime as rt; import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript;from tk_switchboard import Switchboard; sb = Switchboard();from tk_slots_max_init import Init as func;
except: pass



# def flattenComponentNames(list_):
# 	for l in list_:
# 		print type(l)


def getClosestVert(vertices0, vertices1):
	dict_={}
	for vertex0 in vertices0:
		v0 = rt.polyOp.getVert(obj, vertex0)
		for vertex1 in vertices1:
			v1 = rt.polyOp.getVert(obj, vertex1)
			distance = rt.distance(v0, v1)
			
			dict_[distance] = [vertex0, vertex1]

	s = sorted(dict_)
	length = len([item for sublist in vertices for item in sublist])
	list_ = [dict_[s[i]] for i, _ in enumerate(s) if i<length/2] #instead of 4; length of vertices/2 for edge compatibility
	return list({item for sublist in list_ for item in sublist})



sel = rt.selection
#919, 931
#188, 132

for obj in sel:

	faces = [f.index for f in obj.selectedFaces]
	# print faceNums
	vertices = [rt.polyop.getFaceVerts(obj, face) for face in faces]
	print vertices
	
	list_ = getClosestVert(vertices[0], vertices[1])


	edges = rt.polyop.getEdgesUsingVert(obj, list_)
	# edges = [rt.polyop.getEdgesUsingVert(obj, vert) for vert in list_]
	print edges

	# flattenComponentNames(edges)

	edges = [item for sublist in edges for item in sublist]
	# # edges = rt.polyop.getEdgesUsingVert(obj, list_)
	print edges
	vertices = [rt.polyop.getEdgeVerts(obj, edge) for edge in edges]
	# vertices = rt.polyop.getVertsUsingEdge(obj, edges)
	print vertices

	list_ = getClosestVert(vertices)

	rt.polyop.setEdgeSelection(obj, edges)







# edgeCount = rt.polyOp.getNumEdges(sel)

# for edge to edgeCount do
# 	faces = rt.polyOp.getEdgeFaces(obj)
# 	if len(faces)==2:
# 		angle = acos(dot (polyOp.getFaceNormal obj faces[1]) (polyOp.getFaceNormal obj faces[2])) 
# 		if angle >= tolerance do selEdges[e] = true
# 	else 
# 		if includeOpenEdges do selEdges[e] = true

# 	polyOp.setEdgeSelection obj selEdges 
# 	# Edit_Poly: (modPanel.getCurrentObject()).SetSelection #Edge &selEdges
# rt.redrawViews()






#~ # attach objects

#~ #copy selection into a proper array
#~ objs = #()
#~ for o in selection do
	#~ append objs o

#~ #grab first object from array and store
#~ fobj = objs[1]

#~ #pop  first object out of array
#~ deleteitem objs 1
#~ converttopoly fobj

#~ #attach to fobj
#~ for o in objs do
	#~ polyop.attach fobj o















#~ sel = rt.selection[0]

#~ mod = MaxPlus.ClassIds.TurboSmooth
#~ mod = MaxPlus.Class_ID(0x0d727b3e, 0x491d29a7)
#~ print mod

#~ rt.modPanel.addModToSelection(mod)

#~ print sel.modifiers[-1].classID
#~ MaxPlus.Factory.CreateWorldSpaceModifier(MaxPlus.Class_ID(1252338403L, 902438110L))

#~ print MaxPlus.ClassIds.TurboSmooth


#~ MaxPlus.Factory.CreateWorldSpaceModifier(MaxPlus.ClassIds.TurboSmooth) #MaxPlus.Class_ID(0x0d727b3e, 0x491d29a7))

#~ sel.modifiers['TurboSmooth'].renderIterations = 0
#~ print sel.modifiers[-1].renderIterations

#~ modpanel.addmodtoselection myBend 	--adds the bend modifier to the top op the stack
#~ addmodifier $Box017 myBend	 --this will also work

 
 #~ deleteModifier obj index










#~ sbDict = {'selection': {}, 'app': u'max', 'scene': {}, 'rendering': {}, 'nurbs': {}, 
#~ 'polygons':{ 
		#~ 'class':'<Polygons>', 
		#~ 'size':[295, 234], 
		#~ 'connectionDict':{'b001':{'buttonObject':'<b001>', 'buttonObjectWithSignal':'<b001.connect>', 'methodObject':'<main.b001>', 'docString':'Multi-Cut Tool'}},
		#~ }, 'preferences': {}, 'rigging': {}, 'create': {}, 'transform': {}, 'init': {}, 'animation': {}, 'main': {}, 
		#~ 'name' : ['main', 'viewport', 'main', 'viewport', 'init', 'viewport', 'init', 'main', 'main', 'viewport', 'main', 'viewport'],
		#~ 'uiList': [['animation', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FFBA348>'], ['create', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FFBA548>'], ['display', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FFBAC08>'], ['edit', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA490C8>'], ['fx', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4A188>'], ['i020', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4A3C8>'], ['i021', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4A4C8>'], ['init', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4A5C8>'], ['lighting', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4A688>'], ['main', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4A788>'], ['normals', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4C708>'], ['nurbs', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4CD08>'], ['polygons', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4ED48>'], ['preferences', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4F048>'], ['rendering', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4F3C8>'], ['rigging', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4F7C8>'], ['scene', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA4FA08>'], ['scripting', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA501C8>'], ['selection', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA50688>'], ['subdivision', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA511C8>'], ['texturing', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA51988>'], ['transform', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA51DC8>'], ['utilities', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA54AC8>'], ['uv', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA54D08>'], ['viewport', '<PySide2.QtWidgets.QMainWindow object at 0x0000029D6FA53648>']], 
		#~ 'fx': {}, 'hotbox': {'class': '<tk_main.HotBox object at 0x0000029D69702748>'}, 'i021': {}, 'i020': {}, 'utilities': {}, 'lighting': {}, 'viewport': {}, 'subdivision': {}, 'edit': {}, 'signal': {'class': '<class tk_signals.Signal>'}, 'uv': {}, 'texturing': {}, 'normals': {}, 'display': {}, 'scripting': {} }



#~ # print  [sbDict['polygons']['connectionDict'][buttonName]['buttonObjectWithSignal'] for buttonName in sbDict['polygons']['connectionDict']]


#~ # TypeError: 'PySide2.QtCore.QObject.disconnect' called with wrong argument types:
#~ #   PySide2.QtCore.QObject.disconnect(PySide2.QtWidgets.QPushButton, str, list)





#~ def previousName(previousIndex=False, allowDuplicates=False, as_list=False):
		#~ '''
		#~ #args:
			#~ previousIndex=bool 	return the index of the last valid previously opened ui name.
		#~ #returns:
			#~ if previousIndex: int index of previously opened ui
			#~ else: string name of previously opened layout.
		#~ '''
		#~ sbDict['name'] = sbDict['name'][-8:] #keep original list length to last 8 elements

		#~ list_ = [i for i in sbDict['name'] if 'init' not in i] #work on a copy of the list, removing any instances of 'init', keeping the original intact
		
		#~ # for l in list_:
		#~ # 		print l

		#~ [list_.remove(l) for l in list_[:] if list_.count(l)>1] #remove any previous instances if they exist
		
			

		#~ # # # if not allowDuplicates:
		#~ # for l in list_[:]:
		#~ # 		print l
		#~ # 		if list_.count(l)>1: #remove any previous instances if they exist
		#~ # 			list_.remove(l)

		#~ if previousIndex:
			#~ validPrevious = [i for i in list_ if all(['viewport' not in i, 'main' not in i])]
			#~ return self.getUiIndex(validPrevious[-2])

		#~ if as_list:
			#~ return list_

		#~ else:
			#~ try: return list_[-2]
			#~ except: return ''

#~ # print sbDict['name']
#~ print previousName(as_list=1)
# print previousName(as_list=1, allowDuplicates=1)
# print previousName(allowDuplicates=1)

# for l in list_: #remove any previous instances if they exist
# 	if l=='init':
# 		list_.remove(l)
# 	if list_.count(l)>1:
# 		list_.remove(l)

# print list_


# print [list_.pop(list_.index(l)) for l in list_ if list_.count(l)>1]

# print [list_.pop(i) for v, v in enumerate(list_) if list_.count(l)>1]


# sbDict = {'uiList':[['animation', '<animation dynamic ui object>'], ['cameras', '<cameras dynamic ui object>'], ['create', '<create dynamic ui object>'], ['display', '<display dynamic ui object>']]}

# name = [i[0] for i in sbDict['uiList']]
# ui = [i[1] for i in sbDict['uiList']]


# index = name.index('create')
# print ui[index]

# list_= ['init','main','init']

# # for l in list_:
# # 	if 6 in l:
# # 		list_.remove(l)


# print [list_[:].remove(l) for l in list_ if list_.count(l)>1]
# print list_

# print list_

# for obj in rt.selection:
# 	rt.toolMode.coordsys(obj)

#~ verts = rt.polyop.getVertSelection(obj)

#~ rt.polyop.breakVerts (obj, verts)
#~ print 'breakVerts: ' verts


# if sel.count:
# 	for i in sel:
# 		i.pivot = i.center
		
#rt.polyop.cutvert()


#~ sel = rt.Modpanel.getcurrentObject()

#~ if rt.Ribbon_Modeling.IsEditablePoly():
	#~ if rt.subobjectlevel == 1:
		#~ rt.polyOp.ToggleCommandMode ('#CutVertex')
	#~ if rt.Ribbon_Modeling.IsEdgeMode():
		#~ rt.polyOp.ToggleCommandMode ('#CutEdge')
	#~ else:
		#~ rt.polyOp.ToggleCommandMode ('#CutFace')
#~ else:
	#~ rt.polyOp.ToggleCommandMode ('#cut')

#~ rt.toggle



	